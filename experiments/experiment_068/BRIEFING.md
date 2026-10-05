# Experiment 068 — Preregistered Stable-Window Blind Real-System Discovery

> PREREGISTERED BEFORE SCIENTIFIC OUTCOME INSPECTION

## 1. Purpose

Repeat the blind real-system discovery challenge on the NASA Milling Wear dataset using a preregistered real-data adapter that excludes unstable entry/exit portions of each 9000-sample sensor trace.

Experiment 067 remains historically closed and is not reclassified.

## 2. Dataset

NASA Prognostics Center of Excellence — Milling Wear dataset.

Official ZIP:
`https://data.nasa.gov/docs/legacy/mill.zip`

Expected:
- 167 milling runs
- six sensor channels:
  - smcAC
  - smcDC
  - vib_table
  - vib_spindle
  - AE_table
  - AE_spindle

Tool-wear label (VB), case identity, material, feed, DOC and other process metadata are prohibited from:
- adapter fitting
- pair selection
- feature extraction
- candidate generation
- promotion decisions

They remain unavailable until a future physical-interpretation audit.

## 3. Frozen core

Noepedia commit:

`c2c81a04f3d2fe08fc48b4742cab555f22bf2dfd`

No core revision code may be changed in response to Experiment 068 outcomes.

## 4. Stable-window adapter

Each raw run contains approximately 9000 samples per sensor channel.

Frozen stable region:

`Python slice [3000:6000]`

That is:
- start index = 3000 inclusive
- end index = 6000 exclusive
- 3000 samples per run/channel

Frozen run-level feature:

`RMS(stable_window)`

No alternative window, feature family, normalization, clipping, or channel-specific transformation is searched.

## 5. Calibration-only state construction

Each channel is independently converted to LOW/HIGH states.

Calibration:
first 40 runs only.

Method:
deterministic 1-D k-means with two clusters.

Orientation:
- lower RMS centroid -> STATE_LOW
- higher RMS centroid -> STATE_HIGH

Frozen threshold:
midpoint of the two calibration centroids.

The threshold is then applied unchanged to discovery, buffer and confirmation runs.

## 6. Adapter-validity gate

Adapter validity is evaluated before any pair discovery or promotion outcome is inspected.

Required for all six channels:

1. every stable-window RMS is finite;
2. each calibration k-means cluster contains at least 4 of the 40 calibration runs;
3. the two frozen calibration centroids are distinct;
4. the resulting frozen threshold is finite.

If any channel fails:

`NOT_EVALUABLE_ADAPTER_VALIDATION`

and:
- no pair discovery is executed;
- no real promotion count is interpreted;
- no shuffled promotion count is interpreted.

This gate is designed to prevent the state-space collapse observed in Experiment 067 from being mislabeled as a scientific null result.

## 7. Frozen row split

Rows remain in source order.

Required:
`N >= 150`

Frozen split:

- calibration: first 40 runs
- discovery: next 60 runs
- buffer: next 20 runs
- confirmation: all remaining runs

For N=167:

- calibration 1..40
- discovery 41..100
- buffer 101..120
- confirmation 121..167

## 8. Pair universe

All 15 unordered pairs from the six sensor-state series are evaluated.

Pair ranking is secondary evidence only.

The primary outcome depends on the count of independently evaluated pair promotions.

## 9. Frozen revision search

For each pair:

- automatic mismatch-feature extraction
- automatic candidate-family selection
- automatic null selection
- generic evaluator
- frozen promotion gate
- append-only materialization

Temporal search:

- directions: LOW_TO_HIGH, HIGH_TO_LOW
- lag grid: 1..8 runs
- permutation shifts: 7, 13, 19 confirmation positions
- relative null-advantage gate: 10%

Search-boundary hit remains epistemically unresolved.

## 10. Shuffled control

The exact same frozen state series and split are used.

For each pair independently:

- source remains unchanged;
- discovery target is deterministically shuffled with seed:
  `68000 + pair_index`
- confirmation target is deterministically shuffled with seed:
  `68100 + pair_index`

Permutation implementation:

`random.Random(seed).shuffle`

No seed is selected after observing outcomes.

## 11. Primary outcome classes

### A. REAL_PROMOTION_AND_SHUFFLED_ZERO

- real promotion count >= 1
- shuffled promotion count = 0

Positive blind-discovery result.

### B. NO_REAL_PROMOTION_AND_SHUFFLED_ZERO

- real promotion count = 0
- shuffled promotion count = 0

Valid scientific null result.

### C. ANY_SHUFFLED_PROMOTION

- shuffled promotion count >= 1

Primary failure regardless of real promotion count.

### D. NOT_EVALUABLE_ADAPTER_VALIDATION

Adapter gate failed before scientific inference.

## 12. No rescue rule

After execution, the following may not be changed to rescue the result:

- stable window
- RMS feature
- channel set
- cluster-size gate
- row split
- pair universe
- lag grid
- null definitions
- shuffle seeds
- promotion threshold

Any alternative representation requires a new experiment number and a new preregistration.

## 13. Claim boundary

A positive result would show that the frozen Noepedia machinery can discover at least one null-protected relation in a new real physical system while staying silent on deterministic shuffled controls.

It would not establish causality or physical meaning.

Any promoted relation must proceed to a later Physical Interpretation Audit.
