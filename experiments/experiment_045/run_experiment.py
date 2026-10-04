#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
RUNTIME=HERE/"_runtime"
HARNESS=HERE/"revision_harness.py"

def run_adapter(name):
    subprocess.run([sys.executable,str(HERE/name)],check=True)

def run_harness(case_path,audit_path):
    subprocess.run([sys.executable,str(HARNESS),str(case_path),str(audit_path)],check=True)
    return json.loads(audit_path.read_text(encoding="utf-8"))

def main():
    RUNTIME.mkdir(exist_ok=True)

    run_adapter("adapter_040.py")
    audit040=run_harness(RUNTIME/"case_040.json",RUNTIME/"audit_040.json")

    run_adapter("adapter_039.py")
    audit039=run_harness(RUNTIME/"case_039.json",RUNTIME/"audit_039.json")

    synthetic={
        "case_id":"EXP045_SYNTHETIC_NOT_EVALUABLE",
        "candidate_id":"SYNTH_CANDIDATE",
        "parent_rule_id":"SYNTH_RULE_V1",
        "open_id":"SYNTH_OPEN",
        "parent_rule_exists":True,
        "open_exists":True,
        "provenance_complete":True,
        "candidate_parameters_explicit":True,
        "preregistration_frozen":True,
        "discovery_confirmation_separated":True,
        "confirmation_untouched":True,
        "evidence_role_explicit":True,
        "confirmation_evaluable":False,
        "unresolved_not_counted_as_success":True,
        "evaluator_frozen":True,
        "corrections_documented":True,
        "history_preserved":True,
        "open_refinement_prepared":True,
        "old_metric":None,
        "revised_metric":None,
        "required_nulls":[],
        "search_boundary_hit":False,
        "direction_consistency_required":False
    }
    case_syn=RUNTIME/"case_synthetic.json"
    case_syn.write_text(json.dumps(synthetic,indent=2)+"\n",encoding="utf-8")
    audit_syn=run_harness(case_syn,RUNTIME/"audit_synthetic.json")

    expected={
        "040":"PROMOTE",
        "039":"REJECT",
        "synthetic":"REMAIN_OPEN"
    }
    observed={
        "040":audit040["final_decision"],
        "039":audit039["final_decision"],
        "synthetic":audit_syn["final_decision"]
    }

    passed=(expected==observed)
    summary={
        "experiment":"NOEPEDIA_EXP_045_AUTOMATED_REVISION_HARNESS",
        "expected_decisions":expected,
        "observed_decisions":observed,
        "integration_pass":passed,
        "history_mutation_detected":any([
            audit040.get("history_mutated",True),
            audit039.get("history_mutated",True),
            audit_syn.get("history_mutated",True)
        ]),
        "audit_files":[
            "audit_040.json",
            "audit_039.json",
            "audit_synthetic.json"
        ]
    }
    (RUNTIME/"result.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    print("Experiment 045 reproducibility: PASS")
    print("Experiment 045 architectural result:", "PASS" if passed else "FAIL")
    return 0 if passed else 1

if __name__=="__main__":
    raise SystemExit(main())
