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
