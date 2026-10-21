#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WS05 tests: the repaired dictionary contract is self-consistent.

These tests instantiate the dictionary's own shape templates with synthetic,
world-free identifiers and run them through the FROZEN handler code. They
show that the contract now says what the handlers read. They say nothing
about whether a cold translator will land on it (that is exam mode).
"""
from pathlib import Path
import copy, json, subprocess, sys, unittest
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "run_c"), str(HERE)]

from demon_core import Network, Record
from family_executor import _filter_subjects, SchemaError

V2 = ROOT / "current/experiments/GW05_RUN_C_FAMILY_DICTIONARY.json"
V3 = HERE / "dictionary_v0_3.json"
FAM = "CONDITIONAL_NODE_BALANCE_AND_UNIQUE_MISSING_DERIVATION"
FILL = {"<PREDICATE>": "in_container", "<TARGET>": "scoped_node"}


def fill(node):
    if isinstance(node, dict):
        return {k: fill(v) for k, v in node.items()}
    if isinstance(node, list):
        return [fill(v) for v in node if v != "..."]
    return FILL.get(node, node)


def gate(path):
    return subprocess.run([sys.executable, str(HERE / "dictionary_gate.py"), str(path)],
                          capture_output=True, text=True).returncode


class DictionaryV03Test(unittest.TestCase):
    def setUp(self):
        self.d = json.loads(V3.read_text(encoding="utf-8"))["families"][FAM]
        self.net = Network()
        for addr, s in (("x", "item_a"), ("y", "item_b")):
            r = Record(addr, {"SUBJECT": s, "PREDICATE": "in_container", "OBJECT": "box"})
            self.net.records[addr] = r; r.committed = True; self.net.mark(addr, "CURRENT")

    def test_gate_fails_frozen_v02_passes_v03(self):
        self.assertEqual(gate(V2), 1)     # would have caught the Q2/Q4 leak
        self.assertEqual(gate(V3), 0)

    def test_documented_predicate_target_shape_executes(self):
        shape = fill(self.d["filter_variant_shapes"]["predicate_target"]["shape"])
        self.assertEqual(_filter_subjects(self.net, shape, "box"), {"item_a", "item_b"})

    def test_wrapped_reading_is_what_the_handler_rejects(self):
        wrapped = {"predicate_target": fill(self.d["filter_variant_shapes"]["predicate_target"]["shape"])}
        with self.assertRaises(SchemaError):
            _filter_subjects(self.net, wrapped, "box")

    def test_documented_all_shape_with_relation_executes(self):
        pt = fill(self.d["filter_variant_shapes"]["predicate_target"]["shape"])
        rel = self.d["filter_variant_shapes"]["other_members_than_other_side"]["shape"]
        self.assertEqual(_filter_subjects(self.net, {"all": [pt, rel]}, "box", {"item_a"}), {"item_b"})

    def test_world_token_gone_and_replacement_parameterized(self):
        flat = json.dumps(self.d)
        self.assertNotIn("Q2", flat); self.assertNotIn("Q4", flat)
        cond = self.d["condition_shapes"]["members_lacking_value"]["shape"]["members_lacking_value"]
        self.assertEqual(cond["value_predicate"], "<PREDICATE>")

    def test_frozen_v02_untouched(self):
        self.assertIn("adjacent_links_lacking_Q2_or_Q4", V2.read_text(encoding="utf-8"))

    def test_build_is_reproducible(self):
        sys.path.insert(0, str(HERE))
        from make_dictionary_v2 import build
        rebuilt = build(json.loads(V2.read_text(encoding="utf-8")))
        self.assertEqual(rebuilt, json.loads(V3.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
