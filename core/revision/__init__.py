"""Noepedia revision subsystem."""

from .engine import evaluate_case
from .materializer import materialize, verify_invariants
from .candidates import generate_candidates, rank_candidates
from .nulls import select_nulls, build_preregistration_template
from .evaluator import evaluate_candidate, evaluate_temporal_candidate, evaluate_threshold_candidate, evaluate_orientation_candidate, evaluate_local_exception_candidate, evaluate_simpler_rule_comparator
from .pipeline import run_revision, build_gate_case, run_revision_from_observations
from .features import extract_mismatch_features, enrich_context_from_observations
from .scanner import scan_relation_pairs, select_revision_pair, score_pair
from .megagraph_adapter import normalize_history_events, build_common_timeline, materialize_state_series, split_series_by_time
from .graph_pipeline import run_graph_native_revision, run_graph_native_revision_with_strategy, run_graph_native_revision_auto_strategy
from .strategies import RelationScopePolicy, TimelinePolicy, SplitPolicy, SearchPolicy, RevisionStrategy, DEFAULT_REVISION_STRATEGY
from .meta_policy import profile_history, select_revision_strategy, dense_strategy, sparse_strategy, conservative_strategy

__all__ = [
    "evaluate_case",
    "materialize",
    "verify_invariants",
    "generate_candidates",
    "rank_candidates",
    "select_nulls",
    "build_preregistration_template",
    "evaluate_candidate",
    "evaluate_temporal_candidate",
    "evaluate_threshold_candidate",
    "evaluate_orientation_candidate",
    "evaluate_local_exception_candidate",
    "evaluate_simpler_rule_comparator",
    "run_revision",
    "build_gate_case",
    "run_revision_from_observations",
    "extract_mismatch_features",
    "enrich_context_from_observations",
    "scan_relation_pairs",
    "select_revision_pair",
    "score_pair",
    "normalize_history_events",
    "build_common_timeline",
    "materialize_state_series",
    "split_series_by_time",
    "run_graph_native_revision",
    "run_graph_native_revision_with_strategy",
    "run_graph_native_revision_auto_strategy",
    "RelationScopePolicy",
    "TimelinePolicy",
    "SplitPolicy",
    "SearchPolicy",
    "RevisionStrategy",
    "DEFAULT_REVISION_STRATEGY",
    "profile_history",
    "select_revision_strategy",
    "dense_strategy",
    "sparse_strategy",
    "conservative_strategy",
]
