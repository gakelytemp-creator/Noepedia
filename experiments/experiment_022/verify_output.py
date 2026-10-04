#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

N = 5000
HALF = 2500
MARGIN = 100
K_MIN = -100
K_MAX = 100

RULE_AB = "RULE022_AB_DIGITAL_CURRENT"
RULE_AC = "RULE022_AC_DIGITAL_PRESSURE"
RULE_BC = "RULE022_BC_CURRENT_PRESSURE"

EXPECTED_AB_MISMATCH = 1165
EXPECTED_SUPPORT_DIGITAL = 1163
EXPECTED_SUPPORT_CURRENT = 2

ALLOWED_EVENTS = {"CONSISTENT", "FORMAL_MISMATCH"}
FORBIDDEN_INPUT_TOKENS = (
    "MISMATCH","CONSISTENT","AGREEMENT","SUPPORT","ANOMALY",
    "FAULT","NORMAL","LAG","CAUSE","TRUTH"
)


def extract_state(relations, predicate):
    out = {}
    for r in relations:
        if r.get("predicate") == predicate and str(r.get("subject","")).startswith("ASSESSMENT_"):
            out[r["subject"]] = r["object"]
    return out


def anchors_for_half(start_index):
    # sequence indices are 1-based. Fixed 100-row margin on both edges.
    return range(start_index + MARGIN, start_index + HALF - MARGIN)


def score_curve(digital, current, pressure, anchor_indices):
    eligible = []
    for t in anchor_indices:
        sid = f"ASSESSMENT_{t:05d}"
        if digital[sid] == pressure[sid]:
            eligible.append(t)

    curve = {}
    for k in range(K_MIN, K_MAX + 1):
        mismatches = 0
        for t in eligible:
            ref = digital[f"ASSESSMENT_{t:05d}"]
            cur = current[f"ASSESSMENT_{t+k:05d}"]
            if cur != ref:
                mismatches += 1
        curve[k] = mismatches
    return eligible, curve


def choose_offset(curve):
    return min(curve, key=lambda k: (curve[k], abs(k), k))


def paired_effect(digital, current, pressure, anchor_indices, k):
    eligible = []
    baseline_mismatch = 0
    shifted_mismatch = 0
    corrected = 0
    introduced = 0

    for t in anchor_indices:
        sid = f"ASSESSMENT_{t:05d}"
        if digital[sid] != pressure[sid]:
            continue
        eligible.append(t)
        ref = digital[sid]
        b0 = current[sid] != ref
        bk = current[f"ASSESSMENT_{t+k:05d}"] != ref
        baseline_mismatch += int(b0)
        shifted_mismatch += int(bk)
        corrected += int(b0 and not bk)
        introduced += int((not b0) and bk)

    return {
        "eligible_anchors": len(eligible),
        "baseline_mismatches": baseline_mismatch,
        "selected_offset_mismatches": shifted_mismatch,
        "corrected_anchors": corrected,
        "introduced_anchors": introduced,
        "net_reduction": baseline_mismatch - shifted_mismatch,
        "relative_reduction": (
            (baseline_mismatch - shifted_mismatch) / baseline_mismatch
            if baseline_mismatch else 0.0
        )
    }


