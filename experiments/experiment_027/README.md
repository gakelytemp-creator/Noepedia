# Experiment 027 — Per-Transition Raw Response-time Distribution

Experiment 027 is preregistered together with Experiment 026, before the 026 outcome is inspected.

It uses the same untouched event-anchor window:

```text
rows 250,001..255,000
```

but asks a different question: for each DV_eletric transition, how many rows elapse before raw Motor_current reaches and remains in the target raw regime?

Frozen response rule:

```text
LOAD_ON  (0->1):
first k in 0..100 where Motor_current[t+k:t+k+3] are all > band_high

LOAD_OFF (1->0):
first k in 0..100 where Motor_current[t+k:t+k+3] are all < band_low
```

No response threshold is fit from the event window.
