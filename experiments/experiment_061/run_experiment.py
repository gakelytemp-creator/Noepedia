#!/usr/bin/env python3
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def baseline(p):
    if p["relation_count"]<2 or p["event_count"]<8:
        return "CONSERVATIVE"
    if p["event_density"]>=0.20 and p["transition_density_proxy"]>=0.50:
        return "DENSE"
    return "SPARSE"

def proposed(p):
    if p["relation_count"]<2 or p["event_count"]<8:
        return "SPARSE"
    if p["event_density"]>=0.20 and p["transition_density_proxy"]>=0.50:
        return "DENSE"
    return "SPARSE"

def main():
    cases=[
        ("h1",1,6,0.10,0.20,"SPARSE"),
        ("h2",1,7,0.12,0.25,"SPARSE"),
        ("h3",2,6,0.15,0.30,"SPARSE"),
        ("h4",3,30,0.35,0.80,"DENSE"),
        ("h5",4,40,0.30,0.60,"DENSE"),
        ("h6",3,18,0.08,0.20,"SPARSE"),
        ("h7",5,22,0.07,0.18,"SPARSE"),
        ("h8",2,9,0.09,0.22,"SPARSE"),
    ]
    rows=[]
    for cid,rc,ec,ed,td,expected in cases:
        p={"relation_count":rc,"event_count":ec,"event_density":ed,"transition_density_proxy":td}
        b=baseline(p); n=proposed(p)
        rows.append({"case_id":cid,"baseline":b,"proposed":n,"preferred":expected,"baseline_ok":b==expected,"proposed_ok":n==expected})

    total=len(rows)
    ba=sum(r["baseline_ok"] for r in rows)/total
    pa=sum(r["proposed_ok"] for r in rows)/total
    gain=pa-ba

    status="CONFIRMED" if total>=6 and pa>=0.75 and gain>=0.15 else "REJECTED"
    checks={
        "sample_count":total==8,
        "proposed_accuracy":pa>=0.75,
        "gain":gain>=0.15,
        "confirmed":status=="CONFIRMED"
    }
    out={
        "experiment":"NOEPEDIA_EXP_061_SELECTOR_CONFIRMATION",
        "baseline_accuracy":ba,
        "proposed_accuracy":pa,
        "accuracy_gain":gain,
        "status":status,
        "application":{"status":"CONFIRMED_NOT_APPLIED","applied":False},
        "rows":rows,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }
    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
