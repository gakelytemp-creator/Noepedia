# Experiment 005 — Execution Result

> **Status:** local deterministic execution completed after the rule-grammar extension.

## Structural result

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

Observed subject-level events:

~~~text
A → FORMAL_MISMATCH
B → CONSISTENT
C → REQUIRED_RELATION_MISSING
D → ANTECEDENT_NOT_SATISFIED
~~~

OPEN preservation:

~~~text
OPEN_01 preserved
open_records_unchanged = true
~~~

## Interpretation

Experiment 005 demonstrates a first multi-edge antecedent:

~~~text
S --P--> X
S --Q--> X
        ↓
require
S --R--> X
~~~

The requirement is generated only when both input relations exist for the same subject and satisfy the explicit `SAME_OBJECT` join constraint.

The four fixture subjects exercise four distinct states:

1. antecedent satisfied + conflicting stored requirement;
2. antecedent satisfied + matching stored requirement;
3. antecedent satisfied + required relation absent;
4. both input predicates present but join constraint not satisfied.

## Architectural transition

~~~text
Experiment 003
one rule / one input edge

Experiment 004
many rules / same one-input grammar

Experiment 005
two-edge antecedent / explicit join
~~~

The evaluator is therefore no longer limited to deriving a requirement from a single stored edge.

## Scientific boundary

This is still not a general-purpose inference language.

The new grammar currently supports exactly:

~~~text
arity = 2
same subject
two declared input predicates
SAME_OBJECT join
target copied from INPUT_1_OBJECT
one required predicate
~~~

No repair logic was added.

## Next unresolved direction

The next extension should test whether a rule can connect **different subjects through a shared object**, rather than requiring both antecedent relations to originate from the same subject.

That would move from a local star-pattern to a genuine relational path pattern.
