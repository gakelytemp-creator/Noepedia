#!/usr/bin/env python3
from __future__ import annotations

import statistics
from typing import Any

LOW="STATE_LOW"
HIGH="STATE_HIGH"


def mismatch_count(predicted:list[str], target:list[str]) -> int:
    if len(predicted)!=len(target):
        raise ValueError("predicted/target length mismatch")
    return sum(a!=b for a,b in zip(predicted,target))


def transition(prev:str,curr:str) -> str|None:
    if prev==LOW and curr==HIGH:
        return "LOW_TO_HIGH"
    if prev==HIGH and curr==LOW:
        return "HIGH_TO_LOW"
    return None


def temporal_predictions(source:list[str], direction:str, lag:int) -> list[str]:
    preds=list(source)
    last_t=None
    prev_before=None
    for i in range(1,len(source)):
        prev=source[i-1]
        curr=source[i]
        d=transition(prev,curr)
        if d==direction:
            last_t=i
            prev_before=prev
        if last_t is not None and 0<=i-last_t<=lag:
            preds[i]=prev_before
        else:
            preds[i]=curr
    return preds


def circular_shift(values:list[Any], shift:int) -> list[Any]:
    if not values:
        return []
    n=len(values)
    s=shift % n
    return list(values) if s==0 else values[-s:]+values[:-s]


def majority_state(target:list[str]) -> str:
    high=sum(x==HIGH for x in target)
    low=len(target)-high
    return HIGH if high>=low else LOW


def evaluate_temporal_candidate(
    source_discovery:list[str],
    target_discovery:list[str],
    source_confirmation:list[str],
    target_confirmation:list[str],
    *,
    lag_min:int,
    lag_max:int,
    directions:list[str]|None=None,
    permutation_shifts:list[int]|None=None,
) -> dict[str,Any]:
    directions=directions or ["LOW_TO_HIGH","HIGH_TO_LOW"]
    permutation_shifts=permutation_shifts or []

    old_disc=mismatch_count(source_discovery,target_discovery)
    grid=[]
    for direction in directions:
        for lag in range(lag_min,lag_max+1):
            pred=temporal_predictions(source_discovery,direction,lag)
            mm=mismatch_count(pred,target_discovery)
            grid.append({
                "direction":direction,
                "lag":lag,
                "mismatches":mm,
                "net_reduction_vs_old":old_disc-mm,
            })

    grid.sort(key=lambda x:(x["mismatches"],x["lag"],directions.index(x["direction"])))
    selected=grid[0]
    boundary=selected["lag"] in {lag_min,lag_max}

    old_conf=mismatch_count(source_confirmation,target_confirmation)
    revised_conf_pred=temporal_predictions(
        source_confirmation,selected["direction"],selected["lag"]
    )
    revised_conf=mismatch_count(revised_conf_pred,target_confirmation)

    maj=majority_state(target_discovery)
    majority_metric=sum(maj!=x for x in target_confirmation)

    permutation=[]
    for shift in permutation_shifts:
        shifted=circular_shift(source_confirmation,shift)
        pred=temporal_predictions(shifted,selected["direction"],selected["lag"])
        permutation.append({
            "shift":shift,
            "mismatches":mismatch_count(pred,target_confirmation)
        })
    perm_median=(
        statistics.median([x["mismatches"] for x in permutation])
        if permutation else None
    )

    return {
        "family":"TEMPORAL_LAG_REVISION",
        "discovery":{
            "old_mismatches":old_disc,
            "selected_parameters":{
                "direction":selected["direction"],
                "lag":selected["lag"]
            },
            "selected_mismatches":selected["mismatches"],
            "search_boundary_hit":boundary,
            "grid":grid,
        },
        "confirmation":{
            "old_mismatches":old_conf,
            "revised_mismatches":revised_conf,
            "majority_state":maj,
            "majority_mismatches":majority_metric,
            "permutation_mismatches":permutation,
            "permutation_median_mismatches":perm_median,
        },
        "frozen_parameters":{
            "direction":selected["direction"],
            "lag":selected["lag"]
        },
        "required_null_metrics":{
            "MAJORITY_STATE_NULL":majority_metric,
            "SIMPLER_RULE_NULL":majority_metric,
            "TIME_SHIFT_OR_PERMUTATION_NULL":perm_median,
        }
    }


def threshold_predictions(values:list[float], threshold:float) -> list[str]:
    return [HIGH if x>threshold else LOW for x in values]


