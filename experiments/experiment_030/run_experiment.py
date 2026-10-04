#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, math, statistics, urllib.request, zipfile
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

START=350_001
COUNT=5_000
SEARCH_MAX=100
PERSIST=3
BAND_LOW=0.8821033735279131
BAND_HIGH=3.4159886439831877
READ_START=START-1
READ_END=START+COUNT-1+SEARCH_MAX+PERSIST-1

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
RESULT=WORK/"result.json"


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


def percentile(vals,p):
    if not vals:return None
    x=sorted(vals)
    if len(x)==1:return x[0]
    pos=(len(x)-1)*p
    lo=math.floor(pos);hi=math.ceil(pos)
    if lo==hi:return x[lo]
    w=pos-lo
    return x[lo]*(1-w)+x[hi]*w


def hist_bin(k):
    if k==0:return "0"
    if k==1:return "1"
    if k<=5:return "2-5"
    if k<=10:return "6-10"
    if k<=25:return "11-25"
    if k<=50:return "26-50"
    return "51-100"


def target_ok(cls,x):
    return x>BAND_HIGH if cls=="LOAD_ON" else x<BAND_LOW


def summarize(resolved,censored,already_pre,already_t0,event_count):
    h=Counter(hist_bin(k) for k in resolved)
    if censored:h[">100"]+=censored
    return {
        "event_count":event_count,
        "resolved_count":len(resolved),
        "censored_count":censored,
        "already_target_t_minus_1":already_pre,
        "already_target_t0":already_t0,
        "min":min(resolved) if resolved else None,
        "mean":sum(resolved)/len(resolved) if resolved else None,
        "median":statistics.median(resolved) if resolved else None,
        "p25":percentile(resolved,.25),
        "p75":percentile(resolved,.75),
        "p90":percentile(resolved,.90),
        "p95":percentile(resolved,.95),
        "max":max(resolved) if resolved else None,
        "histogram":{k:h.get(k,0) for k in ["0","1","2-5","6-10","11-25","26-50","51-100",">100"]}
    }


def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    seg={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for i,row in enumerate(reader,start=1):
            if READ_START<=i<=READ_END:
                seg[i]={
                    "dv":int(float(row["DV_eletric"])),
                    "mc":float(row["Motor_current"])
                }
            if i>READ_END:break

    output={
        "experiment":"NOEPEDIA_EXP_030_DIRECTIONAL_RESPONSE_REPLICATION",
        "window":{"start":START,"count":COUNT},
        "response_rule":{
            "band_low":BAND_LOW,
            "band_high":BAND_HIGH,
            "search":[0,SEARCH_MAX],
            "persistence_rows":PERSIST
        },
        "classes":{}
    }

    for cls in ["LOAD_ON","LOAD_OFF"]:
        anchors=[]
        for t in range(START,START+COUNT):
            a,b=seg[t-1]["dv"],seg[t]["dv"]
            if cls=="LOAD_ON" and (a,b)==(0,1):anchors.append(t)
            if cls=="LOAD_OFF" and (a,b)==(1,0):anchors.append(t)

        resolved=[];censored=0;already_pre=0;already_t0=0
        for t in anchors:
            already_pre+=int(target_ok(cls,seg[t-1]["mc"]))
            already_t0+=int(target_ok(cls,seg[t]["mc"]))
            rt=None
            for k in range(SEARCH_MAX+1):
                if all(target_ok(cls,seg[t+k+j]["mc"]) for j in range(PERSIST)):
                    rt=k;break
            if rt is None:censored+=1
            else:resolved.append(rt)

        output["classes"][cls]=summarize(resolved,censored,already_pre,already_t0,len(anchors))

    on=output["classes"]["LOAD_ON"]
    off=output["classes"]["LOAD_OFF"]

    on_zero_fraction=(on["histogram"]["0"]/on["resolved_count"]) if on["resolved_count"] else 0.0
    off_26_50_fraction=(off["histogram"]["26-50"]/off["resolved_count"]) if off["resolved_count"] else 0.0

    on_pass=(on["median"]==0 and on_zero_fraction>=0.90) if on["resolved_count"] else False
    off_pass=(
        off["median"] is not None and
        26<=off["median"]<=50 and
        off_26_50_fraction>=0.75
    ) if off["resolved_count"] else False

    if on_pass and off_pass:
        overall="DIRECTIONAL_ASYMMETRY_REPLICATED"
    elif on_pass or off_pass:
        overall="PARTIAL_REPLICATION"
    else:
        overall="NOT_REPLICATED"

    output["replication"]={
        "load_on_zero_fraction":on_zero_fraction,
        "load_on_result":"LOAD_ON_IMMEDIATE_REPLICATED" if on_pass else "LOAD_ON_NOT_REPLICATED",
        "load_off_26_50_fraction":off_26_50_fraction,
        "load_off_result":"LOAD_OFF_DELAY_REPLICATED" if off_pass else "LOAD_OFF_NOT_REPLICATED",
        "overall":overall
    }

    RESULT.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(output,indent=2,ensure_ascii=False))
    print("Experiment 030 reproducibility: PASS")
    print("Experiment 030 result:",overall)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
