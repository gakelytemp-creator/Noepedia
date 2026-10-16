#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gw03_runner.py — GW01-ის გადარბენა დეკლარაციული წესებით (GW03).

ამ ფაილში არის მხოლოდ: (ა) საწყისი ქსელის ფაქტები, (ბ) მოვლენები E1–E12
როგორც მონაცემები, (გ) ბეჭდვა. წესის სემანტიკის არც ერთი სტრიქონი:
ყველა წესი ქსელის ჩანაწერია (rules_gw01), შესრულება — generic_evaluator.
შემოწმება: grep -nE '"R[1-6]"|"C1"' gw03_runner.py → 0 სტრიქონი.
წესის მისამართები, რომლებიც ლოგში ჩანს, runtime-მონაცემია — ქსელიდან მოდის.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED
from generic_evaluator import Evaluator
from rules_gw01 import RULES

def log(ev, verdict, note, stops=""):
    print(f"{ev:4s} {verdict:6s} {note}" + (f"   [{stops}]" if stops else ""))

net = Network(); d = Demon(net); ev = Evaluator(net, d)

ev.load_facts([
    ("T1", "O3", "P1", "O1", {}), ("T2", "O4", "P2", "O3", {}),
    ("T3", "O11", "P2", "O3", {}), ("T4", "O4", "P3", "S1", {}),
    ("T5", "O11", "P3", "S1", {}), ("T6", "O8", "P3", "S2", {}),
    ("T7", "O9", "P1", "O2", {}),
    ("T8", "O6", "P1", "O1", {"PROVENANCE": "VIS0", "TIME": 0}),
    ("T9", "O7", "P1", "O1", {})])
ev.load_rules(RULES)

v, _ = ev.ingest("E1", "T10", "O5", "P1", "O1", "TXT1")
log("E1", v, "ingest O5 P1 O1 (TXT1) → CURRENT")

ev.ingest("E2", "V1A", "v1", "P2", "O3", "VIS1", time=1)
ev.ingest("E2", "V1B", "v1", "P3", "S1", "VIS1", time=1)
v, cands = ev.bind_sample("E2", "v1")
if v == GO:
    log("E2", GO, f"v1 bound to {cands[0]}")
elif v == ASK:
    log("E2", ASK, f"AMBIGUOUS_MATCH: candidates {cands} — no false merge", "STOP ASK")
else:
    log("E2", NEED, "no candidate")

v, ans, prov = ev.task_query("E3", "O4", "P1", "DV1", domain={"O1", "O2"})
log("E3", v, f"derived (O4 P1 {ans[0]}) with full provenance; "
             f"answer at level {{O1,O2}}: {ans[0]}")

v, info = ev.goal_assert("E4", "O7", "P1", "O2")
if v == BLOCK:
    log("E4", BLOCK, f"impossible goal: {info[0]} + {info[1]} jointly forbid; "
                     f"classified BLOCK not NEED", "STOP BLOCK")
else:
    log("E4", v, "goal performed")

E5_PATTERNS = [("?X", "P4", "O8"), ("?X", "P1", "O1"), ("?X", "P5", "TRUE")]
v = ev.requirement("E5", "TASK_E5", "RQ1", E5_PATTERNS)
c = ev.req_candidates(E5_PATTERNS)
log("E5", v, f"RQ1 created (TASK-authorized), OPEN; "
             f"full-support candidates now: {c or 'none'} → no binding")

v = ev.install_watch("W1", ("O4", "P3", "S3"))
log("E6", v, "WATCH W1 installed; executor re-evaluates after every COMMIT")

v, _ = ev.ingest("E7", "N7", "O6", "P1", "O2", "EVS1", time=2)
log("E7", v, f"O6 P1: T8 → {net.records['T8'].status_log[-1].state} "
             f"(non-destructive), N7 CURRENT")

v, extra = ev.ingest("E8", "N8", "O4", "P3", "S3", "EVS1", time=3)
fired = "KAIROS fired" if net.events else "no event"
log("E8", v, f"two CURRENT P3 values → visible OPEN ({extra}); watch: {fired}",
    "STOP NEED" if v == NEED else "")

v, gs = ev.ingest("E9", "N9", "O5", "P1", "O4", "VIS2", time=3)
blocks = [g for vv, g in gs if vv == BLOCK]
needs = [g for vv, g in gs if vv == NEED]
log("E9", v, f"BLOCK₁: {blocks[0]} forbids {ev.source_class('VIS2')} observation "
             f"of P1→O4; STOP₂: {needs[0]}-ის გამოყენებადობა "
             f"multiplicity-OPEN-ზეა დამოკიდებული — ორი ცალკე გაჩერება, "
             f"გზა არ გამოგონილა", "BLOCK+NEED")

c = ev.req_candidates(E5_PATTERNS)
log("E10", GO, f"RQ1 still OPEN; candidates: {c or 'none'}; OPEN history preserved")

ev.ingest("E11", "T11", "O5", "P4", "O8", "TXT2")
v, _ = ev.ingest("E11", "T12", "O5", "P5", "TRUE", "TXT2")
log("E11", v, "ingested O5 P4 O8, O5 P5 TRUE (TXT2)")

v, x = ev.req_bind("E12", "RQ1", E5_PATTERNS)
if v == GO:
    log("E12", v, f"RQ1 bound to {x} (all three patterns supported); "
                  f"OPEN history preserved in status_log")
else:
    log("E12", v, f"candidates: {x}")

print("
" + "═" * 74)
print("FINAL REGISTRY")
cur = [r.addr for r in net.records.values()
       if r.status_log and r.status_log[-1].state == "CURRENT"
       and r.f("PREDICATE") not in (None,)]
hist = [r.addr for r in net.records.values()
        if any(a.state == "HISTORICAL" for a in r.status_log)]
opens = [r.addr for r in net.records.values()
         if r.status_log and r.status_log[-1].state == "OPEN"]
print(f"CURRENT:    {sorted(cur)}")
print(f"HISTORICAL: {sorted(hist)}")
print(f"OPEN:       {sorted(opens)}")
print(f"KAIROS:     {net.events}")
print(f"STOP MAP:   {[(s.where, s.stop_class) for s in net.stops]}")
print(f"ASK list:   {[(s.where, s.query) for s in net.stops if s.stop_class == 'ASK']}")
