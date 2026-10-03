#!/usr/bin/env python3
"""Deterministic rule evaluator for Noepedia experiments.

Detection only. No repair selection, no LLM calls, no domain-specific
knowledge, and no mutation of OPEN records.

Supported:
- one-input SAME_NET rules
- two-input SAME_OBJECT join rules
"""

from __future__ import annotations
import json
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

LEGACY_REQUIRED_RULE_FIELDS = {
    "RULE_SCOPE", "INPUT_PREDICATE", "REQUIRED_PREDICATE", "TARGET_CONSTRAINT",
}
TWO_INPUT_REQUIRED_RULE_FIELDS = {
    "RULE_ARITY", "RULE_SCOPE", "INPUT_PREDICATE_1", "INPUT_PREDICATE_2",
    "INPUT_JOIN_CONSTRAINT", "REQUIRED_PREDICATE", "REQUIRED_TARGET_SOURCE",
}

def _index_relations(relations: list[dict[str, Any]]):
    by_subject_predicate = defaultdict(list)
    for rel in relations:
        by_subject_predicate[(rel["subject"], rel["predicate"])].append(rel)
    return by_subject_predicate

def _rule_spec(rule_id: str, rule_relations: list[dict[str, Any]]) -> dict[str, Any]:
    parts = [r for r in rule_relations if r["subject"] == rule_id]
    fields = {r["predicate"]: r for r in parts}
    arity = str(fields.get("RULE_ARITY", {}).get("object", "1"))

    if arity == "1":
        missing = sorted(LEGACY_REQUIRED_RULE_FIELDS - fields.keys())
        if missing:
            return {"complete": False, "rule": rule_id, "arity": 1,
                    "missing_fields": missing, "rule_path": [r["id"] for r in parts]}
        return {
            "complete": True, "rule": rule_id, "arity": 1,
            "scope_type": fields["RULE_SCOPE"]["object"],
            "input_predicate": fields["INPUT_PREDICATE"]["object"],
            "required_predicate": fields["REQUIRED_PREDICATE"]["object"],
            "target_constraint": fields["TARGET_CONSTRAINT"]["object"],
            "rule_path": [
                fields["RULE_SCOPE"]["id"], fields["INPUT_PREDICATE"]["id"],
                fields["REQUIRED_PREDICATE"]["id"], fields["TARGET_CONSTRAINT"]["id"],
            ],
        }

    if arity == "2":
        missing = sorted(TWO_INPUT_REQUIRED_RULE_FIELDS - fields.keys())
        if missing:
            return {"complete": False, "rule": rule_id, "arity": 2,
                    "missing_fields": missing, "rule_path": [r["id"] for r in parts]}
        return {
            "complete": True, "rule": rule_id, "arity": 2,
            "scope_type": fields["RULE_SCOPE"]["object"],
            "input_predicate_1": fields["INPUT_PREDICATE_1"]["object"],
            "input_predicate_2": fields["INPUT_PREDICATE_2"]["object"],
            "input_join_constraint": fields["INPUT_JOIN_CONSTRAINT"]["object"],
            "required_predicate": fields["REQUIRED_PREDICATE"]["object"],
            "required_target_source": fields["REQUIRED_TARGET_SOURCE"]["object"],
            "rule_path": [
                fields["RULE_ARITY"]["id"], fields["RULE_SCOPE"]["id"],
                fields["INPUT_PREDICATE_1"]["id"], fields["INPUT_PREDICATE_2"]["id"],
                fields["INPUT_JOIN_CONSTRAINT"]["id"], fields["REQUIRED_PREDICATE"]["id"],
                fields["REQUIRED_TARGET_SOURCE"]["id"],
            ],
        }

    return {"complete": False, "rule": rule_id, "arity": arity,
            "missing_fields": ["SUPPORTED_RULE_ARITY"],
            "rule_path": [r["id"] for r in parts]}

def _compare_requirement(rule_id, subject, input_relations, required_predicate,
                         expected_target, constraint, rule_path, index):
    stored = index.get((subject, required_predicate), [])
    exact = [r for r in stored if r["object"] == expected_target]
    differing = [r for r in stored if r["object"] != expected_target]
    common = {
        "rule": rule_id, "subject": subject, "input_relations": input_relations,
        "derived_requirement": {"predicate": required_predicate, "target": expected_target},
        "constraint": constraint, "rule_path": rule_path,
    }
    if len(input_relations) == 1:
        common["input_relation"] = input_relations[0]
    if exact:
        return [{"event": "CONSISTENT", **common,
                 "satisfying_relations": [r["id"] for r in exact]}]
    if differing:
        return [{
            "event": "FORMAL_MISMATCH", **common,
            "conflicting_relation": r["id"], "stored_target": r["object"],
            "conflicting_relation_status": r.get("status"),
            "conflicting_relation_provenance": r.get("provenance", []),
        } for r in differing]
    return [{"event": "REQUIRED_RELATION_MISSING", **common}]

