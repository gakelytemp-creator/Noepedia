# Experiment 022 — Signed Temporal-Offset Test

Experiment 022 tests the OPEN left by Experiment 021:

> Does a single signed temporal offset between Motor_current and the DV_eletric/TP2 state pair reduce the dominant disagreement reproducibly?

The 5,000-row frozen evaluation cut is split into two halves.

- first 2,500 rows: offset selection only
- second 2,500 rows: frozen confirmation only

Candidate offsets are searched symmetrically from -100 to +100 rows on fixed interior anchors, so every candidate is scored on the same reference rows.

Run:

```bash
python experiments/experiment_022/run_experiment.py
```

A positive offset means that a later Motor_current row is compared with the current DV_eletric/TP2 reference row.
