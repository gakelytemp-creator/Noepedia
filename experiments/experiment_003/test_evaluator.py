#!/usr/bin/env python3
import copy
import json
import unittest
from pathlib import Path

from evaluator import evaluate


HERE = Path(__file__).resolve().parent
BASE_INPUT = HERE.parent / "experiment_002" / "INPUT.json"


def load_base():
    with BASE_INPUT.open("r", encoding="utf-8") as f:
        return json.load(f)


def event_types(result):
    return [e["event"] for e in result["events"]]


class EvaluatorTests(unittest.TestCase):
    def test_known_mismatch(self):
        field = load_base()
        result = evaluate(field)

        mismatches = [e for e in result["events"] if e["event"] == "FORMAL_MISMATCH"]
        self.assertTrue(any(
            e["subject"] == "J2_P1"
            and e["input_relation"] == "R18"
            and e["conflicting_relation"] == "R13"
            and e["derived_requirement"]["target"] == "VOUT"
            and e["stored_target"] == "VIN"
            for e in mismatches
        ))
        self.assertIn("OPEN_01", result["open_preserved"])
        self.assertTrue(result["open_records_unchanged"])

    def test_corrected_field(self):
        field = load_base()
        for rel in field["relations"]:
            if rel["id"] == "R13":
                rel["object"] = "VOUT"

        result = evaluate(field)
        relevant = [
            e for e in result["events"]
            if e.get("subject") == "J2_P1" and e.get("input_relation") == "R18"
        ]
        self.assertEqual([e["event"] for e in relevant], ["CONSISTENT"])

    def test_required_relation_missing(self):
        field = load_base()
        field["relations"] = [r for r in field["relations"] if r["id"] != "R13"]

        result = evaluate(field)
        relevant = [
            e for e in result["events"]
            if e.get("subject") == "J2_P1" and e.get("input_relation") == "R18"
        ]
        self.assertEqual([e["event"] for e in relevant], ["REQUIRED_RELATION_MISSING"])

    def test_incomplete_rule(self):
        field = load_base()
        field["rules"] = [r for r in field["rules"] if r["id"] != "RR04"]

        result = evaluate(field)
        incomplete = [e for e in result["events"] if e["event"] == "RULE_INCOMPLETE"]
        self.assertEqual(len(incomplete), 1)
        self.assertEqual(incomplete[0]["rule"], "RULE_TERMINAL_EXPOSE_CONNECT")
        self.assertIn("TARGET_CONSTRAINT", incomplete[0]["missing_fields"])


    def test_multiple_rules_are_generic(self):
        field = {
            "experiment_id": "MULTI_RULE_TEST",
            "objects": [
                {"id": "A", "type": "type_a"},
                {"id": "B", "type": "type_b"},
                {"id": "X", "type": "target"},
                {"id": "Y", "type": "target"},
                {"id": "RULE_A", "type": "consistency_rule"},
                {"id": "RULE_B", "type": "consistency_rule"},
            ],
            "relations": [
                {"id": "A1", "subject": "A", "predicate": "P", "object": "X", "network": "N", "status": "settled", "provenance": []},
                {"id": "A2", "subject": "A", "predicate": "Q", "object": "Y", "network": "N", "status": "settled", "provenance": []},
                {"id": "B1", "subject": "B", "predicate": "R", "object": "X", "network": "N", "status": "settled", "provenance": []},
                {"id": "B2", "subject": "B", "predicate": "S", "object": "X", "network": "N", "status": "settled", "provenance": []},
            ],
            "rules": [
                {"id": "RA1", "subject": "RULE_A", "predicate": "RULE_SCOPE", "object": "type_a", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RA2", "subject": "RULE_A", "predicate": "INPUT_PREDICATE", "object": "P", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RA3", "subject": "RULE_A", "predicate": "REQUIRED_PREDICATE", "object": "Q", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RA4", "subject": "RULE_A", "predicate": "TARGET_CONSTRAINT", "object": "SAME_NET", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RB1", "subject": "RULE_B", "predicate": "RULE_SCOPE", "object": "type_b", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RB2", "subject": "RULE_B", "predicate": "INPUT_PREDICATE", "object": "R", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RB3", "subject": "RULE_B", "predicate": "REQUIRED_PREDICATE", "object": "S", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RB4", "subject": "RULE_B", "predicate": "TARGET_CONSTRAINT", "object": "SAME_NET", "network": "RULE", "status": "settled", "provenance": []},
            ],
            "open": [],
        }

        result = evaluate(field)
        self.assertEqual(result["summary"]["rule_count"], 2)
        self.assertEqual(result["summary"]["event_counts"].get("FORMAL_MISMATCH"), 1)
        self.assertEqual(result["summary"]["event_counts"].get("CONSISTENT"), 1)

        mismatch = [e for e in result["events"] if e["event"] == "FORMAL_MISMATCH"][0]
        self.assertEqual(mismatch["rule"], "RULE_A")
        self.assertEqual(mismatch["subject"], "A")

        consistent = [e for e in result["events"] if e["event"] == "CONSISTENT"][0]
        self.assertEqual(consistent["rule"], "RULE_B")
        self.assertEqual(consistent["subject"], "B")


    def test_two_input_rule(self):
        field = {
            "experiment_id": "TWO_INPUT_TEST",
            "objects": [
                {"id": "A", "type": "node"},
                {"id": "X", "type": "target"},
                {"id": "Y", "type": "target"},
                {"id": "RULE", "type": "consistency_rule"},
            ],
            "relations": [
                {"id": "A1", "subject": "A", "predicate": "P", "object": "X", "network": "N", "status": "settled", "provenance": []},
                {"id": "A2", "subject": "A", "predicate": "Q", "object": "X", "network": "N", "status": "settled", "provenance": []},
                {"id": "A3", "subject": "A", "predicate": "R", "object": "Y", "network": "N", "status": "settled", "provenance": []},
            ],
            "rules": [
                {"id": "RR1", "subject": "RULE", "predicate": "RULE_ARITY", "object": "2", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RR2", "subject": "RULE", "predicate": "RULE_SCOPE", "object": "node", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RR3", "subject": "RULE", "predicate": "INPUT_PREDICATE_1", "object": "P", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RR4", "subject": "RULE", "predicate": "INPUT_PREDICATE_2", "object": "Q", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RR5", "subject": "RULE", "predicate": "INPUT_JOIN_CONSTRAINT", "object": "SAME_OBJECT", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RR6", "subject": "RULE", "predicate": "REQUIRED_PREDICATE", "object": "R", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "RR7", "subject": "RULE", "predicate": "REQUIRED_TARGET_SOURCE", "object": "INPUT_1_OBJECT", "network": "RULE", "status": "settled", "provenance": []},
            ],
            "open": [],
        }
        result = evaluate(field)
        self.assertEqual(result["summary"]["event_counts"].get("FORMAL_MISMATCH"), 1)
        event = result["events"][0]
        self.assertEqual(event["subject"], "A")
        self.assertEqual(event["input_relations"], ["A1", "A2"])
        self.assertEqual(event["derived_requirement"]["target"], "X")
        self.assertEqual(event["conflicting_relation"], "A3")


    def test_cross_subject_join_rule(self):
        field = {
            "experiment_id": "CROSS_SUBJECT_TEST",
            "objects": [
                {"id": "L", "type": "left"},
                {"id": "R", "type": "right"},
                {"id": "BAD", "type": "right"},
                {"id": "X", "type": "join"},
                {"id": "RULE_X", "type": "consistency_rule"},
            ],
            "relations": [
                {"id": "LP", "subject": "L", "predicate": "P", "object": "X", "network": "N", "status": "settled", "provenance": []},
                {"id": "RQ", "subject": "R", "predicate": "Q", "object": "X", "network": "N", "status": "settled", "provenance": []},
                {"id": "LR", "subject": "L", "predicate": "REL", "object": "BAD", "network": "N", "status": "settled", "provenance": []},
            ],
            "rules": [
                {"id": "XR1", "subject": "RULE_X", "predicate": "RULE_ARITY", "object": "2", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR2", "subject": "RULE_X", "predicate": "RULE_PATTERN", "object": "CROSS_SUBJECT_SHARED_OBJECT", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR3", "subject": "RULE_X", "predicate": "INPUT_SUBJECT_TYPE_1", "object": "left", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR4", "subject": "RULE_X", "predicate": "INPUT_PREDICATE_1", "object": "P", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR5", "subject": "RULE_X", "predicate": "INPUT_SUBJECT_TYPE_2", "object": "right", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR6", "subject": "RULE_X", "predicate": "INPUT_PREDICATE_2", "object": "Q", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR7", "subject": "RULE_X", "predicate": "INPUT_JOIN_CONSTRAINT", "object": "SAME_OBJECT", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR8", "subject": "RULE_X", "predicate": "REQUIRED_SUBJECT_SOURCE", "object": "INPUT_1_SUBJECT", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR9", "subject": "RULE_X", "predicate": "REQUIRED_PREDICATE", "object": "REL", "network": "RULE", "status": "settled", "provenance": []},
                {"id": "XR10", "subject": "RULE_X", "predicate": "REQUIRED_TARGET_SOURCE", "object": "INPUT_2_SUBJECT", "network": "RULE", "status": "settled", "provenance": []},
            ],
            "open": [],
        }
        result = evaluate(field)
        mismatches = [e for e in result["events"] if e["event"] == "FORMAL_MISMATCH"]
        self.assertEqual(len(mismatches), 1)
        event = mismatches[0]
        self.assertEqual(event["subject"], "L")
        self.assertEqual(event["input_relations"], ["LP", "RQ"])
        self.assertEqual(event["derived_requirement"]["target"], "R")
        self.assertEqual(event["conflicting_relation"], "LR")


if __name__ == "__main__":
    unittest.main()
