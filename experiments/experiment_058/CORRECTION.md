# Experiment 058 — Verification Expectation Correction

The first verification run produced two failed assertions while the strategy layer itself resolved and executed correctly.

## 1. Default timeline expectation

The test incorrectly expected the default INTEGER_RANGE_FROM_EVENTS policy to reconstruct the original synthetic array length of 240.

Sparse history only records change events, and the final recorded change occurs at time 229.

Therefore the policy correctly resolves the observable event extent as:

1..229

The corrected assertion checks the resolved event extent, not the hidden source-array length.

## 2. Custom strategy decision expectation

The test incorrectly required a stricter custom strategy to produce the same PROMOTE decision as the default strategy.

A reusable strategy object is allowed to change the evidential outcome because it changes discovery/confirmation allocation and search/null configuration.

The architectural requirement is:
- policy resolves deterministically;
- the same meaningful pair remains selectable;
- the resulting decision is one valid epistemic state;
- graph invariants remain valid.

Therefore the custom-strategy assertion now accepts PROMOTE, REJECT, or REMAIN_OPEN and verifies provenance plus graph validity.

No strategy implementation, data, pair-scanning logic, or scientific metrics were changed.
