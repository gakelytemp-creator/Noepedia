# Experiment 006 — Cross-Subject Shared-Object Join

> **Status:** executable rule-grammar extension.

## Purpose

Experiment 005 required two relations from the same subject. Experiment 006 tests a genuine relational path across different subjects:

~~~text
A --P--> X
B --Q--> X
        ↓
derive
A --R--> B
~~~

## Explicit rule grammar

~~~text
RULE_ARITY = 2
RULE_PATTERN = CROSS_SUBJECT_SHARED_OBJECT
INPUT_SUBJECT_TYPE_1 = left_node
INPUT_PREDICATE_1 = P
INPUT_SUBJECT_TYPE_2 = right_node
INPUT_PREDICATE_2 = Q
INPUT_JOIN_CONSTRAINT = SAME_OBJECT
REQUIRED_SUBJECT_SOURCE = INPUT_1_SUBJECT
REQUIRED_PREDICATE = REL
REQUIRED_TARGET_SOURCE = INPUT_2_SUBJECT
~~~

## Expected fixture behavior

- L1 and R1 share X1; stored L1 --REL--> R_BAD → FORMAL_MISMATCH
- L2 and R2 share X2; stored L2 --REL--> R2 → CONSISTENT
- L3 and R3 share X3; required relation absent → REQUIRED_RELATION_MISSING
- L4 points to X4 while no right-side Q relation points to X4 → ANTECEDENT_NOT_SATISFIED

OPEN_01 must remain unchanged.

## Scientific requirement

No special-case identifier or domain meaning may be used by the evaluator.
