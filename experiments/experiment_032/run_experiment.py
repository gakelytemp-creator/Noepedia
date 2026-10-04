#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,json,math,statistics,urllib.request,zipfile
from datetime import datetime
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

BAND_LOW=0.8821033735279131
SEARCH_MAX=100
PERSIST=3
GAP=20
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

def parse_ts(s):
    s=s.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S.%f","%Y-%m-%d %H:%M:%S","%m/%d/%Y %H:%M:%S.%f","%m/%d/%Y %H:%M:%S"):
        try:return datetime.strptime(s,fmt)
        except ValueError:pass
    return datetime.fromisoformat(s)

def percentile(vals,p):
    if not vals:return None
    x=sorted(vals)
    if len(x)==1:return x[0]
    pos=(len(x)-1)*p
    lo=math.floor(pos);hi=math.ceil(pos)
    if lo==hi:return x[lo]
    w=pos-lo
    return x[lo]*(1-w)+x[hi]*w

def hist(vals):
    out={"0-300":0,"301-450":0,"451-600":0,"601-1200":0,">1200":0}
    for v in vals:
        if v<=300:out["0-300"]+=1
        elif v<=450:out["301-450"]+=1
        elif v<=600:out["451-600"]+=1
        elif v<=1200:out["601-1200"]+=1
        else:out[">1200"]+=1
    return out

def stats(vals):
    if not vals:return {"count":0}
    return {
        "count":len(vals),"min":min(vals),"mean":sum(vals)/len(vals),
        "median":statistics.median(vals),"p25":percentile(vals,.25),
        "p75":percentile(vals,.75),"p90":percentile(vals,.90),
        "p95":percentile(vals,.95),"max":max(vals),"histogram":hist(vals)
    }

def response_time(seg,t):
    for k in range(SEARCH_MAX+1):
        if all(seg[t+k+j]["mc"]<BAND_LOW for j in range(PERSIST)):
            return k
    return None

def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    max_end=max(v["start"]+v["count"]-1+SEARCH_MAX+PERSIST for v in SOURCE["windows"].values())
    min_start=min(v["start"]-1 for v in SOURCE["windows"].values())
    seg={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for i,row in enumerate(reader,start=1):
            if min_start<=i<=max_end:
                seg[i]={"dv":int(float(row["DV_eletric"])),"mc":float(row["Motor_current"]),"ts":parse_ts(row["timestamp"])}
            if i>max_end:break

    output={"experiment":"NOEPEDIA_EXP_032_EVENTWISE_PHYSICAL_TIME","windows":{}}
    combined=[];combined_gapfree=[]

    for name,w in SOURCE["windows"].items():
        vals=[];gapfree=[];gapcross=0;events=[]
        for t in range(w["start"],w["start"]+w["count"]):
            if not(seg[t-1]["dv"]==1 and seg[t]["dv"]==0):continue
            k=response_time(seg,t)
            if k is None:continue
            seconds=(seg[t+k]["ts"]-seg[t]["ts"]).total_seconds()
            crosses=False
            for i in range(t,t+k):
                dt=(seg[i+1]["ts"]-seg[i]["ts"]).total_seconds()
                if dt>GAP:
                    crosses=True;break
            vals.append(seconds)
            combined.append(seconds)
            if crosses:
                gapcross+=1
            else:
                gapfree.append(seconds);combined_gapfree.append(seconds)
            events.append({"anchor":t,"response_rows":k,"physical_seconds":seconds,"crosses_large_gap":crosses})
        output["windows"][name]={
            "all":stats(vals),"gap_free":stats(gapfree),
            "gap_crossing_count":gapcross,"events":events
        }

    output["combined"]={"all":stats(combined),"gap_free":stats(combined_gapfree)}
    m27=output["windows"]["W027"]["gap_free"].get("median")
    m30=output["windows"]["W030"]["gap_free"].get("median")
    ok=(m27 is not None and m30 is not None and 360<=m27<=480 and 360<=m30<=480 and abs(m27-m30)<=60)
    output["replication"]="PHYSICAL_TIME_CLUSTER_REPLICATED" if ok else "PHYSICAL_TIME_CLUSTER_NOT_REPLICATED"

    RESULT.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="windows"},indent=2,ensure_ascii=False))
    print(json.dumps({
        "W027_summary":{k:v for k,v in output["windows"]["W027"].items() if k!="events"},
        "W030_summary":{k:v for k,v in output["windows"]["W030"].items() if k!="events"}
    },indent=2,ensure_ascii=False))
    print("Experiment 032 reproducibility: PASS")
    print("Experiment 032 result:",output["replication"])
    return 0

if __name__=="__main__":
    raise SystemExit(main())
