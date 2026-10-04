# Experiment 036 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS
scientific result = SECOND_REVISION_LOOP_CONFIRMED
strong flag = true

Focused GitHub Actions verification:
run_id = 37209531573
conclusion = success

## Independent relation family

This experiment did not use DV_eletric or Motor_current in the rule under test.

Relation family:
TP2 pressure state vs TP3 pressure state.

## Calibration

TP2 threshold = 4.640123582876524
TP3 threshold = 8.99526111417688

Both thresholds were fitted independently on rows 1..50,000.

## Discovery window

rows 550,001..555,000

OLD direct-equality mismatches = 2332

Selected candidate:
- source = TP2
- target = TP3
- transition = HIGH_TO_LOW
- lag = 80 rows

Discovery result:
- revised mismatches = 501
- corrected old mismatches = 1974
- introduced new mismatches = 143
- net mismatch reduction = 1831

The candidate was then frozen before confirmation.

## Confirmation window

rows 600,001..605,000

OLD direct-equality rule:
- mismatches = 2474 / 5000
- mismatch fraction = 49.48%

Frozen revised rule:
- mismatches = 520 / 5000
- mismatch fraction = 10.40%

Net mismatch reduction = 1954
Relative mismatch reduction = 78.981%

Therefore:

SECOND_REVISION_LOOP_CONFIRMED

and:

CONFIRMATION_MISMATCH_REDUCTION_50_PERCENT = true

## Structural meaning

The direct assumption TP2_STATE == TP3_STATE was strongly incomplete.

The discovery window selected a directional temporal relation:

after TP2 changes from HIGH to LOW, TP3 often remains in the previous HIGH state for a substantial interval.

Applying that same frozen relation on untouched confirmation data greatly reduced formal mismatches.

## Noepedia consequence

Experiment 033 showed one full knowledge-revision loop in the DV_eletric ↔ Motor_current family.

Experiment 036 now shows the same structural process in a second independent relation family:

old rule
-> mismatch
-> finite candidate search
-> selected revised relation
-> freeze
-> untouched confirmation
-> core re-evaluation
-> large mismatch reduction

This weakens the interpretation that Experiment 033 was only a one-off compressor-specific success.

## OPEN handling

The OPEN record was preserved.

Resolved component:
one directional TP2 HIGH_TO_LOW -> TP3 lag relation.

Remaining OPEN:
- residual 520 mismatches
- other transition classes
- whether 80 rows is a stable interval or the edge of a broader distribution
- physical interpretation

## Claim boundary

Experiment 036 does not establish causal direction, physical truth, or a universal pressure-control law.

It establishes that a second independent relation family passed the same Noepedia revision architecture on untouched confirmation data.