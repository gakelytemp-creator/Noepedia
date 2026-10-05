# Experiment 072 — Verification Fixture Correction

The first focused run failed before evaluating the repair.

Cause:
the shuffled class-imbalance control generated a compatible temporal candidate, but the verification fixture passed an empty evaluator configuration.

The temporal evaluator therefore correctly raised:

`ValueError: temporal candidate requires lag_search`

Correction:
- repair semantics unchanged;
- data unchanged;
- shuffle seed unchanged;
- candidate generation unchanged;
- promotion gates unchanged;
- only the shuffled-control fixture now supplies the same frozen lag/direction/permutation configuration used by the other temporal controls.

This is a test-fixture execution correction, not an outcome-driven repair change.


## Core enrichment correction found by validation

The second verification run showed that explicit context risk flags were replaced by automatically extracted risk flags inside `enrich_context_from_observations(...)`.

That behavior erased an explicitly preregistered `SIMPLE_BASELINE_PLAUSIBLE` risk and therefore prevented the expected `SIMPLER_RULE_NULL` from being selected.

Correction:
- extracted features/risks are now merged with explicit context features/risks;
- explicit preregistered risks are preserved;
- no candidate ranking priority, promotion threshold, or null definition changed.

This correction restores the intended invariant that automatic feature extraction may add evidence metadata but must not silently delete explicit risk metadata.
