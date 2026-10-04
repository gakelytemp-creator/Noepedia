# Experiment 021 — Temporal Geometry of the 020 Disagreement

Experiment 021 extends Experiment 020 without changing its three real-data paths.

It asks whether the dominant 020 subclass

```text
DV_eletric + TP2 agree
Motor_current disagrees
```

is concentrated near transitions of the independently observed digital load-state path, or whether a substantial residue remains in temporally stable regions.

The experiment uses the same MetroPT-3 calibration rows, the same 5,000-row evaluation cut, the same two analog k-means calibrations, and the same frozen Experiment 003 evaluator.

No physical interpretation is preregistered. In particular, temporal concentration does not by itself establish lag, causality, fault, anomaly, or ground truth.

Run:

```bash
python experiments/experiment_021/run_experiment.py
```
