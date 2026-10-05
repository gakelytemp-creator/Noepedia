#!/usr/bin/env python3
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH,evaluate_simpler_rule_comparator
from core.revision.engine import evaluate_case
from core.revision.pipeline import (
    run_revision_from_observations,
    build_gate_case,
)
from core.revision.nulls import select_nulls


def temporal_source(reps=10):
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
    # Control A: discovery majority HIGH; confirmation prevalence flips LOW.
    # Source remains a perfect relation. Under the old comparator-candidate path,
    # source confirmation would beat the frozen discovery-majority baseline.
    target_d=[HIGH]*90+[LOW]*10
    source_d=list(target_d)
    target_c=[LOW]*90+[HIGH]*10
    source_c=list(target_c)

    prevalence=run_revision_from_observations(
        {
            "case_id":"EXP072_PREVALENCE_SHIFT",
            "parent_rule_id":"RULE072_PREV_V1",
            "open_id":"OPEN072_PREV",
            "proposed_new_rule_id":"RULE072_PREV_V2",
            "search_is_bounded":False,
        },
        {
            "source_discovery":source_d,
            "target_discovery":target_d,
            "source_confirmation":source_c,
            "target_confirmation":target_c,
            "proposed_confirmation":source_c,
        },
        {},
        feature_config=feature_config(),
    )

    # Control B: deterministic shuffled class-imbalance observation pair.
    shuffled_target=list(target_d)
    random.Random(72072).shuffle(shuffled_target)
    shuffled=run_revision_from_observations(
        {
            "case_id":"EXP072_SHUFFLED_IMBALANCE",
            "parent_rule_id":"RULE072_SHUF_V1",
            "open_id":"OPEN072_SHUF",
            "proposed_new_rule_id":"RULE072_SHUF_V2",
            "search_is_bounded":False,
        },
        {
            "source_discovery":source_d,
            "target_discovery":shuffled_target,
            "source_confirmation":source_c,
            "target_confirmation":target_c,
            "proposed_confirmation":source_c,
        },
        {},
        feature_config=feature_config(),
    )

    # Control C: explicit/direct comparator evaluation cannot become knowledge.
    comparator_candidate={
        "candidate_id":"RULE072_DIRECT::CAND_SIMPLER",
        "family":"SIMPLER_RULE_COMPARATOR",
        "parent_rule_id":"RULE072_DIRECT",
        "open_id":"OPEN072_DIRECT",
        "parameters":{"comparator":"MAJORITY_STATE"},
        "status":"PROPOSED",
    }
    comparator_eval=evaluate_simpler_rule_comparator(
        target_d,
        target_c,
        source_c,
    )
    comparator_context={
        "case_id":"EXP072_DIRECT_COMPARATOR",
        "parent_rule_id":"RULE072_DIRECT",
        "open_id":"OPEN072_DIRECT",
        "proposed_new_rule_id":"RULE072_DIRECT_V2",
        "search_is_bounded":False,
        "risk_flags":["CLASS_IMBALANCE","SIMPLE_BASELINE_PLAUSIBLE"],
    }
    comparator_nulls=select_nulls(comparator_candidate,comparator_context)
    comparator_case=build_gate_case(
        comparator_context,
        comparator_candidate,
        comparator_eval,
        comparator_nulls,
        required_relative_advantage=0.10,
    )
    comparator_audit=evaluate_case(comparator_case)

    # Control D: known temporal positive still promotes.
    src=temporal_source()
    tgt=delayed_target(src,3)
    split=120
    positive=run_revision_from_observations(
        {
            "case_id":"EXP072_TEMPORAL_POSITIVE",
            "parent_rule_id":"RULE072_POS_V1",
            "open_id":"OPEN072_POS",
            "proposed_new_rule_id":"RULE072_POS_V2",
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

    # Control E: simpler baseline remains mandatory null protection
    # for a genuine temporal candidate when the risk is explicit.
    protected=run_revision_from_observations(
        {
            "case_id":"EXP072_TEMPORAL_PROTECTED",
            "parent_rule_id":"RULE072_PROT_V1",
            "open_id":"OPEN072_PROT",
            "proposed_new_rule_id":"RULE072_PROT_V2",
            "lag_search":{"min":1,"max":6},
            "search_is_bounded":True,
            "risk_flags":["CLASS_IMBALANCE","SIMPLE_BASELINE_PLAUSIBLE"],
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

    prevalence_families=[c["family"] for c in prevalence["candidates"]]
    shuffled_families=[c["family"] for c in shuffled["candidates"]]
    protected_nulls={n["name"] for n in protected["null_specs"]}

    checks={
        "prevalence_class_imbalance_detected":
            "CLASS_IMBALANCE" in prevalence["feature_context"]["features"],
        "prevalence_no_comparator_candidate":
            "SIMPLER_RULE_COMPARATOR" not in prevalence_families,
        "prevalence_open_decomposition":
            prevalence["selected_candidate"]["family"]=="OPEN_DECOMPOSITION"
            and prevalence["final_decision"]=="REMAIN_OPEN",
        "shuffled_no_comparator_candidate":
            "SIMPLER_RULE_COMPARATOR" not in shuffled_families,
        "shuffled_does_not_promote":
            shuffled["final_decision"]!="PROMOTE",
        "direct_comparator_role_marked":
            comparator_eval.get("candidate_role")=="COMPARATOR_ONLY",
        "direct_comparator_not_promotable_flag":
            comparator_case["candidate_promotable"] is False,
        "direct_comparator_remains_open":
            comparator_audit["final_decision"]=="REMAIN_OPEN",
        "direct_comparator_reason":
            comparator_audit["decision_reason"]=="COMPARATOR_ONLY_NOT_PROMOTABLE",
        "direct_comparator_no_promoted_rule":
            "proposed_new_rule_record" not in comparator_audit,
        "temporal_positive_promotes":
            positive["final_decision"]=="PROMOTE",
        "temporal_positive_lag_3":
            positive["evaluation"]["frozen_parameters"]["lag"]==3,
        "simpler_null_still_protects_real_candidate":
            "SIMPLER_RULE_NULL" in protected_nulls,
        "protected_candidate_not_comparator":
            protected["selected_candidate"]["family"]!="SIMPLER_RULE_COMPARATOR",
    }

    out={
        "experiment":"NOEPEDIA_EXP_072_SIMPLER_RULE_FALSE_PROMOTION_REPAIR",
        "prevalence_shift":{
            "features":prevalence["feature_context"]["features"],
            "candidate_families":prevalence_families,
            "selected_family":prevalence["selected_candidate"]["family"],
            "decision":prevalence["final_decision"],
            "reason":prevalence["gate_audit"]["decision_reason"],
        },
        "shuffled":{
            "features":shuffled["feature_context"]["features"],
            "candidate_families":shuffled_families,
            "selected_family":shuffled["selected_candidate"]["family"],
            "decision":shuffled["final_decision"],
            "reason":shuffled["gate_audit"]["decision_reason"],
        },
        "direct_comparator":{
            "candidate_role":comparator_eval.get("candidate_role"),
            "candidate_promotable":comparator_case["candidate_promotable"],
            "decision":comparator_audit["final_decision"],
            "reason":comparator_audit["decision_reason"],
        },
        "temporal_positive":{
            "family":positive["selected_candidate"]["family"],
            "decision":positive["final_decision"],
            "reason":positive["gate_audit"]["decision_reason"],
            "frozen_parameters":positive["evaluation"]["frozen_parameters"],
        },
        "protected_temporal":{
            "family":protected["selected_candidate"]["family"],
            "nulls":[n["name"] for n in protected["null_specs"]],
            "decision":protected["final_decision"],
        },
        "checks":checks,
        "architectural_pass":all(checks.values()),
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(
        json.dumps(out,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return 0 if out["architectural_pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
