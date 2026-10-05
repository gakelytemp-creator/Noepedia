# Meta-policy regression watch and versioned rollback helpers.

def summarize_outcomes(records):
    n=len(records)
    if n==0:
        return {"sample_count":0,"promotion_rate":None,"remain_open_rate":None,"graph_valid_rate":None}
    promotes=sum(r.get("decision")=="PROMOTE" for r in records)
    opens=sum(r.get("decision")=="REMAIN_OPEN" for r in records)
    valid=sum(bool(r.get("graph_valid",True)) for r in records)
    return {
        "sample_count":n,
        "promotion_rate":promotes/n,
        "remain_open_rate":opens/n,
        "graph_valid_rate":valid/n
    }

def watch_regression(baseline_records, active_records, minimum_samples=5, max_promotion_drop=0.20, max_open_increase=0.20, minimum_graph_valid_rate=1.0):
    baseline=summarize_outcomes(baseline_records)
    active=summarize_outcomes(active_records)

    if active["sample_count"]<minimum_samples:
        status="NOT_EVALUABLE"
        reason="MINIMUM_SAMPLE_GATE_NOT_MET"
    elif active["graph_valid_rate"]<minimum_graph_valid_rate:
        status="REGRESSION_CONFIRMED"
        reason="GRAPH_VALIDITY_REGRESSION"
    else:
        promotion_drop=baseline["promotion_rate"]-active["promotion_rate"]
        open_increase=active["remain_open_rate"]-baseline["remain_open_rate"]
        if promotion_drop>=max_promotion_drop or open_increase>=max_open_increase:
            status="REGRESSION_CONFIRMED"
            reason="OUTCOME_DEGRADATION_GATE_PASSED"
        else:
            status="NO_REGRESSION"
            reason="WITHIN_REGRESSION_GATES"

    return {
        "record_type":"META_POLICY_REGRESSION_WATCH",
        "status":status,
        "reason":reason,
        "baseline":baseline,
        "active":active,
        "gates":{
            "minimum_samples":minimum_samples,
            "max_promotion_drop":max_promotion_drop,
            "max_open_increase":max_open_increase,
            "minimum_graph_valid_rate":minimum_graph_valid_rate
        },
        "live_policy_mutated":False
    }

def authorize_rollback(watch_result, active_policy_id, restore_policy_id, new_policy_id):
    confirmed=watch_result.get("status")=="REGRESSION_CONFIRMED"
    ids_ok=bool(active_policy_id) and bool(restore_policy_id) and bool(new_policy_id)
    distinct=len({active_policy_id,restore_policy_id,new_policy_id})==3 if ids_ok else False
    checks={"regression_confirmed":confirmed,"version_ids_valid":distinct}
    ok=all(checks.values())
    return {
        "authorized":ok,
        "checks":checks,
        "decision":"AUTHORIZE_ROLLBACK" if ok else "BLOCK_ROLLBACK",
        "active_policy_id":active_policy_id,
        "restore_policy_id":restore_policy_id,
        "new_policy_id":new_policy_id
    }

def materialize_rollback(gate, restored_definition, watch_ref):
    if not gate.get("authorized"):
        return {"status":"NOT_APPLIED","objects":[],"relations":[],"history_mutated":False}

    active=gate["active_policy_id"]
    restore=gate["restore_policy_id"]
    new=gate["new_policy_id"]
    objects=[
        {"id":active,"type":"META_POLICY","status":"SUPERSEDED"},
        {"id":restore,"type":"META_POLICY","status":"HISTORICAL_SOURCE"},
        {"id":new,"type":"META_POLICY","status":"ACTIVE","definition":restored_definition},
        {"id":watch_ref,"type":"META_POLICY_REGRESSION_WATCH","status":"FINAL"}
    ]
    relations=[
        {"subject":new,"predicate":"DERIVED_FROM_META_POLICY","object":active},
        {"subject":new,"predicate":"RESTORES_DEFINITION_FROM","object":restore},
        {"subject":active,"predicate":"SUPERSEDED_BY","object":new},
        {"subject":new,"predicate":"SUPPORTED_BY","object":watch_ref}
    ]
    return {
        "status":"ROLLBACK_APPLIED_AS_NEW_VERSION",
        "active_policy_id":new,
        "previous_active_policy_id":active,
        "restored_from_policy_id":restore,
        "objects":objects,
        "relations":relations,
        "history_mutated":False
    }

def verify_rollback(result):
    if result.get("status")!="ROLLBACK_APPLIED_AS_NEW_VERSION":
        return {"all_pass":False}
    active=result["active_policy_id"]
    previous=result["previous_active_policy_id"]
    source=result["restored_from_policy_id"]
    objs={o["id"]:o for o in result["objects"]}
    rels=result["relations"]
    checks={
        "new_active_created":active in objs and objs[active].get("status")=="ACTIVE",
        "previous_preserved":previous in objs,
        "restore_source_preserved":source in objs,
        "ids_distinct":len({active,previous,source})==3,
        "restore_link":any(r["subject"]==active and r["predicate"]=="RESTORES_DEFINITION_FROM" and r["object"]==source for r in rels),
        "superseded_link":any(r["subject"]==previous and r["predicate"]=="SUPERSEDED_BY" and r["object"]==active for r in rels),
        "history_not_mutated":result.get("history_mutated") is False
    }
    checks["all_pass"]=all(checks.values())
    return checks
