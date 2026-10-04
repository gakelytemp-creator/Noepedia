#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

CALIBRATION_ROWS = 50_000
EVALUATION_ROWS = 5_000
MAX_KMEANS_ITER = 100

STATE_LOADED = "STATE_LOADED"
STATE_NOT_LOADED = "STATE_NOT_LOADED"

RULE_ID = "RULE019_CROSS_PATH_STATE_CONSISTENCY"
OPEN_UNKNOWN = "UNKNOWN_VALIDITY"
OPEN_ID = "OPEN_RULE019_MAPPING_VALIDITY"

SRC_DV = "SOURCE_CHANNEL_DV_ELETRIC"
SRC_MC = "SOURCE_CHANNEL_MOTOR_CURRENT"
MODEL_ID = "MOTOR_CURRENT_CALIBRATION_MODEL"


def read_rows(path: Path):
    rows=[]
    with path.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for source_row,row in enumerate(reader,start=2):
            if len(rows) >= CALIBRATION_ROWS + EVALUATION_ROWS:
                break
            rows.append({
                "source_row":source_row,
                "timestamp":row["timestamp"],
                "motor_current":float(row["Motor_current"]),
                "dv_eletric":int(float(row["DV_eletric"])),
            })
    if len(rows) < CALIBRATION_ROWS + EVALUATION_ROWS:
        raise RuntimeError("source does not contain frozen calibration + evaluation rows")
    return rows


def fit_1d_kmeans(values):
    c0=min(values)
    c1=max(values)
    if c0 == c1:
        raise RuntimeError("Motor_current calibration range is zero")

    for _ in range(MAX_KMEANS_ITER):
        g0=[]
        g1=[]
        for x in values:
            d0=abs(x-c0)
            d1=abs(x-c1)
            if d0 <= d1:
                g0.append(x)
            else:
                g1.append(x)
        if not g0 or not g1:
            raise RuntimeError("empty Motor_current calibration cluster")
        n0=sum(g0)/len(g0)
        n1=sum(g1)/len(g1)
        if abs(n0-c0) < 1e-12 and abs(n1-c1) < 1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1

    low=min(c0,c1)
    high=max(c0,c1)
    if abs(high-low) < 1e-12:
        raise RuntimeError("Motor_current calibration centroids collapsed")
    return low,high,(low+high)/2.0


def relation(rid,subject,predicate,obj,network,provenance=None,status="settled"):
    return {
        "id":rid,
        "subject":subject,
        "predicate":predicate,
        "object":obj,
        "network":network,
        "status":status,
        "provenance":provenance or [],
    }


