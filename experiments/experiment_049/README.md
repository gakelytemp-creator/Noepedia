# Experiment 049 — Candidate Generator + Null Selector

Purpose:
validate the first generic candidate-generation and null-selection layer in `core/revision/`.

Components under test:
- `core/revision/candidates.py`
- `core/revision/nulls.py`

Scenarios:
- temporal + directional mismatch structure
- threshold uncertainty
- local residual cluster
- class-imbalance / simpler-baseline risk

Pass criteria:
- expected candidate families are generated
- deterministic ranking is stable
- temporal candidates receive majority + time-shift/permutation nulls
- threshold candidates receive threshold-perturbation null
- local-exception candidates require untouched transfer
- bounded search adds search-boundary protection
- unknown structure falls back to OPEN decomposition rather than invented semantics