#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, subprocess, sys, urllib.request, zipfile
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

START=450_001
N=5_000
HISTORY=101
FUTURE=101
READ_START=START-HISTORY
READ_END=START+N-1+FUTURE
LOW=0.8821033735279131
HIGH=3.4159886439831877

S_HIGH="CURRENT_HIGH"
S_LOW="CURRENT_LOW"
S_MID="CURRENT_MID_UNRESOLVED"
RULE_NEW="RULE033_REVISED_LOAD_OFF_RUNON"

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
FIELD=WORK/"field.json"
EV=WORK/"eval.json"
RESULT=WORK/"result.json"
EVALUATOR=ROOT/"experiments"/"experiment_003"/"evaluator.py"
BUILD033=ROOT/"experiments"/"experiment_033"/"build_field.py"


def sha256_file(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def git_blob_sha1(p):
    d=p.read_bytes()
    return hashlib.sha1(f"blob {len(d)}\0".encode("utf-8")+d).hexdigest()


def download(url,dest):
    with urllib.request.urlopen(url,timeout=120) as r,dest.open("wb") as o:
        while True:
            b=r.read(1<<20)
            if not b:
                break
            o.write(b)


def extract_member(zp,dest,basename):
    with zipfile.ZipFile(zp) as z:
        m=[n for n in z.namelist() if Path(n).name==basename]
        if len(m)!=1:
            raise RuntimeError(m)
        with z.open(m[0]) as s,dest.open("wb") as o:
            while True:
                b=s.read(1<<20)
                if not b:
                    break
                o.write(b)


def current_state(x):
    if x<LOW:
        return S_LOW
    if x>HIGH:
        return S_HIGH
    return S_MID


def since_bin(d):
    if d is None or d>100:
        return ">100_or_none"
    if d<=40:
        return "0-40"
    if d<=52:
        return "41-52"
    return "53-100"


def next_bin(d):
    if d is None or d>100:
        return ">100_or_none"
    if d<=10:
        return "0-10"
    if d<=50:
        return "11-50"
    return "51-100"


def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])
    if git_blob_sha1(EVALUATOR)!=SOURCE["frozen_evaluator"]["git_blob_sha1"]:
        raise RuntimeError("evaluator changed")

    subprocess.run([sys.executable,str(BUILD033),str(CSV),str(FIELD)],check=True)
    with EV.open("w",encoding="utf-8") as o:
        p=subprocess.run([sys.executable,str(EVALUATOR),str(FIELD)],stdout=o)
    if p.returncode:
        raise RuntimeError("evaluator failed")

    field=json.loads(FIELD.read_text(encoding="utf-8"))
    ev=json.loads(EV.read_text(encoding="utf-8"))

    residual_subjects=[]
    expected={}
    observed={}
    for r in field["relations"]:
        if r["predicate"]=="REVISED_EXPECTED_CURRENT_STATE":
            expected[r["subject"]]=r["object"]
        elif r["predicate"]=="CURRENT_CANDIDATE_STATE":
            observed[r["subject"]]=r["object"]

    for e in ev.get("events",[]):
        if e.get("rule")==RULE_NEW and e.get("event")=="FORMAL_MISMATCH":
            residual_subjects.append(e["subject"])

    rows={}
    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
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

    load_offs=[]
    load_ons=[]
    transitions=[]
    for i in range(READ_START+1,READ_END+1):
        a=rows[i-1]["dv"]; b=rows[i]["dv"]
        if a!=b:
            transitions.append(i)
            if (a,b)==(1,0):
                load_offs.append(i)
            elif (a,b)==(0,1):
                load_ons.append(i)

    def prev_dist(points,t):
        pts=[x for x in points if x<=t]
        return t-max(pts) if pts else None

    def next_dist(points,t):
        pts=[x for x in points if x>t]
        return min(pts)-t if pts else None

    residuals=[]
    signatures=Counter()

    for subject in residual_subjects:
        local=int(subject.split("_")[-1])
        t=START+local-1
        d_off=prev_dist(load_offs,t)
        d_on=prev_dist(load_ons,t)
        d_next=next_dist(transitions,t)
        sig={
            "expected":expected.get(subject),
            "observed":observed.get(subject),
            "dv":rows[t]["dv"],
            "since_load_off_bin":since_bin(d_off),
            "next_transition_bin":next_bin(d_next)
        }
        sig_key=json.dumps(sig,sort_keys=True)
        signatures[sig_key]+=1

        context=[]
        for k in range(-5,6):
            rr=rows[t+k]
            context.append({
                "offset":k,
                "source_row":t+k,
                "DV_eletric":rr["dv"],
                "Motor_current":rr["mc"],
                "TP2":rr["tp2"],
                "TP3":rr["tp3"]
            })

        residuals.append({
            "assessment":subject,
            "source_data_row":t,
            "timestamp":rows[t]["timestamp"],
            "DV_eletric":rows[t]["dv"],
            "Motor_current":rows[t]["mc"],
            "observed_current_state":current_state(rows[t]["mc"]),
            "revised_expected_state":expected.get(subject),
            "rows_since_last_LOAD_OFF":d_off,
            "rows_since_last_LOAD_ON":d_on,
            "rows_until_next_DV_transition":d_next,
            "TP2":rows[t]["tp2"],
            "TP3":rows[t]["tp3"],
            "signature":sig,
            "local_context":context
        })

    signature_list=[
        {"signature":json.loads(k),"count":v}
        for k,v in sorted(signatures.items(),key=lambda kv:(-kv[1],kv[0]))
    ]

    if not residuals:
        klass="NO_RESIDUALS"
    elif len(signature_list)==1:
        klass="SINGLE_RESIDUAL_PATTERN"
    else:
        klass="MULTIPLE_RESIDUAL_PATTERNS"

    out={
        "experiment":"NOEPEDIA_EXP_034_RESIDUAL_MISMATCH_AUTOPSY",
        "window":{"start":START,"count":N},
        "residual_count":len(residuals),
        "classification":klass,
        "signature_count":len(signature_list),
        "signatures":signature_list,
        "residuals":residuals,
        "claim_boundary":{
            "new_rule_introduced":False,
            "fault_established":False,
            "anomaly_established":False,
            "causality_established":False
        }
    }

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "experiment":out["experiment"],
        "residual_count":out["residual_count"],
        "classification":out["classification"],
        "signature_count":out["signature_count"],
        "signatures":out["signatures"],
        "residuals":[{k:v for k,v in r.items() if k!="local_context"} for r in residuals]
    },indent=2,ensure_ascii=False))
    print("Experiment 034 reproducibility: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
