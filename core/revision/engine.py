#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path


MANDATORY_BOOLEAN_GATES = [
    ("A1_PARENT_RULE_EXISTS", "parent_rule_exists", "MISSING_PARENT_RULE", "REMAIN_OPEN"),
    ("A2_OPEN_EXISTS", "open_exists", "MISSING_OPEN_CONTEXT", "REMAIN_OPEN"),
    ("A3_PROVENANCE_COMPLETE", "provenance_complete", "PROMOTION_PATH_INCOMPLETE", "REMAIN_OPEN"),
    ("A4_PARAMETERS_EXPLICIT", "candidate_parameters_explicit", "HIDDEN_OR_UNRECORDED_PARAMETER", "REMAIN_OPEN"),
    ("A5_PREREGISTRATION_FROZEN", "preregistration_frozen", "PREREGISTRATION_INCOMPLETE", "REMAIN_OPEN"),
    ("B1_WINDOWS_SEPARATED", "discovery_confirmation_separated", "DISCOVERY_CONFIRMATION_LEAKAGE", "REJECT"),
    ("B2_CONFIRMATION_UNTOUCHED", "confirmation_untouched", "CONFIRMATION_NOT_UNTOUCHED", "REJECT"),
    ("B3_EVIDENCE_ROLE_EXPLICIT", "evidence_role_explicit", "EVIDENCE_ROLE_UNCLEAR", "REMAIN_OPEN"),
    ("C1_CONFIRMATION_EVALUABLE", "confirmation_evaluable", "NOT_EVALUABLE", "REMAIN_OPEN"),
    ("C6_UNRESOLVED_NOT_SUCCESS", "unresolved_not_counted_as_success", "UNRESOLVED_COUNTED_AS_SUCCESS", "REJECT"),
    ("D1_EVALUATOR_FROZEN", "evaluator_frozen", "EVALUATOR_INCOMPATIBLE", "REMAIN_OPEN"),
    ("D2_CORRECTIONS_DOCUMENTED", "corrections_documented", "UNDOCUMENTED_CORRECTION", "REMAIN_OPEN"),
    ("D3_HISTORY_PRESERVED", "history_preserved", "HISTORY_NOT_PRESERVED", "REMAIN_OPEN"),
    ("D4_OPEN_REFINEMENT_PREPARED", "open_refinement_prepared", "OPEN_REFINEMENT_UNSPECIFIED", "REMAIN_OPEN"),
]


def gate(gate_id, status, evidence=None, reason=None, failure_decision=None):
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence": evidence,
        "reason": reason,
        "failure_decision": failure_decision,
    }


