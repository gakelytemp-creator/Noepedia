#!/usr/bin/env python3
"""Deterministic rule evaluator for Noepedia experiments.

Detection only. No repair selection, no LLM calls, no domain-specific
knowledge, and no mutation of OPEN records.

Supported:
- one-input SAME_NET rules
- two-input same-subject SAME_OBJECT joins
- two-input cross-subject shared-object joins
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
CROSS_SUBJECT_REQUIRED_RULE_FIELDS = {
    "RULE_ARITY", "RULE_PATTERN",
    "INPUT_SUBJECT_TYPE_1", "INPUT_PREDICATE_1",
    "INPUT_SUBJECT_TYPE_2", "INPUT_PREDICATE_2",
    "INPUT_JOIN_CONSTRAINT",
    "REQUIRED_SUBJECT_SOURCE", "REQUIRED_PREDICATE", "REQUIRED_TARGET_SOURCE",
}
CROSS_SUBJECT_DERIVE_RULE_FIELDS = {
    "RULE_ARITY", "RULE_PATTERN",
    "INPUT_SUBJECT_TYPE_1", "INPUT_PREDICATE_1",
    "INPUT_SUBJECT_TYPE_2", "INPUT_PREDICATE_2",
    "INPUT_JOIN_CONSTRAINT",
    "OUTPUT_SUBJECT_SOURCE", "OUTPUT_PREDICATE", "OUTPUT_TARGET_SOURCE",
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
    pattern = fields.get("RULE_PATTERN", {}).get("object")

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

    if arity == "2" and pattern == "CROSS_SUBJECT_DERIVE_SHARED_OBJECT":
        missing = sorted(CROSS_SUBJECT_DERIVE_RULE_FIELDS - fields.keys())
        if missing:
            return {"complete": False, "rule": rule_id, "arity": 2,
                    "pattern": pattern, "missing_fields": missing,
                    "rule_path": [r["id"] for r in parts]}
        ordered = [
            "RULE_ARITY", "RULE_PATTERN",
            "INPUT_SUBJECT_TYPE_1", "INPUT_PREDICATE_1",
            "INPUT_SUBJECT_TYPE_2", "INPUT_PREDICATE_2",
            "INPUT_JOIN_CONSTRAINT",
            "OUTPUT_SUBJECT_SOURCE", "OUTPUT_PREDICATE", "OUTPUT_TARGET_SOURCE",
        ]
        return {
            "complete": True, "rule": rule_id, "arity": 2,
            "pattern": pattern,
            "input_subject_type_1": fields["INPUT_SUBJECT_TYPE_1"]["object"],
            "input_predicate_1": fields["INPUT_PREDICATE_1"]["object"],
            "input_subject_type_2": fields["INPUT_SUBJECT_TYPE_2"]["object"],
            "input_predicate_2": fields["INPUT_PREDICATE_2"]["object"],
            "input_join_constraint": fields["INPUT_JOIN_CONSTRAINT"]["object"],
            "output_subject_source": fields["OUTPUT_SUBJECT_SOURCE"]["object"],
            "output_predicate": fields["OUTPUT_PREDICATE"]["object"],
            "output_target_source": fields["OUTPUT_TARGET_SOURCE"]["object"],
            "rule_path": [fields[name]["id"] for name in ordered],
        }

    if arity == "2" and pattern == "CROSS_SUBJECT_SHARED_OBJECT":
        missing = sorted(CROSS_SUBJECT_REQUIRED_RULE_FIELDS - fields.keys())
        if missing:
            return {"complete": False, "rule": rule_id, "arity": 2,
                    "pattern": pattern, "missing_fields": missing,
                    "rule_path": [r["id"] for r in parts]}
        ordered = [
            "RULE_ARITY", "RULE_PATTERN",
            "INPUT_SUBJECT_TYPE_1", "INPUT_PREDICATE_1",
            "INPUT_SUBJECT_TYPE_2", "INPUT_PREDICATE_2",
            "INPUT_JOIN_CONSTRAINT", "REQUIRED_SUBJECT_SOURCE",
            "REQUIRED_PREDICATE", "REQUIRED_TARGET_SOURCE",
        ]
        return {
            "complete": True, "rule": rule_id, "arity": 2,
            "pattern": pattern,
            "input_subject_type_1": fields["INPUT_SUBJECT_TYPE_1"]["object"],
            "input_predicate_1": fields["INPUT_PREDICATE_1"]["object"],
            "input_subject_type_2": fields["INPUT_SUBJECT_TYPE_2"]["object"],
            "input_predicate_2": fields["INPUT_PREDICATE_2"]["object"],
            "input_join_constraint": fields["INPUT_JOIN_CONSTRAINT"]["object"],
            "required_subject_source": fields["REQUIRED_SUBJECT_SOURCE"]["object"],
            "required_predicate": fields["REQUIRED_PREDICATE"]["object"],
            "required_target_source": fields["REQUIRED_TARGET_SOURCE"]["object"],
            "rule_path": [fields[name]["id"] for name in ordered],
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


def _evaluate_cross_subject(spec, objects, index):
    if spec["input_join_constraint"] != "SAME_OBJECT":
        return [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                 "missing_fields": ["SUPPORTED_INPUT_JOIN_CONSTRAINT"],
                 "observed_constraint": spec["input_join_constraint"],
                 "rule_path": spec["rule_path"]}]
    if spec["required_subject_source"] != "INPUT_1_SUBJECT":
        return [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                 "missing_fields": ["SUPPORTED_REQUIRED_SUBJECT_SOURCE"],
                 "observed_subject_source": spec["required_subject_source"],
                 "rule_path": spec["rule_path"]}]
    if spec["required_target_source"] != "INPUT_2_SUBJECT":
        return [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                 "missing_fields": ["SUPPORTED_REQUIRED_TARGET_SOURCE"],
                 "observed_target_source": spec["required_target_source"],
                 "rule_path": spec["rule_path"]}]

    left_subjects = [o["id"] for o in objects if o.get("type") == spec["input_subject_type_1"]]
    right_subjects = [o["id"] for o in objects if o.get("type") == spec["input_subject_type_2"]]
    events = []

    for left_subject in left_subjects:
        left_rels = index.get((left_subject, spec["input_predicate_1"]), [])
        matched = False

        for right_subject in right_subjects:
            right_rels = index.get((right_subject, spec["input_predicate_2"]), [])
            for a in left_rels:
                for b in right_rels:
                    if a["object"] != b["object"]:
                        continue
                    matched = True
                    events.extend(_compare_requirement(
                        spec["rule"], left_subject, [a["id"], b["id"]],
                        spec["required_predicate"], right_subject,
                        spec["input_join_constraint"], spec["rule_path"], index
                    ))

        if left_rels and not matched:
            events.append({
                "event": "ANTECEDENT_NOT_SATISFIED",
                "rule": spec["rule"],
                "subject": left_subject,
                "input_relations_1": [r["id"] for r in left_rels],
                "constraint": spec["input_join_constraint"],
                "rule_path": spec["rule_path"],
            })

    return events

def _derive_cross_subject(spec, objects, index, existing_triples):
    if spec["input_join_constraint"] != "SAME_OBJECT":
        return [], [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                     "missing_fields": ["SUPPORTED_INPUT_JOIN_CONSTRAINT"],
                     "observed_constraint": spec["input_join_constraint"],
                     "rule_path": spec["rule_path"]}]
    if spec["output_subject_source"] != "INPUT_1_SUBJECT":
        return [], [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                     "missing_fields": ["SUPPORTED_OUTPUT_SUBJECT_SOURCE"],
                     "observed_subject_source": spec["output_subject_source"],
                     "rule_path": spec["rule_path"]}]
    if spec["output_target_source"] != "INPUT_2_SUBJECT":
        return [], [{"event": "RULE_INCOMPLETE", "rule": spec["rule"],
                     "missing_fields": ["SUPPORTED_OUTPUT_TARGET_SOURCE"],
                     "observed_target_source": spec["output_target_source"],
                     "rule_path": spec["rule_path"]}]

    left_subjects = [o["id"] for o in objects if o.get("type") == spec["input_subject_type_1"]]
    right_subjects = [o["id"] for o in objects if o.get("type") == spec["input_subject_type_2"]]
    new_relations = []
    events = []

    for left_subject in left_subjects:
        left_rels = index.get((left_subject, spec["input_predicate_1"]), [])
        matched = False

        for right_subject in right_subjects:
            right_rels = index.get((right_subject, spec["input_predicate_2"]), [])
            for a in left_rels:
                for b in right_rels:
                    if a["object"] != b["object"]:
                        continue
                    matched = True
                    triple = (left_subject, spec["output_predicate"], right_subject)
                    if triple in existing_triples:
                        continue
                    relation_id = (
                        "DERIVED::" + spec["rule"] + "::" +
                        left_subject + "::" + spec["output_predicate"] + "::" + right_subject
                    )
                    rel = {
                        "id": relation_id,
                        "subject": left_subject,
                        "predicate": spec["output_predicate"],
                        "object": right_subject,
                        "network": "DERIVED",
                        "status": "derived",
                        "provenance": [],
                        "derived_from": [a["id"], b["id"]] + spec["rule_path"],
                    }
                    new_relations.append(rel)
                    existing_triples.add(triple)
                    events.append({
                        "event": "DERIVED_RELATION",
                        "rule": spec["rule"],
                        "subject": left_subject,
                        "input_relations": [a["id"], b["id"]],
                        "derived_relation": {
                            "id": relation_id,
                            "predicate": spec["output_predicate"],
                            "target": right_subject,
                        },
                        "rule_path": spec["rule_path"],
                    })

        if left_rels and not matched:
            events.append({
                "event": "ANTECEDENT_NOT_SATISFIED",
                "rule": spec["rule"],
                "subject": left_subject,
                "input_relations_1": [r["id"] for r in left_rels],
                "constraint": spec["input_join_constraint"],
                "rule_path": spec["rule_path"],
            })

    return new_relations, events


def evaluate(field: dict[str, Any]) -> dict[str, Any]:
    objects = field.get("objects", [])
    working_relations = list(field.get("relations", []))
    rules = field.get("rules", [])
    open_records = deepcopy(field.get("open", []))
    rule_objects = [o for o in objects if o.get("type") == "consistency_rule"]
    events = []

    specs = []
    for obj in rule_objects:
        spec = _rule_spec(obj["id"], rules)
        specs.append(spec)
        if not spec["complete"]:
            events.append({
                "event": "RULE_INCOMPLETE",
                "rule": obj["id"],
                "rule_arity": spec.get("arity"),
                "rule_pattern": spec.get("pattern"),
                "missing_fields": spec["missing_fields"],
                "rule_path": spec["rule_path"],
            })

    derive_specs = [
        s for s in specs
        if s.get("complete") and s.get("pattern") == "CROSS_SUBJECT_DERIVE_SHARED_OBJECT"
    ]

    existing_triples = {
        (r["subject"], r["predicate"], r["object"])
        for r in working_relations
    }

    # Derivation closure: derived relations live only in this working evaluation.
    while True:
        index = _index_relations(working_relations)
        round_new = []
        round_events = []

        for spec in derive_specs:
            new_relations, derivation_events = _derive_cross_subject(
                spec, objects, index, existing_triples
            )
            round_new.extend(new_relations)
            round_events.extend(derivation_events)

        # Keep DERIVED_RELATION events once. ANTECEDENT_NOT_SATISFIED is emitted
        # only on the final no-growth round below.
        events.extend(
            e for e in round_events
            if e["event"] == "DERIVED_RELATION"
        )

        if not round_new:
            events.extend(
                e for e in round_events
                if e["event"] != "DERIVED_RELATION"
            )
            break

        working_relations.extend(round_new)

    index = _index_relations(working_relations)

    for spec in specs:
        if not spec["complete"]:
            continue
        if spec.get("pattern") == "CROSS_SUBJECT_DERIVE_SHARED_OBJECT":
            continue

        if spec.get("pattern") == "CROSS_SUBJECT_SHARED_OBJECT":
            events.extend(_evaluate_cross_subject(spec, objects, index))
            continue

        subjects = [
            o["id"] for o in objects
            if o.get("type") == spec.get("scope_type")
        ]
        if not subjects:
            events.append({
                "event": "SCOPE_UNRESOLVED",
                "rule": spec["rule"],
                "scope_type": spec.get("scope_type"),
                "rule_path": spec["rule_path"],
            })
            continue

        if spec["arity"] == 1:
            events.extend(_evaluate_one_input(spec, subjects, index))
        elif spec["arity"] == 2:
            events.extend(_evaluate_two_input(spec, subjects, index))

    counts = {}
    for event in events:
        counts[event["event"]] = counts.get(event["event"], 0) + 1

    derived_relations = [
        r for r in working_relations if r.get("status") == "derived"
    ]
    summary = {
        "rule_count": len(rule_objects),
        "event_counts": counts,
    }
    if derived_relations:
        summary["derived_relation_count"] = len(derived_relations)

    result = {
        "experiment": field.get("experiment_id"),
        "events": events,
        "summary": summary,
        "open_preserved": [o["id"] for o in open_records],
        "open_records_unchanged": open_records == field.get("open", []),
    }
    if derived_relations:
        result["derived_relations"] = derived_relations
    return result

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
