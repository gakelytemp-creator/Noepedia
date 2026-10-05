#!/usr/bin/env python3
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.branching import create_branch, replay_branch, compare_branches, materialize_branch_comparison

def evaluator(definition, case):
    if case["profile_class"]=="SMALL":
        return definition["small_history_strategy"]
    return "DENSE" if case["profile_class"]=="DENSE" else "SPARSE"

def main():
    parent="META_POLICY_V1"
    b1=create_branch(parent,"META_POLICY_V1_A",{"small_history_strategy":"CONSERVATIVE"},"retain current boundary")
    b2=create_branch(parent,"META_POLICY_V1_B",{"small_history_strategy":"SPARSE"},"candidate relaxed boundary")

    cases=[
      {"case_id":"c1","profile_class":"SMALL","preferred_outcome":"SPARSE"},
      {"case_id":"c2","profile_class":"SMALL","preferred_outcome":"SPARSE"},
      {"case_id":"c3","profile_class":"SMALL","preferred_outcome":"SPARSE"},
      {"case_id":"c4","profile_class":"DENSE","preferred_outcome":"DENSE"},
      {"case_id":"c5","profile_class":"SPARSE","preferred_outcome":"SPARSE"},
      {"case_id":"c6","profile_class":"SPARSE","preferred_outcome":"SPARSE"},
      {"case_id":"c7","profile_class":"DENSE","preferred_outcome":"DENSE"},
      {"case_id":"c8","profile_class":"SMALL","preferred_outcome":"SPARSE"}
    ]

    r1=replay_branch(b1,cases,evaluator)
    r2=replay_branch(b2,cases,evaluator)
    cmp=compare_branches([r1,r2],minimum_samples=6,minimum_accuracy_margin=0.10,minimum_graph_valid_rate=1.0)
    mat=materialize_branch_comparison(parent,[b1,b2],cmp)

    close1=dict(r1); close1["accuracy"]=0.75; close1["branch_id"]="CLOSE_A"
    close2=dict(r2); close2["accuracy"]=0.70; close2["branch_id"]="CLOSE_B"
    close_cmp=compare_branches([close1,close2],minimum_samples=6,minimum_accuracy_margin=0.10,minimum_graph_valid_rate=1.0)

    checks={
      "same_parent":b1["parent_id"]==parent and b2["parent_id"]==parent,
      "same_replay_sample_count":r1["sample_count"]==r2["sample_count"]==8,
      "branch_b_wins":cmp["status"]=="BRANCH_WINNER_CANDIDATE" and cmp["winner"]=="META_POLICY_V1_B",
      "winner_margin_passed":cmp["accuracy_margin"]>=0.10,
      "parent_preserved":any(o.get("id")==parent and o.get("status")=="PRESERVED" for o in mat["objects"]),
      "active_not_mutated":mat["active_policy_mutated"] is False,
      "branches_linked_to_parent":sum(r["predicate"]=="BRANCHED_FROM_META_POLICY" for r in mat["relations"])==2,
      "close_case_remains_open":close_cmp["status"]=="REMAIN_OPEN" and close_cmp["winner"] is None
    }

    out={
      "experiment":"NOEPEDIA_EXP_065_POLICY_BRANCHING_REPLAY",
      "branch_a":r1,
      "branch_b":r2,
      "comparison":cmp,
      "close_comparison":close_cmp,
      "checks":checks,
      "architectural_pass":all(checks.values())
    }
    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
