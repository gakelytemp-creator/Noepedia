# Experiment 030 — RUN RESULT

## Status

```text
reproducibility = PASS
replication     = DIRECTIONAL_ASYMMETRY_REPLICATED
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37194211386
conclusion = success
```

## Frozen untouched window

```text
rows 350,001..355,000
```

The Experiment 027 response-time rule was transferred unchanged.

## LOAD_ON — 0 -> 1

```text
event_count     = 30
resolved        = 30
censored        = 0

already target at t-1 = 5
already target at t=0 = 30
```

Response-time distribution:

```text
min    = 0
mean   = 0
median = 0
p25    = 0
p75    = 0
p90    = 0
p95    = 0
max    = 0
```

Histogram:

```text
0        = 30
1        = 0
2-5      = 0
6-10     = 0
11-25    = 0
26-50    = 0
51-100   = 0
>100     = 0
```

Thus:

```text
load_on_zero_fraction = 1.0
LOAD_ON_IMMEDIATE_REPLICATED
```

## LOAD_OFF — 1 -> 0

```text
event_count     = 30
resolved        = 30
censored        = 0

already target at t-1 = 0
already target at t=0 = 0
```

Response-time distribution:

```text
min    = 41
mean   = 42.4333
median = 42
p25    = 42
p75    = 42
p90    = 44.1
p95    = 45.55
max    = 52
```

Histogram:

```text
0        = 0
1        = 0
2-5      = 0
6-10     = 0
11-25    = 0
26-50    = 29
51-100   = 1
>100     = 0
```

Thus:

```text
load_off_26_50_fraction = 29/30
                         = 0.9667

LOAD_OFF_DELAY_REPLICATED
```

## Overall preregistered result

Both class-specific replication criteria passed:

```text
LOAD_ON_IMMEDIATE_REPLICATED
LOAD_OFF_DELAY_REPLICATED
```

Therefore:

```text
DIRECTIONAL_ASYMMETRY_REPLICATED
```

## Comparison with Experiment 027

Experiment 027:

```text
LOAD_ON:
47/47 at k=0

LOAD_OFF:
median = 42
p25    = 42
p75    = 42
43/48 in 26-50
5/48 in 51-100
```

Experiment 030:

```text
LOAD_ON:
30/30 at k=0

LOAD_OFF:
median = 42
p25    = 42
p75    = 42
29/30 in 26-50
1/30 in 51-100
```

The central LOAD_OFF timing structure reproduced strikingly closely.

## What this establishes

Under the frozen operational definition, the same directional response-time geometry appears in two separated windows:

```text
LOAD_ON:
immediate entry into high Motor_current regime

LOAD_OFF:
delayed entry into low Motor_current regime,
centered very tightly around ~42 rows
```

This is no longer a one-window exploratory pattern.

It is a replicated temporal relation in the data.

## What it does NOT establish

It still does not establish:

```text
causal mechanism
sensor truth
fault
anomaly
universal compressor law
physical necessity
```

The response-time relation is operationally defined using the frozen raw-gap boundaries from Experiments 025-027.

## OPEN after Experiment 030

The next clean step is not another broad covariate scan.

The stronger question is now:

> Is the ~42-row LOAD_OFF response tied to source sampling/time cadence and does it remain stable when expressed in physical time rather than row count?

That requires using the dataset timestamp field to convert the replicated 42-row structure into an actual time interval and checking whether timestamp spacing itself is stable across the relevant windows.
