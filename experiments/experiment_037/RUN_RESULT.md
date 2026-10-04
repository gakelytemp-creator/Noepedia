# Experiment 037 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS
scientific result = THIRD_REVISION_LOOP_CONFIRMED
strong flag = true

Focused GitHub Actions verification:
run_id = 37218775954
conclusion = success

## Third relation family

This experiment did not use DV_eletric, Motor_current, TP2, or TP3 in the rule under test.

Relation family:
H1 state vs Reservoirs state.

## Calibration

H1 threshold = 4.473384960142661
Reservoirs threshold = 8.997462776820406

Both thresholds were fitted independently on rows 1..50,000.

## Discovery window

rows 650,001..655,000

OLD direct-equality mismatches = 2426

Selected candidate:
- source = Reservoirs
- target = H1
- transition = HIGH_TO_LOW
- lag = 80 rows

Discovery result:
- revised mismatches = 538
- corrected old mismatches = 2101
- introduced new mismatches = 213
- net mismatch reduction = 1888

The candidate was frozen before confirmation.

## Confirmation window

rows 700,001..705,000

OLD direct-equality rule:
- mismatches = 2600 / 5000
- mismatch fraction = 52.00%

Frozen revised rule:
- mismatches = 352 / 5000
- mismatch fraction = 7.04%

Net mismatch reduction = 2248
Relative mismatch reduction = 86.462%

Therefore:

THIRD_REVISION_LOOP_CONFIRMED

and:

CONFIRMATION_MISMATCH_REDUCTION_50_PERCENT = true

## Structural meaning

The direct equality assumption H1_STATE == RESERVOIRS_STATE was strongly incomplete.

The discovery window selected a directional temporal relation:

after Reservoirs changes from HIGH to LOW, H1 often remains in the previous HIGH state for a substantial interval.

Applying that same frozen relation on untouched confirmation data greatly reduced formal mismatches.

## Noepedia consequence

Noepedia now has three independent revision-loop demonstrations:

Experiment 033:
DV_eletric ↔ Motor_current
relative mismatch reduction = 99.565%

Experiment 036:
TP2 ↔ TP3
relative mismatch reduction = 78.981%

Experiment 037:
H1 ↔ Reservoirs
relative mismatch reduction = 86.462%

All three use the same structural logic:

old rule
-> mismatch
-> evidence-derived candidate
-> frozen revised rule
-> untouched confirmation
-> core re-evaluation
-> large mismatch reduction

## OPEN handling

The OPEN record was preserved.

Resolved component:
one directional Reservoirs HIGH_TO_LOW -> H1 lag relation.

Remaining OPEN:
- residual 352 mismatches
- other transition classes
- whether 80 rows is a stable timing object or the edge of a wider response distribution
- physical interpretation

## Claim boundary

Experiment 037 does not establish causal direction, physical truth, or a universal pressure law.

It establishes that a third relation family passed the same Noepedia revision architecture on untouched confirmation data.