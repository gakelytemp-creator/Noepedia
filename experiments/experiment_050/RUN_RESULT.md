# Experiment 050 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS

Focused verification:
run_id = 37238879179
conclusion = success

## Component validated

`core/revision/evaluator.py`

## Supported generic families

- TEMPORAL_LAG_REVISION
- DIRECTION_SPECIFIC_RULE
- THRESHOLD_REFINEMENT

## Validated behaviors

- deterministic temporal direction/lag search;
- discovery-only parameter selection;
- frozen-parameter confirmation evaluation;
- temporal search-boundary detection;
- majority-state null metric computation;
- time-shift/permutation null metric computation;
- deterministic threshold-grid search;
- threshold search-boundary detection;
- threshold-perturbation null metric computation.

## Important correction

The first verification run expected zero confirmation error for the threshold case.

That expectation was wrong: discovery froze threshold = 9.0, while confirmation values were deliberately shifted by +0.1.

The correct frozen-threshold confirmation result is one mismatch.

Changing the threshold on confirmation would have been forbidden retuning.

The evaluator code was unchanged; only the verification assertion was corrected.

See `CORRECTION.md`.

## Architectural conclusion

The core revision subsystem can now carry a candidate from structural template generation into deterministic parameter search and null-metric computation without using confirmation data for tuning.

## Current boundary

Generic evaluators are currently implemented only for temporal/directional and threshold candidate families.

Local-exception, relation-orientation, and richer structural candidate families still require additional evaluator plugins.
