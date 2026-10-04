#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations
from typing import Any

from .features import extract_mismatch_features


FEATURE_WEIGHTS={
    "DIRECTION_ASYMMETRY":4.0,
    "TEMPORAL_CLUSTERING":3.0,
    "TRANSITION_ALIGNED_MISMATCH":3.0,
    "THRESHOLD_SENSITIVITY":2.5,
    "MID_BAND_UNCERTAINTY":2.0,
    "LOCAL_RESIDUAL_CLUSTER":1.5,
    "ORIENTATION_UNCERTAINTY":1.0,
    "CLASS_IMBALANCE":-2.0,
}


def _nontriviality_score(mismatch_fraction:float) -> float:
    # Prefer neither nearly-perfect nor near-random direct mappings.
    # Peak around 0.20, taper toward 0 and 0.5.
    return max(0.0, 1.0 - abs(mismatch_fraction-0.20)/0.20)


def score_pair(feature_result:dict[str,Any]) -> float:
    features=feature_result.get("features",[])
    diag=feature_result.get("diagnostics",{})
    mismatch_fraction=float(diag.get("mismatch_fraction",0.0))

    score=sum(FEATURE_WEIGHTS.get(f,0.0) for f in features)
    score += 3.0*_nontriviality_score(mismatch_fraction)

    # Penalize trivial/no-mismatch pairs and strongly imbalanced targets.
    if mismatch_fraction<0.01:
        score-=5.0
    if mismatch_fraction>0.49:
        score-=1.5
    if float(diag.get("target_majority_fraction",0.5))>=0.95:
        score-=3.0

    return score


def scan_relation_pairs(
    series:dict[str,list[str]],
    *,
    pair_candidates:list[tuple[str,str]]|None=None,
    feature_config:dict[str,Any]|None=None,
) -> list[dict[str,Any]]:
    if not series:
        return []

    lengths={len(v) for v in series.values()}
    if len(lengths)!=1:
        raise ValueError("all relation series must have equal length")

    names=sorted(series)
    pairs=pair_candidates or list(combinations(names,2))
    feature_config=feature_config or {}

    out=[]
    for source_name,target_name in pairs:
        if source_name not in series or target_name not in series:
            raise KeyError(f"unknown pair {source_name}, {target_name}")

        extracted=extract_mismatch_features(
            series[source_name],
            series[target_name],
            **feature_config
        )
        out.append({
            "source":source_name,
            "target":target_name,
            "features":extracted["features"],
            "risk_flags":extracted["risk_flags"],
            "diagnostics":extracted["diagnostics"],
            "score":score_pair(extracted),
        })

    out.sort(key=lambda x:(-x["score"],x["source"],x["target"]))
    return out


def select_revision_pair(scan_results:list[dict[str,Any]], *, minimum_score:float=1.0):
    if not scan_results:
        return None
    top=scan_results[0]
    if top["score"]<minimum_score:
        return None
    if not top["features"]:
        return None
    return top
