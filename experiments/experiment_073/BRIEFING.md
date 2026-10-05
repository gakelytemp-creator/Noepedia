# Experiment 073 — Preregistered Motor-1 Temperature/Voltage Lag Test

> PREREGISTERED BEFORE TELEMETRY OUTCOME INSPECTION

## 1. Hypothesis

For motor 1, temperature-state transitions lag voltage-state transitions by a positive fixed delay.

Source relation:
`motor1_voltage`

Target relation:
`motor1_temperature`

No other motor or pair may replace this pair after outcome inspection.

## 2. External source

Repository:
`efeolgun/robot-predictive-maintenance`

Frozen external commit:
`cec9f8a95d6099201cbf9afb8821696dc0ebd7cd`

Sequence:
`20240527_100759`

File:
`data/testing_data/20240527_100759/data_motor_1.csv`

Observed file length before preregistration:
`3187 rows`

The label column is ignored.

## 3. Timeline and split

The CSV row index is the common timeline.

Sampling is approximately 10 Hz.

Frozen split:

- calibration: rows 1..600
- discovery: rows 601..1800
- buffer: rows 1801..2100
- confirmation: rows 2101..3187

Counts:

- calibration = 600
- discovery = 1200
- buffer = 300
- confirmation = 1087

## 4. State construction

Voltage and temperature are independently binarized.

Method:
deterministic 1-D k-means fitted on calibration only.

Orientation:
- lower centroid -> STATE_LOW
- higher centroid -> STATE_HIGH

Threshold:
midpoint of calibration centroids.

Adapter validity requires, for both variables:

- finite distinct centroids;
- each calibration cluster >= 30 samples;
- finite threshold.

Otherwise:
`NOT_EVALUABLE_ADAPTER_VALIDATION`

## 5. Temporal hypothesis test

Candidate family is fixed before discovery:

`TEMPORAL_LAG_REVISION`

No candidate-family search is performed.

Positive lag search:

`1..600 samples`

At approximately 10 Hz:
`0.1..60 seconds`

Directions searched:

- LOW_TO_HIGH
- HIGH_TO_LOW

Discovery selects one direction and lag.

That direction and lag are frozen for untouched confirmation.

If the selected lag is 1 or 600:

`REMAIN_OPEN / SEARCH_BOUNDARY_UNRESOLVED`

## 6. Required nulls

Confirmation must beat:

1. frozen discovery-majority target comparator;
2. SIMPLER_RULE_NULL using the same frozen majority comparator;
3. circular-shift temporal null median.

Frozen circular shifts:

- 137
- 281
- 419

Required relative advantage over every metric null:

`10%`

## 7. Outcome classes

### HYPOTHESIS_SUPPORTED

All mandatory promotion gates pass.

### HYPOTHESIS_REJECTED

Confirmation is evaluable but the fixed hypothesis fails performance/null gates.

### HYPOTHESIS_REMAINS_OPEN

Boundary/evaluability uncertainty blocks a justified decision.

### NOT_EVALUABLE_ADAPTER_VALIDATION

The preregistered state adapter fails before hypothesis testing.

## 8. No rescue

After outcome inspection, do not change:

- motor;
- variables;
- sequence;
- split;
- k-means adapter;
- cluster-size gate;
- lag range;
- directions;
- null shifts;
- 10% null advantage.

Any alternative is a new experiment number.

## 9. Ten-line stop question

The final RUN_RESULT must answer:

`What do we know now that we did not know before Experiment 073?`
