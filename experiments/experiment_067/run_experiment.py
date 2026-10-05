#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import math
import random
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
from scipy.io import loadmat

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH
from core.revision.pipeline import run_revision_from_observations
from core.revision.scanner import scan_relation_pairs

SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))
RUNTIME=HERE/"_runtime"
ZIP_PATH=RUNTIME/"mill.zip"
EXTRACT=RUNTIME/"data"
RESULT=RUNTIME/"result.json"

CHANNELS=SOURCE["dataset"]["channels"]
CAL_N=SOURCE["split"]["calibration_count"]
DISC_N=SOURCE["split"]["discovery_count"]
BUF_N=SOURCE["split"]["buffer_count"]
MIN_N=SOURCE["split"]["minimum_total_runs"]

def download(url,dest):
    req=urllib.request.Request(url,headers={"User-Agent":"Noepedia-Experiment-067/1.0"})
    with urllib.request.urlopen(req,timeout=180) as src,dest.open("wb") as out:
        shutil.copyfileobj(src,out)

def find_mat(root):
    matches=list(root.rglob("mill.mat"))
    if not matches:
        matches=list(root.rglob("*.mat"))
    if len(matches)!=1:
        raise RuntimeError(f"expected one MATLAB file, found {matches}")
    return matches[0]

def scalar(x):
    a=np.asarray(x).squeeze()
    if a.size==0:
        return None
    return float(a.flat[0])

def flatten_numeric(x):
    a=np.asarray(x)
    if a.dtype==object and a.size==1:
        a=np.asarray(a.flat[0])
    a=np.asarray(a,dtype=float).ravel()
    return a[np.isfinite(a)]

def extract_runs(mat_path):
    data=loadmat(mat_path,squeeze_me=False,struct_as_record=True)
    mill=data.get("mill")
    if mill is None or mill.dtype.names is None:
        raise RuntimeError("could not identify structured milling array")

    fields=set(mill.dtype.names)
    missing=[ch for ch in CHANNELS if ch not in fields]
    if missing:
        raise RuntimeError(f"missing milling fields: {missing}")

    flat=mill.ravel()
    runs=[]
    for idx,item in enumerate(flat):
        rec={}
        for ch in CHANNELS:
            vals=flatten_numeric(item[ch])
            if vals.size==0:
                raise RuntimeError(f"run {idx} empty channel {ch}")
            rec[ch]=float(np.sqrt(np.mean(vals*vals)))
        for meta in ["case","run","VB","time","DOC","feed","material"]:
            rec[meta]=scalar(item[meta]) if meta in fields else None
        rec["_source_index"]=idx
        runs.append(rec)
    return runs

def fit_kmeans_1d(values):
    vals=[float(x) for x in values]
    c0=min(vals); c1=max(vals)
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
    lo,hi=sorted([c0,c1])
    return {"low_centroid":lo,"high_centroid":hi,"threshold":(lo+hi)/2.0}

def state(x,threshold):
    return HIGH if x>threshold else LOW

def shuffle_copy(values,seed):
    out=list(values)
    random.Random(seed).shuffle(out)
    return out

