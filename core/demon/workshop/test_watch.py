#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WS07 tests for watch.py on a tiny synthetic network (no GW content)."""
from pathlib import Path
import sys, unittest
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "run_c"), str(HERE)]

from demon_core import Network, Demon, Record, ASK
from c1_c3_overlay import C1C3Overlay
from resolution import effective_ask_state, answer_on_bind, effectively_open_asks
from watch import (watch_requirement, issue_mandate, current_mandate, bind, binding_state,
                   on_basis_lost, current_candidacies, requirement_variable, current_ambiguities,
                   ONE_SHOT, STANDING_WHILE, AUTO_BIND)

STANDING = {"RECORD": "RQ", "STATE_IN": ["OPEN"]}


class WatchTest(unittest.TestCase):
    def setUp(self):
        self.net = Network(); self.d = Demon(self.net); self.c = C1C3Overlay(self.net)
        for a, (s, p, o) in {"P1": ("?X", "q", "a"), "P2": ("?X", "q", "b")}.items():
            self.d.commit(self.d.propose(add=[Record(a, {"TYPE": "TRIPLET_PATTERN",
                                                         "SUBJECT": s, "PREDICATE": p, "OBJECT": o})]))
        self.d.commit(self.d.propose(add=[Record("T", {"TYPE": "TASK", "REQUIRED_PATTERNS": ["P1", "P2"]})]))
        self.d.commit(self.d.propose(add=[Record("RQ", {"TYPE": "REQUIREMENT_CONCEPT",
                                                        "REQUIREMENT": ["P1", "P2"]})],
                                     mark=[("RQ", "OPEN")], authorized_by="T"))

    def fact(self, addr, s, o):
        self.d.commit(self.d.propose(add=[Record(addr, {"SUBJECT": s, "PREDICATE": "q", "OBJECT": o})],
                                     mark=[(addr, "CURRENT")]))
        return watch_requirement(self.net, self.d, self.c, "RQ")

    def test_watch_creates_candidacy_but_does_not_bind(self):
        self.fact("f1", "z", "a"); out = self.fact("f2", "z", "b")
        self.assertEqual(len(out["created"]), 1)
        c = self.net.read(out["created"][0])
        self.assertEqual((c.f("CANDIDATE"), c.f("N"), c.f("SCOPE"), c.f("METHOD")),
                         ("z", out["N"], "CURRENT_FACTS", "C1_JOINT_BINDINGS"))
        self.assertIn(f"_N{out['N']}", c.addr)
        self.assertEqual(self.net.read("RQ").status_log[-1].state, "OPEN")       # watch != decision

    def test_explicit_bind_records_basis(self):
        self.fact("f1", "z", "a"); c = self.fact("f2", "z", "b")["created"][0]
        b = bind(self.net, self.d, "RQ", c, authorized_by="T")
        self.assertEqual(self.net.read(f"{b}_SUPPORTED_BY_1").f("OBJECT"), c)
        self.assertEqual(binding_state(self.net, b), "SUPPORTED")

    def test_issuer_cannot_be_the_operation(self):
        with self.assertRaises(PermissionError):
            issue_mandate(self.net, self.d, "M", "T", issuer=AUTO_BIND)

    def test_one_shot_mandate_is_used_up(self):
        m = issue_mandate(self.net, self.d, "M", "T", issuer="UPPER")
        self.fact("f1", "z", "a"); c = self.fact("f2", "z", "b")["created"][0]
        self.assertEqual(current_mandate(self.net, "T"), m)
        bind(self.net, self.d, "RQ", c, authorized_by=m)
        self.assertIsNone(current_mandate(self.net, "T"))
        self.assertEqual([s.state for s in self.net.read(m).status_log], ["CURRENT", "HISTORICAL"])

    def test_second_candidate_damages_basis_not_history(self):
        m = issue_mandate(self.net, self.d, "M", "T", issuer="UPPER")
        self.fact("f1", "z", "a"); c = self.fact("f2", "z", "b")["created"][0]
        b = bind(self.net, self.d, "RQ", c, authorized_by=m)
        self.fact("f3", "w", "a"); out = self.fact("f4", "w", "b")
        self.assertEqual(out["historical"], [c])
        self.assertEqual(binding_state(self.net, b), "REVIEW_REQUIRED")
        self.assertIsNotNone(self.net.read(b))                                   # binding kept
        res = on_basis_lost(self.net, self.d, "RQ", b)
        self.assertEqual((res["still_in_force"], res["ask_to"]), (False, "UPPER"))
        self.assertIsNone(current_mandate(self.net, "T"))                        # not revived
        self.assertEqual(self.net.read("RQ").status_log[-1].state, "OPEN")
        self.assertEqual(self.net.stops[-1].stop_class, ASK)

    def test_standing_mandate_needs_checkable_condition(self):
        with self.assertRaises(ValueError):
            issue_mandate(self.net, self.d, "M", "T", issuer="UPPER", lifecycle=STANDING_WHILE,
                          condition="RQ unresolved")

    def test_standing_condition_false_after_bind_true_after_reopen(self):
        m = issue_mandate(self.net, self.d, "M", "T", issuer="UPPER", lifecycle=STANDING_WHILE,
                          condition=STANDING)
        self.fact("f1", "z", "a"); c = self.fact("f2", "z", "b")["created"][0]
        b = bind(self.net, self.d, "RQ", c, authorized_by=m)
        self.assertIsNone(current_mandate(self.net, "T"))          # RQ BOUND -> condition false
        self.assertEqual(self.net.read(m).status_log[-1].state, "CURRENT")  # record not rewritten
        self.fact("f3", "w", "a"); self.fact("f4", "w", "b")
        res = on_basis_lost(self.net, self.d, "RQ", b)
        self.assertTrue(res["still_in_force"])                     # RQ OPEN again -> condition true
        self.assertEqual(current_mandate(self.net, "T"), m)

    def test_sole_ambiguous_sole_again_makes_a_new_claim(self):
        self.fact("f1", "z", "a"); c1 = self.fact("f2", "z", "b")["created"][0]
        self.fact("f3", "w", "a"); amb = self.fact("f4", "w", "b")
        self.assertEqual((amb["historical"], amb["candidates"]), ([c1], ["z", "w"]))
        self.d.commit(self.d.propose(mark=[("f4", "HISTORICAL")]))   # w loses support
        again = watch_requirement(self.net, self.d, self.c, "RQ")
        self.assertEqual(len(again["created"]), 1)
        c2 = again["created"][0]
        self.assertNotEqual(c2, c1)                                  # new snapshot claim
        self.assertEqual(self.net.read(c1).status_log[-1].state, "HISTORICAL")   # old not revived
        self.assertGreater(self.net.read(c2).f("N"), self.net.read(c1).f("N"))
        self.assertEqual(current_candidacies(self.net, "RQ"), [c2])

    def test_unchanged_set_keeps_one_claim(self):
        self.fact("f1", "z", "a"); self.fact("f2", "z", "b")
        out = self.fact("f5", "z", "c")                              # unrelated fact, same set
        self.assertEqual(out["created"], [])
        self.assertEqual(len(current_candidacies(self.net, "RQ")), 1)

    def test_variable_is_the_shared_one(self):
        self.assertEqual(requirement_variable([("?X", "q", "?Y"), ("?X", "r", "b")]), "?X")
        with self.assertRaises(ValueError):
            requirement_variable([("?X", "q", "a"), ("?Y", "q", "b")])

    # ── WS08 ──
    def test_two_candidates_make_ambiguity_record_and_cutting_ask(self):
        self.fact("f1", "z", "a"); self.fact("f2", "z", "b")
        self.fact("f3", "w", "a"); out = self.fact("f4", "w", "b")
        amb = self.net.read(out["ambiguity_created"][0])
        self.assertEqual((amb.f("TYPE"), amb.f("CANDIDATES")), ("AMBIGUOUS_CANDIDATES_ON", ["w", "z"]))
        ask = out["disambiguation_asks"][0]
        self.assertEqual(self.net.read(ask).status_log[-1].state, "OPEN")
        self.assertIn("leaves 1 of 2", self.net.stops[-1].query)
        self.assertEqual(self.net.stops[-1].stop_class, ASK)

    def test_unchanged_ambiguity_asks_once(self):
        self.fact("f1", "z", "a"); self.fact("f2", "z", "b")
        self.fact("f3", "w", "a"); self.fact("f4", "w", "b")
        n = sum(s.stop_class == ASK for s in self.net.stops)
        out = self.fact("f5", "z", "c")                              # same ambiguous set
        self.assertEqual((out["ambiguity_created"], sum(s.stop_class == ASK for s in self.net.stops)), ([], n))

    def test_disambiguation_ask_answered_when_sole_again(self):
        self.fact("f1", "z", "a"); self.fact("f2", "z", "b")
        self.fact("f3", "w", "a"); amb = self.fact("f4", "w", "b")
        ask = amb["disambiguation_asks"][0]
        self.d.commit(self.d.propose(mark=[("f4", "HISTORICAL")]))
        again = watch_requirement(self.net, self.d, self.c, "RQ")
        self.assertEqual(again["disambiguation_answered"], [ask])
        self.assertEqual(effective_ask_state(self.net, ask), "ANSWERED")
        self.assertEqual(current_ambiguities(self.net, "RQ"), [])
        self.assertEqual(self.net.read(amb["ambiguity_created"][0]).status_log[-1].state, "HISTORICAL")

    def test_answered_ask_reopens_when_binding_loses_support(self):
        self.c.requirement_ask("RQ"); self.c.materialize_ask_opens()
        ask = next(r.addr for r in self.net.records.values() if r.f("OPEN_KIND") == "ASK")
        self.fact("f1", "z", "a"); c = self.fact("f2", "z", "b")["created"][0]
        b = bind(self.net, self.d, "RQ", c, authorized_by="T")
        answer_on_bind(self.net, self.d, "RQ", b)
        self.assertEqual(effective_ask_state(self.net, ask), "ANSWERED")
        self.fact("f3", "w", "a"); self.fact("f4", "w", "b")
        self.assertEqual(self.net.read(ask).status_log[-1].state, "ANSWERED")   # stored status untouched
        # the joint ask lost its answer, but a sharper disambiguation ask now supersedes it
        self.assertEqual(effective_ask_state(self.net, ask), "SUPERSEDED")
        self.assertNotIn(ask, effectively_open_asks(self.net))
        amb_ask = [a for a in effectively_open_asks(self.net) if a != ask]
        self.assertEqual(len(amb_ask), 1)

    def test_support_loss_without_ambiguity_reopens(self):
        self.c.requirement_ask("RQ"); self.c.materialize_ask_opens()
        ask = next(r.addr for r in self.net.records.values() if r.f("OPEN_KIND") == "ASK")
        self.fact("f1", "z", "a"); c = self.fact("f2", "z", "b")["created"][0]
        b = bind(self.net, self.d, "RQ", c, authorized_by="T")
        answer_on_bind(self.net, self.d, "RQ", b)
        self.d.commit(self.d.propose(mark=[("f2", "HISTORICAL")]))          # z loses support, no rival
        watch_requirement(self.net, self.d, self.c, "RQ")
        self.assertEqual(effective_ask_state(self.net, ask), "OPEN_BY_SUPPORT_LOSS")
        self.assertIn(ask, effectively_open_asks(self.net))

    # ── WS08b (GPT edge case) ──
    def _joint_answered_then_ambiguous(self):
        self.c.requirement_ask("RQ"); self.c.materialize_ask_opens()
        ask = next(r.addr for r in self.net.records.values() if r.f("OPEN_KIND") == "ASK")
        self.fact("f1", "z", "a"); c = self.fact("f2", "z", "b")["created"][0]
        b = bind(self.net, self.d, "RQ", c, authorized_by="T")
        answer_on_bind(self.net, self.d, "RQ", b)
        self.fact("f3", "w", "a"); amb = self.fact("f4", "w", "b")
        return ask, amb["disambiguation_asks"][0]

    def test_sole_again_without_rebind_keeps_joint_ask_closed(self):
        ask, amb_ask = self._joint_answered_then_ambiguous()
        self.d.commit(self.d.propose(mark=[("f4", "HISTORICAL")]))      # w gone: z sole again
        watch_requirement(self.net, self.d, self.c, "RQ")
        self.assertEqual(effective_ask_state(self.net, amb_ask), "ANSWERED")
        self.assertEqual(effective_ask_state(self.net, ask), "SUPERSEDED")  # not OPEN_BY_SUPPORT_LOSS
        self.assertEqual(effectively_open_asks(self.net), [])

    def test_all_candidates_gone_reopens_joint_ask(self):
        ask, amb_ask = self._joint_answered_then_ambiguous()
        for f in ("f2", "f4"):
            self.d.commit(self.d.propose(mark=[(f, "HISTORICAL")]))
        watch_requirement(self.net, self.d, self.c, "RQ")
        self.assertEqual(effective_ask_state(self.net, ask), "OPEN_BY_SUPPORT_LOSS")
        self.assertEqual(effective_ask_state(self.net, amb_ask), "OBSOLETE")   # "z or w?" no longer exists
        self.assertEqual(effectively_open_asks(self.net), [ask])               # exactly one right question


if __name__ == "__main__":
    unittest.main()
