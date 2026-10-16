# GW01 — Claude cold run and controlled overlay rerun

**Status: EXPERIMENTAL RECORD / GLASS-WORLD ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. Reproducibility package

The rerun package was supplied as `GW01_COLD_RERUN_PACKAGE.md` and states that the sealed answer-book content and previous solver output are not included.

Integrity metadata from the package:

    WORLD_INPUT.md      sha256 841ddd5385d2890e4e90f6775a398045f98af97b445c0684b136af5814bab7d3
    DEMON_CORE_SPEC.md  sha256 0344b90f159437d12bb09c2b0e5dc37e1f042dfa9855018059d7624993cd705b
    ANSWER_BOOK.md      sha256 3ba3627a145fb9bf9653b2c9782d6337542e61a9501f3be2774f867a9605b027

The package says the previous cold solver saw only `WORLD_INPUT.md` and the then-current `DEMON_CORE_SPEC.md`; identifiers were opaque and E1..E12 had to be processed in order.

## 1. First Claude cold-run result

The reported first-run result separated **honesty** from **power**.

Observed strengths:

- E2 identity ambiguity stayed ASK; no false merge.
- E3 derivation was correct and provenance/ROLE was preserved.
- E4 impossible goal was classified BLOCK rather than NEED.
- E7 older state became HISTORICAL without destructive overwrite.
- E9 exposed two separate blocks rather than fabricating a path.
- The solver found an additional world/spec gap: no explicit authorization for ingesting source-supplied records.

Observed limitations:

1. E5 could not create a requirement concept because the general birth rule was OPEN while CREATE_ADDRESS requires explicit authorization.
2. E6 could not install an operational watch/trap because the core had no post-COMMIT reevaluation mechanism.
3. E8 retained two CURRENT P3 values because no P3 multiplicity/cardinality rule existed. This was formally honest, but the ambiguity remained silent.

This was a single-model/single-run synthetic result: GLASS_WORLD evidence, not CONTACT_PASS.

## 2. Minimal WORKING overlay derived from the run

The controlled analysis introduced only four narrow capabilities, deliberately without adding domain knowledge to the demon.

### A. Source ingest authorization

An explicit external source event may **PROPOSE** an addressable observation/assertion carrying source/time provenance; it still passes CHECK → COMMIT. Sources do not write directly into the network.

### B. Requirement lifecycle from explicit task structure

If an addressable TASK explicitly supplies required triplet-patterns, it may authorize creation of one scoped REQUIREMENT_CONCEPT containing exactly those patterns.

Lifecycle:

    explicit TASK
    → create requirement concept
    → remain OPEN while no fully supported binding exists
    → bind only to a candidate satisfying every required pattern
    → preserve prior OPEN history

The general requirement-concept birth rule remains OPEN; this is only the explicit-task case.

### C. Watch / trap executor hook

An explicit task of the form 'notify when pattern becomes current' may create an ACTIVE WATCH record in the network.

Executor responsibility:

    COMMIT
      → re-evaluate affected ACTIVE WATCHes
      → false→true transition emits addressable KAIROS/EVENT

Trap definition lives in the network; the post-COMMIT reevaluation trigger belongs to the executor boundary.

### D. Unknown predicate multiplicity becomes visible OPEN

If one subject/predicate has multiple different CURRENT targets and no current-value multiplicity/cardinality policy exists, create an addressable OPEN describing unresolved multiplicity.

Do not silently assume either single-valued or multi-valued semantics.

## 3. Controlled overlay rerun

This was **not a new blind run**: the analyst already knew the previous Claude outcome. It is therefore a controlled architecture rerun, not independent confirmation.

Event-level result under the minimal overlay:

    E1   GO — source assertion ingested through PROPOSE/CHECK/COMMIT
    E2   ASK — identity remains ambiguous
    E3   GO — O4 P1 O1 derived with provenance
    E4   BLOCK — scene constraint + P1 single-current-target rule
    E5   GO-with-OPEN — scoped requirement concept created; no complete candidate yet
    E6   GO — active watch created for (O4 P3 S3) becoming current
    E7   GO — old O6 P1 O1 marked HISTORICAL; new O6 P1 O2 current
    E8   GO + OPEN — O4 P3 S3 committed; unresolved P3 multiplicity made visible; watch fires KAIROS
    E9   BLOCK — vision blocked by R4 and P1 target conflict remains illegal
    E10  OPEN — same E5 requirement remains unresolved
    E11  GO — O5 P4 O8 and O5 P5 TRUE ingested
    E12  GO — O5 is the complete candidate; requirement is lawfully bound while OPEN history remains traceable

## 4. Main result

The overlay restored the missing functions without giving the demon semantic guessing power.

    HONESTY: preserved
    POWER: substantially restored in GW01

The added mechanisms are structural:

    source → proposal
    explicit task → requirement lifecycle
    commit → affected-watch reevaluation
    unresolved multiplicity → addressable OPEN

Not added:

    guessed ontology
    guessed identity
    guessed predicate cardinality
    guessed closure

## 5. Next test

Run the **same sealed GW01** again with a genuinely fresh cold agent using a revised specification containing only these WORKING changes.

Success criterion:

- E5/E6/E12 close lawfully;
- E8 multiplicity ambiguity becomes visible rather than silently settled;
- previous honesty properties remain intact;
- no new false closures or ontology invention appear.

Until that fresh rerun happens, the four additions remain WORKING CANDIDATES rather than promoted invariants.
