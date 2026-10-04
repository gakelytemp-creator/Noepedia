# Experiment 040 — Preregistered Calibration-Selected Null-Protected Revision Test

> Status: preregistered before inspecting discovery or confirmation rows.

## Purpose

Find a nontrivial relation family before discovery using calibration only, then test a temporal revision with explicit null baselines.

## Frozen candidate families

1. DV_pressure -> TP2
2. COMP -> Motor_current
3. Towers -> TP3
4. LPS -> Reservoirs

Each source is treated as binary.
Each target is independently binarized by deterministic 1-D k-means on rows 1..50,000.

## Calibration-only family selection

For each family evaluate both source orientations:
- mapping A: 0->LOW, 1->HIGH
- mapping B: 0->HIGH, 1->LOW

Freeze the lower-mismatch orientation.

Then compute calibration mismatch fraction.

Eligibility interval:
0.05 <= mismatch fraction <= 0.40

Among eligible families choose the mismatch fraction closest to 0.20.
Tie-break by candidate-list order.

If no family is eligible:
NO_ELIGIBLE_FAMILY

## OLD rule

Mapped binary source state == binarized target state.

## Windows

discovery = rows 950,001..955,000
confirmation = rows 1,000,001..1,005,000

## Candidate revision family

Search both source transition directions:
- LOW_TO_HIGH
- HIGH_TO_LOW

Search every integer lag:
1..400 rows

Within 0..N rows after the selected source transition, expected target remains the source state immediately before transition.
Outside that interval, expected target equals current mapped source state.

Select minimum discovery mismatch count.
Tie-break: smaller lag, LOW_TO_HIGH before HIGH_TO_LOW.

## Null comparator 1

Freeze target majority state from discovery only.
Use it as a constant confirmation predictor.

## Null comparator 2

Use circularly shifted mapped-source confirmation sequences.
Frozen shifts:
500, 1000, 1500, 2000 rows.

Apply the same frozen direction and lag.
Permutation reference = median mismatch count.

## Confirmation gate

NULL_PROTECTED_REVISION_CONFIRMED requires all:
1. revised error < old error
2. revised error <= 0.90 * majority-null error
3. revised error <= 0.90 * permutation-null median error
4. selected lag < 400

Otherwise:
NULL_PROTECTED_REVISION_NOT_CONFIRMED

## Additional reporting

Report OLD confirmation mismatch fraction.
If it lies in 45%-55%, flag OLD_NEAR_CHANCE_BALANCE.

## Claim boundary

A positive result would be a second null-protected revision example on this dataset.
It would not establish causal mechanism or physical independence.