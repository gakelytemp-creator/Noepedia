#!/usr/bin/env python3
from __future__ import annotations

import csv
import itertools
import json
import math
import random
import sys
import urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH
from core.revision.pipeline import run_revision_from_observations
from core.revision.scanner import scan_relation_pairs

SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))
RUNTIME=HERE/"_runtime"
RESULT=RUNTIME/"result.json"

CAL_N=SOURCE["split"]["calibration_count"]
DISC_N=SOURCE["split"]["discovery_count"]
BUF_N=SOURCE["split"]["buffer_count"]
EXPECTED_N=SOURCE["expected_rows"]
MIN_CLUSTER=SOURCE["adapter"]["minimum_cluster_size"]

def raw_url(motor):
    src=SOURCE["source"]
    return (
        f"https://raw.githubusercontent.com/{src['repository']}/"
        f"{src['commit']}/{src['base_path']}/data_motor_{motor}.csv"
    )

def read_motor(motor):
    req=urllib.request.Request(
        raw_url(motor),
        headers={"User-Agent":"Noepedia-Experiment-071/1.0"}
    )
    with urllib.request.urlopen(req,timeout=120) as r:
        text=r.read().decode("utf-8-sig")
    rows=list(csv.DictReader(text.splitlines()))
    out=[]
    for i,row in enumerate(rows):
        rec={
            "time":float(row["time"]),
            "position":float(row["position"]),
            "temperature":float(row["temperature"]),
            "voltage":float(row["voltage"]),
        }
        if not all(math.isfinite(v) for v in rec.values()):
            raise RuntimeError(f"motor {motor} row {i} contains non-finite telemetry")
        out.append(rec)
    return out

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

def state(x,thr):
    return HIGH if x>thr else LOW

def shuffle_copy(values,seed):
    out=list(values)
    random.Random(seed).shuffle(out)
    return out

def feature_config():
    return {
        "transition_radius":5,
        "temporal_fraction_threshold":0.70,
        "class_imbalance_threshold":0.80,
        "direction_ratio_threshold":3.0,
        "local_run_min":3,
        "local_run_fraction_threshold":0.30,
    }

def evaluator_config():
    return {
        "lag_search":{
            "min":SOURCE["temporal_search"]["lag_min"],
            "max":SOURCE["temporal_search"]["lag_max"],
        },
        "directions":SOURCE["temporal_search"]["directions"],
        "permutation_shifts":SOURCE["temporal_search"]["permutation_shifts"],
    }

def evaluate_pair(pair_index,a,b,series,shuffled):
    disc_start=CAL_N
    disc_end=disc_start+DISC_N
    conf_start=disc_end+BUF_N

    src_d=series[a][disc_start:disc_end]
    tgt_d=series[b][disc_start:disc_end]
    src_c=series[a][conf_start:]
    tgt_c=series[b][conf_start:]

    if shuffled:
        tgt_d=shuffle_copy(
            tgt_d,
            SOURCE["shuffled_control"]["discovery_seed_base"]+pair_index
        )
        tgt_c=shuffle_copy(
            tgt_c,
            SOURCE["shuffled_control"]["confirmation_seed_base"]+pair_index
        )

    mode="SHUFFLED" if shuffled else "REAL"
    context={
        "case_id":f"EXP071::{a}::{b}::{mode}",
        "parent_rule_id":f"RULE071::{a}::{b}::V1",
        "open_id":f"OPEN071::{a}::{b}",
        "proposed_new_rule_id":f"RULE071::{a}::{b}::V2",
        "lag_search":{
            "min":SOURCE["temporal_search"]["lag_min"],
            "max":SOURCE["temporal_search"]["lag_max"],
        },
        "search_is_bounded":True,
    }
    data={
        "source_discovery":src_d,
        "target_discovery":tgt_d,
        "source_confirmation":src_c,
        "target_confirmation":tgt_c,
        "proposed_confirmation":src_c,
    }

    r=run_revision_from_observations(
        context,
        data,
        evaluator_config(),
        feature_config=feature_config(),
        required_relative_advantage=SOURCE["temporal_search"]["required_relative_advantage"],
    )

    return {
        "pair_index":pair_index,
        "source":a,
        "target":b,
        "mode":mode,
        "features":r.get("feature_context",{}).get("features",[]),
        "risk_flags":r.get("feature_context",{}).get("risk_flags",[]),
        "selected_family":r.get("selected_candidate",{}).get("family"),
        "nulls":[n["name"] for n in r.get("null_specs",[])],
        "final_decision":r.get("final_decision"),
        "decision_reason":r.get("gate_audit",{}).get("decision_reason"),
        "frozen_parameters":(r.get("evaluation") or {}).get("frozen_parameters"),
        "required_null_metrics":(r.get("evaluation") or {}).get("required_null_metrics",{}),
        "graph_invariants":r.get("graph_invariants"),
    }

