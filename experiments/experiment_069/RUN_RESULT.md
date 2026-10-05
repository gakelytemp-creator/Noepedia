# Experiment 069 — RUN RESULT

## Status

DIAGNOSTIC PASS

Focused audit run:
`37293327142`

Source scientific experiment:
`068 — Stable-Window Blind Real-System Discovery`

Experiment 068 remains unchanged:

`NO_REAL_PROMOTION_AND_SHUFFLED_ZERO`

`scientific_result_mutated = false`

## Real-data bottlenecks

15 real pairs:

- REMAIN_OPEN = 14
- REJECT = 1
- PROMOTE = 0

Decision reasons:

- REQUIRED_NULL_UNAVAILABLE = 9
- SEARCH_BOUNDARY_UNRESOLVED = 3
- NO_PRIMARY_METRIC_IMPROVEMENT = 1
- GENERIC_EVALUATOR_INPUT_NOT_AVAILABLE = 2

## Shuffled-control bottlenecks

15 shuffled pairs:

- REMAIN_OPEN = 12
- REJECT = 3
- PROMOTE = 0

Decision reasons:

- REQUIRED_NULL_UNAVAILABLE = 8
- NO_SUPPORTED_CANDIDATE_FAMILY = 4
- NULL_NOT_BEATEN = 2
- DEGRADED_PERFORMANCE = 1

## Confirmed null-metric coverage gap

Real pairs with an actual selector/evaluator metric-coverage gap:

`5 / 15`

Shuffled pairs with the same coverage gap:

`5 / 15`

In every such case the missing metric is:

`SIMPLER_RULE_NULL`

Mechanism:

`nulls.py` adds `SIMPLER_RULE_NULL` whenever
`SIMPLE_BASELINE_PLAUSIBLE` is present.

However temporal/directional evaluators currently return only:

- `MAJORITY_STATE_NULL`
- `TIME_SHIFT_OR_PERMUTATION_NULL`

They do not return:

`SIMPLER_RULE_NULL`

Therefore those candidates are conservatively blocked by:

`REQUIRED_NULL_UNAVAILABLE`

This is a real plumbing/coverage defect.

## Zero-valued-null semantic ambiguity

Not every `REQUIRED_NULL_UNAVAILABLE` is a missing metric.

After removing the confirmed coverage-gap cases:

- real: 4 additional unavailable cases
- shuffled: 3 additional unavailable cases

For temporal/directional evaluators the relevant metrics are always constructed when shifts are supplied.

The gate engine currently treats:

`metric is None`

and

`metric == 0`

identically:

`REQUIRED_NULL_UNAVAILABLE`

because its condition is:

`metric in (None, 0)`

Thus a zero-error null comparator is classified as unavailable rather than as a valid comparator that cannot be beaten.

This is a second, distinct gate-semantics issue.

## Other bottleneck

Two real pairs ended in:

`GENERIC_EVALUATOR_INPUT_NOT_AVAILABLE`

This means automatic candidate generation can still select a candidate family whose generic evaluator requires data fields not supplied by the observation-pair adapter.

This is a third coverage boundary and should be audited separately before another blind real-data discovery challenge.

## Main conclusion

Experiment 068's scientific result remains valid under its frozen pipeline:

`0 real promotions / 0 shuffled promotions`

But Experiment 069 shows that the zero-promotion result cannot be interpreted simply as:

`all 15 real candidate relations failed complete scientific null tests`

because several candidate paths were blocked structurally:

1. missing `SIMPLER_RULE_NULL` metric plumbing;
2. zero-valued null metrics being labeled unavailable;
3. candidate/evaluator input incompatibility;
4. unresolved search-boundary cases.

Therefore:

`068 = valid result of the frozen system`

but:

`068 is not a clean estimate of discovery power after complete gate coverage`.

## Required next work

Do not rerun 068 or reinterpret it.

The next experiment should be an architecture correction/validation experiment that:

1. provides `SIMPLER_RULE_NULL` for temporal/directional candidates when requested;
2. distinguishes `NULL_METRIC_MISSING` from a valid null metric equal to zero;
3. guarantees candidate families selected from observation pairs have compatible evaluator inputs;
4. reruns synthetic positive/negative controls before any new real-data blind experiment.

Only after that should a new numbered real-data challenge be preregistered.
