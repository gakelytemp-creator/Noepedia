# Experiment 016 — Label-Blind Pre-Onset Drift Test

> **Status:** preregistered real-data follow-up to Experiment 015.

## Motivation

Experiment 014 established two structural COLD families.
Experiment 015 showed that simple time-of-day phase does not explain their difference.

The next question is:

> **Does the long/deep persistent family begin after a stronger downward drift already visible before episode onset?**

This tests a dynamical relation rather than a clock relation.

## Label-blind boundary

Before NAB anomaly labels are loaded, the analyzer receives:

- the pinned real temperature trace;
- Experiment 014 cluster assignments;
- episode start timestamps.

It does not receive anomaly windows.

For every eligible COLD episode it examines only raw samples that occur **before** episode onset.

Only after `PRE_ONSET.json` is written are NAB labels loaded.

## Frozen pre-onset window

Use the 24 raw samples immediately before episode start.

At approximately five-minute sampling, this is about two hours.

Episodes without 24 preceding raw samples are marked `INSUFFICIENT_CONTEXT`.

## Frozen trend estimator

For the 24-point PRE window:

1. compute the median;
2. compute MAD;
3. define robust scale:

~~~text
pre_scale = max(1.4826 * MAD, 1e-6)
~~~

4. estimate slope by the Theil–Sen rule:

~~~text
slope_per_sample =
median of all pairwise slopes
(value_j - value_i) / (j - i)
for j > i
~~~

5. convert to an approximately hourly normalized drift:

~~~text
slope_z_per_hour =
(slope_per_sample * 12) / pre_scale
~~~

because 12 samples ≈ 1 hour.

Also record, descriptively:

- PRE robust range in scale units;
- PRE first-half median;
- PRE second-half median;
- half-window shift z.

## Frozen directional test

After pre-onset descriptors are frozen, load NAB labels and restrict evaluation to outside-only COLD episodes.

Compare:

~~~text
CLUSTER_1 = long/deep/persistent family
CLUSTER_0 = short/recovering family
~~~

Primary separation statistic:

~~~text
pairwise_downward_dominance =
fraction of all CLUSTER_1 × CLUSTER_0 pairs
where slope_z_per_hour(CLUSTER_1)
<
slope_z_per_hour(CLUSTER_0)

ties contribute 0.5
~~~

This is equivalent to a directional rank-separation measure and does not assume Gaussian distributions.

## Preregistered scientific gate

A positive pre-onset drift result requires all of:

~~~text
median slope_z_per_hour(CLUSTER_1) <= -0.50

median slope_z_per_hour(CLUSTER_1)
-
median slope_z_per_hour(CLUSTER_0)
<= -0.75

pairwise_downward_dominance >= 0.75
~~~

Interpretation of PASS:

> the long/deep family tends to enter its episode after a substantially stronger downward pre-onset drift than the short/recovering family.

Interpretation of FAIL:

> the current two-hour pre-onset slope does not justify that distinction.

## Forbidden reinterpretation

If FAIL, do not change:

- 24-sample window;
- Theil–Sen estimator;
- normalization;
- directional statistic;
- scientific gate.

Any alternative window or derivative model becomes a later experiment.

## What this experiment does not establish

Even if PASS, it does not establish:

- causality;
- machine load change;
- ambient influence;
- maintenance event;
- fault identity.

It identifies only a dynamical contextual relation:

~~~text
episode family ↔ pre-onset drift
~~~

## Next OPEN

If PASS:

> **What causes the stronger pre-onset drift, and can that cause be represented by an additional observable relation?**

If FAIL:

> **Which other local dynamical feature — stability duration, curvature, recovery dynamics, or external context — distinguishes the families?**
