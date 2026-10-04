#!/usr/bin/env python3
from __future__ import annotations

import bisect
import csv
import json
import sys
from pathlib import Path

CALIBRATION_ROWS=50_000
WINDOW_START=150_001
WINDOW_ROWS=5_000
FUTURE_CONTEXT_ROWS=101
READ_THROUGH=WINDOW_START-1+WINDOW_ROWS+FUTURE_CONTEXT_ROWS
MAX_KMEANS_ITER=100
DISTANCE_CAP=101
ALPHAS=[0.2,0.3,0.4,0.5,0.6,0.7,0.8]

STATE_LOADED="STATE_LOADED"
STATE_NOT_LOADED="STATE_NOT_LOADED"
SRC_DV="SOURCE_CHANNEL_DV_ELETRIC"
SRC_MC="SOURCE_CHANNEL_MOTOR_CURRENT"
SRC_TP2="SOURCE_CHANNEL_TP2"
MODEL_MC="MODEL_MOTOR_CURRENT_KMEANS"
MODEL_TP2="MODEL_TP2_KMEANS"
RULE_AC="RULE024_AC_DIGITAL_PRESSURE"
OPEN_ID="OPEN_024_THRESHOLD_INTERPRETATION"
UNKNOWN="UNKNOWN_THRESHOLD_INTERPRETATION"


def alpha_tag(a):
    return f"A{int(round(a*100)):02d}"


def current_predicate(a):
    return f"CURRENT_CANDIDATE_STATE_{alpha_tag(a)}"


def current_rule(a):
    return f"RULE024_AB_{alpha_tag(a)}"


def read_rows(path:Path):
    rows=[]
    with path.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        required={"timestamp","DV_eletric","Motor_current","TP2"}
        missing=required-set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing required columns: {sorted(missing)}")
        for data_index,row in enumerate(reader,start=1):
            if data_index>READ_THROUGH:
                break
            rows.append({
                "data_index":data_index,
                "source_row":data_index+1,
                "timestamp":row["timestamp"],
                "dv_eletric":int(float(row["DV_eletric"])),
                "motor_current":float(row["Motor_current"]),
                "tp2":float(row["TP2"]),
            })
    if len(rows)<READ_THROUGH:
        raise RuntimeError(f"source has only {len(rows)} rows; need {READ_THROUGH}")
    return rows


def fit_1d_kmeans(values):
    c0,c1=min(values),max(values)
    if c0==c1:
        raise RuntimeError("calibration range is zero")
    for _ in range(MAX_KMEANS_ITER):
        g0,g1=[],[]
        for x in values:
            (g0 if abs(x-c0)<=abs(x-c1) else g1).append(x)
        if not g0 or not g1:
            raise RuntimeError("empty calibration cluster")
        n0,n1=sum(g0)/len(g0),sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1
    low,high=min(c0,c1),max(c0,c1)
    if abs(high-low)<1e-12:
        raise RuntimeError("collapsed centroids")
    return low,high,(low+high)/2.0


def relation(rid,subject,predicate,obj,network,provenance=None,status="settled"):
    return {
        "id":rid,"subject":subject,"predicate":predicate,"object":obj,
        "network":network,"status":status,"provenance":provenance or []
    }


def add_rule(rules,prefix,rule_id,input_predicate,required_predicate):
    rules.extend([
        relation(prefix+"_01",rule_id,"RULE_SCOPE","assessment","NET_RULE"),
        relation(prefix+"_02",rule_id,"INPUT_PREDICATE",input_predicate,"NET_RULE"),
        relation(prefix+"_03",rule_id,"REQUIRED_PREDICATE",required_predicate,"NET_RULE"),
        relation(prefix+"_04",rule_id,"TARGET_CONSTRAINT","SAME_NET","NET_RULE"),
    ])


