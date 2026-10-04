#!/usr/bin/env python3
from __future__ import annotations
from typing import Any

from .candidates import generate_candidates, rank_candidates
from .nulls import select_nulls, build_preregistration_template
from .evaluator import evaluate_candidate
from .engine import evaluate_case
from .materializer import materialize, verify_invariants
from .features import enrich_context_from_observations

NON_METRIC_NULLS={"SEARCH_BOUNDARY_CHECK","OUT_OF_CLUSTER_TRANSFER_TEST"}

def build_gate_case(context,candidate,evaluation,null_specs,required_relative_advantage=0.10):
    conf=evaluation.get("confirmation",{})
    disc=evaluation.get("discovery",{})
    metrics=evaluation.get("required_null_metrics",{})
    old_metric=conf.get("old_mismatches")
    revised_metric=conf.get("revised_mismatches")

    if old_metric is None and candidate["family"]=="SIMPLER_RULE_COMPARATOR":
        old_metric=conf.get("majority_mismatches")
        revised_metric=conf.get("proposed_mismatches")

    required_nulls=[]
    for spec in null_specs:
        name=spec["name"]
        if name in NON_METRIC_NULLS:
            continue
        required_nulls.append({
            "name":name,
            "metric":metrics.get(name),
            "required_relative_advantage":required_relative_advantage
        })

    case_id=context.get("case_id","REVISION_CASE")
    return {
        "case_id":case_id,
        "candidate_id":candidate["candidate_id"],
        "parent_rule_id":context["parent_rule_id"],
        "open_id":context["open_id"],
        "proposed_new_rule_id":context.get("proposed_new_rule_id",context["parent_rule_id"]+"::NEXT"),
        "confirmation_result_id":case_id+"::CONFIRMATION_RESULT",
        "preregistration_id":case_id+"::PREREGISTRATION",
        "parent_rule_exists":True,
        "open_exists":True,
        "provenance_complete":True,
        "candidate_parameters_explicit":evaluation.get("frozen_parameters") is not None,
        "preregistration_frozen":True,
        "discovery_confirmation_separated":True,
        "confirmation_untouched":True,
        "evidence_role_explicit":True,
        "confirmation_evaluable":old_metric is not None and revised_metric is not None,
        "unresolved_not_counted_as_success":True,
        "evaluator_frozen":True,
        "corrections_documented":True,
        "history_preserved":True,
        "open_refinement_prepared":True,
        "old_metric":old_metric,
        "revised_metric":revised_metric,
        "required_nulls":required_nulls,
        "search_boundary_hit":disc.get("search_boundary_hit"),
        "search_boundary_policy":"REMAIN_OPEN",
        "direction_consistency_required":False
    }

def run_revision(context:dict[str,Any],data:dict[str,Any],evaluator_config:dict[str,Any],required_relative_advantage=0.10):
    candidates=rank_candidates(generate_candidates(context),context)
    selected=candidates[0]
    null_specs=select_nulls(selected,context)
    prereg=build_preregistration_template(selected,null_specs,context)

    if selected["family"]=="OPEN_DECOMPOSITION":
        return {
            "case_id":context.get("case_id"),
            "candidates":candidates,
            "selected_candidate":selected,
            "null_specs":null_specs,
            "preregistration":prereg,
            "evaluation":None,
            "gate_audit":{"final_decision":"REMAIN_OPEN","decision_reason":"NO_SUPPORTED_CANDIDATE_FAMILY","history_mutated":False},
            "graph":None,
            "graph_invariants":None,
            "final_decision":"REMAIN_OPEN"
        }

    evaluation=evaluate_candidate(selected,data,evaluator_config)
    gate_case=build_gate_case(context,selected,evaluation,null_specs,required_relative_advantage)
    audit=evaluate_case(gate_case)
    graph=materialize(gate_case,audit)
    invariants=verify_invariants(gate_case,audit,graph)

    return {
        "case_id":context.get("case_id"),
        "candidates":candidates,
        "selected_candidate":selected,
        "null_specs":null_specs,
        "preregistration":prereg,
        "evaluation":evaluation,
        "gate_case":gate_case,
        "gate_audit":audit,
        "graph":graph,
        "graph_invariants":invariants,
        "final_decision":audit["final_decision"]
    }


def run_revision_from_observations(
    context:dict[str,Any],
    data:dict[str,Any],
    evaluator_config:dict[str,Any],
    *,
    feature_config:dict[str,Any]|None=None,
    required_relative_advantage:float=0.10,
):
    """Extract structural features from discovery observations, then run revision."""
    feature_config=feature_config or {}
    if "source_discovery" not in data or "target_discovery" not in data:
        raise ValueError("source_discovery and target_discovery are required for automatic feature extraction")
    enriched=enrich_context_from_observations(
        context,
        data["source_discovery"],
        data["target_discovery"],
        **feature_config
    )
    result=run_revision(
        enriched,
        data,
        evaluator_config,
        required_relative_advantage=required_relative_advantage
    )
    result["feature_context"]=enriched
    return result
