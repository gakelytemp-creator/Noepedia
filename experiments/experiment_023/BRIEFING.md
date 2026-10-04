# Experiment 023 — Locked Transfer Replication

> **Status:** preregistered transfer experiment.

## Purpose

Experiments 019–022 were developed adaptively on one 5,000-row MetroPT-3 discovery window.

Experiment 023 therefore does not add a new interpretation. It asks whether the already observed structure transfers to a previously unused contiguous window.

## Frozen source windows

```text
Calibration rows: 1..50,000
Discovery rows:   50,001..55,000
Transfer rows:    100,001..105,000
```

The transfer window was selected before inspecting its outcomes.

## Frozen path construction

Path A:

```text
DV_eletric = 1 -> STATE_LOADED
DV_eletric = 0 -> STATE_NOT_LOADED
```

Path B:

```text
Motor_current
-> deterministic 1-D k-means fit on rows 1..50,000 only
-> frozen midpoint threshold
```

Path C:

```text
TP2
-> independent deterministic 1-D k-means fit on rows 1..50,000 only
-> frozen midpoint threshold
```

No calibration is performed on the transfer window.

## Frozen measurements transferred from 019–022

### 019-like two-path disagreement

Measure:

```text
AB FORMAL_MISMATCH
DIGITAL_CANDIDATE_STATE vs CURRENT_CANDIDATE_STATE
```

### 020-like third-path refinement

Among AB mismatches, classify only from evaluator events:

```text
A=C, B differs
B=C, A differs
```

No truth/fault interpretation is attached.

### 021-like temporal geometry

For the dominant A=C, B-different subclass, measure nearest DV_eletric transition distance using the same bins:

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

and the same direction classes:

```text
AT_TRANSITION
AFTER_TRANSITION
BEFORE_TRANSITION
EQUIDISTANT
```

### 022 historical fixed-offset transfer

Experiment 022 selected k=+35 on its selection half but failed confirmation.

Experiment 023 does **not** search for a new k.

It reports only:

```text
baseline k=0 mismatch count
historical frozen k=+35 mismatch count
corrected anchors
introduced anchors
net reduction
```

using a fixed 100-row margin and only anchors where A=C.

This is descriptive transfer of a historical candidate, not a new lag fit.

## Temporal context

To preserve the Experiment 021 transition-distance definition near the end of the transfer window, 101 future rows are read only as lookahead context.

They do not enter the 5,000 assessment field.

## Evaluability gate

The experiment is evaluable only if:

- first-50,000-row analog calibration reproduces the frozen thresholds;
- exactly 5,000 transfer assessments are built;
- A, B, and C each contain both states;
- every assessment receives exactly one AB, AC, and BC evaluator event;
- every dominant-subclass assessment has the frozen temporal descriptors;
- no new threshold or offset is fit on the transfer window;
- historical k=+35 is evaluated without re-selection;
- all OPEN records remain unchanged.

## No preregistered success fraction

No minimum similarity to the discovery window is required.

The following are all valid outcomes:

```text
TRANSFER_REPLICATES_SHAPE
TRANSFER_DIFFERS_IN_MAGNITUDE
TRANSFER_DIFFERS_IN_GEOMETRY
TRANSFER_DOES_NOT_REPLICATE
```

The run records the raw metrics first. Interpretation follows from those metrics.

## Claim boundary

Experiment 023 can establish transfer or non-transfer of measured structure.

It still cannot establish:

```text
ground truth
fault
anomaly
causality
physical independence of the three channels
a universal temporal lag
```
