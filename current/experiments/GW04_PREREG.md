# GW04 — cold encoder + mechanical executor preregistration

**Status: SEALED EXPERIMENT DESIGN**  
**Date: 2026-10-18**

## Integrity before any run

Solver-visible world:

`current/experiments/GW04_WORLD_TEXT.md`

`sha256 = d43cc05f9fafc9098df07fc5961269a887ab579c7ab425e004388ff2693e669c`

Sealed answer book, held outside the solver-visible repository state:

`GW04_ANSWER_BOOK.md`

`sha256 = 9d0b30ad160a5e0afc44bdc53287b9e4aecb88139ea557e0c8261b8ec5d1dca2`

The answer book must remain unopened until both planned runs have produced their logs.


## Candidate-code seal before cold translation

The RUN B candidate implementation is frozen **before the cold encoder is allowed to run**.

Frozen candidate module:

`core/demon/gw04_candidate_overlay.py`

`sha256 = 0c2d031e847e3d1044c4c73ca5947411bf7d070b475e730c96e119d3d5f6a2de`

Source basis: only `current/experiments/GW02_VS_ANSWER_BOOK.md`.

The module implements exactly three candidate mechanisms:

- unsupported explicit requirement patterns may emit ASK through a caller-supplied structural support check;
- OPEN→ASK promotion is fail-closed and requires explicit machine-readable declaration that exactly one external fact resolves the OPEN;
- unresolved ASK stops are materialized as addressable OPEN records so the final OPEN registry cannot silently lose them.

No GW04 world text, cold translation or RUN A log may be used to modify this module before RUN B.

Focused GW01 training-scene regression:

`core/demon/gw04_candidate_overlay_test.py`

GW01 is used here only as already-seen training material, never as fresh evidence for generality.

If the frozen candidate interface proves insufficient for GW04, that insufficiency is an experimental result. It must not be repaired between RUN A and RUN B.

## Cold encoder identity and isolation gate

The experiment must not start until the cold encoder identity is sealed in a commit.

Required execution metadata:

```text
ENCODER_MODEL      = TO_BE_FILLED_AND_COMMITTED_BEFORE_TRANSLATION
ENCODER_SESSION_ID = TO_BE_FILLED_AND_COMMITTED_BEFORE_TRANSLATION
FORMAT_INPUT       = GW04_RULE_RECORD_FORMAT.md
GW01_EXAMPLE_GIVEN = YES | NO   (must be fixed before translation)
```

Eligibility constraints:

- the encoder must not be Claude/the author of GW04 or its answer book;
- it must not be the GPT session that authored this preregistration;
- it must be a new session that receives only the solver-visible world text and the frozen format inputs;
- it must not see the answer book, RUN A output, RUN B output, or a hand-authored GW04 translation.

Until `ENCODER_MODEL`, `ENCODER_SESSION_ID`, and `GW01_EXAMPLE_GIVEN` are committed, the cold-translation gate is **CLOSED**.

Known context-bias note:

If `rules_gw01.py` is supplied as an example, it may attract the encoder toward the six GW03 rule families. That exposure must remain visible in the audit and must not be confused with a semantic law of the world. The preferred input is the neutral `GW04_RULE_RECORD_FORMAT.md`, where RULE_TYPE is explicitly open.

## Unsupported evaluator type policy

The generic evaluator is frozen for RUN A and RUN B.

If the cold encoder emits a faithful rule record whose RULE_TYPE or structural operation has no evaluator handler:

```text
faithful record exists + evaluator cannot execute it
→ EXECUTOR_HOLE
```

If the encoder itself cannot produce a faithful structural record:

```text
world law not faithfully encoded
→ ENCODER_HOLE
```

In either case the A/B experiment continues **without extending `generic_evaluator.py` or `demon_core.py`**. Downstream consequences may therefore remain unavailable or cascade into later STOP/NEED states; those consequences stay in the log.

Any later evaluator extension is a separate **RUN C**, requires a separate preregistration, and may occur only after RUN A and RUN B logs are frozen.

## What GW04 measures

GW04 is not another GW01 rerun. It uses a fresh structure and a cold translation boundary.

The cold encoder receives only the solver-visible world text plus the rule-record format contract. It must translate natural-language laws into addressable rule records. Those records are then executed by the unchanged generic evaluator and unchanged mechanical demon.

The new law families intentionally include structures not directly covered by the earlier GW03 six-type set:

- exact cardinality: exactly two distinct Q1 targets;
- numeric balance/aggregation with derivation allowed only at Freedom = 1;
- explicit positive closure at one node while the universe remains open elsewhere;
- conditional value restriction.

Failure to encode one of these law types is classified as **ENCODER_HOLE**, not silently repaired by the executor.

## Candidate mechanisms under test

Three candidates from the GW02 post-unseal audit are tested on this fresh unseen world:

1. requirement concept → outward ASK when an unsupported requirement pattern is externally queryable;
2. resolvable OPEN → ASK when one external fact can resolve it;
3. every unresolved OPEN must remain present in the final OPEN registry.

A negative control is included: at least one unresolved case must remain NEED and must **not** be over-promoted to ASK.

The world also contains:

- a genuine conflict between supported bases, where the demon must not choose a side;
- an open-universe balance mismatch, which must not become CONFLICT and must not trigger invention of a new object.

## Two-run attribution design

GW04 is executed twice on the same sealed world and the same cold translation.

### RUN A — baseline

Use the current mechanical demon **without** the three new GW02 candidate mechanisms.

Purpose: measure the natural failure surface before the candidates are introduced.

### RUN B — candidate overlay

Use the same translated rule records, the same generic evaluator and the same underlying demon, but enable only the three candidate mechanisms listed above.

Purpose: attribute any change in behavior specifically to those candidates.

No other ontology, heuristic, rule family or repair may be introduced between RUN A and RUN B.

## Frozen comparison

The two logs must be retained separately.

Only after both are complete may the sealed answer book be opened.

The post-unseal audit should compare:

```text
ANSWER BOOK
vs
RUN A — baseline
vs
RUN B — candidate overlay
```

Each discrepancy should be classified at minimum as one of:

```text
ENCODER_HOLE
SPEC_HOLE
EXECUTOR_ERROR
CANDIDATE_EFFECT
OVERPROMOTED_ASK
SEMANTIC_BY_NATURE
ANSWER_BOOK_ERROR
```

The answer book is allowed to be wrong. Its preregistered alternative acceptable outcomes must remain visible in the audit rather than being rewritten after unsealing.

## Experimental discipline

- The cold encoder must not see the answer book.
- The encoder must not see a hand-authored translation of GW04 before producing its own translation.
- RUN A and RUN B must use the same encoder output.
- `generic_evaluator.py` and the base `demon_core.py` must remain unchanged across the pair.
- The only A/B difference is whether the three candidate mechanisms are active.
- No GW01-specific patch may be introduced.
- The solver may not infer meaning from N/K/Q/Z names.
- No object, predicate or law may be invented to make the world balance.

## Why this experiment matters

GW02 separated the mechanical demon from the LLM hologram.

GW03 moved executable rules into data.

GW04 now measures the next boundary:

> **Can a cold translator turn a new natural-language world into executable structural records without smuggling in the answer — and can the same content-blind executor then expose exactly where the remaining intelligence boundary lies?**

The important result is not a perfect score. The important result is a labeled boundary between what the text format can express, what the generic evaluator can execute, what the demon can decide, what requires outward contact, and what still requires semantic interpretation.
