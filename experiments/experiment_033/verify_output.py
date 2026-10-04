#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from collections import defaultdict
from pathlib import Path

N=5000
RULE_OLD="RULE033_OLD_DIRECT_MAPPING"
RULE_NEW="RULE033_REVISED_LOAD_OFF_RUNON"
MID="CURRENT_MID_UNRESOLVED"

def main(argv):
    if len(argv) not in (3,4):
        print("Usage: verify_output.py FIELD EVAL [RESULT]",file=sys.stderr)
        return 2

    field=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    ev=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors=[]

    rels=field["relations"]
    current={}
    new_expected={}
    open_subjects=set()

    for r in rels:
        s=r.get("subject")
        p=r.get("predicate")
        if p=="CURRENT_CANDIDATE_STATE":
            current[s]=r["object"]
        elif p=="REVISED_EXPECTED_CURRENT_STATE":
            new_expected[s]=r["object"]
        elif p=="TEMPORAL_RULE_STATUS" and r.get("object")=="TRANSITION_OPEN":
            open_subjects.add(s)

    events=defaultdict(list)
    for e in ev.get("events",[]):
        if e.get("rule") in {RULE_OLD,RULE_NEW}:
            events[(e["rule"],e["subject"])].append(e["event"])

    old_common_mismatch=0
    new_common_mismatch=0
    common=0
    old_all_eval=0
    old_all_mm=0
    new_all_eval=0
    new_all_mm=0
    mid_count=0

    for i in range(1,N+1):
        s=f"ASSESSMENT_{i:05d}"
        cur=current.get(s)

        if cur==MID:
            mid_count+=1
            continue

        oe=events.get((RULE_OLD,s),[])
        if len(oe)!=1:
            errors.append(f"{s}: old event cardinality {oe}")
        else:
            old_all_eval+=1
            old_all_mm+=int(oe[0]=="FORMAL_MISMATCH")

        if s in new_expected:
            ne=events.get((RULE_NEW,s),[])
            if len(ne)!=1:
                errors.append(f"{s}: new event cardinality {ne}")
            else:
                new_all_eval+=1
                new_all_mm+=int(ne[0]=="FORMAL_MISMATCH")
                if len(oe)==1:
                    common+=1
                    old_common_mismatch+=int(oe[0]=="FORMAL_MISMATCH")
                    new_common_mismatch+=int(ne[0]=="FORMAL_MISMATCH")
        elif s not in open_subjects:
            errors.append(f"{s}: neither revised expectation nor TRANSITION_OPEN")

    old_frac=old_common_mismatch/common if common else None
    new_frac=new_common_mismatch/common if common else None
    improves=(new_frac is not None and old_frac is not None and new_frac<old_frac)
    rel_reduction=((old_common_mismatch-new_common_mismatch)/old_common_mismatch if old_common_mismatch else 0.0)

    out={
        "experiment":"NOEPEDIA_EXP_033_RULE_REVISION_LOOP",
        "architectural_pass":not errors,
        "errors":errors,
        "old_rule":{
            "evaluated":old_all_eval,
            "mismatches":old_all_mm,
            "fraction":old_all_mm/old_all_eval if old_all_eval else None
        },
        "revised_rule":{
            "evaluated":new_all_eval,
            "mismatches":new_all_mm,
            "fraction":new_all_mm/new_all_eval if new_all_eval else None
        },
        "transition_open_count":len(open_subjects),
        "mid_unresolved_count":mid_count,
        "common_subset":{
            "count":common,
            "old_mismatches":old_common_mismatch,
            "revised_mismatches":new_common_mismatch,
            "old_fraction":old_frac,
            "revised_fraction":new_frac,
            "relative_mismatch_reduction":rel_reduction
        },
        "result":"REVISION_IMPROVES_FIELD" if improves else "REVISION_DOES_NOT_IMPROVE_FIELD",
        "strong_flag":rel_reduction>=0.90,
        "open_refinement":{
            "resolved_component":"direction-dependent LOAD_OFF temporal exception",
            "remaining_open":"residual mismatches, transition-zone interpretation, long-tail events, physical mechanism"
        }
    }

    rendered=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    print(rendered,end="")
    if len(argv)==4:
        Path(argv[3]).write_text(rendered,encoding="utf-8")
    return 0 if not errors else 1

if __name__=="__main__":
    raise SystemExit(main(sys.argv))
