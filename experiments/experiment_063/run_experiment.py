#!/usr/bin/env python3
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.meta_regression import watch_regression, authorize_rollback, materialize_rollback, verify_rollback

def make(decisions):
    return [{"decision":d,"graph_valid":True} for d in decisions]

def main():
    baseline=make(["PROMOTE","PROMOTE","PROMOTE","REJECT","PROMOTE","REMAIN_OPEN"])
    regressed=make(["REMAIN_OPEN","REMAIN_OPEN","REJECT","REMAIN_OPEN","PROMOTE","REMAIN_OPEN"])
    stable=make(["PROMOTE","PROMOTE","REJECT","PROMOTE","REMAIN_OPEN","PROMOTE"])
    small=make(["REMAIN_OPEN","PROMOTE"])

    w_bad=watch_regression(baseline,regressed,minimum_samples=5,max_promotion_drop=0.20,max_open_increase=0.20)
    gate=authorize_rollback(w_bad,"META_POLICY_V2","META_POLICY_V1","META_POLICY_V3")
    rb=materialize_rollback(gate,{"small_history_strategy":"CONSERVATIVE"},"EXP063_REGRESSION")
    vr=verify_rollback(rb)

    w_good=watch_regression(baseline,stable,minimum_samples=5,max_promotion_drop=0.20,max_open_increase=0.20)
    blocked=authorize_rollback(w_good,"META_POLICY_V2","META_POLICY_V1","META_POLICY_V3")

    w_small=watch_regression(baseline,small,minimum_samples=5,max_promotion_drop=0.20,max_open_increase=0.20)

    checks={
      "regression_confirmed":w_bad["status"]=="REGRESSION_CONFIRMED",
      "rollback_authorized":gate["authorized"] is True,
      "rollback_new_version":rb["status"]=="ROLLBACK_APPLIED_AS_NEW_VERSION" and rb["active_policy_id"]=="META_POLICY_V3",
      "rollback_graph_valid":vr["all_pass"] is True,
      "old_versions_preserved":vr["previous_preserved"] is True and vr["restore_source_preserved"] is True,
      "stable_no_regression":w_good["status"]=="NO_REGRESSION",
      "stable_rollback_blocked":blocked["authorized"] is False,
      "small_not_evaluable":w_small["status"]=="NOT_EVALUABLE"
    }
    out={"experiment":"NOEPEDIA_EXP_063_REGRESSION_ROLLBACK","regression":w_bad,"rollback":rb,"stable":w_good,"small":w_small,"checks":checks,"architectural_pass":all(checks.values())}
    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
