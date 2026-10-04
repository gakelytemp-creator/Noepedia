# Experiment 039 — Preregistered Null-Protected Revision Test

> Status: preregistered before inspecting rows 850,001..905,000.

## Purpose

Experiment 033 is currently the strongest knowledge-revision loop.
Experiments 036-038 showed why null protection is required.

Experiment 039 attempts a second strong loop using a different measurement relation:

Pressure_switch ↔ Reservoirs

## Calibration and frozen orientation

Use rows 1..50,000 only.

Fit Reservoirs with deterministic 1-D k-means (k=2) and map to:
- STATE_LOW
- STATE_HIGH

Pressure_switch is treated as a binary source.

Freeze its direct orientation by calibration agreement:
- evaluate mapping A: 0->LOW, 1->HIGH
- evaluate mapping B: 0->HIGH, 1->LOW
- choose the mapping with fewer calibration mismatches
- tie-break to mapping A

This orientation is frozen before discovery.

## OLD rule

Mapped Pressure_switch state == Reservoirs state.

## Windows

discovery = rows 850,001..855,000
confirmation = rows 900,001..905,000

## Candidate family

Search transition-specific lag corrections to the OLD rule.

Candidate dimensions:
- source transition: LOW_TO_HIGH or HIGH_TO_LOW
- lag N: every integer from 1..400 rows

For a candidate:
- outside 0..N rows after the selected Pressure_switch transition: expected Reservoirs state = current mapped Pressure_switch state
- inside 0..N rows after that transition: expected Reservoirs state = mapped Pressure_switch state immediately before the transition

Select by minimum discovery mismatch count.
Tie-break to smaller lag, then LOW_TO_HIGH before HIGH_TO_LOW.

If selected lag = 400, mark LAG_BOUNDARY_HIT.

## Null comparator 1 — majority constant

Choose Reservoirs majority state from discovery only.
Freeze it and predict that same state for all confirmation rows.

## Null comparator 2 — circular-shift temporal null

Use the frozen selected lag and transition direction, but circularly shift the mapped Pressure_switch confirmation sequence.

Frozen shifts:
500, 1000, 1500, 2000 rows.

Permutation-null reference = median mismatch count across the four shifts.

## Confirmation gate

NULL_PROTECTED_REVISION_CONFIRMED requires all:

1. revised confirmation error < old error
2. revised error <= 0.90 * majority-null error
3. revised error <= 0.90 * permutation-null median error
4. selected lag is not the 400-row search boundary

Otherwise:
NULL_PROTECTED_REVISION_NOT_CONFIRMED

## Additional guard

If OLD confirmation mismatch fraction is between 45% and 55%, mark OLD_NEAR_CHANCE_BALANCE = true.
This does not automatically fail the test, but must be reported.

## OPEN handling

Initial OPEN:
PRESSURE_SWITCH_RESERVOIRS_DIRECT_MAPPING -> DOMAIN_VALIDITY -> UNKNOWN

A positive result refines but does not delete OPEN.

## Claim boundary

A positive result would establish a second null-protected revision example on this dataset.
It would not establish causal mechanism, physical independence, or universal controller behavior.