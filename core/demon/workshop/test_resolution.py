#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Workshop tests for resolution.py (D4) on a tiny synthetic network."""
from pathlib import Path
import sys, unittest
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "run_c"), str(HERE)]

from demon_core import Network, Demon, Record, ASK
from c1_c3_overlay import C1C3Overlay
from resolution import answer_on_bind, unanswered_ask_stops, requirement_ask_opens


class ResolutionTest(unittest.TestCase):
    def setUp(self):
        self.net = Network(); self.d = Demon(self.net); self.c = C1C3Overlay(self.net)
        for a, (s, p, o) in {"P1": ("?X", "Q", "A"), "P2": ("?X", "Q", "B")}.items():
            self.d.commit(self.d.propose(add=[Record(a, {"TYPE": "TRIPLET_PATTERN",
                                                         "SUBJECT": s, "PREDICATE": p, "OBJECT": o})]))
        self.d.commit(self.d.propose(add=[Record("T", {"TYPE": "TASK", "REQUIRED_PATTERNS": ["P1", "P2"]})]))
        self.d.commit(self.d.propose(add=[Record("RQ", {"TYPE": "REQUIREMENT_CONCEPT",
                                                        "REQUIREMENT": ["P1", "P2"]})],
                                     mark=[("RQ", "OPEN")], authorized_by="T"))
        self.c.requirement_ask("RQ"); self.c.materialize_ask_opens()
        self.ask = requirement_ask_opens(self.net, "RQ")[0]

    def bind(self):
        e = Record("RQ_BIND", {"SUBJECT": "RQ", "PREDICATE": "REFERS_TO", "OBJECT": "Z", "ROLE": "BOUND_CANDIDATE"})
        self.d.commit(self.d.propose(add=[e], mark=[("RQ", "BOUND")]))

    def test_frozen_c3_cannot_close_joint_ask(self):
        # the root cause: no single-triplet RESOLUTION_PATTERN
        self.assertIsNone(self.net.read(self.ask).f("RESOLUTION_PATTERN"))

    def test_bind_answers_ask_without_deleting(self):
        self.bind()
        self.assertEqual(answer_on_bind(self.net, self.d, "RQ", "RQ_BIND"), [self.ask])
        log = self.net.read(self.ask).status_log
        self.assertEqual([s.state for s in log], ["OPEN", "ANSWERED"])     # history kept
        self.assertEqual(log[-1].basis, "RQ_BIND")
        self.assertEqual(self.net.refs_from(self.ask, role="ANSWERED_BY")[0].f("OBJECT"), "RQ_BIND")
        self.assertEqual(unanswered_ask_stops(self.net), [])
        self.assertEqual(sum(s.stop_class == ASK for s in self.net.stops), 1)  # stop card kept

    def test_no_binding_no_answer(self):
        self.assertEqual(answer_on_bind(self.net, self.d, "RQ", "RQ_BIND"), [])
        self.assertEqual(self.net.read(self.ask).status_log[-1].state, "OPEN")

    def test_idempotent(self):
        self.bind(); answer_on_bind(self.net, self.d, "RQ", "RQ_BIND")
        self.assertEqual(answer_on_bind(self.net, self.d, "RQ", "RQ_BIND"), [])


if __name__ == "__main__":
    unittest.main()
