# Experiment 005 — Two-Input Rule Antecedent

Experiment 005 extends the deterministic rule grammar from one input relation to a two-relation antecedent.

## Run

~~~bash
python experiments/experiment_003/evaluator.py experiments/experiment_005/INPUT.json
~~~

## Verify

~~~bash
python experiments/experiment_005/verify_output.py
~~~

Expected:

~~~text
Experiment 005 verification: PASS
~~~

## New grammar

~~~text
RULE_ARITY = 2
INPUT_PREDICATE_1
INPUT_PREDICATE_2
INPUT_JOIN_CONSTRAINT = SAME_OBJECT
REQUIRED_PREDICATE
REQUIRED_TARGET_SOURCE = INPUT_1_OBJECT
~~~
