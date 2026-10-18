#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
candidate_overlay.py — GW04 candidate mechanisms frozen before cold translation.

Source of requirements: current/experiments/GW02_VS_ANSWER_BOOK.md only.

This module is intentionally content-blind and fail-closed.  It does not infer
whether an OPEN is externally resolvable from prose.  OPEN→ASK promotion is
allowed only when the OPEN itself carries explicit machine-readable resolution
metadata.  Requirement ASK generation similarly delegates "is this pattern
already supported?" to the evaluator/runner that owns pattern semantics.

Candidates:
  C1 requirement concept -> ASK for each unsupported explicit requirement pattern
  C2 unresolved OPEN -> ASK only when exactly one external fact is explicitly declared
  C3 final OPEN registry includes every unresolved explicit OPEN and materializes
     unresolved ASK stops as addressable OPEN records
"""

from dataclasses import dataclass
from typing import Callable, Iterable
import os
import sys

try:
    from demon_core import Record, ASK
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from demon_core import Record, ASK


@dataclass(frozen=True)
class CandidateResult:
    created_asks: tuple[str, ...] = ()
    created_opens: tuple[str, ...] = ()


class CandidateOverlay:
    def __init__(self, net):
        self.net = net

    def _current_open(self, rec):
        return (
            rec.f("TYPE") == "OPEN"
            and rec.status_log
            and rec.status_log[-1].state == "OPEN"
        )

    def _ask_exists(self, where, query):
        return any(
            s.stop_class == ASK and s.where == where and s.query == query
            for s in self.net.stops
        )

    def _triplet_query(self, pat):
        """No semantic interpretation: expose the explicit requirement pattern."""
        s, p, o = pat.f("SUBJECT"), pat.f("PREDICATE"), pat.f("OBJECT")
        if s is None or p is None or o is None:
            return ""
        return f"resolve ({s} {p} {o})"

    # C1
    def requirement_asks(
        self,
        rq_addr: str,
        pattern_supported: Callable[[object], bool],
    ) -> CandidateResult:
        rq = self.net.read(rq_addr)
        if rq is None or rq.f("TYPE") != "REQUIREMENT_CONCEPT":
            return CandidateResult()

        made = []
        for paddr in rq.f("REQUIREMENT", []) or []:
            pat = self.net.read(paddr)
            if pat is None or pat.f("TYPE") != "TRIPLET_PATTERN":
                continue
            if pattern_supported(pat):
                continue
            query = self._triplet_query(pat)
            if not query:
                continue
            where = f"candidate/requirement/{rq_addr}/{paddr}"
            if self._ask_exists(where, query):
                continue
            self.net.stop(
                where=where,
                wanted=f"support for requirement pattern {paddr}",
                available=f"requirement pattern {paddr} is explicit but unsupported",
                missing="external fact supporting or excluding this pattern",
                stop_class=ASK,
                can_ask=True,
                query=query,
            )
            made.append(where)
        return CandidateResult(created_asks=tuple(made))

    # C2
    def promote_resolvable_opens(self) -> CandidateResult:
        """
        Promotion is deliberately structural, not heuristic.

        Required OPEN fields:
          RESOLUTION_KIND = "EXTERNAL_FACT"
          RESOLUTION_FACT_COUNT = 1
          RESOLUTION_QUERY = non-empty string

        If these fields are absent, the OPEN stays OPEN/NEED.  This preserves the
        negative control and prevents "ask about everything".
        """
        made = []
        for rec in list(self.net.records.values()):
            if not self._current_open(rec):
                continue
            if rec.f("RESOLUTION_KIND") != "EXTERNAL_FACT":
                continue
            if rec.f("RESOLUTION_FACT_COUNT") != 1:
                continue
            query = rec.f("RESOLUTION_QUERY")
            if not isinstance(query, str) or not query.strip():
                continue
            where = f"candidate/open/{rec.addr}"
            if self._ask_exists(where, query):
                continue
            self.net.stop(
                where=where,
                wanted=f"resolve OPEN {rec.addr}",
                available=f"OPEN {rec.addr} declares one external-fact resolution",
                missing="the declared external fact",
                stop_class=ASK,
                can_ask=True,
                query=query,
            )
            made.append(where)
        return CandidateResult(created_asks=tuple(made))

    # C3
    def materialize_ask_opens(self) -> CandidateResult:
        """
        ASK is unresolved knowledge state too.  Make each unresolved ASK
        addressable in the OPEN registry without deleting the STOP card.
        """
        made = []
        for idx, stop in enumerate(self.net.stops, 1):
            if stop.stop_class != ASK:
                continue
            addr = f"OPEN_ASK_{idx}"
            if self.net.read(addr) is not None:
                continue
            rec = Record(addr, {
                "TYPE": "OPEN",
                "OPEN_KIND": "ASK",
                "ORIGIN_WHERE": stop.where,
                "QUERY": stop.query,
            })
            self.net.records[addr] = rec
            rec.committed = True
            self.net.mark(addr, "OPEN")
            made.append(addr)
        return CandidateResult(created_opens=tuple(made))

    def final_open_registry(self) -> tuple[str, ...]:
        self.materialize_ask_opens()
        return tuple(sorted(
            r.addr for r in self.net.records.values() if self._current_open(r)
        ))

    def apply(
        self,
        requirements: Iterable[tuple[str, Callable[[object], bool]]] = (),
    ) -> CandidateResult:
        asks, opens = [], []
        for rq_addr, supported in requirements:
            out = self.requirement_asks(rq_addr, supported)
            asks.extend(out.created_asks)
        out = self.promote_resolvable_opens()
        asks.extend(out.created_asks)
        out = self.materialize_ask_opens()
        opens.extend(out.created_opens)
        return CandidateResult(tuple(asks), tuple(opens))
