# Experiment 024 — Frozen Motor-current Threshold Sensitivity on a New Untouched Window

Experiment 024 tests whether the replicated disagreement geometry depends systematically on how the continuous Motor_current channel is binarized.

Frozen windows:

```text
Calibration:       rows 1..50,000
Discovery:         rows 50,001..55,000
Transfer 023:      rows 100,001..105,000
Threshold test:    rows 150,001..155,000
```

Frozen Motor_current threshold family:

```text
threshold(alpha) = low_centroid + alpha * (high_centroid - low_centroid)

alpha = 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80
```

Path A (DV_eletric) and Path C (TP2) remain unchanged.

Run:

```bash
python experiments/experiment_024/run_experiment.py
```
