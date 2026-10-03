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


if __name__ == "__main__":
    unittest.main()
