# Experiment 008 — Multi-Round Derived-Relation Closure

> **Status:** preregistered executable experiment.

## Purpose

Experiment 007 showed that a derived working relation can be consumed by a later consistency rule.

Experiment 008 tests a stronger form of recursion:

> **Can a relation derived in round 1 activate a second derivation rule in round 2, producing a new relation that did not become derivable from the stored field alone?**

## Chain

Round 1:

~~~text
L --P--> X
R --Q--> X
        ↓
derive:
L --LINK--> R
~~~

Round 2:

~~~text
L --LINK--> R
M --TOUCHES--> R
        ↓
derive:
L --CHAIN--> M
~~~

Final check:

~~~text
L --CHAIN--> M
        ↓
require:
L --CONFIRMED_CHAIN--> M
~~~

## Key distinction from Experiment 007

Experiment 007 was:

~~~text
stored → derived → checked
~~~

Experiment 008 is:

~~~text
stored → derived₁ → derived₂ → checked
~~~

The second derived relation must require a new evaluator round. It must not be derivable before `LINK` exists.

## Epistemic boundary

All derived relations remain working-memory relations only.

They must not:
- be written back into INPUT.json;
- become stored evidence;
- close OPEN_01.

## Expected fixture behavior

- L1 produces LINK→R1, then CHAIN→M1, and stored CONFIRMED_CHAIN→M1 matches → CONSISTENT.
- L2 produces LINK→R2, then CHAIN→M2, but stored CONFIRMED_CHAIN→M_BAD → FORMAL_MISMATCH.
- L3 produces LINK→R3, then CHAIN→M3, but CONFIRMED_CHAIN is absent → REQUIRED_RELATION_MISSING.
- OPEN_01 remains unchanged.

## Scientific requirement

The evaluator code must not contain fixture-specific branches or hard-coded sequencing for RULE_DERIVE_LINK and RULE_DERIVE_CHAIN.

The second derivation must emerge from generic fixpoint iteration over explicit rules.