def evaluate_threshold_candidate(
    source_discovery:list[str],
    target_values_discovery:list[float],
    source_confirmation:list[str],
    target_values_confirmation:list[float],
    *,
    threshold_grid:list[float],
    old_threshold:float,
    perturbation_grid:list[float]|None=None,
) -> dict[str,Any]:
    if not threshold_grid:
        raise ValueError("threshold_grid must not be empty")

    old_disc=mismatch_count(
        source_discovery,
        threshold_predictions(target_values_discovery,old_threshold)
    )
    scored=[]
    for threshold in sorted(threshold_grid):
        target=threshold_predictions(target_values_discovery,threshold)
        mm=mismatch_count(source_discovery,target)
        scored.append({
            "threshold":threshold,
            "mismatches":mm,
            "net_reduction_vs_old":old_disc-mm,
        })
    scored.sort(key=lambda x:(x["mismatches"],x["threshold"]))
    selected=scored[0]
    min_thr=min(threshold_grid)
    max_thr=max(threshold_grid)
    boundary=selected["threshold"] in {min_thr,max_thr}

    old_conf_target=threshold_predictions(target_values_confirmation,old_threshold)
    revised_conf_target=threshold_predictions(
        target_values_confirmation,selected["threshold"]
    )
    old_conf=mismatch_count(source_confirmation,old_conf_target)
    revised_conf=mismatch_count(source_confirmation,revised_conf_target)

    perturbation_grid=perturbation_grid or []
    perturb=[]
    for threshold in sorted(perturbation_grid):
        if threshold==selected["threshold"]:
            continue
        mm=mismatch_count(
            source_confirmation,
            threshold_predictions(target_values_confirmation,threshold)
        )
        perturb.append({"threshold":threshold,"mismatches":mm})
    perturb_median=(
        statistics.median([x["mismatches"] for x in perturb])
        if perturb else None
    )

    return {
        "family":"THRESHOLD_REFINEMENT",
        "discovery":{
            "old_mismatches":old_disc,
            "selected_parameters":{"threshold":selected["threshold"]},
            "selected_mismatches":selected["mismatches"],
            "search_boundary_hit":boundary,
            "grid":scored,
        },
        "confirmation":{
            "old_mismatches":old_conf,
            "revised_mismatches":revised_conf,
            "threshold_perturbation_mismatches":perturb,
            "threshold_perturbation_median_mismatches":perturb_median,
        },
        "frozen_parameters":{"threshold":selected["threshold"]},
        "required_null_metrics":{
            "THRESHOLD_PERTURBATION_NULL":perturb_median
        }
    }



def invert_states(values:list[str]) -> list[str]:
    return [HIGH if x==LOW else LOW for x in values]


def evaluate_orientation_candidate(
    source_discovery:list[str],
    target_discovery:list[str],
    source_confirmation:list[str],
    target_confirmation:list[str],
) -> dict[str,Any]:
    direct_disc=mismatch_count(source_discovery,target_discovery)
    inverted_disc_pred=invert_states(source_discovery)
    inverted_disc=mismatch_count(inverted_disc_pred,target_discovery)

    if direct_disc<=inverted_disc:
        selected="DIRECT"
        disc_mm=direct_disc
    else:
        selected="INVERTED"
        disc_mm=inverted_disc

    direct_conf=mismatch_count(source_confirmation,target_confirmation)
    inverted_conf=mismatch_count(invert_states(source_confirmation),target_confirmation)
    revised_conf=direct_conf if selected=="DIRECT" else inverted_conf

    maj=majority_state(target_discovery)
    majority_metric=sum(maj!=x for x in target_confirmation)

    return {
        "family":"RELATION_ORIENTATION_REVISION",
        "discovery":{
            "direct_mismatches":direct_disc,
            "inverted_mismatches":inverted_disc,
            "selected_parameters":{"orientation":selected},
            "selected_mismatches":disc_mm,
            "search_boundary_hit":False,
        },
        "confirmation":{
            "direct_mismatches":direct_conf,
            "inverted_mismatches":inverted_conf,
            "revised_mismatches":revised_conf,
            "majority_state":maj,
            "majority_mismatches":majority_metric,
        },
        "frozen_parameters":{"orientation":selected},
        "required_null_metrics":{
            "MAJORITY_STATE_NULL":majority_metric
        }
    }


