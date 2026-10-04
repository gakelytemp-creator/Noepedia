#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

N = 5000
DISTANCE_CAP = 101
RULE_AB = "RULE021_AB_DIGITAL_CURRENT"
RULE_AC = "RULE021_AC_DIGITAL_PRESSURE"
RULE_BC = "RULE021_BC_CURRENT_PRESSURE"

EXPECTED_AB_MISMATCH = 1165
EXPECTED_SUPPORT_DIGITAL = 1163
EXPECTED_SUPPORT_CURRENT = 2

ALLOWED_EVENTS = {"CONSISTENT", "FORMAL_MISMATCH"}
FORBIDDEN_INPUT_TOKENS = (
    "MISMATCH", "CONSISTENT", "AGREEMENT", "SUPPORT",
    "ANOMALY", "FAULT", "NORMAL", "LAG", "CAUSE"
)


def distance_bin(d):
    if d == 0:
        return "0"
    if d == 1:
        return "1"
    if d <= 5:
        return "2-5"
    if d <= 10:
        return "6-10"
    if d <= 25:
        return "11-25"
    if d <= 50:
        return "26-50"
    if d <= 100:
        return "51-100"
    return ">100"


def coarse_region(prev_d, next_d):
    nearest = min(prev_d, next_d)
    if nearest <= 10:
        return "NEAR"
    if nearest <= 100:
        return "INTERMEDIATE"
    return "STABLE_FAR"


def direction(prev_d, next_d):
    if prev_d == 0:
        return "AT_TRANSITION"
    if prev_d < next_d:
        return "AFTER_TRANSITION"
    if next_d < prev_d:
        return "BEFORE_TRANSITION"
    return "EQUIDISTANT"


