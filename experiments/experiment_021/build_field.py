#!/usr/bin/env python3
from __future__ import annotations

import bisect
import csv
import json
import sys
from pathlib import Path

CALIBRATION_ROWS = 50_000
EVALUATION_ROWS = 5_000
FUTURE_CONTEXT_ROWS = 101
TOTAL_ROWS = CALIBRATION_ROWS + EVALUATION_ROWS + FUTURE_CONTEXT_ROWS
MAX_KMEANS_ITER = 100
DISTANCE_CAP = 101

STATE_LOADED = "STATE_LOADED"
STATE_NOT_LOADED = "STATE_NOT_LOADED"

RULE_AB = "RULE021_AB_DIGITAL_CURRENT"
RULE_AC = "RULE021_AC_DIGITAL_PRESSURE"
RULE_BC = "RULE021_BC_CURRENT_PRESSURE"

SRC_DV = "SOURCE_CHANNEL_DV_ELETRIC"
SRC_MC = "SOURCE_CHANNEL_MOTOR_CURRENT"
SRC_TP2 = "SOURCE_CHANNEL_TP2"
MODEL_MC = "MODEL_MOTOR_CURRENT_KMEANS"
MODEL_TP2 = "MODEL_TP2_KMEANS"

OPEN_ID = "OPEN_021_TEMPORAL_PHYSICAL_INTERPRETATION"
UNKNOWN = "UNKNOWN_PHYSICAL_INTERPRETATION"


def read_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"timestamp", "DV_eletric", "Motor_current", "TP2"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing required columns: {sorted(missing)}")
        for source_row, row in enumerate(reader, start=2):
            if len(rows) >= TOTAL_ROWS:
                break
            rows.append({
                "source_row": source_row,
                "timestamp": row["timestamp"],
                "dv_eletric": int(float(row["DV_eletric"])),
                "motor_current": float(row["Motor_current"]),
                "tp2": float(row["TP2"]),
            })
    if len(rows) < TOTAL_ROWS:
        raise RuntimeError("source does not contain frozen calibration + evaluation + future-context rows")
    return rows


def fit_1d_kmeans(values):
    c0 = min(values)
    c1 = max(values)
    if c0 == c1:
        raise RuntimeError("calibration range is zero")
    for _ in range(MAX_KMEANS_ITER):
        g0, g1 = [], []
        for x in values:
            if abs(x - c0) <= abs(x - c1):
                g0.append(x)
            else:
                g1.append(x)
        if not g0 or not g1:
            raise RuntimeError("empty calibration cluster")
        n0 = sum(g0) / len(g0)
        n1 = sum(g1) / len(g1)
        if abs(n0 - c0) < 1e-12 and abs(n1 - c1) < 1e-12:
            c0, c1 = n0, n1
            break
        c0, c1 = n0, n1
    low, high = min(c0, c1), max(c0, c1)
    if abs(high - low) < 1e-12:
        raise RuntimeError("calibration centroids collapsed")
    return low, high, (low + high) / 2.0


def relation(rid, subject, predicate, obj, network, provenance=None, status="settled"):
    return {
        "id": rid,
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "network": network,
        "status": status,
        "provenance": provenance or [],
    }


def add_rule(rules, prefix, rule_id, input_predicate, required_predicate):
    rules.extend([
        relation(prefix + "_01", rule_id, "RULE_SCOPE", "assessment", "NET_RULE"),
        relation(prefix + "_02", rule_id, "INPUT_PREDICATE", input_predicate, "NET_RULE"),
        relation(prefix + "_03", rule_id, "REQUIRED_PREDICATE", required_predicate, "NET_RULE"),
        relation(prefix + "_04", rule_id, "TARGET_CONSTRAINT", "SAME_NET", "NET_RULE"),
    ])


def capped_transition_distances(rows):
    transitions = [
        i for i in range(1, len(rows))
        if rows[i]["dv_eletric"] != rows[i - 1]["dv_eletric"]
    ]
    prev_dist = {}
    next_dist = {}

    start = CALIBRATION_ROWS
    stop = CALIBRATION_ROWS + EVALUATION_ROWS
    for i in range(start, stop):
        pos = bisect.bisect_right(transitions, i)

        if pos:
            d_prev = i - transitions[pos - 1]
        else:
            d_prev = DISTANCE_CAP

        if pos < len(transitions):
            d_next = transitions[pos] - i
        else:
            d_next = DISTANCE_CAP

        prev_dist[i] = min(d_prev, DISTANCE_CAP)
        next_dist[i] = min(d_next, DISTANCE_CAP)

    return transitions, prev_dist, next_dist


