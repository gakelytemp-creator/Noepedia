# Experiment 004 — Multi-Rule Local Execution Result

> **Status:** local execution completed against a fixture equivalent to the rule-relevant subset of `INPUT.json`.
>
> The committed evaluator itself remains domain-agnostic: it contains no branches for terminals, capacitors, regulators, VIN, VOUT, or any concrete relation ID.

## Expected field behavior

Three independent rule objects were active:

1. `RULE_TERMINAL_EXPOSE_CONNECT`
2. `RULE_CAPACITOR_STABILIZE_CONNECT`
3. `RULE_REGULATOR_OUTPUT_CONNECT`

All use the same generic evaluator mechanism:

~~~text
RULE_SCOPE
+ INPUT_PREDICATE
+ REQUIRED_PREDICATE
+ SAME_NET
→ derived requirement
→ stored-relation comparison
~~~

## Observed summary

~~~json
{
  "rule_count": 3,
  "event_counts": {
    "FORMAL_MISMATCH": 2,
    "CONSISTENT": 3
  }
}
~~~

## Observed events

~~~text
FORMAL_MISMATCH
  rule: RULE_TERMINAL_EXPOSE_CONNECT
  subject: J2_P1

CONSISTENT
  rule: RULE_TERMINAL_EXPOSE_CONNECT
  subject: J2_P2

CONSISTENT
  rule: RULE_CAPACITOR_STABILIZE_CONNECT
  subject: C1

FORMAL_MISMATCH
  rule: RULE_CAPACITOR_STABILIZE_CONNECT
  subject: C2

CONSISTENT
  rule: RULE_REGULATOR_OUTPUT_CONNECT
  subject: U1
~~~

## OPEN preservation

~~~text
OPEN_01 preserved
open_records_unchanged = true
~~~

## Interpretation

The same evaluator applied three separately declared rule objects across three different object types.

No new detection branch was added for:

- terminal;
- capacitor;
- regulator;
- EXPOSES_NET;
- STABILIZES;
- REGULATES.

Those distinctions live in the field data.

This is important because the evaluator is beginning to behave as a small **rule interpreter** rather than a one-off checker.

## Scientific limit

This does not yet mean that the evaluator supports arbitrary rules.

Its current rule language is still narrow:

~~~text
one scope type
+ one input predicate
+ one required predicate
+ SAME_NET target constraint
~~~

So Experiment 004 demonstrates **rule multiplicity within one rule form**, not a general inference language.

## Next OPEN

The next useful question is:

> Can the rule language itself become more expressive without moving semantics back into hard-coded Python?

Candidate next extensions should be introduced one at a time, for example:

- different target constraint;
- relation absence as a condition;
- two-input rule;
- relation-to-relation constraint.

Do not add repair selection yet.
