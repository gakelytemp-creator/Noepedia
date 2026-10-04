# Experiment 014 — Label-Blind Structural Clustering of COLD Episodes

> **Status:** preregistered real-data follow-up to Experiment 013.

## Motivation

Experiment 013 failed the preregistered hypothesis that outside-only COLD episodes are predominantly one class of persistent downward level shifts.

Observed:

~~~text
outside-only COLD episodes = 19
DOWNWARD_LEVEL_SHIFT       = 9
RECOVERED_COLD_EXCURSION   = 2
OTHER_COLD                 = 8
~~~

The point-weighted result was different:

~~~text
318 / 480 mismatch points
= 66.25%
~~~

were inside DOWNWARD_LEVEL_SHIFT episodes.

This suggests a new question:

> **Do COLD episodes form more than one structural family when clustered without anomaly labels?**

Experiment 014 tests that question.

## Label-blind boundary

Before NAB anomaly labels are loaded, the clustering stage receives only:

- the pinned real sensor trace;
- Experiment 011 mismatch events;
- Experiment 012 episode boundaries;
- Experiment 013 PRE/POST transition descriptors.

The clustering stage does **not** receive NAB anomaly windows.

Only after `CLUSTERS.json` has been written are external labels loaded.

## Frozen feature vector

For every COLD episode with sufficient PRE/POST context, use:

~~~text
log1p(mismatch_count)
log1p(duration_minutes)
episode_shift_z
post_shift_z
log1p(max_robust_z)
~~~

No label-derived feature is allowed.

## Frozen normalization

For each feature across all eligible COLD episodes:

~~~text
center = median(feature)
scale  = max(1.4826 * MAD(feature), 1e-6)
z      = (feature - center) / scale
~~~

## Frozen clustering algorithm

Use deterministic k-means with:

~~~text
k = 2
distance = Euclidean distance in normalized feature space
initial centroids = farthest pair of eligible COLD episodes
maximum iterations = 100
tie-break = lexical episode_id
~~~

No random seed is used because initialization is deterministic.

If an empty cluster occurs, the run is a structural failure and must not silently reseed.

## Frozen structural evaluation

After clusters are fixed, load NAB labels and restrict scientific evaluation to outside-only COLD episodes.

Report:

- outside-only COLD episode count;
- cluster membership counts;
- cluster mismatch-point counts;
- silhouette score over outside-only COLD episodes using the frozen normalized vectors;
- centroid distance;
- per-cluster medians of:
  - mismatch_count;
  - duration_minutes;
  - episode_shift_z;
  - post_shift_z;
  - max_robust_z.

## Preregistered scientific gate

A positive structural result requires all of:

~~~text
each outside-only cluster has >= 3 episodes
silhouette_score >= 0.35
centroid_distance >= 2.0
~~~

Interpretation of PASS:

> the label-blind feature space contains two nontrivial, measurably separated families among outside-only COLD episodes.

Interpretation of FAIL:

> the current five-feature representation does not justify a two-family claim under the frozen clustering rule.

## Forbidden reinterpretation

If the gate fails, do not change:

- k;
- feature list;
- normalization;
- initialization rule;
- distance metric;
- scientific gate.

Any alternate clustering becomes a new experiment.

## What this experiment does not establish

Even if PASS:

- clusters are not fault classes;
- clusters are not causal mechanisms;
- clusters are not automatically normal/abnormal regimes;
- cluster identity is not a repair decision.

The experiment tests only structural separability.

## Next OPEN

If two families are supported:

> **Which additional external relation would explain the difference between the families?**

If they are not:

> **Which missing variable or relational cut prevents the COLD episodes from separating structurally?**
