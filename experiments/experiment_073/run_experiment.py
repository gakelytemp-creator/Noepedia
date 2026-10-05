#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import sys
import urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH,evaluate_temporal_candidate
from core.revision.engine import evaluate_case

SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))
RUNTIME=HERE/"_runtime"
RESULT=RUNTIME/"result.json"

CAL_N=SOURCE["split"]["calibration_count"]
DISC_N=SOURCE["split"]["discovery_count"]
BUF_N=SOURCE["split"]["buffer_count"]
EXPECTED_N=SOURCE["external"]["expected_rows"]
MIN_CLUSTER=SOURCE["adapter"]["minimum_cluster_size"]

def raw_url():
    ext=SOURCE["external"]
    return (
        f"https://raw.githubusercontent.com/{ext['repository']}/"
        f"{ext['commit']}/{ext['file']}"
    )

def read_rows():
    req=urllib.request.Request(
        raw_url(),
        headers={"User-Agent":"Noepedia-Experiment-073/1.0"}
    )
    with urllib.request.urlopen(req,timeout=120) as r:
        text=r.read().decode("utf-8-sig")
    rows=[]
    for i,row in enumerate(csv.DictReader(text.splitlines())):
        rec={
            "time":float(row["time"]),
            "voltage":float(row["voltage"]),
            "temperature":float(row["temperature"]),
        }
        if not all(math.isfinite(v) for v in rec.values()):
            raise RuntimeError(f"row {i} contains non-finite hypothesis telemetry")
        rows.append(rec)
    return rows

def fit_kmeans_1d(values):
    vals=[float(x) for x in values]
    c0=min(vals); c1=max(vals)
    g0=[]; g1=[]
    for _ in range(100):
        g0=[]; g1=[]
        for x in vals:
            if abs(x-c0)<=abs(x-c1):
                g0.append(x)
            else:
                g1.append(x)
        if not g0 or not g1:
            break
        n0=sum(g0)/len(g0); n1=sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1
    if c0<=c1:
        lo,hi=c0,c1
        low_count,high_count=len(g0),len(g1)
    else:
        lo,hi=c1,c0
        low_count,high_count=len(g1),len(g0)
    return {
        "low_centroid":float(lo),
        "high_centroid":float(hi),
        "threshold":float((lo+hi)/2.0),
        "low_cluster_count":low_count,
        "high_cluster_count":high_count,
    }

def state(x,threshold):
    return HIGH if x>threshold else LOW

def adapter_valid(fit):
    return (
        math.isfinite(fit["low_centroid"])
        and math.isfinite(fit["high_centroid"])
        and math.isfinite(fit["threshold"])
        and fit["low_centroid"]<fit["high_centroid"]
        and fit["low_cluster_count"]>=MIN_CLUSTER
        and fit["high_cluster_count"]>=MIN_CLUSTER
    )

