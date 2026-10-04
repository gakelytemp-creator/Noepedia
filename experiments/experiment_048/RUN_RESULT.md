# Experiment 048 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS

Focused GitHub Actions verification:
run_id = 37236857528
conclusion = success

## Core module

`core.revision`

## Historical behavior reproduced

Experiment 040-derived case:
- decision = PROMOTE
- new rule count = 1

Experiment 039-derived case:
- decision = REJECT
- new rule count = 0

## Invariants

All checks passed:
- positive decision preserved
- negative decision preserved
- positive graph invariants passed
- negative graph invariants passed
- positive case created exactly one new rule
- negative case created no new rule
- parent rules preserved
- OPEN objects preserved
- append-only history preserved

## Architectural conclusion

The reusable revision engine and materializer have been successfully migrated from experiment-local implementations into:

`core/revision/`

The `experiments/` implementations remain historical provenance and validation records.

The active reusable implementation now lives in the core subsystem.

## Current boundary

The core revision subsystem automates gate auditing, decision semantics, and graph materialization.

Candidate generation and domain-specific null-model selection are not yet generic core capabilities.