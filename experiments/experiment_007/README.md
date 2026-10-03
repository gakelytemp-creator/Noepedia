# Experiment 007 — Recursive Chaining

Experiment 007 tests whether one rule's derived working relation can become the input to a second rule in the same deterministic evaluation.

## Chain

~~~text
L --P--> X
R --Q--> X
        ↓
derived working relation:
L --LINK--> R
        ↓
second rule:
L --CONFIRMED_LINK--> R
~~~

## Run

~~~bash
python experiments/experiment_003/evaluator.py experiments/experiment_007/INPUT.json
~~~

## Verify

~~~bash
python experiments/experiment_007/verify_output.py
~~~

Expected:

~~~text
Experiment 007 verification: PASS
~~~

Derived relations are not persisted back into INPUT.json.
