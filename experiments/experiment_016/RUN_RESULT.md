# Experiment 016 — Verified Run Result

> **Status:** repository CI reproduction passed.
>
> **Scientific result:** FAIL under the preregistered pre-onset drift gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37174865988
job: verify
conclusion: success
head commit: 69fc39bf22dcf54c574d9b8d261297593f13c015
~~~

## Pipeline

~~~text
pinned NAB real sensor trace
→ unchanged Experiment 011 detector
→ unchanged Experiment 012 episode decomposition
→ unchanged Experiment 013 transition descriptors
→ unchanged Experiment 014 clusters
→ label-blind two-hour pre-onset window
→ Theil–Sen normalized drift
→ pre_onset.json
→ only then load NAB labels
→ directional cluster comparison
~~~

## Observed result

### CLUSTER_0

~~~text
episodes                         15
median slope_z_per_hour      -1.4686
median half-window shift z   -1.3065
median robust range z         2.6812
~~~

### CLUSTER_1

~~~text
episodes                          4
median slope_z_per_hour      -1.7043
median half-window shift z   -1.3456
median robust range z         7.8827
~~~

Cross-cluster slope comparison:

~~~text
median slope difference
CLUSTER_1 - CLUSTER_0
= -0.2357

pairwise downward dominance
= 0.7833
~~~

## Preregistered gate

~~~text
median slope_z_per_hour(CLUSTER_1) <= -0.50

median slope_z_per_hour(CLUSTER_1)
-
median slope_z_per_hour(CLUSTER_0)
<= -0.75

pairwise_downward_dominance >= 0.75
~~~

Observed:

~~~text
-1.7043 <= -0.50     PASS
-0.2357 <= -0.75     FAIL
0.7833 >= 0.75       PASS
~~~

Therefore:

~~~text
scientific_result = FAIL
~~~

## Interpretation

The long/deep family often has a more negative pre-onset slope than the short/recovering family, as shown by the pairwise directional statistic:

~~~text
0.7833
~~~

But the difference in median normalized slope is small:

~~~text
-0.2357 robust-scale units per hour
~~~

and does not satisfy the preregistered magnitude gate.

The hypothesis that the two families are primarily distinguished by a substantially stronger two-hour downward pre-onset drift is therefore not supported.

## New structural clue

A descriptive variable not used as the primary success criterion differs much more strongly:

~~~text
median PRE robust range z

CLUSTER_0 ≈ 2.68
CLUSTER_1 ≈ 7.88
~~~

This suggests that the long/deep family may be preceded not simply by a steeper monotonic drift, but by a much wider or less stable pre-onset state.

That observation is exploratory only.

## New OPEN

> **Is pre-onset instability / range, rather than mean downward slope, the contextual relation that distinguishes the long/deep family?**

Experiment 016 does not answer this question.

Any direct test of pre-onset instability must be preregistered as a new experiment rather than promoted from this exploratory observation.
