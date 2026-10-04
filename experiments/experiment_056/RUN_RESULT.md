# Experiment 056 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS

Focused verification:
run_id = 37242883439
conclusion = success

## Adapter diagnostics

- relation count = 3
- input events = 38
- normalized events = 36
- input timeline count = 48
- output timeline count = 48
- dropped leading = 0
- dropped stale = 0
- max forward-fill steps = 8

All materialized series had equal length:
48

## Duplicate handling

Duplicate updates at the same relation/time were collapsed deterministically.

The later sequence/event ordering won.

## Split

- discovery length = 32
- buffer length = 8
- confirmation non-empty = true

## Downstream pair discovery

Selected pair:
`A_SOURCE -> B_TEMPORAL`

Detected features:
- TEMPORAL_CLUSTERING
- TRANSITION_ALIGNED_MISMATCH
- DIRECTION_ASYMMETRY
- LOCAL_RESIDUAL_CLUSTER

The identical comparison pair ranked lower.

## Correction

The first run used only change-event timestamps as the common timeline and therefore could not satisfy the intended split indices.

The adapter already supported an explicit timeline, so only the test fixture was corrected to supply the full 1..48 timeline.

Adapter semantics were unchanged.

See `CORRECTION.md`.

## Architectural conclusion

Sparse megagraph relation histories can now be converted into aligned state series and passed directly into the relation-pair scanner.

This removes the previous requirement to manually construct equal-length state series before pair discovery.