def main(argv):
    if len(argv)!=3:
        print(f"Usage: {Path(argv[0]).name} METROPT.csv FIELD_INPUT.json",file=sys.stderr)
        return 2

    rows=read_rows(Path(argv[1]))
    calibration=rows[:CALIBRATION_ROWS]
    start0=WINDOW_START-1
    stop0=start0+WINDOW_ROWS
    window=rows[start0:stop0]
    context=rows[:stop0+FUTURE_CONTEXT_ROWS]

    mc_low,mc_high,mc_mid=fit_1d_kmeans([r["motor_current"] for r in calibration])
    tp_low,tp_high,tp_thr=fit_1d_kmeans([r["tp2"] for r in calibration])
    thresholds={alpha_tag(a):mc_low+a*(mc_high-mc_low) for a in ALPHAS}

    transitions=[
        i for i in range(1,len(context))
        if context[i]["dv_eletric"]!=context[i-1]["dv_eletric"]
    ]

    objects=[
        {"id":STATE_LOADED,"type":"state"},
        {"id":STATE_NOT_LOADED,"type":"state"},
        {"id":RULE_AC,"type":"consistency_rule"},
        {"id":SRC_DV,"type":"source_channel"},
        {"id":SRC_MC,"type":"source_channel"},
        {"id":SRC_TP2,"type":"source_channel"},
        {"id":MODEL_MC,"type":"calibration_model"},
        {"id":MODEL_TP2,"type":"calibration_model"},
        {"id":UNKNOWN,"type":"unknown_interpretation"},
    ]
    for a in ALPHAS:
        objects.append({"id":current_rule(a),"type":"consistency_rule"})

    relations=[
        relation("M024_MC_01",MODEL_MC,"CALIBRATION_CHANNEL",SRC_MC,"NET_MODEL"),
        relation("M024_MC_02",MODEL_MC,"LOW_CENTROID_LITERAL",repr(mc_low),"NET_MODEL"),
        relation("M024_MC_03",MODEL_MC,"HIGH_CENTROID_LITERAL",repr(mc_high),"NET_MODEL"),
        relation("M024_MC_04",MODEL_MC,"MIDPOINT_LITERAL",repr(mc_mid),"NET_MODEL"),
        relation("M024_TP2_01",MODEL_TP2,"CALIBRATION_CHANNEL",SRC_TP2,"NET_MODEL"),
        relation("M024_TP2_02",MODEL_TP2,"LOW_CENTROID_LITERAL",repr(tp_low),"NET_MODEL"),
        relation("M024_TP2_03",MODEL_TP2,"HIGH_CENTROID_LITERAL",repr(tp_high),"NET_MODEL"),
        relation("M024_TP2_04",MODEL_TP2,"THRESHOLD_LITERAL",repr(tp_thr),"NET_MODEL"),
    ]
    for a in ALPHAS:
        tag=alpha_tag(a)
        relations.append(
            relation(f"M024_MC_{tag}",MODEL_MC,f"THRESHOLD_{tag}_LITERAL",
                     repr(thresholds[tag]),"NET_MODEL")
        )

    state_sets={"digital":set(),"pressure":set(),**{alpha_tag(a):set() for a in ALPHAS}}

    for local_i,row in enumerate(window,start=1):
        absolute_i=start0+local_i-1
        pos=bisect.bisect_right(transitions,absolute_i)
        d_prev=absolute_i-transitions[pos-1] if pos else DISTANCE_CAP
        d_next=transitions[pos]-absolute_i if pos<len(transitions) else DISTANCE_CAP
        d_prev=min(d_prev,DISTANCE_CAP)
        d_next=min(d_next,DISTANCE_CAP)

        sid=f"{local_i:05d}"
        assessment=f"ASSESSMENT_{sid}"
        source_row=f"SOURCE_ROW_{row['source_row']}"

        digital=STATE_LOADED if row["dv_eletric"]==1 else STATE_NOT_LOADED
        pressure=STATE_LOADED if row["tp2"]>tp_thr else STATE_NOT_LOADED
        state_sets["digital"].add(digital)
        state_sets["pressure"].add(pressure)

        objects.extend([
            {"id":assessment,"type":"assessment"},
            {"id":source_row,"type":"source_row"},
        ])

        relations.extend([
            relation(f"R_{sid}_D",assessment,"DIGITAL_CANDIDATE_STATE",digital,"NET_STATE",
                     provenance=[SRC_DV,source_row]),
            relation(f"R_{sid}_P",assessment,"PRESSURE_CANDIDATE_STATE",pressure,"NET_STATE",
                     provenance=[SRC_TP2,source_row,MODEL_TP2]),
            relation(f"R_{sid}_PREV",assessment,"ROWS_SINCE_PREVIOUS_DIGITAL_TRANSITION",
                     str(d_prev),"NET_TIME",provenance=[SRC_DV,source_row]),
            relation(f"R_{sid}_NEXT",assessment,"ROWS_UNTIL_NEXT_DIGITAL_TRANSITION",
                     str(d_next),"NET_TIME",provenance=[SRC_DV,source_row]),
        ])

        for a in ALPHAS:
            tag=alpha_tag(a)
            current=STATE_LOADED if row["motor_current"]>thresholds[tag] else STATE_NOT_LOADED
            state_sets[tag].add(current)
            relations.append(
                relation(f"R_{sid}_{tag}",assessment,current_predicate(a),current,"NET_STATE",
                         provenance=[SRC_MC,source_row,MODEL_MC])
            )

    rules=[]
    add_rule(rules,"RULE024AC",RULE_AC,"DIGITAL_CANDIDATE_STATE","PRESSURE_CANDIDATE_STATE")
    for a in ALPHAS:
        tag=alpha_tag(a)
        add_rule(rules,f"RULE024{tag}",current_rule(a),
                 "DIGITAL_CANDIDATE_STATE",current_predicate(a))

    field={
        "experiment_id":"NOEPEDIA_EXP_024_THRESHOLD_SENSITIVITY",
        "metadata":{
            "calibration_rows":CALIBRATION_ROWS,
            "window_start":WINDOW_START,
            "window_rows":WINDOW_ROWS,
            "future_context_rows":FUTURE_CONTEXT_ROWS,
            "distance_cap":DISTANCE_CAP,
            "motor_current_low_centroid":mc_low,
            "motor_current_high_centroid":mc_high,
            "motor_current_midpoint":mc_mid,
            "tp2_threshold":tp_thr,
            "thresholds":thresholds,
            "alphas":[alpha_tag(a) for a in ALPHAS],
            "digital_states_present":sorted(state_sets["digital"]),
            "pressure_states_present":sorted(state_sets["pressure"]),
            "current_states_present":{k:sorted(v) for k,v in state_sets.items() if k.startswith("A")},
            "input_paths_assert_verdicts":False
        },
        "objects":objects,
        "networks":["NET_STATE","NET_TIME","NET_MODEL","NET_RULE"],
        "relations":relations,
        "rules":rules,
        "open":[{
            "id":OPEN_ID,
            "subject":"MOTOR_CURRENT_THRESHOLD_SENSITIVITY",
            "predicate":"PHYSICAL_INTERPRETATION",
            "object":UNKNOWN,
            "status":"open",
            "provenance":["RULE024AC_01"]
        }]
    }

    Path(argv[2]).write_text(json.dumps(field,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "window_start":WINDOW_START,
        "window_rows":WINDOW_ROWS,
        "motor_current_low_centroid":mc_low,
        "motor_current_high_centroid":mc_high,
        "motor_current_midpoint":mc_mid,
        "tp2_threshold":tp_thr,
        "thresholds":thresholds,
        "relations":len(relations)
    },indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
