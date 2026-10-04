# Experiment 020 — Third Independent Relation

Experiment 020 adds a third independent MetroPT-3 path (`TP2`) to the two-path real-data core inference from Experiment 019.

~~~text
Path A: DV_eletric
Path B: Motor_current
Path C: TP2
~~~

The three paths independently map real observations to the same two state tokens.

The Noepedia core applies three explicit pairwise consistency rules.

For assessments where A and B disagree, the third path produces one of two evaluator-derived support shapes:

~~~text
pressure agrees with digital / disagrees with current
pressure agrees with current / disagrees with digital
~~~

These are structural subclasses only. They are not labeled normal, anomalous, or faulty.

## Run

~~~bash
python experiments/experiment_020/run_experiment.py
~~~