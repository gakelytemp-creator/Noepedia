#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


def _candidate(cid, family, parent_rule_id, open_id, rationale, parameters=None, prerequisites=None):
    return {
        "candidate_id": cid,
        "family": family,
        "parent_rule_id": parent_rule_id,
        "open_id": open_id,
        "rationale": rationale,
        "parameters": parameters or {},
        "prerequisites": prerequisites or [],
        "status": "PROPOSED"
    }


def generate_candidates(case_context: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate conservative revision templates from explicit mismatch/Open metadata.

    This function does not infer domain semantics. It only maps observed structural
    features to reusable candidate families.
    """
    parent=case_context["parent_rule_id"]
    open_id=case_context["open_id"]
    features=set(case_context.get("features", []))
    out=[]

    if "TEMPORAL_CLUSTERING" in features or "TRANSITION_ALIGNED_MISMATCH" in features:
        out.append(_candidate(
            f"{parent}::CAND_TEMPORAL_LAG",
            "TEMPORAL_LAG_REVISION",
            parent,open_id,
            "Mismatch structure is aligned to source transitions or time offsets.",
            parameters={
                "direction_search":["LOW_TO_HIGH","HIGH_TO_LOW"],
                "lag_search":case_context.get("lag_search",{"min":1,"max":100})
            },
            prerequisites=["ORDERED_OBSERVATIONS","DISTINCT_DISCOVERY_CONFIRMATION"]
        ))

    if "DIRECTION_ASYMMETRY" in features:
        out.append(_candidate(
            f"{parent}::CAND_DIRECTION_SPLIT",
            "DIRECTION_SPECIFIC_RULE",
            parent,open_id,
            "Opposite transition directions show materially different behavior.",
            parameters={"directions":["LOW_TO_HIGH","HIGH_TO_LOW"]},
            prerequisites=["TRANSITION_IDENTITY_AVAILABLE"]
        ))

    if "THRESHOLD_SENSITIVITY" in features or "MID_BAND_UNCERTAINTY" in features:
        out.append(_candidate(
            f"{parent}::CAND_THRESHOLD_REFINEMENT",
            "THRESHOLD_REFINEMENT",
            parent,open_id,
            "Mismatch may depend on threshold placement or an unresolved intermediate band.",
            parameters={"threshold_policy":"DISCOVERY_ONLY_THEN_FREEZE"},
            prerequisites=["CONTINUOUS_TARGET","CALIBRATION_WINDOW"]
        ))

    if "ORIENTATION_UNCERTAINTY" in features:
        out.append(_candidate(
            f"{parent}::CAND_ORIENTATION_SPLIT",
            "RELATION_ORIENTATION_REVISION",
            parent,open_id,
            "Direct relation orientation is not yet justified.",
            parameters={"orientation_search":["DIRECT","INVERTED"]},
            prerequisites=["CALIBRATION_WINDOW"]
        ))

    if "LOCAL_RESIDUAL_CLUSTER" in features:
        out.append(_candidate(
            f"{parent}::CAND_LOCAL_EXCEPTION",
            "LOCAL_EXCEPTION_CANDIDATE",
            parent,open_id,
            "Residual mismatches form a compact local structure that may warrant separate confirmation.",
            parameters={"promotion_policy":"REQUIRES_NEW_UNTOUCHED_CONFIRMATION"},
            prerequisites=["RESIDUAL_GROUPING"]
        ))

    if "CLASS_IMBALANCE" in features:
        out.append(_candidate(
            f"{parent}::CAND_SIMPLER_BASELINE",
            "SIMPLER_RULE_COMPARATOR",
            parent,open_id,
            "Observed gain may be explained by target prevalence rather than relation structure.",
            parameters={"comparator":"MAJORITY_STATE"},
            prerequisites=[]
        ))

    if not out:
        out.append(_candidate(
            f"{parent}::CAND_DECOMPOSE_OPEN",
            "OPEN_DECOMPOSITION",
            parent,open_id,
            "No supported revision family can be generated from the supplied structural features.",
            parameters={"action":"DECOMPOSE_OR_COLLECT_MORE_EVIDENCE"},
            prerequisites=[]
        ))

    return out


def rank_candidates(candidates: list[dict[str, Any]], case_context: dict[str, Any]) -> list[dict[str, Any]]:
    """Deterministic structural priority; not a truth score."""
    priority={
        "DIRECTION_SPECIFIC_RULE":10,
        "TEMPORAL_LAG_REVISION":20,
        "THRESHOLD_REFINEMENT":30,
        "RELATION_ORIENTATION_REVISION":40,
        "LOCAL_EXCEPTION_CANDIDATE":50,
        "SIMPLER_RULE_COMPARATOR":60,
        "OPEN_DECOMPOSITION":100,
    }
    return sorted(candidates,key=lambda c:(priority.get(c["family"],999),c["candidate_id"]))
