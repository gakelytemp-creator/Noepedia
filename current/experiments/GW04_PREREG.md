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

`sha256 = 5a45c68c5747a257209b964acb902f2b15147b902d1cf00bd1f7387bca503037`

**Seal correction note (pre-run):** the previously recorded value `0c2d031e…` did not match the repository file at commit `f5f2d67`. The repository bytes hash to `15cd6afd16d557a8324e40397c6fb436a5b274c3f84a20f6bc790b21ed8dd893`. No cold translation or GW04 run occurred before this correction. This commit records the discrepancy rather than hiding it. The candidate code will be resealed again if it changes before the cold-translation gate opens.

**C2 structural reseal (pre-translation):** the first overlay expected `RESOLUTION_*` fields but no runtime producer existed. Before any cold translation or GW04 run, option **(b)** was adopted: a generic evaluator-side producer now records a machine-readable MISSING fact-pattern on an unresolved task query; the RUN B overlay may convert only a one-fact pattern (all positions present, at most one `?` variable) into an addressable resolvable OPEN and then ASK. Missing rules, closure, cardinality policies, or other prose/string deficits remain NEED. No natural-language parsing is used.

Frozen files for this A/B boundary:

`core/demon/gw04_candidate_overlay.py`  
`sha256 = 5a45c68c5747a257209b964acb902f2b15147b902d1cf00bd1f7387bca503037`

`core/demon/gw03/generic_evaluator.py`  
`sha256 = 0f6a3cf0520b1887bca7ebdfafb9e2f200297393e46af8357ea5d587b317b595`

`core/demon/gw04_candidate_overlay_test.py`  
`sha256 = 7285621eea8172459a06a038bae6376667983040a901bf3aaaf5a86e62d6e123`

The generic evaluator file is identical in RUN A and RUN B; its candidate hook is inert when `candidate_overlay=None`. RUN B supplies the frozen overlay. The base `demon_core.py` is unchanged.

Source basis: only `current/experiments/GW02_VS_ANSWER_BOOK.md`.

The frozen RUN B path implements exactly three candidate mechanisms:

- unsupported explicit requirement patterns may emit ASK through the evaluator's structural support check;
- a NEED STOP whose MISSING field is one machine-readable fact-pattern is materialized as a resolvable OPEN; only then may OPEN→ASK promotion occur;
- unresolved ASK stops are materialized as addressable OPEN records so the final OPEN registry cannot silently lose them.

No GW04 world text, cold translation or RUN A log may be used to modify this module before RUN B.

Focused GW01 training-scene regression:

`core/demon/gw04_candidate_overlay_test.py`

GW01 is used here only as already-seen training material, never as fresh evidence for generality.

If the frozen candidate interface proves insufficient for GW04, that insufficiency is an experimental result. It must not be repaired between RUN A and RUN B.

## Cold encoder prompt seal

The instruction text shown to the cold encoder is itself a frozen experimental input.

Prompt file:

`current/experiments/GW04_ENCODER_PROMPT.md`

`sha256 = ccec096300cdc401a89bd8d500dc1e5423952d42641052f627f68d8b8d07848d`

The encoder must receive this prompt **verbatim**, together with the allowed input files. No extra explanatory text, examples, hints, reminders, follow-up corrections, or conversational steering may be added before the translation artifact is produced.

If the encoder asks for clarification, that request is part of the experimental result. Do not answer it by supplying new semantic guidance; stop and record the event unless a response policy was preregistered in advance.

## Cold encoder identity and isolation gate

The experiment must not start until the cold encoder identity is sealed in a commit.

Required execution metadata:

```text
ENCODER_MODEL      = GPT-6 (self-reported by the model, not verified in UI); ChatGPT web, Plus plan
ENCODER_EFFORT     = Средний
MODE               = Чат
ENCODER_SESSION_ID = https://chatgpt.com/c/6ad484aa-e4c8-83ed-bab9-4864d9a4e86c
ENCODER_MEMORY     = OFF
ISOLATION          = memory OFF; writing style OFF; record history OFF; web search OFF; connectors OFF; library search OFF; custom instructions = empty; chat opened outside any project; settings changed before the chat was opened
FORMAT_INPUT       = GW04_RULE_RECORD_FORMAT.md
FORMAT_SHA256      = c79bf7cd764c627622edceb0eea209e9e4ba7d54ad5b25db1277f39db1c99ac5
PROMPT_INPUT       = GW04_ENCODER_PROMPT.md
GW01_EXAMPLE_GIVEN = NO
```

