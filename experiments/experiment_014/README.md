# Experiment 014 — Structural Clustering of COLD Episodes

Experiment 014 tests whether COLD episodes separate into two nontrivial structural families using a deterministic, label-blind clustering procedure.

It reuses Experiments 011–013 unchanged.

## Run

~~~bash
python experiments/experiment_014/run_experiment.py
~~~

Pipeline:

~~~text
real sensor trace
→ Exp 011 detector
→ Exp 012 episode decomposition
→ Exp 013 transition descriptors
→ label-blind feature normalization
→ deterministic k=2 clustering
→ clusters.json
→ only then load NAB labels
→ structural evaluation
~~~

A PASS means the frozen five-feature representation supports two measurably separated families among outside-only COLD episodes.

It does not assign causal or fault meaning to those families.
