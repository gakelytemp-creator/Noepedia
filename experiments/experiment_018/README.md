# Experiment 018 — Real Observations in the Noepedia Core

Experiment 018 reconnects the real-data instrumentation track to the Noepedia relational evaluator.

It is an architecture-integration test, not an anomaly-detector validation experiment.

## Run

~~~bash
python experiments/experiment_018/run_experiment.py
~~~

Pipeline:

~~~text
pinned real NAB readings
→ unchanged Experiment 011 detector as instrumentation adapter
→ explicit relational field
→ real measurements + provenance + expectations + OPEN causes
→ unchanged Experiment 003 evaluator
→ 20 CONSISTENT + 20 FORMAL_MISMATCH
→ OPEN causes preserved
~~~

The evaluator itself receives no temperature threshold logic and no NAB anomaly labels.
