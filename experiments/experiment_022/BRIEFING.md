# Experiment 022 — Preregistered Signed Temporal-Offset Confirmation

> **Status:** preregistered real-data experiment.

## Starting point

Experiment 021 found that the dominant Experiment 020 disagreement subclass

```text
DV_eletric = TP2
Motor_current differs
```

was strongly post-transition asymmetric:

```text
AFTER_TRANSITION  = 1126
BEFORE_TRANSITION =   10
```

This suggested, but did not establish, a temporal-offset interpretation.

Experiment 022 tests that interpretation directly.

## Frozen paths

The path construction remains unchanged:

```text
Path A: DV_eletric
Path B: Motor_current -> first-50,000-row 1-D k-means
Path C: TP2          -> first-50,000-row independent 1-D k-means
```

The evaluation cut remains rows 50,001–55,000.

## Split before offset estimation

The 5,000 evaluation rows are split in sequence:

```text
SELECTION HALF: local rows 1..2500
CONFIRMATION HALF: local rows 2501..5000
```

The confirmation half may not participate in choosing the offset.

## Frozen offset model

Candidate signed offsets:

```text
k = -100, -99, ..., 0, ..., +99, +100
```

For a reference anchor at local sequence position `t`:

```text
reference state = Path A state at t
eligible only when Path A state at t == Path C state at t

candidate current state = Path B state at t + k
```

Sign convention:

```text
k > 0:
compare the reference at t with a LATER Motor_current state.
If such a positive k improves alignment, it is compatible with
Motor_current following the reference later in sequence.

k < 0:
compare the reference at t with an EARLIER Motor_current state.
```

Compatibility is not causality.

## Fixed anchor sets

To prevent different offsets from receiving different edge denominators, only fixed interior anchors are used.

For each 2,500-row half:

```text
margin = 100 rows on each edge
usable anchor positions = 101..2400 within that half
```

Thus every candidate offset is evaluated on exactly the same reference anchors.

Eligibility at an anchor depends only on:

```text
Path A state == Path C state
```

and therefore does not vary with k.

## Selection rule

For each k on the SELECTION HALF, count:

```text
MISMATCH(k) =
number of eligible anchors where
Path B[t+k] != Path A[t]
```

Choose the frozen offset:

```text
k* = candidate with minimum MISMATCH(k)
```

Tie break, in order:

1. smaller absolute value `abs(k)`
2. smaller numeric k

The confirmation half is not read during this choice.

## Confirmation rule

On the CONFIRMATION HALF, evaluate only:

```text
baseline k = 0
selected k = k*
```

Report:

```text
baseline mismatches
selected-offset mismatches
corrected anchors:
    baseline mismatch -> selected-offset match
introduced anchors:
    baseline match -> selected-offset mismatch
net reduction
relative reduction
```

The full confirmation curve may be reported descriptively after the frozen k* has been tested, but it cannot redefine k*.

## Continuity gate

The full 5,000-row field must reproduce Experiment 020:

```text
AB mismatch total                  = 1165
pressure supports digital subclass = 1163
pressure supports current subclass = 2
```

The frozen analog thresholds must also reproduce.

## Evaluability gate

The experiment is evaluable only if:

- exactly 5,000 assessments exist;
- both state classes occur in A, B, and C;
- Experiment 020 continuity reproduces;
- all 201 offsets are scored on one fixed eligible-anchor set in selection;
- the confirmation baseline and selected offset use one fixed eligible-anchor set;
- the selected offset is determined only from selection scores;
- no input path asserts mismatch, support, lag, anomaly, fault, causality, or truth;
- OPEN remains unchanged.

## Scientific result classes

```text
CONFIRMED_OFFSET_EFFECT
    k* != 0
    AND confirmation mismatches at k* < confirmation mismatches at k=0

NO_CONFIRMED_OFFSET_EFFECT
    otherwise
```

No minimum effect size is preregistered. Exact counts and relative reduction must be reported so a small effect cannot be rhetorically inflated.

## Claim boundary

Even a confirmed positive k* establishes only:

> A signed sequence offset selected on one half reduces A=C versus B state disagreement on an untouched second half.

It does not by itself establish:

```text
physical causality
sensor correctness
ground truth
fault
anomaly
a universal constant lag
the same offset outside this operating regime
```

Those remain OPEN.
