#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED={
    "CONSISTENT":20,
    "FORMAL_MISMATCH":20,
}


def main(argv):
    if len(argv)!=3:
        print(f"Usage: {Path(argv[0]).name} FIELD_INPUT.json EVALUATOR_RESULT.json",file=sys.stderr)
        return 2

    field=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors=[]

    counts=result.get("summary",{}).get("event_counts",{})
    for event,count in EXPECTED.items():
        if counts.get(event,0)!=count:
            errors.append(f"{event}: expected {count}, got {counts.get(event,0)}")

    unexpected={
        k:v for k,v in counts.items()
        if k not in EXPECTED and v
    }
    if unexpected:
        errors.append("unexpected evaluator events: "+json.dumps(unexpected,sort_keys=True))

    if len(field.get("open",[]))!=20:
        errors.append("field OPEN count is not 20")

    expected_open=sorted(o["id"] for o in field.get("open",[]))
    if sorted(result.get("open_preserved",[]))!=expected_open:
        errors.append("OPEN IDs were not preserved")

    if result.get("open_records_unchanged") is not True:
        errors.append("OPEN records changed")

    assessments=[o for o in field.get("objects",[]) if o.get("type")=="assessment"]
    if len(assessments)!=40:
        errors.append("assessment count is not 40")

    provenance_links=[
        r for r in field.get("relations",[])
        if r.get("predicate") in {"SUPPORTED_BY","FROM_SOURCE_ROW"}
    ]
    if len(provenance_links)<80:
        errors.append("required provenance links are missing")

    if result.get("experiment")!="NOEPEDIA_EXP_018_REAL_FIELD_INTEGRATION":
        errors.append("experiment id mismatch")

    if errors:
        print("Experiment 018 verification: FAIL")
        for e in errors:
            print("- "+e)
        return 1

    print("Experiment 018 verification: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
