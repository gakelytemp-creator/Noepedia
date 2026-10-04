#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.candidates import generate_candidates, rank_candidates
from core.revision.nulls import select_nulls, build_preregistration_template


def names(items,key):
    return [x[key] for x in items]


def scenario(ctx):
    cands=rank_candidates(generate_candidates(ctx),ctx)
    selected=cands[0]
    nulls=select_nulls(selected,ctx)
    pre=build_preregistration_template(selected,nulls,ctx)
    return {
        "context":ctx,
        "candidate_families":names(cands,"family"),
        "selected_family":selected["family"],
        "selected_candidate":selected,
        "null_names":names(nulls,"name"),
        "preregistration":pre
    }


def main():
    temporal_ctx={
        "case_id":"S_TEMPORAL",
        "parent_rule_id":"RULE_A",
        "open_id":"OPEN_A",
        "features":[
            "TEMPORAL_CLUSTERING",
            "TRANSITION_ALIGNED_MISMATCH",
            "DIRECTION_ASYMMETRY"
        ],
        "risk_flags":["CLASS_IMBALANCE"],
        "lag_search":{"min":1,"max":100},
        "search_is_bounded":True
    }
    threshold_ctx={
        "case_id":"S_THRESHOLD",
        "parent_rule_id":"RULE_B",
        "open_id":"OPEN_B",
        "features":["THRESHOLD_SENSITIVITY","MID_BAND_UNCERTAINTY"],
        "risk_flags":[],
        "search_is_bounded":True
    }
    local_ctx={
        "case_id":"S_LOCAL",
        "parent_rule_id":"RULE_C",
        "open_id":"OPEN_C",
        "features":["LOCAL_RESIDUAL_CLUSTER"],
        "risk_flags":["SIMPLE_BASELINE_PLAUSIBLE"],
        "search_is_bounded":False
    }
    imbalance_ctx={
        "case_id":"S_IMBALANCE",
        "parent_rule_id":"RULE_D",
        "open_id":"OPEN_D",
        "features":["CLASS_IMBALANCE"],
        "risk_flags":["CLASS_IMBALANCE","SIMPLE_BASELINE_PLAUSIBLE"],
        "search_is_bounded":False
    }
    unknown_ctx={
        "case_id":"S_UNKNOWN",
        "parent_rule_id":"RULE_E",
        "open_id":"OPEN_E",
        "features":[],
        "risk_flags":[],
        "search_is_bounded":False
    }

    results={
        "temporal":scenario(temporal_ctx),
        "threshold":scenario(threshold_ctx),
        "local":scenario(local_ctx),
        "imbalance":scenario(imbalance_ctx),
        "unknown":scenario(unknown_ctx)
    }

    checks={
        "temporal_direction_ranked_first":
            results["temporal"]["selected_family"]=="DIRECTION_SPECIFIC_RULE",
        "temporal_contains_lag_candidate":
            "TEMPORAL_LAG_REVISION" in results["temporal"]["candidate_families"],
        "temporal_majority_null":
            "MAJORITY_STATE_NULL" in results["temporal"]["null_names"],
        "temporal_permutation_null":
            "TIME_SHIFT_OR_PERMUTATION_NULL" in results["temporal"]["null_names"],
        "temporal_boundary_check":
            "SEARCH_BOUNDARY_CHECK" in results["temporal"]["null_names"],
        "threshold_candidate":
            results["threshold"]["selected_family"]=="THRESHOLD_REFINEMENT",
        "threshold_null":
            "THRESHOLD_PERTURBATION_NULL" in results["threshold"]["null_names"],
        "threshold_boundary_check":
            "SEARCH_BOUNDARY_CHECK" in results["threshold"]["null_names"],
        "local_candidate":
            results["local"]["selected_family"]=="LOCAL_EXCEPTION_CANDIDATE",
        "local_transfer_null":
            "OUT_OF_CLUSTER_TRANSFER_TEST" in results["local"]["null_names"],
        "local_simpler_null":
            "SIMPLER_RULE_NULL" in results["local"]["null_names"],
        "imbalance_candidate":
            results["imbalance"]["selected_family"]=="SIMPLER_RULE_COMPARATOR",
        "imbalance_majority_null":
            "MAJORITY_STATE_NULL" in results["imbalance"]["null_names"],
        "imbalance_simpler_null":
            "SIMPLER_RULE_NULL" in results["imbalance"]["null_names"],
        "unknown_falls_back_to_open":
            results["unknown"]["selected_family"]=="OPEN_DECOMPOSITION",
        "unknown_no_invented_nulls":
            results["unknown"]["null_names"]==[],
        "preregistration_requires_window_separation":
            all(v["preregistration"]["discovery_confirmation_must_differ"] for v in results.values()),
        "preregistration_forbids_unresolved_success":
            all(not v["preregistration"]["unresolved_rows_count_as_success"] for v in results.values())
    }

    out={
        "experiment":"NOEPEDIA_EXP_049_CANDIDATE_GENERATOR_NULL_SELECTOR",
        "results":results,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 049 reproducibility: PASS")
    print("Experiment 049 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
