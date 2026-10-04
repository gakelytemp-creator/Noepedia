# Experiment 021 — RUN RESULT

## Status

```text
reproducibility         = PASS
020 continuity          = PASS
architectural result    = PASS
```

GitHub Actions run:

```text
Noepedia Experiment Verification
run_id = 37186543445
conclusion = success
```

## Frozen continuity check

Experiment 021 exactly reproduced the Experiment 020 disagreement structure:

```text
AB FORMAL_MISMATCH                 = 1165
pressure supports digital subclass = 1163
pressure supports current subclass =    2
```

The calibrated analog thresholds also reproduced:

```text
Motor_current threshold = 2.1490460087555503
TP2 threshold           = 4.640123582876524
```

The loaded source window contained:

```text
digital transitions = 624
evaluation rows      = 5000
```

## New temporal result

The new information in Experiment 021 is the temporal geometry of the 1,163 dominant-subclass cases:

```text
DV_eletric = TP2 state
Motor_current differs
```

Nearest DV_eletric transition distance:

```text
0 rows       =  26
1 row        =  29
2–5 rows     = 114
6–10 rows    = 140
11–25 rows   = 420
26–50 rows   = 434
51–100 rows  =   0
>100 rows    =   0
-------------------
total        = 1163
```

Coarse preregistered regions:

```text
NEAR          <= 10 rows  = 309
INTERMEDIATE  11–100 rows = 854
STABLE_FAR    > 100 rows  =   0
```

Thus, in this frozen cut, every dominant-subclass disagreement lies within 50 source rows of a DV_eletric transition.

## Direction relative to nearest transition

```text
AT_TRANSITION       =   26
AFTER_TRANSITION    = 1126
BEFORE_TRANSITION   =   10
EQUIDISTANT         =    1
-------------------------
total               = 1163
```

The asymmetry is strong: the dominant subclass is overwhelmingly observed after the nearest digital transition rather than before it.

For completeness, the separate bounded-distance histograms were:

### Rows since previous digital transition

```text
0          =  26
1          =  28
2–5        = 112
6–10       = 140
11–25      = 420
26–50      = 434
51–100     =   0
>100       =   3
```

### Rows until next digital transition

```text
0          =    0
1          =    1
2–5        =    2
6–10       =    0
11–25      =    0
26–50      =   24
51–100     =   94
>100       = 1042
```

## What the result establishes

The result supports the architectural claim that a core-derived disagreement subclass can be joined with an independently constructed explicit temporal relation and can acquire a reproducible temporal geometry without the input paths asserting that geometry.

The empirical shape on this cut is sharper than the preregistration required:

```text
dominant disagreement
-> not observed in stable-far regions
-> concentrated within 50 rows of digital transitions
-> overwhelmingly on the post-transition side
```

## What the result does NOT establish

The following remain unsupported by Experiment 021 alone:

```text
Motor_current is lagging
DV_eletric is ground truth
TP2 is ground truth
Motor_current is faulty
the disagreement is normal
the disagreement is anomalous
DV_eletric causes the current response
TP2 causes the current response
```

In particular:

```text
post-transition temporal asymmetry
!= proven physical lag
```

A lag interpretation would require a separate preregistered experiment using an explicit signed temporal-offset model and testing whether shifting one path reduces the disagreement in a reproducible way.

## OPEN after Experiment 021

The OPEN is now narrower:

> Does the strong post-transition concentration represent a reproducible temporal offset between Motor_current and the DV_eletric/TP2 state pair, and does an explicitly estimated offset collapse the 1,163 disagreements?

That question is suitable for Experiment 022.
