#!/usr/bin/env python3
from __future__ import annotations
from typing import Any

from .megagraph_adapter import materialize_state_series, split_series_by_time
from .scanner import scan_relation_pairs, select_revision_pair
from .pipeline import run_revision_from_observations


def run_graph_native_revision(
    *,
    events:list[dict[str,Any]],
    relation_ids:list[str],
    timeline:list[Any],
    discovery_end_index:int,
    confirmation_start_index:int,
    parent_rule_id:str,
    open_id:str,
    proposed_new_rule_id:str|None=None,
    pair_candidates:list[tuple[str,str]]|None=None,
    feature_config:dict[str,Any]|None=None,
    evaluator_config:dict[str,Any]|None=None,
    minimum_pair_score:float=1.0,
    max_forward_fill_steps:int|None=None,
    required_relative_advantage:float=0.10,
) -> dict[str,Any]:
    adapted=materialize_state_series(
        events,
        relation_ids=relation_ids,
        timeline=timeline,
        initial_state_policy="DROP_UNTIL_ALL_KNOWN",
        max_forward_fill_steps=max_forward_fill_steps,
    )
    split=split_series_by_time(
        adapted,
        discovery_end_index=discovery_end_index,
        confirmation_start_index=confirmation_start_index,
    )

    scan=scan_relation_pairs(
        split["discovery"]["series"],
        pair_candidates=pair_candidates,
        feature_config=feature_config or {},
    )
    selected=select_revision_pair(scan,minimum_score=minimum_pair_score)

    if selected is None:
        return {
            "record_type":"GRAPH_NATIVE_REVISION_RUN",
            "adapter":adapted,
            "split":split,
            "scan":scan,
            "selected_pair":None,
            "revision":None,
            "final_decision":"REMAIN_OPEN",
            "decision_reason":"NO_ELIGIBLE_RELATION_PAIR",
        }

    src=selected["source"]
    tgt=selected["target"]

    context={
        "case_id":f"GRAPH_NATIVE::{src}::{tgt}",
        "parent_rule_id":parent_rule_id,
        "open_id":open_id,
        "proposed_new_rule_id":proposed_new_rule_id or (parent_rule_id+"::NEXT"),
        "lag_search":(evaluator_config or {}).get("lag_search",{"min":1,"max":100}),
        "search_is_bounded":True,
    }
    data={
        "source_discovery":split["discovery"]["series"][src],
        "target_discovery":split["discovery"]["series"][tgt],
        "source_confirmation":split["confirmation"]["series"][src],
        "target_confirmation":split["confirmation"]["series"][tgt],
    }

    revision=run_revision_from_observations(
        context,
        data,
        evaluator_config or {},
        feature_config=feature_config or {},
        required_relative_advantage=required_relative_advantage,
    )

    return {
        "record_type":"GRAPH_NATIVE_REVISION_RUN",
        "adapter":adapted,
        "split":split,
        "scan":scan,
        "selected_pair":selected,
        "revision":revision,
        "final_decision":revision["final_decision"],
        "decision_reason":revision["gate_audit"]["decision_reason"],
    }
