# Experiment 030 — Replication of Direction-Dependent Raw Response Times

Experiment 030 transfers the Experiment 027 response-time rule unchanged to a new untouched window.

```text
Confirmation window: rows 350,001..355,000
```

Frozen response rule:

```text
LOAD_ON:
first k in 0..100 with 3 consecutive Motor_current values > 3.4159886439831877

LOAD_OFF:
first k in 0..100 with 3 consecutive Motor_current values < 0.8821033735279131
```

No new channel, threshold, offset, or predictor is fit.
