#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WORKSHOP — evidence composition and admission policy (ATTIC 01 A3.1, A3.4, A3.5).

Status: workshop code. "Works on scene S", not a demonstration claim.

The frozen GW05 executor (run_c/family_executor.py) is NOT modified. This module
post-processes the HandlerResult that its validate_incoming() returns.

Pipeline (A3.4):
    handler evidence -> evidence composition -> materialization
                     -> admission policy -> commit verdict

Principle (A3.1): the signal is recorded; the fact enters with a status.
  * D1 fix: a handler BLOCK with conflicts is materialized as an addressable
    CONFLICT record that refers to the incoming fact, the rule and the existing
    records it clashes with. It can no longer be swallowed.
  * D2 fix: an UNCHECKED dependency no longer vetoes ingest. The fact is
    committed, the UNCHECKED marker is committed and linked to the fact, so the
    debt is visible on the record that depends on the unexecutable law (A6.8).

Invariant (A3.2): the admission verdict may be GO only if every negative
signal in the evidence has a committed record. Otherwise the admission refuses.

The admission policy itself is an addressable network record (A3.5), read by
the admitter, not a constant in code.
"""
from dataclasses import dataclass, field

from demon_core import Record, GO, BLOCK, NEED

POLICY_ADDR = "ADMISSION_POLICY_1"
ADMIT_WITH_RECORD = "ADMIT_WITH_RECORD"
REFUSE = "REFUSE"
# WS04 — shape of UNCHECKED debt (A6.8):
PER_RULE_DEBT = "PER_RULE_DEBT"        # one debt record per unexecutable rule + per-fact DEPENDS_ON edges
PER_FACT_MARKER = "PER_FACT_MARKER"    # WS01-WS03 shape: one OPEN marker per (fact x rule)


def install_default_policy(net, demon, addr=POLICY_ADDR, debt_shape=PER_RULE_DEBT):
    """Commit the workshop default policy as an ordinary network record."""
    if net.read(addr) is not None:
        return addr
    rec = Record(addr, {
        "TYPE": "ADMISSION_POLICY",
        "ON_CONFLICT": ADMIT_WITH_RECORD,
        "ON_UNCHECKED": ADMIT_WITH_RECORD,
        "UNCHECKED_SHAPE": debt_shape,
    })
    demon.commit(demon.propose(add=[rec], mark=[(addr, "CURRENT")]))
    return addr


def read_policy(net, addr=POLICY_ADDR):
    rec = net.read(addr)
    if rec is None or rec.f("TYPE") != "ADMISSION_POLICY":
        raise LookupError(f"no admission policy at {addr}")
    return {"ON_CONFLICT": rec.f("ON_CONFLICT"), "ON_UNCHECKED": rec.f("ON_UNCHECKED"),
            "UNCHECKED_SHAPE": rec.f("UNCHECKED_SHAPE", PER_FACT_MARKER), "ADDR": addr}


def debt_addr(rule):
    """Content-addressed (A1.3): the same rule always maps to the same debt record."""
    return f"DEBT_{rule}"


def _materialize_rule_debt(net, demon, incoming, e, policy):
    """One OPEN debt per rule; the fact gets a DEPENDS_ON edge naming its own check."""
    d = debt_addr(e["RULE"])
    add, mark = [], []
    if net.read(d) is None:
        add.append(Record(d, {"TYPE": "UNEXECUTABLE_RULE_DEBT", "RULE": e["RULE"],
                              "MEANING": "this rule could not perform some checks; see DEPENDS_ON edges",
                              "POLICY": policy["ADDR"]}))
        mark.append((d, "OPEN"))
    edge = f"{incoming.addr}_DEPENDS_ON_{d}"
    if net.read(edge) is None:
        add.append(Record(edge, {"SUBJECT": incoming.addr, "PREDICATE": "DEPENDS_ON", "OBJECT": d,
                                 "ROLE": "UNCHECKED_CHECK", "CHECK": "VALIDATE_INCOMING",
                                 "RULE": e["RULE"], "REASON": e["DETAILS"]["reason"]}))
        mark.append((edge, "UNCHECKED"))     # per-edge state: re-checkable later, not OPEN
    if add:
        v, _ = demon.commit(demon.propose(add=add, mark=mark))
        if v != GO:
            return None
    return edge


def debts_of(net, fact_addr):
    """Fact -> debt view: every rule debt this fact's checks depend on."""
    return sorted(r.f("OBJECT") for r in net.records.values()
                  if r.f("SUBJECT") == fact_addr and r.f("PREDICATE") == "DEPENDS_ON")


def dependents_of(net, debt):
    """Debt -> facts view (for re-checking only the affected edges when the rule is fixed)."""
    return sorted(r.f("SUBJECT") for r in net.records.values()
                  if r.f("OBJECT") == debt and r.f("PREDICATE") == "DEPENDS_ON")


