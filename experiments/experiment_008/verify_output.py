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

def sig(e):
    dr=e.get("derived_relation") or {}
    req=e.get("derived_requirement") or {}
    return {
        "event":e.get("event"),
        "rule":e.get("rule"),
        "subject":e.get("subject"),
        "derived_predicate":dr.get("predicate"),
        "derived_target":dr.get("target"),
        "expected_target":req.get("target"),
        "conflicting_relation":e.get("conflicting_relation"),
        "stored_target":e.get("stored_target"),
        "satisfying_relations":e.get("satisfying_relations"),
    }

def esig(e):
    return {
        "event":e.get("event"),
        "rule":e.get("rule"),
        "subject":e.get("subject"),
        "derived_predicate":e.get("derived_predicate"),
        "derived_target":e.get("derived_target"),
        "expected_target":e.get("expected_target"),
        "conflicting_relation":e.get("conflicting_relation"),
        "stored_target":e.get("stored_target"),
        "satisfying_relations":e.get("satisfying_relations"),
    }

def key(x):
    return (str(x["event"]),str(x["rule"]),str(x["subject"]),str(x["derived_predicate"]))

def main():
    actual=load_eval()(load_json(HERE/"INPUT.json"))
    expected=load_json(HERE/"EXPECTED_OUTPUT.json")
    errors=[]

    if actual.get("experiment")!=expected.get("experiment"):
        errors.append("experiment id differs")
    if actual.get("summary")!=expected.get("summary"):
        errors.append("summary differs: "+json.dumps(actual.get("summary"),sort_keys=True))

    ad=sorted(
        [{"subject":r["subject"],"predicate":r["predicate"],"object":r["object"]}
         for r in actual.get("derived_relations",[])],
        key=lambda x:(x["subject"],x["predicate"],x["object"])
    )
    ed=sorted(expected.get("derived_relations",[]),
        key=lambda x:(x["subject"],x["predicate"],x["object"]))
    if ad!=ed:
        errors.append("derived relation set differs")

    a=sorted((sig(e) for e in actual.get("events",[])),key=key)
    b=sorted((esig(e) for e in expected.get("required_events",[])),key=key)
    if a!=b:
        errors.append("event set differs\nACTUAL:\n"+json.dumps(a,indent=2)+"\nEXPECTED:\n"+json.dumps(b,indent=2))

    if actual.get("open_preserved")!=expected.get("open_preserved"):
        errors.append("OPEN preservation differs")
    if actual.get("open_records_unchanged")!=expected.get("open_records_unchanged"):
        errors.append("OPEN mutation flag differs")

    if errors:
        print("Experiment 008 verification: FAIL")
        for e in errors:
            print("- "+e)
        return 1

    print("Experiment 008 verification: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
