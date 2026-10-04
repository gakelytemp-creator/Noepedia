# Experiment 031 — Timestamp Cadence and Physical-Time Conversion

Experiment 031 converts the replicated row-based LOAD_OFF response into physical time using the MetroPT-3 timestamp field.

Untouched cadence-check window:

```text
rows 400,001..405,000
```

It also reads the previously used response windows only for timestamp-spacing comparison:

```text
Experiment 027 window: 250,001..255,000
Experiment 030 window: 350,001..355,000
```

No signal classifier, response threshold, or predictor is changed.