def main(argv):
    if len(argv) not in (3, 4):
        print(f"Usage: {Path(argv[0]).name} FIELD_INPUT.json EVALUATOR_RESULT.json [TEMPORAL_RESULT.json]",
              file=sys.stderr)
        return 2

    field = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors = []

    expected_states = {"STATE_LOADED", "STATE_NOT_LOADED"}
    for key in ["digital_states_present", "current_states_present", "pressure_states_present"]:
        if set(field["metadata"].get(key, [])) != expected_states:
            errors.append(f"{key} does not contain both frozen states")

    if field["metadata"].get("evaluation_rows") != N:
        errors.append("evaluation row count changed")
    if field["metadata"].get("distance_cap") != DISTANCE_CAP:
        errors.append("distance cap changed")

    relations = field.get("relations", [])
    forbidden_hits = []
    for rel in relations:
        pred = str(rel.get("predicate", "")).upper()
        obj = str(rel.get("object", "")).upper()
        if any(tok in pred or tok in obj for tok in FORBIDDEN_INPUT_TOKENS):
            forbidden_hits.append(rel.get("id"))
    if forbidden_hits:
        errors.append(f"input relations contain forbidden verdict tokens: {forbidden_hits[:10]}")

    temporal = defaultdict(lambda: {"prev": [], "next": []})
    for rel in relations:
        subject = rel.get("subject", "")
        if not subject.startswith("ASSESSMENT_"):
            continue
        if rel.get("predicate") == "ROWS_SINCE_PREVIOUS_DIGITAL_TRANSITION":
            temporal[subject]["prev"].append(rel.get("object"))
        elif rel.get("predicate") == "ROWS_UNTIL_NEXT_DIGITAL_TRANSITION":
            temporal[subject]["next"].append(rel.get("object"))

    if len(temporal) != N:
        errors.append(f"expected temporal relations for {N} assessments, got {len(temporal)}")

    parsed_temporal = {}
    for subject, item in temporal.items():
        if len(item["prev"]) != 1 or len(item["next"]) != 1:
            errors.append(f"{subject}: temporal relation cardinality failure")
            continue
        try:
            prev_d = int(item["prev"][0])
            next_d = int(item["next"][0])
        except Exception:
            errors.append(f"{subject}: temporal distance is not integer")
            continue
        if not (0 <= prev_d <= DISTANCE_CAP and 0 <= next_d <= DISTANCE_CAP):
            errors.append(f"{subject}: temporal distance outside 0..{DISTANCE_CAP}")
            continue
        parsed_temporal[subject] = (prev_d, next_d)

    events_by_rule_subject = defaultdict(list)
    for event in result.get("events", []):
        rule = event.get("rule")
        subject = event.get("subject")
        if rule in {RULE_AB, RULE_AC, RULE_BC} and subject:
            events_by_rule_subject[(rule, subject)].append(event.get("event"))
            if event.get("event") not in ALLOWED_EVENTS:
                errors.append(f"unexpected event {event.get('event')} for {rule} {subject}")

    assessments = [f"ASSESSMENT_{i:05d}" for i in range(1, N + 1)]
    support_digital = []
    support_current = []
    ab_mismatch_subjects = []

    for subject in assessments:
        ev = {}
        for rule in (RULE_AB, RULE_AC, RULE_BC):
            vals = events_by_rule_subject.get((rule, subject), [])
            if len(vals) != 1:
                errors.append(f"{subject}: expected exactly one event for {rule}, got {vals}")
                ev[rule] = None
            else:
                ev[rule] = vals[0]

        if ev[RULE_AB] == "FORMAL_MISMATCH":
            ab_mismatch_subjects.append(subject)
            pattern = (ev[RULE_AC], ev[RULE_BC])
            if pattern == ("CONSISTENT", "FORMAL_MISMATCH"):
                support_digital.append(subject)
            elif pattern == ("FORMAL_MISMATCH", "CONSISTENT"):
                support_current.append(subject)
            else:
                errors.append(f"{subject}: impossible binary third-path pattern {pattern}")

    if len(ab_mismatch_subjects) != EXPECTED_AB_MISMATCH:
        errors.append(
            f"020 continuity failed: AB mismatch {len(ab_mismatch_subjects)} != {EXPECTED_AB_MISMATCH}"
        )
    if len(support_digital) != EXPECTED_SUPPORT_DIGITAL:
        errors.append(
            f"020 continuity failed: support-digital {len(support_digital)} != {EXPECTED_SUPPORT_DIGITAL}"
        )
    if len(support_current) != EXPECTED_SUPPORT_CURRENT:
        errors.append(
            f"020 continuity failed: support-current {len(support_current)} != {EXPECTED_SUPPORT_CURRENT}"
        )

    hist = Counter()
    coarse = Counter()
    directions = Counter()
    prev_hist = Counter()
    next_hist = Counter()

    for subject in support_digital:
        if subject not in parsed_temporal:
            errors.append(f"{subject}: missing parsed temporal geometry")
            continue
        prev_d, next_d = parsed_temporal[subject]
        nearest = min(prev_d, next_d)
        hist[distance_bin(nearest)] += 1
        prev_hist[distance_bin(prev_d)] += 1
        next_hist[distance_bin(next_d)] += 1
        coarse[coarse_region(prev_d, next_d)] += 1
        directions[direction(prev_d, next_d)] += 1

    if sum(hist.values()) != EXPECTED_SUPPORT_DIGITAL:
        errors.append("temporal histogram does not cover all dominant-subclass assessments")

    if not result.get("open_records_unchanged", False):
        errors.append("OPEN records changed during evaluation")

    output = {
        "experiment": "NOEPEDIA_EXP_021_TEMPORAL_DISAGREEMENT_GEOMETRY",
        "architectural_pass": not errors,
        "errors": errors,
        "continuity": {
            "ab_mismatch": len(ab_mismatch_subjects),
            "pressure_supports_digital": len(support_digital),
            "pressure_supports_current": len(support_current),
        },
        "dominant_subclass_temporal_geometry": {
            "n": len(support_digital),
            "nearest_transition_histogram": {
                k: hist.get(k, 0)
                for k in ["0", "1", "2-5", "6-10", "11-25", "26-50", "51-100", ">100"]
            },
            "coarse_regions": {
                k: coarse.get(k, 0)
                for k in ["NEAR", "INTERMEDIATE", "STABLE_FAR"]
            },
            "direction_to_nearest_transition": {
                k: directions.get(k, 0)
                for k in ["AT_TRANSITION", "AFTER_TRANSITION", "BEFORE_TRANSITION", "EQUIDISTANT"]
            },
            "rows_since_previous_transition_histogram": {
                k: prev_hist.get(k, 0)
                for k in ["0", "1", "2-5", "6-10", "11-25", "26-50", "51-100", ">100"]
            },
            "rows_until_next_transition_histogram": {
                k: next_hist.get(k, 0)
                for k in ["0", "1", "2-5", "6-10", "11-25", "26-50", "51-100", ">100"]
            }
        },
        "claim_boundary": {
            "lag_established": False,
            "causality_established": False,
            "fault_established": False,
            "anomaly_established": False,
            "truth_side_established": False
        }
    }

    rendered = json.dumps(output, indent=2, ensure_ascii=False) + "\n"
    print(rendered, end="")
    if len(argv) == 4:
        Path(argv[3]).write_text(rendered, encoding="utf-8")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
