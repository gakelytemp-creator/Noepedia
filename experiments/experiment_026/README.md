# Experiment 026 — Event-Aligned Raw Motor-current Trajectories

Experiment 026 aligns raw Motor_current around DV_eletric transitions on a new untouched window.

```text
Calibration: rows 1..50,000
Event window: rows 250,001..255,000
Signed offsets: -100..+100 rows
Transition classes:
  0 -> 1
  1 -> 0
```

No Motor_current binarization is used to construct the trajectories.

For every signed offset and transition class, the experiment reports:

```text
count, mean, median, p05, p25, p75, p95
```

The frozen Experiment 025 band edges are included only as reference lines.
