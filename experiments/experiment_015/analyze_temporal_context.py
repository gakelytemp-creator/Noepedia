#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from datetime import datetime
from pathlib import Path


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def main(argv):
    if len(argv) != 3:
        print(
            f"Usage: {Path(argv[0]).name} CLUSTERS.json TEMPORAL_CONTEXT.json",
            file=sys.stderr,
        )
        return 2

    clusters = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    episodes = []

    for ep in clusters["episodes"]:
        dt = parse_ts(ep["start"])
        minute_of_day = dt.hour * 60 + dt.minute + dt.second / 60.0
        angle = 2.0 * math.pi * minute_of_day / 1440.0

        episodes.append({
            "episode_id": ep["episode_id"],
            "start": ep["start"],
            "end": ep["end"],
            "cluster": ep["cluster"],
            "mismatch_count": ep["mismatch_count"],
            "start_minute_of_day": minute_of_day,
            "start_phase_angle": angle,
        })

    result = {
        "analysis": {
            "context_relation": "episode_start_time_of_day",
            "period_minutes": 1440,
            "label_input": False,
        },
        "episode_count": len(episodes),
        "episodes": episodes,
    }

    Path(argv[2]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(episodes)} temporal-context records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
