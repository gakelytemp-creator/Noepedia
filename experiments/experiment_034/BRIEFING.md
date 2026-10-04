# Experiment 034 — Preregistered Residual Mismatch Autopsy

> Status: descriptive follow-up to Experiment 033.

## Purpose

Experiment 033 reduced common-subset formal mismatches from 1380 to 6.

Experiment 034 asks:

> Are those six residual mismatches instances of one repeated residual pattern, or several different patterns?

## Frozen source window

Use exactly the Experiment 033 untouched window:

```text
rows 450,001..455,000
```

The Experiment 033 revised rule is reused unchanged.

## Residual definition

A residual is an assessment for which:

```text
REVISED_EXPECTED_CURRENT_STATE
vs
CURRENT_CANDIDATE_STATE
```

produces FORMAL_MISMATCH under the frozen Experiment 003 evaluator.

TRANSITION_OPEN rows are not residual mismatches.

MID raw-current rows remain unresolved and are not forced into a class.

## Per-residual descriptors

For each residual, record:

```text
assessment id
source data row
timestamp
DV_eletric
Motor_current raw value
current raw-state class
revised expected state
rows since last LOAD_OFF
rows since last LOAD_ON
rows until next DV transition
TP2
TP3
```

Also record local context from offsets:

```text
-5..+5
```

containing:

```text
DV_eletric
Motor_current
TP2
TP3
```

## Frozen descriptive grouping

Residuals are grouped only by exact structural signature:

```text
expected state
observed current state
DV state
rows-since-LOAD_OFF bin:
  0-40
  41-52
  53-100
  >100_or_none
next-transition distance bin:
  0-10
  11-50
  51-100
  >100_or_none
```

No fitted clustering algorithm is used.

## Result classes

```text
SINGLE_RESIDUAL_PATTERN
    all residuals share one structural signature

MULTIPLE_RESIDUAL_PATTERNS
    two or more signatures appear

NO_RESIDUALS
    zero residual mismatches
```

## Claim boundary

Experiment 034 does not revise the rule.

It does not label residuals as faults, anomalies, or failures.

It only describes the remaining OPEN structure.
