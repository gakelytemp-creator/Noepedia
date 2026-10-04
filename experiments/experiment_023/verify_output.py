#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

N=5000
DISTANCE_CAP=101
HISTORICAL_K=35
OFFSET_MARGIN=100

RULE_AB="RULE023_AB_DIGITAL_CURRENT"
RULE_AC="RULE023_AC_DIGITAL_PRESSURE"
RULE_BC="RULE023_BC_CURRENT_PRESSURE"

ALLOWED_EVENTS={"CONSISTENT","FORMAL_MISMATCH"}
FORBIDDEN_INPUT_TOKENS=(
    "MISMATCH","CONSISTENT","AGREEMENT","SUPPORT","ANOMALY",
    "FAULT","NORMAL","LAG","CAUSE","TRUTH"
)


def distance_bin(d):
    if d==0: return "0"
    if d==1: return "1"
    if d<=5: return "2-5"
    if d<=10: return "6-10"
    if d<=25: return "11-25"
    if d<=50: return "26-50"
    if d<=100: return "51-100"
    return ">100"


def direction(prev_d,next_d):
    if prev_d==0: return "AT_TRANSITION"
    if prev_d<next_d: return "AFTER_TRANSITION"
    if next_d<prev_d: return "BEFORE_TRANSITION"
    return "EQUIDISTANT"


def extract_state(relations,predicate):
    out={}
    for r in relations:
        s=str(r.get("subject",""))
        if s.startswith("ASSESSMENT_") and r.get("predicate")==predicate:
            out[s]=r["object"]
    return out


