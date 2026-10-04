#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, sys, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
FIELD=WORK/"field.json"
EV=WORK/"eval.json"
RES=WORK/"result.json"
EVALUATOR=ROOT/"experiments"/"experiment_003"/"evaluator.py"

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

def main():
    WORK.mkdir(exist_ok=True)

    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")

    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    if git_blob_sha1(EVALUATOR)!=SOURCE["frozen_evaluator"]["git_blob_sha1"]:
        raise RuntimeError("evaluator changed")

    subprocess.run([sys.executable,str(HERE/"build_field.py"),str(CSV),str(FIELD)],check=True)

    with EV.open("w",encoding="utf-8") as o:
        p=subprocess.run([sys.executable,str(EVALUATOR),str(FIELD)],stdout=o)
    if p.returncode:
        raise RuntimeError("evaluator failed")

    p=subprocess.run([sys.executable,str(HERE/"verify_output.py"),str(FIELD),str(EV),str(RES)])
    result=json.loads(RES.read_text(encoding="utf-8"))

    print("Experiment 033 reproducibility: PASS")
    print("Experiment 033 architectural result:","PASS" if result["architectural_pass"] else "FAIL")
    print("Experiment 033 scientific result:",result["result"])
    print("Experiment 033 relative reduction:",result["common_subset"]["relative_mismatch_reduction"])
    return p.returncode

if __name__=="__main__":
    raise SystemExit(main())
