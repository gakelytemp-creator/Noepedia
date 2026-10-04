# Experiment 054 — Observation-Driven End-to-End Revision

Purpose:
validate `run_revision_from_observations(...)`.

The test does not manually supply:
- structural feature labels,
- candidate family,
- null-model types.

The pipeline must derive them from discovery observations.

Validation cases:
- transition-aligned delayed behavior -> detected temporal/directional structure -> candidate selection -> nulls -> evaluation -> PROMOTE;
- quiet matching observations -> no supported revision family -> OPEN_DECOMPOSITION -> REMAIN_OPEN.
