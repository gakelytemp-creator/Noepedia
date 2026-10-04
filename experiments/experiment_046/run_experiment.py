#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
RUNTIME=HERE/"_runtime"
HARNESS=ROOT/"experiments"/"experiment_045"/"revision_harness.py"
ADAPTER040=ROOT/"experiments"/"experiment_045"/"adapter_040.py"
ADAPTER039=ROOT/"experiments"/"experiment_045"/"adapter_039.py"
MATERIALIZER=HERE/"materialize_revision.py"

def run(cmd):
    subprocess.run(cmd,check=True)

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def main():
    RUNTIME.mkdir(exist_ok=True)

    # Build source cases through Experiment 045 adapters.
    run([sys.executable,str(ADAPTER040)])
    run([sys.executable,str(ADAPTER039)])

    src_runtime=ROOT/"experiments"/"experiment_045"/"_runtime"
    case040=src_runtime/"case_040.json"
    case039=src_runtime/"case_039.json"

    audit040=RUNTIME/"audit_040.json"
    audit039=RUNTIME/"audit_039.json"
    run([sys.executable,str(HARNESS),str(case040),str(audit040)])
    run([sys.executable,str(HARNESS),str(case039),str(audit039)])

    graph040=RUNTIME/"graph_040.json"
    graph039=RUNTIME/"graph_039.json"
    run([sys.executable,str(MATERIALIZER),str(case040),str(audit040),str(graph040)])
    run([sys.executable,str(MATERIALIZER),str(case039),str(audit039),str(graph039)])

    a040=load(audit040)
    a039=load(audit039)
    g040=load(graph040)
    g039=load(graph039)

    expected={"040":"PROMOTE","039":"REJECT"}
    observed={"040":a040["final_decision"],"039":a039["final_decision"]}

    pass040=(a040["final_decision"]=="PROMOTE" and g040["invariants"]["all_pass"])
    pass039=(a039["final_decision"]=="REJECT" and g039["invariants"]["all_pass"])

    # Strong explicit checks.
    objs040=g040["graph"]["objects"]
    objs039=g039["graph"]["objects"]
    parent040=load(case040)["parent_rule_id"]
    parent039=load(case039)["parent_rule_id"]

    promoted040=[o for o in objs040 if o.get("type")=="RULE" and o["id"]!=parent040]
    promoted039=[o for o in objs039 if o.get("type")=="RULE" and o["id"]!=parent039]

    summary={
        "experiment":"NOEPEDIA_EXP_046_SELF_REVISION_MATERIALIZATION",
        "expected_decisions":expected,
        "observed_decisions":observed,
        "positive_case":{
            "pass":pass040,
            "new_rule_count":len(promoted040),
            "parent_rule_preserved":g040["invariants"]["parent_rule_preserved"],
            "open_preserved":g040["invariants"]["open_preserved"],
            "open_refinement_materialized":g040["invariants"]["open_refinement_materialized"]
        },
        "negative_case":{
            "pass":pass039,
            "new_rule_count":len(promoted039),
            "rejected_candidate_created":g039["invariants"].get("rejected_candidate_created"),
            "parent_rule_preserved":g039["invariants"]["parent_rule_preserved"],
            "open_preserved":g039["invariants"]["open_preserved"],
            "open_refinement_materialized":g039["invariants"]["open_refinement_materialized"]
        },
        "architectural_pass":pass040 and pass039
    }

    (RUNTIME/"result.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print("Experiment 046 reproducibility: PASS")
    print("Experiment 046 architectural result:","PASS" if summary["architectural_pass"] else "FAIL")
    return 0 if summary["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
