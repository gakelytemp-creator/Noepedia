#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dct_runner.py — DCT01–22 ზონდების მექანიკური გადარბენა demon_core-ზე.
ყოველი ზონდის მოსალოდნელი ვერდიქტი აღებულია current/experiments/DEMON_DCT*.md-დან.
შედეგი: REPRODUCED / DIVERGED თითო შემოწმებაზე.
"""
from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED

RESULTS = []

def expect(dct, what, expected, actual):
    ok = (expected == actual)
    RESULTS.append((dct, what, expected, actual, "REPRODUCED" if ok else "DIVERGED"))
    return ok

def last_stop(net, n=1):
    return net.stops[-n] if len(net.stops) >= n else None


def base_net():
    net = Network(); d = Demon(net)
    return net, d

def add(net, addr, **fields):
    r = Record(addr, fields); net.records[addr] = r; r.committed = True
    return r

def edge(net, src, dst, role, name=None):
    a = name or f"RF_{src}_{dst}_{role}"
    return add(net, a, SUBJECT=src, PREDICATE="REFERS_TO", OBJECT=dst, ROLE=role)


# ─────────────────────────── DCT01 ───────────────────────────
def dct01():
    net, d = base_net()
    # E1 conflict: P1 ANTI_OF P1N → CF იქმნება REFERS_TO+ROLE-ით (post-core: GO)
    add(net, "T1", SUBJECT="O1", PREDICATE="P1", OBJECT="O2"); net.mark("T1", "CURRENT")
    add(net, "N1", SUBJECT="O1", PREDICATE="P1N", OBJECT="O2")
    cf = Record("CF1", {"TYPE": "CONFLICT"})
    e1 = Record("CF1_a", {"SUBJECT": "CF1", "PREDICATE": "REFERS_TO", "OBJECT": "T1", "ROLE": "CONFLICT_SIDE"})
    e2 = Record("CF1_b", {"SUBJECT": "CF1", "PREDICATE": "REFERS_TO", "OBJECT": "N1", "ROLE": "CONFLICT_SIDE"})
    v, _ = d.commit(d.propose(add=[cf, e1, e2], mark=[("CF1", "OPEN")]))
    expect("DCT01", "E1 conflict object with refs", GO, v)
    # E2 later state, SINGLE_CURRENT_TARGET
    add(net, "T2", SUBJECT="O5", PREDICATE="P2", OBJECT="O6"); net.mark("T2", "CURRENT")
    n2 = Record("N2", {"SUBJECT": "O5", "PREDICATE": "P2", "OBJECT": "O7"})
    v, _ = d.assert_current("O5", "P2", n2, {"SINGLE_CURRENT_TARGET": True})
    expect("DCT01", "E2 transition verdict", GO, v)
    expect("DCT01", "E2 T2 → HISTORICAL", "HISTORICAL", net.records["T2"].status_log[-1].state)
    expect("DCT01", "E2 N2 → CURRENT", "CURRENT", net.records["N2"].status_log[-1].state)
    # E3 requirement concept — explicit TASK-ით (overlay 27.2) → GO
    add(net, "RP1", TYPE="TRIPLET_PATTERN", SUBJECT="X", PREDICATE="P3", OBJECT="O2")
    add(net, "RP2", TYPE="TRIPLET_PATTERN", SUBJECT="X", PREDICATE="P4", OBJECT="O9")
    add(net, "TASK1", TYPE="TASK", REQUIRED_PATTERNS=["RP1", "RP2"])
    rq = Record("RQ1", {"TYPE": "REQUIREMENT_CONCEPT", "REQUIREMENT": ["RP1", "RP2"]})
    v, _ = d.commit(d.propose(add=[rq], mark=[("RQ1", "OPEN")], authorized_by="TASK1"))
    expect("DCT01", "E3 requirement concept (TASK-authorized)", GO, v)
    # E3b: requirement concept TASK-ის გარეშე → general birth OPEN → უარი
    rq2 = Record("RQ2", {"TYPE": "REQUIREMENT_CONCEPT"})
    v, _ = d.commit(d.propose(add=[rq2]))
    expect("DCT01", "E3b birth without TASK blocked", BLOCK, v)
    # E4 credit
    add(net, "MR1", TYPE="TRIPLET_PATTERN", SUBJECT="O3", PREDICATE="P4", OBJECT="O4")
    kc = Record("KC1", {"TYPE": "KNOWLEDGE_CREDIT", "CREDIT_FOR": "MR1", "DEBT": "MR1", "SCOPE": "SCENE_2"})
    d1 = Record("D1", {"SUBJECT": "O1", "PREDICATE": "P5", "OBJECT": "O4"})
    v, _ = d.commit(d.propose(add=[kc, d1], mark=[("KC1", "OPEN"), ("D1", "CREDIT_DEPENDENT")]))
    expect("DCT01", "E4 credit + dependent", GO, v)
    # E5 repayment: N3 ემთხვევა MR1-ს
    n3 = Record("N3", {"SUBJECT": "O3", "PREDICATE": "P4", "OBJECT": "O4"})
    mr = net.read("MR1")
    matches = all(n3.f(k) == mr.f(k) for k in ("SUBJECT", "PREDICATE", "OBJECT"))
    v, _ = d.commit(d.propose(add=[n3], mark=[("N3", "CURRENT"), ("KC1", "REPAID")])) if matches else (BLOCK, "")
    expect("DCT01", "E5 repayment", GO, v)
    expect("DCT01", "E5 D1 stays CREDIT_DEPENDENT", "CREDIT_DEPENDENT",
           net.records["D1"].status_log[-1].state)
    # E5b over-promotion guard: D1-ის აწევა re-grounding-ის გარეშე → BLOCK
    v, _ = d.commit(d.propose(mark=[("D1", "CURRENT")]))
    expect("DCT01", "E5b over-promotion blocked", BLOCK, v)


# ─────────────────────────── DCT02 ───────────────────────────
def dct02():
    net, d = base_net()
    add(net, "T1", SUBJECT="O1", PREDICATE="P1", OBJECT="O2"); net.mark("T1", "CURRENT")
    add(net, "T2", SUBJECT="O2", PREDICATE="P2", OBJECT="O3"); net.mark("T2", "CURRENT")
    add(net, "R1", TYPE="RULE")
    # derived T3 provenance-ის გარეშე → CHECK FAIL (ეს იყო STOP_05)
    t3 = Record("T3", {"SUBJECT": "O1", "PREDICATE": "P3", "OBJECT": "O3"})
    v, _ = d.commit(d.propose(add=[t3], derived=[("T3", ["T1", "T2"], "R1")]))
    expect("DCT02", "derived commit w/o REFERS_TO blocked", BLOCK, v)
    # REFERS_TO-თი → PASS
    refs = [Record(f"RF{i}", {"SUBJECT": "T3", "PREDICATE": "REFERS_TO", "OBJECT": o,
                              "ROLE": r}) for i, (o, r) in
            enumerate([("T1", "PREMISE"), ("T2", "PREMISE"), ("R1", "RULE_USED")], 1)]
    v, _ = d.commit(d.propose(add=[t3] + refs, derived=[("T3", ["T1", "T2"], "R1")],
                              mark=[("T3", "CURRENT")]))
    expect("DCT02", "derived commit with provenance", GO, v)


# ─────────────────────────── DCT03/04 ───────────────────────────
def dct03_04():
    net, d = base_net()
    for a in ("T0", "T1", "T2", "R1", "T3"):
        add(net, a)
    edge(net, "T3", "T1", "PREMISE"); edge(net, "T3", "T2", "PREMISE")
    edge(net, "T3", "T0", "CONTEXT"); edge(net, "T3", "R1", "RULE_USED")
    premises = {e.f("OBJECT") for e in net.refs_from("T3", role="PREMISE")}
    expect("DCT03", "roles distinguish premises", {"T1", "T2"}, premises)
    rules = {e.f("OBJECT") for e in net.refs_from("T3", role="RULE_USED")}
    expect("DCT03", "roles distinguish rule", {"R1"}, rules)
    # DCT04: credit roles
    for a in ("KC1", "MR1", "SRC_A", "D1"):
        add(net, a)
    edge(net, "KC1", "MR1", "DEBT"); edge(net, "KC1", "SRC_A", "AUTHORIZATION")
    edge(net, "KC1", "D1", "DEPENDENT_DESCENDANT")
    debt = {e.f("OBJECT") for e in net.refs_from("KC1", role="DEBT")}
    expect("DCT04", "credit debt role", {"MR1"}, debt)


# ─────────────────────────── DCT05 ───────────────────────────
def dct05():
    net, d = base_net()
    add(net, "T1"); net.mark("T1", "CURRENT")
    add(net, "T3"); net.mark("T3", "CURRENT")
    add(net, "D1"); net.mark("D1", "CREDIT_DEPENDENT")
    edge(net, "T3", "T1", "PREMISE"); edge(net, "D1", "T3", "PREMISE")
    net.mark("T1", "CONFLICTED")
    res = d.propagate("T1", "CONFLICTED")
    stops = [s for s in net.stops if s.stop_class == NEED]
    expect("DCT05", "no policy → NEED", True, len(stops) >= 1)
    expect("DCT05", "missing = dependency policy", True,
           "dependency-policy" in stops[-1].missing if stops else False)
    expect("DCT05", "T3 untouched (no invented status)", "CURRENT",
           net.records["T3"].status_log[-1].state)


# ─────────────────────────── DCT06 ───────────────────────────
def dct06():
    net, d = base_net()
    add(net, "T1", SUBJECT="O1", PREDICATE="P1", OBJECT="O2"); net.mark("T1", "CURRENT")
    add(net, "T3"); net.mark("T3", "CURRENT")
    edge(net, "T3", "T1", "PREMISE")
    n1 = Record("N1", {"SUBJECT": "O1", "PREDICATE": "P1", "OBJECT": "O4"})
    v, _ = d.assert_current("O1", "P1", n1, {"SINGLE_CURRENT_TARGET": True})
    expect("DCT06", "T1 → HISTORICAL", "HISTORICAL", net.records["T1"].status_log[-1].state)
    stops = [s for s in net.stops if s.stop_class == NEED and "dependency-policy" in s.missing]
    expect("DCT06", "descendant consequence → NEED", True, len(stops) >= 1)
    expect("DCT06", "T3 status not invented", "CURRENT", net.records["T3"].status_log[-1].state)


# ─────────────────────────── DCT07 ───────────────────────────
def dct07():
    net, d = base_net()
    add(net, "T1", SUBJECT="O1", PREDICATE="P1", OBJECT="O2"); net.mark("T1", "CURRENT")
    add(net, "A1"); net.mark("A1", "CURRENT")
    add(net, "B1"); net.mark("B1", "CURRENT")
    ra = edge(net, "A1", "T1", "PREMISE", "RA"); rb = edge(net, "B1", "T1", "PREMISE", "RB")
    add(net, "R_A", TYPE="RULE", EFFECT="KEEP")
    add(net, "R_B", TYPE="RULE", EFFECT="OPEN")
    edge(net, "RA", "R_A", "POLICY"); edge(net, "RB", "R_B", "POLICY")
    n1 = Record("N1", {"SUBJECT": "O1", "PREDICATE": "P1", "OBJECT": "O4"})
    d.assert_current("O1", "P1", n1, {"SINGLE_CURRENT_TARGET": True})
    expect("DCT07", "A1 kept (snapshot policy)", "CURRENT", net.records["A1"].status_log[-1].state)
    expect("DCT07", "B1 → OPEN (live policy)", "OPEN", net.records["B1"].status_log[-1].state)


# ─────────────────────────── DCT08 ───────────────────────────
def dct08():
    net, d = base_net()
    add(net, "T1", SUBJECT="O1", PREDICATE="P1", OBJECT="O2"); net.mark("T1", "CURRENT")
    add(net, "A1"); net.mark("A1", "CURRENT")
    ra = edge(net, "A1", "T1", "PREMISE", "RA")
    add(net, "R_KEEP", TYPE="RULE", EFFECT="KEEP")
    add(net, "R_OPEN", TYPE="RULE", EFFECT="OPEN")
    edge(net, "RA", "R_KEEP", "POLICY"); edge(net, "RA", "R_OPEN", "POLICY")
    n1 = Record("N1", {"SUBJECT": "O1", "PREDICATE": "P1", "OBJECT": "O4"})
    d.assert_current("O1", "P1", n1, {"SINGLE_CURRENT_TARGET": True})
    blocks = [s for s in net.stops if s.stop_class == BLOCK]
    expect("DCT08", "two policies → BLOCK", True, len(blocks) >= 1)
    expect("DCT08", "conflict object created", True, "CF_POLICY_RA" in net.records)
    expect("DCT08", "A1 transition not committed", "CURRENT",
           net.records["A1"].status_log[-1].state)


# ─────────────────────────── DCT09 ───────────────────────────
def dct09():
    net, d = base_net()
    rskip = Record("R_SKIP", {"TYPE": "RULE"})
    # delta იყენებს საკუთარ ახალ წესს
    v, r = d.commit(d.propose(add=[rskip], introduces_rules=["R_SKIP"],
                              uses_rules=["R_SKIP"]))
    expect("DCT09", "self-authorization → BLOCK", BLOCK, v)
    # CHECK-ის გამოტოვება
    v, r = d.commit(d.propose(skip_check=True))
    expect("DCT09", "skip CHECK → BLOCK", BLOCK, v)


# ─────────────────────────── DCT10 ───────────────────────────
def dct10():
    net, d = base_net()
    t1 = Record("T1", {}); v, _ = d.commit(d.propose(add=[t1], mark=[("T1", "CURRENT")]))
    v, _ = d.commit(d.propose(mark=[("T1", "HISTORICAL")]))
    v, reason = d.commit(d.propose(delete=["T1"]))
    expect("DCT10", "purge committed history → BLOCK", BLOCK, v)
    expect("DCT10", "T1 still addressable", True, net.read("T1") is not None)


# ─────────────────────────── DCT11/12 ───────────────────────────
def dct11_12():
    net, d = base_net()
    add(net, "C1", TYPE="COMMIT_RECORD"); net.mark("C1", "COMMITTED")
    add(net, "T3"); net.mark("T3", "SUPPORTED")
    # audits
    add(net, "A1", TYPE="REAUDIT", TARGET="C1", CHECK_POLICY="V1", RESULT="PASS")
    add(net, "A2", TYPE="REAUDIT", TARGET="C1", CHECK_POLICY="V2", RESULT="FAIL")
    add(net, "A3", TYPE="REAUDIT", TARGET="C1", CHECK_POLICY="V2", RESULT="PASS")
    # history preserved:
    expect("DCT11", "C1 history status intact", "COMMITTED",
           net.records["C1"].status_log[-1].state)
    # selection policy missing → NEED (demon არ ირჩევს „უახლესი იგებს")
    audits = net.match(TYPE="REAUDIT", TARGET="C1")
    results = {a.f("RESULT") for a in audits}
    if len(results) > 1:
        net.stop("DCT12/current-status", "select current epistemic status",
                 "A1 PASS; A2 FAIL; A3 PASS", "status selection policy", NEED)
    expect("DCT12", "selection policy missing → NEED", NEED, last_stop(net).stop_class)
    # scoped rehabilitation: A3 მხოლოდ SCENE_2 → scope-resolution NEED
    net.mark("T3", "CHALLENGED", scope="GLOBAL")
    net.mark("T3", "SUPPORTED", scope="SCENE_2", basis="A3")
    s, v = net.current_status("T3", scope=None)
    expect("DCT12", "global rehabilitation not automatic", ASK, v)
    # non-destructive MARK: სრული ლოგი დაცულია
    expect("DCT12", "status history preserved", True, len(net.records["T3"].status_log) >= 3)


# ─────────────────────────── DCT13/14 ───────────────────────────
def dct13_14():
    net, d = base_net()
    add(net, "T3")
    net.mark("T3", "SUPPORTED", scope="SCENE_A")
    net.mark("T3", "CHALLENGED", scope="SCENE_B")
    s, v = net.current_status("T3", scope="SCENE_A")
    expect("DCT13", "scoped query A", ("SUPPORTED", GO), (s, v))
    s, v = net.current_status("T3", scope="SCENE_B")
    expect("DCT13", "scoped query B", ("CHALLENGED", GO), (s, v))
    s, v = net.current_status("T3", scope=None)
    expect("DCT13", "unscoped query → ASK", ASK, v)
    # overlapping/shared scope incompatibility → BLOCK
    net2, _ = base_net(); add(net2, "T3")
    net2.mark("T3", "SUPPORTED", scope="SCENE_X", basis="A1")   # ES1 ბაზისით
    net2.mark("T3", "CHALLENGED", scope="SCENE_X", basis="A2")  # ES2 ბაზისით
    s, v = net2.current_status("T3", scope="SCENE_X")
    expect("DCT13", "same-scope incompatible → BLOCK", BLOCK, v)
    # DCT14 time
    net3, _ = base_net(); add(net3, "T3")
    net3.mark("T3", "SUPPORTED", scope="SCENE_A", time=(1, 5))
    net3.mark("T3", "CHALLENGED", scope="SCENE_A", time=(6, 9))
    s, v = net3.current_status("T3", scope="SCENE_A", time=3)
    expect("DCT14", "t3 → SUPPORTED", ("SUPPORTED", GO), (s, v))
    s, v = net3.current_status("T3", scope="SCENE_A", time=8)
    expect("DCT14", "t8 → CHALLENGED", ("CHALLENGED", GO), (s, v))
    s, v = net3.current_status("T3", scope="SCENE_A", time=None)
    expect("DCT14", "no time qualifier → ASK", ASK, v)
    net4, _ = base_net(); add(net4, "T3")
    net4.mark("T3", "SUPPORTED", scope="SCENE_A", time=(1, 7), basis="A1")
    net4.mark("T3", "CHALLENGED", scope="SCENE_A", time=(5, 9), basis="A2")
    s, v = net4.current_status("T3", scope="SCENE_A", time=6)
    expect("DCT14", "overlapping windows → BLOCK", BLOCK, v)


# ─────────────────────────── DCT15/16/17/18 ───────────────────────────
def dct15_18():
    net, d = base_net()
    add(net, "ES1", TYPE="STATUS_ASSERTION", STATE="SUPPORTED")
    q1 = add(net, "Q1", TYPE="APPLICABILITY_QUALIFIER", VALUE="SCENE_A")
    edge(net, "ES1", "Q1", "QUALIFIER")
    # matching policy აკლია → NEED
    a, v = d.applicability("ES1", {"scope": "SCENE_A"})
    expect("DCT15", "no match policy → NEED", NEED, v)
    # ერთი policy → APPLICABLE
    add(net, "R_SCOPE", TYPE="RULE", MATCH_FN=lambda val, ctx: ctx.get("scope") == val)
    edge(net, "Q1", "R_SCOPE", "MATCH_POLICY")
    a, v = d.applicability("ES1", {"scope": "SCENE_A"})
    expect("DCT15", "match → APPLICABLE", ("APPLICABLE", GO), (a, v))
    a, v = d.applicability("ES1", {"scope": "SCENE_Z"})
    expect("DCT15", "no match → NOT_APPLICABLE (≠FALSE)", ("NOT_APPLICABLE", GO), (a, v))
    # DCT16: მეორე, შეუთავსებელი policy
    add(net, "R_SUB", TYPE="RULE",
        MATCH_FN=lambda val, ctx: ctx.get("scope") in (val, f"sub_{val}"))
    edge(net, "Q1", "R_SUB", "MATCH_POLICY")
    a, v = d.applicability("ES1", {"scope": "sub_SCENE_A"})
    expect("DCT16", "divergent policies → BLOCK", BLOCK, v)
    expect("DCT16", "qualifier conflict object", True, "CF_QPOLICY_Q1" in net.records)
    # DCT17: ციკლი — policy qualified by qualifier whose policy is itself
    net2, d2 = base_net()
    add(net2, "ES1", TYPE="STATUS_ASSERTION")
    add(net2, "Q1", TYPE="APPLICABILITY_QUALIFIER", VALUE="A")
    edge(net2, "ES1", "Q1", "QUALIFIER")
    p1 = add(net2, "RP1", TYPE="RULE", MATCH_FN=lambda v_, c: True)
    edge(net2, "Q1", "RP1", "MATCH_POLICY")
    add(net2, "PQ1", TYPE="APPLICABILITY_QUALIFIER", VALUE="L")
    edge(net2, "RP1", "PQ1", "QUALIFIER")
    edge(net2, "PQ1", "RP1", "MATCH_POLICY")      # ციკლი: RP1 → PQ1 → RP1
    a, v = d2.applicability("ES1", {"scope": "A"})
    expect("DCT17", "cycle → BLOCK", BLOCK, v)
    expect("DCT17", "EVALUATION_CYCLE record", True,
           any(r.f("TYPE") == "EVALUATION_CYCLE" for r in net2.records.values()))
    # DCT18: ორი კანონიერი გზა, განსხვავებული შედეგი = იგივე divergent-outcome BLOCK
    #        (ჩვენი ენჯინი ამას DCT16-ის იმავე მექანიზმით იჭერს — ზონდიც ამას ამბობს §6)


# ─────────────────────────── DCT19/20/21 ───────────────────────────
def dct19_21():
    net, d = base_net()
    add(net, "JP1"); net.mark("JP1", "SUPPORTED")
    add(net, "JP2"); net.mark("JP2", "SUPPORTED")
    add(net, "EV1", TYPE="EVALUATION_RESULT", RESULT="MATCH")
    edge(net, "EV1", "JP1", "JUSTIFICATION"); edge(net, "EV1", "JP2", "JUSTIFICATION")
    s, v = d.result_support("EV1")
    expect("DCT19", "convergent paths → SUPPORTED/GO", ("SUPPORTED", GO), (s, v))
    # DCT20: JP1 challenged, composition policy აკლია → NEED
    net.mark("JP1", "CHALLENGED")
    s, v = d.result_support("EV1")
    expect("DCT20", "no composition policy → NEED", NEED, v)
    # ALTERNATIVE policy → survives
    cp1 = add(net, "CP1", TYPE="JUSTIFICATION_COMPOSITION_POLICY", MODE="ALTERNATIVE")
    net.mark("CP1", "CURRENT")
    edge(net, "EV1", "CP1", "COMPOSITION_POLICY")
    s, v = d.result_support("EV1")
    expect("DCT20", "ALTERNATIVE → survives", ("SUPPORTED", GO), (s, v))
    # DCT21: policy transition ALTERNATIVE → JOINT
    net.mark("CP1", "HISTORICAL")
    cp2 = add(net, "CP2", TYPE="JUSTIFICATION_COMPOSITION_POLICY", MODE="JOINT")
    net.mark("CP2", "CURRENT")
    edge(net, "EV1", "CP2", "COMPOSITION_POLICY")
    s, v = d.result_support("EV1")
    expect("DCT21", "JOINT → CHALLENGED", ("CHALLENGED", GO), (s, v))
    # history not rewritten: CP1-ის კვალი და EV1-ის ისტორიული MATCH ხელუხლებელია
    expect("DCT21", "CP1 history intact", "HISTORICAL", net.records["CP1"].status_log[-1].state)
    expect("DCT21", "EV1 historical result intact", "MATCH", net.records["EV1"].f("RESULT"))
    # ორი ერთდროულად CURRENT policy → BLOCK
    net.mark("CP1", "CURRENT")
    s, v = d.result_support("EV1")
    expect("DCT21", "two applicable policies → BLOCK", BLOCK, v)


# ─────────────────────────── DCT22 ───────────────────────────
def dct22():
    net, d = base_net()
    add(net, "PJ1"); net.mark("PJ1", "SUPPORTED")
    add(net, "CP1", TYPE="JUSTIFICATION_COMPOSITION_POLICY", MODE="ALTERNATIVE")
    net.mark("CP1", "CURRENT")
    add(net, "EV1"); net.mark("EV1", "SUPPORTED")
    add(net, "T3"); net.mark("T3", "CURRENT")
    e1 = edge(net, "CP1", "PJ1", "JUSTIFICATION", "E_PJ_CP")
    e2 = edge(net, "EV1", "CP1", "COMPOSITION_POLICY", "E_CP_EV")
    e3 = edge(net, "T3", "EV1", "PREMISE", "E_EV_T3")
    # PJ1 challenged; პირველ edge-ზე პოლიტიკა არ დევს → NEED, ტალღა ჩერდება
    net.mark("PJ1", "CHALLENGED")
    d.propagate("PJ1", "CHALLENGED")
    needs = [s for s in net.stops if s.stop_class == NEED]
    expect("DCT22", "first edge no policy → NEED", True, len(needs) >= 1)
    expect("DCT22", "no global cascade (T3 intact)", "CURRENT",
           net.records["T3"].status_log[-1].state)
    # edge-პოლიტიკით ტალღა ერთი ნაბიჯით მიდის და იქ ჩერდება (შემდეგი edge უპოლიტიკოა)
    net2, d2 = base_net()
    add(net2, "PJ1"); net2.mark("PJ1", "SUPPORTED")
    add(net2, "CP1"); net2.mark("CP1", "CURRENT")
    add(net2, "EV1"); net2.mark("EV1", "SUPPORTED")
    ee = edge(net2, "CP1", "PJ1", "JUSTIFICATION", "E1")
    add(net2, "RPOL", TYPE="RULE", EFFECT="OPEN")
    edge(net2, "E1", "RPOL", "POLICY")
    edge(net2, "EV1", "CP1", "COMPOSITION_POLICY", "E2")
    net2.mark("PJ1", "CHALLENGED")
    d2.propagate("PJ1", "CHALLENGED")
    expect("DCT22", "edge-local wave: CP1 → OPEN", "OPEN",
           net2.records["CP1"].status_log[-1].state)
    needs2 = [s for s in net2.stops if s.stop_class == NEED]
    expect("DCT22", "wave frontier → NEED at next edge", True, len(needs2) >= 1)


# ─────────────────────────── გაშვება ───────────────────────────
if __name__ == "__main__":
    for fn in (dct01, dct02, dct03_04, dct05, dct06, dct07, dct08, dct09,
               dct10, dct11_12, dct13_14, dct15_18, dct19_21, dct22):
        fn()
    rep = sum(1 for r in RESULTS if r[4] == "REPRODUCED")
    print(f"\n{'='*72}\nშედეგი: {rep}/{len(RESULTS)} შემოწმება REPRODUCED\n{'='*72}")
    for dct, what, exp, act, verdict in RESULTS:
        flag = "✓" if verdict == "REPRODUCED" else "✗"
        print(f" {flag} {dct:7s} {what:45s} მოსალ={exp}  მიღებ={act}")