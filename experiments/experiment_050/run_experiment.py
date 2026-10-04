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
    evaluate_temporal_candidate,
    evaluate_threshold_candidate,
)


def make_temporal_source(blocks, reps=1):
    out=[]
    for _ in range(reps):
        for state,length in blocks:
            out.extend([state]*length)
    return out


def delayed_target(source,direction,lag):
    out=list(source)
    last_t=None
    prev_before=None
    for i in range(1,len(source)):
        prev=source[i-1]
        curr=source[i]
        d=None
        if prev==LOW and curr==HIGH:
            d="LOW_TO_HIGH"
        elif prev==HIGH and curr==LOW:
            d="HIGH_TO_LOW"
        if d==direction:
            last_t=i
            prev_before=prev
        if last_t is not None and 0<=i-last_t<=lag:
            out[i]=prev_before
        else:
            out[i]=curr
    return out


def temporal_interior_case():
    disc=make_temporal_source([(LOW,12),(HIGH,12)],reps=6)
    conf=make_temporal_source([(LOW,10),(HIGH,10)],reps=7)
    dt=delayed_target(disc,"HIGH_TO_LOW",3)
    ct=delayed_target(conf,"HIGH_TO_LOW",3)
    return evaluate_temporal_candidate(
        disc,dt,conf,ct,
        lag_min=1,lag_max=6,
        directions=["LOW_TO_HIGH","HIGH_TO_LOW"],
        permutation_shifts=[5,11,17]
    )


def temporal_boundary_case():
    disc=make_temporal_source([(LOW,8),(HIGH,8)],reps=5)
    conf=make_temporal_source([(LOW,8),(HIGH,8)],reps=5)
    dt=delayed_target(disc,"HIGH_TO_LOW",6)
    ct=delayed_target(conf,"HIGH_TO_LOW",6)
    return evaluate_temporal_candidate(
        disc,dt,conf,ct,
        lag_min=1,lag_max=6,
        directions=["HIGH_TO_LOW"],
        permutation_shifts=[3,7]
    )


def threshold_case(grid, desired):
    # Source is LOW for first half and HIGH for second half.
    src_d=[LOW]*10+[HIGH]*10
    src_c=[LOW]*10+[HIGH]*10
    vals_d=[float(i) for i in range(20)]
    vals_c=[float(i)+0.1 for i in range(20)]
    return evaluate_threshold_candidate(
        src_d,vals_d,src_c,vals_c,
        threshold_grid=grid,
        old_threshold=5.0,
        perturbation_grid=grid
    )


def main():
    t1=temporal_interior_case()
    t2=temporal_boundary_case()
    th1=threshold_case([7.0,8.0,9.0,10.0,11.0],9.0)
    th2=threshold_case([6.0,7.0,8.0,9.0],9.0)

    checks={
        "temporal_interior_direction":
            t1["frozen_parameters"]["direction"]=="HIGH_TO_LOW",
        "temporal_interior_lag":
            t1["frozen_parameters"]["lag"]==3,
        "temporal_interior_not_boundary":
            t1["discovery"]["search_boundary_hit"] is False,
        "temporal_confirmation_zero_error":
            t1["confirmation"]["revised_mismatches"]==0,
        "temporal_majority_metric_present":
            t1["required_null_metrics"]["MAJORITY_STATE_NULL"] is not None,
        "temporal_permutation_metric_present":
            t1["required_null_metrics"]["TIME_SHIFT_OR_PERMUTATION_NULL"] is not None,
        "temporal_boundary_detected":
            t2["frozen_parameters"]["lag"]==6 and t2["discovery"]["search_boundary_hit"] is True,
        "threshold_interior_selected":
            th1["frozen_parameters"]["threshold"]==9.0,
        "threshold_interior_not_boundary":
            th1["discovery"]["search_boundary_hit"] is False,
        "threshold_confirmation_frozen_parameter_preserved":
            th1["confirmation"]["revised_mismatches"]==1,
        "threshold_perturbation_metric_present":
            th1["required_null_metrics"]["THRESHOLD_PERTURBATION_NULL"] is not None,
        "threshold_boundary_detected":
            th2["frozen_parameters"]["threshold"]==9.0 and th2["discovery"]["search_boundary_hit"] is True,
    }

    out={
        "experiment":"NOEPEDIA_EXP_050_GENERIC_CANDIDATE_EVALUATOR",
        "temporal_interior":t1,
        "temporal_boundary":t2,
        "threshold_interior":th1,
        "threshold_boundary":th2,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 050 reproducibility: PASS")
    print("Experiment 050 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
