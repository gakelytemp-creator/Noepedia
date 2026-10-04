# Experiment 047 — Preregistered External Transfer Test

> Status: preregistered before inspecting scientific outcomes from the external dataset.

## Goal

Test whether the revision architecture transfers beyond MetroPT-3 to a different physical system and dataset.

## Dataset

UCI Condition Monitoring of Hydraulic Systems, dataset 447.

Archive:
`https://archive.ics.uci.edu/static/public/447/condition+monitoring+of+hydraulic+systems.zip`

Cycle structure:
- 2205 cycles
- 60 seconds per cycle
- profile.txt stores component-condition labels
- sensor files store one row per cycle

## Frozen candidate families

F1: cooler condition -> CE cycle mean
F2: valve condition -> PS2 cycle mean
F3: pump leakage -> SE cycle mean
F4: accumulator condition -> PS1 cycle mean

## Source-label binarization

Healthy source state:
- cooler = 100
- valve = 100
- pump leakage = 0
- accumulator = 130

All other listed condition values map to DEGRADED.

Each analog target is independently binarized by deterministic 1-D k-means on calibration cycles.

For each family, both source-to-target orientations are compared on calibration only.

## Windows

calibration cycles = 1..800
discovery cycles = 801..1400
confirmation cycles = 1601..2200

Cycles 1401..1600 are unused separation buffer.

## Family selection

For each family compute calibration mismatch fraction after choosing the lower-mismatch orientation.

Eligibility:
`0.05 <= mismatch_fraction <= 0.40`

Select eligible family closest to 0.20 mismatch fraction.
Tie-break by F1, F2, F3, F4 order.

If none eligible:
`NO_ELIGIBLE_EXTERNAL_FAMILY`

## OLD rule

Mapped component-condition state == binarized target sensor state.

## Candidate temporal revision

Search both source transition directions:
- LOW_TO_HIGH
- HIGH_TO_LOW

Search integer lag:
`1..30 cycles`

Within 0..N cycles after the selected source transition, expected target remains the mapped source state immediately before transition.

Outside that interval, expected target equals current mapped source state.

Select minimum discovery mismatch count.
Tie-break to smaller lag, then LOW_TO_HIGH before HIGH_TO_LOW.

## Null 1 — majority-state predictor

Freeze target majority state from discovery only.

## Null 2 — circular-shift temporal null

Frozen confirmation source shifts:
`50, 100, 150, 200 cycles`

Apply the frozen candidate direction and lag to each shifted sequence.
Permutation reference = median mismatch count.

## Confirmation gate

`EXTERNAL_NULL_PROTECTED_REVISION_CONFIRMED` requires all:

1. revised confirmation error < OLD error
2. revised error <= 0.90 * majority-null error
3. revised error <= 0.90 * permutation-null median error
4. selected lag < 30

Otherwise:
`EXTERNAL_NULL_PROTECTED_REVISION_NOT_CONFIRMED`

## Automated architecture transfer

The resulting revision case must then be processed by:
- Experiment 045 revision harness
- Experiment 046 graph materializer

Expected mapping:
- scientific confirmation -> PROMOTE
- scientific non-confirmation -> REJECT
- non-evaluable dataset/case -> REMAIN_OPEN

## Claim boundary

A positive result would demonstrate protocol/harness transfer to a different hydraulic physical system.

It would not establish universal applicability to arbitrary domains.