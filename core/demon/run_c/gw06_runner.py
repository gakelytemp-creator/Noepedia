#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GW06 deterministic post-translation exam harness.

Built only from solver-visible GW06_WORLD_TEXT.md and the frozen interfaces at
baseline 83ca690. It contains no answer-book outcomes, expected verdicts,
expected candidate names, or expected registry contents.

Modes:
  baseline  — frozen GW05-style ingest + C1/C3 requirement handling;
  workshop  — baseline + WS01–WS08b mechanisms (admission, ASK resolution,
              per-fact watch, ONE_SHOT mandate, support-derived ASK views).

Cold encoder output and dictionary are explicit CLI inputs. The same translated
rules can therefore be run under both modes.
"""
from pathlib import Path
from dataclasses import asdict, is_dataclass
import argparse, hashlib, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / "core/demon"), str(ROOT / "core/demon/run_c"), str(ROOT / "core/demon/workshop")]

from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED
from family_executor import FamilyExecutor
from c1_c3_overlay import C1C3Overlay
from admission import admit, install_default_policy, PER_RULE_DEBT
from resolution import answer_on_bind, unanswered_ask_stops, effectively_open_asks
import watch as W

BASELINE_COMMIT = "83ca690adf4e55f42edf085a23b27321fa8d1557"
WORLD_SHA256 = "ecf2271147ccce8c0fd4eff1151ee52776740ef92ec3391bda6f819f4b3671d4"


def j(x):
    if is_dataclass(x):
        return j(asdict(x))
    if isinstance(x, Record):
        return {"addr": x.addr, "fields": j(x.fields), "status": [j(s) for s in x.status_log], "committed": x.committed}
    if isinstance(x, dict):
        return {str(k): j(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set)):
        return [j(v) for v in x]
    return x


def stop_dict(s):
    return {"WHERE": s.where, "WANTED": s.wanted, "AVAILABLE": j(s.available), "MISSING": j(s.missing),
            "STOP_CLASS": s.stop_class, "CAN_ASK_OUTSIDE": s.can_ask_outside, "QUERY": s.query}


def snapshot(net):
    return {a: (repr(r.fields), [(s.state, s.scope, s.time, s.basis, s.seq) for s in r.status_log], r.committed)
            for a, r in net.records.items()}


def delta(before, net):
    after = snapshot(net)
    return {"CREATED": sorted(a for a in after if a not in before),
            "CHANGED": sorted(a for a in after if a in before and after[a] != before[a])}


def add_fact(net, addr, s, p, o, source="SRC_INIT", time=None):
    fields = {"SUBJECT": s, "PREDICATE": p, "OBJECT": o, "PROVENANCE": source}
    if time is not None:
        fields["TIME"] = time
    r = Record(addr, fields)
    net.records[addr] = r
    r.committed = True
    net.mark(addr, "SUPPORTED")
    net.mark(addr, "CURRENT")
    return r


def load_initial(net):
    rows = [
        ("J1", "U1", "Y1", "H1"), ("J2", "U2", "Y1", "H1"), ("J3", "U3", "Y1", "H1"),
        ("J4", "U4", "Y1", "H1"), ("J5", "U5", "Y1", "H2"), ("J6", "U6", "Y1", "H2"),
        ("J7", "U7", "Y1", "H3"), ("J8", "H1", "Y3", 20), ("J9", "H2", "Y3", 11),
        ("J10", "U1", "Y2", 6), ("J11", "U2", "Y2", 5), ("J12", "U4", "Y2", 4),
        ("J13", "U5", "Y2", 7), ("J14", "U1", "Y5", "W1"), ("J15", "U1", "Y5", "W2"),
        ("J16", "U2", "Y5", "W3"), ("J17", "U3", "Y5", "W1"), ("J18", "U3", "Y5", "W3"),
        ("J19", "U2", "Y4", "XT1"), ("J20", "U5", "Y6", "XS1"),
        ("J21", "H1", "Y7", 4), ("J22", "H2", "Y7", 3),
    ]
    for row in rows:
        add_fact(net, *row)


def load_rules(net, path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for rd in data:
        fields = dict(rd)
        addr = fields.pop("addr")
        rec = Record(addr, {"TYPE": "RULE", **fields})
        net.records[addr] = rec
        rec.committed = True
        net.mark(addr, "CURRENT")
    return [r["addr"] for r in data]


def rule(net, addr):
    return net.read(addr)


def materialize_signals(net, demon, event_name, result):
    made = []
    for i, o in enumerate(result.opens, 1):
        a = f"OPEN_{event_name}_{i}"
        if net.read(a) is None:
            rec = Record(a, {"TYPE": "OPEN", "ORIGIN": event_name, "DETAILS": j(o)})
            demon.commit(demon.propose(add=[rec], mark=[(a, "OPEN")]))
            made.append(a)
    for i, c in enumerate(result.conflicts, 1):
        a = f"CONFLICT_{event_name}_{i}"
        if net.read(a) is None:
            rec = Record(a, {"TYPE": "CONFLICT", "ORIGIN": event_name, "DETAILS": j(c)})
            demon.commit(demon.propose(add=[rec], mark=[(a, "OPEN")]))
            made.append(a)
    for st in result.stops:
        net.stop(f"{event_name}/handler", event_name, j(st), "handler stop", result.verdict,
                 can_ask=(result.verdict == ASK), query="")
    return made


def commit_markers(net, demon, result):
    made = []
    for rec in result.proposed_delta:
        if isinstance(rec, Record) and net.read(rec.addr) is None:
            demon.commit(demon.propose(add=[rec]))
            made.append(rec.addr)
    return made


def commit_derivation(net, demon, result):
    made = []
    for rec in result.derived_records:
        refs = [Record(f"{rec.addr}_REF{i}", {"SUBJECT": rec.addr, "PREDICATE": "REFERS_TO",
                                              "OBJECT": target, "ROLE": "PREMISE_OR_RULE"})
                for i, target in enumerate(result.provenance_requirements, 1)]
        used_rule = result.provenance_requirements[-1] if result.provenance_requirements else None
        premises = list(result.provenance_requirements[:-1]) if used_rule else []
        derived = [(rec.addr, premises, used_rule)] if used_rule else []
        v, _ = demon.commit(demon.propose(add=[rec] + refs, mark=[(rec.addr, "CURRENT")], derived=derived))
        if v == GO:
            made.append(rec.addr)
    return made


def event(log, net, name, ops, fn):
    before = snapshot(net)
    n = len(net.stops)
    verdict, note = fn()
    log.append({"EVENT": name, "OPERATIONS": ops, "VERDICT": verdict, "NOTE": j(note),
                "NETWORK_DELTA": delta(before, net),
                "STOPS": [stop_dict(s) for s in net.stops[n:]],
                "NEED": [stop_dict(s) for s in net.stops[n:] if s.stop_class == NEED]})


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def execute(encoder_output, dictionary_path, mode):
    workshop = mode == "workshop"
    net = Network()
    demon = Demon(net)
    dictionary = json.loads(Path(dictionary_path).read_text(encoding="utf-8"))
    ex = FamilyExecutor(dictionary)
    c13 = C1C3Overlay(net)
    load_initial(net)
    rules = load_rules(net, encoder_output)
    if workshop:
        install_default_policy(net, demon, debt_shape=PER_RULE_DEBT)
    events = []

    def unique_scope(subject):
        rs = [r for r in net.records.values()
              if r.f("SUBJECT") == subject and r.f("PREDICATE") == "Y1"
              and r.status_log and r.status_log[-1].state == "CURRENT"]
        vals = sorted({r.f("OBJECT") for r in rs}, key=repr)
        return vals[0] if len(vals) == 1 else None

    def require_rule(ev, addr, wanted):
        r = rule(net, addr)
        if r is not None:
            return r
        net.stop(f"{ev}/rule", wanted, {"RULE_ADDR": addr}, "RULE_ABSENT", NEED)
        return None

    def derive_y2(ev, subject):
        scope = unique_scope(subject)
        if scope is None:
            net.stop(f"{ev}/scope", f"determine Y2 of {subject}", "current Y1 records",
                     "unique current Y1 target", NEED)
            return NEED, {"SCOPE": None}
        r = require_rule(ev, "YL3", f"determine Y2 of {subject}")
        if r is None:
            return NEED, {"SCOPE": scope, "RULE": "YL3", "CLASS": "RULE_ABSENT"}
        res = ex.execute(r, net, {"OP": "DERIVE", "SCOPE": scope,
                                  "SUBJECT": subject, "PREDICATE": "Y2",
                                  "DERIVED_ADDR": f"{ev}_DERIVED"})
        commit_markers(net, demon, res)
        materialize_signals(net, demon, ev, res)
        committed = commit_derivation(net, demon, res)
        if res.verdict != GO:
            net.stop(f"{ev}/derive", f"determine Y2 of {subject}", j(res.details),
                     res.classification or "executable derivation", NEED)
        return res.verdict, {"SCOPE": scope, "HANDLER_RESULT": j(res), "COMMITTED_DERIVED": committed}

    def check_rule(ev, rule_addr, subject=None):
        r = require_rule(ev, rule_addr, f"check {rule_addr}" + (f" for {subject}" if subject is not None else ""))
        if r is None:
            return NEED, {"RULE": rule_addr, "CLASS": "RULE_ABSENT"}
        req = {"OP": "CHECK"}
        if subject is not None:
            req["SUBJECT"] = subject
        res = ex.execute(r, net, req)
        commit_markers(net, demon, res)
        materialize_signals(net, demon, ev, res)
        return res.verdict, {"HANDLER_RESULT": j(res)}

    def current_bindings(rq):
        return sorted(r.addr for r in net.records.values()
                      if r.f("SUBJECT") == rq and r.f("ROLE") == "BOUND_CANDIDATE")

    def reconcile_bindings(rq):
        out = []
        if not workshop:
            return out
        for b in current_bindings(rq):
            if W.binding_state(net, b) == "REVIEW_REQUIRED":
                r = W.on_basis_lost(net, demon, rq, b)
                if r is not None:
                    out.append({"BIND": b, "ACTION": r})
        return out

    def watch_step(rq="RQ_X7"):
        w = W.watch_requirement(net, demon, c13, rq)
        out = {"WATCH": w}
        m = W.current_mandate(net, "TASK_X7")
        cands = W.current_candidacies(net, rq)
        if m and cands and W._latest(net, rq) != "BOUND":
            b = W.bind(net, demon, rq, cands[0], authorized_by=m, bind_addr="RQ_X7_BIND_AUTO")
            out["AUTO_BIND"] = {"BIND": b, "MANDATE": m}
            if b:
                out["ASKS_ANSWERED"] = answer_on_bind(net, demon, rq, b)
        out["REVALIDATED_BINDINGS"] = reconcile_bindings(rq)
        return out

    def ingest(ev, rows):
        results, verdicts, watches = [], [], []
        for idx, (s, p, o, source, time) in enumerate(rows, 1):
            incoming = Record(f"{ev}_IN_{idx}", {"SUBJECT": s, "PREDICATE": p, "OBJECT": o,
                                                  "TYPE": "OBSERVATION", "SOURCE": source, "TIME": time})
            vr = ex.validate_incoming(net, incoming, marker_prefix=f"{ev}_UNCHECKED_{idx}")
            if workshop:
                adm = admit(net, demon, incoming, vr, prefix=f"{ev}_{idx}")
                committed = adm.fact_committed
                verdicts.append(adm.verdict)
                if adm.verdict != GO:
                    net.stop(f"{ev}/{idx}", f"admit incoming ({s} {p} {o})", j(adm.evidence), adm.reason, adm.verdict)
            else:
                commit_markers(net, demon, vr)
                materialize_signals(net, demon, f"{ev}_{idx}", vr)
                adm = None
                committed = False
                if vr.verdict == GO:
                    v, _ = demon.commit(demon.propose(add=[incoming], mark=[(incoming.addr, "CURRENT")]))
                    committed = v == GO
                    verdicts.append(v)
                else:
                    net.stop(f"{ev}/{idx}", f"validate incoming ({s} {p} {o})", j(vr.details),
                             j(vr.unchecked_dependencies), vr.verdict)
                    verdicts.append(vr.verdict)
            if committed:
                c13.resolve_from_fact(incoming)
                if workshop and net.read("RQ_X7") is not None:
                    watches.append(watch_step())
            results.append({"VALIDATION": j(vr), "COMMITTED": committed,
                            "ADMISSION": None if adm is None else {"VERDICT": adm.verdict, "REASON": adm.reason,
                                "EVIDENCE": j(adm.evidence), "RECORDS": adm.records, "POLICY": adm.policy}})
        verdict = BLOCK if BLOCK in verdicts else NEED if NEED in verdicts else ASK if ASK in verdicts else GO
        return verdict, {"ROWS": results, "WATCH_PER_COMMIT": watches}

    def registry():
        opens = set(c13.current_open_registry())
        if workshop:
            opens |= set(effectively_open_asks(net))
        signals = sorted(r.addr for r in net.records.values()
                         if r.f("TYPE") in ("CONFLICT", "CHECK_STATUS", "UNEXECUTABLE_RULE_DEBT")
                         and r.status_log and r.status_log[-1].state == "OPEN")
        asks = ([stop_dict(s) for s in unanswered_ask_stops(net)] if workshop
                else [stop_dict(s) for s in net.stops if s.stop_class == ASK])
        needs = [stop_dict(s) for s in net.stops if s.stop_class == NEED]
        return GO, {"OPEN_REGISTRY": sorted(opens), "OPEN_SIGNALS": signals,
                    "ASK_UNANSWERED": asks, "NEED": needs}

    event(events, net, "X1", ["READ", "MATCH", "DERIVE"], lambda: derive_y2("X1", "U3"))
    event(events, net, "X2", ["READ", "MATCH", "DERIVE"], lambda: derive_y2("X2", "U6"))
    event(events, net, "X3", ["READ", "CHECK"], lambda: check_rule("X3", "YL2", "U2"))
    event(events, net, "X4", ["PROPOSE", "CHECK", "COMMIT"],
          lambda: ingest("X4", [("U2", "Y6", "XS2", "SRC1", "t1")]))
    event(events, net, "X5", ["PROPOSE", "CHECK", "COMMIT"],
          lambda: ingest("X5", [("U7", "Y2", 9, "SRC2", "t2")]))

    def x6():
        net.stop("X6/task", "determine which hub has the most units", "current records are addressable",
                 "frozen aggregate-max task operator", NEED)
        return NEED, {"CLASS": "EXECUTOR_HOLE", "REASON": "no frozen aggregate-max task operator"}
    event(events, net, "X6", ["READ", "AGGREGATE_MAX"], x6)

    patterns = [("?X", "Y5", "W2"), ("?X", "Y5", "W3")]
    def x7():
        paddrs = []
        for i, (s, p, o) in enumerate(patterns, 1):
            a = f"X7_PAT{i}"
            paddrs.append(a)
            demon.commit(demon.propose(add=[Record(a, {"TYPE": "TRIPLET_PATTERN", "SUBJECT": s,
                                                        "PREDICATE": p, "OBJECT": o})]))
        demon.commit(demon.propose(add=[Record("TASK_X7", {"TYPE": "TASK", "REQUIRED_PATTERNS": paddrs})]))
        rq = Record("RQ_X7", {"TYPE": "REQUIREMENT_CONCEPT", "REQUIREMENT": paddrs})
        v, _ = demon.commit(demon.propose(add=[rq], mark=[("RQ_X7", "OPEN")], authorized_by="TASK_X7"))
        note = {"RQ_COMMIT": v}
        if workshop:
            note["MANDATE"] = W.issue_mandate(net, demon, "MANDATE_X7", "TASK_X7", issuer="REQUESTER",
                                                lifecycle=W.ONE_SHOT)
        out = c13.requirement_ask("RQ_X7")
        c13.materialize_ask_opens()
        note["C1"] = j(out)
        return (ASK if out.created_asks else v), note
    event(events, net, "X7", ["CREATE_ADDRESS", "MATCH", "LINK", "MARK"], x7)

    event(events, net, "X8", ["PROPOSE", "CHECK", "COMMIT"],
          lambda: ingest("X8", [("U8", "Y1", "H2", "SRC3", "t3"), ("U8", "Y2", 4, "SRC3", "t3")]))
    event(events, net, "X9", ["PROPOSE", "CHECK", "COMMIT"],
          lambda: ingest("X9", [("U9", "Y5", "W2", "SRC4", "t4"), ("U9", "Y5", "W3", "SRC4", "t4")]))
    event(events, net, "X10", ["READ", "OPEN_REGISTRY"], registry)
    event(events, net, "X11", ["PROPOSE", "CHECK", "COMMIT"],
          lambda: ingest("X11", [("U10", "Y5", "W2", "SRC5", "t5"), ("U10", "Y5", "W3", "SRC5", "t5")]))

    def x12():
        matches = [r for r in net.records.values()
                   if r.f("SUBJECT") == "U10" and r.f("PREDICATE") == "Y5" and r.f("OBJECT") == "W3"
                   and r.status_log and r.status_log[-1].state == "CURRENT"]
        if len(matches) != 1:
            net.stop("X12/retraction", "retract U10 Y5 W3", [r.addr for r in matches],
                     "exactly one current matching record", NEED)
            return NEED, {"MATCHES": [r.addr for r in matches]}
        target = matches[0].addr
        v, _ = demon.commit(demon.propose(mark=[(target, "HISTORICAL", None, None, "SRC6 retraction at t6")]))
        note = {"RETRACTED": target, "COMMIT": v}
        if workshop:
            note["WATCH"] = watch_step()
        return v, note
    event(events, net, "X12", ["READ", "MARK", "WATCH"], x12)

    def x13():
        if workshop:
            supported = [b for b in current_bindings("RQ_X7") if W.binding_state(net, b) == "SUPPORTED"]
            if supported and W._latest(net, "RQ_X7") == "BOUND":
                return GO, {"ALREADY_BOUND": supported, "BINDING_STATE": "SUPPORTED"}
            cands = W.current_candidacies(net, "RQ_X7")
            if cands:
                b = W.bind(net, demon, "RQ_X7", cands[0], authorized_by="TASK_X7", bind_addr="RQ_X7_BIND_X13")
                note = {"BIND": b, "BASIS": cands[0], "AUTHORIZED_BY": "TASK_X7"}
                if b:
                    note["ASKS_ANSWERED"] = answer_on_bind(net, demon, "RQ_X7", b)
                    return GO, note
            out = c13.requirement_ask("RQ_X7")
            c13.materialize_ask_opens()
            return ASK, {"CANDIDACIES": cands, "C1": j(out)}
        branches = c13.joint_bindings(patterns)
        candidates = []
        for b, _ in branches:
            x = b.get("?X")
            if x not in candidates:
                candidates.append(x)
        if len(candidates) == 1:
            edge = Record("RQ_X7_BIND_X13", {"SUBJECT": "RQ_X7", "PREDICATE": "REFERS_TO",
                                              "OBJECT": candidates[0], "ROLE": "BOUND_CANDIDATE"})
            v, _ = demon.commit(demon.propose(add=[edge], mark=[("RQ_X7", "BOUND")]))
            return v, {"CANDIDATES": candidates, "BOUND": candidates[0]}
        out = c13.requirement_ask("RQ_X7")
        c13.materialize_ask_opens()
        return (ASK if candidates or out.created_asks else NEED), {"CANDIDATES": candidates, "C1": j(out)}
    event(events, net, "X13", ["READ", "MATCH", "LINK", "MARK"], x13)
    event(events, net, "X14", ["READ", "OPEN_REGISTRY"], registry)

    return {
        "GW06": True,
        "BASELINE_COMMIT": BASELINE_COMMIT,
        "WORLD_SHA256": WORLD_SHA256,
        "MODE": mode,
        "ENCODER_OUTPUT": str(Path(encoder_output)),
        "ENCODER_SHA256": sha256_file(encoder_output),
        "DICTIONARY": str(Path(dictionary_path)),
        "DICTIONARY_SHA256": sha256_file(dictionary_path),
        "RULES": rules,
        "EVENTS": events,
        "FINAL": registry()[1],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoder-output", required=True, help="cold N or L translation JSON")
    ap.add_argument("--dictionary", required=True, help="frozen V0.3 dictionary JSON")
    ap.add_argument("--mode", choices=["baseline", "workshop"], required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = execute(a.encoder_output, a.dictionary, a.mode)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
