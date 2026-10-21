#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Workshop tests for admission.py on a tiny synthetic network (no GW content)."""
from pathlib import Path
import sys, unittest
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "run_c"), str(HERE)]

from demon_core import Network, Demon, Record, GO, BLOCK, NEED
from family_executor import HandlerResult
from admission import (admit, install_default_policy, compose_evidence, POLICY_ADDR,
                       PER_FACT_MARKER, PER_RULE_DEBT, debt_addr, debts_of, dependents_of)


def fact(net, addr, s, p, o):
    r = Record(addr, {"SUBJECT": s, "PREDICATE": p, "OBJECT": o}); net.records[addr] = r
    r.committed = True; net.mark(addr, "CURRENT")


def incoming(addr="IN1", s="A", p="P", o="Y"):
    return Record(addr, {"SUBJECT": s, "PREDICATE": p, "OBJECT": o, "TYPE": "OBSERVATION", "SOURCE": "S1"})


def blocked():
    return HandlerResult(details={"rule_results": [{"rule": "RULE1", "result": HandlerResult(
        verdict=BLOCK, conflicts=[{"rule": "RULE1", "subject": "A", "current_objects": ["X"]}])}]})


def unchecked():
    return HandlerResult(verdict=NEED, unchecked_dependencies=[{"dependency": "RULE2", "reason": "EXECUTOR_HOLE"}])


class AdmissionTest(unittest.TestCase):
    def setUp(self):
        self.net = Network(); self.d = Demon(self.net)
        fact(self.net, "F0", "A", "P", "X")
        install_default_policy(self.net, self.d, debt_shape=PER_FACT_MARKER)   # WS01-WS03 shape

    def test_d1_conflict_is_materialized_not_swallowed(self):
        adm = admit(self.net, self.d, incoming(), blocked(), prefix="E1")
        self.assertEqual(adm.verdict, GO)
        self.assertTrue(adm.fact_committed)
        c = self.net.read("E1_CONFLICT_1")
        self.assertIsNotNone(c)
        self.assertEqual(c.f("TYPE"), "CONFLICT")
        self.assertEqual(c.f("PARTIES"), ["IN1", "F0"])          # both sides addressable
        self.assertEqual(c.status_log[-1].state, "OPEN")
        self.assertEqual(self.net.read("F0").status_log[-1].state, "CURRENT")  # nothing deleted

    def test_d2_unchecked_does_not_veto_and_is_linked(self):
        adm = admit(self.net, self.d, incoming(), unchecked(), prefix="E2")
        self.assertEqual(adm.verdict, GO)
        self.assertTrue(adm.fact_committed)
        m = self.net.read("E2_UNCHECKED_1")
        self.assertEqual(m.f("CHECKED_RECORD"), "IN1")
        self.assertEqual(self.net.refs_from("E2_UNCHECKED_1", role="UNCHECKED_RECORD")[0].f("OBJECT"), "IN1")

    def test_clean_admission(self):
        adm = admit(self.net, self.d, incoming(), HandlerResult(), prefix="E3")
        self.assertEqual((adm.verdict, adm.records, adm.reason), (GO, [], "admitted clean"))

    def test_policy_is_a_network_record_and_refuse_still_records(self):
        self.net.read(POLICY_ADDR).fields["ON_CONFLICT"] = "REFUSE"
        adm = admit(self.net, self.d, incoming(), blocked(), prefix="E4")
        self.assertEqual(adm.verdict, BLOCK)
        self.assertFalse(adm.fact_committed)
        self.assertIsNotNone(self.net.read("E4_CONFLICT_1"))       # signal survives refusal

    def test_d3_unsupported_operation_is_unchecked(self):
        vr = HandlerResult(details={"rule_results": [{"rule": "RULE3", "result": HandlerResult(
            verdict=NEED, stops=[{"rule": "RULE3", "missing": "operation VALIDATE_INCOMING"}])}]})
        adm = admit(self.net, self.d, incoming(), vr, prefix="E5")
        self.assertEqual((adm.verdict, adm.fact_committed), (GO, True))
        m = self.net.read("E5_UNCHECKED_1")
        self.assertEqual((m.f("DEPENDENCY"), m.f("REASON")), ("RULE3", "OPERATION_UNSUPPORTED"))

    def test_d3_other_need_is_not_unchecked(self):
        vr = HandlerResult(details={"rule_results": [{"rule": "RULE4", "result": HandlerResult(
            verdict=NEED, stops=[{"rule": "RULE4", "missing": "consequent value"}])}]})
        self.assertEqual(compose_evidence(vr), [])

    def test_composition_keeps_every_signal(self):
        both = blocked(); both.unchecked_dependencies = unchecked().unchecked_dependencies
        self.assertEqual([e["KIND"] for e in compose_evidence(both)], ["CONFLICT", "UNCHECKED"])


class RuleDebtTest(unittest.TestCase):
    """WS04 — one debt per unexecutable rule, per-fact DEPENDS_ON edges."""
    def setUp(self):
        self.net = Network(); self.d = Demon(self.net)
        install_default_policy(self.net, self.d, debt_shape=PER_RULE_DEBT)

    def two_rules(self):
        return HandlerResult(verdict=NEED, unchecked_dependencies=[
            {"dependency": "RULE2", "reason": "EXECUTOR_HOLE"},
            {"dependency": "RULE5", "reason": "SCHEMA_DRIFT"}])

    def test_one_debt_per_rule_not_per_fact(self):
        for i in (1, 2, 3):
            adm = admit(self.net, self.d, incoming(f"IN{i}"), self.two_rules(), prefix=f"E{i}")
            self.assertEqual((adm.verdict, adm.fact_committed), (GO, True))
        debts = sorted(r.addr for r in self.net.records.values() if r.f("TYPE") == "UNEXECUTABLE_RULE_DEBT")
        self.assertEqual(debts, ["DEBT_RULE2", "DEBT_RULE5"])                 # 2, not 6
        opens = [r.addr for r in self.net.records.values() if r.status_log and r.status_log[-1].state == "OPEN"]
        self.assertEqual(sorted(opens), debts)                                 # registry sees 2

    def test_fact_still_sees_its_debt(self):
        admit(self.net, self.d, incoming("IN1"), self.two_rules(), prefix="E1")
        self.assertEqual(debts_of(self.net, "IN1"), ["DEBT_RULE2", "DEBT_RULE5"])

    def test_edge_carries_the_specific_check(self):
        admit(self.net, self.d, incoming("IN1"), self.two_rules(), prefix="E1")
        e = self.net.read("IN1_DEPENDS_ON_DEBT_RULE5")
        self.assertEqual((e.f("CHECK"), e.f("RULE"), e.f("REASON")), ("VALIDATE_INCOMING", "RULE5", "SCHEMA_DRIFT"))
        self.assertEqual(e.status_log[-1].state, "UNCHECKED")

    def test_debt_to_dependents_for_targeted_recheck(self):
        for i in (1, 2):
            admit(self.net, self.d, incoming(f"IN{i}"), self.two_rules(), prefix=f"E{i}")
        admit(self.net, self.d, incoming("IN3"), HandlerResult(), prefix="E3")
        self.assertEqual(dependents_of(self.net, debt_addr("RULE2")), ["IN1", "IN2"])


if __name__ == "__main__":
    unittest.main()
