# Experiment 045 — Automated Revision Harness Specification

## Status before execution

`IMPLEMENTATION_CANDIDATE`

## Purpose

Implement the decision layer defined by Experiments 042–044.

## Input

A machine-readable `REVISION_CASE` containing:
- parent rule identity
- OPEN identity
- candidate identity
- explicit candidate parameters
- preregistration state
- discovery and confirmation window identities
- evaluator identity state
- confirmation evaluability
- old and revised primary metrics
- required null metrics/gates
- unresolved-success accounting state
- correction documentation state
- history preservation state
- OPEN refinement state

## Output

`PROMOTION_GATE_AUDIT` containing:
- every gate result
- evidence used by the gate
- reason token
- final decision

Allowed decisions:
- PROMOTE
- REJECT
- REMAIN_OPEN

## Decision precedence

1. Structural/history incompleteness that prevents a justified test -> REMAIN_OPEN.
2. Scientific invalidity or fair-test failure -> REJECT.
3. Only if every mandatory gate passes -> PROMOTE.

## Non-mutation invariant

The harness must never overwrite the parent rule.

A PROMOTE decision emits a proposed new-rule record:
`DERIVED_FROM_RULE = parent_rule`
`PROMOTED_FROM = candidate`

A REJECT decision emits a rejected-candidate record.

A REMAIN_OPEN decision emits no new rule.

## Integration validation

Experiment 040 must map to PROMOTE.
Experiment 039 must map to REJECT.
A deliberately non-evaluable synthetic case must map to REMAIN_OPEN.