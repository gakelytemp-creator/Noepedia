# Experiment 025 — Raw Motor-current Distribution Relative to the Frozen Threshold Band

> **Status:** preregistered real-data transfer experiment.

## Motivation

Experiment 024 varied the Motor_current binarization threshold over:

```text
0.8821033735279131 .. 3.4159886439831877
```

yet every threshold produced the same disagreement count and temporal geometry.

A simple explanation is that the raw Motor_current values occupy separated low/high regions with little or no mass inside that threshold interval.

Experiment 025 tests that directly.

## Untouched evaluation window

Frozen before outcome inspection:

```text
rows 200,001..205,000
```

Calibration remains:

```text
rows 1..50,000
```

## Frozen threshold band

From the first-50,000-row Motor_current k-means centroids:

```text
L = low centroid
H = high centroid
```

use the Experiment 024 frozen thresholds:

```text
band_low  = L + 0.20*(H-L)
band_high = L + 0.80*(H-L)
```

Expected numerical values are the already frozen Experiment 024 values.

No fitting occurs on the Experiment 025 window.

## Raw-value regions

Each raw Motor_current value is classified only geometrically as:

```text
BELOW_BAND : x < band_low
IN_BAND    : band_low <= x <= band_high
ABOVE_BAND : x > band_high
```

These are raw range labels, not machine-state labels.

## Temporal split

Use the frozen DV_eletric transition relation from Experiments 021/023/024.

For each assessment, define nearest transition distance:

```text
min(rows_since_previous_transition,
    rows_until_next_transition)
```

Frozen coarse regions:

```text
NEAR         <= 10 rows
INTERMEDIATE 11..100 rows
STABLE_FAR   > 100 rows
```

Report raw Motor_current region counts separately for these temporal regions.

## Additional descriptive statistics

For each temporal region, report:

```text
count
minimum
maximum
median
p05
p25
p75
p95
```

Also report the closest raw values immediately below and above the threshold band if they exist.

## A=C subset

Because Experiments 020–024 focused on the A=C reference subset, repeat the same raw-band counts on:

```text
DV_eletric state == TP2 frozen state
```

No Motor_current threshold is used to define this subset.

## Evaluability gate

The experiment is evaluable only if:

- first-50,000-row Motor_current centroids reproduce;
- Experiment 024 band edges reproduce;
- TP2 frozen midpoint reproduces;
- exactly 5,000 untouched assessments are built;
- every assessment has one raw Motor_current value;
- every assessment has frozen temporal descriptors;
- A=C eligibility is computed independently of Motor_current;
- no new Motor_current classifier or optimized threshold is introduced.

## Result classes

```text
RAW_BAND_EMPTY
    zero Motor_current values lie in the frozen threshold band

RAW_BAND_SPARSE
    nonzero but <= 1% of values lie in the band

RAW_BAND_OCCUPIED
    > 1% of values lie in the band
```

The same class is also reported for the A=C subset.

## Claim boundary

If the band is empty or sparse, that explains why a wide family of thresholds can produce identical binary assignments.

It does not establish:

```text
causality
fault
anomaly
ground truth
physical independence
universal dynamics
```
