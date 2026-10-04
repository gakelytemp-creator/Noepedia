#!/usr/bin/env python3
from __future__ import annotations
from typing import Any


def _null(name, targets_failure_mode, required=True, params=None):
    return {
        "name":name,
        "targets_failure_mode":targets_failure_mode,
        "required":required,
        "parameters":params or {}
    }


def select_nulls(candidate: dict[str, Any], case_context: dict[str, Any]) -> list[dict[str, Any]]:
    """Select null-model specifications from candidate family and explicit risk flags."""
    family=candidate["family"]
    risks=set(case_context.get("risk_flags", []))
    out=[]

    if "CLASS_IMBALANCE" in risks or family in {
        "TEMPORAL_LAG_REVISION","DIRECTION_SPECIFIC_RULE","RELATION_ORIENTATION_REVISION"
    }:
        out.append(_null(
            "MAJORITY_STATE_NULL",
            "CLASS_IMBALANCE",
            required=True
        ))

    if family in {"TEMPORAL_LAG_REVISION","DIRECTION_SPECIFIC_RULE"}:
        out.append(_null(
            "TIME_SHIFT_OR_PERMUTATION_NULL",
            "TEMPORAL_ALIGNMENT_ARTIFACT",
            required=True,
            params={"method":"CIRCULAR_SHIFT","shifts":"PREREGISTER"}
        ))

    if family=="THRESHOLD_REFINEMENT":
        out.append(_null(
            "THRESHOLD_PERTURBATION_NULL",
            "THRESHOLD_PLACEMENT_ARTIFACT",
            required=True,
            params={"grid":"PREREGISTER_AROUND_FROZEN_THRESHOLD"}
        ))

    if family=="LOCAL_EXCEPTION_CANDIDATE":
        out.append(_null(
            "OUT_OF_CLUSTER_TRANSFER_TEST",
            "LOCAL_OVERFIT",
            required=True,
            params={"requires_new_untouched_window":True}
        ))

    if "SIMPLE_BASELINE_PLAUSIBLE" in risks or family=="SIMPLER_RULE_COMPARATOR":
        out.append(_null(
            "SIMPLER_RULE_NULL",
            "UNNECESSARY_COMPLEXITY",
            required=True
        ))

    if case_context.get("search_is_bounded",False):
        out.append(_null(
            "SEARCH_BOUNDARY_CHECK",
            "BOUNDARY_OPTIMUM",
            required=True,
            params={"policy":"REMAIN_OPEN_UNLESS_BOUNDARY_RESOLVED"}
        ))

    # deterministic dedup
    seen=set()
    dedup=[]
    for n in out:
        if n["name"] not in seen:
            seen.add(n["name"])
            dedup.append(n)
    return dedup


def build_preregistration_template(candidate: dict[str, Any], nulls: list[dict[str, Any]], case_context: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id":candidate["candidate_id"],
        "candidate_family":candidate["family"],
        "status":"DRAFT_PREREGISTRATION",
        "must_freeze_before_confirmation":[
            "candidate_parameters",
            "confirmation_window",
            "primary_metric",
            "success_gate",
            "evaluator_identity",
            "claim_boundary"
        ],
        "required_nulls":nulls,
        "discovery_confirmation_must_differ":True,
        "unresolved_rows_count_as_success":False
    }