def main(argv):
    if len(argv) not in (3,4):
        print(f"Usage: {Path(argv[0]).name} FIELD_INPUT.json EVALUATOR_RESULT.json [TRANSFER_RESULT.json]",
              file=sys.stderr)
        return 2

    field=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors=[]

    md=field["metadata"]
    if md.get("transfer_start")!=100001 or md.get("transfer_rows")!=N:
        errors.append("transfer window changed")
    if abs(md.get("motor_current_threshold",0)-2.1490460087555503)>1e-12:
        errors.append("Motor_current threshold did not reproduce")
    if abs(md.get("tp2_threshold",0)-4.640123582876524)>1e-12:
        errors.append("TP2 threshold did not reproduce")

    expected_states={"STATE_LOADED","STATE_NOT_LOADED"}
    for key in ["digital_states_present","current_states_present","pressure_states_present"]:
        if set(md.get(key,[]))!=expected_states:
            errors.append(f"{key} does not contain both states")

    relations=field.get("relations",[])
    forbidden=[]
    for r in relations:
        pred=str(r.get("predicate","")).upper()
        obj=str(r.get("object","")).upper()
        if any(tok in pred or tok in obj for tok in FORBIDDEN_INPUT_TOKENS):
            forbidden.append(r.get("id"))
    if forbidden:
        errors.append(f"input relations contain forbidden verdict tokens: {forbidden[:10]}")

    digital=extract_state(relations,"DIGITAL_CANDIDATE_STATE")
    current=extract_state(relations,"CURRENT_CANDIDATE_STATE")
    pressure=extract_state(relations,"PRESSURE_CANDIDATE_STATE")
    if not (len(digital)==len(current)==len(pressure)==N):
        errors.append("candidate-state cardinality failure")

    temporal=defaultdict(lambda:{"prev":[],"next":[]})
    for r in relations:
        s=str(r.get("subject",""))
        if not s.startswith("ASSESSMENT_"):
            continue
        if r.get("predicate")=="ROWS_SINCE_PREVIOUS_DIGITAL_TRANSITION":
            temporal[s]["prev"].append(r["object"])
        elif r.get("predicate")=="ROWS_UNTIL_NEXT_DIGITAL_TRANSITION":
            temporal[s]["next"].append(r["object"])

    parsed_temporal={}
    for s,item in temporal.items():
        if len(item["prev"])!=1 or len(item["next"])!=1:
            errors.append(f"{s}: temporal cardinality failure")
            continue
        try:
            p=int(item["prev"][0]); n=int(item["next"][0])
        except Exception:
            errors.append(f"{s}: non-integer temporal distance")
            continue
        if not (0<=p<=DISTANCE_CAP and 0<=n<=DISTANCE_CAP):
            errors.append(f"{s}: temporal distance outside range")
            continue
        parsed_temporal[s]=(p,n)
    if len(parsed_temporal)!=N:
        errors.append(f"parsed temporal relations {len(parsed_temporal)} != {N}")

    events=defaultdict(list)
    for e in result.get("events",[]):
        rule=e.get("rule"); subject=e.get("subject")
        if rule in {RULE_AB,RULE_AC,RULE_BC} and subject:
            events[(rule,subject)].append(e.get("event"))
            if e.get("event") not in ALLOWED_EVENTS:
                errors.append(f"unexpected event {e.get('event')}")

    ab_mismatch=[]
    support_digital=[]
    support_current=[]

    for i in range(1,N+1):
        s=f"ASSESSMENT_{i:05d}"
        ev={}
        for rule in (RULE_AB,RULE_AC,RULE_BC):
            got=events.get((rule,s),[])
            if len(got)!=1:
                errors.append(f"{s}: event cardinality failure for {rule}: {got}")
                ev[rule]=None
            else:
                ev[rule]=got[0]
        if ev[RULE_AB]=="FORMAL_MISMATCH":
            ab_mismatch.append(s)
            pattern=(ev[RULE_AC],ev[RULE_BC])
            if pattern==("CONSISTENT","FORMAL_MISMATCH"):
                support_digital.append(s)
            elif pattern==("FORMAL_MISMATCH","CONSISTENT"):
                support_current.append(s)
            else:
                errors.append(f"{s}: impossible binary third-path pattern {pattern}")

    hist=Counter()
    dirs=Counter()
    near=intermediate=stable_far=0
    for s in support_digital:
        p,n=parsed_temporal[s]
        nearest=min(p,n)
        hist[distance_bin(nearest)]+=1
        dirs[direction(p,n)]+=1
        if nearest<=10:
            near+=1
        elif nearest<=100:
            intermediate+=1
        else:
            stable_far+=1

    anchors=range(1+OFFSET_MARGIN, N-OFFSET_MARGIN+1)
    eligible=[]
    baseline=shifted=corrected=introduced=0
    for t in anchors:
        s=f"ASSESSMENT_{t:05d}"
        if digital[s]!=pressure[s]:
            continue
        eligible.append(t)
        ref=digital[s]
        b0=current[s]!=ref
        bk=current[f"ASSESSMENT_{t+HISTORICAL_K:05d}"]!=ref
        baseline+=int(b0)
        shifted+=int(bk)
        corrected+=int(b0 and not bk)
        introduced+=int((not b0) and bk)

    transfer_offset={
        "historical_k":HISTORICAL_K,
        "eligible_anchors":len(eligible),
        "baseline_mismatches":baseline,
        "historical_k_mismatches":shifted,
        "corrected_anchors":corrected,
        "introduced_anchors":introduced,
        "net_reduction":baseline-shifted,
        "relative_reduction":((baseline-shifted)/baseline if baseline else 0.0)
    }

    if not result.get("open_records_unchanged",False):
        errors.append("OPEN records changed")

    output={
        "experiment":"NOEPEDIA_EXP_023_LOCKED_TRANSFER_REPLICATION",
        "architectural_pass":not errors,
        "errors":errors,
        "transfer_window":{"start":100001,"count":5000},
        "thresholds":{
            "motor_current":md["motor_current_threshold"],
            "tp2":md["tp2_threshold"]
        },
        "metrics":{
            "ab_mismatch":len(ab_mismatch),
            "ab_mismatch_fraction":len(ab_mismatch)/N,
            "pressure_supports_digital":len(support_digital),
            "pressure_supports_current":len(support_current),
            "support_digital_fraction_of_ab_mismatch":(
                len(support_digital)/len(ab_mismatch) if ab_mismatch else 0.0
            )
        },
        "dominant_subclass_temporal_geometry":{
            "n":len(support_digital),
            "nearest_transition_histogram":{
                k:hist.get(k,0)
                for k in ["0","1","2-5","6-10","11-25","26-50","51-100",">100"]
            },
            "coarse_regions":{
                "NEAR":near,
                "INTERMEDIATE":intermediate,
                "STABLE_FAR":stable_far
            },
            "direction_to_nearest_transition":{
                k:dirs.get(k,0)
                for k in ["AT_TRANSITION","AFTER_TRANSITION","BEFORE_TRANSITION","EQUIDISTANT"]
            }
        },
        "historical_fixed_offset_transfer":transfer_offset,
        "discovery_reference":{
            "ab_mismatch":1165,
            "pressure_supports_digital":1163,
            "pressure_supports_current":2,
            "temporal_after":1126,
            "temporal_before":10,
            "temporal_at":26,
            "temporal_equidistant":1,
            "stable_far":0,
            "experiment_022_historical_k":35,
            "experiment_022_confirmation_net_reduction":-11
        },
        "claim_boundary":{
            "ground_truth_established":False,
            "fault_established":False,
            "anomaly_established":False,
            "causality_established":False,
            "universal_lag_established":False
        }
    }

    rendered=json.dumps(output,indent=2,ensure_ascii=False)+"\n"
    print(rendered,end="")
    if len(argv)==4:
        Path(argv[3]).write_text(rendered,encoding="utf-8")

    return 0 if not errors else 1


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
