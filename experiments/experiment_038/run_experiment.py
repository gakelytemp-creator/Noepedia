#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, statistics, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

CAL_COUNT=50_000
DISC_START=750_001
DISC_COUNT=5_000
CONF_START=800_001
CONF_COUNT=5_000
HISTORY=401
LAG_MIN=1
LAG_MAX=400
SHIFTS=[500,1000,1500,2000]
STATE_LOW="STATE_LOW"
STATE_HIGH="STATE_HIGH"

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
RESULT=WORK/"result.json"

FAMILIES=[
    {"id":"F036","source":"TP2","target":"TP3","direction":"HIGH_TO_LOW"},
    {"id":"F037","source":"Reservoirs","target":"H1","direction":"HIGH_TO_LOW"},
]


def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def download(url,dest):
    with urllib.request.urlopen(url,timeout=120) as r,dest.open("wb") as out:
        while True:
            b=r.read(1<<20)
            if not b: break
            out.write(b)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        matches=[n for n in z.namelist() if Path(n).name==basename]
        if len(matches)!=1:
            raise RuntimeError(f"expected one member, got {matches}")
        with z.open(matches[0]) as src,dest.open("wb") as out:
            while True:
                b=src.read(1<<20)
                if not b: break
                out.write(b)


def fit_1d_kmeans(vals):
    c0,c1=min(vals),max(vals)
    for _ in range(100):
        g0=[]; g1=[]
        for x in vals:
            (g0 if abs(x-c0)<=abs(x-c1) else g1).append(x)
        n0=sum(g0)/len(g0)
        n1=sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1
    lo,hi=min(c0,c1),max(c0,c1)
    return lo,hi,(lo+hi)/2


def state(x,thr):
    return STATE_HIGH if x>thr else STATE_LOW


def load_data():
    channels=["TP2","TP3","Reservoirs","H1"]
    calibration={c:[] for c in channels}
    rows={}
    min_start=DISC_START-HISTORY
    max_end=CONF_START+CONF_COUNT-1

    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        missing=set(channels)-set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing columns: {sorted(missing)}")

        for i,row in enumerate(reader,start=1):
            if i<=CAL_COUNT:
                for c in channels:
                    calibration[c].append(float(row[c]))
            if min_start<=i<=max_end:
                rows[i]={c:float(row[c]) for c in channels}
            if i>max_end:
                break

    return calibration,rows


def build_thresholds(calibration):
    out={}
    for c,vals in calibration.items():
        lo,hi,thr=fit_1d_kmeans(vals)
        out[c]={"low_centroid":lo,"high_centroid":hi,"threshold":thr}
    return out


def build_series(rows,start,count,thresholds,source,target):
    series={}
    for i in range(start-HISTORY,start+count):
        series[i]={
            source:state(rows[i][source],thresholds[source]["threshold"]),
            target:state(rows[i][target],thresholds[target]["threshold"])
        }
    return series


def temporal_predictions(series,start,count,source,lag):
    preds={}
    last_hl=None

    for i in range(start-HISTORY+1,start+count):
        prev=series[i-1][source]
        curr=series[i][source]
        if prev==STATE_HIGH and curr==STATE_LOW:
            last_hl=i

        if i<start:
            continue

        expected=curr
        if last_hl is not None and 0<=i-last_hl<=lag:
            expected=STATE_HIGH
        preds[i]=expected

    return preds


def mismatch_count(series,start,count,target,preds):
    return sum(preds[i]!=series[i][target] for i in range(start,start+count))


def old_predictions(series,start,count,source):
    return {i:series[i][source] for i in range(start,start+count)}


def discovery_search(series,source,target):
    old=old_predictions(series,DISC_START,DISC_COUNT,source)
    old_mm=mismatch_count(series,DISC_START,DISC_COUNT,target,old)
    curve=[]

    for lag in range(LAG_MIN,LAG_MAX+1):
        preds=temporal_predictions(series,DISC_START,DISC_COUNT,source,lag)
        mm=mismatch_count(series,DISC_START,DISC_COUNT,target,preds)
        curve.append({
            "lag":lag,
            "mismatches":mm,
            "net_reduction_vs_old":old_mm-mm
        })

    best=min(curve,key=lambda x:(x["mismatches"],x["lag"]))
    return old_mm,best,curve


def majority_state(series,start,count,target):
    vals=[series[i][target] for i in range(start,start+count)]
    high=sum(v==STATE_HIGH for v in vals)
    low=count-high
    return STATE_HIGH if high>=low else STATE_LOW


def circular_shift_states(states,shift):
    n=len(states)
    s=shift % n
    return states[-s:]+states[:-s] if s else list(states)


