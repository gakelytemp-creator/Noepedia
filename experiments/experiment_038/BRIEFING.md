# Experiment 038 — Preregistered Null-Protected Validation

> Status: preregistered before inspecting rows 750,001..805,000.

## Purpose

Experiments 036 and 037 selected lag=80, the upper edge of their search grid.
Experiment 038 tests whether those results survive:
- a wider lag search
- a majority-state baseline
- temporal permutation baselines

## Families

F036:
source = TP2
target = TP3
direction = HIGH_TO_LOW

F037:
source = Reservoirs
target = H1
direction = HIGH_TO_LOW

The direction is frozen from the earlier experiments.

## Calibration

Use rows 1..50,000.
Fit each channel independently with deterministic 1-D k-means (k=2).
Map to STATE_LOW / STATE_HIGH using midpoint thresholds.

## Windows

discovery = rows 750,001..755,000
confirmation = rows 800,001..805,000

## Expanded lag search

For each family search every integer lag:

1..400 rows

Candidate rule:
- outside 0..N rows after source HIGH_TO_LOW transition: expected target = current source state
- inside 0..N rows after source HIGH_TO_LOW transition: expected target = source state immediately before transition

Select discovery lag by minimum mismatch count; tie-break to smaller lag.

If the selected lag is exactly 400, mark LAG_BOUNDARY_HIT = true.

## Null comparator 1 — majority constant

Choose the target majority state from the discovery window only.
Freeze that state.
On confirmation predict that same target state for all 5,000 rows.

## Null comparator 2 — deterministic circular-shift temporal null

Use the frozen selected temporal rule, but replace the confirmation source-state sequence by circularly shifted copies.

Frozen shifts:
500, 1000, 1500, 2000 rows.

For each shift:
- preserve the source-state sequence and its transition structure
- destroy its original alignment with target time
- apply the same selected lag and HIGH_TO_LOW rule
- compute confirmation mismatch count

The permutation-null reference error is the median mismatch count across the four shifts.

## Confirmation gate

For each family compute:
- revised error
- old direct-equality error
- majority-constant error
- permutation-null median error

Null-protected success requires all of:

1. revised error < old direct-equality error
2. revised error <= 0.90 * majority error
3. revised error <= 0.90 * permutation-null median error

This is at least 10% relative error reduction versus both null baselines.

Family classes:
- NULL_PROTECTED_CONFIRMED
- NOT_NULL_PROTECTED

Overall Experiment 038 class:
- BOTH_FAMILIES_NULL_PROTECTED
- ONE_FAMILY_NULL_PROTECTED
- NO_FAMILY_NULL_PROTECTED

## Interpretation

If a family fails, Experiments 036/037 remain transferred temporal patterns but not null-protected evidence.
If it passes, the relation survives class-balance and time-alignment nulls.

## Claim boundary

Null protection does not establish causal mechanism or physical independence.