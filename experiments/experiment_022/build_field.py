#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

CALIBRATION_ROWS = 50_000
EVALUATION_ROWS = 5_000
MAX_KMEANS_ITER = 100

STATE_LOADED = "STATE_LOADED"
STATE_NOT_LOADED = "STATE_NOT_LOADED"

RULE_AB = "RULE022_AB_DIGITAL_CURRENT"
RULE_AC = "RULE022_AC_DIGITAL_PRESSURE"
RULE_BC = "RULE022_BC_CURRENT_PRESSURE"

SRC_DV = "SOURCE_CHANNEL_DV_ELETRIC"
SRC_MC = "SOURCE_CHANNEL_MOTOR_CURRENT"
SRC_TP2 = "SOURCE_CHANNEL_TP2"
MODEL_MC = "MODEL_MOTOR_CURRENT_KMEANS"
MODEL_TP2 = "MODEL_TP2_KMEANS"

OPEN_ID = "OPEN_022_OFFSET_PHYSICAL_INTERPRETATION"
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
            if len(rows) >= CALIBRATION_ROWS + EVALUATION_ROWS:
                break
            rows.append({
                "source_row": source_row,
                "timestamp": row["timestamp"],
                "dv_eletric": int(float(row["DV_eletric"])),
                "motor_current": float(row["Motor_current"]),
                "tp2": float(row["TP2"]),
            })
    if len(rows) < CALIBRATION_ROWS + EVALUATION_ROWS:
        raise RuntimeError("source does not contain frozen calibration + evaluation rows")
    return rows


def fit_1d_kmeans(values):
    c0, c1 = min(values), max(values)
    if c0 == c1:
        raise RuntimeError("calibration range is zero")
    for _ in range(MAX_KMEANS_ITER):
        g0, g1 = [], []
        for x in values:
            (g0 if abs(x-c0) <= abs(x-c1) else g1).append(x)
        if not g0 or not g1:
            raise RuntimeError("empty calibration cluster")
        n0, n1 = sum(g0)/len(g0), sum(g1)/len(g1)
        if abs(n0-c0) < 1e-12 and abs(n1-c1) < 1e-12:
            c0, c1 = n0, n1
            break
        c0, c1 = n0, n1
    low, high = min(c0,c1), max(c0,c1)
    if abs(high-low) < 1e-12:
        raise RuntimeError("calibration centroids collapsed")
    return low, high, (low+high)/2.0


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
        relation(prefix+"_01", rule_id, "RULE_SCOPE", "assessment", "NET_RULE"),
        relation(prefix+"_02", rule_id, "INPUT_PREDICATE", input_predicate, "NET_RULE"),
        relation(prefix+"_03", rule_id, "REQUIRED_PREDICATE", required_predicate, "NET_RULE"),
        relation(prefix+"_04", rule_id, "TARGET_CONSTRAINT", "SAME_NET", "NET_RULE"),
    ])