Pre-file messages, exact, before any GW04 file:

```text
1. "გამარჯობა"
2. "რომელი მოდელი ხარ? მხოლოდ სახელი დაწერე."
```

Purpose: obtain the session link and the model name. No Noepedia/GW04 content was mentioned.

Planned encoder input, verbatim, nothing else:

```text
GW04_ENCODER_PROMPT.md       sha256 ccec096300cdc401a89bd8d500dc1e5423952d42641052f627f68d8b8d07848d
GW04_WORLD_TEXT.md           sha256 d43cc05f9fafc9098df07fc5961269a887ab579c7ab425e004388ff2693e669c
GW04_RULE_RECORD_FORMAT.md   sha256 c79bf7cd764c627622edceb0eea209e9e4ba7d54ad5b25db1277f39db1c99ac5
```

Clarification policy: if the encoder asks a question, the only permitted reply is:

> უპასუხე მხოლოდ მოცემული ფაილების საფუძველზე. რაც არ წერია, მონიშნე როგორც ENCODER_HOLE.

Any such question is recorded as an experimental result.

Eligibility constraints:

- the encoder must not be Claude/the author of GW04 or its answer book;
- it must not be the GPT session that authored this preregistration;
- it must be a new session that receives only the solver-visible world text and the frozen format inputs;
- encoder memory must be OFF, or the chosen external model/account must have no prior Noepedia context and this must be recorded explicitly;
- it must not see the answer book, RUN A output, RUN B output, or a hand-authored GW04 translation.

Gate status: **OPEN.** The encoder identity/session, model self-report, effort, mode, isolation state, memory state, GW01-example policy, pre-file messages, clarification policy, prompt hash, world-text hash, and format-contract hash are committed before any GW04 file is shown to the encoder.

Known context-bias note:

The default cold-encoder input is exactly two files:

```text
GW04_WORLD_TEXT.md
GW04_RULE_RECORD_FORMAT.md
```

`rules_gw01.py` may be added only if `GW01_EXAMPLE_GIVEN = YES` was committed before translation. If supplied, it may attract the encoder toward the six GW03 rule families. That exposure must remain visible in the audit.

## Cold-translation output seal

The encoder output becomes a sealed artifact before either mechanical run starts.

```text
cold translation
→ save encoder output verbatim
→ compute sha256
→ commit output filename + sha256
→ only then start RUN A
```

Required metadata:

```text
ENCODER_OUTPUT_FILE   = TO_BE_FILLED_AFTER_TRANSLATION_BEFORE_RUN_A
ENCODER_OUTPUT_SHA256 = TO_BE_FILLED_AND_COMMITTED_BEFORE_RUN_A
```

RUN A and RUN B must consume the same exact encoder-output bytes. The translation may not be edited between runs.

If deterministic loader normalization is unavoidable, both raw and normalized artifacts must be kept and separately hashed before RUN A.

No mechanical run may begin while `ENCODER_OUTPUT_SHA256` is unset.

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
- the resealed `generic_evaluator.py` and the base `demon_core.py` must remain unchanged across the pair; the evaluator's candidate hook is disabled in RUN A and enabled only by supplying the frozen overlay in RUN B.
- The only A/B difference is whether the frozen candidate overlay is supplied; no code or translation changes are allowed between the runs.
- No GW01-specific patch may be introduced.
- The solver may not infer meaning from N/K/Q/Z names.
- No object, predicate or law may be invented to make the world balance.

## Why this experiment matters

GW02 separated the mechanical demon from the LLM hologram.

GW03 moved executable rules into data.

GW04 now measures the next boundary:

> **Can a cold translator turn a new natural-language world into executable structural records without smuggling in the answer — and can the same content-blind executor then expose exactly where the remaining intelligence boundary lies?**

The important result is not a perfect score. The important result is a labeled boundary between what the text format can express, what the generic evaluator can execute, what the demon can decide, what requires outward contact, and what still requires semantic interpretation.
