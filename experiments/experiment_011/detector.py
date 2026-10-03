#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

WINDOW = 288
ROBUST_Z_THRESHOLD = 6.0
MAD_SCALE = 1.4826
EPSILON = 1e-6
RULE_ID = "RULE_TRAILING_MEDIAN_MAD_Z6"


def load_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row_number, row in enumerate(reader, start=2):
            rows.append({
                "row_number": row_number,
                "timestamp": row["timestamp"],
                "value": float(row["value"]),
            })
    return rows


def detect(rows):
    mismatches = []

    for i in range(WINDOW, len(rows)):
        history = [r["value"] for r in rows[i-WINDOW:i]]
        median = statistics.median(history)
        abs_dev = [abs(x - median) for x in history]
        mad = statistics.median(abs_dev)
        scale = max(MAD_SCALE * mad, EPSILON)

        current = rows[i]
        robust_z = abs(current["value"] - median) / scale

        if robust_z >= ROBUST_Z_THRESHOLD:
            mismatches.append({
                "event": "FORMAL_MISMATCH",
                "rule": RULE_ID,
                "row_number": current["row_number"],
                "timestamp": current["timestamp"],
                "observed_value": current["value"],
                "trailing_window": WINDOW,
                "trailing_median": median,
                "trailing_mad": mad,
                "robust_z": robust_z,
                "threshold": ROBUST_Z_THRESHOLD,
            })

    return {
        "detector": {
            "rule_id": RULE_ID,
            "window": WINDOW,
            "mad_scale": MAD_SCALE,
            "threshold": ROBUST_Z_THRESHOLD,
            "future_samples_used": False,
            "label_input": False,
        },
        "total_samples": len(rows),
        "scored_samples": max(0, len(rows) - WINDOW),
        "mismatches": mismatches,
    }


def main(argv):
    if len(argv) != 3:
        print(f"Usage: {Path(argv[0]).name} DATA.csv PREDICTIONS.json", file=sys.stderr)
        return 2

    result = detect(load_rows(Path(argv[1])))
    Path(argv[2]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(result['mismatches'])} mismatches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