def main(argv):
    if len(argv) != 3:
        print(f"Usage: {Path(argv[0]).name} METROPT.csv FIELD_INPUT.json", file=sys.stderr)
        return 2

    rows = read_rows(Path(argv[1]))
    calibration = rows[:CALIBRATION_ROWS]
    evaluation = rows[CALIBRATION_ROWS:CALIBRATION_ROWS+EVALUATION_ROWS]

    mc_low, mc_high, mc_thr = fit_1d_kmeans([r["motor_current"] for r in calibration])
    tp_low, tp_high, tp_thr = fit_1d_kmeans([r["tp2"] for r in calibration])

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
        relation("M022_MC_01", MODEL_MC, "CALIBRATION_CHANNEL", SRC_MC, "NET_MODEL"),
        relation("M022_MC_02", MODEL_MC, "LOW_CENTROID_LITERAL", repr(mc_low), "NET_MODEL"),
        relation("M022_MC_03", MODEL_MC, "HIGH_CENTROID_LITERAL", repr(mc_high), "NET_MODEL"),
        relation("M022_MC_04", MODEL_MC, "THRESHOLD_LITERAL", repr(mc_thr), "NET_MODEL"),
        relation("M022_TP2_01", MODEL_TP2, "CALIBRATION_CHANNEL", SRC_TP2, "NET_MODEL"),
        relation("M022_TP2_02", MODEL_TP2, "LOW_CENTROID_LITERAL", repr(tp_low), "NET_MODEL"),
        relation("M022_TP2_03", MODEL_TP2, "HIGH_CENTROID_LITERAL", repr(tp_high), "NET_MODEL"),
        relation("M022_TP2_04", MODEL_TP2, "THRESHOLD_LITERAL", repr(tp_thr), "NET_MODEL"),
    ]

    state_sets = {"digital": set(), "current": set(), "pressure": set()}

    for i, row in enumerate(evaluation, start=1):
        sid = f"{i:05d}"
        assessment = f"ASSESSMENT_{sid}"
        source_row = f"SOURCE_ROW_{row['source_row']}"

        digital = STATE_LOADED if row["dv_eletric"] == 1 else STATE_NOT_LOADED
        current = STATE_LOADED if row["motor_current"] > mc_thr else STATE_NOT_LOADED
        pressure = STATE_LOADED if row["tp2"] > tp_thr else STATE_NOT_LOADED

        state_sets["digital"].add(digital)
        state_sets["current"].add(current)
        state_sets["pressure"].add(pressure)

        objects.extend([
            {"id": assessment, "type": "assessment"},
            {"id": source_row, "type": "source_row"},
        ])

        relations.extend([
            relation(f"R_{sid}_D", assessment, "DIGITAL_CANDIDATE_STATE", digital, "NET_STATE",
                     provenance=[SRC_DV, source_row]),
            relation(f"R_{sid}_C", assessment, "CURRENT_CANDIDATE_STATE", current, "NET_STATE",
                     provenance=[SRC_MC, source_row, MODEL_MC]),
            relation(f"R_{sid}_P", assessment, "PRESSURE_CANDIDATE_STATE", pressure, "NET_STATE",
                     provenance=[SRC_TP2, source_row, MODEL_TP2]),
            relation(f"R_{sid}_SEQ", assessment, "EVALUATION_SEQUENCE_INDEX", str(i), "NET_SEQUENCE",
                     provenance=[source_row]),
        ])

    rules = []
    add_rule(rules, "RULE022AB", RULE_AB, "DIGITAL_CANDIDATE_STATE", "CURRENT_CANDIDATE_STATE")
    add_rule(rules, "RULE022AC", RULE_AC, "DIGITAL_CANDIDATE_STATE", "PRESSURE_CANDIDATE_STATE")
    add_rule(rules, "RULE022BC", RULE_BC, "CURRENT_CANDIDATE_STATE", "PRESSURE_CANDIDATE_STATE")

    field = {
        "experiment_id": "NOEPEDIA_EXP_022_SIGNED_TEMPORAL_OFFSET",
        "metadata": {
            "calibration_rows": CALIBRATION_ROWS,
            "evaluation_rows": EVALUATION_ROWS,
            "motor_current_low_centroid": mc_low,
            "motor_current_high_centroid": mc_high,
            "motor_current_threshold": mc_thr,
            "tp2_low_centroid": tp_low,
            "tp2_high_centroid": tp_high,
            "tp2_threshold": tp_thr,
            "digital_states_present": sorted(state_sets["digital"]),
            "current_states_present": sorted(state_sets["current"]),
            "pressure_states_present": sorted(state_sets["pressure"]),
            "input_paths_assert_verdicts": False,
        },
        "objects": objects,
        "networks": ["NET_STATE","NET_SEQUENCE","NET_MODEL","NET_RULE"],
        "relations": relations,
        "rules": rules,
        "open": [{
            "id": OPEN_ID,
            "subject": "SIGNED_TEMPORAL_OFFSET_EFFECT",
            "predicate": "PHYSICAL_INTERPRETATION",
            "object": UNKNOWN,
            "status": "open",
            "provenance": ["RULE022AB_01","RULE022AC_01","RULE022BC_01"]
        }]
    }

    Path(argv[2]).write_text(json.dumps(field, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({
        "evaluation_assessments": EVALUATION_ROWS,
        "motor_current_threshold": mc_thr,
        "tp2_threshold": tp_thr,
        "relations": len(relations)
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
