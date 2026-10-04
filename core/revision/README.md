# Noepedia Core — Revision Subsystem

This directory contains the reusable revision subsystem extracted from Experiments 042–047.

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