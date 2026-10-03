#!/usr/bin/env python3
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

DATASET_KEY = "realKnownCause/machine_temperature_system_failure.csv"
EPISODE_FRACTION_GATE = 0.50
POINT_FRACTION_GATE = 0.50


def parse_ts(value):
    return datetime.fromisoformat(value)


def overlaps(ep, window):
    s = parse_ts(ep["start"])
    e = parse_ts(ep["end"])
    a = parse_ts(window[0])
    b = parse_ts(window[1])
    return s <= b and e >= a


def evaluate(transitions, labels):
    windows = labels[DATASET_KEY]

    outside_cold = [
        ep for ep in transitions["episodes"]
        if ep.get("sign_class") == "COLD"
        and not any(overlaps(ep, w) for w in windows)
        and ep.get("transition_class") != "INSUFFICIENT_CONTEXT"
    ]

    counts = {
        "DOWNWARD_LEVEL_SHIFT": 0,
        "RECOVERED_COLD_EXCURSION": 0,
        "OTHER_COLD": 0,
    }
    for ep in outside_cold:
        cls = ep["transition_class"]
        if cls in counts:
            counts[cls] += 1

    total_episodes = len(outside_cold)
    downward_episodes = counts["DOWNWARD_LEVEL_SHIFT"]
    episode_fraction = (
        downward_episodes / total_episodes if total_episodes else 0.0
    )

    total_points = sum(ep["mismatch_count"] for ep in outside_cold)
    downward_points = sum(
        ep["mismatch_count"] for ep in outside_cold
        if ep["transition_class"] == "DOWNWARD_LEVEL_SHIFT"
    )
    point_fraction = downward_points / total_points if total_points else 0.0

    post_shift_values = [ep["post_shift_z"] for ep in outside_cold]
    episode_shift_values = [ep["episode_shift_z"] for ep in outside_cold]

    scientific_pass = (
        episode_fraction >= EPISODE_FRACTION_GATE
        and point_fraction >= POINT_FRACTION_GATE
    )

    return {
        "dataset_key": DATASET_KEY,
        "outside_only_cold_episode_count": total_episodes,
        "classification_counts": counts,
        "downward_level_shift_episode_fraction": episode_fraction,
        "outside_only_cold_mismatch_points": total_points,
        "downward_level_shift_mismatch_points": downward_points,
        "downward_level_shift_point_fraction": point_fraction,
        "median_post_shift_z": (
            statistics.median(post_shift_values)
            if post_shift_values else None
        ),
        "median_episode_shift_z": (
            statistics.median(episode_shift_values)
            if episode_shift_values else None
        ),
        "success_gate": {
            "downward_level_shift_episode_fraction_min": EPISODE_FRACTION_GATE,
            "downward_level_shift_point_fraction_min": POINT_FRACTION_GATE,
        },
        "scientific_result": "PASS" if scientific_pass else "FAIL",
        "outside_cold_episodes": outside_cold,
    }


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} TRANSITIONS.json LABELS.json RESULT.json",
            file=sys.stderr,
        )
        return 2

    transitions = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    labels = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = evaluate(transitions, labels)

    Path(argv[3]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    summary = {
        k: v for k, v in result.items()
        if k != "outside_cold_episodes"
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
