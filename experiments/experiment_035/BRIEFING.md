# Experiment 035 — Preregistered Pre-LOAD_ON Replication Test

> Status: confirmatory follow-up to Experiment 034.

## Motivation

Experiment 034 found six residual mismatches, all consecutive and all sharing the same geometry:

```text
DV_eletric = 0
Motor_current = HIGH
next LOAD_ON in 1..6 rows
```

Experiment 035 tests whether that pre-transition structure repeats on untouched data.

## Untouched window

```text
LOAD_ON anchors: rows 500,001..505,000
```

Read six rows of history before the first anchor so every event can be evaluated.

## Frozen event definition

```text
LOAD_ON = DV_eletric 0 -> 1
```

## Frozen Motor_current HIGH regime

Reuse Experiments 024-025:

```text
HIGH iff Motor_current > 3.4159886439831877
```

No threshold is estimated from the Experiment 035 window.

## Primary event-level measurement

For each LOAD_ON transition at row t, inspect:

```text
t-6, t-5, t-4, t-3, t-2, t-1
```

Record the earliest pre-transition offset in -6..-1 at which Motor_current is HIGH.

If none of the six rows is HIGH:

```text
NO_PRE_HIGH
```

Also record whether Motor_current is HIGH at t=0.

## Frozen summaries

Report:

```text
LOAD_ON event count
events with any pre-HIGH in 1..6 rows
pre-HIGH event fraction

earliest-pre-HIGH histogram:
-6
-5
-4
-3
-2
-1
NO_PRE_HIGH

HIGH-at-t0 fraction
```

For events with pre-HIGH, also report the number of consecutive HIGH rows immediately before t.

## Preregistered replication classes

```text
PRE_LOAD_ON_PATTERN_REPLICATED
    at least 50% of LOAD_ON events have any HIGH row in t-6..t-1

PRE_LOAD_ON_PATTERN_WEAK
    >0% but <50%

PRE_LOAD_ON_PATTERN_NOT_REPLICATED
    0%
```

The 50% threshold is frozen before outcome inspection.

## Secondary descriptive check

For the same events, report TP2 and TP3 values at t-1 and t=0.

These channels do not affect the replication class.

## Claim boundary

A replicated pre-HIGH pattern means only that Motor_current frequently enters the HIGH raw regime before the DV_eletric LOAD_ON transition.

It does not establish:

```text
causal precedence
controller implementation
sensor delay
fault
anomaly
universal behavior
```

Experiment 035 does not modify the Experiment 033 rule.
