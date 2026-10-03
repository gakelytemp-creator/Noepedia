# Experiment 003 — Deterministic Evaluator

This directory contains the first executable deterministic layer in the Noepedia experiment series.

## Files

- `BRIEFING.md` — frozen conceptual briefing
- `SPEC.md` — accepted design specification
- `evaluator.py` — deterministic detection-only evaluator
- `test_evaluator.py` — four acceptance tests

## Run

From the repository root:

~~~bash
python experiments/experiment_003/evaluator.py experiments/experiment_002/INPUT.json
~~~

## Tests

~~~bash
python -m unittest experiments/experiment_003/test_evaluator.py
~~~

## Boundary

The evaluator performs **detection only**.

It does not:
- call an LLM;
- use electronics knowledge;
- inspect human-readable labels;
- choose a repair;
- alter OPEN records.

The formal result must arise from:

~~~text
object type
+ explicit relation
+ explicit rule
+ explicit constraint
~~~
