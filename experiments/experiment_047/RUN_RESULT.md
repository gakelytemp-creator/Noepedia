# Experiment 047 — RUN RESULT

## Status

reproducibility = PASS
external architecture transfer = PASS
scientific result = EXTERNAL_NULL_PROTECTED_REVISION_NOT_CONFIRMED
harness decision = REMAIN_OPEN

Focused GitHub Actions verification:
run_id = 37234155839
conclusion = success

## External dataset

UCI Condition Monitoring of Hydraulic Systems

Dataset size:
2205 cycles

This is a different hydraulic test rig and a different dataset from MetroPT-3.

## Calibration-only family selection

Frozen candidate families:
- cooler condition -> CE mean
- valve condition -> PS2 mean
- pump leakage -> SE mean
- accumulator condition -> PS1 mean

Selected family:

`pump leakage -> SE`

Calibration mismatch fraction:
`14.75%`

Frozen orientation:
`HEALTHY -> HIGH`
`DEGRADED -> LOW`

SE threshold:
`44.82091233630951`

## Discovery

Discovery cycles:
`801..1400`

OLD mismatches:
`305 / 600`

Selected candidate:
- direction = HIGH_TO_LOW
- lag = 30 cycles

Revised discovery mismatches:
`181 / 600`

Important:

`lag_boundary_hit = true`

The optimum remained at the upper preregistered lag boundary.

## Untouched confirmation

Confirmation cycles:
`1601..2200`

OLD mismatches:
`328 / 600`

REVISED mismatches:
`204 / 600`

Majority-state null:
`0 / 600`

Permutation temporal nulls:
- shift 50 -> 204
- shift 100 -> 208
- shift 150 -> 204
- shift 200 -> 204

Permutation median:
`204`

## Scientific interpretation

The revised rule beats the OLD rule:

`37.80% relative mismatch reduction`

but it does not beat either required null baseline.

The majority predictor is perfect on this confirmation window.

The revised rule is also equal to the permutation-null median.

Therefore:

`EXTERNAL_NULL_PROTECTED_REVISION_NOT_CONFIRMED`

## Harness decision

The generic Experiment 045 harness returned:

`REMAIN_OPEN`

This is correct under Experiment 044 gate semantics because:
- the selected lag hit the search boundary;
- the required majority-null comparison is not promotable when the null has zero error;
- the candidate does not beat the permutation null.

Therefore the candidate is not promoted and is not treated as a scientifically completed rejection of the underlying relation.

## Graph materialization

All Experiment 046 materialization invariants passed:
- parent rule preserved
- OPEN preserved
- gate audit materialized
- decision materialized
- OPEN refinement materialized
- append-only history preserved
- no new rule created
- no rejected-candidate terminal object created

## External-transfer conclusion

The scientific candidate did not confirm.

But the Noepedia revision architecture itself transferred successfully to a different dataset and physical system:

`external_architecture_pass = true`

The same protocol correctly produced a non-promotion state without overwriting history.

## Correction

The first wrapper execution incorrectly expected every non-confirmed scientific result to map to REJECT.

Experiment 044 distinguishes REJECT from REMAIN_OPEN.

This implementation-only wrapper correction is documented in:
`CORRECTION.md`

No scientific criterion or data selection changed.

## Final claim boundary

Experiment 047 supports external transfer of the revision architecture.

It does not support the specific pump-leakage -> SE temporal revision candidate.

It does not yet establish successful positive rule promotion on a non-MetroPT dataset.