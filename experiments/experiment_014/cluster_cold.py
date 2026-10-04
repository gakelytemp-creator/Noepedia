#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

FEATURES = [
    "log_mismatch_count",
    "log_duration_minutes",
    "episode_shift_z",
    "post_shift_z",
    "log_max_robust_z",
]
MAD_SCALE = 1.4826
EPSILON = 1e-6
K = 2
MAX_ITERATIONS = 100


def euclidean(a, b):
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))


def median_abs_deviation(values, median):
    return statistics.median(abs(x-median) for x in values)


def raw_features(ep):
    return {
        "log_mismatch_count": math.log1p(ep["mismatch_count"]),
        "log_duration_minutes": math.log1p(ep["duration_minutes"]),
        "episode_shift_z": ep["episode_shift_z"],
        "post_shift_z": ep["post_shift_z"],
        "log_max_robust_z": math.log1p(ep["max_robust_z"]),
    }


def normalize(rows):
    stats = {}
    for feature in FEATURES:
        values = [r["features_raw"][feature] for r in rows]
        center = statistics.median(values)
        mad = median_abs_deviation(values, center)
        scale = max(MAD_SCALE * mad, EPSILON)
        stats[feature] = {"center": center, "scale": scale}

    for row in rows:
        row["vector"] = [
            (row["features_raw"][f] - stats[f]["center"]) / stats[f]["scale"]
            for f in FEATURES
        ]
    return stats


def farthest_pair(rows):
    best = None
    for i in range(len(rows)):
        for j in range(i+1, len(rows)):
            d = euclidean(rows[i]["vector"], rows[j]["vector"])
            key = (
                d,
                tuple(sorted([rows[i]["episode_id"], rows[j]["episode_id"]]))
            )
            if best is None or key[0] > best[0] or (
                abs(key[0]-best[0]) < 1e-12 and key[1] < best[1]
            ):
                best = (key[0], key[1], i, j)
    return best[2], best[3]


def mean_vector(vectors):
    return [
        sum(values) / len(values)
        for values in zip(*vectors)
    ]


def cluster(rows):
    if len(rows) < 2:
        raise RuntimeError("need at least two eligible COLD episodes")

    i, j = farthest_pair(rows)
    centroids = [list(rows[i]["vector"]), list(rows[j]["vector"])]
    assignments = None

    for iteration in range(1, MAX_ITERATIONS + 1):
        new_assignments = []
        for row in rows:
            ds = [euclidean(row["vector"], c) for c in centroids]
            if abs(ds[0] - ds[1]) < 1e-12:
                choice = 0 if row["episode_id"] <= rows[j]["episode_id"] else 1
            else:
                choice = 0 if ds[0] < ds[1] else 1
            new_assignments.append(choice)

        if assignments == new_assignments:
            return assignments, centroids, iteration

        assignments = new_assignments
        groups = [
            [rows[n]["vector"] for n, a in enumerate(assignments) if a == c]
            for c in range(K)
        ]

        if any(len(g) == 0 for g in groups):
            raise RuntimeError("empty cluster under frozen initialization")

        centroids = [mean_vector(g) for g in groups]

    return assignments, centroids, MAX_ITERATIONS


def main(argv):
    if len(argv) != 3:
        print(
            f"Usage: {Path(argv[0]).name} TRANSITIONS.json CLUSTERS.json",
            file=sys.stderr,
        )
        return 2

    transitions = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    eligible = []

    for ep in transitions["episodes"]:
        if ep.get("sign_class") != "COLD":
            continue
        if ep.get("transition_class") == "INSUFFICIENT_CONTEXT":
            continue
        eligible.append({
            "episode_id": ep["episode_id"],
            "start": ep["start"],
            "end": ep["end"],
            "mismatch_count": ep["mismatch_count"],
            "duration_minutes": ep["duration_minutes"],
            "episode_shift_z": ep["episode_shift_z"],
            "post_shift_z": ep["post_shift_z"],
            "max_robust_z": ep["max_robust_z"],
            "features_raw": raw_features(ep),
        })

    eligible.sort(key=lambda x: x["episode_id"])
    normalization = normalize(eligible)
    assignments, centroids, iterations = cluster(eligible)

    for row, assignment in zip(eligible, assignments):
        row["cluster"] = f"CLUSTER_{assignment}"

    result = {
        "clustering": {
            "k": K,
            "features": FEATURES,
            "normalization": "median + 1.4826*MAD",
            "distance": "euclidean",
            "initialization": "farthest_pair",
            "max_iterations": MAX_ITERATIONS,
            "iterations_used": iterations,
            "label_input": False,
        },
        "normalization": normalization,
        "centroids": {
            f"CLUSTER_{i}": centroids[i]
            for i in range(K)
        },
        "eligible_cold_episode_count": len(eligible),
        "episodes": eligible,
    }

    Path(argv[2]).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"clustered {len(eligible)} COLD episodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
