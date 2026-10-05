# Noepedia Revision Subsystem

> Scope note: this directory is one reusable deterministic epistemic organ. It is not the whole Noepedia core and not the whole Socratic Daimonion.

This directory contains the reusable revision subsystem extracted from Experiments 042–047.

In the current architecture, this code is best understood as a crystallized Daimonion habit: a once-flexible revision procedure that became explicit enough to execute deterministically, audit separately, and invoke only when its preconditions are met.

The persistent Noepedia field remains the simpler substrate of addressable objects, relation tables, provenance/source tokens, status, uncertainty, time/version information, and OPEN structure. See CURRENT_ARCHITECTURE.md.

Primary modules:
- `engine.py` — promotion-gate audit and PROMOTE / REJECT / REMAIN_OPEN decision engine
- `materializer.py` — append-only graph materialization of revision decisions

Core lifecycle:
`MISMATCH -> OPEN -> CANDIDATE -> FREEZE -> CONFIRM -> NULLS -> DECIDE -> MATERIALIZE -> REFINE OPEN`

Architectural invariants:
- no in-place rule mutation
- rejected candidates remain queryable
- OPEN is refined, not erased
- promotion creates a new rule version
- confirmation and null gates control promotion
- history remains append-only

Historical specifications:
- Experiment 042 — Revision Protocol
- Experiment 043 — Core Revision Data Model
- Experiment 044 — Promotion Gates

Executable provenance:
- Experiment 045 — automated decision harness
- Experiment 046 — graph materialization
- Experiment 047 — external architecture transfer

The files in `experiments/` remain historical records. The reusable implementation now lives here.

## Candidate generation and null selection

The subsystem now also provides:
- `candidates.py` — conservative structural candidate-template generation from explicit mismatch/Open features;
- `nulls.py` — null-model selection from candidate family and explicit risk flags;
- preregistration-template construction before confirmation.

The generator does not invent domain semantics. If supplied structure does not justify a known revision family, it emits `OPEN_DECOMPOSITION` rather than fabricating a rule.

Validated by Experiment 049.


## Generic candidate evaluator

The subsystem now includes `evaluator.py` for deterministic parameter search and null-metric computation.

Currently supported families:
- `TEMPORAL_LAG_REVISION`
- `DIRECTION_SPECIFIC_RULE`
- `THRESHOLD_REFINEMENT`

The evaluator:
- searches parameters on discovery data only;
- freezes the selected parameters;
- evaluates them unchanged on confirmation data;
- detects search-boundary optima;
- computes majority/permutation null metrics for temporal candidates;
- computes threshold-perturbation null metrics for threshold candidates.

Validated by Experiment 050.
