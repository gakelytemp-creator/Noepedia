# Experiment 045 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS

Focused GitHub Actions verification:
run_id = 37231772611
conclusion = success

## Integration cases

Expected decisions:
- Experiment 040 derived case -> PROMOTE
- Experiment 039 derived case -> REJECT
- synthetic non-evaluable case -> REMAIN_OPEN

Observed decisions:
- Experiment 040 derived case -> PROMOTE
- Experiment 039 derived case -> REJECT
- synthetic non-evaluable case -> REMAIN_OPEN

Therefore:

`integration_pass = true`

## History invariant

`history_mutation_detected = false`

The harness emitted decision/audit records without mutating historical parent rules in place.

## What was implemented

`revision_harness.py`
- evaluates mandatory structural gates
- evaluates confirmation evaluability
- compares old vs revised primary metric
- evaluates preregistered null advantages
- handles search-boundary policy
- distinguishes REJECT from REMAIN_OPEN
- emits PROMOTION_GATE_AUDIT
- emits proposed new-rule record on PROMOTE
- emits rejected-candidate record on REJECT

`adapter_040.py`
- maps the strong Experiment 040 result into a generic REVISION_CASE

`adapter_039.py`
- maps the failed-transfer Experiment 039 result into the same generic REVISION_CASE structure

`run_experiment.py`
- reruns source experiments
- builds cases
- executes one common harness
- verifies all three decision classes

## Decision semantics validated

`PROMOTE`
means all mandatory gates passed.

`REJECT`
means the candidate was fairly tested and failed a scientific gate.

`REMAIN_OPEN`
means no justified scientific decision was available because evaluation was incomplete or unavailable.

## Architectural significance

Experiment 045 is the first executable implementation of the protocol defined in Experiments 042–044.

The revision lifecycle is no longer only a document specification.

The same decision engine can now discriminate between:
- a strong positive revision;
- a scientifically failed revision;
- an unresolved/non-evaluable case.

## Current limitation

Candidate generation and domain-specific null computation are still performed by experiment-specific adapters.

The generic harness currently governs:
- gate validation;
- decision semantics;
- promotion/rejection record generation;
- history-preservation behavior.

It does not yet autonomously generate candidates or choose domain-specific null models.

## Claim boundary

Experiment 045 demonstrates automated revision decision orchestration.

It does not yet demonstrate fully autonomous knowledge revision from raw mismatch to candidate generation.

## Next step

Experiment 046 should perform a Self-Revision Test:
- feed a complete revision case into the new architecture;
- automatically construct the gate audit;
- produce PROMOTE/REJECT/REMAIN_OPEN;
- materialize the resulting graph records;
- verify that the promoted rule appears as a new version and OPEN is refined without deleting history.