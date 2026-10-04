# Experiment 024 — RUN RESULT

## Status

```text
reproducibility      = PASS
architectural result = PASS
scientific class     = THRESHOLD_INVARIANT
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37190140201
conclusion = success
```

## Frozen untouched window

```text
calibration        = rows 1..50,000
threshold-test     = rows 150,001..155,000
```

The threshold family and window were frozen before outcome inspection.

## Frozen Motor_current calibration

First-50,000-row centroids:

```text
low centroid  = 0.03747495004282162
high centroid = 4.260617067468279
midpoint      = 2.1490460087555503
```

Frozen threshold family:

```text
alpha   threshold
0.20    0.8821033735279131
0.30    1.3044175852704587
0.40    1.7267317970130045
0.50    2.1490460087555503
0.60    2.571360220498096
0.70    2.9936744322406414
0.80    3.4159886439831877
```

TP2 kept its frozen midpoint threshold:

```text
4.640123582876524
```

## A=C eligibility

On the new 5,000-row window:

```text
A=C eligible anchors = 4990
```

This eligibility is independent of the Motor_current threshold family.

## Primary threshold-sensitivity result

Mismatch counts:

```text
alpha   A=C vs Motor_current mismatch
0.20    949
0.30    949
0.40    949
0.50    949
0.60    949
0.70    949
0.80    949
```

Summary:

```text
minimum = 949
maximum = 949
range   = 0
```

Therefore:

```text
scientific class = THRESHOLD_INVARIANT
```

Within the preregistered threshold interval, moving the Motor_current binary threshold over a large fraction of the two k-means centroids did not change a single A=C disagreement classification.

## Temporal geometry is also invariant

For every alpha, the 949 disagreements had the same nearest-transition histogram:

```text
0          =  22
1          =  23
2-5        =  92
6-10       = 115
11-25      = 345
26-50      = 352
51-100     =   0
>100       =   0
----------------
total      = 949
```

Coarse regions, identical for every alpha:

```text
NEAR          = 252
INTERMEDIATE  = 697
STABLE_FAR    =   0
```

Direction, identical for every alpha:

```text
AT_TRANSITION     =  22
AFTER_TRANSITION  = 927
BEFORE_TRANSITION =   0
EQUIDISTANT       =   0
```

Thus the strong post-transition geometry survives the entire preregistered threshold family unchanged.

## What this rules against

A specific alternative explanation before Experiment 024 was:

> The 019-023 disagreement geometry may mainly be an artifact of choosing the k-means midpoint as the Motor_current binary threshold.

Experiment 024 strongly weakens that **simple threshold-placement explanation** over the tested interval.

The midpoint was moved from:

```text
0.8821 ... 3.4160
```

without changing:

```text
mismatch count
nearest-transition histogram
coarse temporal regions
directional asymmetry
```

## What this does NOT establish

Threshold invariance over this interval does not prove:

```text
the disagreement is not a discretization artifact of any kind
Motor_current is physically delayed
DV_eletric or TP2 is ground truth
fault
anomaly
causality
physical independence
```

For example, the continuous Motor_current distribution may occupy separated regions such that all seven thresholds produce the same binary state assignments on this window.

That possibility was not directly measured in Experiment 024 and remains OPEN.

## Relation to Experiments 021 and 023

The replicated structure is now:

```text
Experiment 021:
transition-bound, strongly post-transition

Experiment 023:
same shape transfers to a separated untouched window

Experiment 024:
same type of geometry on another untouched window is invariant
to the preregistered Motor_current threshold family
```

This is stronger than the original single-window result, while still remaining a structural data finding rather than a physical causal claim.

## OPEN after Experiment 024

The next clean question is:

> Why do thresholds from 0.8821 to 3.4160 produce exactly the same Motor_current binary classifications on the tested A=C anchors?

A direct next experiment should inspect the raw Motor_current value distribution relative to the entire frozen threshold interval, especially around transition windows, without introducing a new classifier.

That would distinguish a true broad signal gap from other possible explanations.
