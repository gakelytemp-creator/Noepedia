# Experiment 070 — Frozen Repair Semantics

## SIMPLER_RULE_NULL

For temporal and direction-specific state-relation candidates, the simpler comparator is the discovery-frozen target majority state already computed by the evaluator.

Therefore:
SIMPLER_RULE_NULL = majority_mismatches on confirmation.

This does not add a new fitted parameter.

## Zero-valued null

Null-error metrics are nonnegative mismatch counts.

- metric is None -> REQUIRED_NULL_UNAVAILABLE / REMAIN_OPEN
- metric = 0 -> valid perfect null comparator

A candidate with nonnegative revised error cannot beat a perfect zero-error null by the required positive relative advantage.

Therefore metric=0 must fail:
NULL_NOT_BEATEN / REJECT

It must not be labeled unavailable.

## Observation-pair compatibility

The generic observation-pair path supplies:
- source_discovery
- target_discovery
- source_confirmation
- target_confirmation
- optional proposed_confirmation

Families requiring continuous target values, residual event-match arrays, or other absent structures are ineligible in this path.

Candidate filtering occurs before ranking, with OPEN_DECOMPOSITION retained as fallback if no compatible candidate remains.

## Claim boundary

070 validates repaired architecture only.
It is not a new scientific discovery experiment.
