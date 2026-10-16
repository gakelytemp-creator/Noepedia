#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gw01_runner.py — GW01-ის მექანიკური გადარბენა (GW02 ნაწილი II).
შემავალი: WORLD_INPUT.md (sha256 841ddd53… შემოწმებული byte-for-byte).
შემსრულებელი: demon_core (დეტერმინისტული). LLM არ მონაწილეობს.
E1–E12 მკაცრად რიგით; ყოველ მოვლენაზე: ops, NETWORK DELTA, STOP, NEED.
"""
import sys; sys.path.insert(0, "/home/claude/demon")
from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED

LOG = []
def log(ev, verdict, note, stops=""):
    LOG.append((ev, verdict, note, stops))
    print(f"{ev:4s} {verdict:6s} {note}" + (f"   [{stops}]" if stops else ""))

net = Network(); d = Demon(net)

def add(addr, **f):
    r = Record(addr, f); net.records[addr] = r; r.committed = True; return r

# ── N0 ──
for a, s, p, o, extra in [
    ("T1","O3","P1","O1",{}), ("T2","O4","P2","O3",{}), ("T3","O11","P2","O3",{}),
    ("T4","O4","P3","S1",{}), ("T5","O11","P3","S1",{}), ("T6","O8","P3","S2",{}),
    ("T7","O9","P1","O2",{}), ("T8","O6","P1","O1",{"PROVENANCE":"VIS0","TIME":0}),
    ("T9","O7","P1","O1",{})]:
    add(a, SUBJECT=s, PREDICATE=p, OBJECT=o, **extra); net.mark(a, "CURRENT")
for ra in ("R1","R2","R3","R4","R5","R6","C1"):
    add(ra, TYPE="RULE"); net.mark(ra, "CURRENT")

P_PROPS = {"P1": {"SINGLE_CURRENT_TARGET": True}}      # R1; P3/P4/P5 — პოლიტიკა არ არის

def current(subj=None, pred=None, obj=None):
    out = []
    for r in net.records.values():
        if r.f("PREDICATE") is None: continue
        if subj and r.f("SUBJECT") != subj: continue
        if pred and r.f("PREDICATE") != pred: continue
        if obj and r.f("OBJECT") != obj: continue
        if r.status_log and r.status_log[-1].state == "CURRENT":
            out.append(r)
    return out

# ════ E1 — TXT1: O5 P1 O1 (overlay 27.1: source PROPOSE → CHECK → COMMIT) ════
t10 = Record("T10", {"SUBJECT":"O5","PREDICATE":"P1","OBJECT":"O1",
                     "TYPE":"OBSERVATION","SOURCE":"TXT1"})
v,_ = d.commit(d.propose(add=[t10], mark=[("T10","CURRENT")]))
log("E1", v, "ingest O5 P1 O1 (TXT1) → CURRENT")

# ════ E2 — VIS1 t1: v1 sample; binding candidates ════
v1a = Record("V1A", {"SUBJECT":"v1","PREDICATE":"P2","OBJECT":"O3","SOURCE":"VIS1","TIME":1})
v1b = Record("V1B", {"SUBJECT":"v1","PREDICATE":"P3","OBJECT":"S1","SOURCE":"VIS1","TIME":1})
d.commit(d.propose(add=[v1a, v1b], mark=[("V1A","CURRENT"),("V1B","CURRENT")]))
# identity binding: ვის ემთხვევა v1-ის ორივე თვისება?
cands = [o for o in ("O4","O11","O3","O5","O6","O7","O8","O9")
         if current(o,"P2","O3") and current(o,"P3","S1")]
if len(cands) == 1:
    log("E2", GO, f"v1 bound to {cands[0]}")
elif len(cands) > 1:
    net.stop("E2/identity", "bind v1 to an O-id", f"candidates {cands}",
             "discriminating evidence", ASK, can_ask=True,
             query=f"which of {cands} is v1?")
    log("E2", ASK, f"AMBIGUOUS_MATCH: candidates {cands} — no false merge", "STOP ASK")
else:
    log("E2", NEED, "no candidate")

# ════ E3 — TASK: current P1 target of O4 at level {O1,O2} ════
# R2: (O4 P2 O3)+(O3 P1 O1) ⇒ derive (O4 P1 O1); authorized; REFERS_TO premises+rule
t2, t1 = net.read("T2"), net.read("T1")
assert current("O4","P2","O3") and current("O3","P1","O1")
dv = Record("DV1", {"SUBJECT":"O4","PREDICATE":"P1","OBJECT":"O1"})
refs = [Record(f"DV1_r{i}", {"SUBJECT":"DV1","PREDICATE":"REFERS_TO","OBJECT":o,"ROLE":r})
        for i,(o,r) in enumerate([("T2","PREMISE"),("T1","PREMISE"),("R2","RULE_USED")],1)]
v,_ = d.commit(d.propose(add=[dv]+refs, derived=[("DV1",["T2","T1"],"R2")],
                         mark=[("DV1","CURRENT")]))
log("E3", v, "derived (O4 P1 O1) with full provenance; answer at level {O1,O2}: O1")

# ════ E4 — TASK: make (O7 P1 O2) current — C1 კრძალავს ════
# C1: (O7 P1 O1) must remain current; R1 single-target ⇒ გადასვლა დაარღვევდა C1-ს
if current("O7","P1","O1"):
    net.stop("E4/goal", "make (O7 P1 O2) current",
             "C1 requires (O7 P1 O1) current; R1 single target",
             "none — rules forbid this path", BLOCK)
    log("E4", BLOCK, "impossible goal: C1 + R1 jointly forbid; classified BLOCK not NEED", "STOP BLOCK")

# ════ E5 — TASK: requirement concept (overlay 27.2 explicit authorization) ════
for i,(s,p,o) in enumerate([("X","P4","O8"),("X","P1","O1"),("X","P5","TRUE")],1):
    add(f"RP{i}", TYPE="TRIPLET_PATTERN", SUBJECT=s, PREDICATE=p, OBJECT=o)
add("TASK_E5", TYPE="TASK", REQUIRED_PATTERNS=["RP1","RP2","RP3"])
rq = Record("RQ1", {"TYPE":"REQUIREMENT_CONCEPT","REQUIREMENT":["RP1","RP2","RP3"]})
v,_ = d.commit(d.propose(add=[rq], mark=[("RQ1","OPEN")], authorized_by="TASK_E5"))
def rq_candidates():
    xs = {r.f("SUBJECT") for r in current(None,"P1","O1")}
    full = [x for x in xs if current(x,"P4","O8") and current(x,"P5","TRUE")]
    return full
log("E5", v, f"RQ1 created (TASK-authorized), OPEN; full-support candidates now: {rq_candidates() or 'none'} → no binding")

# ════ E6 — TASK: watch on (O4 P3 S3) becomes current (overlay 27.3) ════
w = Record("W1", {"TYPE":"WATCH", "FIRED": False,
                  "CONDITION": lambda n: any(
                      r.f("SUBJECT")=="O4" and r.f("PREDICATE")=="P3" and r.f("OBJECT")=="S3"
                      and r.status_log and r.status_log[-1].state=="CURRENT"
                      for r in n.records.values())})
v,_ = d.commit(d.propose(add=[w]))
net.active_watches.append("W1")
log("E6", v, "WATCH W1 installed; executor re-evaluates after every COMMIT")

# ════ E7 — EVS1 t2: O6 P1 O2 (R1+R5: supersede T8) ════
n7 = Record("N7", {"SUBJECT":"O6","PREDICATE":"P1","OBJECT":"O2","SOURCE":"EVS1","TIME":2})
v,_ = d.assert_current("O6","P1", n7, P_PROPS["P1"])
log("E7", v, f"O6 P1: T8 → {net.records['T8'].status_log[-1].state} (non-destructive), N7 CURRENT")

# ════ E8 — EVS1 t3: O4 P3 S3 (P3-ს multiplicity პოლიტიკა არ აქვს → overlay 27.4) ════
n8 = Record("N8", {"SUBJECT":"O4","PREDICATE":"P3","OBJECT":"S3","SOURCE":"EVS1","TIME":3})
v, extra = d.assert_current("O4","P3", n8, {})      # no SINGLE_CURRENT_TARGET, no CARDINALITY
fired = "KAIROS fired" if net.events else "no event"
log("E8", v, f"two CURRENT P3 values → visible OPEN ({extra}); watch: {fired}",
    "STOP NEED" if v==NEED else "")

# ════ E9 — VIS2 t3: O5 P1 O4 — R4 + multiplicity entanglement ════
# R4: if (Y P3 S1) current then (X P1 Y) not observable by VIS class.
y_s1 = bool(current("O4","P3","S1"))
y_mult_open = "OPEN_MULT_P3" in net.records
if y_s1:
    net.stop("E9/R4", "ingest (O5 P1 O4) from VIS2",
             "(O4 P3 S1) CURRENT ⇒ P1→O4 unobservable by VIS", "none — R4 forbids", BLOCK)
    b1 = "BLOCK₁: R4 forbids VIS observation of P1→O4"
if y_mult_open:
    net.stop("E9/R4-applicability", "decide R4 applicability",
             "O4 P3 multiplicity unresolved (S1 and S3 both CURRENT)",
             "cardinality policy for P3", NEED)
    b2 = "STOP₂: R4-ის გამოყენებადობა multiplicity-OPEN-ზეა დამოკიდებული"
log("E9", BLOCK, f"{b1}; {b2} — ორი ცალკე გაჩერება, გზა არ გამოგონილა", "BLOCK+NEED")

# ════ E10 — revisit E5 ════
log("E10", GO, f"RQ1 still OPEN; candidates: {rq_candidates() or 'none'}; OPEN history preserved")

# ════ E11 — TXT2: O5 P4 O8 ; O5 P5 TRUE ════
a1 = Record("T11", {"SUBJECT":"O5","PREDICATE":"P4","OBJECT":"O8","SOURCE":"TXT2","TYPE":"OBSERVATION"})
a2 = Record("T12", {"SUBJECT":"O5","PREDICATE":"P5","OBJECT":"TRUE","SOURCE":"TXT2","TYPE":"OBSERVATION"})
v,_ = d.commit(d.propose(add=[a1,a2], mark=[("T11","CURRENT"),("T12","CURRENT")]))
log("E11", v, "ingested O5 P4 O8, O5 P5 TRUE (TXT2)")

# ════ E12 — revisit E5; bind თუ ყველა pattern supported ════
c = rq_candidates()
if len(c) == 1:
    bind = Record("RQ1_BIND", {"SUBJECT":"RQ1","PREDICATE":"REFERS_TO","OBJECT":c[0],"ROLE":"BOUND_CANDIDATE"})
    v,_ = d.commit(d.propose(add=[bind], mark=[("RQ1","BOUND")]))
    log("E12", v, f"RQ1 bound to {c[0]} (all three patterns supported); OPEN history preserved in status_log")
else:
    log("E12", NEED if not c else ASK, f"candidates: {c}")

# ════ Final registry ════
print("\n" + "═"*74)
print("FINAL REGISTRY")
cur = [r.addr for r in net.records.values()
       if r.status_log and r.status_log[-1].state == "CURRENT" and r.f("PREDICATE") not in (None,)]
hist = [r.addr for r in net.records.values()
        if any(a.state == "HISTORICAL" for a in r.status_log)]
opens = [r.addr for r in net.records.values()
         if r.status_log and r.status_log[-1].state == "OPEN"]
print(f"CURRENT:    {sorted(cur)}")
print(f"HISTORICAL: {sorted(hist)}")
print(f"OPEN:       {sorted(opens)}")
print(f"KAIROS:     {net.events}")
print(f"STOP MAP:   {[(s.where, s.stop_class) for s in net.stops]}")
print(f"ASK list:   {[(s.where, s.query) for s in net.stops if s.stop_class=='ASK']}")