def _evaluate_one_input(spec, subjects, index):
    if spec["target_constraint"] != "SAME_NET":
        return [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                 "missing_fields": ["SUPPORTED_TARGET_CONSTRAINT"],
                 "observed_constraint": spec["target_constraint"],
                 "rule_path": spec["rule_path"]}]
    events = []
    for subject in subjects:
        for rel in index.get((subject, spec["input_predicate"]), []):
            events.extend(_compare_requirement(
                spec["rule"], subject, [rel["id"]], spec["required_predicate"],
                rel["object"], spec["target_constraint"], spec["rule_path"], index))
    return events

def _evaluate_two_input(spec, subjects, index):
    if spec["input_join_constraint"] != "SAME_OBJECT":
        return [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                 "missing_fields": ["SUPPORTED_INPUT_JOIN_CONSTRAINT"],
                 "observed_constraint": spec["input_join_constraint"],
                 "rule_path": spec["rule_path"]}]
    if spec["required_target_source"] != "INPUT_1_OBJECT":
        return [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                 "missing_fields": ["SUPPORTED_REQUIRED_TARGET_SOURCE"],
                 "observed_target_source": spec["required_target_source"],
                 "rule_path": spec["rule_path"]}]
    events = []
    for subject in subjects:
        left = index.get((subject, spec["input_predicate_1"]), [])
        right = index.get((subject, spec["input_predicate_2"]), [])
        pairs = [(a, b) for a in left for b in right if a["object"] == b["object"]]
        if not pairs and left and right:
            events.append({
                "event": "ANTECEDENT_NOT_SATISFIED", "rule": spec["rule"],
                "subject": subject,
                "input_relations_1": [r["id"] for r in left],
                "input_relations_2": [r["id"] for r in right],
                "constraint": spec["input_join_constraint"],
                "rule_path": spec["rule_path"],
            })
            continue
        for a, b in pairs:
            events.extend(_compare_requirement(
                spec["rule"], subject, [a["id"], b["id"]],
                spec["required_predicate"], a["object"],
                spec["input_join_constraint"], spec["rule_path"], index))
    return events

def evaluate(field: dict[str, Any]) -> dict[str, Any]:
    objects = field.get("objects", [])
    index = _index_relations(field.get("relations", []))
    rules = field.get("rules", [])
    open_records = deepcopy(field.get("open", []))
    rule_objects = [o for o in objects if o.get("type") == "consistency_rule"]
    events = []

    for obj in rule_objects:
        spec = _rule_spec(obj["id"], rules)
        if not spec["complete"]:
            events.append({
                "event": "RULE_INCOMPLETE", "rule": obj["id"],
                "rule_arity": spec.get("arity"),
                "missing_fields": spec["missing_fields"],
                "rule_path": spec["rule_path"],
            })
            continue

        subjects = [o["id"] for o in objects if o.get("type") == spec["scope_type"]]
        if not subjects:
            events.append({"event": "SCOPE_UNRESOLVED", "rule": obj["id"],
                           "scope_type": spec["scope_type"],
                           "rule_path": spec["rule_path"]})
            continue

        if spec["arity"] == 1:
            events.extend(_evaluate_one_input(spec, subjects, index))
        elif spec["arity"] == 2:
            events.extend(_evaluate_two_input(spec, subjects, index))

    counts = {}
    for event in events:
        counts[event["event"]] = counts.get(event["event"], 0) + 1

    return {
        "experiment": field.get("experiment_id"),
        "events": events,
        "summary": {"rule_count": len(rule_objects), "event_counts": counts},
        "open_preserved": [o["id"] for o in open_records],
        "open_records_unchanged": open_records == field.get("open", []),
    }

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {Path(argv[0]).name} INPUT.json", file=sys.stderr)
        return 2
    with Path(argv[1]).open("r", encoding="utf-8") as f:
        field = json.load(f)
    json.dump(evaluate(field), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
