# Experiment 029 — Preregistered TP3 +10 Confirmation

> **Status:** confirmatory transfer experiment preregistered before inspecting rows 300,001..305,000.

## Candidate frozen from Experiment 028

```text
TP3 at t=+10 after LOAD_OFF
```

Exploratory discovery values:

```text
CORE median = 9.914
TAIL median = 9.602
Cliff's delta CORE vs TAIL = +0.90698
```

## Untouched window

```text
LOAD_OFF anchors: rows 300,001..305,000
```

## Response labels

Reuse Experiment 027 exactly:

```text
LOAD_OFF = DV_eletric 1 -> 0

response_rows =
first k in 0..100 where three consecutive Motor_current values
are all below 0.8821033735279131

CORE = response_rows <= 50
TAIL = response_rows > 50
```

Events unresolved by +100 are reported separately and excluded from CORE/TAIL comparison.

## Frozen candidate measurement

For each resolved LOAD_OFF event:

```text
candidate_value = TP3[t+10]
```

No other channel or offset participates in the confirmatory result.

## Preregistered result classes

If TAIL contains fewer than 3 resolved events:

```text
NOT_EVALUABLE_FOR_CLASS_CONFIRMATION
```

Otherwise:

```text
DIRECTION_REPLICATED
    CORE median > TAIL median
    AND Cliff's delta > 0

STRONG_EFFECT_REPLICATED
    DIRECTION_REPLICATED
    AND Cliff's delta >= 0.50

NOT_REPLICATED
    otherwise
```

Exact medians, counts, and Cliff's delta are reported regardless of class.

## Claim boundary

Even a strong replication means only that TP3 at +10 is associated with the LOAD_OFF response-time class on a new window.

It does not establish:

```text
causality
mechanism
ground truth
fault
anomaly
universal compressor dynamics
```
