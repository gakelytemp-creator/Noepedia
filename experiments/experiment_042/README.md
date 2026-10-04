# Experiment 042 — Revision Protocol

Primary document:
`REVISION_PROTOCOL.md`

Status:
`SPECIFICATION_COMPLETE`

This experiment converts the validated workflow from Experiments 019–041 into a reusable Noepedia revision protocol.

Canonical sequence:

`MISMATCH -> OPEN -> CANDIDATE -> FREEZE -> CONFIRM -> NULLS -> PROMOTE/REJECT -> REFINE OPEN`

Key rules:
- discovery and confirmation must be separated;
- failed confirmation blocks promotion;
- plausible trivial explanations require explicit null models;
- negative results remain stored;
- OPEN is refined, not erased;
- corrections preserve historical results;
- promotion requires complete provenance.

Next step:
`Experiment 043 — Core Data Model for Revision`