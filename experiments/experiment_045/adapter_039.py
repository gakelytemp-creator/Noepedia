#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
EXP=ROOT/"experiments"/"experiment_039"
RUNTIME=EXP/"_runtime"
RESULT=RUNTIME/"result.json"

def main():
    subprocess.run([sys.executable,str(EXP/"run_experiment.py")],check=True)
    r=json.loads(RESULT.read_text(encoding="utf-8"))
    c=r["confirmation"]
    case={
        "case_id":"EXP045_CASE_FROM_039",
        "candidate_id":"EXP039_SELECTED_TEMPORAL_CANDIDATE",
        "parent_rule_id":"EXP039_OLD_DIRECT_MAPPING",
        "open_id":"OPEN_EXP039_DOMAIN_VALIDITY",
        "confirmation_result_id":"EXP039_CONFIRMATION_RESULT",
        "preregistration_id":"EXP039_PREREGISTRATION",
        "parent_rule_exists":True,
        "open_exists":True,
        "provenance_complete":True,
        "candidate_parameters_explicit":True,
        "preregistration_frozen":True,
        "discovery_confirmation_separated":True,
        "confirmation_untouched":True,
        "evidence_role_explicit":True,
        "confirmation_evaluable":True,
        "unresolved_not_counted_as_success":True,
        "evaluator_frozen":True,
        "corrections_documented":True,
        "history_preserved":True,
        "open_refinement_prepared":True,
        "old_metric":c["old_mismatches"],
        "revised_metric":c["revised_mismatches"],
        "required_nulls":[
            {
                "name":"MAJORITY_STATE_NULL",
                "metric":c["majority_mismatches"],
                "required_relative_advantage":0.10
            },
            {
                "name":"PERMUTATION_NULL",
                "metric":c["permutation_median_mismatches"],
                "required_relative_advantage":0.10
            }
        ],
        "search_boundary_hit":r["discovery"]["lag_boundary_hit"],
        "search_boundary_policy":"REMAIN_OPEN",
        "direction_consistency_required":False
    }
    out=HERE/"_runtime"/"case_039.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(case,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(out)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
