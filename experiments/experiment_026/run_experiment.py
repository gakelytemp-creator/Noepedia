#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, math, statistics, sys, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

CALIBRATION_ROWS=50_000
ANCHOR_START=250_001
ANCHOR_ROWS=5_000
KMIN=-100
KMAX=100
READ_START=ANCHOR_START+KMIN
READ_END=ANCHOR_START+ANCHOR_ROWS-1+KMAX
MAX_KMEANS_ITER=100

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
RESULT=WORK/"result.json"

LANDMARKS=[-100,-50,-25,-10,-5,-1,0,1,5,10,25,50,100]


def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()


def download(url,dest):
    with urllib.request.urlopen(url,timeout=120) as r,dest.open("wb") as out:
        while True:
            b=r.read(1<<20)
            if not b: break
            out.write(b)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        m=[n for n in z.namelist() if Path(n).name==basename]
        if len(m)!=1: raise RuntimeError(f"expected one member, got {m}")
        with z.open(m[0]) as src,dest.open("wb") as out:
            while True:
                b=src.read(1<<20)
                if not b: break
                out.write(b)


def fit_1d_kmeans(vals):
    c0,c1=min(vals),max(vals)
    for _ in range(MAX_KMEANS_ITER):
        g0,g1=[],[]
        for x in vals: (g0 if abs(x-c0)<=abs(x-c1) else g1).append(x)
        n0,n1=sum(g0)/len(g0),sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1; break
        c0,c1=n0,n1
    lo,hi=min(c0,c1),max(c0,c1)
    return lo,hi,(lo+hi)/2


def percentile(vals,p):
    if not vals:return None
    x=sorted(vals)
    if len(x)==1:return x[0]
    pos=(len(x)-1)*p
    lo=math.floor(pos);hi=math.ceil(pos)
    if lo==hi:return x[lo]
    w=pos-lo
    return x[lo]*(1-w)+x[hi]*w


def summary(vals):
    if not vals:
        return {"count":0,"mean":None,"median":None,"p05":None,"p25":None,"p75":None,"p95":None}
    return {
        "count":len(vals),
        "mean":sum(vals)/len(vals),
        "median":statistics.median(vals),
        "p05":percentile(vals,.05),
        "p25":percentile(vals,.25),
        "p75":percentile(vals,.75),
        "p95":percentile(vals,.95)
    }


def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]: raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    calibration=[]
    segment={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for i,row in enumerate(reader,start=1):
            if i<=CALIBRATION_ROWS:
                calibration.append((float(row["Motor_current"]),float(row["TP2"])))
            if READ_START-1 <= i <= READ_END:
                segment[i]={
                    "dv":int(float(row["DV_eletric"])),
                    "mc":float(row["Motor_current"]),
                    "tp2":float(row["TP2"])
                }
            if i>READ_END: break

    if len(calibration)!=CALIBRATION_ROWS: raise RuntimeError("calibration incomplete")
    mc_lo,mc_hi,mc_mid=fit_1d_kmeans([x[0] for x in calibration])
    _,_,tp_mid=fit_1d_kmeans([x[1] for x in calibration])
    band_lo=mc_lo+.2*(mc_hi-mc_lo); band_hi=mc_lo+.8*(mc_hi-mc_lo)
    if abs(mc_mid-2.1490460087555503)>1e-12: raise RuntimeError("MC calibration changed")
    if abs(tp_mid-4.640123582876524)>1e-12: raise RuntimeError("TP2 calibration changed")
    if abs(band_lo-0.8821033735279131)>1e-12 or abs(band_hi-3.4159886439831877)>1e-12:
        raise RuntimeError("band continuity failed")

    events={"LOAD_ON":[],"LOAD_OFF":[]}
    for t in range(ANCHOR_START,ANCHOR_START+ANCHOR_ROWS):
        prev=segment[t-1]["dv"]; cur=segment[t]["dv"]
        if prev==cur: continue
        cls="LOAD_ON" if (prev,cur)==(0,1) else "LOAD_OFF"
        events[cls].append(t)

    out={
        "experiment":"NOEPEDIA_EXP_026_EVENT_ALIGNED_RAW_TRAJECTORIES",
        "anchor_window":{"start":ANCHOR_START,"count":ANCHOR_ROWS},
        "offsets":{"min":KMIN,"max":KMAX},
        "reference_band":{"low":band_lo,"high":band_hi},
        "event_counts":{k:len(v) for k,v in events.items()},
        "trajectories":{},
        "landmarks":{}
    }

    for cls,anchors in events.items():
        mc_curve={};tp_curve={}
        for k in range(KMIN,KMAX+1):
            mc=[segment[t+k]["mc"] for t in anchors]
            tp=[segment[t+k]["tp2"] for t in anchors]
            mc_curve[str(k)]=summary(mc)
            tp_curve[str(k)]=summary(tp)
        out["trajectories"][cls]={"Motor_current":mc_curve,"TP2":tp_curve}
        out["landmarks"][cls]={
            str(k):{
                "Motor_current":mc_curve[str(k)],
                "TP2":tp_curve[str(k)]
            } for k in LANDMARKS
        }

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "experiment":out["experiment"],
        "event_counts":out["event_counts"],
        "reference_band":out["reference_band"],
        "landmarks":out["landmarks"]
    },indent=2,ensure_ascii=False))
    print("Experiment 026 reproducibility: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
