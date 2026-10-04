# Experiment 014 — Verified Run Result

> **Status:** repository CI reproduction passed.
>
> **Scientific result:** PASS under the preregistered structural clustering gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37172525478
job: verify
conclusion: success
head commit: 3ed1d793e061bad6c88af9450b7c81d73fd0b763
~~~

## Pipeline

~~~text
pinned NAB real sensor trace
→ unchanged Experiment 011 detector
→ unchanged Experiment 012 episode decomposition
→ unchanged Experiment 013 transition descriptors
→ label-blind deterministic k=2 clustering
→ clusters.json
→ only then load NAB anomaly labels
→ structural evaluation
~~~

The clustering stage was completed before anomaly labels were downloaded.

## Frozen clustering representation

Features:

~~~text
log1p(mismatch_count)
log1p(duration_minutes)
episode_shift_z
post_shift_z
log1p(max_robust_z)
~~~

Normalization:

~~~text
median + 1.4826 × MAD
~~~

Clustering:

~~~text
k = 2
Euclidean distance
farthest-pair deterministic initialization
no random seed
~~~

## Observed result

~~~text
eligible COLD episodes clustered        21
outside-only COLD episodes              19

CLUSTER_0 episodes                      15
CLUSTER_1 episodes                       4

CLUSTER_0 mismatch points              223
CLUSTER_1 mismatch points              257

silhouette score                    0.5805761838
centroid distance                   5.8402787422
~~~

## Preregistered gate

~~~text
each outside-only cluster >= 3 episodes
silhouette_score >= 0.35
centroid_distance >= 2.0
~~~

Observed:

~~~text
cluster sizes = 15 and 4
silhouette    ≈ 0.581
distance      ≈ 5.84
~~~

Therefore:

~~~text
scientific_result = PASS
~~~

## Cluster profiles

### CLUSTER_0

~~~text
episodes                         15
mismatch points                 223
median mismatch count             7
median duration                  45 min
median episode_shift_z          -2.8437
median post_shift_z             -0.0865
median max_robust_z              6.8797
~~~

### CLUSTER_1

~~~text
episodes                          4
mismatch points                 257
median mismatch count            54
median duration                 280 min
median episode_shift_z         -12.1300
median post_shift_z             -6.4987
median max_robust_z             12.4534
~~~

## Interpretation

The frozen five-feature representation supports two nontrivial, strongly separated structural families among outside-only COLD episodes.

The small cluster is not merely a set of more numerous detections. It has a different profile:

~~~text
few episodes
+ many mismatch points
+ long duration
+ much deeper episode displacement
+ post-episode baseline remains strongly lower
+ larger mismatch magnitude
~~~

The larger cluster has the opposite profile:

~~~text
many episodes
+ fewer mismatch points per episode
+ shorter duration
+ moderate episode displacement
+ post-baseline returns near the prior level
+ lower mismatch magnitude
~~~

A compact working description is:

~~~text
CLUSTER_0 ≈ short / recovering COLD episodes
CLUSTER_1 ≈ long / deep / persistent downward episodes
~~~

These names are descriptive, not causal labels.

## Relation to Experiment 013

Experiment 013 failed the hypothesis that one persistent-downshift class dominates episode count.

Experiment 014 explains why that binary hypothesis was too coarse:

- the majority of episodes belong to the short/recovering family;
- a minority of four long/deep episodes contain 257 of 480 outside-only COLD mismatch points.

So the episode-count and point-count views were measuring different structural families rather than merely disagreeing statistically.

## What is still OPEN

The clusters are not yet identified as:

- normal operating modes;
- failures;
- maintenance effects;
- ambient influences;
- sensor artifacts.

The next question is no longer “are there two families?”

That question now has a positive structural answer.

The next OPEN is:

> **What external relation distinguishes the long/deep persistent family from the short/recovering family?**
