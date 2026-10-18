#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C1/C3 candidate overlay frozen before GW05 translation.

Specification source: GW04 post-unseal audit only.

C1: one binding must satisfy all requirement patterns jointly.
C3: current OPEN registry is status-based; machine-readable answers cause a
    non-destructive RESOLVED status transition.
"""
from dataclasses import dataclass
from typing import Iterable

try:
    from demon_core import Record, ASK
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from demon_core import Record, ASK


def is_var(value):
    return isinstance(value, str) and value.startswith("?")


@dataclass(frozen=True)
class CandidateResult:
    created_asks: tuple[str, ...] = ()
    created_opens: tuple[str, ...] = ()
    resolved_opens: tuple[str, ...] = ()


class C1C3Overlay:
    def __init__(self, net):
        self.net = net

    def _current_facts(self):
        return [
            r for r in self.net.records.values()
            if r.f("PREDICATE") not in (None, "REFERS_TO")
            and r.status_log
            and r.status_log[-1].state == "CURRENT"
        ]

    def _unify(self, pattern, record, binding):
        out = dict(binding)
        for key, term in zip(("SUBJECT", "PREDICATE", "OBJECT"), pattern):
            value = record.f(key)
            if is_var(term):
                if term in out and out[term] != value:
                    return None
                out[term] = value
            elif term != value:
                return None
        return out

    def joint_bindings(self, patterns: Iterable[tuple]):
        branches = [({}, [])]
        facts = self._current_facts()
        for pattern in patterns:
            next_branches = []
            for binding, records in branches:
                for rec in facts:
                    new_binding = self._unify(pattern, rec, binding)
                    if new_binding is not None:
                        next_branches.append((new_binding, records + [rec]))
            branches = next_branches
            if not branches:
                break
        return branches

    def _requirement_patterns(self, rq):
        patterns = []
        for paddr in rq.f("REQUIREMENT", []) or []:
            pat = self.net.read(paddr)
            if pat is None or pat.f("TYPE") != "TRIPLET_PATTERN":
                continue
            patterns.append((
                pat.f("SUBJECT"),
                pat.f("PREDICATE"),
                pat.f("OBJECT"),
            ))
        return patterns

    def requirement_joint_supported(self, rq_addr):
        rq = self.net.read(rq_addr)
        if rq is None or rq.f("TYPE") != "REQUIREMENT_CONCEPT":
            return False
        patterns = self._requirement_patterns(rq)
        return bool(patterns) and bool(self.joint_bindings(patterns))

    def requirement_ask(self, rq_addr):
        rq = self.net.read(rq_addr)
        if rq is None or rq.f("TYPE") != "REQUIREMENT_CONCEPT":
            return CandidateResult()

        patterns = self._requirement_patterns(rq)
        if not patterns or self.joint_bindings(patterns):
            return CandidateResult()

        where = f"candidate/joint-requirement/{rq_addr}"
        if any(s.stop_class == ASK and s.where == where for s in self.net.stops):
            return CandidateResult()

        query = "resolve jointly: " + " AND ".join(
            f"({s} {p} {o})" for s, p, o in patterns
        )
        self.net.stop(
            where=where,
            wanted=f"one binding satisfying all patterns of {rq_addr}",
            available="each requirement pattern is explicit; no joint binding is current",
            missing=tuple(patterns),
            stop_class=ASK,
            can_ask=True,
            query=query,
        )
        return CandidateResult(created_asks=(where,))

    def _latest_open(self, rec):
        return bool(rec.status_log and rec.status_log[-1].state == "OPEN")

    def materialize_ask_opens(self):
        made = []
        for idx, stop in enumerate(self.net.stops, 1):
            if stop.stop_class != ASK:
                continue
            addr = f"OPEN_ASK_{idx}"
            if self.net.read(addr) is not None:
                continue
            fields = {
                "TYPE": "OPEN",
                "OPEN_KIND": "ASK",
                "ORIGIN_WHERE": stop.where,
                "QUERY": stop.query,
            }
            missing = stop.missing
            if isinstance(missing, (tuple, list)) and len(missing) == 3:
                fields["RESOLUTION_PATTERN"] = tuple(missing)
            rec = Record(addr, fields)
            self.net.records[addr] = rec
            rec.committed = True
            self.net.mark(addr, "OPEN")
            made.append(addr)
        return CandidateResult(created_opens=tuple(made))

    def _fact_matches_pattern(self, fact, pattern):
        return self._unify(tuple(pattern), fact, {}) is not None

    def resolve_from_fact(self, fact):
        resolved = []
        for rec in self.net.records.values():
            if not self._latest_open(rec):
                continue
            pattern = rec.f("RESOLUTION_PATTERN")
            if not isinstance(pattern, (tuple, list)) or len(pattern) != 3:
                continue
            if self._fact_matches_pattern(fact, pattern):
                self.net.mark(rec.addr, "RESOLVED")
                resolved.append(rec.addr)
        return CandidateResult(resolved_opens=tuple(resolved))

    def current_open_registry(self):
        self.materialize_ask_opens()
        return tuple(sorted(
            rec.addr
            for rec in self.net.records.values()
            if self._latest_open(rec)
        ))
