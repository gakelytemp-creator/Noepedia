#!/usr/bin/env python3
"""Minimal deterministic evaluator for Noepedia Experiment 003.

Detection only. No repair selection, no LLM calls, no domain-specific
knowledge, and no mutation of OPEN records.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any


REQUIRED_RULE_FIELDS = {
    "RULE_SCOPE",
    "INPUT_PREDICATE",
    "REQUIRED_PREDICATE",
    "TARGET_CONSTRAINT",
}


def _index_relations(relations: list[dict[str, Any]]):
    by_subject = defaultdict(list)
    by_subject_predicate = defaultdict(list)
    for rel in relations:
        by_subject[rel["subject"]].append(rel)
        by_subject_predicate[(rel["subject"], rel["predicate"])].append(rel)
    return by_subject, by_subject_predicate


def _rule_spec(rule_id: str, rule_relations: list[dict[str, Any]]) -> dict[str, Any]:
    parts = [r for r in rule_relations if r["subject"] == rule_id]
    fields = {r["predicate"]: r for r in parts}

    missing = sorted(REQUIRED_RULE_FIELDS - fields.keys())
    if missing:
        return {
            "complete": False,
            "rule": rule_id,
            "missing_fields": missing,
            "rule_path": [r["id"] for r in parts],
        }

    return {
        "complete": True,
        "rule": rule_id,
        "scope_type": fields["RULE_SCOPE"]["object"],
        "input_predicate": fields["INPUT_PREDICATE"]["object"],
        "required_predicate": fields["REQUIRED_PREDICATE"]["object"],
        "target_constraint": fields["TARGET_CONSTRAINT"]["object"],
        "rule_path": [
            fields["RULE_SCOPE"]["id"],
            fields["INPUT_PREDICATE"]["id"],
            fields["REQUIRED_PREDICATE"]["id"],
            fields["TARGET_CONSTRAINT"]["id"],
        ],
    }


def evaluate(field: dict[str, Any]) -> dict[str, Any]:
    """Evaluate explicit consistency rules against a Noepedia JSON field."""

    objects = field.get("objects", [])
    relations = field.get("relations", [])
    rule_relations = field.get("rules", [])
    open_records = deepcopy(field.get("open", []))

    object_by_id = {obj["id"]: obj for obj in objects}
    _, rel_by_subject_predicate = _index_relations(relations)

    rule_objects = [obj for obj in objects if obj.get("type") == "consistency_rule"]

    events: list[dict[str, Any]] = []

    for rule_obj in rule_objects:
        rule_id = rule_obj["id"]
        spec = _rule_spec(rule_id, rule_relations)

        if not spec["complete"]:
            events.append({
                "event": "RULE_INCOMPLETE",
                "rule": rule_id,
                "missing_fields": spec["missing_fields"],
                "rule_path": spec["rule_path"],
            })
            continue

        if spec["target_constraint"] != "SAME_NET":
            events.append({
                "event": "RULE_INCOMPLETE",
                "rule": rule_id,
                "missing_fields": ["SUPPORTED_TARGET_CONSTRAINT"],
                "observed_constraint": spec["target_constraint"],
                "rule_path": spec["rule_path"],
            })
            continue

        scoped_subjects = [
            obj["id"] for obj in objects
            if obj.get("type") == spec["scope_type"]
        ]

        if not scoped_subjects:
            events.append({
                "event": "SCOPE_UNRESOLVED",
                "rule": rule_id,
                "scope_type": spec["scope_type"],
                "rule_path": spec["rule_path"],
            })
            continue

        for subject in scoped_subjects:
            input_relations = rel_by_subject_predicate.get(
                (subject, spec["input_predicate"]), []
            )

            for input_rel in input_relations:
                expected_target = input_rel["object"]
                stored_required = rel_by_subject_predicate.get(
                    (subject, spec["required_predicate"]), []
                )

                exact = [r for r in stored_required if r["object"] == expected_target]
                differing = [r for r in stored_required if r["object"] != expected_target]

                if exact:
                    events.append({
                        "event": "CONSISTENT",
                        "rule": rule_id,
                        "subject": subject,
                        "input_relation": input_rel["id"],
                        "derived_requirement": {
                            "predicate": spec["required_predicate"],
                            "target": expected_target,
                        },
                        "satisfying_relations": [r["id"] for r in exact],
                        "constraint": spec["target_constraint"],
                        "rule_path": spec["rule_path"],
                    })
                elif differing:
                    for conflict in differing:
                        events.append({
                            "event": "FORMAL_MISMATCH",
                            "rule": rule_id,
                            "subject": subject,
                            "input_relation": input_rel["id"],
                            "derived_requirement": {
                                "predicate": spec["required_predicate"],
                                "target": expected_target,
                            },
                            "conflicting_relation": conflict["id"],
                            "stored_target": conflict["object"],
                            "constraint": spec["target_constraint"],
                            "rule_path": spec["rule_path"],
                            "conflicting_relation_status": conflict.get("status"),
                            "conflicting_relation_provenance": conflict.get("provenance", []),
                        })
                else:
                    events.append({
                        "event": "REQUIRED_RELATION_MISSING",
                        "rule": rule_id,
                        "subject": subject,
                        "input_relation": input_rel["id"],
                        "derived_requirement": {
                            "predicate": spec["required_predicate"],
                            "target": expected_target,
                        },
                        "constraint": spec["target_constraint"],
                        "rule_path": spec["rule_path"],
                    })

    return {
        "experiment": field.get("experiment_id"),
        "events": events,
        "open_preserved": [item["id"] for item in open_records],
        "open_records_unchanged": open_records == field.get("open", []),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {Path(argv[0]).name} INPUT.json", file=sys.stderr)
        return 2

    path = Path(argv[1])
    with path.open("r", encoding="utf-8") as f:
        field = json.load(f)

    result = evaluate(field)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