# ── 1. composition: turn raw handler output into a flat evidence list ──
def compose_evidence(validation):
    """validation: HandlerResult from FamilyExecutor.validate_incoming()."""
    ev = []
    for item in validation.details.get("rule_results", []):
        res = item["result"]
        if res.verdict == BLOCK or res.conflicts:
            for c in (res.conflicts or [{"rule": item["rule"]}]):
                ev.append({"KIND": "CONFLICT", "RULE": item["rule"], "DETAILS": c})
        # D3 (WS02): a dependent rule that cannot perform the check is UNCHECKED,
        # not silence. Only the "operation not supported" stop qualifies; other
        # NEEDs (e.g. missing data) are not a statement about checkability.
        elif res.verdict == NEED and any(
                str(s.get("missing", "")).startswith("operation ") for s in res.stops):
            ev.append({"KIND": "UNCHECKED", "RULE": item["rule"],
                       "DETAILS": {"reason": "OPERATION_UNSUPPORTED",
                                   "missing": [s["missing"] for s in res.stops]}})
    for dep in validation.unchecked_dependencies:
        ev.append({"KIND": "UNCHECKED", "RULE": dep["dependency"], "DETAILS": {"reason": dep["reason"]}})
    return ev


def _clashing_records(net, details):
    """Existing current records named by a conflict (subject + current_objects/values)."""
    subj = details.get("subject")
    objs = details.get("current_objects") or details.get("values") or []
    out = []
    for r in net.records.values():
        if r.f("SUBJECT") == subj and r.f("OBJECT") in objs and r.status_log \
                and r.status_log[-1].state == "CURRENT":
            out.append(r.addr)
    return sorted(out)


# ── 2+3+4. materialize, apply policy, commit ──
@dataclass
class Admission:
    verdict: str
    fact_committed: bool
    evidence: list
    records: list = field(default_factory=list)   # addresses of materialized signal records
    policy: dict = field(default_factory=dict)
    reason: str = ""


def admit(net, demon, incoming, validation, prefix, policy_addr=POLICY_ADDR):
    policy = read_policy(net, policy_addr)
    evidence = compose_evidence(validation)

    refuse = [e for e in evidence
              if (e["KIND"] == "CONFLICT" and policy["ON_CONFLICT"] == REFUSE)
              or (e["KIND"] == "UNCHECKED" and policy["ON_UNCHECKED"] == REFUSE)]

    fact_committed = False
    if not refuse:
        v, _ = demon.commit(demon.propose(add=[incoming], mark=[(incoming.addr, "CURRENT")]))
        fact_committed = (v == GO)

    made = []
    for i, e in enumerate(evidence, 1):
        a = f"{prefix}_{e['KIND']}_{i}"
        if e["KIND"] == "CONFLICT":
            parties = [incoming.addr] + _clashing_records(net, e["DETAILS"])
            rec = Record(a, {"TYPE": "CONFLICT", "RULE": e["RULE"], "PARTIES": parties,
                             "DETAILS": e["DETAILS"], "POLICY": policy["ADDR"]})
            edges = [Record(f"{a}_REF{k}", {"SUBJECT": a, "PREDICATE": "REFERS_TO",
                                            "OBJECT": p, "ROLE": "CONFLICT_PARTY"})
                     for k, p in enumerate(parties, 1)]
            edges.append(Record(f"{a}_RULE", {"SUBJECT": a, "PREDICATE": "REFERS_TO",
                                              "OBJECT": e["RULE"], "ROLE": "VIOLATED_RULE"}))
            state = "OPEN"
        elif policy["UNCHECKED_SHAPE"] == PER_RULE_DEBT:
            got = _materialize_rule_debt(net, demon, incoming, e, policy)
            if got is not None:
                made.append(got)
            continue
        else:
            rec = Record(a, {"TYPE": "CHECK_STATUS", "STATUS": "UNCHECKED",
                             "DEPENDENCY": e["RULE"], "REASON": e["DETAILS"]["reason"],
                             "CHECKED_RECORD": incoming.addr, "POLICY": policy["ADDR"]})
            edges = [Record(f"{a}_REF1", {"SUBJECT": a, "PREDICATE": "REFERS_TO",
                                          "OBJECT": incoming.addr, "ROLE": "UNCHECKED_RECORD"})]
            state = "OPEN"
        v, _ = demon.commit(demon.propose(add=[rec] + edges, mark=[(a, state)]))
        if v == GO:
            made.append(a)

    # invariant A3.2: no negative signal without a committed record
    recorded = len(made) == len(evidence)
    if refuse:
        verdict, reason = BLOCK, "policy REFUSE on " + ",".join(sorted({e["KIND"] for e in refuse}))
    elif not recorded:
        verdict, reason = BLOCK, "invariant: evidence not fully materialized"
    elif not fact_committed:
        verdict, reason = BLOCK, "membrane refused the fact"
    else:
        verdict, reason = GO, "admitted with status" if evidence else "admitted clean"
    return Admission(verdict, fact_committed, evidence, made, policy, reason)
