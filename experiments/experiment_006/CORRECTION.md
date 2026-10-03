# Experiment 006 — Execution Correction

A post-run code audit found that the committed evaluator parsed the cross-subject rule pattern but the main `evaluate()` dispatcher still routed all arity-2 rules through the same-subject evaluator.

Therefore the earlier `RUN_RESULT.md` must **not** be treated as a verified execution of the committed evaluator.

The dispatcher has now been corrected so that:

~~~text
RULE_PATTERN = CROSS_SUBJECT_SHARED_OBJECT
~~~

is routed to the cross-subject evaluator.

This correction is preserved explicitly rather than silently rewriting the historical record.

## Revalidation requirement

Experiment 006 must be rerun from the committed repository files:

~~~bash
python experiments/experiment_006/verify_output.py
~~~

Only a passing verifier run should be cited as executable confirmation.
