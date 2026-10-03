# Experiment 008 — Multi-Round Derived-Relation Closure

Experiment 008 tests a two-stage deterministic derivation chain.

~~~text
stored
→ LINK (round 1)
→ CHAIN (round 2)
→ consistency check
~~~

Run:

~~~bash
python experiments/experiment_003/evaluator.py experiments/experiment_008/INPUT.json
~~~

Verify:

~~~bash
python experiments/experiment_008/verify_output.py
~~~

Expected:

~~~text
Experiment 008 verification: PASS
~~~
