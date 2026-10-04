#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

LOW="STATE_LOW"
HIGH="STATE_HIGH"


def _transition(prev:str,curr:str):
    if prev==LOW and curr==HIGH:
        return "LOW_TO_HIGH"
    if prev==HIGH and curr==LOW:
        return "HIGH_TO_LOW"
    return None


def _longest_true_run(flags:list[bool]) -> int:
    best=cur=0
    for x in flags:
        if x:
            cur+=1
            best=max(best,cur)
        else:
            cur=0
    return best


def extract_mismatch_features(
    source:list[str],
    target:list[str],
    *,
    transition_radius:int=5,
    temporal_fraction_threshold:float=0.70,
    class_imbalance_threshold:float=0.80,
    direction_ratio_threshold:float=3.0,
    local_run_min:int=3,
    local_run_fraction_threshold:float=0.30,
    continuous_target:list[float]|None=None,
    reference_threshold:float|None=None,
    threshold_band:float|None=None,
    mid_band_fraction_threshold:float=0.10,
) -> dict[str,Any]:
    if len(source)!=len(target):
        raise ValueError("source/target length mismatch")
    n=len(source)
    if n==0:
        return {"features":[],"risk_flags":[],"diagnostics":{}}

    mismatch=[a!=b for a,b in zip(source,target)]
    mismatch_idx=[i for i,x in enumerate(mismatch) if x]

    transitions=[]
    for i in range(1,n):
        d=_transition(source[i-1],source[i])
        if d:
            transitions.append((i,d))

    near_transition=0
    direction_counts={"LOW_TO_HIGH":0,"HIGH_TO_LOW":0}
    if mismatch_idx and transitions:
        for m in mismatch_idx:
            nearest=min(transitions,key=lambda t:abs(m-t[0]))
            if abs(m-nearest[0])<=transition_radius:
                near_transition+=1
                direction_counts[nearest[1]]+=1

    temporal_fraction=(near_transition/len(mismatch_idx)) if mismatch_idx else 0.0

    low_to_high=direction_counts["LOW_TO_HIGH"]
    high_to_low=direction_counts["HIGH_TO_LOW"]
    small=min(low_to_high,high_to_low)
    large=max(low_to_high,high_to_low)
    direction_ratio=(large/small) if small>0 else (float("inf") if large>0 else 1.0)

    high_frac=sum(x==HIGH for x in target)/n
    majority_fraction=max(high_frac,1-high_frac)

    longest_run=_longest_true_run(mismatch)
    local_run_fraction=(longest_run/len(mismatch_idx)) if mismatch_idx else 0.0

    direct_mm=len(mismatch_idx)
    inverted_mm=sum((HIGH if s==LOW else LOW)!=t for s,t in zip(source,target))
    orientation_gap_fraction=abs(direct_mm-inverted_mm)/n

    features=[]
    risks=[]

    if mismatch_idx and temporal_fraction>=temporal_fraction_threshold:
        features.extend(["TEMPORAL_CLUSTERING","TRANSITION_ALIGNED_MISMATCH"])

    if near_transition>0 and large>=local_run_min and direction_ratio>=direction_ratio_threshold:
        features.append("DIRECTION_ASYMMETRY")

    if longest_run>=local_run_min and local_run_fraction>=local_run_fraction_threshold:
        features.append("LOCAL_RESIDUAL_CLUSTER")

    if majority_fraction>=class_imbalance_threshold:
        features.append("CLASS_IMBALANCE")
        risks.append("CLASS_IMBALANCE")

    if orientation_gap_fraction<=0.10:
        features.append("ORIENTATION_UNCERTAINTY")

    mid_band_fraction=None
    if continuous_target is not None and reference_threshold is not None and threshold_band is not None:
        if len(continuous_target)!=n:
            raise ValueError("continuous_target length mismatch")
        mid=sum(abs(x-reference_threshold)<=threshold_band for x in continuous_target)
        mid_band_fraction=mid/n
        if mid_band_fraction>=mid_band_fraction_threshold:
            features.extend(["MID_BAND_UNCERTAINTY","THRESHOLD_SENSITIVITY"])

    # Simpler baseline is plausible whenever target imbalance is material.
    if majority_fraction>=class_imbalance_threshold:
        risks.append("SIMPLE_BASELINE_PLAUSIBLE")

    # stable dedup
    features=list(dict.fromkeys(features))
    risks=list(dict.fromkeys(risks))

    return {
        "features":features,
        "risk_flags":risks,
        "diagnostics":{
            "row_count":n,
            "mismatch_count":len(mismatch_idx),
            "mismatch_fraction":len(mismatch_idx)/n,
            "transition_count":len(transitions),
            "near_transition_mismatch_count":near_transition,
            "temporal_fraction":temporal_fraction,
            "direction_counts":direction_counts,
            "direction_ratio":direction_ratio,
            "longest_mismatch_run":longest_run,
            "local_run_fraction":local_run_fraction,
            "target_majority_fraction":majority_fraction,
            "direct_mismatches":direct_mm,
            "inverted_mismatches":inverted_mm,
            "orientation_gap_fraction":orientation_gap_fraction,
            "mid_band_fraction":mid_band_fraction,
        }
    }


def enrich_context_from_observations(context:dict[str,Any], source:list[str], target:list[str], **kwargs) -> dict[str,Any]:
    extracted=extract_mismatch_features(source,target,**kwargs)
    out=dict(context)
    out["features"]=extracted["features"]
    out["risk_flags"]=extracted["risk_flags"]
    out["feature_diagnostics"]=extracted["diagnostics"]
    return out
