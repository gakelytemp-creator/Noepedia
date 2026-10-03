#!/usr/bin/env python3
"""Independent structural verifier for Noepedia Experiment 004."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
EVALUATOR_PATH = ROOT / "experiments" / "experiment_003" / "evaluator.py"
INPUT_PATH = HERE / "INPUT.json"
EXPECTED_PATH = HERE / "EXPECTED_OUTPUT.json"


def load_evaluator():
    spec = importlib.util.spec_from_file_location("noepedia_evaluator", EVALUATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load evaluator.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.evaluate


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def event_signature(event):
    return {
        "event": event.get("event"),
        "rule": event.get("rule"),
        "subject": event.get("subject"),
        "input_relation": event.get("input_relation"),
        "conflicting_relation": event.get("conflicting_relation"),
        "expected_target": (event.get("derived_requirement") or {}).get("target"),
        "stored_target": event.get("stored_target"),
        "satisfying_relations": sorted(event.get("satisfying_relations", [])),
    }


def expected_signature(event):
    return {
        "event": event.get("event"),
        "rule": event.get("rule"),
        "subject": event.get("subject"),
        "input_relation": event.get("input_relation"),
        "conflicting_relation": event.get("conflicting_relation"),
        "expected_target": event.get("expected_target"),
        "stored_target": event.get("stored_target"),
        "satisfying_relations": sorted(event.get("satisfying_relations", [])),
    }


def main() -> int:
    evaluate = load_evaluator()
    field = load_json(INPUT_PATH)
    expected = load_json(EXPECTED_PATH)
    actual = evaluate(field)

    errors = []

    if actual.get("experiment") != expected.get("experiment"):
        errors.append(
            f"experiment mismatch: {actual.get('experiment')} != {expected.get('experiment')}"
        )

    if actual.get("summary") != expected.get("summary"):
        errors.append(
            f"summary mismatch: {actual.get('summary')} != {expected.get('summary')}"
        )

    actual_events = sorted(
        (event_signature(e) for e in actual.get("events", [])),
        key=lambda x: (
            str(x["event"]),
            str(x["rule"]),
            str(x["subject"]),
            str(x["input_relation"]),
        ),
    )
    expected_events = sorted(
        (expected_signature(e) for e in expected.get("required_events", [])),
        key=lambda x: (
            str(x["event"]),
            str(x["rule"]),
            str(x["subject"]),
            str(x["input_relation"]),
        ),
    )

    if actual_events != expected_events:
        errors.append(
            "event set mismatch\n"
            + "ACTUAL:\n"
            + json.dumps(actual_events, indent=2, ensure_ascii=False)
            + "\nEXPECTED:\n"
            + json.dumps(expected_events, indent=2, ensure_ascii=False)
        )

    if sorted(actual.get("open_preserved", [])) != sorted(expected.get("open_preserved", [])):
        errors.append(
            f"OPEN preservation mismatch: {actual.get('open_preserved')} != {expected.get('open_preserved')}"
        )

    if actual.get("open_records_unchanged") != expected.get("open_records_unchanged"):
        errors.append(
            "open_records_unchanged mismatch: "
            f"{actual.get('open_records_unchanged')} != {expected.get('open_records_unchanged')}"
        )

    if errors:
        print("Experiment 004 verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Experiment 004 verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
