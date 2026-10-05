# Meta-policy version application helpers.

def authorize_application(confirmation, candidate, current_id, new_id):
    confirmed = confirmation.get("status") in {"CONFIRMED", "META_POLICY_CONFIRMED"}
    proposed = candidate.get("status") in {"PROPOSED_NOT_APPLIED", "CONFIRMED_NOT_APPLIED"}
    distinct = bool(current_id) and bool(new_id) and current_id != new_id
    checks = {
        "confirmation_passed": confirmed,
        "candidate_not_applied": proposed,
        "version_ids_valid": distinct,
    }
    ok = all(checks.values())
    return {
        "authorized": ok,
        "checks": checks,
        "decision": "AUTHORIZE" if ok else "BLOCK",
        "current_id": current_id,
        "new_id": new_id,
    }

def materialize_version(gate, selector_definition, confirmation_ref):
    if not gate.get("authorized"):
        return {
            "status": "NOT_APPLIED",
            "objects": [],
            "relations": [],
            "history_mutated": False,
        }

    old_id = gate["current_id"]
    new_id = gate["new_id"]
    objects = [
        {"id": old_id, "type": "META_POLICY", "status": "SUPERSEDED"},
        {"id": new_id, "type": "META_POLICY", "status": "ACTIVE", "definition": selector_definition},
        {"id": confirmation_ref, "type": "META_POLICY_CONFIRMATION", "status": "FINAL"},
    ]
    relations = [
        {"subject": new_id, "predicate": "DERIVED_FROM_META_POLICY", "object": old_id},
        {"subject": old_id, "predicate": "SUPERSEDED_BY", "object": new_id},
        {"subject": new_id, "predicate": "SUPPORTED_BY", "object": confirmation_ref},
    ]
    return {
        "status": "APPLIED_AS_NEW_VERSION",
        "objects": objects,
        "relations": relations,
        "active_policy_id": new_id,
        "previous_policy_id": old_id,
        "history_mutated": False,
    }

def verify_materialization(result):
    if result.get("status") != "APPLIED_AS_NEW_VERSION":
        return {"all_pass": False}

    old_id = result["previous_policy_id"]
    new_id = result["active_policy_id"]
    objs = {o["id"]: o for o in result["objects"]}
    rels = result["relations"]
    checks = {
        "old_policy_preserved": old_id in objs,
        "new_policy_created": new_id in objs,
        "ids_distinct": old_id != new_id,
        "old_superseded": objs[old_id].get("status") == "SUPERSEDED",
        "new_active": objs[new_id].get("status") == "ACTIVE",
        "derived_from_link": any(r["subject"] == new_id and r["predicate"] == "DERIVED_FROM_META_POLICY" and r["object"] == old_id for r in rels),
        "superseded_by_link": any(r["subject"] == old_id and r["predicate"] == "SUPERSEDED_BY" and r["object"] == new_id for r in rels),
        "history_not_mutated": result.get("history_mutated") is False,
    }
    checks["all_pass"] = all(checks.values())
    return checks
