# Experiment 069 — Diagnostic Protocol

## Frozen source

Replay the exact Experiment 068 adapter, split, pair universe, state construction, lag grid, shuffle seeds and revision machinery.

## Audit categories

For every real and shuffled pair, record:

- selected candidate family;
- selected null list;
- final decision;
- decision reason;
- frozen parameters;
- search-boundary status when available.

Aggregate decision reasons.

## Null-coverage audit

For each selected candidate family, compare nulls demanded by `select_nulls(...)` with null metrics actually supplied by the evaluator family.

Known evaluator metric capabilities are read from the current frozen implementation, not inferred from outcomes.

A required metric requested by the selector but absent from evaluator output is classified:

`NULL_METRIC_COVERAGE_GAP`

Non-metric controls such as `SEARCH_BOUNDARY_CHECK` are not counted as metric gaps.

## Interpretation boundary

Experiment 069 does not change the scientific result of Experiment 068.

If a coverage gap is found, it means only that some 068 candidates were conservatively blocked by incomplete evaluation plumbing.

Any code correction must occur in a later experiment and any new real-data discovery test must receive a new experiment number.
