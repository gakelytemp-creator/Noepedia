# Experiment 009 — Branching, Competition, and Non-Closure

> **Status:** preregistered executable experiment.

## Purpose

Experiment 008 showed multi-round deterministic closure. Experiment 009 tests what happens when two independently justified derivation paths produce competing targets for the same subject and predicate.

The system must preserve both branches and expose the competition without silently choosing a winner.

## Core pattern

Two independent derivation rules can produce:

```text
L --CANDIDATE--> A
L --CANDIDATE--> B
```

A separate explicit cardinality rule states:

```text
scope = left_node
predicate = CANDIDATE
max distinct targets = 1
```

If two distinct candidate targets are present, the evaluator must emit `COMPETING_DERIVATIONS` but must not delete, rank, merge, or select either candidate.

## Expected fixture behavior

- L1 has two independently derived candidates, A1 and B1 → COMPETING_DERIVATIONS.
- L2 has only one derived candidate, A2 → UNIQUE_CANDIDATE.
- Both L1 candidate branches remain present in `derived_relations`.
- No repair or closure event is permitted.
- OPEN_01 remains unchanged.

## Scientific requirement

The evaluator must contain no fixture-specific logic for L1/L2, A1/B1/A2, or the predicate CANDIDATE.
Competition must arise only from explicit derived relations plus an explicit cardinality rule.