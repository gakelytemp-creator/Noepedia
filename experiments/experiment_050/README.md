# Experiment 050 — Generic Candidate Evaluator / Parameter Search Engine

Purpose:
validate the first generic parameter-search and null-metric engine in `core/revision/evaluator.py`.

Families covered:
- TEMPORAL_LAG_REVISION / DIRECTION_SPECIFIC_RULE
- THRESHOLD_REFINEMENT

Validation scenarios:
- interior temporal optimum with null metrics
- temporal boundary hit
- interior threshold optimum
- threshold boundary hit

Pass criteria:
- deterministic parameter selection
- correct tie-breaking
- correct boundary detection
- confirmation metrics computed with frozen discovery-selected parameters
- majority and permutation null metrics computed for temporal candidates
- threshold-perturbation null metric computed for threshold candidates
