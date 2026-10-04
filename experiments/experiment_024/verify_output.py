#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter,defaultdict
from pathlib import Path

N=5000
DISTANCE_CAP=101
ALPHAS=["A20","A30","A40","A50","A60","A70","A80"]
RULE_AC="RULE024_AC_DIGITAL_PRESSURE"
ALLOWED_EVENTS={"CONSISTENT","FORMAL_MISMATCH"}
FORBIDDEN_INPUT_TOKENS=(
    "MISMATCH","CONSISTENT","AGREEMENT","SUPPORT","ANOMALY",
    "FAULT","NORMAL","LAG","CAUSE","TRUTH","ARTIFACT"
)


def rule_for(tag):
    return f"RULE024_AB_{tag}"


def pred_for(tag):
    return f"CURRENT_CANDIDATE_STATE_{tag}"


def distance_bin(d):
    if d==0:return "0"
    if d==1:return "1"
    if d<=5:return "2-5"
    if d<=10:return "6-10"
    if d<=25:return "11-25"
    if d<=50:return "26-50"
    if d<=100:return "51-100"
    return ">100"


def direction(p,n):
    if p==0:return "AT_TRANSITION"
    if p<n:return "AFTER_TRANSITION"
    if n<p:return "BEFORE_TRANSITION"
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
        print(f"Usage: {Path(argv[0]).name} FIELD_INPUT.json EVALUATOR_RESULT.json [THRESHOLD_RESULT.json]",
              file=sys.stderr)
        return 2

    field=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors=[]
    md=field["metadata"]

    if md.get("window_start")!=150001 or md.get("window_rows")!=N:
        errors.append("frozen threshold-test window changed")
    if abs(md.get("motor_current_midpoint",0)-2.1490460087555503)>1e-12:
        errors.append("Motor_current midpoint did not reproduce")
    if abs(md.get("tp2_threshold",0)-4.640123582876524)>1e-12:
        errors.append("TP2 threshold did not reproduce")
    if md.get("alphas")!=ALPHAS:
        errors.append("alpha family changed")

    expected_states={"STATE_LOADED","STATE_NOT_LOADED"}
    if set(md.get("digital_states_present",[]))!=expected_states:
        errors.append("digital states incomplete")
    if set(md.get("pressure_states_present",[]))!=expected_states:
        errors.append("pressure states incomplete")
    for tag in ALPHAS:
        if set(md.get("current_states_present",{}).get(tag,[]))!=expected_states:
            errors.append(f"{tag} current states incomplete")

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
    pressure=extract_state(relations,"PRESSURE_CANDIDATE_STATE")
    currents={tag:extract_state(relations,pred_for(tag)) for tag in ALPHAS}
    if len(digital)!=N or len(pressure)!=N or any(len(v)!=N for v in currents.values()):
        errors.append("candidate-state cardinality failure")

    temporal=defaultdict(lambda:{"p":[],"n":[]})
    for r in relations:
        s=str(r.get("subject",""))
        if not s.startswith("ASSESSMENT_"):continue
        if r.get("predicate")=="ROWS_SINCE_PREVIOUS_DIGITAL_TRANSITION":
            temporal[s]["p"].append(r["object"])
        elif r.get("predicate")=="ROWS_UNTIL_NEXT_DIGITAL_TRANSITION":
            temporal[s]["n"].append(r["object"])
    parsed={}
    for s,x in temporal.items():
        if len(x["p"])!=1 or len(x["n"])!=1:
            errors.append(f"{s}: temporal cardinality failure");continue
        p,n=int(x["p"][0]),int(x["n"][0])
        if not(0<=p<=DISTANCE_CAP and 0<=n<=DISTANCE_CAP):
            errors.append(f"{s}: temporal range failure");continue
        parsed[s]=(p,n)
    if len(parsed)!=N:
        errors.append("temporal coverage failure")

    events=defaultdict(list)
    valid_rules={RULE_AC,*[rule_for(t) for t in ALPHAS]}
    for e in result.get("events",[]):
        rule=e.get("rule");subject=e.get("subject")
        if rule in valid_rules and subject:
            events[(rule,subject)].append(e.get("event"))
            if e.get("event") not in ALLOWED_EVENTS:
                errors.append(f"unexpected event {e.get('event')}")

    eligible=[]
    for i in range(1,N+1):
        s=f"ASSESSMENT_{i:05d}"
        ac=events.get((RULE_AC,s),[])
        if len(ac)!=1:
            errors.append(f"{s}: AC event cardinality failure {ac}")
            continue
        if ac[0]=="CONSISTENT":
            eligible.append(s)

    per_alpha={}
    counts=[]
    for tag in ALPHAS:
        hist=Counter();dirs=Counter()
        near=intermediate=stable_far=0
        mismatches=[]
        rule=rule_for(tag)

        for i in range(1,N+1):
            s=f"ASSESSMENT_{i:05d}"
            ev=events.get((rule,s),[])
            if len(ev)!=1:
                errors.append(f"{s}: {tag} event cardinality failure {ev}")

        for s in eligible:
            ev=events[(rule,s)][0]
            if ev=="FORMAL_MISMATCH":
                mismatches.append(s)
                p,n=parsed[s]
                nearest=min(p,n)
                hist[distance_bin(nearest)]+=1
                dirs[direction(p,n)]+=1
                if nearest<=10:near+=1
                elif nearest<=100:intermediate+=1
                else:stable_far+=1

        c=len(mismatches)
        counts.append(c)
        per_alpha[tag]={
            "threshold":md["thresholds"][tag],
            "eligible_a_equals_c":len(eligible),
            "mismatch_count":c,
            "mismatch_fraction":c/len(eligible) if eligible else 0.0,
            "nearest_transition_histogram":{
                k:hist.get(k,0) for k in ["0","1","2-5","6-10","11-25","26-50","51-100",">100"]
            },
            "coarse_regions":{
                "NEAR":near,"INTERMEDIATE":intermediate,"STABLE_FAR":stable_far
            },
            "direction":{
                k:dirs.get(k,0) for k in ["AT_TRANSITION","AFTER_TRANSITION","BEFORE_TRANSITION","EQUIDISTANT"]
            }
        }

    nondec=all(a<=b for a,b in zip(counts,counts[1:]))
    noninc=all(a>=b for a,b in zip(counts,counts[1:]))
    all_equal=len(set(counts))==1

    if all_equal:
        klass="THRESHOLD_INVARIANT"
    elif nondec or noninc:
        klass="THRESHOLD_MONOTONIC"
    else:
        klass="THRESHOLD_NONMONOTONIC"

    if not result.get("open_records_unchanged",False):
        errors.append("OPEN records changed")

    output={
        "experiment":"NOEPEDIA_EXP_024_THRESHOLD_SENSITIVITY",
        "architectural_pass":not errors,
        "errors":errors,
        "window":{"start":150001,"count":5000},
        "a_equals_c_eligible":len(eligible),
        "threshold_sensitivity":{
            "classification":klass,
            "mismatch_counts":{tag:per_alpha[tag]["mismatch_count"] for tag in ALPHAS},
            "minimum":min(counts),
            "maximum":max(counts),
            "range":max(counts)-min(counts),
            "midpoint_A50":per_alpha["A50"]["mismatch_count"],
            "monotonic_nondecreasing":nondec,
            "monotonic_nonincreasing":noninc
        },
        "per_alpha":per_alpha,
        "claim_boundary":{
            "all_disagreement_explained_as_threshold_artifact":False,
            "ground_truth_established":False,
            "fault_established":False,
            "anomaly_established":False,
            "causality_established":False
        }
    }

    rendered=json.dumps(output,indent=2,ensure_ascii=False)+"\n"
    print(rendered,end="")
    if len(argv)==4:
        Path(argv[3]).write_text(rendered,encoding="utf-8")
    return 0 if not errors else 1


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