def evaluate_case(case: dict) -> dict:
    gates=[]

    for gate_id,key,reason,decision in MANDATORY_BOOLEAN_GATES:
        val=case.get(key)
        if val is True:
            gates.append(gate(gate_id,"PASS",evidence={key:True}))
        elif val is False:
            gates.append(gate(gate_id,"FAIL",evidence={key:False},reason=reason,failure_decision=decision))
        else:
            gates.append(gate(gate_id,"NOT_EVALUABLE",evidence={key:val},reason=reason,failure_decision="REMAIN_OPEN"))

    # Scientific metric gate.
    old_metric=case.get("old_metric")
    revised_metric=case.get("revised_metric")
    if old_metric is None or revised_metric is None:
        gates.append(gate("C2_PRIMARY_METRIC_IMPROVES","NOT_EVALUABLE",
                          evidence={"old_metric":old_metric,"revised_metric":revised_metric},
                          reason="PRIMARY_METRIC_MISSING",failure_decision="REMAIN_OPEN"))
    elif revised_metric < old_metric:
        gates.append(gate("C2_PRIMARY_METRIC_IMPROVES","PASS",
                          evidence={"old_metric":old_metric,"revised_metric":revised_metric}))
    else:
        reason="DEGRADED_PERFORMANCE" if revised_metric>old_metric else "NO_PRIMARY_METRIC_IMPROVEMENT"
        gates.append(gate("C2_PRIMARY_METRIC_IMPROVES","FAIL",
                          evidence={"old_metric":old_metric,"revised_metric":revised_metric},
                          reason=reason,failure_decision="REJECT"))

    # Optional minimum effect gate.
    min_effect=case.get("minimum_relative_improvement")
    if min_effect is None:
        gates.append(gate("C3_MINIMUM_EFFECT","NOT_APPLICABLE"))
    elif old_metric in (None,0) or revised_metric is None:
        gates.append(gate("C3_MINIMUM_EFFECT","NOT_EVALUABLE",
                          reason="EFFECT_NOT_COMPUTABLE",failure_decision="REMAIN_OPEN"))
    else:
        rel=(old_metric-revised_metric)/old_metric
        if rel>=min_effect:
            gates.append(gate("C3_MINIMUM_EFFECT","PASS",
                              evidence={"relative_improvement":rel,"required":min_effect}))
        else:
            gates.append(gate("C3_MINIMUM_EFFECT","FAIL",
                              evidence={"relative_improvement":rel,"required":min_effect},
                              reason="EFFECT_TOO_SMALL",failure_decision="REJECT"))

    # Null gates.
    required_nulls=case.get("required_nulls",[])
    if not required_nulls:
        gates.append(gate("C4_REQUIRED_NULLS","NOT_APPLICABLE"))
    else:
        for idx,n in enumerate(required_nulls,1):
            metric=n.get("metric")
            required_advantage=n.get("required_relative_advantage",0.0)
            name=n.get("name",f"NULL_{idx}")
            if metric is None or revised_metric is None:
                gates.append(gate(f"C4_NULL_{idx}_{name}","NOT_EVALUABLE",
                                  evidence=n,reason="REQUIRED_NULL_UNAVAILABLE",
                                  failure_decision="REMAIN_OPEN"))
                continue
            if metric==0:
                gates.append(gate(f"C4_NULL_{idx}_{name}","FAIL",
                                  evidence={"null_metric":metric,"revised_metric":revised_metric,
                                            "relative_advantage":None,"required":required_advantage},
                                  reason="NULL_NOT_BEATEN",failure_decision="REJECT"))
                continue
            rel=(metric-revised_metric)/metric
            if rel>=required_advantage:
                gates.append(gate(f"C4_NULL_{idx}_{name}","PASS",
                                  evidence={"null_metric":metric,"revised_metric":revised_metric,
                                            "relative_advantage":rel,"required":required_advantage}))
            else:
                gates.append(gate(f"C4_NULL_{idx}_{name}","FAIL",
                                  evidence={"null_metric":metric,"revised_metric":revised_metric,
                                            "relative_advantage":rel,"required":required_advantage},
                                  reason="NULL_NOT_BEATEN",failure_decision="REJECT"))

    # Search boundary.
    boundary_policy=case.get("search_boundary_policy","REMAIN_OPEN")
    boundary_hit=case.get("search_boundary_hit")
    if boundary_hit is None:
        gates.append(gate("C5_SEARCH_BOUNDARY","NOT_APPLICABLE"))
    elif boundary_hit:
        gates.append(gate("C5_SEARCH_BOUNDARY","FAIL",
                          evidence={"search_boundary_hit":True},
                          reason="SEARCH_BOUNDARY_UNRESOLVED",
                          failure_decision=boundary_policy))
    else:
        gates.append(gate("C5_SEARCH_BOUNDARY","PASS",
                          evidence={"search_boundary_hit":False}))

    # Direction consistency.
    direction_required=case.get("direction_consistency_required",False)
    if not direction_required:
        gates.append(gate("C7_DIRECTION_CONSISTENCY","NOT_APPLICABLE"))
    else:
        ok=case.get("direction_consistent")
        if ok is True:
            gates.append(gate("C7_DIRECTION_CONSISTENCY","PASS"))
        elif ok is False:
            gates.append(gate("C7_DIRECTION_CONSISTENCY","FAIL",
                              reason="DIRECTION_REVERSED",failure_decision="REJECT"))
        else:
            gates.append(gate("C7_DIRECTION_CONSISTENCY","NOT_EVALUABLE",
                              reason="DIRECTION_RESULT_MISSING",failure_decision="REMAIN_OPEN"))

    # Simpler-rule comparator.
    simpler=case.get("simpler_rule_metric")
    if simpler is None:
        gates.append(gate("C8_SIMPLER_RULE","NOT_APPLICABLE"))
    elif revised_metric is None:
        gates.append(gate("C8_SIMPLER_RULE","NOT_EVALUABLE",
                          reason="SIMPLER_RULE_COMPARISON_UNAVAILABLE",failure_decision="REMAIN_OPEN"))
    elif revised_metric < simpler:
        gates.append(gate("C8_SIMPLER_RULE","PASS",
                          evidence={"simpler_rule_metric":simpler,"revised_metric":revised_metric}))
    else:
        gates.append(gate("C8_SIMPLER_RULE","FAIL",
                          evidence={"simpler_rule_metric":simpler,"revised_metric":revised_metric},
                          reason="SIMPLER_RULE_NOT_BEATEN",failure_decision="REJECT"))

    # Decision precedence: structural/evaluability -> REMAIN_OPEN, then scientific reject, else promote.
    remain_open_failures=[
        g for g in gates
        if g.get("status") in {"FAIL","NOT_EVALUABLE"} and g.get("failure_decision")=="REMAIN_OPEN"
    ]
    reject_failures=[
        g for g in gates
        if g.get("status")=="FAIL" and g.get("failure_decision")=="REJECT"
    ]

    if remain_open_failures:
        decision="REMAIN_OPEN"
        reason=remain_open_failures[0].get("reason")
    elif reject_failures:
        decision="REJECT"
        reason=reject_failures[0].get("reason")
    else:
        decision="PROMOTE"
        reason="ALL_MANDATORY_PROMOTION_GATES_PASSED"

    out={
        "record_type":"PROMOTION_GATE_AUDIT",
        "case_id":case.get("case_id"),
        "candidate_id":case.get("candidate_id"),
        "parent_rule_id":case.get("parent_rule_id"),
        "open_id":case.get("open_id"),
        "gates":gates,
        "final_decision":decision,
        "decision_reason":reason,
        "history_mutated":False,
    }

    if decision=="PROMOTE":
        out["proposed_new_rule_record"]={
            "id":case.get("proposed_new_rule_id") or f"{case.get('candidate_id','CANDIDATE')}::PROMOTED_RULE",
            "type":"RULE",
            "epistemic_status":"EMPIRICALLY_SUPPORTED_RULE",
            "derived_from_rule":case.get("parent_rule_id"),
            "promoted_from":case.get("candidate_id"),
            "supported_by_confirmation":case.get("confirmation_result_id"),
            "preregistered_by":case.get("preregistration_id"),
        }
    elif decision=="REJECT":
        out["rejected_candidate_record"]={
            "id":f"{case.get('candidate_id','CANDIDATE')}::REJECTED",
            "type":"REJECTED_CANDIDATE",
            "rejected_from":case.get("candidate_id"),
            "failed_on":case.get("confirmation_result_id"),
            "rejection_reason":reason,
            "addresses_open":case.get("open_id"),
        }

    return out


def main(argv):
    if len(argv) not in (2,3):
        print("Usage: revision_harness.py CASE.json [AUDIT.json]",file=sys.stderr)
        return 2
    case=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    audit=evaluate_case(case)
    rendered=json.dumps(audit,indent=2,ensure_ascii=False)+"\n"
    print(rendered,end="")
    if len(argv)==3:
        Path(argv[2]).write_text(rendered,encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
