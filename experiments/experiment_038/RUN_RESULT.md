# Experiment 038 — RUN RESULT

## Status

reproducibility = PASS
overall result = NO_FAMILY_NULL_PROTECTED

Focused GitHub Actions verification:
run_id = 37221427440
conclusion = success

## Purpose

Experiment 038 tested the temporal relations suggested by Experiments 036 and 037 against wider lag search and explicit null baselines.

Null baselines:
- target majority-state constant predictor
- four deterministic circular-shift temporal nulls

Null-protected success required at least 10% relative error reduction versus both null baselines.

## Family F036 — TP2 -> TP3

Direction frozen from Experiment 036:
HIGH_TO_LOW

Expanded discovery lag search:
1..400 rows

Selected lag:
75 rows

LAG_BOUNDARY_HIT = false

Discovery:
- old mismatches = 2426
- selected revised mismatches = 227

Confirmation:
- old mismatches = 2314
- revised mismatches = 2286
- majority mismatches = 2306
- permutation null mismatches = 2308, 2320, 2298, 2312
- permutation median = 2310

Relative reduction:
- vs old = 1.21%
- vs majority = 0.87%
- vs permutation median = 1.04%

Therefore:
NOT_NULL_PROTECTED

## Family F037 — Reservoirs -> H1

Direction frozen from Experiment 037:
HIGH_TO_LOW

Expanded discovery lag search:
1..400 rows

Selected lag:
75 rows

LAG_BOUNDARY_HIT = false

Discovery:
- old mismatches = 2554
- selected revised mismatches = 315

Confirmation:
- old mismatches = 2661
- revised mismatches = 1022
- majority mismatches = 1022
- permutation null mismatches = 1022, 1022, 1022, 1022
- permutation median = 1022

Relative reduction:
- vs old = 61.59%
- vs majority = 0%
- vs permutation median = 0%

Therefore:
NOT_NULL_PROTECTED

## Overall result

NO_FAMILY_NULL_PROTECTED

## Interpretation

The wider lag search resolves one concern from Experiments 036 and 037:
the best lag is not at the expanded grid boundary.

Both families show a discovery minimum near 75 rows.

However, neither family survives explicit null comparison on new confirmation data.

F036 produces only a very small improvement over both nulls.

F037 is exactly equal to the majority predictor and all tested circular-shift nulls.

Therefore the large mismatch reductions previously reported in Experiments 036 and 037 should not be treated as null-protected evidence of distinct revision relations.

## Retrospective status of Experiments 036 and 037

Experiment 036:
transferred temporal pattern, but NOT null-protected.

Experiment 037:
transferred temporal pattern, but NOT null-protected.

They should not be described as independent confirmed knowledge-revision loops.

## What remains strong

Experiment 033 remains the strongest confirmed knowledge-revision loop because its revised rule was developed from structured mismatch evidence and produced a 99.565% mismatch reduction on untouched data, while Experiments 034-035 prevented a weak residual pattern from being promoted.

## Claim boundary

Experiment 038 does not prove that TP2/TP3 or Reservoirs/H1 have no physical relation.

It shows only that the tested temporal rules do not outperform the preregistered null baselines strongly enough to support the stronger Noepedia revision-loop claim.