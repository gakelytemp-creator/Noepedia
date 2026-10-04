# Experiment 040 — RUN RESULT

## Status

reproducibility = PASS
scientific result = NULL_PROTECTED_REVISION_CONFIRMED

Focused GitHub Actions verification:
run_id = 37225483333
conclusion = success

## Calibration-only family selection

Frozen candidate families:
- DV_pressure -> TP2
- COMP -> Motor_current
- Towers -> TP3
- LPS -> Reservoirs

Eligible calibration mismatch interval:
5%..40%

Selected family:
COMP -> Motor_current

Calibration mismatch fraction = 23.706%

Frozen orientation:
COMP 0 -> CURRENT_HIGH
COMP 1 -> CURRENT_LOW

Motor_current threshold = 2.1490460087555503

## Discovery window

rows 950,001..955,000

OLD direct-mapping mismatches = 1616

Selected candidate:
- transition = HIGH_TO_LOW
- lag = 40 rows
- lag boundary hit = false

Discovery revised mismatches = 15
net reduction vs old = 1601

The lag curve has a clear interior minimum at 40 rows.

## Confirmation window

rows 1,000,001..1,005,000

OLD rule:
- mismatches = 1982 / 5000
- mismatch fraction = 39.64%

REVISED frozen temporal rule:
- mismatches = 26 / 5000

Majority-state null:
- mismatches = 2690

Permutation temporal nulls:
- shift 500 = 2909
- shift 1000 = 3225
- shift 1500 = 1729
- shift 2000 = 2361
- median = 2635

Relative mismatch reduction:
- vs OLD = 98.688%
- vs majority null = 99.033%
- vs permutation-null median = 99.013%

All preregistered confirmation gates passed:
- revised < old
- revised beats majority null by >=10%
- revised beats permutation median by >=10%
- selected lag is not at the search boundary

Therefore:

NULL_PROTECTED_REVISION_CONFIRMED

## Noepedia significance

Experiment 040 is a second strong null-protected knowledge-revision example on this dataset.

It differs structurally from Experiment 033 in that:
- the relation family was selected using calibration data only from a frozen candidate list
- discovery selected the temporal correction
- confirmation used explicit majority and time-shift null baselines from the start

The successful sequence is:

calibration-only family selection
-> OLD rule
-> discovery mismatch
-> temporal candidate selection
-> freeze
-> untouched confirmation
-> majority null comparison
-> permutation null comparison
-> large retained improvement

## Relation to Experiment 033

Experiment 040 uses Motor_current as one channel, so it should not be described as physically independent of Experiment 033.

It is a distinct measurement relation and an independent null-protected confirmation design, not a separate physical system.

## OPEN handling

The temporal relation can be promoted to empirically supported status for this tested domain, while keeping OPEN on:
- physical/controller interpretation
- transfer outside tested windows
- relation to the DV_eletric timing structure from Experiment 033

## Claim boundary

Experiment 040 does not establish causal mechanism, physical independence, or universal controller behavior.

It establishes that a second preregistered, null-protected revision procedure produced a large improvement on untouched confirmation data.