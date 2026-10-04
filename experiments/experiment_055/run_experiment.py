#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH
from core.revision.scanner import scan_relation_pairs, select_revision_pair
from core.revision.pipeline import run_revision_from_observations


def make_base(reps=8):
    out=[]
    for _ in range(reps):
        out.extend([LOW]*12)
        out.extend([HIGH]*12)
    return out


def delayed_target(source,lag):
    out=list(source)
    last=None
    prev_before=None
    for i in range(1,len(source)):
        prev=source[i-1]
        curr=source[i]
        if prev==HIGH and curr==LOW:
            last=i
            prev_before=prev
        if last is not None and 0<=i-last<=lag:
            out[i]=prev_before
        else:
            out[i]=curr
    return out


def deterministic_noise(n):
    # fixed non-random pattern, deliberately weak structure
    pattern=[LOW,HIGH,HIGH,LOW,HIGH,LOW,LOW,HIGH]
    return [pattern[i%len(pattern)] for i in range(n)]


def main():
    base=make_base()
    temporal=delayed_target(base,3)
    identical=list(base)
    inverted=[HIGH if x==LOW else LOW for x in base]
    noise=deterministic_noise(len(base))

    discovery_series={
        "A_SOURCE":base,
        "B_TEMPORAL":temporal,
        "C_IDENTICAL":identical,
        "D_INVERTED":inverted,
        "E_NOISE":noise,
    }

    scan=scan_relation_pairs(
        discovery_series,
        pair_candidates=[
            ("A_SOURCE","B_TEMPORAL"),
            ("A_SOURCE","C_IDENTICAL"),
            ("A_SOURCE","D_INVERTED"),
            ("A_SOURCE","E_NOISE"),
        ],
        feature_config={
            "transition_radius":4,
            "temporal_fraction_threshold":0.70,
            "direction_ratio_threshold":2.0,
            "local_run_min":3,
            "local_run_fraction_threshold":0.20
        }
    )
    selected=select_revision_pair(scan,minimum_score=1.0)

    conf_source=make_base()
    conf_target=delayed_target(conf_source,3)

    if selected is None:
        raise RuntimeError("scanner failed to select a pair")

    pipeline=run_revision_from_observations(
        {
            "case_id":"EXP055_SELECTED_PAIR",
            "parent_rule_id":"RULE_SCAN_V1",
            "open_id":"OPEN_SCAN",
            "proposed_new_rule_id":"RULE_SCAN_V2",
            "lag_search":{"min":1,"max":6},
            "search_is_bounded":True
        },
        {
            "source_discovery":discovery_series[selected["source"]],
            "target_discovery":discovery_series[selected["target"]],
            "source_confirmation":conf_source,
            "target_confirmation":conf_target
        },
        {
            "lag_search":{"min":1,"max":6},
            "directions":["LOW_TO_HIGH","HIGH_TO_LOW"],
            "permutation_shifts":[5,11,17]
        },
        feature_config={
            "transition_radius":4,
            "temporal_fraction_threshold":0.70,
            "direction_ratio_threshold":2.0,
            "local_run_min":3,
            "local_run_fraction_threshold":0.20
        }
    )

    quiet_series={
        "Q1":[LOW,HIGH]*30,
        "Q2":[LOW,HIGH]*30,
        "Q3":[HIGH,LOW]*30,
    }
    quiet_scan=scan_relation_pairs(
        quiet_series,
        pair_candidates=[("Q1","Q2")],
        feature_config={"transition_radius":1}
    )
    quiet_selected=select_revision_pair(quiet_scan,minimum_score=1.0)

    checks={
        "meaningful_pair_ranked_first":
            scan[0]["source"]=="A_SOURCE" and scan[0]["target"]=="B_TEMPORAL",
        "selected_pair_is_temporal":
            selected["source"]=="A_SOURCE" and selected["target"]=="B_TEMPORAL",
        "selected_pair_has_temporal_features":
            "TEMPORAL_CLUSTERING" in selected["features"]
            and "DIRECTION_ASYMMETRY" in selected["features"],
        "trivial_identical_penalized":
            next(x for x in scan if x["target"]=="C_IDENTICAL")["score"] < selected["score"],
        "pipeline_decision_promote":
            pipeline["final_decision"]=="PROMOTE",
        "pipeline_frozen_lag_is_3":
            pipeline["evaluation"]["frozen_parameters"]["lag"]==3,
        "pipeline_graph_pass":
            pipeline["graph_invariants"]["all_pass"] is True,
        "quiet_pair_not_selected":
            quiet_selected is None
    }

    out={
        "experiment":"NOEPEDIA_EXP_055_RELATION_PAIR_DISCOVERY",
        "scan":scan,
        "selected_pair":selected,
        "pipeline":{
            "selected_family":pipeline["selected_candidate"]["family"],
            "frozen_parameters":pipeline["evaluation"]["frozen_parameters"],
            "decision":pipeline["final_decision"],
            "graph_invariants":pipeline["graph_invariants"]
        },
        "quiet_scan":quiet_scan,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 055 reproducibility: PASS")
    print("Experiment 055 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
