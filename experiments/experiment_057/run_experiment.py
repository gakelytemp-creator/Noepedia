#!/usr/bin/env python3
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))
from core.revision.evaluator import LOW,HIGH
from core.revision.graph_pipeline import run_graph_native_revision

def sparse(rid,series):
    out=[]; prev=None
    for i,s in enumerate(series,1):
        if s!=prev:
            out.append({"relation_id":rid,"time":i,"state":s,"sequence":0,"event_id":rid+"-"+str(i)})
            prev=s
    return out

def delayed(src,lag):
    out=list(src); last=None; before=None
    for i in range(1,len(src)):
        if src[i-1]==HIGH and src[i]==LOW:
            last=i; before=HIGH
        out[i]=before if last is not None and 0<=i-last<=lag else src[i]
    return out

def main():
    src=[]
    for _ in range(8):
        src += [LOW]*12+[HIGH]*12
    tgt=delayed(src,3)
    events=sparse("A_SOURCE",src)+sparse("B_TEMPORAL",tgt)+sparse("C_IDENTICAL",src)

    pos=run_graph_native_revision(
        events=events,
        relation_ids=["A_SOURCE","B_TEMPORAL","C_IDENTICAL"],
        timeline=list(range(1,len(src)+1)),
        discovery_end_index=120,
        confirmation_start_index=144,
        parent_rule_id="RULE_GRAPH_V1",
        open_id="OPEN_GRAPH",
        proposed_new_rule_id="RULE_GRAPH_V2",
        pair_candidates=[("A_SOURCE","B_TEMPORAL"),("A_SOURCE","C_IDENTICAL")],
        feature_config={"transition_radius":4,"temporal_fraction_threshold":0.70,"direction_ratio_threshold":2.0,"local_run_min":3,"local_run_fraction_threshold":0.20},
        evaluator_config={"lag_search":{"min":1,"max":6},"directions":["LOW_TO_HIGH","HIGH_TO_LOW"],"permutation_shifts":[5,11,17]},
        minimum_pair_score=1.0,
        max_forward_fill_steps=20
    )

    q=[LOW,HIGH]*40
    quiet=run_graph_native_revision(
        events=sparse("Q1",q)+sparse("Q2",q),
        relation_ids=["Q1","Q2"],
        timeline=list(range(1,len(q)+1)),
        discovery_end_index=50,
        confirmation_start_index=60,
        parent_rule_id="RULE_QUIET_V1",
        open_id="OPEN_QUIET",
        pair_candidates=[("Q1","Q2")],
        feature_config={"transition_radius":1},
        evaluator_config={},
        minimum_pair_score=1.0,
        max_forward_fill_steps=4
    )

    rev=pos["revision"]
    new_rules=[o for o in rev["graph"]["objects"] if o.get("type")=="RULE" and o["id"]!="RULE_GRAPH_V1"]
    checks={
      "pair":pos["selected_pair"]["source"]=="A_SOURCE" and pos["selected_pair"]["target"]=="B_TEMPORAL",
      "features":"TEMPORAL_CLUSTERING" in rev["feature_context"]["features"] and "DIRECTION_ASYMMETRY" in rev["feature_context"]["features"],
      "lag":rev["evaluation"]["frozen_parameters"]["lag"]==3,
      "promote":pos["final_decision"]=="PROMOTE",
      "graph":rev["graph_invariants"]["all_pass"] is True,
      "one_new_rule":len(new_rules)==1,
      "quiet_no_pair":quiet["selected_pair"] is None,
      "quiet_open":quiet["final_decision"]=="REMAIN_OPEN"
    }
    out={"experiment":"NOEPEDIA_EXP_057_GRAPH_NATIVE_END_TO_END_REVISION","checks":checks,"architectural_pass":all(checks.values()),"positive":{"selected_pair":pos["selected_pair"],"decision":pos["final_decision"],"frozen_parameters":rev["evaluation"]["frozen_parameters"],"new_rule_count":len(new_rules)},"quiet":{"decision":quiet["final_decision"],"reason":quiet["decision_reason"]}}
    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
