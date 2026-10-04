#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import (
    LOW,HIGH,
    evaluate_orientation_candidate,
    evaluate_local_exception_candidate,
    evaluate_simpler_rule_comparator,
)

def main():
    src_d=[LOW,LOW,HIGH,HIGH,LOW,HIGH]
    tgt_d=[HIGH,HIGH,LOW,LOW,HIGH,LOW]
    src_c=[LOW,HIGH,HIGH,LOW]
    tgt_c=[HIGH,LOW,LOW,HIGH]
    orientation=evaluate_orientation_candidate(src_d,tgt_d,src_c,tgt_c)

    local_pass=evaluate_local_exception_candidate(
        [True,True,True,True],
        [True,True,True,False],
        replication_threshold=0.50
    )
    local_fail=evaluate_local_exception_candidate(
        [True,True,True,True],
        [True,False,False,False,False,False,False,False,False,False],
        replication_threshold=0.50
    )

    target_d=[HIGH,HIGH,HIGH,LOW,HIGH,HIGH]
    target_c=[HIGH,HIGH,HIGH,HIGH,LOW,HIGH]
    proposed=[LOW,HIGH,LOW,HIGH,LOW,HIGH]
    simpler=evaluate_simpler_rule_comparator(target_d,target_c,proposed)

    checks={
        "orientation_selected_inverted":
            orientation["frozen_parameters"]["orientation"]=="INVERTED",
        "orientation_confirmation_frozen_zero_error":
            orientation["confirmation"]["revised_mismatches"]==0,
        "orientation_majority_null_present":
            orientation["required_null_metrics"]["MAJORITY_STATE_NULL"] is not None,
        "local_pass_replicated":
            local_pass["confirmation"]["replicated"] is True,
        "local_fail_not_replicated":
            local_fail["confirmation"]["replicated"] is False,
        "local_pass_metric_better":
            local_pass["confirmation"]["revised_mismatches"] < local_pass["confirmation"]["old_mismatches"],
        "local_fail_transfer_null_blocks":
            local_fail["required_null_metrics"]["OUT_OF_CLUSTER_TRANSFER_TEST"]==0,
        "simpler_majority_selected_from_discovery":
            simpler["frozen_parameters"]["majority_state"]==HIGH,
        "simpler_proposed_does_not_beat_majority":
            simpler["confirmation"]["proposed_beats_majority"] is False,
        "simpler_null_metric_present":
            simpler["required_null_metrics"]["SIMPLER_RULE_NULL"] is not None,
    }

    out={
        "experiment":"NOEPEDIA_EXP_051_REMAINING_EVALUATOR_PLUGINS",
        "orientation":orientation,
        "local_pass":local_pass,
        "local_fail":local_fail,
        "simpler":simpler,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 051 reproducibility: PASS")
    print("Experiment 051 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
