#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GW04 A/B harness.

Post-translation harness, constrained by GW04_PREREG:
- A1-A20 and E1-E10 are mechanically transcribed from sealed GW04_WORLD_TEXT.md.
- RULE_TYPE logic is forbidden except exact membership in the six pre-GW04
  generic_evaluator rule-family names.
- Every non-matching type becomes EXECUTOR_HOLE; there is no alias/synonym map.
- RUN A: candidate overlay absent.
- RUN B: same evaluator + same normalized encoder bytes, candidate overlay present.

This file intentionally does NOT implement any of the five new encoder rule types.
"""
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "gw03"))

from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED
from generic_evaluator import Evaluator
from gw04_candidate_overlay import CandidateOverlay


SUPPORTED_RULE_TYPES = frozenset({
    "CARDINALITY_POLICY",
    "DERIVATION",
    "TEMPORAL_POLICY",
    "INGEST_GUARD",
    "CLOSURE_POLICY",
    "INVARIANT",
})

ENCODER_JSON = ROOT / "current/experiments/GW04_ENCODER_OUTPUT.normalized.json"


def add_initial(net, addr, s, p, o):
    r = Record(addr, {
        "SUBJECT": s,
        "PREDICATE": p,
        "OBJECT": o,
        "PROVENANCE": "SRC_INIT",
    })
    net.records[addr] = r
    r.committed = True
    net.mark(addr, "SUPPORTED")
    net.mark(addr, "CURRENT")


def load_world_facts(net):
    rows = [
        ("A1","K1","Q1","N1"), ("A2","K1","Q1","N2"),
        ("A3","K2","Q1","N2"), ("A4","K2","Q1","N3"),
        ("A5","K3","Q1","N2"), ("A6","K3","Q1","N4"),
        ("A7","K4","Q1","N3"), ("A8","K4","Q1","N5"),
        ("A9","K5","Q1","N4"), ("A10","K5","Q1","N5"),
        ("A11","K6","Q1","N5"), ("A12","K6","Q1","N6"),
        ("A13","K1","Q2",10), ("A14","K1","Q4","N2"),
        ("A15","K2","Q2",6), ("A16","K2","Q4","N3"),
        ("A17","K4","Q2",5), ("A18","K4","Q4","N5"),
        ("A19","K6","Q2",10), ("A20","K6","Q4","N6"),
    ]
    for row in rows:
        add_initial(net, *row)


def load_rule_records(net, evaluator):
    data = json.loads(ENCODER_JSON.read_text(encoding="utf-8"))
    holes = []
    passed = []
    for rd in data:
        addr = rd["addr"]
        rtype = rd["RULE_TYPE"]
        if rtype in SUPPORTED_RULE_TYPES:
            evaluator.load_rules([rd])
            passed.append(addr)
        else:
            # Preserve the translated law as inert, addressable data.
            fields = dict(rd)
            fields.pop("addr", None)
            rec = Record(addr, {"TYPE": "RULE", **fields})
            net.records[addr] = rec
            rec.committed = True
            net.mark(addr, "CURRENT")
            holes.append({
                "CLASS": "EXECUTOR_HOLE",
                "RULE": addr,
                "RULE_TYPE": rtype,
                "REASON": "RULE_TYPE not in frozen six-name evaluator vocabulary",
            })
    return passed, holes


def record_sig(r):
    return (
        tuple(sorted((k, repr(v)) for k, v in r.fields.items())),
        tuple((a.state, a.scope, a.time, a.basis, a.seq) for a in r.status_log),
        r.committed,
    )


def snapshot(net):
    return {a: record_sig(r) for a, r in net.records.items()}


def delta(before, net):
    after = snapshot(net)
    created = sorted(a for a in after if a not in before)
    changed = sorted(a for a in after if a in before and after[a] != before[a])
    return created, changed


def stop_dict(s):
    return {
        "WHERE": s.where,
        "WANTED": s.wanted,
        "AVAILABLE": s.available,
        "MISSING": s.missing,
        "STOP_CLASS": s.stop_class,
        "CAN_ASK_OUTSIDE": s.can_ask_outside,
        "QUERY": s.query,
    }


def combine(verdicts):
    # Event-level summary only; individual STOP cards remain authoritative.
    if BLOCK in verdicts:
        return BLOCK
    if ASK in verdicts:
        return ASK
    if NEED in verdicts:
        return NEED
    return GO


def run_event(name, ops, fn, net, log):
    before = snapshot(net)
    stop_n = len(net.stops)
    verdict, note = fn()
    created, changed = delta(before, net)
    new_stops = [stop_dict(s) for s in net.stops[stop_n:]]
    log.append({
        "EVENT": name,
        "OPERATIONS": ops,
        "VERDICT": verdict,
        "NOTE": note,
        "NETWORK_DELTA": {"CREATED": created, "CHANGED": changed},
        "STOPS": new_stops,
        "NEED": [s for s in new_stops if s["STOP_CLASS"] == NEED],
    })


def execute(mode):
    use_candidates = mode == "B"
    net = Network()
    demon = Demon(net)
    overlay = CandidateOverlay(net) if use_candidates else None
    evaluator = Evaluator(net, demon, candidate_overlay=overlay)

    load_world_facts(net)
    passed_rules, executor_holes = load_rule_records(net, evaluator)
    runtime_holes = []
    events = []

    def query(ev, s, p, addr):
        v, vals, prov = evaluator.task_query(ev, s, p, addr)
        return v, f"values={vals}; derivation={prov}"

    run_event("E1", ["READ","MATCH","TASK_QUERY"], lambda: (
        (lambda rs: (combine([x[0] for x in rs]),
                     "Q2=" + rs[0][1] + "; Q4=" + rs[1][1]))([
            query("E1/Q2","K3","Q2","E1_DQ2"),
            query("E1/Q4","K3","Q4","E1_DQ4"),
        ])
    ), net, events)

    run_event("E2", ["READ","MATCH","TASK_QUERY"],
              lambda: query("E2","K5","Q2","E2_DQ2"), net, events)

    def e3():
        r1 = evaluator.ingest("E3/Q2","E3_Q2","K5","Q2",5,"SEN1",1)
        r2 = evaluator.ingest("E3/Q4","E3_Q4","K5","Q4","N5","SEN1",1)
        return combine([r1[0], r2[0]]), f"Q2={r1}; Q4={r2}"
    run_event("E3", ["PROPOSE","CHECK","COMMIT"], e3, net, events)

    def check_rule(evname, rule_addr, subject):
        if any(h["RULE"] == rule_addr for h in executor_holes):
            net.stop(
                f"{evname}/{rule_addr}",
                f"check {rule_addr} at {subject}",
                f"{rule_addr} is addressable but has EXECUTOR_HOLE",
                f"executable handler for rule {rule_addr}",
                NEED,
            )
            return NEED, f"EXECUTOR_HOLE {rule_addr}"
        runtime_holes.append({
            "CLASS":"EXECUTOR_HOLE",
            "TASK":evname,
            "REASON":"no pre-GW04 generic evaluator operation for arbitrary rule-check task",
        })
        net.stop(
            f"{evname}/task",
            f"check rule at {subject}",
            "rule loaded",
            "pre-existing generic rule-check task operator",
            NEED,
        )
        return NEED, "EXECUTOR_HOLE task operator"

    run_event("E4", ["READ","CHECK_RULE"], lambda: check_rule("E4","L2","N3"),
              net, events)

    run_event("E5", ["PROPOSE","CHECK","COMMIT"],
              lambda: evaluator.ingest("E5","E5_Q6","K3","Q6","Z2","TXT1",2),
              net, events)

    def e6():
        runtime_holes.append({
            "CLASS":"EXECUTOR_HOLE",
            "TASK":"E6",
            "REASON":"generic_evaluator has no pre-GW04 aggregate-sum task operator",
        })
        net.stop(
            "E6/task",
            "compute sum of Q2 over all known links",
            "current Q2 records are addressable",
            "pre-existing aggregate-sum task operator",
            NEED,
        )
        return NEED, "EXECUTOR_HOLE aggregate-sum task operator"
    run_event("E6", ["READ","AGGREGATE_SUM"], e6, net, events)

    patterns = [("?X","Q1","N3"), ("?X","Q1","N4")]
    def e7():
        v1 = evaluator.requirement("E7","TASK_E7","RQ_E7",patterns,"E7_RP")
        v2, bound = evaluator.req_bind("E7","RQ_E7",patterns)
        new_asks = [s for s in net.stops if s.stop_class == ASK and s.where.startswith("candidate/requirement/RQ_E7/")]
        return combine([v1, v2] + ([ASK] if new_asks else [])), f"requirement={v1}; bind={v2},{bound}"
    run_event("E7", ["CREATE_ADDRESS","MATCH","LINK","MARK"], e7, net, events)

    def e8():
        r1 = evaluator.ingest("E8/1","E8_Q1A","K7","Q1","N3","TXT2",3)
        r2 = evaluator.ingest("E8/2","E8_Q1B","K7","Q1","N4","TXT2",3)
        return combine([r1[0], r2[0]]), f"first={r1}; second={r2}"
    run_event("E8", ["PROPOSE","CHECK","COMMIT"], e8, net, events)

    def e9():
        r1 = evaluator.ingest("E9/Q2","E9_Q2","K7","Q2",1,"SEN2",4)
        r2 = evaluator.ingest("E9/Q4","E9_Q4","K7","Q4","N4","SEN2",4)
        return combine([r1[0], r2[0]]), f"Q2={r1}; Q4={r2}"
    run_event("E9", ["PROPOSE","CHECK","COMMIT"], e9, net, events)

    run_event("E10", ["READ","CHECK_RULE"],
              lambda: check_rule("E10","L2","N3"), net, events)

    opens = list(evaluator.final_open_registry())
    historical = sorted(
        r.addr for r in net.records.values()
        if any(a.state == "HISTORICAL" for a in r.status_log)
    )
    changed_records = sorted(
        r.addr for r in net.records.values()
        if r.addr not in {f"A{i}" for i in range(1,21)} and not r.addr.startswith("L")
    )

    out = {
        "GW04_RUN": mode,
        "CANDIDATES": use_candidates,
        "ENCODER_INPUT": "current/experiments/GW04_ENCODER_OUTPUT.normalized.json",
        "SUPPORTED_RULE_TYPES": sorted(SUPPORTED_RULE_TYPES),
        "RULES_PASSED_TO_EVALUATOR": passed_rules,
        "EXECUTOR_HOLES": executor_holes + runtime_holes,
        "EVENTS": events,
        "FINAL": {
            "CREATED_OR_CHANGED_NONINITIAL_RECORDS": changed_records,
            "HISTORICAL": historical,
            "OPEN_REGISTRY": opens,
            "STOP_MAP": [stop_dict(s) for s in net.stops],
            "ASK_LIST": [stop_dict(s) for s in net.stops if s.stop_class == ASK],
            "NEED_MAP": [stop_dict(s) for s in net.stops if s.stop_class == NEED],
        },
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", choices=["A","B"], required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    result = execute(args.run)
    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=list) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
