# Experiment 007 — Recursive Chaining Through Derived Working Relations

> **Status:** executable rule-grammar extension.

## Purpose

Experiment 006 derives a required relation from a cross-subject shared-object topology, but the derived result is not yet used by another rule.

Experiment 007 tests the next step:

> **Can a relation derived by one deterministic rule become the input to a second deterministic rule in the same evaluation, without being written back into the persistent field?**

## Chain

Stage 1:

~~~text
L --P--> X
R --Q--> X
        ↓
derive in working memory:
L --LINK--> R
~~~

Stage 2:

~~~text
L --LINK--> R
        ↓
require:
L --CONFIRMED_LINK--> R
~~~

The second rule therefore depends on the first rule's derived relation.

## Epistemic boundary

Derived relations are **working relations**, not stored evidence.

They must:
- carry `status = derived`;
- preserve their derivation path;
- exist only inside the current evaluation result;
- not mutate `INPUT.json`;
- not close OPENs.

## Expected fixture behavior

- L1/R1 share X1 → derive LINK → stored CONFIRMED_LINK matches → CONSISTENT
- L2/R2 share X2 → derive LINK → stored CONFIRMED_LINK points to R_BAD → FORMAL_MISMATCH
- L3/R3 share X3 → derive LINK → CONFIRMED_LINK absent → REQUIRED_RELATION_MISSING
- L4 points to X4 while right-side relation points to Y4 → no LINK derived → ANTECEDENT_NOT_SATISFIED

OPEN_01 remains unchanged.

## Scientific requirement

No special-case knowledge of L1/L2/L3/L4, LINK, CONFIRMED_LINK, or any fixture ID may exist in evaluator code.

The chain must arise from explicit rule descriptions plus temporary derived working relations.
