#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, math, statistics, urllib.request, zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
RESULT=WORK/"result.json"

WINDOWS=SOURCE["windows"]
LANDMARKS=SOURCE["row_response_landmarks"]


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
        m=[n for n in z.namelist() if Path(n).name==basename]
        if len(m)!=1:
            raise RuntimeError(f"expected one member, got {m}")
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


def parse_ts(s):
    s=s.strip()
    fmts=[
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y %H:%M:%S.%f",
        "%m/%d/%Y %H:%M:%S"
    ]
    for fmt in fmts:
        try:return datetime.strptime(s,fmt)
        except ValueError:pass
    try:return datetime.fromisoformat(s)
    except Exception as e:raise RuntimeError(f"cannot parse timestamp: {s}") from e


def cadence_class(dts):
    pos=[x for x in dts if x>0]
    if not pos:return "VARIABLE_CADENCE"
    if max(pos)==min(pos):return "UNIFORM_CADENCE"
    med=statistics.median(pos)
    if med!=0 and (max(pos)-min(pos))<=0.01*med:
        return "NEAR_UNIFORM_CADENCE"
    return "VARIABLE_CADENCE"


def summarize(dts):
    pos=[x for x in dts if x>0]
    med=statistics.median(pos) if pos else None
    c=Counter(dts)
    return {
        "interval_count":len(dts),
        "positive_interval_count":len(pos),
        "nonpositive_count":sum(x<=0 for x in dts),
        "min_dt_seconds":min(pos) if pos else None,
        "max_dt_seconds":max(pos) if pos else None,
        "mean_dt_seconds":sum(pos)/len(pos) if pos else None,
        "median_dt_seconds":med,
        "p05":percentile(pos,.05),
        "p25":percentile(pos,.25),
        "p75":percentile(pos,.75),
        "p95":percentile(pos,.95),
        "unique_dt_counts":{str(k):v for k,v in sorted(c.items())},
        "gaps_gt_2x_median":sum(x>2*med for x in pos) if med else None,
        "cadence_class":cadence_class(dts)
    }


def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    max_end=max(v["start"]+v["count"]-1 for v in WINDOWS.values())
    ts_by_index={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        if "timestamp" not in (reader.fieldnames or []):
            raise RuntimeError("timestamp column missing")
        for i,row in enumerate(reader,start=1):
            if any(v["start"]<=i<=v["start"]+v["count"]-1 for v in WINDOWS.values()):
                ts_by_index[i]=parse_ts(row["timestamp"])
            if i>max_end:break

    output={
        "experiment":"NOEPEDIA_EXP_031_TIMESTAMP_CADENCE",
        "windows":{},
        "physical_time_conversion":{}
    }

    medians=[]
    for name,w in WINDOWS.items():
        start=w["start"];count=w["count"]
        stamps=[ts_by_index[i] for i in range(start,start+count)]
        dts=[(stamps[i+1]-stamps[i]).total_seconds() for i in range(len(stamps)-1)]
        s=summarize(dts)
        output["windows"][name]=s
        medians.append(s["median_dt_seconds"])

    output["cross_window_cadence_class"]=(
        "CROSS_WINDOW_CADENCE_MATCH"
        if len(set(medians))==1 else
        "CROSS_WINDOW_CADENCE_DIFFERS"
    )

    for name in ["W027","W030"]:
        med=output["windows"][name]["median_dt_seconds"]
        output["physical_time_conversion"][name]={
            f"{rows}_rows_seconds":rows*med for rows in LANDMARKS
        }

    RESULT.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(output,indent=2,ensure_ascii=False))
    print("Experiment 031 reproducibility: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
