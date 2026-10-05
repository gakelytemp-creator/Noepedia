#!/usr/bin/env python3
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH
from core.revision.meta_policy import select_revision_strategy
from core.revision.graph_pipeline import run_graph_native_revision_auto_strategy

def sparse(rid,series):
    out=[]; prev=None
    for i,s in enumerate(series,1):
        if s!=prev:
            out.append({"relation_id":rid,"time":i,"state":s,"sequence":0,"event_id":rid+"-"+str(i)})
            prev=s
    return out

def source(reps=10):
    out=[]
    for _ in range(reps):
        out += [LOW]*12+[HIGH]*12
    return out

def delayed(src,lag):
    out=list(src); last=None
    for i in range(1,len(src)):
        if src[i-1]==HIGH and src[i]==LOW:
            last=i
        out[i]=HIGH if last is not None and 0<=i-last<=lag else src[i]
    return out

def dense_events():
    out=[]
    for t in range(1,61):
        for rid,phase in [("D1",0),("D2",1),("D3",2)]:
            s=HIGH if ((t+phase)%4)<2 else LOW
            out.append({"relation_id":rid,"time":t,"state":s,"sequence":0,"event_id":rid+"-"+str(t)})
    return out

def main():
    dense=select_revision_strategy(dense_events())

    src=source()
    tgt=delayed(src,3)
    sparse_events=sparse("A_SOURCE",src)+sparse("B_TEMPORAL",tgt)+sparse("C_IDENTICAL",src)
    sparse_sel=select_revision_strategy(sparse_events)

    small_events=[
        {"relation_id":"S1","time":1,"state":LOW,"sequence":0,"event_id":"s1"},
        {"relation_id":"S2","time":1,"state":HIGH,"sequence":0,"event_id":"s2"},
        {"relation_id":"S1","time":2,"state":HIGH,"sequence":0,"event_id":"s3"},
        {"relation_id":"S2","time":2,"state":LOW,"sequence":0,"event_id":"s4"},
    ]
    small=select_revision_strategy(small_events)

    auto=run_graph_native_revision_auto_strategy(
        events=sparse_events,
        parent_rule_id="RULE059_V1",
        open_id="OPEN059",
        proposed_new_rule_id="RULE059_V2"
    )

    checks={
        "dense_selects_dense":dense["strategy_name"]=="DENSE",
        "sparse_selects_sparse":sparse_sel["strategy_name"]=="SPARSE",
        "small_selects_conservative":small["strategy_name"]=="CONSERVATIVE",
        "auto_records_meta_policy":auto["meta_policy"]["strategy_name"]=="SPARSE",
        "auto_pair_selected":auto["selected_pair"] is not None,
        "auto_valid_decision":auto["final_decision"] in {"PROMOTE","REJECT","REMAIN_OPEN"},
        "auto_strategy_resolution_present":"strategy_resolution" in auto
    }
    out={
        "experiment":"NOEPEDIA_EXP_059_STRATEGY_META_POLICY",
        "dense":dense["strategy_name"],
        "sparse":sparse_sel["strategy_name"],
        "small":small["strategy_name"],
        "auto":{"strategy":auto["meta_policy"]["strategy_name"],"decision":auto["final_decision"],"pair":auto["selected_pair"]},
        "checks":checks,
        "architectural_pass":all(checks.values())
    }
    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
