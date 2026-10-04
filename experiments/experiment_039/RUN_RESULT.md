# Experiment 039 — RUN RESULT

## Status

reproducibility = PASS
scientific result = NULL_PROTECTED_REVISION_NOT_CONFIRMED

Focused GitHub Actions verification:
run_id = 37223713884
conclusion = success

## Relation family

Pressure_switch ↔ Reservoirs

## Calibration

Reservoirs threshold = 8.997462776820406

Frozen Pressure_switch orientation:
0 -> HIGH
1 -> LOW

Calibration mismatches:
- mapping A (0->LOW,1->HIGH) = 26280
- mapping B (0->HIGH,1->LOW) = 23720

## Discovery window

rows 850,001..855,000

OLD direct-mapping mismatches = 2622

Selected candidate:
- direction = HIGH_TO_LOW
- lag = 59 rows
- lag boundary hit = false

Discovery revised mismatches = 2232
net reduction vs old = 390

## Confirmation window

rows 900,001..905,000

OLD direct rule:
- mismatches = 21 / 5000
- mismatch fraction = 0.42%

Frozen revised rule:
- mismatches = 1226 / 5000

Majority null:
- mismatches = 5000

Permutation temporal nulls:
- shift 500 = 1226
- shift 1000 = 1226
- shift 1500 = 1226
- shift 2000 = 1226
- median = 1226

Therefore:

NULL_PROTECTED_REVISION_NOT_CONFIRMED

## Interpretation

The discovery window suggested a 59-row HIGH_TO_LOW correction.

That correction did not transfer.

On the untouched confirmation window the original direct rule was already extremely accurate:
21 mismatches out of 5000 rows.

The revised rule strongly degraded performance:
1226 mismatches.

It also exactly matched the temporal permutation-null error.

Therefore the discovery correction should not be promoted into Noepedia knowledge.

## Noepedia significance

This is a strong negative result.

It demonstrates that a large discovery-window mismatch and an apparently useful temporal correction are not sufficient for revision.

Untouched confirmation can show that the old rule remains locally valid and that the proposed correction is non-transferable.

The correct action is:

retain OLD rule
retain OPEN about domain variation
reject the proposed 59-row revision

## Claim boundary

Experiment 039 does not establish that Pressure_switch and Reservoirs are universally identical.

It establishes that the tested discovery-derived temporal revision failed transfer and null protection.