# Experiment 005 — Two-Input Rule Antecedent

> **Status:** executable rule-grammar extension.

## Purpose

Experiments 003–004 showed that a deterministic evaluator can apply one-input consistency rules.

Experiment 005 asks:

> **Can the rule language require two independent stored relations before a derived requirement is created?**

This is the first extension from a single-edge antecedent to a multi-edge antecedent.

## New rule form

The new rule declares:

~~~text
RULE_ARITY = 2
INPUT_PREDICATE_1 = P
INPUT_PREDICATE_2 = Q
INPUT_JOIN_CONSTRAINT = SAME_OBJECT
REQUIRED_PREDICATE = R
REQUIRED_TARGET_SOURCE = INPUT_1_OBJECT
~~~

Operational reading:

~~~text
S --P--> X
S --Q--> X
~~~

jointly trigger:

~~~text
S --R--> X
~~~

The evaluator must not derive the requirement if the two input relations do not share the same object.

## Expected fixture behavior

- A: both inputs point to X; stored required relation points to Y → FORMAL_MISMATCH
- B: both inputs point to X; stored required relation points to X → CONSISTENT
- C: both inputs point to X; required relation absent → REQUIRED_RELATION_MISSING
- D: input predicates point to different objects → ANTECEDENT_NOT_SATISFIED

OPEN_01 must remain unchanged.

## Scientific requirement

The evaluator must contain no special branches for A/B/C/D, P/Q/R, X/Y, or fixture IDs.

The result must arise only from the explicit rule grammar.
