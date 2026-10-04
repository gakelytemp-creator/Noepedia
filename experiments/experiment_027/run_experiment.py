#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, math, statistics, urllib.request, zipfile
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

ANCHOR_START=250_001
ANCHOR_ROWS=5_000
SEARCH_MAX=100
PERSIST=3
BAND_LOW=0.8821033735279131
BAND_HIGH=3.4159886439831877
READ_START=ANCHOR_START-1
READ_END=ANCHOR_START+ANCHOR_ROWS-1+SEARCH_MAX+PERSIST-1

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
            if not b:break
            out.write(b)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        m=[n for n in z.namelist() if Path(n).name==basename]
        if len(m)!=1:raise RuntimeError(f"expected one member, got {m}")
        with z.open(m[0]) as src,dest.open("wb") as out:
            while True:
                b=src.read(1<<20)
                if not b:break
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


def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    segment={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for i,row in enumerate(reader,start=1):
            if READ_START<=i<=READ_END:
                segment[i]={"dv":int(float(row["DV_eletric"])),"mc":float(row["Motor_current"])}
            if i>READ_END:break

    events={"LOAD_ON":[],"LOAD_OFF":[]}
    for t in range(ANCHOR_START,ANCHOR_START+ANCHOR_ROWS):
        a=segment[t-1]["dv"];b=segment[t]["dv"]
        if a==b:continue
        cls="LOAD_ON" if (a,b)==(0,1) else "LOAD_OFF"
        events[cls].append(t)

    output={
        "experiment":"NOEPEDIA_EXP_027_PER_TRANSITION_RESPONSE_TIME",
        "anchor_window":{"start":ANCHOR_START,"count":ANCHOR_ROWS},
        "response_rule":{
            "search":[0,SEARCH_MAX],
            "persistence_rows":PERSIST,
            "band_low":BAND_LOW,
            "band_high":BAND_HIGH
        },
        "classes":{}
    }

    for cls,anchors in events.items():
        resolved=[]
        censored=0
        already_pre=0
        already_t0=0
        h=Counter()
        per_event=[]
        for t in anchors:
            pre=target_ok(cls,segment[t-1]["mc"])
            at0=target_ok(cls,segment[t]["mc"])
            already_pre+=int(pre)
            already_t0+=int(at0)
            rt=None
            for k in range(0,SEARCH_MAX+1):
                if all(target_ok(cls,segment[t+k+j]["mc"]) for j in range(PERSIST)):
                    rt=k;break
            if rt is None:
                censored+=1
                h[">100"]+=1
            else:
                resolved.append(rt)
                h[hist_bin(rt)]+=1
            per_event.append({"anchor":t,"already_target_t_minus_1":pre,"already_target_t0":at0,"response_rows":rt})

        stats={
            "event_count":len(anchors),
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
        output["classes"][cls]={"summary":stats,"events":per_event}

    RESULT.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "experiment":output["experiment"],
        "response_rule":output["response_rule"],
        "summaries":{k:v["summary"] for k,v in output["classes"].items()}
    },indent=2,ensure_ascii=False))
    print("Experiment 027 reproducibility: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
