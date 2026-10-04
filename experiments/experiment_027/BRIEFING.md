# Experiment 027 — Preregistered Per-Transition Response-time Distribution

> **Status:** preregistered simultaneously with Experiment 026, before inspecting Experiment 026 results.

## Question

Does a single fixed lag fail because individual DV transitions have a distribution of raw Motor_current response times?

## Event set

Use exactly the DV_eletric transition anchors from Experiment 026:

```text
anchor rows 250,001..255,000
LOAD_ON  = 0 -> 1
LOAD_OFF = 1 -> 0
```

## Frozen target regimes

Reuse the Experiment 025/026 raw gap:

```text
band_low  = 0.8821033735279131
band_high = 3.4159886439831877
```

No new threshold is estimated.

Target regime:

```text
LOAD_ON  target: Motor_current > band_high
LOAD_OFF target: Motor_current < band_low
```

## Stable-entry rule

For each transition at t, response time is:

```text
the smallest k in 0..100 such that
Motor_current at k, k+1, and k+2
are all in the target regime
```

The 3-row persistence rule is frozen to avoid counting a one-row excursion.

If no such k exists by +100:

```text
RIGHT_CENSORED_>100
```

## Additional frozen descriptors

For each transition report whether the signal is already in the target regime at:

```text
t-1
t
```

and summarize response-time distributions with:

```text
resolved count
censored count
min
median
p25
p75
p90
p95
max
mean
```

Histogram bins:

```text
0
1
2-5
6-10
11-25
26-50
51-100
>100 censored
```

## Interpretation

A broad response-time distribution would explain why one constant signed offset can fail even when a strong post-transition geometry repeats.

A narrow distribution would support a more fixed timing relation.

Neither result establishes causality or ground truth.
