# Experiment 049 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS

Focused verification:
run_id = 37237702196
conclusion = success

## Components validated

`core/revision/candidates.py`
`core/revision/nulls.py`

## Validated behaviors

- temporal/directional mismatch structure generated direction-specific and temporal-lag candidates;
- temporal candidates received majority-state, time-shift/permutation, and search-boundary protection;
- threshold uncertainty generated a threshold-refinement candidate and threshold-perturbation null;
- local residual structure generated a local-exception candidate requiring new untouched transfer;
- class imbalance generated a simpler-baseline comparator with majority and simpler-rule nulls;
- unknown structure generated `OPEN_DECOMPOSITION` and no invented null model;
- preregistration templates require discovery/confirmation separation;
- unresolved rows are not counted as success.

## Architectural conclusion

The core revision subsystem can now generate conservative candidate templates and select matching null protections from explicit structural metadata.

Candidate generation remains semantics-conservative: it does not invent domain-specific mechanisms.

## Current boundary

The subsystem can propose candidate families and null specifications, but domain adapters must still compute actual candidate parameters and null metrics on data.
