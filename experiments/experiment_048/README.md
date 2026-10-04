# Experiment 048 — Core Revision Subsystem Integration

Purpose:
verify that the reusable `core/revision/` subsystem reproduces the validated behavior of Experiments 045–046.

Cases:
- Experiment 040-derived positive revision -> PROMOTE -> one new rule version
- Experiment 039-derived failed revision -> REJECT -> zero new rule versions

Pass criteria:
- decisions match historical validated decisions
- graph invariants pass
- parent rule preserved
- OPEN preserved
- positive case creates exactly one new rule
- negative case creates no new rule
- append-only history preserved