#!/usr/bin/env python3
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.branching import create_branch, replay_branch
from core.revision.branch_merge import analyze_merge, create_merged_branch, compare_merge_with_parents, materialize_merge

def evaluator(definition,case):
    if case["profile_class"]=="SMALL":
        return definition["small_history_strategy"]
    if case["profile_class"]=="DENSE":
        return definition["dense_history_strategy"]
    return "SPARSE"

def main():
    parent_def={
        "small_history_strategy":"CONSERVATIVE",
        "dense_history_strategy":"DENSE"
    }
    parent_id="META_POLICY_V1"

    a=create_branch(parent_id,"BRANCH_A",{
        "small_history_strategy":"SPARSE",
        "dense_history_strategy":"DENSE"
    },"improve small histories")

    b=create_branch(parent_id,"BRANCH_B",{
        "small_history_strategy":"CONSERVATIVE",
        "dense_history_strategy":"SPARSE"
    },"improve dense histories")

    analysis=analyze_merge(parent_def,a,b)
    merged=create_merged_branch(parent_id,"MERGED_AB",a,b,analysis)

    cases=[
        {"case_id":"s1","profile_class":"SMALL","preferred_outcome":"SPARSE"},
        {"case_id":"s2","profile_class":"SMALL","preferred_outcome":"SPARSE"},
        {"case_id":"s3","profile_class":"SMALL","preferred_outcome":"SPARSE"},
        {"case_id":"d1","profile_class":"DENSE","preferred_outcome":"SPARSE"},
        {"case_id":"d2","profile_class":"DENSE","preferred_outcome":"SPARSE"},
        {"case_id":"d3","profile_class":"DENSE","preferred_outcome":"SPARSE"},
        {"case_id":"x1","profile_class":"SPARSE","preferred_outcome":"SPARSE"},
        {"case_id":"x2","profile_class":"SPARSE","preferred_outcome":"SPARSE"}
    ]

    ra=replay_branch(a,cases,evaluator)
    rb=replay_branch(b,cases,evaluator)
    rm=replay_branch(merged,cases,evaluator)
    cmp=compare_merge_with_parents(rm,[ra,rb],minimum_samples=6,max_accuracy_loss=0.0,minimum_graph_valid_rate=1.0)
    mat=materialize_merge(parent_id,a,b,merged,cmp)

    conflict_b=create_branch(parent_id,"BRANCH_CONFLICT",{
        "small_history_strategy":"DENSE",
        "dense_history_strategy":"DENSE"
    },"conflicting small-history change")
    conflict_analysis=analyze_merge(parent_def,a,conflict_b)
    conflict_merge=create_merged_branch(parent_id,"MERGED_CONFLICT",a,conflict_b,conflict_analysis)

    checks={
        "non_conflicting_mergeable":analysis["status"]=="MERGEABLE",
        "merged_definition_combines_fields":
            merged["definition"]["small_history_strategy"]=="SPARSE"
            and merged["definition"]["dense_history_strategy"]=="SPARSE",
        "merge_accuracy_is_one":rm["accuracy"]==1.0,
        "merge_no_worse_than_best_parent":cmp["status"]=="MERGE_WINNER_CANDIDATE",
        "history_preserved":any(o.get("id")==parent_id for o in mat["objects"]),
        "active_not_mutated":mat["active_policy_mutated"] is False,
        "merge_has_two_sources":
            sum(r["predicate"]=="MERGED_FROM_BRANCH" for r in mat["relations"])==2,
        "conflict_detected":conflict_analysis["status"]=="MERGE_CONFLICT",
        "conflict_merge_not_created":conflict_merge["status"]=="NOT_CREATED"
    }

    out={
        "experiment":"NOEPEDIA_EXP_066_BRANCH_MERGE",
        "branch_a":ra,
        "branch_b":rb,
        "merged":rm,
        "comparison":cmp,
        "conflict_analysis":conflict_analysis,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
