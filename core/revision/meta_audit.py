#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from typing import Any


VALID_DECISIONS={"PROMOTE","REJECT","REMAIN_OPEN"}
VALID_STRATEGIES={"DENSE","SPARSE","CONSERVATIVE"}


def summarize_strategy_outcomes(records:list[dict[str,Any]]) -> dict[str,Any]:
    groups=defaultdict(list)
    invalid=[]

    for i,raw in enumerate(records):
        r=dict(raw)
        strategy=r.get("strategy_name")
        decision=r.get("decision")
        graph_valid=r.get("graph_valid",True)

        if strategy not in VALID_STRATEGIES or decision not in VALID_DECISIONS:
            invalid.append({"index":i,"record":r})
            continue

        groups[strategy].append({
            "decision":decision,
            "graph_valid":bool(graph_valid),
            "profile_class":r.get("profile_class"),
            "run_id":r.get("run_id"),
        })

    summary={}
    for strategy in sorted(VALID_STRATEGIES):
        rs=groups.get(strategy,[])
        n=len(rs)
        counts={d:sum(x["decision"]==d for x in rs) for d in sorted(VALID_DECISIONS)}
        valid_count=sum(x["graph_valid"] for x in rs)
        summary[strategy]={
            "sample_count":n,
            "promote_count":counts["PROMOTE"],
            "reject_count":counts["REJECT"],
            "remain_open_count":counts["REMAIN_OPEN"],
            "promotion_rate":counts["PROMOTE"]/n if n else None,
            "rejection_rate":counts["REJECT"]/n if n else None,
            "remain_open_rate":counts["REMAIN_OPEN"]/n if n else None,
            "graph_valid_rate":valid_count/n if n else None,
            "run_ids":[x["run_id"] for x in rs if x.get("run_id") is not None],
        }

    return {
        "strategies":summary,
        "invalid_records":invalid,
        "valid_record_count":sum(v["sample_count"] for v in summary.values()),
    }


def audit_meta_policy(
    records:list[dict[str,Any]],
    *,
    minimum_samples:int=5,
    low_promotion_rate:float=0.20,
    high_open_rate:float=0.60,
    minimum_graph_valid_rate:float=1.0,
) -> dict[str,Any]:
    summary=summarize_strategy_outcomes(records)
    recommendations=[]

    for strategy,stats in summary["strategies"].items():
        n=stats["sample_count"]

        if n<minimum_samples:
            recommendations.append({
                "strategy_name":strategy,
                "status":"INSUFFICIENT_EVIDENCE",
                "action":"KEEP",
                "reason":"MINIMUM_SAMPLE_GATE_NOT_MET",
                "sample_count":n,
            })
            continue

        if stats["graph_valid_rate"] is None or stats["graph_valid_rate"]<minimum_graph_valid_rate:
            recommendations.append({
                "strategy_name":strategy,
                "status":"IMPLEMENTATION_REVIEW_REQUIRED",
                "action":"REVIEW",
                "reason":"GRAPH_VALIDITY_BELOW_GATE",
                "sample_count":n,
            })
            continue

        if stats["promotion_rate"]<=low_promotion_rate and stats["remain_open_rate"]>=high_open_rate:
            recommendations.append({
                "strategy_name":strategy,
                "status":"META_POLICY_CANDIDATE",
                "action":"REVIEW_SELECTION_BOUNDARY",
                "reason":"LOW_PROMOTION_HIGH_OPEN_RATE",
                "sample_count":n,
                "evidence":{
                    "promotion_rate":stats["promotion_rate"],
                    "remain_open_rate":stats["remain_open_rate"],
                },
            })
        else:
            recommendations.append({
                "strategy_name":strategy,
                "status":"SUPPORTED_CURRENT_POLICY",
                "action":"KEEP",
                "reason":"OUTCOME_PROFILE_WITHIN_GATES",
                "sample_count":n,
                "evidence":{
                    "promotion_rate":stats["promotion_rate"],
                    "rejection_rate":stats["rejection_rate"],
                    "remain_open_rate":stats["remain_open_rate"],
                },
            })

    candidate_changes=[
        r for r in recommendations if r["status"]=="META_POLICY_CANDIDATE"
    ]

    return {
        "record_type":"META_POLICY_SELF_AUDIT",
        "summary":summary,
        "audit_gates":{
            "minimum_samples":minimum_samples,
            "low_promotion_rate":low_promotion_rate,
            "high_open_rate":high_open_rate,
            "minimum_graph_valid_rate":minimum_graph_valid_rate,
        },
        "recommendations":recommendations,
        "candidate_changes":candidate_changes,
        "policy_mutated":False,
    }


def build_meta_policy_candidate(audit:dict[str,Any]) -> dict[str,Any]:
    changes=audit.get("candidate_changes",[])
    if not changes:
        return {
            "type":"META_POLICY_CANDIDATE",
            "status":"NO_CHANGE_PROPOSED",
            "proposals":[],
            "source_audit":audit["record_type"],
        }

    proposals=[]
    for change in changes:
        strategy=change["strategy_name"]
        proposals.append({
            "target_strategy":strategy,
            "proposal":"REVIEW_SELECTION_BOUNDARY",
            "reason":change["reason"],
            "evidence":change.get("evidence",{}),
            "requires_preregistered_confirmation":True,
        })

    return {
        "type":"META_POLICY_CANDIDATE",
        "status":"PROPOSED_NOT_APPLIED",
        "proposals":proposals,
        "source_audit":audit["record_type"],
    }
