# Experiment 071 — RUN RESULT

## Final status

`ANY_SHUFFLED_PROMOTION`

Experiment class:
`SCIENTIFIC_REAL_DATA`

Focused verification run:
`37308635015`

Frozen Noepedia core:
`e9885e1bc3f0fcddad2d982eea2ec273e968575e`

Frozen external source:
`efeolgun/robot-predictive-maintenance`
commit:
`cec9f8a95d6099201cbf9afb8821696dc0ebd7cd`

Selected blind sequence:
`20240527_094865`

## Adapter result

Input candidate channels:
`18`

Valid channels after calibration-only adapter gate:
`7`

Invalid channels:
`11`

Valid channels:

- motor1_temperature
- motor2_voltage
- motor3_position
- motor4_voltage
- motor6_position
- motor6_temperature
- motor6_voltage

The experiment remained evaluable because the preregistered minimum requirements were met:

- at least 6 valid channels;
- at least 2 distinct motors;
- at least 2 distinct signal types.

All six motor files contained 2423 aligned rows with monotonic time.

## Frozen split

- calibration = 500
- discovery = 800
- buffer = 300
- confirmation = 823

## Primary outcome

Real-data promotions:

`6`

Deterministic shuffled-control promotions:

`6`

Therefore the preregistered primary class is:

`ANY_SHUFFLED_PROMOTION`

This is the primary failure class.

No rescue or threshold change is permitted inside Experiment 071.

## Promotion-family diagnostic

All real promotions were:

`SIMPLER_RULE_COMPARATOR`

All shuffled promotions were also:

`SIMPLER_RULE_COMPARATOR`

No temporal/directional promotion is responsible for the shuffled failure.

### Real promoted pairs

1. motor1_temperature -> motor2_voltage
2. motor1_temperature -> motor4_voltage
3. motor2_voltage -> motor6_voltage
4. motor4_voltage -> motor6_voltage
5. motor6_position -> motor6_voltage
6. motor6_temperature -> motor6_voltage

### Shuffled promoted pairs

1. motor1_temperature -> motor2_voltage
2. motor1_temperature -> motor4_voltage
3. motor1_temperature -> motor6_voltage
4. motor4_voltage -> motor6_voltage
5. motor6_position -> motor6_voltage
6. motor6_temperature -> motor6_voltage

Five promoted pairs overlap between real and shuffled controls.

## Failure mechanism indicated by 071

The class-imbalance feature can generate a:

`SIMPLER_RULE_COMPARATOR`

candidate.

In the generic observation-pair path, the proposed confirmation sequence is the source relation state sequence.

The simpler comparator freezes the target-majority state on discovery and evaluates that frozen majority rule on confirmation.

Under distribution shift, the frozen discovery-majority rule can perform poorly on confirmation even when source/target temporal correspondence has been destroyed by shuffling.

Therefore the source relation can appear to beat the frozen majority comparator without carrying genuine pairwise temporal structure.

This is consistent with the observed result:

`real promotions ~= shuffled promotions`

and with every shuffled promotion belonging to the simpler-rule family.

## Scientific interpretation

Experiment 071 does not demonstrate blind discovery capability.

It demonstrates a false-positive path in the repaired pipeline.

The primary safety requirement:

`shuffled promotion count = 0`

failed.

Therefore the correct conclusion is not to interpret any of the six real promotions physically.

They are not promoted knowledge.

## Integrity statement

After outcome inspection, no change was made to:

- sequence selection;
- telemetry channels;
- split;
- adapter;
- minimum cluster-size gate;
- pair universe;
- lag range;
- null models;
- shuffle seeds;
- promotion gates;
- frozen core.

Experiment 071 is closed as a preregistered failure.

## Required next work

Before another scientific blind challenge, the simpler-rule path must be audited and repaired.

The next architecture experiment should establish that:

1. a comparator/null family cannot become a promoted relation merely because a frozen discovery-majority baseline degrades under confirmation distribution shift;
2. shuffled pair data cannot promote through class-imbalance-only structure;
3. positive temporal synthetic controls remain promotable;
4. class-imbalance controls under train/confirmation prevalence shift remain non-promotable.

Only after those tests pass should another real-data blind challenge receive a new experiment number.
