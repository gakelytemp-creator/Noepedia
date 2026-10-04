#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED_ASSESSMENTS=5000
FORBIDDEN_INPUT_TOKENS=("MISMATCH","CONSISTENT","AGREEMENT")


def main(argv):
    if len(argv)!=3:
        print(f"Usage: {Path(argv[0]).name} FIELD_INPUT.json EVALUATOR_RESULT.json",file=sys.stderr)
        return 2

    field=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors=[]

    assessments=[o for o in field["objects"] if o.get("type")=="assessment"]
    if len(assessments)!=EXPECTED_ASSESSMENTS:
        errors.append(f"expected {EXPECTED_ASSESSMENTS} assessments, got {len(assessments)}")

    ds=set(field["metadata"].get("digital_states_present",[]))
    ans=set(field["metadata"].get("analog_states_present",[]))
    expected_states={"STATE_LOADED","STATE_NOT_LOADED"}
    if ds!=expected_states:
        errors.append(f"Path A not evaluable; digital states present={sorted(ds)}")
    if ans!=expected_states:
        errors.append(f"Path B not evaluable; analog states present={sorted(ans)}")

    if abs(field["metadata"]["motor_current_high_centroid"]-field["metadata"]["motor_current_low_centroid"])<1e-12:
        errors.append("calibration centroids are not distinct")

    for rel in field.get("relations",[]):
        hay=(str(rel.get("predicate",""))+" "+str(rel.get("object",""))).upper()
        if any(tok in hay for tok in FORBIDDEN_INPUT_TOKENS):
            errors.append(f"input relation asserts forbidden verdict token: {rel['id']}")
            break

    counts=result.get("summary",{}).get("event_counts",{})
    consistent=counts.get("CONSISTENT",0)
    mismatch=counts.get("FORMAL_MISMATCH",0)

    if consistent+mismatch!=EXPECTED_ASSESSMENTS:
        errors.append(f"evaluator classified {consistent+mismatch} of {EXPECTED_ASSESSMENTS} assessments")
    if consistent<=0:
        errors.append("no CONSISTENT events produced")
    if mismatch<=0:
        errors.append("no FORMAL_MISMATCH events produced")

    unexpected={k:v for k,v in counts.items() if k not in {"CONSISTENT","FORMAL_MISMATCH"} and v}
    if unexpected:
        errors.append("unexpected evaluator events: "+json.dumps(unexpected,sort_keys=True))

    rel_by_id={r["id"]:r for r in field["relations"]}
    for event in result.get("events",[]):
        if event.get("event")!="FORMAL_MISMATCH":
            continue
        inp=rel_by_id.get(event.get("input_relation"))
        conflict=rel_by_id.get(event.get("conflicting_relation"))
        if not inp or inp.get("predicate")!="DIGITAL_CANDIDATE_STATE":
            errors.append("mismatch missing digital-path input relation")
            break
        if not conflict or conflict.get("predicate")!="ANALOG_CANDIDATE_STATE":
            errors.append("mismatch missing analog-path conflicting relation")
            break
        if "SOURCE_CHANNEL_DV_ELETRIC" not in inp.get("provenance",[]):
            errors.append("digital mismatch relation lacks digital-channel provenance")
            break
        if "SOURCE_CHANNEL_MOTOR_CURRENT" not in conflict.get("provenance",[]):
            errors.append("analog mismatch relation lacks motor-current provenance")
            break

    expected_open=sorted(o["id"] for o in field.get("open",[]))
    if sorted(result.get("open_preserved",[]))!=expected_open:
        errors.append("OPEN IDs not preserved")
    if result.get("open_records_unchanged") is not True:
        errors.append("OPEN records changed")

    if errors:
        print("Experiment 019 verification: FAIL")
        for e in errors:
            print("- "+e)
        return 1

    print("Experiment 019 verification: PASS")
    print(json.dumps({
        "CONSISTENT":consistent,
        "FORMAL_MISMATCH":mismatch,
        "mismatch_fraction":mismatch/EXPECTED_ASSESSMENTS,
    },indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
