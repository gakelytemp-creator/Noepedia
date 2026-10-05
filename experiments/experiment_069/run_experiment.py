#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

EXP068=ROOT/"experiments"/"experiment_068"
RESULT068=EXP068/"_runtime"/"result.json"

NON_METRIC_NULLS={"SEARCH_BOUNDARY_CHECK","OUT_OF_CLUSTER_TRANSFER_TEST"}

SUPPORTED_METRICS={
    "TEMPORAL_LAG_REVISION":{
        "MAJORITY_STATE_NULL",
        "TIME_SHIFT_OR_PERMUTATION_NULL",
    },
    "DIRECTION_SPECIFIC_RULE":{
        "MAJORITY_STATE_NULL",
        "TIME_SHIFT_OR_PERMUTATION_NULL",
    },
    "RELATION_ORIENTATION_REVISION":{
        "MAJORITY_STATE_NULL",
    },
    "THRESHOLD_REFINEMENT":{
        "THRESHOLD_PERTURBATION_NULL",
    },
    "SIMPLER_RULE_COMPARATOR":{
        "MAJORITY_STATE_NULL",
        "SIMPLER_RULE_NULL",
    },
    "LOCAL_EXCEPTION_CANDIDATE":set(),
    "OPEN_DECOMPOSITION":set(),
}

def load_exp068():
    spec=importlib.util.spec_from_file_location("exp068_runner",EXP068/"run_experiment.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Experiment 068 runner")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def audit_rows(rows):
    audited=[]
    for r in rows:
        family=r.get("selected_family")
        demanded=set(r.get("nulls",[]))
        supported=SUPPORTED_METRICS.get(family,set())
        metric_nulls=demanded-NON_METRIC_NULLS
        missing=sorted(metric_nulls-supported)
        audited.append({
            "pair_index":r.get("pair_index"),
            "source":r.get("source"),
            "target":r.get("target"),
            "family":family,
            "decision":r.get("final_decision"),
            "decision_reason":r.get("decision_reason"),
            "selected_nulls":sorted(demanded),
            "missing_required_metric_nulls":missing,
            "null_metric_coverage_gap":bool(missing),
            "frozen_parameters":r.get("frozen_parameters")
        })
    return audited

def summarize(rows):
    return {
        "pair_count":len(rows),
        "decision_counts":dict(Counter(r["decision"] for r in rows)),
        "decision_reason_counts":dict(Counter(r["decision_reason"] for r in rows)),
        "family_counts":dict(Counter(r["family"] for r in rows)),
        "null_metric_coverage_gap_count":sum(r["null_metric_coverage_gap"] for r in rows),
        "missing_null_counts":dict(Counter(
            n for r in rows for n in r["missing_required_metric_nulls"]
        ))
    }

def main():
    exp068=load_exp068()
    rc=exp068.main()
    if rc!=0:
        raise RuntimeError(f"Experiment 068 replay failed with rc={rc}")
    source=json.loads(RESULT068.read_text(encoding="utf-8"))

    if source.get("primary_class")!="NO_REAL_PROMOTION_AND_SHUFFLED_ZERO":
        raise RuntimeError("Experiment 068 replay did not reproduce frozen primary class")

    real=audit_rows(source["real_pair_results"])
    shuffled=audit_rows(source["shuffled_pair_results"])

    out={
        "experiment":"NOEPEDIA_EXP_069_PROMOTION_BOTTLENECK_AUDIT",
        "source_experiment":"NOEPEDIA_EXP_068_STABLE_WINDOW_BLIND_DISCOVERY",
        "source_primary_class":source["primary_class"],
        "source_real_promotion_count":source["real_promotion_count"],
        "source_shuffled_promotion_count":source["shuffled_promotion_count"],
        "real_summary":summarize(real),
        "shuffled_summary":summarize(shuffled),
        "real_pairs":real,
        "shuffled_pairs":shuffled,
        "scientific_result_mutated":False
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
