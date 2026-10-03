#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
EVALUATOR_PATH = ROOT / "experiments" / "experiment_003" / "evaluator.py"

def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_evaluator():
    spec = importlib.util.spec_from_file_location("noepedia_evaluator", EVALUATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.evaluate

def sig(e):
    return {
        "event": e.get("event"), "rule": e.get("rule"), "subject": e.get("subject"),
        "input_relations": e.get("input_relations"),
        "input_relations_1": e.get("input_relations_1"),
        "input_relations_2": e.get("input_relations_2"),
        "expected_target": (e.get("derived_requirement") or {}).get("target"),
        "conflicting_relation": e.get("conflicting_relation"),
        "stored_target": e.get("stored_target"),
        "satisfying_relations": e.get("satisfying_relations"),
    }

def expected_sig(e):
    return {
        "event": e.get("event"), "rule": e.get("rule"), "subject": e.get("subject"),
        "input_relations": e.get("input_relations"),
        "input_relations_1": e.get("input_relations_1"),
        "input_relations_2": e.get("input_relations_2"),
        "expected_target": e.get("expected_target"),
        "conflicting_relation": e.get("conflicting_relation"),
        "stored_target": e.get("stored_target"),
        "satisfying_relations": e.get("satisfying_relations"),
    }

def key(x):
    return (str(x["event"]), str(x["subject"]), str(x["rule"]))

def main():
    evaluate = load_evaluator()
    actual = evaluate(load_json(HERE / "INPUT.json"))
    expected = load_json(HERE / "EXPECTED_OUTPUT.json")
    errors = []

    if actual.get("experiment") != expected.get("experiment"):
        errors.append("experiment id differs")
    if actual.get("summary") != expected.get("summary"):
        errors.append("summary differs")

    a = sorted((sig(e) for e in actual.get("events", [])), key=key)
    b = sorted((expected_sig(e) for e in expected.get("required_events", [])), key=key)
    if a != b:
        errors.append("event set differs\nACTUAL:\n" + json.dumps(a, indent=2) +
                      "\nEXPECTED:\n" + json.dumps(b, indent=2))
    if actual.get("open_preserved") != expected.get("open_preserved"):
        errors.append("OPEN preservation differs")
    if actual.get("open_records_unchanged") != expected.get("open_records_unchanged"):
        errors.append("OPEN mutation flag differs")

    if errors:
        print("Experiment 005 verification: FAIL")
        for e in errors:
            print("- " + e)
        return 1
    print("Experiment 005 verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
