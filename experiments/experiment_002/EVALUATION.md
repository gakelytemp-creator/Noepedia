# Experiment 002 — Evaluation

## Headline result

Experiment 002 repaired the two structural gaps found in Experiment 001:

1. terminal/pin granularity is explicit;
2. the `EXPOSES_NET` → `CONNECTED_TO` SAME_NET consistency rule is explicit.

The returned run therefore moved from **mismatch candidate** to **formal mismatch**.

## Formal derivation

```text
J2_P1 : terminal
+
R18: J2_P1 → EXPOSES_NET → VOUT
+
RR01–RR04
↓
required:
J2_P1 → CONNECTED_TO → VOUT

stored:
R13: J2_P1 → CONNECTED_TO → VIN
↓
formal mismatch
```

## Criterion check

- Smallest task-specific cut: PASS
- Explicit rule path: PASS
- Formal mismatch: PASS
- OPEN_01 preservation: PASS
- Provenance preservation: PASS
- Stored facts vs inference separation: PASS
- Hidden domain knowledge avoided: PASS
- Repair-selection uncertainty exposed: PASS

## Main architectural distinction exposed

```text
mismatch detection
≠
repair selection
```

The mismatch is formally established.

The choice to revise R13 specifically remains conditional because the field lacks revision-precedence policy.

## Scientific status

This is still an LLM-mediated synthetic dry-run.

It does not yet demonstrate deterministic field execution.

## Next required experiment

Implement the smallest deterministic JSON evaluator that can:

1. read object type;
2. read rule scope;
3. match input predicate;
4. derive required predicate;
5. enforce SAME_NET;
6. compare against stored relation;
7. emit mismatch;
8. leave unrelated OPEN untouched.

Only after that evaluator produces the mismatch should an LLM be asked to interpret or propose repair.
