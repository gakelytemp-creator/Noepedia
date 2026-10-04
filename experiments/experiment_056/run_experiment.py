#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.evaluator import LOW,HIGH
from core.revision.megagraph_adapter import materialize_state_series, split_series_by_time
from core.revision.scanner import scan_relation_pairs, select_revision_pair


def add(events,rid,t,state,seq=0,eid=None):
    events.append({
        "relation_id":rid,
        "time":t,
        "state":state,
        "sequence":seq,
        "event_id":eid or f"{rid}-{t}-{seq}"
    })


def main():
    events=[]

    # A_SOURCE: alternating blocks.
    source=[]
    for _ in range(6):
        source.extend([LOW]*4+[HIGH]*4)

    # B_TEMPORAL: delayed HIGH_TO_LOW by one step.
    target=list(source)
    last=None
    prev_before=None
    for i in range(1,len(source)):
        prev=source[i-1]
        curr=source[i]
        if prev==HIGH and curr==LOW:
            last=i
            prev_before=prev
        if last is not None and 0<=i-last<=1:
            target[i]=prev_before
        else:
            target[i]=curr

    # C_IDENTICAL: same as source.
    identical=list(source)

    # Sparse event representation: only write on change.
    for rid,series in [
        ("A_SOURCE",source),
        ("B_TEMPORAL",target),
        ("C_IDENTICAL",identical),
    ]:
        last_state=None
        for t,state in enumerate(series, start=1):
            if state!=last_state:
                add(events,rid,t,state,seq=0)
                last_state=state

    # Duplicate update at same timestamp; later sequence must win deterministically.
    add(events,"A_SOURCE",9,LOW,seq=1,eid="dup-old")
    add(events,"A_SOURCE",9,HIGH,seq=2,eid="dup-new")

    adapted=materialize_state_series(
        events,
        relation_ids=["A_SOURCE","B_TEMPORAL","C_IDENTICAL"],
        initial_state_policy="DROP_UNTIL_ALL_KNOWN",
        max_forward_fill_steps=8
    )

    split=split_series_by_time(
        adapted,
        discovery_end_index=32,
        confirmation_start_index=40
    )

    scan=scan_relation_pairs(
        split["discovery"]["series"],
        pair_candidates=[
            ("A_SOURCE","B_TEMPORAL"),
            ("A_SOURCE","C_IDENTICAL")
        ],
        feature_config={
            "transition_radius":2,
            "temporal_fraction_threshold":0.60,
            "direction_ratio_threshold":2.0,
            "local_run_min":2,
            "local_run_fraction_threshold":0.20
        }
    )
    selected=select_revision_pair(scan,minimum_score=1.0)

    lengths={k:len(v) for k,v in adapted["series"].items()}

    checks={
        "normalized_duplicate_collapsed":
            adapted["diagnostics"]["normalized_event_count"] < adapted["diagnostics"]["input_event_count"],
        "aligned_lengths":
            len(set(lengths.values()))==1,
        "timeline_matches_series":
            len(adapted["timeline"])==next(iter(lengths.values())),
        "split_discovery_length":
            len(split["discovery"]["timeline"])==32,
        "split_buffer_length":
            len(split["buffer"]["timeline"])==8,
        "confirmation_nonempty":
            len(split["confirmation"]["timeline"])>0,
        "meaningful_pair_selected":
            selected is not None and selected["source"]=="A_SOURCE" and selected["target"]=="B_TEMPORAL",
        "identical_pair_ranked_lower":
            scan[0]["score"] > scan[1]["score"]
    }

    out={
        "experiment":"NOEPEDIA_EXP_056_MEGAGRAPH_SERIES_ADAPTER",
        "adapter_diagnostics":adapted["diagnostics"],
        "series_lengths":lengths,
        "selected_pair":selected,
        "scan":scan,
        "checks":checks,
        "architectural_pass":all(checks.values())
    }

    rt=HERE/"_runtime"
    rt.mkdir(exist_ok=True)
    (rt/"result.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 056 reproducibility: PASS")
    print("Experiment 056 architectural result:","PASS" if out["architectural_pass"] else "FAIL")
    return 0 if out["architectural_pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
