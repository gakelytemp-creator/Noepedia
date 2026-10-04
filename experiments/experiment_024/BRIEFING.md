# Experiment 024 — Frozen Threshold Sensitivity Test

> **Status:** preregistered real-data transfer experiment.

## Motivation

Experiments 021 and 023 showed a highly reproducible structure:

```text
DV_eletric = TP2
Motor_current differs
```

with the disagreement concentrated near DV_eletric transitions and overwhelmingly after them.

One plausible physical/data-processing explanation is that Motor_current is continuous while the experiment converts it into a binary state through one threshold.

Experiment 024 directly tests whether the observed disagreement structure changes systematically when only that threshold changes.

## Untouched evaluation window

The new window is frozen before outcome inspection:

```text
rows 150,001..155,000
```

Calibration remains:

```text
rows 1..50,000
```

No threshold is fit on the new window.

## Frozen calibration

Fit the same deterministic 1-D k-means to Motor_current on rows 1..50,000:

```text
low centroid  = L
high centroid = H
```

Instead of using only the midpoint, define the frozen threshold family:

```text
T(alpha) = L + alpha * (H-L)

alpha:
0.20
0.30
0.40
0.50
0.60
0.70
0.80
```

The previous midpoint corresponds to alpha=0.50.

TP2 retains its original independent k-means midpoint threshold.

## Frozen paths

Path A:

```text
DV_eletric -> STATE_LOADED / STATE_NOT_LOADED
```

Path C:

```text
TP2 -> frozen first-50,000-row midpoint -> state
```

Path B becomes seven parallel candidate-state relations, each reading only Motor_current and one preregistered threshold.

No path asserts mismatch, support, artifact, normality, anomaly, fault, lag, or truth.

## Explicit core rules

For each alpha, the field contains:

```text
DIGITAL_CANDIDATE_STATE
vs
CURRENT_CANDIDATE_STATE_Axx
```

using the frozen Experiment 003 SAME_NET evaluator grammar.

A separate fixed rule checks:

```text
DIGITAL_CANDIDATE_STATE
vs
PRESSURE_CANDIDATE_STATE
```

Thus A=C eligibility is independent of the Motor_current threshold family.

## Measurements per alpha

For anchors where:

```text
Path A == Path C
```

report:

```text
A-vs-B(alpha) mismatch count
mismatch fraction
nearest-DV-transition histogram
AT / AFTER / BEFORE / EQUIDISTANT direction counts
NEAR / INTERMEDIATE / STABLE_FAR counts
```

The same temporal bins are frozen from Experiment 021:

```text
0
1
2-5
6-10
11-25
26-50
51-100
>100
```

## Primary sensitivity summary

Across alpha, report:

```text
min mismatch count
max mismatch count
range = max-min

midpoint alpha=0.50 mismatch count

whether mismatch counts are:
- monotonically nondecreasing
- monotonically nonincreasing
- neither
```

Also report the mismatch-count sequence exactly.

No minimum range is preregistered.

## Scientific interpretation classes

The experiment reports one of:

```text
THRESHOLD_INVARIANT
    all seven mismatch counts are identical

THRESHOLD_MONOTONIC
    mismatch counts are monotonic with alpha and not all equal

THRESHOLD_NONMONOTONIC
    mismatch counts vary but are not monotonic
```

These are descriptive classes, not causal conclusions.

## Evaluability gate

The experiment is evaluable only if:

- the first-50,000-row Motor_current centroids reproduce;
- the TP2 midpoint reproduces;
- exactly 5,000 new assessments are built;
- all seven preregistered alpha thresholds are present;
- every assessment receives exactly one evaluator event for every alpha rule and for A-vs-C;
- every dominant A=C anchor has frozen temporal descriptors;
- no threshold is selected or optimized after looking at the new window;
- all OPEN records remain unchanged.

## Claim boundary

A threshold-dependent result would support only:

> The binary disagreement geometry depends on the chosen Motor_current discretization threshold.

It would not by itself prove that all disagreement is an artifact.

A threshold-invariant residue, if present, would be a stronger candidate for structure not explained solely by threshold placement.

None of the result classes establishes:

```text
ground truth
fault
anomaly
causality
physical independence
universal lag
```
