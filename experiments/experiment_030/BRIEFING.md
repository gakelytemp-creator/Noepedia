# Experiment 030 — Preregistered Replication of Direction-Dependent Response Times

> **Status:** confirmatory replication experiment.

## Purpose

Experiments 026–027 found a strong directional asymmetry:

```text
LOAD_ON  0->1 : response at k=0 for all observed events
LOAD_OFF 1->0 : median response ~42 rows, with a right tail
```

Experiment 030 tests whether that response-time structure transfers to a new untouched window.

## Untouched window

```text
rows 350,001..355,000
```

## Frozen event definitions

```text
LOAD_ON  = DV_eletric 0 -> 1
LOAD_OFF = DV_eletric 1 -> 0
```

## Frozen raw target regimes

Reuse Experiments 025–027:

```text
band_low  = 0.8821033735279131
band_high = 3.4159886439831877
```

Target regimes:

```text
LOAD_ON  target: Motor_current > band_high
LOAD_OFF target: Motor_current < band_low
```

## Frozen stable-entry response rule

For each transition anchor t:

```text
response_rows =
smallest k in 0..100 such that
Motor_current[t+k],
Motor_current[t+k+1],
Motor_current[t+k+2]
are all in the target regime.
```

If no such k exists:

```text
RIGHT_CENSORED_>100
```

## Frozen summaries

For LOAD_ON and LOAD_OFF separately report:

```text
event_count
resolved_count
censored_count
already_target_t_minus_1
already_target_t0
min
mean
median
p25
p75
p90
p95
max
histogram:
  0
  1
  2-5
  6-10
  11-25
  26-50
  51-100
  >100
```

## Replication classes

LOAD_ON replication:

```text
LOAD_ON_IMMEDIATE_REPLICATED
    median == 0
    AND at least 90% of resolved events have response_rows == 0
```

LOAD_OFF replication:

```text
LOAD_OFF_DELAY_REPLICATED
    median in [26,50]
    AND at least 75% of resolved events fall in 26-50
```

Overall:

```text
DIRECTIONAL_ASYMMETRY_REPLICATED
    both class-specific criteria pass

PARTIAL_REPLICATION
    exactly one passes

NOT_REPLICATED
    neither passes
```

The thresholds above are frozen before outcome inspection.

## Claim boundary

Replication establishes transfer of the response-time structure under the same operational definition.

It does not establish:

```text
causality
mechanism
ground truth
fault
anomaly
universal compressor dynamics
```
