#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

MAX_GAP_MINUTES = 30
HOT_FRACTION = 0.80
COLD_FRACTION = 0.80


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def sign_class(pos: int, neg: int) -> str:
    total = pos + neg
    if total == 0:
        return "MIXED"
    if pos / total >= HOT_FRACTION:
        return "HOT"
    if neg / total >= COLD_FRACTION:
        return "COLD"
    return "MIXED"


def build_episode(items, episode_number):
    times = [parse_ts(x["timestamp"]) for x in items]
    residuals = [x["observed_value"] - x["trailing_median"] for x in items]
    zs = [x["robust_z"] for x in items]

    positive = sum(1 for r in residuals if r > 0)
    negative = sum(1 for r in residuals if r < 0)

    return {
        "episode_id": f"EP_{episode_number:04d}",
        "start": min(times).isoformat(sep=" "),
        "end": max(times).isoformat(sep=" "),
        "mismatch_count": len(items),
        "duration_minutes": (max(times) - min(times)).total_seconds() / 60.0,
        "mean_robust_z": sum(zs) / len(zs),
        "max_robust_z": max(zs),
        "positive_residual_count": positive,
        "negative_residual_count": negative,
        "sign_class": sign_class(positive, negative),
        "event_timestamps": [x["timestamp"] for x in items],
        "source_rows": [x["row_number"] for x in items],
    }


def decompose(predictions):
    mismatches = sorted(
        predictions["mismatches"],
        key=lambda x: parse_ts(x["timestamp"]),
    )

    episodes = []
    current = []

    for item in mismatches:
        if not current:
            current = [item]
            continue

        gap = (
            parse_ts(item["timestamp"])
            - parse_ts(current[-1]["timestamp"])
        ).total_seconds() / 60.0

        if gap <= MAX_GAP_MINUTES:
            current.append(item)
        else:
            episodes.append(build_episode(current, len(episodes) + 1))
            current = [item]

    if current:
        episodes.append(build_episode(current, len(episodes) + 1))

    return {
        "decomposition": {
            "max_gap_minutes": MAX_GAP_MINUTES,
            "hot_fraction": HOT_FRACTION,
            "cold_fraction": COLD_FRACTION,
            "label_input": False,
        },
        "mismatch_count": len(mismatches),
        "episode_count": len(episodes),
        "episodes": episodes,
    }


def main(argv):
    if len(argv) != 3:
        print(
            f"Usage: {Path(argv[0]).name} PREDICTIONS.json EPISODES.json",
            file=sys.stderr,
        )
        return 2

    predictions = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result = decompose(predictions)
    Path(argv[2]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {result['episode_count']} episodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
