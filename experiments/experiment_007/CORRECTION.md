# Experiment 007 — Correction Record

## Why this correction exists

The first GitHub Actions verification run for Experiment 007 failed.

The failure did **not** change the scientific verdicts of the experiment.

The deterministic evaluator produced the expected structural outcomes:

- three `DERIVED_RELATION` events;
- one `ANTECEDENT_NOT_SATISFIED`;
- one `CONSISTENT`;
- one `FORMAL_MISMATCH`;
- one `REQUIRED_RELATION_MISSING`;
- OPEN_01 preserved.

The failure occurred because the frozen `EXPECTED_OUTPUT.json` did not include the provenance-bearing
`input_relations` field for the second-stage events.

The evaluator correctly reported that the second-stage rule consumed the derived working relations:

~~~text
DERIVED::RULE_DERIVE_LINK::L1::LINK::R1
DERIVED::RULE_DERIVE_LINK::L2::LINK::R2
DERIVED::RULE_DERIVE_LINK::L3::LINK::R3
~~~

while the frozen expected file implicitly expected those fields to be absent.

## Classification

~~~text
prediction error?          NO
scientific verdict error?  NO
verifier/schema omission?  YES
~~~

## Correction scope

Only the expected provenance/input contract is being corrected.

The following remain unchanged:

- event counts;
- event types;
- subject-level verdicts;
- derived relation set;
- mismatch target;
- missing-relation target;
- OPEN preservation;
- rule semantics.

## Audit rule

The failed CI run must remain part of the public history.

The corrected expectation is committed separately after this correction record so the post-hoc nature of the schema fix is explicit.
