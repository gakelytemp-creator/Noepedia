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
