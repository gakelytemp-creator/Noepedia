# Experiment 026 — RUN RESULT

## Status

```text
reproducibility = PASS
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37192202202
conclusion = success
```

## Frozen untouched event window

```text
DV transition anchors = rows 250,001..255,000
signed trajectory      = -100..+100 rows
```

The event window and summary rules were frozen before the outcome was inspected.

## Event counts

```text
LOAD_ON  (0 -> 1) = 47
LOAD_OFF (1 -> 0) = 48
```

## Raw Motor_current trajectory

### LOAD_ON

Selected Motor_current medians:

```text
t=-1   0.0375
t= 0   4.8700
t=+1   5.7175
t=+10  6.0450
t=+25  3.7900
t=+50  3.7975
t=+100 0.0400
```

At t=-1 the interquartile range is:

```text
p25 = 0.0375
p75 = 0.0400
```

At t=0:

```text
p25 = 4.72625
median = 4.8700
p75 = 5.1525
```

Thus the LOAD_ON transition is associated with an abrupt raw Motor_current jump between t=-1 and t=0 on this event set.

### LOAD_OFF

Selected Motor_current medians:

```text
t=-1   6.1650
t= 0   3.8875
t=+1   3.81875
t=+10  3.78375
t=+25  3.7800
t=+50  0.0400
t=+100 0.0400
```

At t=-1:

```text
p25 = 6.10875
median = 6.1650
p75 = 6.2250
```

At t=0:

```text
p25 = 3.8200
median = 3.8875
p75 = 3.9650
```

At t=+25 the median is still above the frozen high-band edge:

```text
band_high = 3.41599
median    = 3.7800
```

By t=+50 the median is in the low regime:

```text
median = 0.0400
```

## TP2 descriptive trajectory

TP2 was recorded only as a parallel raw trajectory.

LOAD_ON median:

```text
t=-1  = -0.014
t=0   =  3.956
t=+1  =  8.578
t=+10 = 10.154
```

LOAD_OFF median:

```text
t=-1  = 10.516
t=0   =  0.027
t=+1  = -0.024
t=+10 = -0.012
```

No truth or causal status is assigned to TP2.

## Main empirical result

The two transition directions have strongly different raw Motor_current geometry:

```text
LOAD_ON:
low regime at t=-1
-> high regime already at t=0

LOAD_OFF:
high regime at t=-1
-> remains above high-band threshold through the early post-transition window
-> reaches low regime tens of rows later
```

This directly explains why a single signed temporal offset is a poor model.

The temporal relation is direction-dependent rather than a symmetric constant lag.

## Important limitation

The event-aligned curves are descriptive ensemble summaries.

Because multiple DV transitions can occur within a ±100-row trajectory window, late offsets can contain influence from subsequent transitions.

Therefore the +50 and +100 landmarks should not be interpreted as an isolated single-step response function without additional event-isolation rules.

The strongest local result is the immediate asymmetry around t=-1, t=0, and the early post-transition window.

## Claim boundary

Experiment 026 does not establish:

```text
causality
ground truth
fault
anomaly
universal response law
physical independence
```

It establishes only a reproducible event-aligned raw-signal asymmetry on this frozen window.
