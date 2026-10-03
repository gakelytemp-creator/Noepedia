#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
EVALUATOR=ROOT/"experiments"/"experiment_003"/"evaluator.py"

def load_json(path):
    with path.open("r",encoding="utf-8") as f:
        return json.load(f)

def load_eval():
    spec=importlib.util.spec_from_file_location("noepedia_evaluator",EVALUATOR)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.evaluate

def main():
    actual=load_eval()(load_json(HERE/"INPUT.json"))
    expected=load_json(HERE/"EXPECTED_OUTPUT.json")
    errors=[]

    if actual.get("experiment")!=expected.get("experiment"):
        errors.append("experiment id differs")
    if actual.get("summary")!=expected.get("summary"):
        errors.append("summary differs: "+json.dumps(actual.get("summary"),sort_keys=True))

    actual_derived=sorted(
        [{"subject":r["subject"],"predicate":r["predicate"],"object":r["object"]}
         for r in actual.get("derived_relations",[])],
        key=lambda x:(x["subject"],x["predicate"],x["object"])
    )
    expected_derived=sorted(expected["derived_relations"],key=lambda x:(x["subject"],x["predicate"],x["object"]))
    if actual_derived!=expected_derived:
        errors.append("derived relation set differs")

    evidence=[]
    cards=[]
    for e in actual.get("events",[]):
        if e.get("event")=="CANDIDATE_SUPPORTED_BY_EVIDENCE":
            evidence.append({"event":e["event"],"subject":e["subject"],"candidate":e["candidate"],"evidence":sorted(e.get("evidence",[]))})
        elif e.get("event")=="CANDIDATE_REJECTED_BY_EVIDENCE":
            evidence.append({"event":e["event"],"subject":e["subject"],"candidate":e["candidate"],"observed":sorted(e.get("observed",[])),"candidate_features":sorted(e.get("candidate_features",[]))})
        elif e.get("event") in {"COMPETING_DERIVATIONS","UNIQUE_CANDIDATE"}:
            cards.append({"event":e["event"],"rule":e["rule"],"subject":e["subject"],"predicate":e["predicate"],"targets":sorted(e.get("targets",[]))})

    evkey=lambda x:(x["event"],x["subject"],x["candidate"])
    ckey=lambda x:(x["rule"],x["subject"],x["event"])
    if sorted(evidence,key=evkey)!=sorted(expected["evidence_outcomes"],key=evkey):
        errors.append("evidence outcomes differ")
    if sorted(cards,key=ckey)!=sorted(expected["cardinality_outcomes"],key=ckey):
        errors.append("cardinality outcomes differ")

    if actual.get("open_preserved")!=expected.get("open_preserved"):
        errors.append("OPEN preservation differs")
    if actual.get("open_records_unchanged")!=expected.get("open_records_unchanged"):
        errors.append("OPEN mutation flag differs")

    if errors:
        print("Experiment 010 verification: FAIL")
        for e in errors:
            print("- "+e)
        return 1

    print("Experiment 010 verification: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
