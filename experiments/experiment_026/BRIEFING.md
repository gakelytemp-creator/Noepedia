# Experiment 026 — Preregistered Event-Aligned Raw Trajectory Test

> **Status:** preregistered before inspecting rows 250,001..255,000.

## Question

What does raw Motor_current do around DV_eletric transitions when no Motor_current threshold is used to construct the response?

## Frozen event window

```text
DV transition anchors: data rows 250,001..255,000
trajectory offsets:    -100..+100 source rows
```

The source reader loads 100 rows before and after the anchor window so each accepted transition can have a complete trajectory.

## Transition definition

A transition at anchor t occurs when:

```text
DV_eletric[t] != DV_eletric[t-1]
```

Classes:

```text
LOAD_ON  = 0 -> 1
LOAD_OFF = 1 -> 0
```

## Raw trajectory

For every transition and signed offset k in:

```text
-100 .. +100
```

record:

```text
Motor_current[t+k]
TP2[t+k]
```

Motor_current remains raw.

TP2 is included descriptively so its event-aligned geometry can be inspected without declaring it truth or an independent physical witness.

## Frozen summaries

For each transition class and each signed offset, report separately for Motor_current and TP2:

```text
count
mean
median
p05
p25
p75
p95
```

Also report event counts and selected landmark offsets:

```text
-100, -50, -25, -10, -5, -1, 0, +1, +5, +10, +25, +50, +100
```

## Reference band

The Experiment 025 Motor_current band is reproduced only as a reference:

```text
band_low  = 0.8821033735279131
band_high = 3.4159886439831877
```

It does not define which transitions enter the experiment and does not alter raw trajectory values.

## Evaluability

Evaluable only if:

- first-50,000-row calibration reproduces;
- Experiment 025 band edges reproduce;
- transition anchors are selected only from DV_eletric;
- every accepted event has complete -100..+100 context;
- raw Motor_current is not thresholded before aggregation;
- LOAD_ON and LOAD_OFF are summarized independently.

## Claim boundary

The experiment describes event-aligned dynamics.

It does not establish:

```text
causality
ground truth
fault
anomaly
universal response law
physical independence of channels
```
