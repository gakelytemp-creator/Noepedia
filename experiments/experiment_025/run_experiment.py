#!/usr/bin/env python3
from __future__ import annotations

import bisect
import csv
import hashlib
import json
import math
import statistics
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

CALIBRATION_ROWS=50_000
WINDOW_START=200_001
WINDOW_ROWS=5_000
FUTURE_CONTEXT_ROWS=101
READ_THROUGH=WINDOW_START-1+WINDOW_ROWS+FUTURE_CONTEXT_ROWS
MAX_KMEANS_ITER=100
DISTANCE_CAP=101
ALPHA_LOW=0.2
ALPHA_HIGH=0.8

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
RESULT=WORK/"result.json"


def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
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
            raise RuntimeError(f"expected one CSV member named {basename}, found {matches}")
        with z.open(matches[0]) as src,dest.open("wb") as out:
            while True:
                b=src.read(1<<20)
                if not b: break
                out.write(b)


def read_rows(path):
    rows=[]
    with path.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        required={"DV_eletric","Motor_current","TP2"}
        missing=required-set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing columns: {sorted(missing)}")
        for i,row in enumerate(reader,start=1):
            if i>READ_THROUGH: break
            rows.append({
                "i":i,
                "dv":int(float(row["DV_eletric"])),
                "mc":float(row["Motor_current"]),
                "tp2":float(row["TP2"])
            })
    if len(rows)<READ_THROUGH:
        raise RuntimeError(f"need {READ_THROUGH} rows, got {len(rows)}")
    return rows


def fit_1d_kmeans(values):
    c0,c1=min(values),max(values)
    for _ in range(MAX_KMEANS_ITER):
        g0,g1=[],[]
        for x in values:
            (g0 if abs(x-c0)<=abs(x-c1) else g1).append(x)
        if not g0 or not g1:
            raise RuntimeError("empty cluster")
        n0,n1=sum(g0)/len(g0),sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1
    low,high=min(c0,c1),max(c0,c1)
    return low,high,(low+high)/2


def percentile(vals,p):
    if not vals: return None
    x=sorted(vals)
    if len(x)==1: return x[0]
    pos=(len(x)-1)*p
    lo=math.floor(pos); hi=math.ceil(pos)
    if lo==hi: return x[lo]
    w=pos-lo
    return x[lo]*(1-w)+x[hi]*w


def stats(vals):
    if not vals:
        return {"count":0,"min":None,"max":None,"median":None,"p05":None,"p25":None,"p75":None,"p95":None}
    return {
        "count":len(vals),
        "min":min(vals),
        "max":max(vals),
        "median":statistics.median(vals),
        "p05":percentile(vals,0.05),
        "p25":percentile(vals,0.25),
        "p75":percentile(vals,0.75),
        "p95":percentile(vals,0.95)
    }


def region(x,lo,hi):
    if x<lo: return "BELOW_BAND"
    if x>hi: return "ABOVE_BAND"
    return "IN_BAND"


def temporal_region(p,n):
    d=min(p,n)
    if d<=10: return "NEAR"
    if d<=100: return "INTERMEDIATE"
    return "STABLE_FAR"


def classify_band(n,total):
    frac=(n/total) if total else 0.0
    if n==0: return "RAW_BAND_EMPTY"
    if frac<=0.01: return "RAW_BAND_SPARSE"
    return "RAW_BAND_OCCUPIED"


