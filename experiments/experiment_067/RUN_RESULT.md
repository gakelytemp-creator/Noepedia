# Experiment 067 — RUN RESULT

## Final status

`NOT_EVALUABLE_PREPROCESSING_FAILURE`

Experiment class:
`SCIENTIFIC_REAL_DATA`

Frozen core commit:
`85ec973cf4b38fce9a6aa41fedd77f123ebfd6bc`

## Dataset

NASA / UC Berkeley Milling Wear

Parsed runs:
167

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

## Execution history

Initial focused run:
`37284718832`

A MATLAB parser problem was detected because calibration RMS thresholds were physically implausible.

The parser-only correction was documented in:
`CORRECTION.md`

Corrected-parser focused run:
`37285598762`

## Corrected-parser diagnostic

Even after structured-array parsing was corrected, full-trace RMS produced degenerate calibration scales.

Examples:

- smcAC threshold ≈ 7.29e27
- smcDC threshold ≈ 2.47e18
- vib_table threshold ≈ 6.80e27
- vib_spindle threshold ≈ 2.69e32
- AE_table threshold ≈ 1.98e32
- AE_spindle threshold ≈ 8.54e25

The resulting discovery state series collapsed to extreme class imbalance / constant states.

The mechanical classifier therefore printed:

- real promotion count = 0
- shuffled promotion count = 0
- provisional class = NO_REAL_PROMOTION_AND_SHUFFLED_ZERO

That provisional class is NOT accepted as the scientific result.

## Why the result is not evaluable

Experiment 067 preregistered:

`run_feature = RMS(full raw trace)`

Published processing of this dataset uses a stable cutting interval inside each run rather than treating the entire recorded trace as a homogeneous cutting signal.

The preregistered full-trace RMS transformation therefore failed to produce a scientifically usable state representation.

Changing the feature window after seeing this behavior would violate the blind preregistration.

Therefore Experiment 067 is closed as:

`NOT_EVALUABLE_PREPROCESSING_FAILURE`

not as:

`NO_REAL_PROMOTION_AND_SHUFFLED_ZERO`

## Integrity statement

No scientific rescue was performed.

The following remain unchanged:

- real dataset
- six sensor channels
- pair universe
- calibration/discovery/buffer/confirmation split
- candidate machinery
- lag grid
- null models
- shuffled-control seeds
- promotion gates
- frozen core revision code

No stable-window feature was substituted after outcome inspection.

## What 067 did establish

The blind-test framework itself executed end to end on a new real physical system.

It also exposed a new requirement that the architecture/unit tests had not revealed:

`REAL_DATA_ADAPTER_VALIDATION MUST PRECEDE BLIND DISCOVERY`

A representation that collapses the state space must make the scientific experiment NOT_EVALUABLE rather than silently produce a null discovery result.

## Next experiment

A new preregistered experiment must be created before using a stable cutting region or any alternative real-data representation.

That experiment must retain:

- untouched confirmation
- all-pair evaluation
- shuffled promotion count = 0 as the primary safety criterion
- null result allowed

and must freeze the real-data adapter before observing promotion outcomes.
