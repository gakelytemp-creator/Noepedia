#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, statistics, urllib.request, zipfile
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

START=500_001
COUNT=5_000
HISTORY=6
READ_START=START-HISTORY
READ_END=START+COUNT-1
HIGH=3.4159886439831877

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
RESULT=WORK/"result.json"


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
            if not b:
                break
            out.write(b)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        m=[n for n in z.namelist() if Path(n).name==basename]
        if len(m)!=1:
            raise RuntimeError(f"expected one member, got {m}")
        with z.open(m[0]) as src,dest.open("wb") as out:
            while True:
                b=src.read(1<<20)
                if not b:
                    break
                out.write(b)


def main():
    WORK.mkdir(exist_ok=True)

    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")

    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    rows={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        required={"DV_eletric","Motor_current","TP2","TP3","timestamp"}
        missing=required-set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing columns: {sorted(missing)}")

        for i,row in enumerate(reader,start=1):
            if READ_START<=i<=READ_END:
                rows[i]={
                    "timestamp":row["timestamp"],
                    "dv":int(float(row["DV_eletric"])),
                    "mc":float(row["Motor_current"]),
                    "tp2":float(row["TP2"]),
                    "tp3":float(row["TP3"])
                }
            if i>READ_END:
                break

    events=[]
    hist=Counter()

    for t in range(START,START+COUNT):
        if not (rows[t-1]["dv"]==0 and rows[t]["dv"]==1):
            continue

        pre_high_offsets=[k for k in range(-6,0) if rows[t+k]["mc"]>HIGH]
        earliest=min(pre_high_offsets) if pre_high_offsets else None

        consecutive=0
        for k in range(-1,-7,-1):
            if rows[t+k]["mc"]>HIGH:
                consecutive+=1
            else:
                break

        if earliest is None:
            hist["NO_PRE_HIGH"]+=1
        else:
            hist[str(earliest)]+=1

        events.append({
            "anchor":t,
            "timestamp":rows[t]["timestamp"],
            "earliest_pre_high_offset":earliest,
            "consecutive_high_rows_immediately_before_t":consecutive,
            "high_at_t0":rows[t]["mc"]>HIGH,
            "motor_current_t_minus_1":rows[t-1]["mc"],
            "motor_current_t0":rows[t]["mc"],
            "tp2_t_minus_1":rows[t-1]["tp2"],
            "tp2_t0":rows[t]["tp2"],
            "tp3_t_minus_1":rows[t-1]["tp3"],
            "tp3_t0":rows[t]["tp3"]
        })

    total=len(events)
    with_pre=sum(e["earliest_pre_high_offset"] is not None for e in events)
    frac=(with_pre/total) if total else 0.0
    high_t0=sum(e["high_at_t0"] for e in events)

    if frac>=0.5:
        klass="PRE_LOAD_ON_PATTERN_REPLICATED"
    elif frac>0:
        klass="PRE_LOAD_ON_PATTERN_WEAK"
    else:
        klass="PRE_LOAD_ON_PATTERN_NOT_REPLICATED"

    consecutive_vals=[
        e["consecutive_high_rows_immediately_before_t"]
        for e in events
        if e["earliest_pre_high_offset"] is not None
    ]

    out={
        "experiment":"NOEPEDIA_EXP_035_PRE_LOAD_ON_REPLICATION",
        "window":{"start":START,"count":COUNT},
        "load_on_event_count":total,
        "events_with_pre_high":with_pre,
        "pre_high_fraction":frac,
        "earliest_pre_high_histogram":{
            k:hist.get(k,0)
            for k in ["-6","-5","-4","-3","-2","-1","NO_PRE_HIGH"]
        },
        "high_at_t0_count":high_t0,
        "high_at_t0_fraction":(high_t0/total) if total else 0.0,
        "consecutive_pre_high_rows":{
            "count":len(consecutive_vals),
            "min":min(consecutive_vals) if consecutive_vals else None,
            "median":statistics.median(consecutive_vals) if consecutive_vals else None,
            "max":max(consecutive_vals) if consecutive_vals else None
        },
        "result_class":klass,
        "events":events,
        "claim_boundary":{
            "causal_precedence_established":False,
            "controller_mechanism_established":False,
            "sensor_delay_established":False,
            "rule_modified":False
        }
    }

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    print(json.dumps({
        k:v for k,v in out.items()
        if k!="events"
    },indent=2,ensure_ascii=False))
    print("Experiment 035 reproducibility: PASS")
    print("Experiment 035 result:",klass)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
