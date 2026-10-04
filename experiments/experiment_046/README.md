# Experiment 046 — Self-Revision Materialization Test

Experiment 046 tests whether the Experiment 045 revision harness can materialize revision decisions into append-only Noepedia graph records.

Validation cases:
- Experiment 040-derived PROMOTE case
- Experiment 039-derived REJECT case

PROMOTE must create:
- a new versioned RULE object
- provenance relations
- SUPERSEDED_BY relation from parent rule
- OPEN_REFINEMENT object
- preserved parent rule and OPEN history

REJECT must create:
- REJECTED_CANDIDATE object
- rejection provenance
- OPEN_REFINEMENT object
- no new promoted rule

No historical object may be deleted or mutated in place.