#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))
WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
FIELD=WORK/"field_input.json"
RESULT=WORK/"evaluator_result.json"
THRESH=WORK/"threshold_result.json"
AUDIT=WORK/"audit.json"
EVALUATOR=ROOT/"experiments"/"experiment_003"/"evaluator.py"


def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def git_blob_sha1(path):
    data=path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8")+data).hexdigest()


def download(url,dest):
    with urllib.request.urlopen(url,timeout=120) as response,dest.open("wb") as out:
        while True:
            block=response.read(1<<20)
            if not block:break
            out.write(block)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        matches=[n for n in z.namelist() if Path(n).name==basename]
        if len(matches)!=1:
            raise RuntimeError(f"expected one CSV member named {basename}, found {matches}")
        with z.open(matches[0]) as src,dest.open("wb") as out:
            while True:
                block=src.read(1<<20)
                if not block:break
                out.write(block)


def run_to_file(script,args,out_path):
    with out_path.open("w",encoding="utf-8") as out:
        return subprocess.run([sys.executable,str(script),*map(str,args)],check=False,stdout=out)


def main():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA-256 mismatch")

    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    blob=git_blob_sha1(EVALUATOR)
    expected=SOURCE["frozen_evaluator"]["git_blob_sha1"]
    if blob!=expected:
        raise RuntimeError(f"evaluator changed: expected {expected}, got {blob}")

    subprocess.run([sys.executable,str(HERE/"build_field.py"),str(CSV),str(FIELD)],check=True)
    ev=run_to_file(EVALUATOR,[FIELD],RESULT)
    if ev.returncode!=0:
        raise RuntimeError(f"evaluator failed with {ev.returncode}")

    verify=subprocess.run(
        [sys.executable,str(HERE/"verify_output.py"),str(FIELD),str(RESULT),str(THRESH)],
        check=False
    )

    field=json.loads(FIELD.read_text(encoding="utf-8"))
    threshold=json.loads(THRESH.read_text(encoding="utf-8"))
    audit={
        "archive_sha256_verified":True,
        "frozen_evaluator_blob_verified":True,
        "window_start":field["metadata"]["window_start"],
        "window_rows":field["metadata"]["window_rows"],
        "thresholds":field["metadata"]["thresholds"],
        "threshold_sensitivity":threshold.get("threshold_sensitivity",{}),
        "verification_exit_code":verify.returncode
    }
    AUDIT.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")

    if verify.returncode!=0:
        print("Experiment 024 reproducibility: PASS")
        print("Experiment 024 architectural result: FAIL")
        return 1

    print("Experiment 024 reproducibility: PASS")
    print("Experiment 024 architectural result: PASS")
    print("Experiment 024 scientific class:",threshold["threshold_sensitivity"]["classification"])
    return 0


if __name__=="__main__":
    raise SystemExit(main())
