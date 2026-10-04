# Experiment 023 — Locked Transfer Replication on an Untouched MetroPT-3 Window

Experiment 023 freezes the 019–022 measurement pipeline and transfers it to a previously unused contiguous MetroPT-3 window.

Frozen windows:

```text
Calibration:       rows 1..50,000
Discovery window:  rows 50,001..55,000
Transfer window:   rows 100,001..105,000
```

No thresholds, rules, temporal bins, or offset-selection logic are re-fit on the transfer window.

The historical +35 row offset from Experiment 022 is evaluated only as a frozen historical candidate. It is not re-selected.

Run:

```bash
python experiments/experiment_023/run_experiment.py
```
