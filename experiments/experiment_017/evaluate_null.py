#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path

DATASET_KEY = "realKnownCause/ambient_temperature_system_failure.csv"
P_VALUE_GATE = 0.01
QUANTILE = 0.99
DETECTOR_WINDOW = 288


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def load_scored_timestamps(path: Path):
    rows=[]
    with path.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for row in reader:
            rows.append(parse_ts(row["timestamp"]))
    return rows[DETECTOR_WINDOW:]


def inside(t, windows):
    return any(a <= t <= b for a,b in windows)


def hypergeom_pmf_start(N,K,n,x):
    # log-combination form avoids huge intermediate integers.
    def logc(a,b):
        if b < 0 or b > a:
            return float("-inf")
        return math.lgamma(a+1)-math.lgamma(b+1)-math.lgamma(a-b+1)
    return math.exp(logc(K,x)+logc(N-K,n-x)-logc(N,n))


def hypergeom_distribution(N,K,n):
    lo=max(0,n-(N-K))
    hi=min(n,K)
    probs=[]
    p=hypergeom_pmf_start(N,K,n,lo)
    probs.append((lo,p))
    x=lo
    while x < hi:
        num=(K-x)*(n-x)
        den=(x+1)*(N-K-n+x+1)
        p = p * num / den if den else 0.0
        x += 1
        probs.append((x,p))
    total=sum(p for _,p in probs)
    if total <= 0:
        raise RuntimeError("invalid hypergeometric normalization")
    return [(x,p/total) for x,p in probs]


def quantile_hit_count(dist,q):
    c=0.0
    for x,p in dist:
        c += p
        if c >= q:
            return x
    return dist[-1][0]


def main(argv):
    if len(argv)!=5:
        print(f"Usage: {Path(argv[0]).name} DATA.csv PREDICTIONS.json LABELS.json RESULT.json",file=sys.stderr)
        return 2

    data_path=Path(argv[1])
    predictions=json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    labels=json.loads(Path(argv[3]).read_text(encoding="utf-8"))
    windows=[(parse_ts(a),parse_ts(b)) for a,b in labels[DATASET_KEY]]

    scored=load_scored_timestamps(data_path)
    N=len(scored)
    K=sum(1 for t in scored if inside(t,windows))
    mismatch_times=[parse_ts(x["timestamp"]) for x in predictions["mismatches"]]
    n=len(mismatch_times)
    X=sum(1 for t in mismatch_times if inside(t,windows))

    dist=hypergeom_distribution(N,K,n)
    p_tail=sum(p for x,p in dist if x >= X)
    p99_hits=quantile_hit_count(dist,QUANTILE)

    observed_precision=X/n if n else 0.0
    null_mean_precision=K/N if N else 0.0
    null_p99_precision=p99_hits/n if n else 0.0
    enrichment=observed_precision/null_mean_precision if null_mean_precision else None

    scientific_pass=(
        n > 0
        and observed_precision > null_p99_precision
        and p_tail < P_VALUE_GATE
    )

    result={
        "dataset_key":DATASET_KEY,
        "N_scored":N,
        "K_scored_inside_windows":K,
        "n_detector_mismatches":n,
        "X_mismatches_inside_windows":X,
        "observed_precision":observed_precision,
        "null_mean_precision":null_mean_precision,
        "null_p99_hit_count":p99_hits,
        "null_p99_precision":null_p99_precision,
        "precision_enrichment_over_null_mean":enrichment,
        "one_sided_null_p":p_tail,
        "success_gate":{
            "observed_precision_strictly_above_null_p99":True,
            "one_sided_null_p_max_exclusive":P_VALUE_GATE
        },
        "primary_scientific_result":"PASS" if scientific_pass else "FAIL"
    }

    Path(argv[4]).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
