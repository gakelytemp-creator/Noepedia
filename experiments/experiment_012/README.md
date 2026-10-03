# Experiment 012 — Structural Decomposition of Real-Data Mismatches

Experiment 012 does not retune Experiment 011.

It reuses the frozen Experiment 011 detector and asks whether its mismatch events form coherent temporal episodes before any NAB anomaly labels are introduced.

## Run

~~~bash
python experiments/experiment_012/run_experiment.py
~~~

Pipeline:

~~~text
pinned real sensor trace
→ Experiment 011 detector
→ predictions.json
→ label-blind episode decomposition
→ episodes.json
→ only then load NAB labels
→ structural evaluation
~~~

## Frozen decomposition

~~~text
same episode if consecutive mismatch gap <= 30 minutes
persistent episode if mismatch_count >= 6
~~~

## Important distinction

A structural PASS means unexplained mismatches are temporally organized.

It does not mean they are true unlabeled faults.