def evaluate_local_exception_candidate(
    discovery_event_matches:list[bool],
    confirmation_event_matches:list[bool],
    *,
    replication_threshold:float,
) -> dict[str,Any]:
    if not discovery_event_matches:
        raise ValueError("discovery_event_matches must not be empty")
    if not confirmation_event_matches:
        raise ValueError("confirmation_event_matches must not be empty")
    if not 0.0<=replication_threshold<=1.0:
        raise ValueError("replication_threshold must be between 0 and 1")

    disc_rate=sum(discovery_event_matches)/len(discovery_event_matches)
    conf_rate=sum(confirmation_event_matches)/len(confirmation_event_matches)
    replicated=conf_rate>=replication_threshold

    # For the generic gate engine, lower metric is better.
    # Exception error = non-matching confirmation events.
    revised_metric=sum(not x for x in confirmation_event_matches)
    old_metric=len(confirmation_event_matches)

    return {
        "family":"LOCAL_EXCEPTION_CANDIDATE",
        "discovery":{
            "event_count":len(discovery_event_matches),
            "match_count":sum(discovery_event_matches),
            "match_fraction":disc_rate,
            "selected_parameters":{
                "replication_threshold":replication_threshold
            },
            "search_boundary_hit":False,
        },
        "confirmation":{
            "event_count":len(confirmation_event_matches),
            "match_count":sum(confirmation_event_matches),
            "match_fraction":conf_rate,
            "replicated":replicated,
            "old_mismatches":old_metric,
            "revised_mismatches":revised_metric,
        },
        "frozen_parameters":{
            "replication_threshold":replication_threshold
        },
        "required_null_metrics":{
            "OUT_OF_CLUSTER_TRANSFER_TEST":revised_metric if replicated else 0
        }
    }


def evaluate_simpler_rule_comparator(
    target_discovery:list[str],
    target_confirmation:list[str],
    proposed_confirmation:list[str],
) -> dict[str,Any]:
    maj=majority_state(target_discovery)
    majority_metric=sum(maj!=x for x in target_confirmation)
    proposed_metric=mismatch_count(proposed_confirmation,target_confirmation)

    return {
        "family":"SIMPLER_RULE_COMPARATOR",
        "discovery":{
            "majority_state":maj,
            "search_boundary_hit":False,
        },
        "confirmation":{
            "proposed_mismatches":proposed_metric,
            "majority_mismatches":majority_metric,
            "proposed_beats_majority":proposed_metric<majority_metric,
        },
        "frozen_parameters":{
            "majority_state":maj
        },
        "required_null_metrics":{
            "SIMPLER_RULE_NULL":majority_metric,
            "MAJORITY_STATE_NULL":majority_metric,
        }
    }


def evaluate_candidate(candidate:dict[str,Any], data:dict[str,Any], config:dict[str,Any]) -> dict[str,Any]:
    family=candidate["family"]

    if family in {"TEMPORAL_LAG_REVISION","DIRECTION_SPECIFIC_RULE"}:
        lag=config.get("lag_search") or candidate.get("parameters",{}).get("lag_search")
        if not lag:
            raise ValueError("temporal candidate requires lag_search")
        return evaluate_temporal_candidate(
            data["source_discovery"],
            data["target_discovery"],
            data["source_confirmation"],
            data["target_confirmation"],
            lag_min=int(lag["min"]),
            lag_max=int(lag["max"]),
            directions=config.get("directions") or candidate.get("parameters",{}).get("direction_search"),
            permutation_shifts=config.get("permutation_shifts",[]),
        )

    if family=="THRESHOLD_REFINEMENT":
        return evaluate_threshold_candidate(
            data["source_discovery"],
            data["target_values_discovery"],
            data["source_confirmation"],
            data["target_values_confirmation"],
            threshold_grid=list(config["threshold_grid"]),
            old_threshold=float(config["old_threshold"]),
            perturbation_grid=list(config.get("perturbation_grid",[])),
        )

    if family=="RELATION_ORIENTATION_REVISION":
        return evaluate_orientation_candidate(
            data["source_discovery"],
            data["target_discovery"],
            data["source_confirmation"],
            data["target_confirmation"],
        )

    if family=="LOCAL_EXCEPTION_CANDIDATE":
        return evaluate_local_exception_candidate(
            data["discovery_event_matches"],
            data["confirmation_event_matches"],
            replication_threshold=float(config["replication_threshold"]),
        )

    if family=="SIMPLER_RULE_COMPARATOR":
        return evaluate_simpler_rule_comparator(
            data["target_discovery"],
            data["target_confirmation"],
            data["proposed_confirmation"],
        )

    raise NotImplementedError(f"generic evaluator does not support family {family}")
