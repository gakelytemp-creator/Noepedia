# Experiment 025 — RUN RESULT

## Status

```text
reproducibility   = PASS
scientific class  = RAW_BAND_SPARSE
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37190828564
conclusion = success
```

## Frozen untouched window

```text
calibration     = rows 1..50,000
raw-gap test    = rows 200,001..205,000
```

The window and raw-value test were frozen before outcome inspection.

## Frozen Motor_current threshold band

From Experiment 024:

```text
band low  = 0.8821033735279131
band high = 3.4159886439831877
```

The first-50,000-row calibration reproduced:

```text
low centroid  = 0.03747495004282162
high centroid = 4.260617067468279
midpoint      = 2.1490460087555503
```

## Primary raw-band result

Across all 5,000 untouched rows:

```text
BELOW_BAND = 3246
IN_BAND    =    2
ABOVE_BAND = 1752
-----------------
total      = 5000
```

Therefore:

```text
in-band fraction = 2 / 5000
                 = 0.0004
                 = 0.04%
```

Preregistered class:

```text
RAW_BAND_SPARSE
```

The frozen interval spanning most of the two calibration centroids is almost empty on this untouched window.

## Gap geometry

The closest observed values outside the band were:

```text
closest below band = 0.0725
band low           = 0.8821

band high          = 3.4160
closest above band = 3.6775
```

Thus the observed low and high raw-value regions are separated by a large sparsely occupied interval.

Overall raw Motor_current summary:

```text
min     = 0.0300
p05     = 0.0350
p25     = 0.0375
median  = 0.0375
p75     = 3.7650
p95     = 5.9051
max     = 8.0075
```

The median remains in the low cluster while the upper quartile is already above the entire frozen threshold band.

## Temporal split

### NEAR — within 10 rows of a DV_eletric transition

```text
BELOW_BAND = 320
IN_BAND    =   0
ABOVE_BAND = 756
----------------
total      = 1076
```

Raw summary:

```text
min     = 0.0325
median  = 3.8250
p75     = 5.8775
p95     = 6.1656
max     = 8.0075
```

### INTERMEDIATE — 11..100 rows from transition

```text
BELOW_BAND = 2908
IN_BAND    =    2
ABOVE_BAND =  996
-----------------
total      = 3906
```

Raw summary:

```text
min     = 0.0300
median  = 0.0375
p75     = 3.7025
p95     = 3.8050
max     = 3.9300
```

### STABLE_FAR — more than 100 rows from transition

```text
BELOW_BAND = 18
IN_BAND    =  0
ABOVE_BAND =  0
---------------
total      = 18
```

Raw summary:

```text
min     = 0.0350
median  = 0.0375
max     = 0.0400
```

In this window, every STABLE_FAR raw Motor_current value is in the low region.

## A=C subset

The A=C reference subset contains:

```text
4977 rows
```

Its raw-band counts are:

```text
BELOW_BAND = 3246
IN_BAND    =    2
ABOVE_BAND = 1729
-----------------
total      = 4977
```

So:

```text
in-band fraction
= 2 / 4977
≈ 0.0402%
```

and its preregistered class is also:

```text
RAW_BAND_SPARSE
```

The two in-band observations are in the INTERMEDIATE temporal region; none occur in NEAR or STABLE_FAR.

## Interpretation

Experiment 025 strongly supports a broad raw-signal-gap explanation for why the Experiment 024 threshold family can behave invariantly.

The key empirical fact is:

```text
0.8821 .. 3.4160
contains only 2 / 5000 raw Motor_current observations
on a new untouched window.
```

Therefore moving a binary threshold anywhere across most of this interval will usually leave the binary Motor_current state unchanged.

This does **not** retroactively prove the exact Experiment 024 window had the identical raw distribution, because Experiment 025 deliberately used a different untouched window.

It does, however, show that the threshold-invariance mechanism is physically/data-wise plausible and itself transfers to another separated window.

## Relation to the earlier hypothesis

The original simple hypothesis was:

> The temporal mismatch structure is mainly caused by the arbitrary placement of the single midpoint threshold.

Experiment 024 argued against that narrow claim because thresholds from alpha=0.20 to 0.80 produced identical classifications.

Experiment 025 explains why those threshold choices may be functionally equivalent:

> The raw Motor_current signal itself spends almost no time in the entire threshold interval.

So the better model is no longer:

```text
midpoint placement artifact
```

but potentially:

```text
two-regime Motor_current signal
+
transition-associated switching between those regimes
```

The remaining question is not where to put the binary threshold inside the gap, but what temporal process governs movement between the low and high raw regimes.

## Claim boundary

Experiment 025 does not establish:

```text
causality
fault
anomaly
ground truth
physical independence
universal compressor dynamics
```

Nor does a sparse raw band prove that all previous disagreement is a discretization artifact.

## OPEN after Experiment 025

The next clean question is:

> For each DV_eletric transition, what does the raw Motor_current trajectory itself do before and after the transition, without binarizing it?

That suggests an event-aligned raw-signal experiment:

```text
DV transition at t=0
-> collect Motor_current raw trajectory around t
-> separate 0->1 and 1->0 transitions
-> summarize median / quantiles by signed row offset
```

This would test transition dynamics directly without choosing any Motor_current threshold.
