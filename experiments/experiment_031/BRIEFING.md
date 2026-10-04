# Experiment 031 — Preregistered Timestamp Cadence Audit

> **Status:** preregistered before inspecting the cadence-check window.

## Purpose

Experiments 027 and 030 independently replicated a LOAD_OFF response centered at:

```text
42 source rows
```

Experiment 031 asks:

1. What physical time interval does one source-row step represent?
2. Is timestamp spacing stable within and across the relevant windows?
3. What physical duration corresponds to the replicated 42-row response?

## Windows

Cadence is summarized separately for:

```text
W027 = rows 250,001..255,000
W030 = rows 350,001..355,000
W031 = rows 400,001..405,000   # new untouched cadence-check window
```

## Timestamp parsing

Use the dataset `timestamp` field directly.

For each adjacent row pair, compute:

```text
dt_seconds = timestamp[i+1] - timestamp[i]
```

No interpolation is used.

## Frozen summaries per window

Report:

```text
adjacent interval count
minimum dt
maximum dt
mean dt
median dt
p05
p25
p75
p95
unique dt values with counts
nonpositive dt count
gaps larger than 2 * median dt
```

## Cadence stability class

For each window:

```text
UNIFORM_CADENCE
    all positive dt values are identical

NEAR_UNIFORM_CADENCE
    max(dt)-min(dt) <= 1% of median(dt)

VARIABLE_CADENCE
    otherwise
```

Cross-window cadence class:

```text
CROSS_WINDOW_CADENCE_MATCH
    all three window medians are equal

CROSS_WINDOW_CADENCE_DIFFERS
    otherwise
```

## Physical-time conversion

Using the median cadence from W027 and W030 separately, report:

```text
42 rows * median_dt
41 rows * median_dt
52 rows * median_dt
99 rows * median_dt
```

These correspond to the replicated LOAD_OFF center and observed bounds/tails in Experiments 027/030.

## Claim boundary

This experiment establishes only timestamp cadence and row-to-time conversion.

It does not establish:

```text
causal mechanism
physical necessity
sensor truth
fault
anomaly
universal compressor dynamics
```
