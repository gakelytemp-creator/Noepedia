# Experiment 032 — Event-wise Physical-Time Audit

> **Status:** preregistered audit of already frozen response events.

## Event sets

Reuse the exact LOAD_OFF response rule from Experiments 027 and 030 on:

```text
W027 = rows 250,001..255,000
W030 = rows 350,001..355,000
```

Response rule:

```text
first k in 0..100 where three consecutive Motor_current values
are below 0.8821033735279131
```

## Physical response time

For each resolved event:

```text
physical_response_seconds =
timestamp[t + k] - timestamp[t]
```

## Gap flag

Within the inclusive timestamp path from t through t+k:

```text
crosses_large_gap = any adjacent dt > 20 seconds
```

The 20 s threshold is frozen as 2 × the 10 s median cadence from Experiment 031.

## Outputs

For W027, W030, and combined:

```text
event count
gap-free event count
gap-crossing event count
min / mean / median / p25 / p75 / p90 / p95 / max
histogram:
  0-300 s
  301-450 s
  451-600 s
  601-1200 s
  >1200 s
```

Also report the same summaries restricted to gap-free events.

## Physical-time replication class

```text
PHYSICAL_TIME_CLUSTER_REPLICATED

iff:
- W027 gap-free median is in 360..480 s
- W030 gap-free median is in 360..480 s
- absolute difference between the two gap-free medians <= 60 s
```

Otherwise:

```text
PHYSICAL_TIME_CLUSTER_NOT_REPLICATED
```

## Claim boundary

This audit does not identify the mechanism.
It only tests whether the row-space object corresponds to a reproducible physical-time cluster.
