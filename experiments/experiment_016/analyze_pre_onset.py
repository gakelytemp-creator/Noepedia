#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

PRE_SAMPLES = 24
MAD_SCALE = 1.4826
EPSILON = 1e-6
SAMPLES_PER_HOUR = 12.0


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def load_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "timestamp": row["timestamp"],
                "value": float(row["value"]),
            })
    return rows


def theil_sen(values):
    slopes = []
    n = len(values)
    for i in range(n):
        for j in range(i + 1, n):
            slopes.append((values[j] - values[i]) / (j - i))
    return statistics.median(slopes)


def analyze(rows, clusters_doc):
    index_by_timestamp = {
        row["timestamp"]: i for i, row in enumerate(rows)
    }

    output = []

    for ep in clusters_doc["episodes"]:
        start_idx = index_by_timestamp[ep["start"]]

        base = {
            "episode_id": ep["episode_id"],
            "start": ep["start"],
            "end": ep["end"],
            "cluster": ep["cluster"],
            "mismatch_count": ep["mismatch_count"],
        }

        if start_idx < PRE_SAMPLES:
            base["pre_onset_status"] = "INSUFFICIENT_CONTEXT"
            output.append(base)
            continue

        values = [
            row["value"]
            for row in rows[start_idx-PRE_SAMPLES:start_idx]
        ]

        med = statistics.median(values)
        mad = statistics.median(abs(x - med) for x in values)
        scale = max(MAD_SCALE * mad, EPSILON)

        slope_per_sample = theil_sen(values)
        slope_z_per_hour = (
            slope_per_sample * SAMPLES_PER_HOUR / scale
        )

        first_half = statistics.median(values[:PRE_SAMPLES//2])
        second_half = statistics.median(values[PRE_SAMPLES//2:])
        half_shift_z = (second_half - first_half) / scale
        robust_range_z = (max(values) - min(values)) / scale

        base.update({
            "pre_onset_status": "OK",
            "pre_samples": PRE_SAMPLES,
            "pre_median": med,
            "pre_mad": mad,
            "pre_scale": scale,
            "slope_per_sample": slope_per_sample,
            "slope_z_per_hour": slope_z_per_hour,
            "first_half_median": first_half,
            "second_half_median": second_half,
            "half_window_shift_z": half_shift_z,
            "robust_range_z": robust_range_z,
        })
        output.append(base)

    result = {
        "analysis": {
            "pre_samples": PRE_SAMPLES,
            "trend_estimator": "Theil-Sen median pairwise slope",
            "samples_per_hour": SAMPLES_PER_HOUR,
            "normalization": "1.4826*MAD",
            "label_input": False,
        },
        "episode_count": len(output),
        "episodes": output,
    }
    return result


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} DATA.csv CLUSTERS.json PRE_ONSET.json",
            file=sys.stderr,
        )
        return 2

    rows = load_rows(Path(argv[1]))
    clusters_doc = json.loads(
        Path(argv[2]).read_text(encoding="utf-8")
    )
    result = analyze(rows, clusters_doc)

    Path(argv[3]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"wrote {result['episode_count']} pre-onset records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
