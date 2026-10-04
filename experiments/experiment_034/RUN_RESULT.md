# Experiment 034 — RUN RESULT

## Status

reproducibility = PASS
classification = SINGLE_RESIDUAL_PATTERN

Focused GitHub Actions verification:
run_id = 37203756498
conclusion = success

## Starting point

Experiment 033 left 6 revised-rule formal mismatches on rows 450,001..455,000.

Experiment 034 introduced no new rule and performed only descriptive residual analysis.

## Result

All 6 residual mismatches share one structural signature:

- DV_eletric = 0
- revised expected state = CURRENT_LOW
- observed state = CURRENT_HIGH
- rows since last LOAD_OFF > 100
- next DV transition is within 1..6 rows

Therefore:

SINGLE_RESIDUAL_PATTERN

## Six residual rows

451284: next DV transition in 6 rows, Motor_current = 3.8075
451285: next DV transition in 5 rows, Motor_current = 3.7450
451286: next DV transition in 4 rows, Motor_current = 3.8425
451287: next DV transition in 3 rows, Motor_current = 3.7425
451288: next DV transition in 2 rows, Motor_current = 3.7850
451289: next DV transition in 1 row, Motor_current = 3.8500

All six occur consecutively.

At these rows:

TP2 remains near zero:
- approximately -0.014 to -0.012

TP3 remains near:
- 8.148 down to 8.090

## Structural interpretation

The residuals are not a continuation of the LOAD_OFF long tail.

They occur more than 100 rows after the last LOAD_OFF transition and immediately before the next DV transition.

The descriptive pattern is:

DV still reports 0
while Motor_current is already in the HIGH regime
for the final 1..6 rows before the next DV transition.

This is consistent with a possible pre-LOAD_ON current rise, but Experiment 034 does not promote that interpretation to a rule.

## What this changes

After Experiment 033 the remaining OPEN looked like six unexplained residual mismatches.

After Experiment 034 those six rows are no longer six unrelated points.

They form one compact temporal structure attached to the next transition.

Thus the remaining OPEN can be narrowed further:

possible pre-LOAD_ON temporal relation

rather than:

generic unexplained residual mismatches

## Claim boundary

Experiment 034 does not establish:

- that Motor_current physically causes or precedes LOAD_ON
- that a 1..6-row anticipation interval is universal
- that the DV signal is delayed
- fault or anomaly

It only establishes that all six residual mismatches in this window share the same pre-transition geometry.

## Next clean test

A new untouched-window experiment should test a preregistered prediction:

before each LOAD_ON transition, does Motor_current enter the HIGH regime within a short pre-transition interval, and with what distribution?

That test should be performed before adding a second temporal exception to the Noepedia rule.