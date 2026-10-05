# Experiment 068 — RUN RESULT

## Final status

`NO_REAL_PROMOTION_AND_SHUFFLED_ZERO`

Experiment class:
`SCIENTIFIC_REAL_DATA`

Focused verification run:
`37288541898`

Frozen core commit:
`c2c81a04f3d2fe08fc48b4742cab555f22bf2dfd`

## Dataset

NASA / UC Berkeley Milling Wear

Parsed runs:
`167`

Channels:
- smcAC
- smcDC
- vib_table
- vib_spindle
- AE_table
- AE_spindle

Frozen split:
- calibration = 40
- discovery = 60
- buffer = 20
- confirmation = 47

## Stable-window adapter

Frozen window:

`Python slice [3000:6000]`

Run-level feature:

`RMS(stable_window)`

Adapter validation:
`PASS`

Calibration cluster diagnostics:

- smcAC: LOW=23, HIGH=17, threshold=2.155365534888225
- smcDC: LOW=20, HIGH=20, threshold=7.428387713984215
- vib_table: LOW=33, HIGH=7, threshold=1.4293787397618938
- vib_spindle: LOW=30, HIGH=10, threshold=0.46515646792985355
- AE_table: LOW=27, HIGH=13, threshold=0.25476137990722214
- AE_spindle: LOW=26, HIGH=14, threshold=0.3262129277406151

No adapter-validity failure occurred.

The state-space collapse seen in Experiment 067 did not recur.

## Blind discovery result

All 15 unordered sensor pairs were evaluated with the frozen revision machinery.

Real-data promotion count:

`0`

Deterministic shuffled-control promotion count:

`0`

Therefore the preregistered primary class is:

`NO_REAL_PROMOTION_AND_SHUFFLED_ZERO`

## Interpretation

This is a valid scientific null result.

The frozen Noepedia pipeline remained conservative on this new real physical system:

- it did not promote any relation on the real dataset;
- it also did not promote any relation after temporal correspondence was destroyed by deterministic shuffling.

Therefore Experiment 068 does not demonstrate blind discovery capability on this dataset.

It also does not show false-positive promotion under the preregistered shuffled control.

## Secondary observation

The discovery scan did detect structured mismatch patterns in real data.

For example, the highest-ranked relation included:

`smcDC -> AE_table`

with:
- TEMPORAL_CLUSTERING
- TRANSITION_ALIGNED_MISMATCH
- DIRECTION_ASYMMETRY
- LOCAL_RESIDUAL_CLUSTER

However no candidate crossed the frozen promotion gates.

These secondary structures are not promoted knowledge.

## Integrity statement

No post-outcome changes were made to:

- stable window;
- RMS feature;
- channel set;
- adapter-validity gate;
- calibration/discovery/buffer/confirmation split;
- pair universe;
- lag search;
- null models;
- shuffled-control seeds;
- promotion gates;
- frozen core.

Experiment 068 is therefore closed as a preregistered scientific null result.

## Cross-experiment meaning

Experiment 067:
`NOT_EVALUABLE_PREPROCESSING_FAILURE`

Experiment 068:
`NO_REAL_PROMOTION_AND_SHUFFLED_ZERO`

Together they distinguish two very different outcomes:

1. invalid representation -> experiment not evaluable;
2. valid representation + no promotion -> legitimate scientific null.

## Claim boundary

Experiment 068 supports the claim that the frozen pipeline can remain silent on both real and shuffled data when promotion evidence is insufficient.

It does not support the claim that Noepedia has demonstrated a new blind real-system discovery beyond the MetroPT result.
