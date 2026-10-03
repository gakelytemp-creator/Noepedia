# Experiment 010 — Evidence-Driven Branch Discrimination

Experiment 010 tests whether explicit new evidence can reduce a preserved branch competition without deleting branch history or using hidden winner-selection policy.

Run:

~~~bash
python experiments/experiment_003/evaluator.py experiments/experiment_010/INPUT.json
~~~

Verify:

~~~bash
python experiments/experiment_010/verify_output.py
~~~

Expected:

~~~text
Experiment 010 verification: PASS
~~~

Key boundary:

~~~text
candidate generation
≠ evidence compatibility
≠ winner selection
~~~
