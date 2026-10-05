#!/usr/bin/env python3
import json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.meta_application import authorize_application, materialize_version, verify_materialization

def main():
    confirmed={"status":"CONFIRMED"}
    candidate={"status":"CONFIRMED_NOT_APPLIED"}

    gate=authorize_application(
        confirmed,candidate,
        "META_POLICY_V1","META_POLICY_V2"
    )
    applied=materialize_version(
        gate,
        {"small_history_strategy":"SPARSE"},
        "EXP061_CONFIRMATION"
    )
    checks_ok=verify_materialization(applied)

    blocked_gate=authorize_application(
        {"status":"REJECTED"},
        {"status":"PROPOSED_NOT_APPLIED"},
        "META_POLICY_V1","META_POLICY_V2"
    )
    blocked=materialize_version(
        blocked_gate,
        {"small_history_strategy":"SPARSE"},
        "EXP061_FAILED_CONFIRMATION"
    )

    checks={
        "confirmed_authorized":gate["authorized"] is True,
        "confirmed_applied_as_new_version":applied["status"]=="APPLIED_AS_NEW_VERSION",
        "confirmed_graph_valid":checks_ok["all_pass"] is True,
        "old_policy_preserved":checks_ok["old_policy_preserved"] is True,
        "new_policy_active":checks_ok["new_active"] is True,
        "history_not_mutated":checks_ok["history_not_mutated"] is True,
        "unconfirmed_blocked":blocked_gate["authorized"] is False,
        "blocked_not_applied":blocked["status"]=="NOT_APPLIED",
        "blocked_no_objects":blocked["objects"]==[]
    }

    out={
        "experiment":"NOEPEDIA_EXP_062_META_POLICY_APPLICATION_GATE",
        "confirmed":{"gate":gate,"materialization":applied,"verification":checks_ok},
        "blocked":{"gate":blocked_gate,"materialization":blocked},
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