def evaluate_pair(pair_index,a,b,series,shuffled=False):
    cal_end=CAL_N
    disc_end=cal_end+DISC_N
    buf_end=disc_end+BUF_N

    src=series[a]
    tgt=series[b]

    src_d=src[cal_end:disc_end]
    tgt_d=tgt[cal_end:disc_end]
    src_c=src[buf_end:]
    tgt_c=tgt[buf_end:]

    if shuffled:
        tgt_d=shuffle_copy(tgt_d,SOURCE["shuffled_control"]["discovery_seed_base"]+pair_index)
        tgt_c=shuffle_copy(tgt_c,SOURCE["shuffled_control"]["confirmation_seed_base"]+pair_index)

    data={
        "source_discovery":src_d,
        "target_discovery":tgt_d,
        "source_confirmation":src_c,
        "target_confirmation":tgt_c,
        "proposed_confirmation":src_c
    }
    context={
        "case_id":f"EXP067::{a}::{b}::{'SHUFFLED' if shuffled else 'REAL'}",
        "parent_rule_id":f"RULE067::{a}::{b}::V1",
        "open_id":f"OPEN067::{a}::{b}",
        "proposed_new_rule_id":f"RULE067::{a}::{b}::V2",
        "lag_search":{
            "min":SOURCE["temporal_search"]["lag_min"],
            "max":SOURCE["temporal_search"]["lag_max"]
        },
        "search_is_bounded":True
    }
    config={
        "lag_search":{
            "min":SOURCE["temporal_search"]["lag_min"],
            "max":SOURCE["temporal_search"]["lag_max"]
        },
        "directions":SOURCE["temporal_search"]["directions"],
        "permutation_shifts":SOURCE["temporal_search"]["permutation_shifts"]
    }
    feature_config={
        "transition_radius":5,
        "temporal_fraction_threshold":0.70,
        "class_imbalance_threshold":0.80,
        "direction_ratio_threshold":3.0,
        "local_run_min":3,
        "local_run_fraction_threshold":0.30
    }

    try:
        r=run_revision_from_observations(
            context,data,config,
            feature_config=feature_config,
            required_relative_advantage=SOURCE["temporal_search"]["required_relative_advantage"]
        )
        return {
            "pair_index":pair_index,
            "source":a,
            "target":b,
            "mode":"SHUFFLED" if shuffled else "REAL",
            "features":r.get("feature_context",{}).get("features",[]),
            "risk_flags":r.get("feature_context",{}).get("risk_flags",[]),
            "selected_family":r.get("selected_candidate",{}).get("family"),
            "nulls":[n["name"] for n in r.get("null_specs",[])],
            "final_decision":r.get("final_decision"),
            "decision_reason":r.get("gate_audit",{}).get("decision_reason"),
            "frozen_parameters":(r.get("evaluation") or {}).get("frozen_parameters"),
            "graph_invariants":r.get("graph_invariants")
        }
    except (KeyError,NotImplementedError,ValueError) as exc:
        return {
            "pair_index":pair_index,
            "source":a,
            "target":b,
            "mode":"SHUFFLED" if shuffled else "REAL",
            "final_decision":"REMAIN_OPEN",
            "decision_reason":"GENERIC_EVALUATOR_INPUT_NOT_AVAILABLE",
            "error_type":type(exc).__name__
        }

def main():
    RUNTIME.mkdir(exist_ok=True)
    if not ZIP_PATH.exists():
        download(SOURCE["dataset"]["official_zip"],ZIP_PATH)
    if not EXTRACT.exists():
        EXTRACT.mkdir()
        with zipfile.ZipFile(ZIP_PATH) as z:
            z.extractall(EXTRACT)

    runs=extract_runs(find_mat(EXTRACT))
    n=len(runs)
    if n<MIN_N:
        out={
            "experiment":SOURCE["experiment"],
            "primary_class":"NOT_EVALUABLE_DATASET_PARSE",
            "run_count":n
        }
        RESULT.write_text(json.dumps(out,indent=2)+"\n")
        print(json.dumps(out,indent=2))
        return 0

    thresholds={}
    series={}
    for ch in CHANNELS:
        fit=fit_kmeans_1d([r[ch] for r in runs[:CAL_N]])
        thresholds[ch]=fit
        series[ch]=[state(r[ch],fit["threshold"]) for r in runs]

    pair_list=list(itertools.combinations(CHANNELS,2))

    # Discovery ranking is recorded as secondary evidence only.
    disc_series={ch:series[ch][CAL_N:CAL_N+DISC_N] for ch in CHANNELS}
    scan=scan_relation_pairs(
        disc_series,
        pair_candidates=pair_list,
        feature_config={
            "transition_radius":5,
            "temporal_fraction_threshold":0.70,
            "class_imbalance_threshold":0.80,
            "direction_ratio_threshold":3.0,
            "local_run_min":3,
            "local_run_fraction_threshold":0.30
        }
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
        "dataset":{
            "parsed_runs":n,
            "channels":CHANNELS,
            "calibration_count":CAL_N,
            "discovery_count":DISC_N,
            "buffer_count":BUF_N,
            "confirmation_count":n-(CAL_N+DISC_N+BUF_N)
        },
        "thresholds":thresholds,
        "ranked_pairs":scan,
        "real_pair_results":real,
        "shuffled_pair_results":shuffled,
        "real_promotion_count":real_promotions,
        "shuffled_promotion_count":shuffled_promotions,
        "primary_class":primary
    }
    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
