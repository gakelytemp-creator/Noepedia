# Experiment 007 — Local Semantic Validation

> **Status:** local semantic validation completed.
>
> The expected event structure was independently checked in a local Python calculation using the same frozen fixture relations and the same declared rule semantics.
>
> This is **not** yet a byte-for-byte execution of the committed repository evaluator. The repository verifier remains the authoritative reproduction path.

## Observed structural counts

~~~text
DERIVED_RELATION              3
ANTECEDENT_NOT_SATISFIED     1
CONSISTENT                    1
FORMAL_MISMATCH               1
REQUIRED_RELATION_MISSING     1
~~~

Derived working relations:

~~~text
L1 --LINK--> R1
L2 --LINK--> R2
L3 --LINK--> R3
~~~

Second-stage outcomes:

~~~text
L1 → CONSISTENT
L2 → FORMAL_MISMATCH
L3 → REQUIRED_RELATION_MISSING
L4 → ANTECEDENT_NOT_SATISFIED
~~~

OPEN_01 remains unrelated to the chain and must remain unchanged.

## Reproduction command

Run the committed evaluator directly:

~~~bash
python experiments/experiment_007/verify_output.py
~~~

Expected:

~~~text
Experiment 007 verification: PASS
~~~

## Architectural result

Experiment 007 introduces a working-memory boundary:

~~~text
stored relations
→ deterministic derivation
→ temporary derived relation
→ second deterministic rule
→ structural result
~~~

The derived `LINK` relations are not persisted back into `INPUT.json`.
