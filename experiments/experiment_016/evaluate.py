#!/usr/bin/env python3
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DATASET_KEY = "realKnownCause/machine_temperature_system_failure.csv"

CLUSTER1_MEDIAN_SLOPE_GATE = -0.50
MEDIAN_DIFFERENCE_GATE = -0.75
PAIRWISE_DOMINANCE_GATE = 0.75


def parse_ts(value):
    return datetime.fromisoformat(value)


def overlaps(ep, window):
    s = parse_ts(ep["start"])
    e = parse_ts(ep["end"])
    a = parse_ts(window[0])
    b = parse_ts(window[1])
    return s <= b and e >= a


def pairwise_downward_dominance(cluster1, cluster0):
    wins = 0.0
    total = 0
    for a in cluster1:
        for b in cluster0:
            total += 1
            av = a["slope_z_per_hour"]
            bv = b["slope_z_per_hour"]
            if av < bv:
                wins += 1.0
            elif av == bv:
                wins += 0.5
    return wins / total if total else 0.0


def med(values):
    return statistics.median(values) if values else None


def evaluate(pre_doc, labels):
    windows = labels[DATASET_KEY]

    outside = [
        ep for ep in pre_doc["episodes"]
        if ep.get("pre_onset_status") == "OK"
        and not any(overlaps(ep, w) for w in windows)
    ]

    by_cluster = defaultdict(list)
    for ep in outside:
        by_cluster[ep["cluster"]].append(ep)

    c0 = by_cluster.get("CLUSTER_0", [])
    c1 = by_cluster.get("CLUSTER_1", [])

    c0_median = med([ep["slope_z_per_hour"] for ep in c0])
    c1_median = med([ep["slope_z_per_hour"] for ep in c1])

    if c0_median is None or c1_median is None:
        median_difference = None
        dominance = 0.0
        scientific_pass = False
    else:
        median_difference = c1_median - c0_median
        dominance = pairwise_downward_dominance(c1, c0)
        scientific_pass = (
            c1_median <= CLUSTER1_MEDIAN_SLOPE_GATE
            and median_difference <= MEDIAN_DIFFERENCE_GATE
            and dominance >= PAIRWISE_DOMINANCE_GATE
        )

    profiles = {}
    for name, eps in [("CLUSTER_0", c0), ("CLUSTER_1", c1)]:
        profiles[name] = {
            "episode_count": len(eps),
            "median_slope_z_per_hour": med([
                ep["slope_z_per_hour"] for ep in eps
            ]),
            "median_half_window_shift_z": med([
                ep["half_window_shift_z"] for ep in eps
            ]),
            "median_robust_range_z": med([
                ep["robust_range_z"] for ep in eps
            ]),
        }

    return {
        "dataset_key": DATASET_KEY,
        "outside_only_cold_episode_count": len(outside),
        "cluster_pre_onset_profiles": profiles,
        "median_slope_difference_cluster1_minus_cluster0": median_difference,
        "pairwise_downward_dominance": dominance,
        "success_gate": {
            "cluster_1_median_slope_z_per_hour_max": CLUSTER1_MEDIAN_SLOPE_GATE,
            "median_difference_cluster1_minus_cluster0_max": MEDIAN_DIFFERENCE_GATE,
            "pairwise_downward_dominance_min": PAIRWISE_DOMINANCE_GATE,
        },
        "scientific_result": "PASS" if scientific_pass else "FAIL",
        "outside_episodes": outside,
    }


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} PRE_ONSET.json LABELS.json RESULT.json",
            file=sys.stderr,
        )
        return 2

    pre_doc = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    labels = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = evaluate(pre_doc, labels)

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
