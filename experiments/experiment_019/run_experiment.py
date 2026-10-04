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
    with urllib.request.urlopen(url,timeout=120) as response, dest.open("wb") as out:
        while True:
            block=response.read(1<<20)
            if not block:
                break
            out.write(block)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        matches=[n for n in z.namelist() if Path(n).name==basename]
        if len(matches)!=1:
            raise RuntimeError(f"expected one CSV member named {basename}, found {matches}")
        with z.open(matches[0]) as src, dest.open("wb") as out:
            while True:
                block=src.read(1<<20)
                if not block:
                    break
                out.write(block)


def run_to_file(script,args,out_path):
    with out_path.open("w",encoding="utf-8") as out:
        subprocess.run([sys.executable,str(script),*map(str,args)],check=True,stdout=out)


def main():
    WORK.mkdir(exist_ok=True)

    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)

    actual_sha=sha256_file(ZIP)
    if actual_sha!=SOURCE["archive_sha256"]:
        raise RuntimeError(f"archive SHA-256 mismatch: {actual_sha}")

    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    evaluator_blob=git_blob_sha1(EVALUATOR)
    expected_blob=SOURCE["frozen_evaluator"]["git_blob_sha1"]
    if evaluator_blob!=expected_blob:
        raise RuntimeError(
            f"evaluator changed after preregistration: expected {expected_blob}, got {evaluator_blob}"
        )

    subprocess.run([sys.executable,str(HERE/"build_field.py"),str(CSV),str(FIELD)],check=True)
    run_to_file(EVALUATOR,[FIELD],RESULT)

    verify=subprocess.run(
        [sys.executable,str(HERE/"verify_output.py"),str(FIELD),str(RESULT)],
        check=False,
    )

    field=json.loads(FIELD.read_text(encoding="utf-8"))
    result=json.loads(RESULT.read_text(encoding="utf-8"))
    counts=result.get("summary",{}).get("event_counts",{})

    audit={
        "archive_sha256_verified":True,
        "frozen_evaluator_blob_verified":True,
        "failure_labels_used":False,
        "evaluation_assessments":field["metadata"]["evaluation_rows"],
        "digital_states_present":field["metadata"]["digital_states_present"],
        "analog_states_present":field["metadata"]["analog_states_present"],
        "motor_current_threshold":field["metadata"]["motor_current_threshold"],
        "input_paths_assert_verdicts":field["metadata"]["input_paths_assert_verdicts"],
        "event_counts":counts,
        "verification_exit_code":verify.returncode,
    }
    AUDIT.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")

    if verify.returncode!=0:
        print("Experiment 019 reproducibility: PASS")
        print("Experiment 019 architectural result: FAIL / NOT_EVALUABLE")
        return 1

    print("Experiment 019 reproducibility: PASS")
    print("Experiment 019 architectural result: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
