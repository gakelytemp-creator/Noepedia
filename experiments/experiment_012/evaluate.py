#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

DATASET_KEY = "realKnownCause/machine_temperature_system_failure.csv"
PERSISTENT_MIN_EVENTS = 6
PERSISTENT_OUTSIDE_FRACTION_GATE = 0.50
MAX_OUTSIDE_DURATION_GATE_MIN = 60.0


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def episode_overlaps_window(episode, window):
    start = parse_ts(episode["start"])
    end = parse_ts(episode["end"])
    w_start = parse_ts(window[0])
    w_end = parse_ts(window[1])
    return start <= w_end and end >= w_start


def event_inside_windows(ts: str, windows):
    t = parse_ts(ts)
    for a, b in windows:
        if parse_ts(a) <= t <= parse_ts(b):
            return True
    return False


def evaluate(episodes_doc, labels):
    windows = labels[DATASET_KEY]

    evaluated = []
    outside_points = 0
    persistent_outside_points = 0
    outside_only_episodes = []

    for ep in episodes_doc["episodes"]:
        overlap = any(episode_overlaps_window(ep, w) for w in windows)
        status = "OVERLAPS_LABEL" if overlap else "OUTSIDE_LABEL"

        outside_event_count = sum(
            1 for ts in ep["event_timestamps"]
            if not event_inside_windows(ts, windows)
        )

        row = dict(ep)
        row["label_overlap"] = status
        row["outside_event_count"] = outside_event_count
        evaluated.append(row)

        outside_points += outside_event_count

        if not overlap:
            outside_only_episodes.append(row)
            if ep["mismatch_count"] >= PERSISTENT_MIN_EVENTS:
                persistent_outside_points += ep["mismatch_count"]

    isolated_outside = sum(
        1 for ep in outside_only_episodes
        if ep["mismatch_count"] == 1
    )
    persistent_outside = sum(
        1 for ep in outside_only_episodes
        if ep["mismatch_count"] >= PERSISTENT_MIN_EVENTS
    )

    max_outside_duration = max(
        (ep["duration_minutes"] for ep in outside_only_episodes),
        default=0.0,
    )

    persistent_fraction = (
        persistent_outside_points / outside_points
        if outside_points else 0.0
    )

    outside_counts = sorted(
        (ep["mismatch_count"] for ep in outside_only_episodes),
        reverse=True,
    )
    top10_points = sum(outside_counts[:10])
    top10_concentration = (
        top10_points / outside_points
        if outside_points else 0.0
    )

    scientific_pass = (
        persistent_fraction >= PERSISTENT_OUTSIDE_FRACTION_GATE
        and max_outside_duration >= MAX_OUTSIDE_DURATION_GATE_MIN
    )

    return {
        "dataset_key": DATASET_KEY,
        "mismatch_count": episodes_doc["mismatch_count"],
        "episode_count": episodes_doc["episode_count"],
        "anomaly_window_count": len(windows),
        "outside_label_mismatch_points": outside_points,
        "outside_only_episode_count": len(outside_only_episodes),
        "isolated_outside_episode_count": isolated_outside,
        "persistent_outside_episode_count": persistent_outside,
        "persistent_min_events": PERSISTENT_MIN_EVENTS,
        "persistent_outside_mismatch_points": persistent_outside_points,
        "persistent_outside_fraction": persistent_fraction,
        "max_outside_episode_duration_minutes": max_outside_duration,
        "top10_outside_episode_concentration": top10_concentration,
        "sign_class_counts_outside": {
            "HOT": sum(1 for ep in outside_only_episodes if ep["sign_class"] == "HOT"),
            "COLD": sum(1 for ep in outside_only_episodes if ep["sign_class"] == "COLD"),
            "MIXED": sum(1 for ep in outside_only_episodes if ep["sign_class"] == "MIXED"),
        },
        "success_gate": {
            "persistent_outside_fraction_min": PERSISTENT_OUTSIDE_FRACTION_GATE,
            "max_outside_episode_duration_minutes_min": MAX_OUTSIDE_DURATION_GATE_MIN,
        },
        "scientific_result": "PASS" if scientific_pass else "FAIL",
        "episodes": evaluated,
    }


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} EPISODES.json LABELS.json RESULT.json",
            file=sys.stderr,
        )
        return 2

    episodes = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    labels = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = evaluate(episodes, labels)

    Path(argv[3]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    summary = {k: v for k, v in result.items() if k != "episodes"}
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
