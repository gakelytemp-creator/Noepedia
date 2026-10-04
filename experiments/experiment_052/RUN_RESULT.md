# Experiment 052 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS

Focused verification:
run_id = 37240102673
conclusion = success

## Positive end-to-end case

Selected family:
`TEMPORAL_LAG_REVISION`

Frozen parameters:
- direction = HIGH_TO_LOW
- lag = 3

Decision:
`PROMOTE`

Graph result:
- parent rule preserved
- OPEN preserved
- gate audit materialized
- decision materialized
- OPEN refinement materialized
- one distinct new rule version created
- DERIVED_FROM_RULE and SUPERSEDED_BY links present
- append-only invariants passed

## Unknown-structure case

Selected family:
`OPEN_DECOMPOSITION`

Decision:
`REMAIN_OPEN`

No graph mutation was performed and no unsupported rule was invented.

## Architectural conclusion

The reusable core pipeline now connects:

`candidate generation -> null selection -> preregistration template -> parameter search -> confirmation metrics -> gate audit -> decision -> graph materialization`

The main remaining manual input is structural feature metadata describing mismatch geometry.
