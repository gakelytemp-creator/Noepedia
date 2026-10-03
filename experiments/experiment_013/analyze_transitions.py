#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

PRE_SAMPLES = 12
POST_SAMPLES = 12
MAD_SCALE = 1.4826
EPSILON = 1e-6
DOWN_SHIFT_Z = -2.0
RECOVERED_ABS_POST_Z = 1.0


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def load_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "timestamp": row["timestamp"],
                "dt": parse_ts(row["timestamp"]),
                "value": float(row["value"]),
            })
    return rows


def median_abs_deviation(values, median):
    return statistics.median(abs(x - median) for x in values)


def classify(sign_class, episode_shift_z, post_shift_z):
    if sign_class != "COLD":
        return "NOT_COLD"
    if post_shift_z <= DOWN_SHIFT_Z:
        return "DOWNWARD_LEVEL_SHIFT"
    if episode_shift_z <= DOWN_SHIFT_Z and abs(post_shift_z) < RECOVERED_ABS_POST_Z:
        return "RECOVERED_COLD_EXCURSION"
    return "OTHER_COLD"


def analyze(rows, episodes_doc):
    index_by_timestamp = {r["timestamp"]: i for i, r in enumerate(rows)}
    output = []

    for ep in episodes_doc["episodes"]:
        start_idx = index_by_timestamp[ep["start"]]
        end_idx = index_by_timestamp[ep["end"]]

        if start_idx < PRE_SAMPLES or end_idx + POST_SAMPLES >= len(rows):
            row = dict(ep)
            row.update({
                "transition_class": "INSUFFICIENT_CONTEXT",
                "pre_samples": PRE_SAMPLES,
                "post_samples": POST_SAMPLES,
            })
            output.append(row)
            continue

        pre = [r["value"] for r in rows[start_idx-PRE_SAMPLES:start_idx]]
        post = [r["value"] for r in rows[end_idx+1:end_idx+1+POST_SAMPLES]]
        episode_values = [r["value"] for r in rows[start_idx:end_idx+1]]

        pre_median = statistics.median(pre)
        pre_mad = median_abs_deviation(pre, pre_median)
        pre_scale = max(MAD_SCALE * pre_mad, EPSILON)
        post_median = statistics.median(post)
        episode_median = statistics.median(episode_values)

        post_shift_z = (post_median - pre_median) / pre_scale
        episode_shift_z = (episode_median - pre_median) / pre_scale

        row = dict(ep)
        row.update({
            "pre_samples": PRE_SAMPLES,
            "post_samples": POST_SAMPLES,
            "pre_median": pre_median,
            "pre_mad": pre_mad,
            "pre_scale": pre_scale,
            "episode_raw_median": episode_median,
            "post_median": post_median,
            "episode_shift_z": episode_shift_z,
            "post_shift_z": post_shift_z,
            "transition_class": classify(
                ep["sign_class"], episode_shift_z, post_shift_z
            ),
        })
        output.append(row)

    return {
        "analysis": {
            "pre_samples": PRE_SAMPLES,
            "post_samples": POST_SAMPLES,
            "mad_scale": MAD_SCALE,
            "down_shift_z_threshold": DOWN_SHIFT_Z,
            "recovered_abs_post_z_max": RECOVERED_ABS_POST_Z,
            "label_input": False,
        },
        "episode_count": len(output),
        "episodes": output,
    }


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} DATA.csv EPISODES.json TRANSITIONS.json",
            file=sys.stderr,
        )
        return 2

    rows = load_rows(Path(argv[1]))
    episodes = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = analyze(rows, episodes)
    Path(argv[3]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {result['episode_count']} transition records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
