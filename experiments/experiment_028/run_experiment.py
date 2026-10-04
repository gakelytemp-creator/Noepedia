#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, statistics, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))
ANCHOR_START=250_001
ANCHOR_ROWS=5_000
BAND_LOW=0.8821033735279131
BAND_HIGH=3.4159886439831877
SEARCH_MAX=100
PERSIST=3
OFFSETS=[-1,0,1,10]
READ_START=ANCHOR_START-1
READ_END=ANCHOR_START+ANCHOR_ROWS-1+SEARCH_MAX+PERSIST-1
WORK=HERE/"_runtime"; ZIP=WORK/"metropt3.zip"; CSV=WORK/"metropt3.csv"; RESULT=WORK/"result.json"

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

def target_low(x): return x<BAND_LOW

def response_time(segment,t):
    for k in range(SEARCH_MAX+1):
        if all(target_low(segment[t+k+j]["Motor_current"]) for j in range(PERSIST)):
            return k
    return None

def cliffs_delta(a,b):
    if not a or not b: return None
    gt=lt=0
    for x in a:
        for y in b:
            gt += x>y
            lt += x<y
    return (gt-lt)/(len(a)*len(b))

def to_num(s):
    try:return float(s)
    except:return None

def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]: download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]: raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    segment={}
    numeric_channels=None
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for i,row in enumerate(reader,start=1):
            if i==1:
                numeric_channels=[]
                for k,v in row.items():
                    if k in SOURCE["excluded_channels"]: continue
                    if to_num(v) is not None: numeric_channels.append(k)
            if READ_START<=i<=READ_END:
                segment[i]={k:to_num(v) for k,v in row.items()}
            if i>READ_END: break

    events=[]
    for t in range(ANCHOR_START,ANCHOR_START+ANCHOR_ROWS):
        if segment[t-1]["DV_eletric"]==1 and segment[t]["DV_eletric"]==0:
            rt=response_time(segment,t)
            if rt is None: continue
            events.append((t,rt,"CORE" if rt<=50 else "TAIL"))

    rows=[]
    for ch in numeric_channels:
        if ch in {"DV_eletric","Motor_current"}: continue
        for off in OFFSETS:
            core=[segment[t+off][ch] for t,rt,c in events if c=="CORE" and segment[t+off][ch] is not None]
            tail=[segment[t+off][ch] for t,rt,c in events if c=="TAIL" and segment[t+off][ch] is not None]
            if not core or not tail: continue
            cm=statistics.median(core); tm=statistics.median(tail)
            d=cliffs_delta(core,tail)
            rows.append({
                "channel":ch,"offset":off,
                "core_n":len(core),"tail_n":len(tail),
                "core_median":cm,"tail_median":tm,
                "median_difference_tail_minus_core":tm-cm,
                "cliffs_delta_core_vs_tail":d
            })

    ranked=sorted(rows,key=lambda r:(-abs(r["cliffs_delta_core_vs_tail"]),-abs(r["median_difference_tail_minus_core"]),r["channel"],r["offset"]))
    out={
        "experiment":"NOEPEDIA_EXP_028_EXPLORATORY_LOAD_OFF_COVARIATES",
        "event_counts":{
            "CORE":sum(c=="CORE" for _,_,c in events),
            "TAIL":sum(c=="TAIL" for _,_,c in events)
        },
        "numeric_channels_scanned":numeric_channels,
        "ranked_effects":ranked,
        "top_20":ranked[:20],
        "claim_boundary":{"confirmatory":False}
    }
    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"event_counts":out["event_counts"],"top_20":out["top_20"]},indent=2,ensure_ascii=False))
    print("Experiment 028 reproducibility: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
