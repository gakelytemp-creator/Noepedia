# Experiment 006 — Cross-Subject Shared-Object Join

Pattern:

~~~text
A --P--> X
B --Q--> X
        ↓
A --REL--> B
~~~

Run:

~~~bash
python experiments/experiment_003/evaluator.py experiments/experiment_006/INPUT.json
~~~

Verify:

~~~bash
python experiments/experiment_006/verify_output.py
~~~

Expected:

~~~text
Experiment 006 verification: PASS
~~~
