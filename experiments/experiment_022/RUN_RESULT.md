# Experiment 022 — RUN RESULT

## Status

```text
reproducibility         = PASS
020 continuity          = PASS
architectural result    = PASS
scientific result       = NO_CONFIRMED_OFFSET_EFFECT
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37188219827
conclusion = success
```

## Continuity

Experiment 022 reproduced the Experiment 020 structure:

```text
AB FORMAL_MISMATCH                 = 1165
pressure supports digital subclass = 1163
pressure supports current subclass =    2
```

The frozen thresholds also reproduced:

```text
Motor_current threshold = 2.1490460087555503
TP2 threshold           = 4.640123582876524
```

## Preregistered offset protocol

Candidate signed offsets:

```text
k = -100 .. +100
```

Sign convention:

```text
k > 0
= compare the reference A=C state at t
  with a later Motor_current state at t+k
```

The 5,000-row evaluation cut was split before offset estimation:

```text
SELECTION HALF    = rows 1..2500
CONFIRMATION HALF = rows 2501..5000
```

Each half used a fixed 100-row edge margin, so every offset candidate was scored on the same anchors.

## Selection-half result

Fixed anchors:

```text
2300
```

Eligible anchors where A=C:

```text
2293
```

Baseline:

```text
k = 0
mismatches = 493
```

Selected offset:

```text
k* = +35
mismatches = 458
```

Thus the selection half showed an apparent improvement of:

```text
493 - 458 = 35 fewer mismatches
```

The minimum was broad rather than sharp:

```text
k=35  -> 458
k=36  -> 458
k=37  -> 458
k=38  -> 458
k=39  -> 458
k=40  -> 458
k=41  -> 458
k=34  -> 459
k=33  -> 460
k=32  -> 461
```

The preregistered tie-break selected k=+35.

## Untouched confirmation-half result

Eligible anchors where A=C:

```text
2288
```

Frozen baseline:

```text
k = 0
mismatches = 580
```

Frozen selected offset from the first half:

```text
k = +35
mismatches = 591
```

Paired anchor changes:

```text
corrected mismatches  = 481
introduced mismatches = 492
net reduction         = -11
relative reduction    = -1.8966%
```

Therefore the selected +35-row offset did not reproduce its selection-half improvement.

It slightly worsened the untouched confirmation half.

For descriptive context only, after the frozen confirmation test was complete, the best offset on the confirmation curve itself was:

```text
k = 0
mismatches = 580
```

That descriptive result is not used to choose a replacement offset.

## Scientific result

```text
NO_CONFIRMED_OFFSET_EFFECT
```

The preregistered condition for a confirmed effect was:

```text
k* != 0
AND
confirmation_mismatches(k*) < confirmation_mismatches(0)
```

The observed result was the opposite:

```text
591 > 580
```

## Interpretation boundary

Experiment 021 showed that the dominant disagreement is:

```text
transition-bound
and
strongly post-transition asymmetric
```

Experiment 022 now shows that this geometry is **not explained by one fixed signed row offset that generalizes from the first half to the second half of the same frozen cut**.

This rules out the simple model:

```text
Motor_current state
= reference state shifted by one constant k
```

for this split and this binary representation.

It does NOT rule out:

```text
state-dependent delay
transition-direction-dependent delay
variable delay
different dynamics for load-on and load-off transitions
hysteresis
binary-threshold distortion
multi-stage physical response
different local operating regimes
```

Nor does it establish fault, anomaly, ground truth, or causality.

## OPEN after Experiment 022

The next OPEN is narrower:

> If one constant temporal offset does not generalize, is the post-transition disagreement composed of different transition classes — for example LOAD_ON versus LOAD_OFF — with different temporal response geometries?

A suitable next experiment would therefore split transitions by direction before estimating any temporal response shape.
