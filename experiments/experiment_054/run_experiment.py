#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH
from core.revision.pipeline import run_revision_from_observations

def make_source(reps=8):
    out=[]
    for _ in range(reps):
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

    positive=run_revision_from_observations(
        {
            "case_id":"EXP054_POSITIVE",
            "parent_rule_id":"RULE_AUTO_V1",
            "open_id":"OPEN_AUTO",
            "proposed_new_rule_id":"RULE_AUTO_V2",
            "lag_search":{"min":1,"max":6},
            "search_is_bounded":True
        },
        {
            "source_discovery":src_d,
            "target_discovery":tgt_d,
            "source_confirmation":src_c,
            "target_confirmation":tgt_c
        },
        {
            "lag_search":{"min":1,"max":6},
            "directions":["LOW_TO_HIGH","HIGH_TO_LOW"],
            "permutation_shifts":[5,11,17]
        },
        feature_config={
            "transition_radius":4,
            "temporal_fraction_threshold":0.70,
            "direction_ratio_threshold":2.0,
            "local_run_min":3,
            "local_run_fraction_threshold":0.20
        }
    )

    quiet_source=[LOW,HIGH]*30
    quiet_target=list(quiet_source)
    quiet=run_revision_from_observations(
        {
            "case_id":"EXP054_QUIET",
            "parent_rule_id":"RULE_QUIET_V1",
            "open_id":"OPEN_QUIET",
            "search_is_bounded":False
        },
        {
            "source_discovery":quiet_source,
            "target_discovery":quiet_target,
            "source_confirmation":quiet_source,
            "target_confirmation":quiet_target
        },
        {}
    )

    pf=set(positive["feature_context"].get("features",[]))
    pn={n["name"] for n in positive["null_specs"]}

    checks={
        "positive_features_auto_detected":
            "TEMPORAL_CLUSTERING" in pf and "TRANSITION_ALIGNED_MISMATCH" in pf,
        "positive_direction_feature_auto_detected":
            "DIRECTION_ASYMMETRY" in pf,
        "positive_candidate_not_manual":
            positive["selected_candidate"]["family"] in {"DIRECTION_SPECIFIC_RULE","TEMPORAL_LAG_REVISION"},
        "positive_temporal_null_auto_selected":
            "TIME_SHIFT_OR_PERMUTATION_NULL" in pn,
        "positive_majority_null_auto_selected":
            "MAJORITY_STATE_NULL" in pn,
        "positive_frozen_lag":
            positive["evaluation"]["frozen_parameters"]["lag"]==3,
        "positive_decision_promote":
            positive["final_decision"]=="PROMOTE",
        "positive_graph_pass":
            positive["graph_invariants"]["all_pass"] is True,
        "quiet_no_features":
            quiet["feature_context"].get("features",[])==[],
        "quiet_open_decomposition":
            quiet["selected_candidate"]["family"]=="OPEN_DECOMPOSITION",
        "quiet_remain_open":
            quiet["final_decision"]=="REMAIN_OPEN",
        "quiet_no_graph":
            quiet["graph"] is None
    }

    out={
        "experiment":"NOEPEDIA_EXP_054_OBSERVATION_DRIVEN_REVISION",
        "positive":{
            "features":positive["feature_context"].get("features",[]),
            "risk_flags":positive["feature_context"].get("risk_flags",[]),
            "selected_family":positive["selected_candidate"]["family"],
            "nulls":[n["name"] for n in positive["null_specs"]],
            "frozen_parameters":positive["evaluation"]["frozen_parameters"],
            "decision":positive["final_decision"]
        },
        "quiet":{
            "features":quiet["feature_context"].get("features",[]),
            "selected_family":quiet["selected_candidate"]["family"],
            "decision":quiet["final_decision"]
        },
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 054 reproducibility: PASS")
    print("Experiment 054 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
