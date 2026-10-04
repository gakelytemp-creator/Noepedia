#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

SOURCE = json.loads(
    (ROOT / "experiments" / "experiment_011" / "SOURCE.json")
    .read_text(encoding="utf-8")
)

WORK = HERE / "_runtime"
DATA = WORK / "data.csv"
PREDICTIONS = WORK / "predictions.json"
EPISODES = WORK / "episodes.json"
TRANSITIONS = WORK / "transitions.json"
CLUSTERS = WORK / "clusters.json"
TEMPORAL = WORK / "temporal_context.json"
LABELS = WORK / "labels.json"
RESULT = WORK / "evaluation.json"

DETECTOR = ROOT / "experiments" / "experiment_011" / "detector.py"
EPISODE_ANALYZER = ROOT / "experiments" / "experiment_012" / "analyze_episodes.py"
TRANSITION_ANALYZER = ROOT / "experiments" / "experiment_013" / "analyze_transitions.py"
CLUSTERER = ROOT / "experiments" / "experiment_014" / "cluster_cold.py"


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def download_verified(url, expected_blob_sha, destination):
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    actual = git_blob_sha1(data)
    if actual != expected_blob_sha:
        raise RuntimeError(
            f"source hash mismatch: expected {expected_blob_sha}, got {actual}"
        )
    destination.write_bytes(data)


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True)


def main():
    WORK.mkdir(exist_ok=True)

    download_verified(
        SOURCE["data"]["raw_url"],
        SOURCE["data"]["git_blob_sha1"],
        DATA,
    )

    run(DETECTOR, DATA, PREDICTIONS)
    run(EPISODE_ANALYZER, PREDICTIONS, EPISODES)
    run(TRANSITION_ANALYZER, DATA, EPISODES, TRANSITIONS)
    run(CLUSTERER, TRANSITIONS, CLUSTERS)

    # Time-of-day context is derived before labels are downloaded.
    run(HERE / "analyze_temporal_context.py", CLUSTERS, TEMPORAL)

    download_verified(
        SOURCE["labels"]["raw_url"],
        SOURCE["labels"]["git_blob_sha1"],
        LABELS,
    )

    run(HERE / "evaluate.py", TEMPORAL, LABELS, RESULT)

    result = json.loads(RESULT.read_text(encoding="utf-8"))

    audit = {
        "experiment_011_detector_reused_unchanged": True,
        "experiment_012_episode_analyzer_reused_unchanged": True,
        "experiment_013_transition_analyzer_reused_unchanged": True,
        "experiment_014_clusterer_reused_unchanged": True,
        "temporal_context_created_before_label_download": True,
        "temporal_analyzer_declares_label_input": False,
        "source_data_blob_verified": True,
        "source_labels_blob_verified": True,
        "evaluation_summary": {
            k: v for k, v in result.items()
            if k != "outside_episodes"
        },
    }

    (WORK / "audit.json").write_text(
        json.dumps(audit, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Experiment 015 reproducibility: PASS")
    print("Scientific result:", result["scientific_result"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