def main(argv):
    if len(argv)!=3:
        print(f"Usage: {Path(argv[0]).name} METROPT.csv FIELD_INPUT.json",file=sys.stderr)
        return 2

    rows=read_rows(Path(argv[1]))
    calibration=rows[:CALIBRATION_ROWS]
    evaluation=rows[CALIBRATION_ROWS:CALIBRATION_ROWS+EVALUATION_ROWS]

    low,high,threshold=fit_1d_kmeans([r["motor_current"] for r in calibration])

    objects=[
        {"id":STATE_LOADED,"type":"state"},
        {"id":STATE_NOT_LOADED,"type":"state"},
        {"id":RULE_ID,"type":"consistency_rule"},
        {"id":OPEN_UNKNOWN,"type":"unknown_validity"},
        {"id":SRC_DV,"type":"source_channel"},
        {"id":SRC_MC,"type":"source_channel"},
        {"id":MODEL_ID,"type":"calibration_model"},
    ]
    relations=[
        relation("MODEL019_01",MODEL_ID,"CALIBRATION_CHANNEL",SRC_MC,"NET_MODEL"),
        relation("MODEL019_02",MODEL_ID,"CALIBRATION_ROW_COUNT",str(CALIBRATION_ROWS),"NET_MODEL"),
        relation("MODEL019_03",MODEL_ID,"LOW_CENTROID_LITERAL",repr(low),"NET_MODEL"),
        relation("MODEL019_04",MODEL_ID,"HIGH_CENTROID_LITERAL",repr(high),"NET_MODEL"),
        relation("MODEL019_05",MODEL_ID,"THRESHOLD_LITERAL",repr(threshold),"NET_MODEL"),
    ]

    digital_states=set()
    analog_states=set()

    for i,row in enumerate(evaluation,start=1):
        sid=f"{i:05d}"
        assessment=f"ASSESSMENT_{sid}"
        time_obj=f"TIME_{sid}"
        source_row=f"SOURCE_ROW_{row['source_row']}"
        dv_obs=f"DV_OBSERVATION_{sid}"
        mc_obs=f"MOTOR_CURRENT_OBSERVATION_{sid}"

        digital_state=STATE_LOADED if row["dv_eletric"]==1 else STATE_NOT_LOADED
        analog_state=STATE_LOADED if row["motor_current"]>threshold else STATE_NOT_LOADED

        digital_states.add(digital_state)
        analog_states.add(analog_state)

        objects.extend([
            {"id":assessment,"type":"assessment"},
            {"id":time_obj,"type":"time"},
            {"id":source_row,"type":"source_row"},
            {"id":dv_obs,"type":"digital_observation"},
            {"id":mc_obs,"type":"analog_observation"},
        ])

        relations.extend([
            relation(f"R_{sid}_DS",assessment,"DIGITAL_CANDIDATE_STATE",digital_state,"NET_STATE",
                     provenance=[SRC_DV,source_row,dv_obs]),
            relation(f"R_{sid}_AS",assessment,"ANALOG_CANDIDATE_STATE",analog_state,"NET_STATE",
                     provenance=[SRC_MC,source_row,mc_obs,MODEL_ID]),
            relation(f"R_{sid}_AT",assessment,"AT_TIME",time_obj,"NET_TIME",
                     provenance=[source_row]),
            relation(f"R_{sid}_DVV",dv_obs,"OBSERVED_BINARY_LITERAL",str(row["dv_eletric"]),"NET_OBSERVATION",
                     provenance=[SRC_DV,source_row]),
            relation(f"R_{sid}_MCV",mc_obs,"OBSERVED_VALUE_LITERAL",repr(row["motor_current"]),"NET_OBSERVATION",
                     provenance=[SRC_MC,source_row]),
            relation(f"R_{sid}_DVC",dv_obs,"FROM_CHANNEL",SRC_DV,"NET_PROVENANCE",
                     provenance=[source_row]),
            relation(f"R_{sid}_MCC",mc_obs,"FROM_CHANNEL",SRC_MC,"NET_PROVENANCE",
                     provenance=[source_row]),
        ])

    rules=[
        relation("RULE019_01",RULE_ID,"RULE_SCOPE","assessment","NET_RULE"),
        relation("RULE019_02",RULE_ID,"INPUT_PREDICATE","DIGITAL_CANDIDATE_STATE","NET_RULE"),
        relation("RULE019_03",RULE_ID,"REQUIRED_PREDICATE","ANALOG_CANDIDATE_STATE","NET_RULE"),
        relation("RULE019_04",RULE_ID,"TARGET_CONSTRAINT","SAME_NET","NET_RULE"),
    ]

    open_records=[{
        "id":OPEN_ID,
        "subject":RULE_ID,
        "predicate":"DOMAIN_VALIDITY_OF_CROSS_PATH_MAPPING",
        "object":OPEN_UNKNOWN,
        "status":"open",
        "provenance":["RULE019_01","RULE019_02","RULE019_03","RULE019_04"],
    }]

    field={
        "experiment_id":"NOEPEDIA_EXP_019_REAL_CROSS_PATH_INFERENCE",
        "metadata":{
            "calibration_rows":CALIBRATION_ROWS,
            "evaluation_rows":EVALUATION_ROWS,
            "motor_current_low_centroid":low,
            "motor_current_high_centroid":high,
            "motor_current_threshold":threshold,
            "digital_states_present":sorted(digital_states),
            "analog_states_present":sorted(analog_states),
            "input_paths_assert_verdicts":False,
        },
        "objects":objects,
        "networks":["NET_STATE","NET_TIME","NET_OBSERVATION","NET_PROVENANCE","NET_MODEL","NET_RULE"],
        "relations":relations,
        "rules":rules,
        "open":open_records,
    }

    Path(argv[2]).write_text(json.dumps(field,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    print(json.dumps({
        "evaluation_assessments":EVALUATION_ROWS,
        "digital_states_present":sorted(digital_states),
        "analog_states_present":sorted(analog_states),
        "motor_current_threshold":threshold,
        "relations":len(relations),
        "open_records":len(open_records),
    },indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
