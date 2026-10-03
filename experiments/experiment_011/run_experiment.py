#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = json.loads((HERE / "SOURCE.json").read_text(encoding="utf-8"))
WORK = HERE / "_runtime"
DATA = WORK / "data.csv"
LABELS = WORK / "labels.json"
PREDICTIONS = WORK / "predictions.json"
RESULT = WORK / "evaluation.json"


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def download_verified(url: str, expected_blob_sha: str, destination: Path):
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

    # Detection happens before labels are downloaded.
    run(HERE / "detector.py", DATA, PREDICTIONS)

    # Ground truth is introduced only after predictions exist.
    download_verified(
        SOURCE["labels"]["raw_url"],
        SOURCE["labels"]["git_blob_sha1"],
        LABELS,
    )

    run(HERE / "evaluate.py", PREDICTIONS, LABELS, RESULT)

    result = json.loads(RESULT.read_text(encoding="utf-8"))

    audit = {
        "source_data_blob_verified": True,
        "source_labels_blob_verified": True,
        "predictions_created_before_label_download": True,
        "detector_declares_label_input": False,
        "evaluation": result,
    }

    (WORK / "audit.json").write_text(
        json.dumps(audit, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Experiment 011 reproducibility: PASS")
    print("Scientific result:", result["scientific_result"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