def main():
    RUNTIME.mkdir(exist_ok=True)

    motors={m:read_motor(m) for m in SOURCE["motors"]}
    lengths={m:len(rows) for m,rows in motors.items()}

    if len(set(lengths.values()))!=1 or next(iter(lengths.values()))!=EXPECTED_N:
        out={
            "experiment":SOURCE["experiment"],
            "primary_class":"NOT_EVALUABLE_ALIGNMENT",
            "lengths":lengths,
        }
        RESULT.write_text(json.dumps(out,indent=2)+"\n")
        print(json.dumps(out,indent=2))
        return 0

    for m,rows in motors.items():
        times=[r["time"] for r in rows]
        if any(times[i+1]<=times[i] for i in range(len(times)-1)):
            out={
                "experiment":SOURCE["experiment"],
                "primary_class":"NOT_EVALUABLE_ALIGNMENT",
                "reason":f"NON_MONOTONIC_TIME_MOTOR_{m}",
            }
            RESULT.write_text(json.dumps(out,indent=2)+"\n")
            print(json.dumps(out,indent=2))
            return 0

    thresholds={}
    invalid=[]
    series={}
    valid_meta={}

    for m in SOURCE["motors"]:
        for signal in SOURCE["signals"]:
            name=f"motor{m}_{signal}"
            vals=[row[signal] for row in motors[m]]
            fit=fit_kmeans_1d(vals[:CAL_N])
            thresholds[name]=fit
            valid=(
                math.isfinite(fit["low_centroid"])
                and math.isfinite(fit["high_centroid"])
                and math.isfinite(fit["threshold"])
                and fit["low_centroid"]<fit["high_centroid"]
                and fit["low_cluster_count"]>=MIN_CLUSTER
                and fit["high_cluster_count"]>=MIN_CLUSTER
            )
            if valid:
                series[name]=[state(x,fit["threshold"]) for x in vals]
                valid_meta[name]={"motor":m,"signal":signal}
            else:
                invalid.append({"channel":name,"fit":fit})

    valid_names=sorted(series)
    valid_motors={valid_meta[n]["motor"] for n in valid_names}
    valid_signals={valid_meta[n]["signal"] for n in valid_names}

    adapter_ok=(
        len(valid_names)>=SOURCE["adapter"]["minimum_valid_channels"]
        and len(valid_motors)>=SOURCE["adapter"]["minimum_distinct_motors"]
        and len(valid_signals)>=SOURCE["adapter"]["minimum_distinct_signal_types"]
    )

    if not adapter_ok:
        out={
            "experiment":SOURCE["experiment"],
            "experiment_class":SOURCE["experiment_class"],
            "primary_class":"NOT_EVALUABLE_ADAPTER_VALIDATION",
            "valid_channels":valid_names,
            "invalid_channels":invalid,
            "thresholds":thresholds,
        }
        RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
        print(json.dumps(out,indent=2,ensure_ascii=False))
        return 0

    pair_list=list(itertools.combinations(valid_names,2))
    disc_series={
        n:series[n][CAL_N:CAL_N+DISC_N]
        for n in valid_names
    }
    ranked=scan_relation_pairs(
        disc_series,
        pair_candidates=pair_list,
        feature_config=feature_config(),
    )

    real=[]
    shuffled=[]
    for i,(a,b) in enumerate(pair_list):
        real.append(evaluate_pair(i,a,b,series,False))
        shuffled.append(evaluate_pair(i,a,b,series,True))

    real_promotions=sum(x["final_decision"]=="PROMOTE" for x in real)
    shuffled_promotions=sum(x["final_decision"]=="PROMOTE" for x in shuffled)

    if shuffled_promotions>=1:
        primary="ANY_SHUFFLED_PROMOTION"
    elif real_promotions>=1:
        primary="REAL_PROMOTION_AND_SHUFFLED_ZERO"
    else:
        primary="NO_REAL_PROMOTION_AND_SHUFFLED_ZERO"

    out={
        "experiment":SOURCE["experiment"],
        "experiment_class":SOURCE["experiment_class"],
        "frozen_core_commit":SOURCE["frozen_core_commit"],
        "source":SOURCE["source"],
        "dataset":{
            "rows":EXPECTED_N,
            "valid_channel_count":len(valid_names),
            "invalid_channel_count":len(invalid),
            "valid_channels":valid_names,
            "invalid_channels":invalid,
            "pair_count":len(pair_list),
            "calibration_count":CAL_N,
            "discovery_count":DISC_N,
            "buffer_count":BUF_N,
            "confirmation_count":EXPECTED_N-(CAL_N+DISC_N+BUF_N),
        },
        "thresholds":thresholds,
        "ranked_pairs":ranked,
        "real_pair_results":real,
        "shuffled_pair_results":shuffled,
        "real_promotion_count":real_promotions,
        "shuffled_promotion_count":shuffled_promotions,
        "primary_class":primary,
    }
    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
