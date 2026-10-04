# Experiment 015 — Label-Blind Temporal-Context Test of the Two COLD Families

> **Status:** preregistered real-data follow-up to Experiment 014.

## Motivation

Experiment 014 found two structurally separated COLD families:

~~~text
CLUSTER_0 ≈ short / recovering
CLUSTER_1 ≈ long / deep / persistent downward
~~~

The next OPEN is:

> **What additional relation distinguishes the long/deep family from the short/recovering family?**

The first contextual relation tested is **time-of-day phase**.

This experiment does not claim that clock time is causal.
It asks only whether the two structural families occupy different temporal phases of the observed process.

## Label-blind boundary

Before NAB anomaly labels are loaded, the temporal-context analyzer receives:

- Experiment 014 cluster assignments;
- episode start/end timestamps.

It does not receive anomaly windows.

For every eligible COLD episode, it derives:

~~~text
START_MINUTE_OF_DAY
START_PHASE_ANGLE
~~~

where:

~~~text
minute_of_day = hour * 60 + minute
phase_angle = 2π * minute_of_day / 1440
~~~

Only after `TEMPORAL_CONTEXT.json` has been written are NAB labels loaded.

## Frozen circular statistics

For each cluster, after restricting evaluation to outside-only COLD episodes, calculate:

~~~text
mean_cos = mean(cos(angle))
mean_sin = mean(sin(angle))

resultant_length R =
sqrt(mean_cos² + mean_sin²)
~~~

`R` ranges from 0 to 1:

~~~text
R ≈ 0  → start times spread around the day
R ≈ 1  → start times concentrated at a common daily phase
~~~

Also calculate the circular mean start time.

## Frozen cross-cluster phase separation

Let the circular mean angles be μ0 and μ1.

~~~text
phase_separation_hours =
minimum circular distance between μ0 and μ1
converted to hours
~~~

Range:

~~~text
0 ... 12 hours
~~~

## Preregistered scientific gate

A positive temporal-context result requires all of:

~~~text
CLUSTER_1 resultant_length >= 0.70
phase_separation_hours >= 2.0
CLUSTER_1 resultant_length - CLUSTER_0 resultant_length >= 0.20
~~~

Interpretation of PASS:

> the long/deep family is strongly concentrated in a daily phase that is meaningfully separated from the short/recovering family, and its phase concentration is substantially stronger.

Interpretation of FAIL:

> time-of-day alone does not justify the missing contextual distinction under the frozen test.

## Forbidden reinterpretation

If FAIL, do not change:

- cluster assignments;
- circular metric;
- concentration threshold;
- phase-separation threshold.

Any alternate temporal analysis becomes a later experiment.

## What this experiment does not establish

Even if PASS, it does not establish:

- ambient-temperature causation;
- operator schedule;
- maintenance schedule;
- machine load schedule;
- normality or abnormality.

It identifies only a reusable contextual relation:

~~~text
episode family ↔ daily phase
~~~

## Next OPEN

If PASS:

> **What physical or operational variable follows that daily phase and can explain the cluster difference?**

If FAIL:

> **Which non-temporal contextual variable is missing from the single-channel trace?**
