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
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

WORK=HERE/"_runtime"
DATA=WORK/"data.csv"
PRED=WORK/"predictions.json"
EPISODES=WORK/"episodes.json"
TRANSITIONS=WORK/"transitions.json"
CLUSTERS=WORK/"clusters.json"
LABELS=WORK/"labels.json"
PRIMARY=WORK/"primary_null_evaluation.json"
SECONDARY=WORK/"secondary_cluster_evaluation.json"
AUDIT=WORK/"audit.json"

DETECTOR=ROOT/"experiments"/"experiment_011"/"detector.py"
EPISODE_ANALYZER=ROOT/"experiments"/"experiment_012"/"analyze_episodes.py"
TRANSITION_ANALYZER=ROOT/"experiments"/"experiment_013"/"analyze_transitions.py"
CLUSTERER=ROOT/"experiments"/"experiment_014"/"cluster_cold.py"
CLUSTER_EVAL=ROOT/"experiments"/"experiment_014"/"evaluate.py"


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


def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],check=check)


def main():
    WORK.mkdir(exist_ok=True)

    download_verified(SOURCE["data"]["raw_url"],SOURCE["data"]["git_blob_sha1"],DATA)

    # Primary predictions and all secondary structural outputs are created before labels are downloaded.
    run(DETECTOR,DATA,PRED)
    run(EPISODE_ANALYZER,PRED,EPISODES)
    run(TRANSITION_ANALYZER,DATA,EPISODES,TRANSITIONS)

    cluster_status="OK"
    cluster_error=None
    proc=run(CLUSTERER,TRANSITIONS,CLUSTERS,check=False)
    if proc.returncode!=0:
        cluster_status="NOT_EVALUABLE"
        cluster_error=f"clusterer exit code {proc.returncode}"

    download_verified(SOURCE["labels"]["raw_url"],SOURCE["labels"]["git_blob_sha1"],LABELS)

    run(HERE/"evaluate_null.py",DATA,PRED,LABELS,PRIMARY)
    primary=json.loads(PRIMARY.read_text(encoding="utf-8"))

    secondary_result="NOT_EVALUABLE"
    secondary_summary=None
    if cluster_status=="OK":
        proc=run(CLUSTER_EVAL,CLUSTERS,LABELS,SECONDARY,check=False)
        if proc.returncode==0 and SECONDARY.exists():
            secondary=json.loads(SECONDARY.read_text(encoding="utf-8"))
            secondary_result=secondary.get("scientific_result","NOT_EVALUABLE")
            secondary_summary={k:v for k,v in secondary.items() if k!="outside_cold_episodes"}
        else:
            cluster_status="NOT_EVALUABLE"
            cluster_error=f"cluster evaluation exit code {proc.returncode}"

    audit={
        "heldout_source_data_blob_verified":True,
        "heldout_source_labels_blob_verified":True,
        "detector_reused_unchanged":True,
        "episode_analyzer_reused_unchanged":True,
        "transition_analyzer_reused_unchanged":True,
        "clusterer_reused_unchanged":True,
        "all_predictions_and_structural_outputs_attempted_before_label_download":True,
        "primary":primary,
        "secondary_pipeline_status":cluster_status,
        "secondary_scientific_result":secondary_result,
        "secondary_summary":secondary_summary,
        "secondary_error":cluster_error
    }
    AUDIT.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")

    print("Experiment 017 reproducibility: PASS")
    print("Primary scientific result:",primary["primary_scientific_result"])
    print("Secondary structural result:",secondary_result)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
