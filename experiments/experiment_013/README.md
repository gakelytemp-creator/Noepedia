# Experiment 013 — Baseline Transition Test

Experiment 013 asks whether the outside-only COLD episodes found in Experiment 012 look like persistent downward level changes or recovered excursions.

It does not retune Experiments 011 or 012.

## Run

~~~bash
python experiments/experiment_013/run_experiment.py
~~~

Pipeline:

~~~text
pinned real sensor trace
→ unchanged Experiment 011 detector
→ unchanged Experiment 012 episode decomposition
→ label-blind PRE/POST baseline analysis
→ transitions.json
→ only then load NAB labels
→ evaluate outside-only COLD episodes
~~~

## Frozen classification

~~~text
DOWNWARD_LEVEL_SHIFT
    post_shift_z <= -2.0

RECOVERED_COLD_EXCURSION
    episode_shift_z <= -2.0
    and abs(post_shift_z) < 1.0

OTHER_COLD
    otherwise
~~~

A PASS means persistent downward baseline relocation dominates the outside-only COLD structure. It does not mean those transitions are faults.
