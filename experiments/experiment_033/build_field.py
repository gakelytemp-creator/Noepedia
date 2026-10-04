#!/usr/bin/env python3
from __future__ import annotations
import csv, json, sys
from pathlib import Path

START=450_001
N=5_000
HISTORY=101
READ_START=START-HISTORY
READ_END=START+N-1
LOW=0.8821033735279131
HIGH=3.4159886439831877

S_HIGH="CURRENT_HIGH"
S_LOW="CURRENT_LOW"
S_MID="CURRENT_MID_UNRESOLVED"

RULE_OLD="RULE033_OLD_DIRECT_MAPPING"
RULE_NEW="RULE033_REVISED_LOAD_OFF_RUNON"
OPEN_ID="OPEN_033_REMAINING_DOMAIN_VALIDITY"

def relation(i,s,p,o,n,prov=None,status="settled"):
    return {"id":i,"subject":s,"predicate":p,"object":o,"network":n,"status":status,"provenance":prov or []}

def add_same_net_rule(rules,prefix,rule_id,input_pred,required_pred):
    rules.extend([
        relation(prefix+"_01",rule_id,"RULE_SCOPE","assessment","NET_RULE"),
        relation(prefix+"_02",rule_id,"INPUT_PREDICATE",input_pred,"NET_RULE"),
        relation(prefix+"_03",rule_id,"REQUIRED_PREDICATE",required_pred,"NET_RULE"),
        relation(prefix+"_04",rule_id,"TARGET_CONSTRAINT","SAME_NET","NET_RULE")
    ])

def current_state(x):
    if x<LOW:
        return S_LOW
    if x>HIGH:
        return S_HIGH
    return S_MID

def main(argv):
    if len(argv)!=3:
        print(f"Usage: {Path(argv[0]).name} METROPT.csv FIELD.json",file=sys.stderr)
        return 2

    src=Path(argv[1]); out=Path(argv[2])
    rows={}
    with src.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for i,row in enumerate(reader,start=1):
            if READ_START<=i<=READ_END:
                rows[i]={"dv":int(float(row["DV_eletric"])),"mc":float(row["Motor_current"])}
            if i>READ_END:
                break

    objects=[
        {"id":S_HIGH,"type":"current_state"},
        {"id":S_LOW,"type":"current_state"},
        {"id":S_MID,"type":"unresolved_current_state"},
        {"id":RULE_OLD,"type":"consistency_rule"},
        {"id":RULE_NEW,"type":"consistency_rule"},
        {"id":"EXP027","type":"evidence"},
        {"id":"EXP030","type":"evidence"},
        {"id":"EXP031","type":"evidence"},
        {"id":"EXP032","type":"evidence"}
    ]

    rels=[
        relation("P033_01",RULE_NEW,"SUPPORTED_BY","EXP027","NET_PROVENANCE"),
        relation("P033_02",RULE_NEW,"SUPPORTED_BY","EXP030","NET_PROVENANCE"),
        relation("P033_03",RULE_NEW,"SUPPORTED_BY","EXP031","NET_PROVENANCE"),
        relation("P033_04",RULE_NEW,"SUPPORTED_BY","EXP032","NET_PROVENANCE"),
        relation("P033_05",RULE_NEW,"EPISTEMIC_STATUS","EMPIRICALLY_SUPPORTED_RULE","NET_PROVENANCE")
    ]

    transition_open=[]
    mid_unresolved=[]
    last_load_off=None

    for i in range(READ_START+1,START):
        if rows[i-1]["dv"]==1 and rows[i]["dv"]==0:
            last_load_off=i

    for local,t in enumerate(range(START,START+N),start=1):
        if rows[t-1]["dv"]==1 and rows[t]["dv"]==0:
            last_load_off=t

        sid=f"ASSESSMENT_{local:05d}"
        objects.append({"id":sid,"type":"assessment"})
        cur=current_state(rows[t]["mc"])
        rels.append(relation(
            f"R{local:05d}_CUR",sid,"CURRENT_CANDIDATE_STATE",cur,"NET_STATE",
            prov=[f"SOURCE_ROW_{t+1}"]
        ))

        if cur==S_MID:
            mid_unresolved.append(sid)

        old=S_HIGH if rows[t]["dv"]==1 else S_LOW
        rels.append(relation(
            f"R{local:05d}_OLD",sid,"OLD_EXPECTED_CURRENT_STATE",old,"NET_STATE",
            prov=[RULE_OLD]
        ))

        new=None
        if rows[t]["dv"]==1:
            new=S_HIGH
        else:
            d=(t-last_load_off) if last_load_off is not None and last_load_off<=t else None
            if d is None:
                new=S_LOW
            elif d<=40:
                new=S_HIGH
            elif 41<=d<=52:
                transition_open.append(sid)
                rels.append(relation(
                    f"R{local:05d}_OPEN",sid,"TEMPORAL_RULE_STATUS","TRANSITION_OPEN","NET_TIME",
                    prov=[RULE_NEW,"EXP027","EXP030","EXP032"],status="open"
                ))
            else:
                new=S_LOW

        if new is not None:
            rels.append(relation(
                f"R{local:05d}_NEW",sid,"REVISED_EXPECTED_CURRENT_STATE",new,"NET_STATE",
                prov=[RULE_NEW,"EXP027","EXP030","EXP031","EXP032"]
            ))

    rules=[]
    add_same_net_rule(rules,"RULE033OLD",RULE_OLD,"OLD_EXPECTED_CURRENT_STATE","CURRENT_CANDIDATE_STATE")
    add_same_net_rule(rules,"RULE033NEW",RULE_NEW,"REVISED_EXPECTED_CURRENT_STATE","CURRENT_CANDIDATE_STATE")

    field={
        "experiment_id":"NOEPEDIA_EXP_033_RULE_REVISION_LOOP",
        "metadata":{
            "window_start":START,
            "window_rows":N,
            "current_band_low":LOW,
            "current_band_high":HIGH,
            "transition_open_start":41,
            "transition_open_end":52,
            "transition_open_count":len(transition_open),
            "mid_unresolved_count":len(mid_unresolved)
        },
        "objects":objects,
        "networks":["NET_STATE","NET_RULE","NET_TIME","NET_PROVENANCE"],
        "relations":rels,
        "rules":rules,
        "open":[{
            "id":OPEN_ID,
            "subject":"DOMAIN_VALIDITY_OF_CROSS_PATH_MAPPING",
            "predicate":"REMAINING_UNRESOLVED_COMPONENT",
            "object":"RESIDUAL_MISMATCH_OR_TRANSITION_INTERPRETATION",
            "status":"open",
            "provenance":[RULE_OLD,RULE_NEW,"EXP027","EXP030","EXP031","EXP032"]
        }]
    }

    out.write_text(json.dumps(field,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(field["metadata"],indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main(sys.argv))
