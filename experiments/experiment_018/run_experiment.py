#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=json.loads(
    (ROOT/"experiments"/"experiment_011"/"SOURCE.json").read_text(encoding="utf-8")
)

WORK=HERE/"_runtime"
DATA=WORK/"data.csv"
PRED=WORK/"predictions.json"
FIELD=WORK/"field_input.json"
RESULT=WORK/"evaluator_result.json"
AUDIT=WORK/"audit.json"

DETECTOR=ROOT/"experiments"/"experiment_011"/"detector.py"
EVALUATOR=ROOT/"experiments"/"experiment_003"/"evaluator.py"


def git_blob_sha1(data:bytes)->str:
    header=f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header+data).hexdigest()


def download_verified(url,expected,dest):
    with urllib.request.urlopen(url,timeout=60) as response:
        data=response.read()
    actual=git_blob_sha1(data)
    if actual!=expected:
        raise RuntimeError(f"source hash mismatch: expected {expected}, got {actual}")
    dest.write_bytes(data)


def run_to_file(script,args,out_path):
    with out_path.open("w",encoding="utf-8") as out:
        subprocess.run(
            [sys.executable,str(script),*map(str,args)],
            check=True,
            stdout=out,
        )


def main():
    WORK.mkdir(exist_ok=True)

    download_verified(
        SOURCE["data"]["raw_url"],
        SOURCE["data"]["git_blob_sha1"],
        DATA,
    )

    subprocess.run([sys.executable,str(DETECTOR),str(DATA),str(PRED)],check=True)
    subprocess.run([sys.executable,str(HERE/"build_field.py"),str(DATA),str(PRED),str(FIELD)],check=True)

    run_to_file(EVALUATOR,[FIELD],RESULT)

    subprocess.run(
        [sys.executable,str(HERE/"verify_output.py"),str(FIELD),str(RESULT)],
        check=True,
    )

    field=json.loads(FIELD.read_text(encoding="utf-8"))
    result=json.loads(RESULT.read_text(encoding="utf-8"))

    audit={
        "source_data_blob_verified":True,
        "experiment_011_detector_reused_as_instrumentation_adapter":True,
        "experiment_003_evaluator_invoked_directly":True,
        "evaluator_received_field_json_only":True,
        "nab_labels_used":False,
        "assessment_count":len([o for o in field["objects"] if o.get("type")=="assessment"]),
        "open_count":len(field["open"]),
        "evaluator_summary":result["summary"],
    }
    AUDIT.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")

    print("Experiment 018 reproducibility: PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
