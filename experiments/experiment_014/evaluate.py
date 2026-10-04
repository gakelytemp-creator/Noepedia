#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DATASET_KEY = "realKnownCause/machine_temperature_system_failure.csv"
MIN_EPISODES_PER_CLUSTER = 3
SILHOUETTE_GATE = 0.35
CENTROID_DISTANCE_GATE = 2.0


def parse_ts(value):
    return datetime.fromisoformat(value)


def overlaps(ep, window):
    s = parse_ts(ep["start"])
    e = parse_ts(ep["end"])
    a = parse_ts(window[0])
    b = parse_ts(window[1])
    return s <= b and e >= a


def euclidean(a, b):
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))


def silhouette(rows):
    if len(rows) < 3:
        return 0.0

    clusters = defaultdict(list)
    for i, row in enumerate(rows):
        clusters[row["cluster"]].append(i)

    if len(clusters) != 2:
        return 0.0

    scores = []
    for i, row in enumerate(rows):
        own = clusters[row["cluster"]]
        other_key = next(k for k in clusters if k != row["cluster"])
        other = clusters[other_key]

        if len(own) <= 1:
            a = 0.0
        else:
            a = sum(
                euclidean(row["vector"], rows[j]["vector"])
                for j in own if j != i
            ) / (len(own)-1)

        b = sum(
            euclidean(row["vector"], rows[j]["vector"])
            for j in other
        ) / len(other)

        denom = max(a, b)
        scores.append((b-a)/denom if denom > 0 else 0.0)

    return sum(scores)/len(scores)


def med(values):
    return statistics.median(values) if values else None


def evaluate(clusters_doc, labels):
    windows = labels[DATASET_KEY]

    outside = [
        ep for ep in clusters_doc["episodes"]
        if not any(overlaps(ep, w) for w in windows)
    ]

    by_cluster = defaultdict(list)
    for ep in outside:
        by_cluster[ep["cluster"]].append(ep)

    cluster_counts = {
        name: len(by_cluster.get(name, []))
        for name in ["CLUSTER_0", "CLUSTER_1"]
    }

    point_counts = {
        name: sum(ep["mismatch_count"] for ep in by_cluster.get(name, []))
        for name in ["CLUSTER_0", "CLUSTER_1"]
    }

    sil = silhouette(outside)
    c0 = clusters_doc["centroids"]["CLUSTER_0"]
    c1 = clusters_doc["centroids"]["CLUSTER_1"]
    centroid_distance = euclidean(c0, c1)

    profiles = {}
    for name in ["CLUSTER_0", "CLUSTER_1"]:
        eps = by_cluster.get(name, [])
        profiles[name] = {
            "episode_count": len(eps),
            "mismatch_point_count": sum(ep["mismatch_count"] for ep in eps),
            "median_mismatch_count": med([ep["mismatch_count"] for ep in eps]),
            "median_duration_minutes": med([ep["duration_minutes"] for ep in eps]),
            "median_episode_shift_z": med([ep["episode_shift_z"] for ep in eps]),
            "median_post_shift_z": med([ep["post_shift_z"] for ep in eps]),
            "median_max_robust_z": med([ep["max_robust_z"] for ep in eps]),
        }

    nontrivial = all(
        cluster_counts[name] >= MIN_EPISODES_PER_CLUSTER
        for name in ["CLUSTER_0", "CLUSTER_1"]
    )

    scientific_pass = (
        nontrivial
        and sil >= SILHOUETTE_GATE
        and centroid_distance >= CENTROID_DISTANCE_GATE
    )

    return {
        "dataset_key": DATASET_KEY,
        "outside_only_cold_episode_count": len(outside),
        "cluster_episode_counts": cluster_counts,
        "cluster_mismatch_point_counts": point_counts,
        "silhouette_score": sil,
        "centroid_distance": centroid_distance,
        "cluster_profiles": profiles,
        "success_gate": {
            "min_episodes_per_cluster": MIN_EPISODES_PER_CLUSTER,
            "silhouette_score_min": SILHOUETTE_GATE,
            "centroid_distance_min": CENTROID_DISTANCE_GATE,
        },
        "scientific_result": "PASS" if scientific_pass else "FAIL",
        "outside_cold_episodes": outside,
    }


def main(argv):
    if len(argv) != 4:
        print(
            f"Usage: {Path(argv[0]).name} CLUSTERS.json LABELS.json RESULT.json",
            file=sys.stderr,
        )
        return 2

    clusters_doc = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    labels = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    result = evaluate(clusters_doc, labels)

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
