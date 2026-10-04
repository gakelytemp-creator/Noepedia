#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, statistics, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

START=300_001
COUNT=5_000
SEARCH_MAX=100
PERSIST=3
BAND_LOW=0.8821033735279131
OFFSET=10
READ_START=START-1
READ_END=START+COUNT-1+SEARCH_MAX+PERSIST-1
WORK=HERE/"_runtime"; ZIP=WORK/"metropt3.zip"; CSV=WORK/"metropt3.csv"; RESULT=WORK/"result.json"

def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
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

def response_time(seg,t):
    for k in range(SEARCH_MAX+1):
        if all(seg[t+k+j]["Motor_current"]<BAND_LOW for j in range(PERSIST)):
            return k
    return None

def cliffs_delta(core,tail):
    gt=lt=0
    for x in core:
        for y in tail:
            gt+=x>y;lt+=x<y
    return (gt-lt)/(len(core)*len(tail))

def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    seg={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        if "TP3" not in (reader.fieldnames or []):raise RuntimeError("TP3 missing")
        for i,row in enumerate(reader,start=1):
            if READ_START<=i<=READ_END:
                seg[i]={
                    "DV_eletric":int(float(row["DV_eletric"])),
                    "Motor_current":float(row["Motor_current"]),
                    "TP3":float(row["TP3"])
                }
            if i>READ_END:break

    core=[];tail=[];censored=0;resolved=[]
    for t in range(START,START+COUNT):
        if not(seg[t-1]["DV_eletric"]==1 and seg[t]["DV_eletric"]==0):continue
        rt=response_time(seg,t)
        if rt is None:
            censored+=1
            continue
        val=seg[t+OFFSET]["TP3"]
        resolved.append({"anchor":t,"response_rows":rt,"TP3_plus10":val})
        (core if rt<=50 else tail).append(val)

    if len(tail)<3:
        klass="NOT_EVALUABLE_FOR_CLASS_CONFIRMATION"
        delta=None
    else:
        delta=cliffs_delta(core,tail)
        direction=statistics.median(core)>statistics.median(tail) and delta>0
        klass="STRONG_EFFECT_REPLICATED" if direction and delta>=0.5 else ("DIRECTION_REPLICATED" if direction else "NOT_REPLICATED")

    out={
        "experiment":"NOEPEDIA_EXP_029_TP3_PLUS10_CONFIRMATION",
        "window":{"start":START,"count":COUNT},
        "load_off_events_total":len(resolved)+censored,
        "resolved_count":len(resolved),
        "censored_count":censored,
        "core_count":len(core),
        "tail_count":len(tail),
        "core_median":statistics.median(core) if core else None,
        "tail_median":statistics.median(tail) if tail else None,
        "median_difference_tail_minus_core":(statistics.median(tail)-statistics.median(core)) if core and tail else None,
        "cliffs_delta_core_vs_tail":delta,
        "result_class":klass,
        "events":resolved,
        "claim_boundary":{"causality":False,"mechanism":False}
    }
    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in out.items() if k!="events"},indent=2,ensure_ascii=False))
    print("Experiment 029 reproducibility: PASS")
    print("Experiment 029 result:",klass)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
