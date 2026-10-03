# Experiment 002 — Conceptual Briefing

> **Status:** FROZEN PRE-RUN BRIEFING

## Purpose

Experiment 001 exposed two structural gaps:

1. connector terminal / pin granularity was not represented;
2. no explicit consistency rule linked `EXPOSES_NET` and `CONNECTED_TO`.

Experiment 002 makes both structures explicit and asks a narrower question:

> Can a formal mismatch now be derived entirely from explicit object typing, explicit stored relations, and explicit field rules?

## Under test

- terminal-level object granularity;
- explicit relation semantics;
- SAME_NET constraint;
- task-specific cut;
- formal mismatch derivation;
- preservation of unrelated OPEN;
- separation of mismatch detection from repair selection.

## Not under test

- real electronics correctness;
- deterministic code execution;
- performance or cost advantage;
- autonomous Daimonion;
- large-scale ontology maintenance.

## Success condition

A run succeeds at this stage if it can:

1. derive the required relation from explicit rule structure;
2. compare it against the stored relation;
3. identify a formal mismatch;
4. preserve unrelated OPEN;
5. distinguish mismatch proof from repair-governance policy.

## Failure condition

The run fails if formal mismatch still depends on hidden domain knowledge, labels, or unstated semantics.
