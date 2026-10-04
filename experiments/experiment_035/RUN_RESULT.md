# Experiment 035 — RUN RESULT

## Status

reproducibility = PASS
result = PRE_LOAD_ON_PATTERN_WEAK

Focused GitHub Actions verification:
run_id = 37204494070
conclusion = success

## Untouched window

rows 500,001..505,000

## LOAD_ON events

event count = 28

Events with any Motor_current HIGH row in t-6..t-1:

3 / 28
= 10.71%

Preregistered replication threshold was 50%.

Therefore:

PRE_LOAD_ON_PATTERN_WEAK

not:

PRE_LOAD_ON_PATTERN_REPLICATED

## Earliest pre-HIGH offsets

-6 rows: 2 events
-5 rows: 0
-4 rows: 0
-3 rows: 0
-2 rows: 0
-1 row: 1 event
NO_PRE_HIGH: 25 events

## Motor_current at LOAD_ON itself

HIGH at t=0:

27 / 28
= 96.43%

So the strong result from Experiments 027 and 030 remains:

Motor_current is usually already HIGH at the LOAD_ON transition itself.

But a repeated 1..6-row pre-transition HIGH interval is uncommon.

## Interpretation

Experiment 034 found six consecutive residual mismatches immediately before one LOAD_ON transition.

Experiment 035 shows that this geometry does not generalize as a common rule across LOAD_ON events.

The 034 pattern should therefore remain a local residual episode, not be promoted into the Noepedia revised rule.

This is an important negative result:

local repeated structure != general rule

## Consequence for Experiment 033 rule

No second temporal exception is added.

The Experiment 033 revised rule remains unchanged.

The six residuals from Experiment 034 remain part of the OPEN rather than being absorbed by a weakly supported repair.

## Claim boundary

Experiment 035 does not establish that pre-LOAD_ON current rise never occurs.

It establishes only that the preregistered 1..6-row pre-HIGH pattern did not replicate strongly on this untouched window.