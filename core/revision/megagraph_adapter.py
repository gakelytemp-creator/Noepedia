#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from typing import Any

VALID_STATES={"STATE_LOW","STATE_HIGH"}


def _event_sort_key(event:dict[str,Any]):
    return (
        event["time"],
        int(event.get("sequence",0)),
        str(event.get("event_id",""))
    )


def normalize_history_events(events:list[dict[str,Any]]) -> list[dict[str,Any]]:
    """Validate and deterministically collapse duplicate updates.

    Duplicate identity is (relation_id, time). The last event by
    (sequence,event_id) wins. History is not mutated.
    """
    latest={}
    for raw in events:
        event=dict(raw)
        relation_id=str(event["relation_id"])
        state=str(event["state"])
        if state not in VALID_STATES:
            raise ValueError(f"unsupported state {state!r}")
        time=event["time"]
        key=(relation_id,time)
        prev=latest.get(key)
        if prev is None or _event_sort_key(event)>_event_sort_key(prev):
            latest[key]=event

    return sorted(latest.values(),key=lambda e:(e["time"],str(e["relation_id"]),int(e.get("sequence",0)),str(e.get("event_id",""))))


def build_common_timeline(
    events:list[dict[str,Any]],
    *,
    relation_ids:list[str]|None=None,
    include_times:list[Any]|None=None,
) -> list[Any]:
    ids=set(relation_ids or [])
    times=set(include_times or [])
    for e in events:
        if not ids or str(e["relation_id"]) in ids:
            times.add(e["time"])
    return sorted(times)


def materialize_state_series(
    events:list[dict[str,Any]],
    *,
    relation_ids:list[str]|None=None,
    timeline:list[Any]|None=None,
    initial_state_policy:str="DROP_UNTIL_ALL_KNOWN",
    max_forward_fill_steps:int|None=None,
) -> dict[str,Any]:
    """Convert sparse relation histories into aligned state series.

    Policies:
    - DROP_UNTIL_ALL_KNOWN: omit leading timeline positions until every relation
      has received at least one state.
    - REQUIRE_INITIAL: fail if any relation lacks a state at the first timeline item.

    max_forward_fill_steps limits how many timeline steps an old state may be
    carried forward. When exceeded, that timestamp is dropped from all series.
    """
    normalized=normalize_history_events(events)

    ids=sorted(set(relation_ids or [str(e["relation_id"]) for e in normalized]))
    if not ids:
        return {"timeline":[],"series":{},"diagnostics":{"relation_count":0}}

    time_axis=list(timeline or build_common_timeline(normalized,relation_ids=ids))
    by_time=defaultdict(list)
    for e in normalized:
        if str(e["relation_id"]) in ids:
            by_time[e["time"]].append(e)

    current={rid:None for rid in ids}
    age={rid:None for rid in ids}
    output={rid:[] for rid in ids}
    kept_times=[]
    dropped_leading=0
    dropped_stale=0

    for t in time_axis:
        for rid in ids:
            if age[rid] is not None:
                age[rid]+=1

        for e in by_time.get(t,[]):
            rid=str(e["relation_id"])
            current[rid]=str(e["state"])
            age[rid]=0

        if initial_state_policy=="REQUIRE_INITIAL" and not kept_times and any(current[rid] is None for rid in ids):
            raise ValueError("missing initial state for one or more relations")

        if any(current[rid] is None for rid in ids):
            if initial_state_policy=="DROP_UNTIL_ALL_KNOWN":
                dropped_leading+=1
                continue
            raise ValueError(f"unsupported initial_state_policy {initial_state_policy!r}")

        if max_forward_fill_steps is not None:
            if any(age[rid] is not None and age[rid]>max_forward_fill_steps for rid in ids):
                dropped_stale+=1
                continue

        kept_times.append(t)
        for rid in ids:
            output[rid].append(current[rid])

    lengths={len(v) for v in output.values()}
    if len(lengths)>1:
        raise RuntimeError("adapter produced misaligned series")

    return {
        "timeline":kept_times,
        "series":output,
        "diagnostics":{
            "relation_count":len(ids),
            "input_event_count":len(events),
            "normalized_event_count":len(normalized),
            "input_timeline_count":len(time_axis),
            "output_timeline_count":len(kept_times),
            "dropped_leading_count":dropped_leading,
            "dropped_stale_count":dropped_stale,
            "max_forward_fill_steps":max_forward_fill_steps,
            "initial_state_policy":initial_state_policy,
        }
    }


def split_series_by_time(
    adapted:dict[str,Any],
    *,
    discovery_end_index:int,
    confirmation_start_index:int,
) -> dict[str,Any]:
    """Split aligned series without re-fitting or reordering."""
    timeline=adapted["timeline"]
    series=adapted["series"]
    n=len(timeline)
    if not (0<discovery_end_index<=confirmation_start_index<=n):
        raise ValueError("invalid split indices")

    return {
        "discovery":{
            "timeline":timeline[:discovery_end_index],
            "series":{k:v[:discovery_end_index] for k,v in series.items()},
        },
        "confirmation":{
            "timeline":timeline[confirmation_start_index:],
            "series":{k:v[confirmation_start_index:] for k,v in series.items()},
        },
        "buffer":{
            "timeline":timeline[discovery_end_index:confirmation_start_index],
            "series":{k:v[discovery_end_index:confirmation_start_index] for k,v in series.items()},
        }
    }
