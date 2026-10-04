# Experiment 033 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS
scientific result = REVISION_IMPROVES_FIELD
strong flag = true

Focused GitHub Actions verification:
run_id = 37198518403
conclusion = success

## Untouched window

rows 450,001..455,000

## OLD direct-mapping rule

evaluated rows = 5000
formal mismatches = 1394
mismatch fraction = 27.88%

## REVISED provenance-bearing rule

evaluated rows = 4616
formal mismatches = 6
mismatch fraction = 0.12998%

Explicit TRANSITION_OPEN rows = 384
MID raw-current unresolved rows = 0

The 384 transition-zone rows are not counted as successful matches. They remain explicitly unresolved.

## Common evaluable subset

rows = 4616

OLD rule mismatches = 1380
REVISED rule mismatches = 6

OLD mismatch fraction = 29.896%
REVISED mismatch fraction = 0.12998%

relative mismatch reduction = 99.565%

Therefore:

REVISION_IMPROVES_FIELD
REVISION_REDUCES_MISMATCH_BY_90_PERCENT = true

## Knowledge-revision loop

This experiment completes the intended loop:

old rule
-> formal mismatch
-> OPEN
-> independent evidence gathering
-> replicated temporal relation
-> physical-time audit
-> provenance-bearing revised rule
-> re-entry into the frozen Noepedia evaluator
-> large mismatch reduction on untouched data

## Provenance of revised rule

EXP027: direction-specific response-time discovery
EXP030: held-out replication of the directional response
EXP031: timestamp cadence audit
EXP032: event-wise physical-time replication

Epistemic status remains EMPIRICALLY_SUPPORTED_RULE, not FACT.

## OPEN refinement

Resolved component:
direction-dependent LOAD_OFF temporal exception.

Remaining OPEN:
- 6 residual formal mismatches
- interpretation of the explicit 41..52 transition zone
- minority long-tail response events
- physical/controller mechanism

The original DOMAIN_VALIDITY_OF_CROSS_PATH_MAPPING OPEN is therefore refined, not erased.

## Claim boundary

Experiment 033 establishes that the learned temporal rule dramatically improves the Noepedia field on untouched data using the frozen evaluator.

It does not establish causal mechanism, fault, anomaly, or universal compressor law.