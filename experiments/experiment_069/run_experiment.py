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

def deep_metric_audit(exp068):
    runs=exp068.extract_runs(exp068.find_mat(exp068.EXTRACT))
    thresholds={}
    series={}
    for ch in exp068.CHANNELS:
        fit=exp068.fit_kmeans_1d([r[ch] for r in runs[:exp068.CAL_N]])
        thresholds[ch]=fit
        series[ch]=[exp068.state(r[ch],fit["threshold"]) for r in runs]

    from core.revision.pipeline import run_revision_from_observations
    import itertools

    audited=[]
    pair_list=list(itertools.combinations(exp068.CHANNELS,2))
    for mode in ["REAL","SHUFFLED"]:
        for i,(a,b) in enumerate(pair_list):
            cal_end=exp068.CAL_N
            disc_end=cal_end+exp068.DISC_N
            buf_end=disc_end+exp068.BUF_N
            src_d=series[a][cal_end:disc_end]
            tgt_d=series[b][cal_end:disc_end]
            src_c=series[a][buf_end:]
            tgt_c=series[b][buf_end:]
            if mode=="SHUFFLED":
                tgt_d=exp068.shuffle_copy(tgt_d,exp068.SOURCE["shuffled_control"]["discovery_seed_base"]+i)
                tgt_c=exp068.shuffle_copy(tgt_c,exp068.SOURCE["shuffled_control"]["confirmation_seed_base"]+i)

            context={
                "case_id":f"EXP069::{a}::{b}::{mode}",
                "parent_rule_id":f"RULE069::{a}::{b}::V1",
                "open_id":f"OPEN069::{a}::{b}",
                "proposed_new_rule_id":f"RULE069::{a}::{b}::V2",
                "lag_search":{"min":1,"max":8},
                "search_is_bounded":True
            }
            config={
                "lag_search":{"min":1,"max":8},
                "directions":["LOW_TO_HIGH","HIGH_TO_LOW"],
                "permutation_shifts":[7,13,19]
            }
            feature_config={
                "transition_radius":5,
                "temporal_fraction_threshold":0.70,
                "class_imbalance_threshold":0.80,
                "direction_ratio_threshold":3.0,
                "local_run_min":3,
                "local_run_fraction_threshold":0.30
            }
            data={
                "source_discovery":src_d,
                "target_discovery":tgt_d,
                "source_confirmation":src_c,
                "target_confirmation":tgt_c,
                "proposed_confirmation":src_c
            }
            try:
                r=run_revision_from_observations(
                    context,data,config,
                    feature_config=feature_config,
                    required_relative_advantage=0.10
                )
            except Exception:
                continue
            if r.get("gate_audit",{}).get("decision_reason")=="REQUIRED_NULL_UNAVAILABLE":
                audited.append({
                    "mode":mode,
                    "pair_index":i,
                    "source":a,
                    "target":b,
                    "family":r.get("selected_candidate",{}).get("family"),
                    "required_nulls":r.get("gate_case",{}).get("required_nulls",[]),
                    "evaluator_metrics":(r.get("evaluation") or {}).get("required_null_metrics",{})
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
    deep=deep_metric_audit(exp068)

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
        "required_null_unavailable_metrics":deep,
        "scientific_result_mutated":False
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
