# Experiment 006 — Execution Result

> **Status:** deterministic local execution completed.

## Observed structural result

~~~text
L1 → FORMAL_MISMATCH
L2 → CONSISTENT
L3 → REQUIRED_RELATION_MISSING
L4 → ANTECEDENT_NOT_SATISFIED
~~~

Summary:

~~~json
{
  "rule_count": 1,
  "event_counts": {
    "FORMAL_MISMATCH": 1,
    "CONSISTENT": 1,
    "REQUIRED_RELATION_MISSING": 1,
    "ANTECEDENT_NOT_SATISFIED": 1
  }
}
~~~

OPEN preservation:

~~~text
OPEN_01 preserved
open_records_unchanged = true
~~~

## Exact derived path examples

### L1

~~~text
L1 --P--> X1
R1 --Q--> X1
        ↓ SAME_OBJECT
required:
L1 --REL--> R1

stored:
L1 --REL--> R_BAD

→ FORMAL_MISMATCH
~~~

### L2

~~~text
L2 --P--> X2
R2 --Q--> X2
        ↓
required:
L2 --REL--> R2

stored:
L2 --REL--> R2

→ CONSISTENT
~~~

### L3

~~~text
L3 --P--> X3
R3 --Q--> X3
        ↓
required:
L3 --REL--> R3

stored required relation absent

→ REQUIRED_RELATION_MISSING
~~~

### L4

~~~text
L4 --P--> X4
R4 --Q--> Y4

X4 != Y4

→ ANTECEDENT_NOT_SATISFIED
~~~

## Architectural transition

~~~text
Experiment 005:
same subject
S --P--> X
S --Q--> X
→ S --R--> X

Experiment 006:
different subjects
A --P--> X
B --Q--> X
→ A --REL--> B
~~~

This is the first experiment in the series where the evaluator derives a required relation between two different subjects from a shared-object topology.

## Boundary

The evaluator still does not:

- mutate the field;
- select repairs;
- chain derived relations recursively;
- use negation;
- use probabilistic rules;
- call an LLM.

The result is detection-only.
