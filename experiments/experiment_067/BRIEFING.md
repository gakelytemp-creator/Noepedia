# Experiment 067 — Preregistered Blind Real-System Discovery Challenge

> PREREGISTERED BEFORE SCIENTIFIC OUTCOME INSPECTION

## 1. Purpose

Test the discovery capability of the frozen Noepedia core on a new real multichannel physical system.

This is not an architecture/unit-test PASS experiment.

## 2. Dataset

NASA Prognostics Center of Excellence — Milling Wear dataset.

Official source:
`https://data.nasa.gov/docs/legacy/mill.zip`

The source contains 167 milling runs across 16 operating cases and six raw sensor traces:

- smcAC
- smcDC
- vib_table
- vib_spindle
- AE_table
- AE_spindle

No tool-wear label (VB), material, DOC, feed, or case identifier may be used for pair selection or rule construction.

Those metadata are retained only for later physical interpretation if Experiment 067 produces a promotion.

## 3. Frozen core

Noepedia commit:

`85ec973cf4b38fce9a6aa41fedd77f123ebfd6bc`

Core modules used:

- series/state construction
- pair scan
- feature extraction
- candidate generation
- null selection
- generic evaluation
- promotion gate
- append-only materialization

No core revision code may be changed after preregistration in response to Experiment 067 results.

## 4. Preprocessing

For each of the six raw sensor traces and each milling run:

`run_feature = RMS(raw_trace)`

No alternative feature family is searched.

Each of the six RMS series is converted independently into LOW/HIGH states using deterministic 1-D k-means fitted on calibration runs only.

Cluster orientation is numeric:
- lower RMS cluster -> STATE_LOW
- higher RMS cluster -> STATE_HIGH

Frozen thresholds are then applied to discovery, buffer and confirmation runs.

## 5. Run ordering and split

Rows are ordered exactly as stored by the source dataset.

Let N be the number of runs successfully parsed.

Required:
`N >= 150`

Frozen split by row index:

- calibration: first 40 runs
- discovery: next 60 runs
- buffer: next 20 runs
- confirmation: all remaining runs

Thus for N=167:

- calibration 1..40
- discovery 41..100
- buffer 101..120
- confirmation 121..167

If parsing yields fewer than 150 runs:

`NOT_EVALUABLE_DATASET_PARSE`

## 6. Pair universe

Six sensor-state series produce 15 unordered pairs.

Every pair is evaluated independently with the same frozen observation-driven revision machinery.

The pipeline may therefore produce 0..15 real-data promotions.

Pair ranking is recorded, but promotion-count inference does not depend on only the top-ranked pair.

## 7. Candidate search

For every pair:

- automatic mismatch-feature extraction
- automatic candidate-family selection
- automatic null selection

Temporal search configuration is frozen:

- directions: LOW_TO_HIGH, HIGH_TO_LOW
- lag grid: 1..8 runs
- permutation shifts: 7, 13, 19 confirmation positions
- relative null-advantage gate: 10%

Search-boundary hit remains epistemically unresolved.

## 8. Shuffled control

The control uses the exact same six state series and exact same split.

Only discovery and confirmation target order are destroyed.

For each pair independently:

- source series remains unchanged
- target discovery is permuted with deterministic seed:
  `67000 + pair_index`
- target confirmation is permuted with deterministic seed:
  `67100 + pair_index`

Python `random.Random(seed).shuffle` is the frozen permutation rule.

The same candidate/null/promotion machinery is applied without modification.

## 9. Primary outcome classes

### A. REAL_PROMOTION_AND_SHUFFLED_ZERO

Conditions:

- real promotion count >= 1
- shuffled promotion count = 0

Interpretation:
positive blind-discovery result.

### B. NO_REAL_PROMOTION_AND_SHUFFLED_ZERO

Conditions:

- real promotion count = 0
- shuffled promotion count = 0

Interpretation:
valid null result; pipeline remained conservative but discovery capability was not demonstrated on this dataset.

### C. ANY_SHUFFLED_PROMOTION

Condition:

- shuffled promotion count >= 1

Interpretation:
primary failure, regardless of real-data promotion count.

The experiment must stop at this classification and must not rescue the result by changing thresholds, features, seeds, pair filters, or search ranges.

## 10. Secondary records

Record:

- selected/ranked pairs
- per-pair extracted features
- per-pair candidate family
- per-pair final decision
- real promotion count
- shuffled promotion count
- all frozen thresholds
- parse diagnostics

These do not alter the primary outcome class.

## 11. Claim boundary

A positive result would show that the frozen Noepedia machinery can find at least one null-protected relation on a new real system while remaining silent on the deterministic shuffled control.

It would not yet establish causal or physically meaningful discovery.

Any promoted pair must proceed to a separate Experiment 068 Physical Interpretation Audit.
