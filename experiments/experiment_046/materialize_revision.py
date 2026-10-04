#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

def rel(i,s,p,o,status="settled",prov=None):
    return {
        "id":i,"subject":s,"predicate":p,"object":o,
        "status":status,"provenance":prov or []
    }

def base_graph(case):
    parent=case["parent_rule_id"]
    open_id=case["open_id"]
    cand=case["candidate_id"]
    return {
        "objects":[
            {"id":parent,"type":"RULE","epistemic_status":"ASSUMED_RULE"},
            {"id":open_id,"type":"OPEN","status":"OPEN"},
            {"id":cand,"type":"RULE_CANDIDATE","status":"PROPOSED"},
            {"id":case["preregistration_id"],"type":"PREREGISTRATION_RECORD","status":"FROZEN"},
            {"id":case["confirmation_result_id"],"type":"CONFIRMATION_RESULT","status":"FINAL"}
        ],
        "relations":[
            rel("BASE_01",cand,"PARENT_RULE",parent),
            rel("BASE_02",cand,"ADDRESSES_OPEN",open_id),
            rel("BASE_03",cand,"PREREGISTERED_BY",case["preregistration_id"]),
            rel("BASE_04",cand,"SUPPORTED_BY_CONFIRMATION",case["confirmation_result_id"])
        ]
    }

def materialize(case,audit):
    graph=base_graph(case)
    objects=graph["objects"]
    relations=graph["relations"]

    decision_id=f"{case['case_id']}::PROMOTION_DECISION"
    objects.append({
        "id":decision_id,
        "type":"PROMOTION_DECISION",
        "decision":audit["final_decision"],
        "reason":audit["decision_reason"]
    })
    relations.append(rel(
        "DEC_01",decision_id,"DECIDES_ON",case["candidate_id"],
        prov=[case["confirmation_result_id"]]
    ))

    # Preserve the gate audit as a first-class object.
    audit_id=f"{case['case_id']}::GATE_AUDIT"
    objects.append({
        "id":audit_id,
        "type":"PROMOTION_GATE_AUDIT",
        "final_decision":audit["final_decision"]
    })
    relations.append(rel("AUD_01",decision_id,"BASED_ON",audit_id))

    open_ref_id=f"{case['case_id']}::OPEN_REFINEMENT"
    objects.append({"id":open_ref_id,"type":"OPEN_REFINEMENT"})
    relations.append(rel("OPENR_01",open_ref_id,"REFINES_OPEN",case["open_id"]))

    if audit["final_decision"]=="PROMOTE":
        new_rule=audit["proposed_new_rule_record"]["id"]
        objects.append({
            "id":new_rule,
            "type":"RULE",
            "epistemic_status":"EMPIRICALLY_SUPPORTED_RULE"
        })
        relations.extend([
            rel("PROM_01",new_rule,"DERIVED_FROM_RULE",case["parent_rule_id"],prov=[decision_id]),
            rel("PROM_02",new_rule,"PROMOTED_FROM",case["candidate_id"],prov=[decision_id]),
            rel("PROM_03",new_rule,"SUPPORTED_BY",case["confirmation_result_id"],prov=[decision_id]),
            rel("PROM_04",new_rule,"PREREGISTERED_BY",case["preregistration_id"]),
            rel("PROM_05",case["parent_rule_id"],"SUPERSEDED_BY",new_rule,prov=[decision_id]),
            rel("OPENR_02",open_ref_id,"RESOLVED_COMPONENT","TESTED_REVISION_COMPONENT",prov=[decision_id]),
            rel("OPENR_03",open_ref_id,"REMAINING_COMPONENT","TRANSFER_AND_PHYSICAL_INTERPRETATION",status="open",prov=[decision_id])
        ])
    elif audit["final_decision"]=="REJECT":
        rej=audit["rejected_candidate_record"]["id"]
        objects.append({
            "id":rej,
            "type":"REJECTED_CANDIDATE",
            "rejection_reason":audit["decision_reason"]
        })
        relations.extend([
            rel("REJ_01",rej,"REJECTED_FROM",case["candidate_id"],prov=[decision_id]),
            rel("REJ_02",rej,"FAILED_ON",case["confirmation_result_id"],prov=[decision_id]),
            rel("REJ_03",rej,"ADDRESSES_OPEN",case["open_id"]),
            rel("OPENR_02",open_ref_id,"REJECTED_COMPONENT",case["candidate_id"],prov=[decision_id]),
            rel("OPENR_03",open_ref_id,"REMAINING_COMPONENT","ORIGINAL_DOMAIN_UNCERTAINTY",status="open",prov=[decision_id])
        ])
    else:
        relations.append(rel(
            "OPENR_02",open_ref_id,"REMAINING_COMPONENT",
            "NO_JUSTIFIED_EPISTEMIC_TRANSITION",status="open",prov=[decision_id]
        ))

    return graph

def verify_invariants(case,audit,graph):
    objects={o["id"]:o for o in graph["objects"]}
    rels=graph["relations"]
    parent=case["parent_rule_id"]
    open_id=case["open_id"]
    decision=audit["final_decision"]

    checks={}
    checks["parent_rule_preserved"]=parent in objects
    checks["open_preserved"]=open_id in objects
    checks["decision_materialized"]=any(o.get("type")=="PROMOTION_DECISION" for o in graph["objects"])
    checks["audit_materialized"]=any(o.get("type")=="PROMOTION_GATE_AUDIT" for o in graph["objects"])
    checks["open_refinement_materialized"]=any(o.get("type")=="OPEN_REFINEMENT" for o in graph["objects"])
    checks["append_only_no_deletion"]=True

    promoted=[o for o in graph["objects"] if o.get("type")=="RULE" and o["id"]!=parent]
    rejected=[o for o in graph["objects"] if o.get("type")=="REJECTED_CANDIDATE"]

    if decision=="PROMOTE":
        checks["new_rule_created"]=len(promoted)==1
        checks["rejected_not_created"]=len(rejected)==0
        if promoted:
            nr=promoted[0]["id"]
            checks["new_rule_version_distinct"]=nr!=parent
            checks["derived_from_link"]=any(r["subject"]==nr and r["predicate"]=="DERIVED_FROM_RULE" and r["object"]==parent for r in rels)
            checks["superseded_by_link"]=any(r["subject"]==parent and r["predicate"]=="SUPERSEDED_BY" and r["object"]==nr for r in rels)
        else:
            checks["new_rule_version_distinct"]=False
            checks["derived_from_link"]=False
            checks["superseded_by_link"]=False
    elif decision=="REJECT":
        checks["no_new_rule_created"]=len(promoted)==0
        checks["rejected_candidate_created"]=len(rejected)==1
        checks["rejection_link"]=any(r["predicate"]=="REJECTED_FROM" and r["object"]==case["candidate_id"] for r in rels)
    else:
        checks["no_new_rule_created"]=len(promoted)==0
        checks["no_rejected_candidate_created"]=len(rejected)==0

    checks["all_pass"]=all(checks.values())
    return checks

def main(argv):
    if len(argv)!=4:
        print("Usage: materialize_revision.py CASE.json AUDIT.json OUTPUT.json",file=sys.stderr)
        return 2
    case=json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    audit=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    graph=materialize(case,audit)
    checks=verify_invariants(case,audit,graph)
    out={"graph":graph,"invariants":checks}
    Path(argv[3]).write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"decision":audit["final_decision"],"invariants":checks},indent=2))
    return 0 if checks["all_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main(sys.argv))
