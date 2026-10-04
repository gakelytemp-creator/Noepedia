#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

N=5000
RULE_AB="RULE020_AB_DIGITAL_CURRENT"
RULE_AC="RULE020_AC_DIGITAL_PRESSURE"
RULE_BC="RULE020_BC_CURRENT_PRESSURE"
ALLOWED_EVENTS={"CONSISTENT","FORMAL_MISMATCH"}
FORBIDDEN_INPUT_TOKENS=("MISMATCH","CONSISTENT","AGREEMENT","SUPPORT","ANOMALY","FAULT","NORMAL")


def main(argv):
    if len(argv)!=3:
        print(f"Usage: {Path(argv[0]).name} FIELD_INPUT.json EVALUATOR_RESULT.json",file=sys.stderr)
        return 2

    field=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors=[]

    expected_states={"STATE_LOADED","STATE_NOT_LOADED"}
    for key in ["digital_states_present","current_states_present","pressure_states_present"]:
        got=set(field["metadata"].get(key,[]))
        if got!=expected_states:
            errors.append(f"{key} not evaluable: {sorted(got)}")

    if abs(field["metadata"]["motor_current_high_centroid"]-field["metadata"]["motor_current_low_centroid"])<1e-12:
        errors.append("Motor_current centroids collapsed")
    if abs(field["metadata"]["tp2_high_centroid"]-field["metadata"]["tp2_low_centroid"])<1e-12:
        errors.append("TP2 centroids collapsed")

    for rel in field.get("relations",[]):
        hay=(str(rel.get("predicate",""))+" "+str(rel.get("object",""))).upper()
        if any(tok in hay for tok in FORBIDDEN_INPUT_TOKENS):
            errors.append(f"input relation asserts forbidden classification token: {rel['id']}")
            break

    per_subject=defaultdict(dict)
    for e in result.get("events",[]):
        if e.get("event") not in ALLOWED_EVENTS:
            errors.append(f"unexpected evaluator event {e.get('event')}")
            continue
        per_subject[e.get("subject")][e.get("rule")]=e.get("event")

    if len(per_subject)!=N:
        errors.append(f"event subjects {len(per_subject)} != {N}")

    support_digital=0
    support_current=0
    ab_mismatch=0

    for i in range(1,N+1):
        subject=f"ASSESSMENT_{i:05d}"
        events=per_subject.get(subject,{})
        if set(events)!= {RULE_AB,RULE_AC,RULE_BC}:
            errors.append(f"{subject} does not have exactly AB/AC/BC evaluator events")
            break

        ab=events[RULE_AB]
        ac=events[RULE_AC]
        bc=events[RULE_BC]

        if ab=="FORMAL_MISMATCH":
            ab_mismatch+=1
            if ac=="CONSISTENT" and bc=="FORMAL_MISMATCH":
                support_digital+=1
            elif ac=="FORMAL_MISMATCH" and bc=="CONSISTENT":
                support_current+=1
            else:
                errors.append(f"{subject} AB mismatch has impossible third-path event pattern: {ab}/{ac}/{bc}")
                break

    if ab_mismatch<=0:
        errors.append("Rule AB produced no mismatch")
    if support_digital<=0:
        errors.append("third path never supports digital side")
    if support_current<=0:
        errors.append("third path never supports current side")
    if support_digital+support_current!=ab_mismatch:
        errors.append("not every AB mismatch received exactly one third-path subclass")

    expected_open=sorted(o["id"] for o in field.get("open",[]))
    if sorted(result.get("open_preserved",[]))!=expected_open:
        errors.append("OPEN IDs not preserved")
    if result.get("open_records_unchanged") is not True:
        errors.append("OPEN records changed")

    if errors:
        print("Experiment 020 verification: FAIL")
        for e in errors:
            print("- "+e)
        return 1

    print("Experiment 020 verification: PASS")
    print(json.dumps({
        "AB_FORMAL_MISMATCH":ab_mismatch,
        "PRESSURE_SUPPORTS_DIGITAL_SIDE":support_digital,
        "PRESSURE_SUPPORTS_CURRENT_SIDE":support_current,
        "digital_support_fraction":support_digital/ab_mismatch,
        "current_support_fraction":support_current/ab_mismatch,
    },indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
