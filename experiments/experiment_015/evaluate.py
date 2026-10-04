#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DATASET_KEY = "realKnownCause/machine_temperature_system_failure.csv"

CLUSTER_1_R_GATE = 0.70
PHASE_SEPARATION_HOURS_GATE = 2.0
R_DIFFERENCE_GATE = 0.20


def parse_ts(value):
    return datetime.fromisoformat(value)


def overlaps(ep, window):
    s = parse_ts(ep["start"])
    e = parse_ts(ep["end"])
    a = parse_ts(window[0])
    b = parse_ts(window[1])
    return s <= b and e >= a


def circular_stats(episodes):
    if not episodes:
        return {
            "count": 0,
            "resultant_length": 0.0,
            "mean_angle": None,
            "mean_start_minute_of_day": None,
            "mean_start_clock": None,
        }

    mean_cos = sum(math.cos(ep["start_phase_angle"]) for ep in episodes) / len(episodes)
    mean_sin = sum(math.sin(ep["start_phase_angle"]) for ep in episodes) / len(episodes)
    r = math.sqrt(mean_cos * mean_cos + mean_sin * mean_sin)

    angle = math.atan2(mean_sin, mean_cos)
    if angle < 0:
        angle += 2.0 * math.pi

    minute = angle * 1440.0 / (2.0 * math.pi)
    total_minutes = int(round(minute)) % 1440
    hh = total_minutes // 60
    mm = total_minutes % 60

    return {
        "count": len(episodes),
        "resultant_length": r,
        "mean_angle": angle,
        "mean_start_minute_of_day": minute,
        "mean_start_clock": f"{hh:02d}:{mm:02d}",
    }


def circular_distance_hours(a, b):
    d = abs(a - b)
    d = min(d, 2.0 * math.pi - d)
    return d * 24.0 / (2.0 * math.pi)


def evaluate(context, labels):
    windows = labels[DATASET_KEY]

    outside = [
        ep for ep in context["episodes"]
        if not any(overlaps(ep, w) for w in windows)
    ]

    by_cluster = defaultdict(list)
    for ep in outside:
        by_cluster[ep["cluster"]].append(ep)

    stats0 = circular_stats(by_cluster.get("CLUSTER_0", []))
    stats1 = circular_stats(by_cluster.get("CLUSTER_1", []))

    if stats0["mean_angle"] is None or stats1["mean_angle"] is None:
        separation = 0.0
    else:
        separation = circular_distance_hours(
            stats0["mean_angle"], stats1["mean_angle"]
        )

    r_difference = (
        stats1["resultant_length"] - stats0["resultant_length"]
    )

    scientific_pass = (
        stats1["resultant_length"] >= CLUSTER_1_R_GATE
        and separation >= PHASE_SEPARATION_HOURS_GATE
        and r_difference >= R_DIFFERENCE_GATE
    )

    return {
        "dataset_key": DATASET_KEY,
        "outside_only_cold_episode_count": len(outside),
        "cluster_temporal_stats": {
            "CLUSTER_0": stats0,
            "CLUSTER_1": stats1,
        },
        "phase_separation_hours": separation,
        "resultant_length_difference_cluster1_minus_cluster0": r_difference,
        "success_gate": {
            "cluster_1_resultant_length_min": CLUSTER_1_R_GATE,
            "phase_separation_hours_min": PHASE_SEPARATION_HOURS_GATE,
            "cluster_1_minus_cluster_0_resultant_length_min": R_DIFFERENCE_GATE,
        },
        "scientific_result": "PASS" if scientific_pass else "FAIL",
        "outside_episodes": outside,
    }


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} TEMPORAL_CONTEXT.json LABELS.json RESULT.json",
            file=sys.stderr,
        )
        return 2

    context = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    labels = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = evaluate(context, labels)

    Path(argv[3]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    summary = {
        k: v for k, v in result.items()
        if k != "outside_episodes"
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
