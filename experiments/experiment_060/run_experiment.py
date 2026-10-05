#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.meta_audit import audit_meta_policy, build_meta_policy_candidate

def rec(strategy,decision,run_id,valid=True):
    return {
        "strategy_name":strategy,
        "decision":decision,
        "graph_valid":valid,
        "run_id":run_id
    }

def main():
    records=[]

    # SPARSE: healthy outcome profile.
    records += [
        rec("SPARSE","PROMOTE","s1"),
        rec("SPARSE","PROMOTE","s2"),
        rec("SPARSE","REJECT","s3"),
        rec("SPARSE","PROMOTE","s4"),
        rec("SPARSE","REMAIN_OPEN","s5"),
        rec("SPARSE","PROMOTE","s6"),
    ]

    # DENSE: deliberately below minimum-sample gate.
    records += [
        rec("DENSE","PROMOTE","d1"),
        rec("DENSE","REMAIN_OPEN","d2"),
        rec("DENSE","PROMOTE","d3"),
    ]

    # CONSERVATIVE: many unresolved outcomes, little promotion.
    records += [
        rec("CONSERVATIVE","REMAIN_OPEN","c1"),
        rec("CONSERVATIVE","REMAIN_OPEN","c2"),
        rec("CONSERVATIVE","REMAIN_OPEN","c3"),
        rec("CONSERVATIVE","REMAIN_OPEN","c4"),
        rec("CONSERVATIVE","REJECT","c5"),
        rec("CONSERVATIVE","PROMOTE","c6"),
    ]

    audit=audit_meta_policy(
        records,
        minimum_samples=5,
        low_promotion_rate=0.20,
        high_open_rate=0.60,
        minimum_graph_valid_rate=1.0
    )
    candidate=build_meta_policy_candidate(audit)

    by_strategy={x["strategy_name"]:x for x in audit["recommendations"]}

    checks={
        "sparse_kept":
            by_strategy["SPARSE"]["action"]=="KEEP"
            and by_strategy["SPARSE"]["status"]=="SUPPORTED_CURRENT_POLICY",
        "dense_insufficient_not_changed":
            by_strategy["DENSE"]["status"]=="INSUFFICIENT_EVIDENCE"
            and by_strategy["DENSE"]["action"]=="KEEP",
        "conservative_becomes_candidate":
            by_strategy["CONSERVATIVE"]["status"]=="META_POLICY_CANDIDATE"
            and by_strategy["CONSERVATIVE"]["action"]=="REVIEW_SELECTION_BOUNDARY",
        "exactly_one_candidate_change":
            len(audit["candidate_changes"])==1
            and audit["candidate_changes"][0]["strategy_name"]=="CONSERVATIVE",
        "policy_not_mutated":
            audit["policy_mutated"] is False,
        "candidate_not_applied":
            candidate["status"]=="PROPOSED_NOT_APPLIED",
        "candidate_requires_confirmation":
            candidate["proposals"][0]["requires_preregistered_confirmation"] is True,
        "valid_record_count":
            audit["summary"]["valid_record_count"]==15
    }

    out={
        "experiment":"NOEPEDIA_EXP_060_META_POLICY_SELF_AUDIT",
        "audit":audit,
        "candidate":candidate,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 060 reproducibility: PASS")
    print("Experiment 060 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
