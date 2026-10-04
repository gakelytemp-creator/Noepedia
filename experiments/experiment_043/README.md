# Experiment 043 — Core Revision Data Model

Primary document:
`CORE_REVISION_DATA_MODEL.md`

Status:
`DATA_MODEL_SPECIFICATION_COMPLETE`

This experiment turns the Experiment 042 revision protocol into explicit core objects, relations, lifecycle states, provenance edges, and immutable history.

Key object classes:
- RULE
- FORMAL_MISMATCH
- OPEN
- EVIDENCE
- RULE_CANDIDATE
- PREREGISTRATION_RECORD
- NULL_MODEL
- CONFIRMATION_RUN
- CONFIRMATION_RESULT
- PROMOTION_DECISION
- EMPIRICALLY_SUPPORTED_RULE
- REJECTED_CANDIDATE
- CORRECTION
- OPEN_REFINEMENT
- EVALUATOR_SNAPSHOT
- DATA_WINDOW

Core principle:
`revision = append-only epistemic history, not in-place knowledge mutation`

Next step:
`Experiment 044 — Promotion Gates`