#!/usr/bin/env python3
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH,evaluate_temporal_candidate
from core.revision.engine import evaluate_case
from core.revision.pipeline import run_revision_from_observations,run_revision

def make_source(reps=10):
    out=[]
    for _ in range(reps):
        out.extend([LOW]*12)
        out.extend([HIGH]*12)
    return out

def delayed_target(source,lag):
    out=list(source)
    last=None
    for i in range(1,len(source)):
        if source[i-1]==HIGH and source[i]==LOW:
            last=i
        out[i]=HIGH if last is not None and 0<=i-last<=lag else source[i]
    return out

def feature_config():
    return {
        "transition_radius":4,
        "temporal_fraction_threshold":0.70,
        "class_imbalance_threshold":0.80,
        "direction_ratio_threshold":2.0,
        "local_run_min":3,
        "local_run_fraction_threshold":0.20,
    }

def evaluator_config():
    return {
        "lag_search":{"min":1,"max":6},
        "directions":["LOW_TO_HIGH","HIGH_TO_LOW"],
        "permutation_shifts":[11,23,37],
    }

def main():
    src=make_source()
    tgt=delayed_target(src,3)
    split=120

    positive=run_revision_from_observations(
        {
            "case_id":"EXP070_POSITIVE",
            "parent_rule_id":"RULE070_POS_V1",
            "open_id":"OPEN070_POS",
            "proposed_new_rule_id":"RULE070_POS_V2",
            "lag_search":{"min":1,"max":6},
            "search_is_bounded":True,
        },
        {
            "source_discovery":src[:split],
            "target_discovery":tgt[:split],
            "source_confirmation":src[split:],
            "target_confirmation":tgt[split:],
            "proposed_confirmation":src[split:],
        },
        evaluator_config(),
        feature_config=feature_config(),
        required_relative_advantage=0.10,
    )

    shuffled_tgt=list(tgt)
    random.Random(70070).shuffle(shuffled_tgt)
    negative=run_revision_from_observations(
        {
            "case_id":"EXP070_NEGATIVE",
            "parent_rule_id":"RULE070_NEG_V1",
            "open_id":"OPEN070_NEG",
            "proposed_new_rule_id":"RULE070_NEG_V2",
            "lag_search":{"min":1,"max":6},
            "search_is_bounded":True,
        },
        {
            "source_discovery":src[:split],
            "target_discovery":shuffled_tgt[:split],
            "source_confirmation":src[split:],
            "target_confirmation":shuffled_tgt[split:],
            "proposed_confirmation":src[split:],
        },
        evaluator_config(),
        feature_config=feature_config(),
        required_relative_advantage=0.10,
    )

    temporal=evaluate_temporal_candidate(
        src[:split],tgt[:split],src[split:],tgt[split:],
        lag_min=1,lag_max=6,
        directions=["LOW_TO_HIGH","HIGH_TO_LOW"],
        permutation_shifts=[11,23,37],
    )

    zero_case={
        "case_id":"EXP070_ZERO_NULL",
        "candidate_id":"CAND_ZERO",
        "parent_rule_id":"RULE_ZERO",
        "open_id":"OPEN_ZERO",
        "parent_rule_exists":True,
        "open_exists":True,
        "provenance_complete":True,
        "candidate_parameters_explicit":True,
        "preregistration_frozen":True,
        "discovery_confirmation_separated":True,
        "confirmation_untouched":True,
        "evidence_role_explicit":True,
        "confirmation_evaluable":True,
        "unresolved_not_counted_as_success":True,
        "evaluator_frozen":True,
        "corrections_documented":True,
        "history_preserved":True,
        "open_refinement_prepared":True,
        "old_metric":10,
        "revised_metric":1,
        "required_nulls":[
            {"name":"PERFECT_NULL","metric":0,"required_relative_advantage":0.10}
        ],
        "search_boundary_hit":False,
        "direction_consistency_required":False,
    }
    zero_audit=evaluate_case(zero_case)

    incompatible=run_revision(
        {
            "case_id":"EXP070_INCOMPATIBLE",
            "parent_rule_id":"RULE070_INC_V1",
            "open_id":"OPEN070_INC",
            "features":["THRESHOLD_SENSITIVITY","LOCAL_RESIDUAL_CLUSTER"],
            "risk_flags":[],
            "search_is_bounded":False,
        },
        {
            "source_discovery":[LOW,HIGH,LOW,HIGH],
            "target_discovery":[LOW,HIGH,HIGH,LOW],
            "source_confirmation":[LOW,HIGH,LOW,HIGH],
            "target_confirmation":[LOW,HIGH,HIGH,LOW],
        },
        {},
    )

    positive_nulls={n["name"] for n in positive["null_specs"]}
    positive_metrics=(positive["evaluation"] or {}).get("required_null_metrics",{})

    checks={
        "temporal_evaluator_exposes_simpler_rule_null":
            "SIMPLER_RULE_NULL" in temporal["required_null_metrics"],
        "simpler_rule_metric_equals_majority_metric":
            temporal["required_null_metrics"]["SIMPLER_RULE_NULL"]
            == temporal["required_null_metrics"]["MAJORITY_STATE_NULL"],
        "positive_promotes":
            positive["final_decision"]=="PROMOTE",
        "positive_no_required_null_unavailable":
            positive["gate_audit"]["decision_reason"]!="REQUIRED_NULL_UNAVAILABLE",
        "positive_metrics_complete":
            all(positive_metrics.get(name) is not None
                for name in positive_nulls
                if name not in {"SEARCH_BOUNDARY_CHECK","OUT_OF_CLUSTER_TRANSFER_TEST"}),
        "negative_does_not_promote":
            negative["final_decision"]!="PROMOTE",
        "zero_null_is_reject":
            zero_audit["final_decision"]=="REJECT",
        "zero_null_reason":
            zero_audit["decision_reason"]=="NULL_NOT_BEATEN",
        "incompatible_families_filtered":
            incompatible["selected_candidate"]["family"]=="OPEN_DECOMPOSITION",
        "incompatible_remains_open_without_exception":
            incompatible["final_decision"]=="REMAIN_OPEN"
            and incompatible["gate_audit"]["decision_reason"]=="NO_SUPPORTED_CANDIDATE_FAMILY",
    }

    out={
        "experiment":"NOEPEDIA_EXP_070_GATE_COVERAGE_REPAIR",
        "positive":{
            "family":positive["selected_candidate"]["family"],
            "decision":positive["final_decision"],
            "reason":positive["gate_audit"]["decision_reason"],
            "nulls":[n["name"] for n in positive["null_specs"]],
            "null_metrics":positive_metrics,
            "frozen_parameters":positive["evaluation"]["frozen_parameters"],
        },
        "negative":{
            "family":negative["selected_candidate"]["family"],
            "decision":negative["final_decision"],
            "reason":negative["gate_audit"]["decision_reason"],
        },
        "zero_null":{
            "decision":zero_audit["final_decision"],
            "reason":zero_audit["decision_reason"],
        },
        "incompatible":{
            "selected_family":incompatible["selected_candidate"]["family"],
            "decision":incompatible["final_decision"],
            "reason":incompatible["gate_audit"]["decision_reason"],
        },
        "checks":checks,
        "architectural_pass":all(checks.values()),
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
