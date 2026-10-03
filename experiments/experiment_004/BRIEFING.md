# Experiment 004 — Multi-Rule Deterministic Field

> **Status:** executable extension of Experiment 003.

## Purpose

Experiment 003 showed that one explicit consistency rule can produce a deterministic formal mismatch without LLM interpretation.

Experiment 004 asks the next question:

> **Can the same evaluator apply several explicit rules over several object types in one field, producing multiple independent consistency results without any domain-specific branches in code?**

## What changes

The evaluator code is not given special knowledge about:
- terminals;
- capacitors;
- regulators;
- VIN;
- VOUT;
- specific relation IDs.

Instead, the field contains three rule objects:

1. terminal: `EXPOSES_NET → CONNECTED_TO` with `SAME_NET`;
2. capacitor: `STABILIZES → CONNECTED_TO` with `SAME_NET`;
3. regulator: `REGULATES → CONNECTED_TO` with `SAME_NET`.

## Expected events

The fixture is designed to produce:

- J2_P1 — formal mismatch;
- J2_P2 — consistent;
- C1 — consistent;
- C2 — formal mismatch;
- U1 — consistent;
- OPEN_01 — preserved untouched.

## Scientific requirement

If the evaluator needs a special-case branch for any of these objects or predicates, the experiment fails.

The result must arise only from the explicit rule descriptions.
