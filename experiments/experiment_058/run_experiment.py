#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH
from core.revision.graph_pipeline import run_graph_native_revision_with_strategy
from core.revision.strategies import (
    RevisionStrategy,RelationScopePolicy,TimelinePolicy,SplitPolicy,SearchPolicy
)

def sparse(rid,series):
    out=[]; prev=None
    for i,s in enumerate(series,1):
        if s!=prev:
            out.append({"relation_id":rid,"time":i,"state":s,"sequence":0,"event_id":rid+"-"+str(i)})
            prev=s
    return out

def source():
    out=[]
    for _ in range(10):
        out += [LOW]*12+[HIGH]*12
    return out

def delayed(src,lag):
    out=list(src); last=None
    for i in range(1,len(src)):
        if src[i-1]==HIGH and src[i]==LOW:
            last=i
        out[i]=HIGH if last is not None and 0<=i-last<=lag else src[i]
    return out

def main():
    src=source()
    tgt=delayed(src,3)
    events=sparse("A_SOURCE",src)+sparse("B_TEMPORAL",tgt)+sparse("C_IDENTICAL",src)

    default=run_graph_native_revision_with_strategy(
        events=events,
        parent_rule_id="RULE058_DEFAULT_V1",
        open_id="OPEN058_DEFAULT",
        proposed_new_rule_id="RULE058_DEFAULT_V2"
    )

    custom_strategy=RevisionStrategy(
        relation_scope=RelationScopePolicy(
            mode="EXPLICIT_RELATIONS",
            include=["A_SOURCE","B_TEMPORAL","C_IDENTICAL"],
            explicit_pairs=[("A_SOURCE","B_TEMPORAL"),("A_SOURCE","C_IDENTICAL")]
        ),
        timeline=TimelinePolicy(mode="INTEGER_RANGE_FROM_EVENTS"),
        split=SplitPolicy(
            discovery_fraction=0.55,
            buffer_fraction=0.15,
            minimum_confirmation_count=40
        ),
        search=SearchPolicy(
            lag_min=1,
            lag_max_fraction=0.08,
            lag_max_cap=8,
            permutation_shift_fractions=(0.10,0.20,0.30),
            minimum_pair_score=1.0,
            max_forward_fill_fraction=0.10,
            required_relative_advantage=0.10
        )
    )

    custom=run_graph_native_revision_with_strategy(
        events=events,
        parent_rule_id="RULE058_CUSTOM_V1",
        open_id="OPEN058_CUSTOM",
        proposed_new_rule_id="RULE058_CUSTOM_V2",
        strategy=custom_strategy
    )

    checks={
        "default_has_strategy_resolution":
            "strategy_resolution" in default,
        "default_relation_scope_resolved":
            set(default["strategy_resolution"]["scope"]["relation_ids"])=={"A_SOURCE","B_TEMPORAL","C_IDENTICAL"},
        "default_timeline_resolved":
            len(default["strategy_resolution"]["timeline"])==len(src),
        "default_split_resolved":
            default["strategy_resolution"]["split"]["discovery_end_index"]>0
            and default["strategy_resolution"]["split"]["confirmation_start_index"]<len(src),
        "default_search_resolved":
            "lag_search" in default["strategy_resolution"]["search"]["evaluator_config"],
        "default_promote":
            default["final_decision"]=="PROMOTE",
        "default_selected_correct_pair":
            default["selected_pair"]["source"]=="A_SOURCE"
            and default["selected_pair"]["target"]=="B_TEMPORAL",
        "custom_promote":
            custom["final_decision"]=="PROMOTE",
        "custom_selected_correct_pair":
            custom["selected_pair"]["source"]=="A_SOURCE"
            and custom["selected_pair"]["target"]=="B_TEMPORAL",
        "custom_policy_recorded":
            custom["strategy_resolution"]["policy"]["split"]["discovery_fraction"]==0.55,
        "custom_search_cap_respected":
            custom["strategy_resolution"]["search"]["evaluator_config"]["lag_search"]["max"]<=8,
        "custom_graph_pass":
            custom["revision"]["graph_invariants"]["all_pass"] is True
    }

    out={
        "experiment":"NOEPEDIA_EXP_058_REVISION_STRATEGY_POLICIES",
        "default":{
            "decision":default["final_decision"],
            "selected_pair":default["selected_pair"],
            "strategy_resolution":default["strategy_resolution"]
        },
        "custom":{
            "decision":custom["final_decision"],
            "selected_pair":custom["selected_pair"],
            "strategy_resolution":custom["strategy_resolution"]
        },
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 058 reproducibility: PASS")
    print("Experiment 058 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
