# Experiment 015 — Temporal Context of the Two COLD Families

Experiment 015 tests time-of-day as the first explicit contextual relation that might distinguish the two label-blind COLD families found in Experiment 014.

It reuses Experiments 011–014 unchanged.

## Run

~~~bash
python experiments/experiment_015/run_experiment.py
~~~

Pipeline:

~~~text
real sensor trace
→ Exp 011 mismatch detector
→ Exp 012 episodes
→ Exp 013 transition descriptors
→ Exp 014 structural clusters
→ label-blind time-of-day relation
→ temporal_context.json
→ only then load NAB labels
→ circular phase evaluation
~~~

A PASS means the long/deep family is strongly concentrated in a distinct daily phase.

It does not establish the physical cause of that phase relation.