def main(argv):
    if len(argv) != 3:
        print(f"Usage: {Path(argv[0]).name} METROPT.csv FIELD_INPUT.json", file=sys.stderr)
        return 2

    rows = read_rows(Path(argv[1]))
    calibration = rows[:CALIBRATION_ROWS]
    evaluation = rows[CALIBRATION_ROWS:CALIBRATION_ROWS + EVALUATION_ROWS]

    mc_low, mc_high, mc_thr = fit_1d_kmeans([r["motor_current"] for r in calibration])
    tp_low, tp_high, tp_thr = fit_1d_kmeans([r["tp2"] for r in calibration])

    transitions, prev_dist, next_dist = capped_transition_distances(rows)

    objects = [
        {"id": STATE_LOADED, "type": "state"},
        {"id": STATE_NOT_LOADED, "type": "state"},
        {"id": RULE_AB, "type": "consistency_rule"},
        {"id": RULE_AC, "type": "consistency_rule"},
        {"id": RULE_BC, "type": "consistency_rule"},
        {"id": SRC_DV, "type": "source_channel"},
        {"id": SRC_MC, "type": "source_channel"},
        {"id": SRC_TP2, "type": "source_channel"},
        {"id": MODEL_MC, "type": "calibration_model"},
        {"id": MODEL_TP2, "type": "calibration_model"},
        {"id": UNKNOWN, "type": "unknown_interpretation"},
    ]

    relations = [
        relation("M021_MC_01", MODEL_MC, "CALIBRATION_CHANNEL", SRC_MC, "NET_MODEL"),
        relation("M021_MC_02", MODEL_MC, "LOW_CENTROID_LITERAL", repr(mc_low), "NET_MODEL"),
        relation("M021_MC_03", MODEL_MC, "HIGH_CENTROID_LITERAL", repr(mc_high), "NET_MODEL"),
        relation("M021_MC_04", MODEL_MC, "THRESHOLD_LITERAL", repr(mc_thr), "NET_MODEL"),
        relation("M021_TP2_01", MODEL_TP2, "CALIBRATION_CHANNEL", SRC_TP2, "NET_MODEL"),
        relation("M021_TP2_02", MODEL_TP2, "LOW_CENTROID_LITERAL", repr(tp_low), "NET_MODEL"),
        relation("M021_TP2_03", MODEL_TP2, "HIGH_CENTROID_LITERAL", repr(tp_high), "NET_MODEL"),
        relation("M021_TP2_04", MODEL_TP2, "THRESHOLD_LITERAL", repr(tp_thr), "NET_MODEL"),
    ]

    state_sets = {"digital": set(), "current": set(), "pressure": set()}

    for local_i, row in enumerate(evaluation, start=1):
        absolute_i = CALIBRATION_ROWS + local_i - 1
        sid = f"{local_i:05d}"
        assessment = f"ASSESSMENT_{sid}"
        source_row = f"SOURCE_ROW_{row['source_row']}"
        time_obj = f"TIME_{sid}"
        dv_obs = f"DV_OBS_{sid}"
        mc_obs = f"MC_OBS_{sid}"
        tp_obs = f"TP2_OBS_{sid}"

        digital = STATE_LOADED if row["dv_eletric"] == 1 else STATE_NOT_LOADED
        current = STATE_LOADED if row["motor_current"] > mc_thr else STATE_NOT_LOADED
        pressure = STATE_LOADED if row["tp2"] > tp_thr else STATE_NOT_LOADED

        state_sets["digital"].add(digital)
        state_sets["current"].add(current)
        state_sets["pressure"].add(pressure)

        objects.extend([
            {"id": assessment, "type": "assessment"},
            {"id": source_row, "type": "source_row"},
            {"id": time_obj, "type": "time"},
            {"id": dv_obs, "type": "digital_observation"},
            {"id": mc_obs, "type": "analog_observation"},
            {"id": tp_obs, "type": "analog_observation"},
        ])

        relations.extend([
            relation(f"R_{sid}_D", assessment, "DIGITAL_CANDIDATE_STATE", digital, "NET_STATE",
                     provenance=[SRC_DV, source_row, dv_obs]),
            relation(f"R_{sid}_C", assessment, "CURRENT_CANDIDATE_STATE", current, "NET_STATE",
                     provenance=[SRC_MC, source_row, mc_obs, MODEL_MC]),
            relation(f"R_{sid}_P", assessment, "PRESSURE_CANDIDATE_STATE", pressure, "NET_STATE",
                     provenance=[SRC_TP2, source_row, tp_obs, MODEL_TP2]),
            relation(f"R_{sid}_AT", assessment, "AT_TIME", time_obj, "NET_TIME", provenance=[source_row]),
            relation(f"R_{sid}_PREV", assessment, "ROWS_SINCE_PREVIOUS_DIGITAL_TRANSITION",
                     str(prev_dist[absolute_i]), "NET_TIME", provenance=[SRC_DV, source_row]),
            relation(f"R_{sid}_NEXT", assessment, "ROWS_UNTIL_NEXT_DIGITAL_TRANSITION",
                     str(next_dist[absolute_i]), "NET_TIME", provenance=[SRC_DV, source_row]),
            relation(f"R_{sid}_DVV", dv_obs, "OBSERVED_BINARY_LITERAL", str(row["dv_eletric"]),
                     "NET_OBSERVATION", provenance=[SRC_DV, source_row]),
            relation(f"R_{sid}_MCV", mc_obs, "OBSERVED_VALUE_LITERAL", repr(row["motor_current"]),
                     "NET_OBSERVATION", provenance=[SRC_MC, source_row]),
            relation(f"R_{sid}_TPV", tp_obs, "OBSERVED_VALUE_LITERAL", repr(row["tp2"]),
                     "NET_OBSERVATION", provenance=[SRC_TP2, source_row]),
        ])

    rules = []
    add_rule(rules, "RULE021AB", RULE_AB, "DIGITAL_CANDIDATE_STATE", "CURRENT_CANDIDATE_STATE")
    add_rule(rules, "RULE021AC", RULE_AC, "DIGITAL_CANDIDATE_STATE", "PRESSURE_CANDIDATE_STATE")
    add_rule(rules, "RULE021BC", RULE_BC, "CURRENT_CANDIDATE_STATE", "PRESSURE_CANDIDATE_STATE")

    open_records = [{
        "id": OPEN_ID,
        "subject": "TEMPORAL_DISAGREEMENT_GEOMETRY",
        "predicate": "PHYSICAL_INTERPRETATION",
        "object": UNKNOWN,
        "status": "open",
        "provenance": ["RULE021AB_01", "RULE021AC_01", "RULE021BC_01"],
    }]

    field = {
        "experiment_id": "NOEPEDIA_EXP_021_TEMPORAL_DISAGREEMENT_GEOMETRY",
        "metadata": {
            "calibration_rows": CALIBRATION_ROWS,
            "evaluation_rows": EVALUATION_ROWS,
            "future_context_rows": FUTURE_CONTEXT_ROWS,
            "distance_cap": DISTANCE_CAP,
            "motor_current_low_centroid": mc_low,
            "motor_current_high_centroid": mc_high,
            "motor_current_threshold": mc_thr,
            "tp2_low_centroid": tp_low,
            "tp2_high_centroid": tp_high,
            "tp2_threshold": tp_thr,
            "digital_states_present": sorted(state_sets["digital"]),
            "current_states_present": sorted(state_sets["current"]),
            "pressure_states_present": sorted(state_sets["pressure"]),
            "digital_transition_count_in_loaded_window": len(transitions),
            "input_paths_assert_verdicts": False,
        },
        "objects": objects,
        "networks": ["NET_STATE", "NET_TIME", "NET_OBSERVATION", "NET_MODEL", "NET_RULE"],
        "relations": relations,
        "rules": rules,
        "open": open_records,
    }

    Path(argv[2]).write_text(json.dumps(field, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "evaluation_assessments": EVALUATION_ROWS,
        "motor_current_threshold": mc_thr,
        "tp2_threshold": tp_thr,
        "digital_transition_count_in_loaded_window": len(transitions),
        "relations": len(relations),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
