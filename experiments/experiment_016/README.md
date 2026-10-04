# Experiment 016 — Pre-Onset Drift

Experiment 016 tests whether the long/deep COLD family begins after a stronger downward drift than the short/recovering family.

It reuses Experiments 011–014 unchanged and derives pre-onset dynamics before NAB labels are loaded.

## Run

~~~bash
python experiments/experiment_016/run_experiment.py
~~~

Pipeline:

~~~text
real sensor trace
→ Exp 011 mismatch detector
→ Exp 012 episodes
→ Exp 013 transition descriptors
→ Exp 014 clusters
→ label-blind two-hour PRE window
→ Theil–Sen normalized drift
→ pre_onset.json
→ only then load NAB labels
→ directional cluster comparison
~~~

A PASS supports a dynamical contextual distinction between the two families.

It does not identify the physical cause of that distinction.
