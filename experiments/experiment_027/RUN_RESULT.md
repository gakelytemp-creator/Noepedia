# Experiment 027 — RUN RESULT

## Status

```text
reproducibility = PASS
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37192202202
conclusion = success
```

Experiment 027 was preregistered together with Experiment 026, before Experiment 026 results were inspected.

## Frozen response rule

Motor_current target regimes:

```text
LOAD_ON:
Motor_current > 3.4159886439831877

LOAD_OFF:
Motor_current < 0.8821033735279131
```

Response time:

```text
first k in 0..100
for which 3 consecutive rows are in target regime
```

## LOAD_ON — 0 -> 1

```text
events          = 47
resolved        = 47
censored        = 0

already target at t-1 = 6
already target at t=0 = 47
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
0        = 47
1        = 0
2-5      = 0
6-10     = 0
11-25    = 0
26-50    = 0
51-100   = 0
>100     = 0
```

Every LOAD_ON event satisfies the frozen stable-high response rule at t=0.

## LOAD_OFF — 1 -> 0

```text
events          = 48
resolved        = 48
censored        = 0

already target at t-1 = 0
already target at t=0 = 0
```

Response-time distribution:

```text
min    = 41
mean   = 46.9375
median = 42
p25    = 42
p75    = 42
p90    = 51.3
p95    = 91.85
max    = 99
```

Histogram:

```text
0        = 0
1        = 0
2-5      = 0
6-10     = 0
11-25    = 0
26-50    = 43
51-100   = 5
>100     = 0
```

Thus 43 of 48 LOAD_OFF transitions enter the stable low regime in the 26-50-row bin, while 5 require 51-100 rows.

## Combined interpretation

The fixed-lag model rejected in Experiment 022 is now replaced by a much more specific observed geometry:

```text
LOAD_ON response:
essentially immediate under the frozen raw-regime rule

LOAD_OFF response:
strongly delayed
median 42 rows
with a right tail reaching 99 rows
```

This is not a single lag with noise.

It is a strong transition-direction asymmetry.

The distribution also explains the earlier post-transition mismatch geometry:

```text
after a LOAD_OFF DV transition,
Motor_current remains in the high raw regime
for roughly tens of rows,
so a binary comparison with the already-switched DV state
naturally produces post-transition disagreement.
```

This is a structural explanation consistent with Experiments 021-026.

## What changed epistemically

Before 026-027, plausible models included:

```text
arbitrary midpoint artifact
one constant lag
variable but symmetric lag
direction-dependent transition dynamics
```

The accumulated evidence now argues:

```text
arbitrary midpoint placement:
strongly weakened by 024-025

one constant lag:
rejected by 022 confirmation

direction-dependent raw transition dynamics:
strongly supported by 026-027
```

## Claim boundary

The result does not establish why the physical system behaves this way.

It does not establish:

```text
causal direction
sensor truth
fault
anomaly
universal compressor behavior
```

The response-time rule is also defined relative to the frozen raw gap boundaries from 025.

## OPEN after Experiment 027

The next clean question is no longer whether there is a temporal asymmetry.

There is.

The next question is:

> Is the approximately 42-row LOAD_OFF response a stable event class, or does it decompose according to another observable operating relation?

A suitable next experiment would inspect the 48 LOAD_OFF events themselves and test whether the 43 events near 42 rows and the 5 long-tail events differ systematically in other already-recorded channels, without fitting on the response label itself.
