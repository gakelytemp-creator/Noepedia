# Experiment 034 — Residual Mismatch Autopsy

Experiment 034 examines only the residual mismatches left by Experiment 033.

No new rule is introduced.

For each residual mismatch, record:

- source row and timestamp
- revised expected current state
- observed raw Motor_current and raw-state class
- DV_eletric
- rows since most recent LOAD_OFF
- rows since most recent LOAD_ON
- rows until next DV transition
- TP2 and TP3
- local ±5-row context

The goal is description and clustering, not repair.
