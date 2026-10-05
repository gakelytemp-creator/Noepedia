# Experiment 070 — RUN RESULT

## Status

ARCHITECTURAL PASS

Focused verification run:
`37298206618`

Experiment class:
`ARCHITECTURE_CORRECTION / VALIDATION`

Experiments 068 and 069 remain historically unchanged.

## Repair 1 — SIMPLER_RULE_NULL coverage

Temporal and direction-specific evaluators now expose:

`SIMPLER_RULE_NULL`

using the same discovery-frozen majority-state comparator already used for:

`MAJORITY_STATE_NULL`

Synthetic temporal validation confirmed:

- family = DIRECTION_SPECIFIC_RULE
- frozen direction = HIGH_TO_LOW
- frozen lag = 3
- decision = PROMOTE
- reason = ALL_MANDATORY_PROMOTION_GATES_PASSED

Null metrics:

- MAJORITY_STATE_NULL = 40
- SIMPLER_RULE_NULL = 40
- TIME_SHIFT_OR_PERMUTATION_NULL = 80

No required null metric was unavailable.

## Repair 2 — zero-valued null semantics

Previous behavior:

`metric in (None, 0) -> REQUIRED_NULL_UNAVAILABLE`

New behavior:

- `metric is None` -> REQUIRED_NULL_UNAVAILABLE / REMAIN_OPEN
- `metric == 0` -> valid perfect comparator

Because mismatch metrics are nonnegative, a candidate cannot beat a zero-error null.

Synthetic zero-null validation:

- revised metric = 1
- null metric = 0
- decision = REJECT
- reason = NULL_NOT_BEATEN

Thus zero is no longer conflated with missing data.

## Repair 3 — candidate/evaluator input compatibility

Candidate families are now filtered against the data fields available to the evaluator before ranking.

The generic observation-pair path can select only families whose required inputs are present.

Synthetic incompatibility control supplied only state-pair observations while structural features proposed:

- THRESHOLD_REFINEMENT
- LOCAL_EXCEPTION_CANDIDATE

Both were filtered as incompatible.

Fallback:

- selected family = OPEN_DECOMPOSITION
- decision = REMAIN_OPEN
- reason = NO_SUPPORTED_CANDIDATE_FAMILY

No evaluator-input exception occurred.

## Negative control

A deterministic shuffled synthetic relation did not promote.

Result:

- selected family = RELATION_ORIENTATION_REVISION
- decision = REMAIN_OPEN
- no false promotion

## Regression validation

Core changes triggered the existing experiment workflows.

Relevant prior architecture validations remained successful after the repair, including:

- 048
- 049
- 050
- 051
- 052
- 053
- 054
- 055
- 056
- 057
- 058
- 059
- 060
- 062
- 063
- 064
- 065
- 066

## Architectural conclusion

All three gate-coverage defects identified by Experiment 069 are now repaired at the core level:

1. missing SIMPLER_RULE_NULL metric plumbing;
2. zero-valued null metrics misclassified as unavailable;
3. observation-pair candidate/evaluator incompatibility.

Synthetic positive behavior remains promotable.

Synthetic negative behavior does not promote.

The repair therefore passes architecture validation.

## Claim boundary

Experiment 070 is not a scientific discovery result.

It does not alter or reinterpret Experiment 068.

Experiment 068 remains:

`NO_REAL_PROMOTION_AND_SHUFFLED_ZERO`

under its historically frozen pipeline.

A future blind real-data discovery challenge must use a new experiment number and should freeze the repaired core before outcome inspection.
