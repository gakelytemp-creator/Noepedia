# Experiment 017 — Held-Out Replication with Null Baseline

Experiment 017 is the first one-shot held-out replication in the real-data instrumentation track.

Held-out source:

~~~text
NAB / realKnownCause / ambient_temperature_system_failure.csv
~~~

The file was selected before inspecting its values or anomaly-window entry.

## Primary question

Does the unchanged Experiment 011 detector produce precision above the exact matched-count random p99 baseline?

## Secondary question

Can the unchanged Experiment 011→012→013→014 structural pipeline reproduce a nontrivial two-cluster result on the held-out series?

## Run

~~~bash
python experiments/experiment_017/run_experiment.py
~~~

## Important distinction

~~~text
CI PASS
≠ primary scientific PASS
≠ secondary structural PASS
~~~

No parameter may be changed after the first held-out result.
