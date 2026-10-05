# Experiment 071 — Preregistered Blind Robot-Telemetry Discovery

> PREREGISTERED BEFORE SCIENTIFIC OUTCOME INSPECTION

## 1. Goal

Test the repaired Noepedia pipeline on a new real robot system.

Question:

Can the frozen pipeline identify at least one null-protected relation among unlabeled robot telemetry channels while remaining silent on deterministic shuffled controls?

## 2. Source

Public reproducibility mirror:

`https://github.com/efeolgun/robot-predictive-maintenance`

Frozen mirror commit:

`cec9f8a95d6099201cbf9afb8821696dc0ebd7cd`

Original dataset provenance:
CentraleSupélec Robot Predictive Maintenance challenge.

The selected blind sequence is:

`data/testing_data/20240527_094865`

Reason:
it is the lexicographically first testing sequence.

No sequence is selected based on observed signal structure or outcomes.

## 3. Input channels

Six motors.

For every motor:

- position
- temperature
- voltage

Total candidate telemetry channels:

`18`

The following CSV fields are prohibited from scientific inference:

- label
- file/folder name beyond deterministic ordering

The `time` column is used only to verify alignment.

## 4. Alignment

All six motor CSVs must contain the same number of rows.

Expected selected-sequence length from source inspection:

`2423`

Timestamps must be monotonically increasing.

Row index is the frozen common timeline.

If files are misaligned:

`NOT_EVALUABLE_ALIGNMENT`

## 5. Frozen split

For 2423 rows:

- calibration: rows 1..500
- discovery: rows 501..1300
- buffer: rows 1301..1600
- confirmation: rows 1601..2423

Counts:

- calibration = 500
- discovery = 800
- buffer = 300
- confirmation = 823

No row may move between windows after outcome inspection.

## 6. State adapter

Each of the 18 numeric telemetry channels is treated independently.

Calibration-only deterministic 1-D k-means with two clusters:

- lower centroid -> STATE_LOW
- higher centroid -> STATE_HIGH

Frozen threshold:
midpoint of calibration centroids.

No normalization, smoothing, detrending, clipping, derivative, or feature engineering is searched.

## 7. Channel-validity gate

For each channel, using calibration only:

- both centroids finite and distinct;
- both calibration clusters contain at least 25 samples;
- threshold finite.

Invalid channels are excluded before pair construction.

Experiment remains evaluable only if the surviving channel set contains:

- at least 6 valid channels;
- at least 2 distinct motors;
- at least 2 distinct signal types among position / temperature / voltage.

Otherwise:

`NOT_EVALUABLE_ADAPTER_VALIDATION`

## 8. Pair universe

All unordered pairs among valid channels.

No pair is selected manually.

Each pair is evaluated independently.

## 9. Frozen revision search

Core commit:

`e9885e1bc3f0fcddad2d982eea2ec273e968575e`

For every pair:

- automatic mismatch feature extraction;
- compatibility-filtered candidate generation;
- automatic null selection;
- generic evaluation;
- promotion gates;
- append-only materialization.

Temporal search:

- directions: LOW_TO_HIGH, HIGH_TO_LOW
- lag grid: 1..50 samples
- permutation shifts: 137, 281, 419 confirmation samples
- required relative null advantage: 10%

At 10 Hz, lag search spans 0.1..5.0 seconds.

Search-boundary hits remain unresolved.

## 10. Shuffled control

For each pair independently:

- source sequence unchanged;
- target discovery shuffled with seed:
  `71000 + pair_index`
- target confirmation shuffled with seed:
  `71100 + pair_index`

Algorithm:

`random.Random(seed).shuffle`

Exactly the same repaired revision machinery is applied.

## 11. Primary outcome classes

### REAL_PROMOTION_AND_SHUFFLED_ZERO

- real promotion count >= 1
- shuffled promotion count = 0

### NO_REAL_PROMOTION_AND_SHUFFLED_ZERO

- real promotion count = 0
- shuffled promotion count = 0

### ANY_SHUFFLED_PROMOTION

- shuffled promotion count >= 1

Primary failure regardless of real promotion count.

### NOT_EVALUABLE_*

Alignment or adapter gate failed before scientific inference.

## 12. No-rescue rule

After outcome inspection, do not change:

- sequence choice;
- channel set definition;
- split;
- k-means adapter;
- cluster-size gate;
- lag range;
- feature thresholds;
- null definitions;
- shuffle seeds;
- promotion gates.

Any alternative requires a new experiment number.

## 13. Claim boundary

A positive outcome would demonstrate blind null-protected relation discovery on a new real robot telemetry system.

It would not establish causal meaning, fault detection, or physical interpretation.

Any promoted relation must receive a later interpretation audit.
