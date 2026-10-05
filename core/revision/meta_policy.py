#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .strategies import (
    RevisionStrategy,
    RelationScopePolicy,
    TimelinePolicy,
    SplitPolicy,
    SearchPolicy,
)


def profile_history(events:list[dict[str,Any]]) -> dict[str,Any]:
    if not events:
        return {
            "relation_count":0,
            "event_count":0,
            "time_count":0,
            "time_span":0,
            "event_density":0.0,
            "mean_events_per_relation":0.0,
            "transition_density_proxy":0.0,
        }

    relation_ids=sorted({str(e["relation_id"]) for e in events})
    times=sorted({e["time"] for e in events})

    if all(isinstance(t,int) for t in times):
        time_span=max(times)-min(times)+1
    else:
        time_span=len(times)

    event_density=(len(events)/(len(relation_ids)*time_span)) if relation_ids and time_span else 0.0
    mean_events=len(events)/len(relation_ids) if relation_ids else 0.0

    # Sparse histories normally only record changes, so events/time acts as a transition proxy.
    transition_density=(len(events)/time_span) if time_span else 0.0

    return {
        "relation_count":len(relation_ids),
        "event_count":len(events),
        "time_count":len(times),
        "time_span":time_span,
        "event_density":event_density,
        "mean_events_per_relation":mean_events,
        "transition_density_proxy":transition_density,
    }


def dense_strategy() -> RevisionStrategy:
    return RevisionStrategy(
        relation_scope=RelationScopePolicy(mode="ALL_RELATIONS"),
        timeline=TimelinePolicy(mode="INTEGER_RANGE_FROM_EVENTS"),
        split=SplitPolicy(
            discovery_fraction=0.60,
            buffer_fraction=0.10,
            minimum_confirmation_count=20,
        ),
        search=SearchPolicy(
            lag_min=1,
            lag_max_fraction=0.08,
            lag_max_cap=50,
            permutation_shift_fractions=(0.10,0.20,0.30,0.40),
            minimum_pair_score=1.0,
            max_forward_fill_fraction=0.05,
            required_relative_advantage=0.10,
        ),
    )


def sparse_strategy() -> RevisionStrategy:
    return RevisionStrategy(
        relation_scope=RelationScopePolicy(mode="ALL_RELATIONS"),
        timeline=TimelinePolicy(mode="INTEGER_RANGE_FROM_EVENTS"),
        split=SplitPolicy(
            discovery_fraction=0.55,
            buffer_fraction=0.15,
            minimum_confirmation_count=15,
        ),
        search=SearchPolicy(
            lag_min=1,
            lag_max_fraction=0.12,
            lag_max_cap=100,
            permutation_shift_fractions=(0.10,0.25,0.40),
            minimum_pair_score=1.5,
            max_forward_fill_fraction=0.20,
            required_relative_advantage=0.10,
        ),
    )


def conservative_strategy() -> RevisionStrategy:
    return RevisionStrategy(
        relation_scope=RelationScopePolicy(mode="ALL_RELATIONS"),
        timeline=TimelinePolicy(mode="EVENT_TIMES_ONLY"),
        split=SplitPolicy(
            discovery_fraction=0.50,
            buffer_fraction=0.20,
            minimum_confirmation_count=10,
        ),
        search=SearchPolicy(
            lag_min=1,
            lag_max_fraction=0.05,
            lag_max_cap=30,
            permutation_shift_fractions=(0.20,0.40),
            minimum_pair_score=2.0,
            max_forward_fill_fraction=0.05,
            required_relative_advantage=0.15,
        ),
    )


def select_revision_strategy(events:list[dict[str,Any]]) -> dict[str,Any]:
    profile=profile_history(events)

    if profile["relation_count"]<2 or profile["event_count"]<8:
        name="CONSERVATIVE"
        strategy=conservative_strategy()
        reason="INSUFFICIENT_OR_SMALL_HISTORY"
    elif profile["event_density"]>=0.20 and profile["transition_density_proxy"]>=0.50:
        name="DENSE"
        strategy=dense_strategy()
        reason="DENSE_MULTI_RELATION_HISTORY"
    else:
        name="SPARSE"
        strategy=sparse_strategy()
        reason="SPARSE_CHANGE_EVENT_HISTORY"

    return {
        "strategy_name":name,
        "selection_reason":reason,
        "history_profile":profile,
        "strategy":strategy,
    }