def main(argv):
    if len(argv) not in (3,4):
        print(f"Usage: {Path(argv[0]).name} FIELD_INPUT.json EVALUATOR_RESULT.json [OFFSET_RESULT.json]",
              file=sys.stderr)
        return 2

    field = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors = []

    if field["metadata"].get("evaluation_rows") != N:
        errors.append("evaluation row count changed")

    expected_states = {"STATE_LOADED","STATE_NOT_LOADED"}
    for key in ["digital_states_present","current_states_present","pressure_states_present"]:
        if set(field["metadata"].get(key,[])) != expected_states:
            errors.append(f"{key} does not contain both states")

    relations = field.get("relations", [])
    forbidden = []
    for r in relations:
        pred = str(r.get("predicate","")).upper()
        obj = str(r.get("object","")).upper()
        if any(tok in pred or tok in obj for tok in FORBIDDEN_INPUT_TOKENS):
            forbidden.append(r.get("id"))
    if forbidden:
        errors.append(f"input relations contain forbidden verdict tokens: {forbidden[:10]}")

    digital = extract_state(relations, "DIGITAL_CANDIDATE_STATE")
    current = extract_state(relations, "CURRENT_CANDIDATE_STATE")
    pressure = extract_state(relations, "PRESSURE_CANDIDATE_STATE")
    if not (len(digital) == len(current) == len(pressure) == N):
        errors.append("candidate-state cardinality failure")

    events = defaultdict(list)
    for e in result.get("events",[]):
        rule = e.get("rule")
        subject = e.get("subject")
        if rule in {RULE_AB,RULE_AC,RULE_BC} and subject:
            events[(rule,subject)].append(e.get("event"))
            if e.get("event") not in ALLOWED_EVENTS:
                errors.append(f"unexpected event {e.get('event')}")

    ab_mismatch = support_digital = support_current = 0
    for i in range(1,N+1):
        subject = f"ASSESSMENT_{i:05d}"
        vals = {}
        for rule in (RULE_AB,RULE_AC,RULE_BC):
            got = events.get((rule,subject),[])
            if len(got) != 1:
                errors.append(f"{subject}: event cardinality failure for {rule}: {got}")
                vals[rule] = None
            else:
                vals[rule] = got[0]

        if vals[RULE_AB] == "FORMAL_MISMATCH":
            ab_mismatch += 1
            pattern = (vals[RULE_AC], vals[RULE_BC])
            if pattern == ("CONSISTENT","FORMAL_MISMATCH"):
                support_digital += 1
            elif pattern == ("FORMAL_MISMATCH","CONSISTENT"):
                support_current += 1
            else:
                errors.append(f"{subject}: impossible binary third-path event pattern {pattern}")

    if ab_mismatch != EXPECTED_AB_MISMATCH:
        errors.append(f"020 continuity AB mismatch {ab_mismatch} != {EXPECTED_AB_MISMATCH}")
    if support_digital != EXPECTED_SUPPORT_DIGITAL:
        errors.append(f"020 continuity support-digital {support_digital} != {EXPECTED_SUPPORT_DIGITAL}")
    if support_current != EXPECTED_SUPPORT_CURRENT:
        errors.append(f"020 continuity support-current {support_current} != {EXPECTED_SUPPORT_CURRENT}")

    selection_anchors = list(anchors_for_half(1))
    confirmation_anchors = list(anchors_for_half(HALF+1))

    selection_eligible, selection_curve = score_curve(
        digital,current,pressure,selection_anchors
    )
    selected_k = choose_offset(selection_curve)

    confirmation_eligible, confirmation_curve = score_curve(
        digital,current,pressure,confirmation_anchors
    )
    effect = paired_effect(
        digital,current,pressure,confirmation_anchors,selected_k
    )

    if len(selection_curve) != 201 or len(confirmation_curve) != 201:
        errors.append("offset curve does not contain all 201 preregistered candidates")
    if len(selection_eligible) == 0 or len(confirmation_eligible) == 0:
        errors.append("no A=C eligible anchors in one half")

    scientific_result = (
        "CONFIRMED_OFFSET_EFFECT"
        if selected_k != 0 and effect["selected_offset_mismatches"] < effect["baseline_mismatches"]
        else "NO_CONFIRMED_OFFSET_EFFECT"
    )

    selection_top = sorted(
        [{"k":k,"mismatches":v} for k,v in selection_curve.items()],
        key=lambda x:(x["mismatches"],abs(x["k"]),x["k"])
    )[:10]

    confirmation_best_descriptive = min(
        confirmation_curve,
        key=lambda k:(confirmation_curve[k],abs(k),k)
    )

    if not result.get("open_records_unchanged",False):
        errors.append("OPEN records changed")

    output = {
        "experiment":"NOEPEDIA_EXP_022_SIGNED_TEMPORAL_OFFSET",
        "architectural_pass": not errors,
        "errors": errors,
        "continuity":{
            "ab_mismatch":ab_mismatch,
            "pressure_supports_digital":support_digital,
            "pressure_supports_current":support_current
        },
        "protocol":{
            "candidate_offsets":[K_MIN,K_MAX],
            "selection_half_rows":[1,HALF],
            "confirmation_half_rows":[HALF+1,N],
            "edge_margin":MARGIN,
            "positive_k_meaning":"later Motor_current state compared with current A=C reference"
        },
        "selection":{
            "fixed_anchor_count":len(selection_anchors),
            "eligible_a_equals_c":len(selection_eligible),
            "selected_k":selected_k,
            "baseline_mismatches":selection_curve[0],
            "selected_k_mismatches":selection_curve[selected_k],
            "top_10_offsets":selection_top
        },
        "confirmation":{
            **effect,
            "selected_k":selected_k,
            "scientific_result":scientific_result,
            "descriptive_only_best_k_on_confirmation":confirmation_best_descriptive,
            "descriptive_only_best_k_mismatches":confirmation_curve[confirmation_best_descriptive]
        },
        "claim_boundary":{
            "causality_established":False,
            "ground_truth_established":False,
            "fault_established":False,
            "anomaly_established":False,
            "universal_lag_established":False
        }
    }

    rendered = json.dumps(output,indent=2,ensure_ascii=False)+"\n"
    print(rendered,end="")
    if len(argv)==4:
        Path(argv[3]).write_text(rendered,encoding="utf-8")
    return 0 if not errors else 1


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
