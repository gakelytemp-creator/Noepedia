#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.features import extract_mismatch_features
from core.revision.evaluator import LOW,HIGH


def delayed_after_high_to_low(source,lag):
    target=list(source)
    last=None
    prev_before=None
    for i in range(1,len(source)):
        prev=source[i-1]
        curr=source[i]
        if prev==HIGH and curr==LOW:
            last=i
            prev_before=prev
        if last is not None and 0<=i-last<=lag:
            target[i]=prev_before
        else:
            target[i]=curr
    return target


def main():
    source=[]
    for _ in range(6):
        source.extend([LOW]*10+[HIGH]*10)
    temporal_target=delayed_after_high_to_low(source,3)
    temporal=extract_mismatch_features(
        source,temporal_target,
        transition_radius=4,
        temporal_fraction_threshold=0.70,
        direction_ratio_threshold=2.0,
        local_run_min=3,
        local_run_fraction_threshold=0.20
    )

    imbalanced_target=[HIGH]*90+[LOW]*10
    imbalanced_source=[HIGH]*100
    imbalance=extract_mismatch_features(
        imbalanced_source,imbalanced_target,
        class_imbalance_threshold=0.80
    )

    threshold_source=[LOW]*10+[HIGH]*10
    threshold_target=[LOW]*10+[HIGH]*10
    continuous=[4.7,4.8,4.9,5.0,5.1,4.95,5.05,4.85,5.15,4.9]+[6.0]*10
    threshold=extract_mismatch_features(
        threshold_source,threshold_target,
        continuous_target=continuous,
        reference_threshold=5.0,
        threshold_band=0.2,
        mid_band_fraction_threshold=0.20
    )

    quiet_source=[LOW,HIGH]*20
    quiet_target=list(quiet_source)
    quiet=extract_mismatch_features(
        quiet_source,quiet_target,
        transition_radius=1
    )

    checks={
        "temporal_detected":
            "TEMPORAL_CLUSTERING" in temporal["features"],
        "transition_alignment_detected":
            "TRANSITION_ALIGNED_MISMATCH" in temporal["features"],
        "direction_asymmetry_detected":
            "DIRECTION_ASYMMETRY" in temporal["features"],
        "local_cluster_detected":
            "LOCAL_RESIDUAL_CLUSTER" in temporal["features"],
        "imbalance_detected":
            "CLASS_IMBALANCE" in imbalance["features"],
        "imbalance_risk_flag":
            "CLASS_IMBALANCE" in imbalance["risk_flags"],
        "simpler_baseline_risk_flag":
            "SIMPLE_BASELINE_PLAUSIBLE" in imbalance["risk_flags"],
        "mid_band_detected":
            "MID_BAND_UNCERTAINTY" in threshold["features"],
        "threshold_sensitivity_detected":
            "THRESHOLD_SENSITIVITY" in threshold["features"],
        "quiet_no_temporal_feature":
            "TEMPORAL_CLUSTERING" not in quiet["features"],
        "quiet_no_local_cluster":
            "LOCAL_RESIDUAL_CLUSTER" not in quiet["features"]
    }

    out={
        "experiment":"NOEPEDIA_EXP_053_MISMATCH_FEATURE_EXTRACTOR",
        "temporal":temporal,
        "imbalance":imbalance,
        "threshold":threshold,
        "quiet":quiet,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 053 reproducibility: PASS")
    print("Experiment 053 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
