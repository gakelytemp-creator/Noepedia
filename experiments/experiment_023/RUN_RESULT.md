# Experiment 023 — RUN RESULT

## Status

```text
reproducibility      = PASS
architectural result = PASS
transfer result      = STRONG DESCRIPTIVE SHAPE REPLICATION
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37189043420
conclusion = success
```

The transfer window was frozen before its outcomes were inspected:

```text
calibration       = rows 1..50,000
discovery window  = rows 50,001..55,000
transfer window   = rows 100,001..105,000
```

No threshold, rule, temporal bin, or offset was re-fit on the transfer window.

## Frozen thresholds

The first-50,000-row calibration reproduced exactly:

```text
Motor_current threshold = 2.1490460087555503
TP2 threshold           = 4.640123582876524
```

## 019-like two-path disagreement transfer

Discovery window:

```text
AB mismatch = 1165 / 5000
            = 23.30%
```

Untouched transfer window:

```text
AB mismatch = 1158 / 5000
            = 23.16%
```

Difference:

```text
-7 cases
-0.14 percentage points
```

The overall two-path disagreement magnitude therefore transferred closely.

## 020-like third-path refinement transfer

Discovery:

```text
A=C, B differs = 1163
B=C, A differs =    2

A=C share among AB mismatches
= 1163 / 1165
≈ 99.83%
```

Transfer:

```text
A=C, B differs = 1156
B=C, A differs =    2

A=C share among AB mismatches
= 1156 / 1158
≈ 99.83%
```

The third-path asymmetry therefore reproduced almost exactly.

As before:

```text
A=C
!= A is truth

B differs
!= B is faulty
```

## 021-like temporal geometry transfer

Dominant subclass:

```text
A=C, B differs
```

### Discovery window

```text
0           26
1           29
2-5        114
6-10       140
11-25      420
26-50      434
51-100       0
>100         0
----------------
total      1163
```

### Transfer window

```text
0           26
1           28
2-5        111
6-10       140
11-25      424
26-50      427
51-100       0
>100         0
----------------
total      1156
```

The coarse regions were:

```text
                 discovery   transfer
NEAR <=10             309        305
INTERMEDIATE          854        851
STABLE_FAR              0          0
```

Again, every dominant-subclass disagreement in the transfer window lies within 50 source rows of a DV_eletric transition.

## Directional geometry

```text
                    discovery   transfer
AT_TRANSITION              26         26
AFTER_TRANSITION         1126       1120
BEFORE_TRANSITION          10          9
EQUIDISTANT                 1          1
```

The strong post-transition asymmetry therefore transferred to the untouched window.

This is the most important result of Experiment 023.

The 021 temporal shape was not confined to the original discovery window.

## Historical +35 offset transfer

Experiment 022 selected k=+35 on one discovery half, but that offset failed on the untouched second half of the same discovery window.

For Experiment 023, k=+35 was therefore treated only as a frozen historical candidate and was not re-selected.

On fixed transfer anchors where A=C:

```text
baseline k=0 mismatches = 1147
historical k=+35        = 1115

corrected anchors       = 963
introduced anchors      = 931
net reduction           = 32
relative reduction      = +2.7899%
```

Thus +35 happens to improve the transfer window slightly.

However, because Experiment 022 confirmation gave:

```text
net reduction = -11
```

the combined evidence does not support one universal fixed offset.

The appropriate conclusion remains:

```text
constant-lag model = not established
```

## Transfer interpretation

No numerical similarity tolerance was preregistered, so this is not a threshold-based hypothesis-test PASS.

Descriptively, however, the replication is strong:

```text
AB mismatch:
1165 -> 1158

A=C/B-different subclass:
1163 -> 1156

minority opposite subclass:
2 -> 2

AFTER_TRANSITION:
1126 -> 1120

BEFORE_TRANSITION:
10 -> 9

AT_TRANSITION:
26 -> 26

STABLE_FAR:
0 -> 0
```

Accordingly, the defensible descriptive classification is:

```text
TRANSFER_REPLICATES_SHAPE
```

## What Experiment 023 changes

Before Experiment 023, a serious alternative was:

> The 019–021 structure may be peculiar to the single adaptively explored 5,000-row discovery window.

Experiment 023 substantially weakens that alternative.

The measured structure transferred to a window 45,000 rows away without re-fitting the analog thresholds or temporal definitions.

What transfers is not yet a new physical law. It may still reflect ordinary compressor transition dynamics plus the binary representation of continuous signals.

But it is now a reproducible data structure across two separated windows rather than a single-window observation.

## What remains OPEN

Experiment 023 does not distinguish between:

```text
real multi-stage transition dynamics
binary-threshold artifact
transition-direction dependence
operating-regime dependence
variable delay
hysteresis
other coupled-channel dynamics
```

The next clean experiment should therefore test a frozen family of Motor_current thresholds on an untouched window rather than continue adapting explanations on the discovery window.

That experiment can ask whether the replicated mismatch geometry moves systematically with the Motor_current binarization threshold.
