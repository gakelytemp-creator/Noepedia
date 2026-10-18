# GW05 — preregistration (sealed world before RUN C handlers)

**Status: WORLD SEALED / PRE-HANDLER GATE**  
**Date: 2026-10-18**

## Sealed inputs

Solver-visible world:

`current/experiments/GW05_WORLD_TEXT.md`

`sha256 = 325932a64bf7bd31b1e34a553c897e8fdff01534e12ec6b3143dff7a746f277c`

Sealed answer book, held outside the solver-visible repository state until all planned GW05 runs are frozen:

`GW05_ANSWER_BOOK.md`

`sha256 = 654ad18d938af40651925537893e654326687ca3de960b262c855669b745f4c1`

The answer book must not be opened, copied into the repository, shown to the handler author, shown to the cold encoder, or used to modify handlers before the GW05 logs are sealed.

## Purpose split

GW04 is public and may be used only as the **RUN C cost benchmark** for implementing executor support.

GW05 is the **transfer/correctness benchmark**. Because its world and answer-book hash are sealed before RUN C handler implementation, GW05 must not be used to tune handler behavior.

The experiment separates:

- **cost**: how much executable machinery a programmer must add on the public GW04 records;
- **correctness/transfer**: whether those frozen handlers work on a fresh world with the same law families after a fresh cold translation.

## Programmer-share metrics for RUN C

These metrics must be fixed before handler implementation and reported after the handler code is frozen:

- number of new generic operations reusable across rule families;
- number of rule-type-specific handlers;
- source lines of code excluding docstrings/comments;
- source lines of code including docstrings/comments;
- structured design-decision log count and entries.

Each design-decision entry must record at minimum:

```text
DECISION_ID
RULE_OR_INTERFACE
UNDERSPECIFIED_POINT
ALTERNATIVES
CHOICE
RATIONALE
EXECUTABLE_SEMANTICS_CHANGED = YES | NO
```

The design-decision log is part of the measured programmer share, not post-hoc commentary.

## Generality gate for RUN C handlers

Handler code must be world-content-blind.

It may read rule-record fields and generic network structures, but it must not contain:

- any GW04 or GW05 world fact;
- any event-specific answer;
- any object/predicate/status identifier from the tested worlds as implementation logic;
- branches keyed to concrete N/K/Q/Z or I/B/G/V/S/R identifiers.

This gate must be checked mechanically, including an AST-level inspection in addition to text search.

## SCHEMA_DRIFT

GW05 requires a fresh cold translation in a new isolated session after RUN C handlers and the decision log are frozen.

Handlers are written against the already public GW04 translation/interface. After the GW05 translation is produced, handler code, adapters, aliases, and schema mappings must remain frozen through the correctness run.

Difference class:

```text
SCHEMA_DRIFT
```

Use `SCHEMA_DRIFT` when the cold encoder faithfully expresses the same rule family but chooses a record shape or field vocabulary that the frozen handler interface does not accept.

Keep distinct:

```text
ENCODER_HOLE   = faithful representation could not be produced
EXECUTOR_HOLE  = required executable capability does not exist
SCHEMA_DRIFT   = capability exists for the family, but the fresh faithful schema does not fit the frozen handler interface
EXECUTOR_ERROR = handler accepts the schema/path but executes it incorrectly
```

No GW05-specific adapter may be added after observing the GW05 translation.

## Candidate isolation

RUN C measures executor support for the five law families only.

C1 and C3 fixes are not part of RUN C handler development. They may be tested on GW05 only in separately attributed runs/mechanisms whose code is frozen independently. No C1/C3 repair may be justified by re-running GW04.

## Required order

The experiment order is frozen as follows:

1. Commit `GW05_WORLD_TEXT.md` and both GW05 hashes. **This commit must exist before any RUN C handler implementation begins.**
2. Only after step 1, implement RUN C handlers using public GW04 material for cost measurement. The GW05 answer book remains sealed. The GW05 world must not be used to tune handlers.
3. Freeze handler code, all generic operations, the handler interface/schema expectations, the structured decision log, and their hashes.
4. Open a new isolated cold-encoder session for GW05 and translate only the solver-visible GW05 inputs under the separately frozen encoder protocol.
5. Freeze the raw GW05 translation before execution. If normalization is required, freeze raw and normalized artifacts separately before the run.
6. Run GW05 with the already frozen handlers. Freeze all logs and hashes.
7. Only after all planned GW05 logs are frozen may the sealed GW05 answer book be opened and audited.

## Current gate

**PRE-HANDLER GATE: OPEN.**

The GW05 world text and answer-book hash are sealed before RUN C handler implementation.

No RUN C handler code is included in this commit.