def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])
    rows=read_rows(CSV)

    cal=rows[:CALIBRATION_ROWS]
    mc_low,mc_high,mc_mid=fit_1d_kmeans([r["mc"] for r in cal])
    tp_low,tp_high,tp_thr=fit_1d_kmeans([r["tp2"] for r in cal])
    band_low=mc_low+ALPHA_LOW*(mc_high-mc_low)
    band_high=mc_low+ALPHA_HIGH*(mc_high-mc_low)

    if abs(mc_mid-2.1490460087555503)>1e-12:
        raise RuntimeError("Motor_current midpoint continuity failed")
    if abs(tp_thr-4.640123582876524)>1e-12:
        raise RuntimeError("TP2 threshold continuity failed")
    if abs(band_low-0.8821033735279131)>1e-12 or abs(band_high-3.4159886439831877)>1e-12:
        raise RuntimeError("Experiment 024 threshold band continuity failed")

    start0=WINDOW_START-1
    stop0=start0+WINDOW_ROWS
    window=rows[start0:stop0]
    context=rows[:stop0+FUTURE_CONTEXT_ROWS]
    transitions=[i for i in range(1,len(context)) if context[i]["dv"]!=context[i-1]["dv"]]

    counts={"BELOW_BAND":0,"IN_BAND":0,"ABOVE_BAND":0}
    temporal_counts={k:{"BELOW_BAND":0,"IN_BAND":0,"ABOVE_BAND":0} for k in ["NEAR","INTERMEDIATE","STABLE_FAR"]}
    temporal_values={k:[] for k in ["NEAR","INTERMEDIATE","STABLE_FAR"]}
    all_values=[]
    ac_values=[]
    ac_counts={"BELOW_BAND":0,"IN_BAND":0,"ABOVE_BAND":0}
    ac_temporal_counts={k:{"BELOW_BAND":0,"IN_BAND":0,"ABOVE_BAND":0} for k in ["NEAR","INTERMEDIATE","STABLE_FAR"]}

    below_candidates=[]
    above_candidates=[]

    for local_i,row in enumerate(window,start=1):
        absolute_i=start0+local_i-1
        pos=bisect.bisect_right(transitions,absolute_i)
        p=absolute_i-transitions[pos-1] if pos else DISTANCE_CAP
        n=transitions[pos]-absolute_i if pos<len(transitions) else DISTANCE_CAP
        p=min(p,DISTANCE_CAP); n=min(n,DISTANCE_CAP)
        treg=temporal_region(p,n)

        x=row["mc"]
        reg=region(x,band_low,band_high)
        counts[reg]+=1
        temporal_counts[treg][reg]+=1
        temporal_values[treg].append(x)
        all_values.append(x)

        if x<band_low:
            below_candidates.append(x)
        elif x>band_high:
            above_candidates.append(x)

        digital="STATE_LOADED" if row["dv"]==1 else "STATE_NOT_LOADED"
        pressure="STATE_LOADED" if row["tp2"]>tp_thr else "STATE_NOT_LOADED"
        if digital==pressure:
            ac_values.append(x)
            ac_counts[reg]+=1
            ac_temporal_counts[treg][reg]+=1

    result={
        "experiment":"NOEPEDIA_EXP_025_RAW_MOTOR_CURRENT_GAP",
        "window":{"start":WINDOW_START,"count":WINDOW_ROWS},
        "calibration":{
            "motor_current_low_centroid":mc_low,
            "motor_current_high_centroid":mc_high,
            "motor_current_midpoint":mc_mid,
            "tp2_threshold":tp_thr
        },
        "frozen_band":{"low":band_low,"high":band_high},
        "all_rows":{
            "counts":counts,
            "in_band_fraction":counts["IN_BAND"]/WINDOW_ROWS,
            "classification":classify_band(counts["IN_BAND"],WINDOW_ROWS),
            "summary":stats(all_values),
            "temporal_counts":temporal_counts,
            "temporal_summary":{k:stats(v) for k,v in temporal_values.items()},
            "closest_below_band":max(below_candidates) if below_candidates else None,
            "closest_above_band":min(above_candidates) if above_candidates else None
        },
        "a_equals_c_subset":{
            "count":len(ac_values),
            "counts":ac_counts,
            "in_band_fraction":ac_counts["IN_BAND"]/len(ac_values) if ac_values else 0.0,
            "classification":classify_band(ac_counts["IN_BAND"],len(ac_values)),
            "summary":stats(ac_values),
            "temporal_counts":ac_temporal_counts
        },
        "claim_boundary":{
            "causality_established":False,
            "fault_established":False,
            "anomaly_established":False,
            "ground_truth_established":False
        }
    }

    RESULT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    print("Experiment 025 reproducibility: PASS")
    print("Experiment 025 scientific class:",result["all_rows"]["classification"])
    return 0


if __name__=="__main__":
    raise SystemExit(main())
