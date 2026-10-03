#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

DATASET_KEY = "realKnownCause/machine_temperature_system_failure.csv"
WINDOW_RECALL_GATE = 0.50
POINT_PRECISION_GATE = 0.20


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def inside_any(timestamp: datetime, windows):
    return any(start <= timestamp <= end for start, end in windows)


def evaluate(predictions, labels):
    raw_windows = labels[DATASET_KEY]
    windows = [(parse_ts(a), parse_ts(b)) for a, b in raw_windows]

    mismatch_times = [
        parse_ts(item["timestamp"])
        for item in predictions["mismatches"]
    ]

    windows_hit = sum(
        1 for start, end in windows
        if any(start <= t <= end for t in mismatch_times)
    )

    inside = sum(1 for t in mismatch_times if inside_any(t, windows))
    outside = len(mismatch_times) - inside

    window_recall = windows_hit / len(windows) if windows else 1.0
    point_precision = inside / len(mismatch_times) if mismatch_times else 0.0

    scientific_pass = (
        window_recall >= WINDOW_RECALL_GATE
        and point_precision >= POINT_PRECISION_GATE
    )

    return {
        "dataset_key": DATASET_KEY,
        "total_samples": predictions["total_samples"],
        "scored_samples": predictions["scored_samples"],
        "mismatch_count": len(mismatch_times),
        "anomaly_window_count": len(windows),
        "anomaly_windows_hit": windows_hit,
        "window_recall": window_recall,
        "mismatch_points_inside_windows": inside,
        "mismatch_points_outside_windows": outside,
        "point_precision": point_precision,
        "success_gate": {
            "window_recall_min": WINDOW_RECALL_GATE,
            "point_precision_min": POINT_PRECISION_GATE,
        },
        "scientific_result": "PASS" if scientific_pass else "FAIL",
    }


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} PREDICTIONS.json LABELS.json RESULT.json",
            file=sys.stderr,
        )
        return 2

    predictions = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    labels = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = evaluate(predictions, labels)

    Path(argv[3]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
