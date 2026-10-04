#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from itertools import combinations
from typing import Any


@dataclass(frozen=True)
class RelationScopePolicy:
    mode:str="ALL_RELATIONS"
    include:list[str]|None=None
    exclude:list[str]|None=None
    explicit_pairs:list[tuple[str,str]]|None=None

    def resolve(self, events:list[dict[str,Any]]) -> dict[str,Any]:
        present=sorted({str(e["relation_id"]) for e in events})
        include=set(self.include or present)
        exclude=set(self.exclude or [])
        relation_ids=[r for r in present if r in include and r not in exclude]

        if self.mode=="EXPLICIT_RELATIONS":
            relation_ids=[r for r in (self.include or []) if r in present and r not in exclude]
        elif self.mode!="ALL_RELATIONS":
            raise ValueError(f"unsupported relation scope mode {self.mode!r}")

        pairs=self.explicit_pairs
        if pairs is None:
            pairs=list(combinations(relation_ids,2))
        else:
            pairs=[
                (a,b) for a,b in pairs
                if a in relation_ids and b in relation_ids and a!=b
            ]
        return {"relation_ids":relation_ids,"pair_candidates":pairs}


@dataclass(frozen=True)
class TimelinePolicy:
    mode:str="INTEGER_RANGE_FROM_EVENTS"
    explicit_timeline:list[Any]|None=None

    def resolve(self, events:list[dict[str,Any]]) -> list[Any]:
        if self.mode=="EXPLICIT":
            if self.explicit_timeline is None:
                raise ValueError("EXPLICIT timeline policy requires explicit_timeline")
            return list(self.explicit_timeline)

        times=sorted({e["time"] for e in events})
        if not times:
            return []

        if self.mode=="EVENT_TIMES_ONLY":
            return times

        if self.mode=="INTEGER_RANGE_FROM_EVENTS":
            if not all(isinstance(t,int) for t in times):
                raise ValueError("INTEGER_RANGE_FROM_EVENTS requires integer event times")
            return list(range(min(times),max(times)+1))

        raise ValueError(f"unsupported timeline policy {self.mode!r}")


@dataclass(frozen=True)
class SplitPolicy:
    discovery_fraction:float=0.625
    buffer_fraction:float=0.125
    minimum_confirmation_count:int=10

    def resolve(self, timeline:list[Any]) -> dict[str,int]:
        n=len(timeline)
        if n<=0:
            raise ValueError("cannot split empty timeline")
        if not (0.0<self.discovery_fraction<1.0):
            raise ValueError("discovery_fraction must be between 0 and 1")
        if not (0.0<=self.buffer_fraction<1.0):
            raise ValueError("buffer_fraction must be between 0 and 1")

        discovery_end=max(1,int(n*self.discovery_fraction))
        confirmation_start=min(n,discovery_end+int(n*self.buffer_fraction))

        if n-confirmation_start < self.minimum_confirmation_count:
            confirmation_start=max(discovery_end,n-self.minimum_confirmation_count)

        if confirmation_start<discovery_end or confirmation_start>=n:
            raise ValueError("split policy leaves insufficient confirmation data")

        return {
            "discovery_end_index":discovery_end,
            "confirmation_start_index":confirmation_start
        }


@dataclass(frozen=True)
class SearchPolicy:
    lag_min:int=1
    lag_max_fraction:float=0.10
    lag_max_cap:int=100
    permutation_shift_fractions:tuple[float,...]=(0.10,0.20,0.30,0.40)
    minimum_pair_score:float=1.0
    max_forward_fill_fraction:float=0.10
    required_relative_advantage:float=0.10

    def resolve(self, discovery_count:int) -> dict[str,Any]:
        if discovery_count<=0:
            raise ValueError("discovery_count must be positive")
        lag_max=max(self.lag_min,int(discovery_count*self.lag_max_fraction))
        lag_max=min(lag_max,self.lag_max_cap)

        shifts=[]
        for frac in self.permutation_shift_fractions:
            s=max(1,int(discovery_count*frac))
            if s not in shifts:
                shifts.append(s)

        max_ff=max(1,int(discovery_count*self.max_forward_fill_fraction))

        return {
            "feature_config":{
                "transition_radius":max(1,min(5,lag_max)),
                "temporal_fraction_threshold":0.70,
                "direction_ratio_threshold":2.0,
                "local_run_min":3,
                "local_run_fraction_threshold":0.20
            },
            "evaluator_config":{
                "lag_search":{"min":self.lag_min,"max":lag_max},
                "directions":["LOW_TO_HIGH","HIGH_TO_LOW"],
                "permutation_shifts":shifts
            },
            "minimum_pair_score":self.minimum_pair_score,
            "max_forward_fill_steps":max_ff,
            "required_relative_advantage":self.required_relative_advantage
        }


@dataclass(frozen=True)
class RevisionStrategy:
    relation_scope:RelationScopePolicy=RelationScopePolicy()
    timeline:TimelinePolicy=TimelinePolicy()
    split:SplitPolicy=SplitPolicy()
    search:SearchPolicy=SearchPolicy()

    def resolve(self, events:list[dict[str,Any]]) -> dict[str,Any]:
        scope=self.relation_scope.resolve(events)
        timeline=self.timeline.resolve(events)
        split=self.split.resolve(timeline)
        discovery_count=split["discovery_end_index"]
        search=self.search.resolve(discovery_count)
        return {
            "scope":scope,
            "timeline":timeline,
            "split":split,
            "search":search,
            "policy":{
                "relation_scope":asdict(self.relation_scope),
                "timeline":asdict(self.timeline),
                "split":asdict(self.split),
                "search":asdict(self.search)
            }
        }


DEFAULT_REVISION_STRATEGY=RevisionStrategy()