def main():
    RUNTIME.mkdir(exist_ok=True)
    rows=read_rows()

    if len(rows)!=EXPECTED_N:
        out={
            "experiment":SOURCE["experiment"],
            "outcome":"NOT_EVALUABLE_ALIGNMENT",
            "reason":"UNEXPECTED_ROW_COUNT",
            "observed_rows":len(rows),
            "expected_rows":EXPECTED_N,
        }
        RESULT.write_text(json.dumps(out,indent=2)+"\n")
        print(json.dumps(out,indent=2))
        return 0

    times=[r["time"] for r in rows]
    if any(times[i+1]<=times[i] for i in range(len(times)-1)):
        out={
            "experiment":SOURCE["experiment"],
            "outcome":"NOT_EVALUABLE_ALIGNMENT",
            "reason":"NON_MONOTONIC_TIME",
        }
        RESULT.write_text(json.dumps(out,indent=2)+"\n")
        print(json.dumps(out,indent=2))
        return 0

    voltage=[r["voltage"] for r in rows]
    temp=[r["temperature"] for r in rows]

    voltage_fit=fit_kmeans_1d(voltage[:CAL_N])
    temp_fit=fit_kmeans_1d(temp[:CAL_N])

    if not adapter_valid(voltage_fit) or not adapter_valid(temp_fit):
        out={
            "experiment":SOURCE["experiment"],
            "outcome":"NOT_EVALUABLE_ADAPTER_VALIDATION",
            "adapter":{
                "voltage":voltage_fit,
                "temperature":temp_fit,
                "minimum_cluster_size":MIN_CLUSTER,
            }
        }
        RESULT.write_text(json.dumps(out,indent=2)+"\n")
        print(json.dumps(out,indent=2))
        return 0

    source=[state(x,voltage_fit["threshold"]) for x in voltage]
    target=[state(x,temp_fit["threshold"]) for x in temp]

    disc_start=CAL_N
    disc_end=disc_start+DISC_N
    conf_start=disc_end+BUF_N

    ev=evaluate_temporal_candidate(
        source[disc_start:disc_end],
        target[disc_start:disc_end],
        source[conf_start:],
        target[conf_start:],
        lag_min=SOURCE["temporal_search"]["lag_min"],
        lag_max=SOURCE["temporal_search"]["lag_max"],
        directions=SOURCE["temporal_search"]["directions"],
        permutation_shifts=SOURCE["temporal_search"]["permutation_shifts"],
    )

    conf=ev["confirmation"]
    disc=ev["discovery"]
    metrics=ev["required_null_metrics"]

    gate_case={
        "case_id":"EXP073_MOTOR1_THERMAL_LAG",
        "candidate_id":"RULE073_MOTOR1_THERMAL_LAG_CANDIDATE",
        "parent_rule_id":"RULE073_BASELINE_NO_FIXED_THERMAL_LAG",
        "open_id":"OPEN073_MOTOR1_THERMAL_LAG",
        "proposed_new_rule_id":"RULE073_MOTOR1_THERMAL_LAG_SUPPORTED",
        "confirmation_result_id":"EXP073::CONFIRMATION_RESULT",
        "preregistration_id":"EXP073::PREREGISTRATION",
        "parent_rule_exists":True,
        "open_exists":True,
        "provenance_complete":True,
        "candidate_parameters_explicit":True,
        "candidate_promotable":True,
        "preregistration_frozen":True,
        "discovery_confirmation_separated":True,
        "confirmation_untouched":True,
        "evidence_role_explicit":True,
        "confirmation_evaluable":True,
        "unresolved_not_counted_as_success":True,
        "evaluator_frozen":True,
        "corrections_documented":True,
        "history_preserved":True,
        "open_refinement_prepared":True,
        "old_metric":conf["old_mismatches"],
        "revised_metric":conf["revised_mismatches"],
        "required_nulls":[
            {
                "name":"MAJORITY_STATE_NULL",
                "metric":metrics["MAJORITY_STATE_NULL"],
                "required_relative_advantage":SOURCE["temporal_search"]["required_relative_advantage"],
            },
            {
                "name":"SIMPLER_RULE_NULL",
                "metric":metrics["SIMPLER_RULE_NULL"],
                "required_relative_advantage":SOURCE["temporal_search"]["required_relative_advantage"],
            },
            {
                "name":"TIME_SHIFT_OR_PERMUTATION_NULL",
                "metric":metrics["TIME_SHIFT_OR_PERMUTATION_NULL"],
                "required_relative_advantage":SOURCE["temporal_search"]["required_relative_advantage"],
            },
        ],
        "search_boundary_hit":disc["search_boundary_hit"],
        "search_boundary_policy":"REMAIN_OPEN",
        "direction_consistency_required":False,
    }

    audit=evaluate_case(gate_case)

    if audit["final_decision"]=="PROMOTE":
        outcome="HYPOTHESIS_SUPPORTED"
    elif audit["final_decision"]=="REJECT":
        outcome="HYPOTHESIS_REJECTED"
    else:
        outcome="HYPOTHESIS_REMAINS_OPEN"

    out={
        "experiment":SOURCE["experiment"],
        "experiment_class":SOURCE["experiment_class"],
        "hypothesis":SOURCE["hypothesis"]["statement"],
        "source":SOURCE["external"],
        "adapter":{
            "voltage":voltage_fit,
            "temperature":temp_fit,
            "minimum_cluster_size":MIN_CLUSTER,
        },
        "split":SOURCE["split"],
        "discovery":{
            "old_mismatches":disc["old_mismatches"],
            "selected_parameters":disc["selected_parameters"],
            "selected_mismatches":disc["selected_mismatches"],
            "search_boundary_hit":disc["search_boundary_hit"],
        },
        "confirmation":{
            "old_mismatches":conf["old_mismatches"],
            "revised_mismatches":conf["revised_mismatches"],
            "majority_state":conf["majority_state"],
            "majority_mismatches":conf["majority_mismatches"],
            "permutation_mismatches":conf["permutation_mismatches"],
            "permutation_median_mismatches":conf["permutation_median_mismatches"],
        },
        "required_null_metrics":metrics,
        "gate_audit":audit,
        "outcome":outcome,
    }

    RESULT.write_text(
        json.dumps(out,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
