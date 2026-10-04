# Experiment 028 — Exploratory LOAD_OFF Covariate Scan

> **Status:** exploratory candidate-generation experiment.

## Starting point

Experiment 027 produced 48 LOAD_OFF events:

```text
43 events response_rows in 26..50
5 events response_rows in 51..100
```

Experiment 028 asks whether these two response classes differ in other already-recorded raw channels.

## Response-class labels

Frozen from Experiment 027:

```text
CORE = response_rows <= 50
TAIL = response_rows > 50
```

The response-time rule is not recomputed differently.

## Frozen offsets

For every numeric channel except:

```text
timestamp
DV_eletric
Motor_current
```

report values at:

```text
t=-1
t=0
t=+1
t=+10
```

Motor_current is excluded because it directly defines the response label.

DV_eletric is excluded because it defines the event.

## Effect summaries

For each channel/offset:

```text
CORE median
TAIL median
median difference
Cliff's delta
```

Rank candidates by absolute Cliff's delta, then absolute median difference.

No p-value threshold and no confirmatory claim is used.

## Claim boundary

This experiment only generates candidate relations for later untouched-window confirmation.

Any top-ranked channel can be a chance finding because:

- TAIL has only 5 events;
- many channels are scanned;
- the same event window generated the response labels.
