# Experiment 046 — Self-Revision Test Specification

## Purpose

Test the first end-to-end materialization step after automated gate decisions.

## Source architecture

Uses Experiment 045 `revision_harness.py` unchanged.

## Positive case

Experiment 040-derived case must produce:
`PROMOTE`

Then materialize:
- parent RULE V1
- candidate
- promotion decision
- RULE V2 with `EPISTEMIC_STATUS = EMPIRICALLY_SUPPORTED_RULE`
- `DERIVED_FROM_RULE` relation
- `PROMOTED_FROM` relation
- `SUPERSEDED_BY` relation
- `OPEN_REFINEMENT` with resolved and remaining components

## Negative case

Experiment 039-derived case must produce:
`REJECT`

Then materialize:
- parent rule preserved
- rejected candidate record
- rejection reason
- OPEN_REFINEMENT recording rejected explanation
- no new promoted rule

## Invariants

1. append-only history
2. parent rule remains present
3. original OPEN remains present
4. promotion creates a new rule id
5. rejection creates no new rule version
6. every new object has provenance links
7. decision record and gate audit remain queryable

## Pass criteria

PASS requires all invariants for both cases.