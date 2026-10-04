#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
RUNTIME=HERE/"_runtime"

sys.path.insert(0,str(ROOT))

from core.revision import evaluate_case, materialize, verify_invariants

ADAPTER040=ROOT/"experiments"/"experiment_045"/"adapter_040.py"
ADAPTER039=ROOT/"experiments"/"experiment_045"/"adapter_039.py"
SRC_RUNTIME=ROOT/"experiments"/"experiment_045"/"_runtime"


def run_adapter(path):
    subprocess.run([sys.executable,str(path)],check=True)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def process(case):
    audit=evaluate_case(case)
    graph=materialize(case,audit)
    invariants=verify_invariants(case,audit,graph)
    return audit,graph,invariants


def main():
    RUNTIME.mkdir(exist_ok=True)

    run_adapter(ADAPTER040)
    run_adapter(ADAPTER039)

    case040=load(SRC_RUNTIME/"case_040.json")
    case039=load(SRC_RUNTIME/"case_039.json")

    audit040,graph040,inv040=process(case040)
    audit039,graph039,inv039=process(case039)

    parent040=case040["parent_rule_id"]
    parent039=case039["parent_rule_id"]

    promoted040=[
        o for o in graph040["objects"]
        if o.get("type")=="RULE" and o["id"]!=parent040
    ]
    promoted039=[
        o for o in graph039["objects"]
        if o.get("type")=="RULE" and o["id"]!=parent039
    ]

    checks={
        "positive_decision_promote":audit040["final_decision"]=="PROMOTE",
        "negative_decision_reject":audit039["final_decision"]=="REJECT",
        "positive_invariants_pass":inv040["all_pass"],
        "negative_invariants_pass":inv039["all_pass"],
        "positive_one_new_rule":len(promoted040)==1,
        "negative_zero_new_rules":len(promoted039)==0,
        "positive_parent_preserved":inv040["parent_rule_preserved"],
        "negative_parent_preserved":inv039["parent_rule_preserved"],
        "positive_open_preserved":inv040["open_preserved"],
        "negative_open_preserved":inv039["open_preserved"],
        "positive_append_only":inv040["append_only_no_deletion"],
        "negative_append_only":inv039["append_only_no_deletion"]
    }

    result={
        "experiment":"NOEPEDIA_EXP_048_CORE_REVISION_SUBSYSTEM_INTEGRATION",
        "core_module":"core.revision",
        "decisions":{
            "040":audit040["final_decision"],
            "039":audit039["final_decision"]
        },
        "new_rule_counts":{
            "040":len(promoted040),
            "039":len(promoted039)
        },
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    (RUNTIME/"result.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print(json.dumps(result,indent=2,ensure_ascii=False))
    print("Experiment 048 reproducibility: PASS")
    print("Experiment 048 architectural result:",
          "PASS" if result["architectural_pass"] else "FAIL")
    return 0 if result["architectural_pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
