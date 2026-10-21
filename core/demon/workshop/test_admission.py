#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Workshop tests for admission.py on a tiny synthetic network (no GW content)."""
from pathlib import Path
import sys, unittest
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "run_c"), str(HERE)]

from demon_core import Network, Demon, Record, GO, BLOCK, NEED
from family_executor import HandlerResult
from admission import admit, install_default_policy, compose_evidence, POLICY_ADDR


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
        install_default_policy(self.net, self.d)

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

    def test_composition_keeps_every_signal(self):
        both = blocked(); both.unchecked_dependencies = unchecked().unchecked_dependencies
        self.assertEqual([e["KIND"] for e in compose_evidence(both)], ["CONFLICT", "UNCHECKED"])


if __name__ == "__main__":
    unittest.main()
