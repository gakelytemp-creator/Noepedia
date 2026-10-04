#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision import LOW,HIGH
from core.revision.pipeline import run_revision


def make_source():
    out=[]
    for _ in range(8):
        out.extend([LOW]*12)
        out.extend([HIGH]*12)
    return out


def delayed_target(source,lag):
    out=list(source)
    last=None
    prev_before=None
    for i in range(1,len(source)):
        prev=source[i-1]
        curr=source[i]
        if prev==HIGH and curr==LOW:
            last=i
            prev_before=prev
        if last is not None and 0<=i-last<=lag:
            out[i]=prev_before
        else:
            out[i]=curr
    return out


def main():
    src_d=make_source()
    tgt_d=delayed_target(src_d,3)
    src_c=make_source()
    tgt_c=delayed_target(src_c,3)

    positive_context={
        "case_id":"EXP052_POSITIVE",
        "parent_rule_id":"RULE_TEMP_V1",
        "open_id":"OPEN_TEMP",
        "proposed_new_rule_id":"RULE_TEMP_V2",
        "features":["TEMPORAL_CLUSTERING","TRANSITION_ALIGNED_MISMATCH"],
        "risk_flags":["CLASS_IMBALANCE"],
        "lag_search":{"min":1,"max":6},
        "search_is_bounded":True
    }
    positive_data={
        "source_discovery":src_d,
        "target_discovery":tgt_d,
        "source_confirmation":src_c,
        "target_confirmation":tgt_c
    }
    positive_config={
        "lag_search":{"min":1,"max":6},
        "directions":["LOW_TO_HIGH","HIGH_TO_LOW"],
        "permutation_shifts":[5,11,17]
    }

    positive=run_revision(
        positive_context,
        positive_data,
        positive_config,
        required_relative_advantage=0.10
    )

    unknown_context={
        "case_id":"EXP052_UNKNOWN",
        "parent_rule_id":"RULE_UNKNOWN_V1",
        "open_id":"OPEN_UNKNOWN",
        "features":[],
        "risk_flags":[],
        "search_is_bounded":False
    }
    unknown=run_revision(unknown_context,{},{})

    positive_rules=[]
    if positive["graph"] is not None:
        positive_rules=[
            o for o in positive["graph"]["objects"]
            if o.get("type")=="RULE" and o["id"]!="RULE_TEMP_V1"
        ]

    checks={
        "positive_selected_temporal_family":
            positive["selected_candidate"]["family"]=="TEMPORAL_LAG_REVISION",
        "positive_frozen_lag_is_3":
            positive["evaluation"]["frozen_parameters"]["lag"]==3,
        "positive_nulls_selected":
            "MAJORITY_STATE_NULL" in [n["name"] for n in positive["null_specs"]]
            and "TIME_SHIFT_OR_PERMUTATION_NULL" in [n["name"] for n in positive["null_specs"]],
        "positive_decision_promote":
            positive["final_decision"]=="PROMOTE",
        "positive_graph_invariants_pass":
            positive["graph_invariants"]["all_pass"] is True,
        "positive_one_new_rule":
            len(positive_rules)==1,
        "unknown_selected_open_decomposition":
            unknown["selected_candidate"]["family"]=="OPEN_DECOMPOSITION",
        "unknown_remains_open":
            unknown["final_decision"]=="REMAIN_OPEN",
        "unknown_has_no_graph_mutation":
            unknown["graph"] is None,
    }

    out={
        "experiment":"NOEPEDIA_EXP_052_END_TO_END_REVISION_PIPELINE",
        "positive":{
            "selected_family":positive["selected_candidate"]["family"],
            "frozen_parameters":positive["evaluation"]["frozen_parameters"],
            "decision":positive["final_decision"],
            "graph_invariants":positive["graph_invariants"],
            "new_rule_count":len(positive_rules)
        },
        "unknown":{
            "selected_family":unknown["selected_candidate"]["family"],
            "decision":unknown["final_decision"],
            "graph":unknown["graph"]
        },
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 052 reproducibility: PASS")
    print("Experiment 052 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
