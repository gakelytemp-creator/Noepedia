# Experiment 038 — Null-Protected Temporal Relation Validation

Experiment 038 re-evaluates the temporal relations suggested by Experiments 036 and 037 with wider lag search and explicit null baselines.

Families:
- F036: TP2 -> TP3
- F037: Reservoirs -> H1

New windows:
- discovery = rows 750,001..755,000
- confirmation = rows 800,001..805,000

For each family the discovery step searches lag 1..400 rows for the already observed HIGH_TO_LOW source transition direction.

The selected lag is frozen before confirmation.

On confirmation, the revised temporal rule must beat:
1. old direct equality
2. target majority-state constant predictor
3. deterministic circular-shift temporal nulls

to receive a null-protected confirmation.