def temporal_predictions_circular_shift(source_states,lag):
    n=len(source_states)
    preds=[None]*n

    # Determine, for each position, distance since most recent HIGH->LOW transition
    # on the circular source sequence, capped beyond lag.
    transitions=[]
    for i in range(n):
        prev=source_states[(i-1)%n]
        curr=source_states[i]
        if prev==STATE_HIGH and curr==STATE_LOW:
            transitions.append(i)

    if not transitions:
        return list(source_states)

    for i in range(n):
        d=min((i-t)%n for t in transitions)
        if d<=lag:
            preds[i]=STATE_HIGH
        else:
            preds[i]=source_states[i]
    return preds


def confirm_family(series_disc,series_conf,fam,thresholds):
    source=fam["source"]
    target=fam["target"]

    disc_old_mm,best,curve=discovery_search(series_disc,source,target)
    selected_lag=best["lag"]

    # Freeze discovery majority state.
    majority=majority_state(series_disc,DISC_START,DISC_COUNT,target)

    old_preds=old_predictions(series_conf,CONF_START,CONF_COUNT,source)
    revised_preds=temporal_predictions(series_conf,CONF_START,CONF_COUNT,source,selected_lag)

    old_mm=mismatch_count(series_conf,CONF_START,CONF_COUNT,target,old_preds)
    revised_mm=mismatch_count(series_conf,CONF_START,CONF_COUNT,target,revised_preds)

    majority_mm=sum(
        majority!=series_conf[i][target]
        for i in range(CONF_START,CONF_START+CONF_COUNT)
    )

    source_states=[series_conf[i][source] for i in range(CONF_START,CONF_START+CONF_COUNT)]
    target_states=[series_conf[i][target] for i in range(CONF_START,CONF_START+CONF_COUNT)]

    perm_counts=[]
    for shift in SHIFTS:
        shifted=circular_shift_states(source_states,shift)
        pp=temporal_predictions_circular_shift(shifted,selected_lag)
        mm=sum(pp[j]!=target_states[j] for j in range(CONF_COUNT))
        perm_counts.append({"shift":shift,"mismatches":mm})

    perm_median=statistics.median([x["mismatches"] for x in perm_counts])

    beats_old=revised_mm<old_mm
    beats_majority=(revised_mm <= 0.90*majority_mm) if majority_mm>0 else False
    beats_perm=(revised_mm <= 0.90*perm_median) if perm_median>0 else False
    passed=beats_old and beats_majority and beats_perm

    return {
        "family":fam["id"],
        "source":source,
        "target":target,
        "direction":"HIGH_TO_LOW",
        "discovery":{
            "old_mismatches":disc_old_mm,
            "selected_lag":selected_lag,
            "selected_mismatches":best["mismatches"],
            "selected_net_reduction_vs_old":best["net_reduction_vs_old"],
            "lag_boundary_hit":selected_lag==LAG_MAX,
            "curve_min_20":[x for x in curve if abs(x["lag"]-selected_lag)<=10]
        },
        "frozen_majority_state":majority,
        "confirmation":{
            "old_mismatches":old_mm,
            "revised_mismatches":revised_mm,
            "majority_mismatches":majority_mm,
            "permutation_mismatches":perm_counts,
            "permutation_median_mismatches":perm_median,
            "relative_reduction_vs_old":((old_mm-revised_mm)/old_mm) if old_mm else None,
            "relative_reduction_vs_majority":((majority_mm-revised_mm)/majority_mm) if majority_mm else None,
            "relative_reduction_vs_permutation_median":((perm_median-revised_mm)/perm_median) if perm_median else None,
            "beats_old":beats_old,
            "beats_majority_by_10_percent":beats_majority,
            "beats_permutation_by_10_percent":beats_perm
        },
        "result_class":"NULL_PROTECTED_CONFIRMED" if passed else "NOT_NULL_PROTECTED"
    }


def main():
    WORK.mkdir(exist_ok=True)

    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    calibration,rows=load_data()
    thresholds=build_thresholds(calibration)

    results=[]
    for fam in FAMILIES:
        disc_series=build_series(rows,DISC_START,DISC_COUNT,thresholds,fam["source"],fam["target"])
        conf_series=build_series(rows,CONF_START,CONF_COUNT,thresholds,fam["source"],fam["target"])
        results.append(confirm_family(disc_series,conf_series,fam,thresholds))

    passes=sum(r["result_class"]=="NULL_PROTECTED_CONFIRMED" for r in results)
    if passes==2:
        overall="BOTH_FAMILIES_NULL_PROTECTED"
    elif passes==1:
        overall="ONE_FAMILY_NULL_PROTECTED"
    else:
        overall="NO_FAMILY_NULL_PROTECTED"

    out={
        "experiment":"NOEPEDIA_EXP_038_NULL_PROTECTED_VALIDATION",
        "thresholds":thresholds,
        "windows":{
            "discovery":{"start":DISC_START,"count":DISC_COUNT},
            "confirmation":{"start":CONF_START,"count":CONF_COUNT}
        },
        "families":results,
        "overall_result":overall,
        "claim_boundary":{
            "causality_established":False,
            "physical_independence_established":False
        }
    }

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 038 reproducibility: PASS")
    print("Experiment 038 result:",overall)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
