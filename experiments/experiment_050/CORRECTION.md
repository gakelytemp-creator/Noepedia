# Experiment 050 — Test Expectation Correction

The first verification run failed one assertion:

`threshold_confirmation_zero_error`

This was a test-design error, not an evaluator error.

Discovery selected and froze threshold = 9.0.

The confirmation target values are deliberately shifted by +0.1, so the frozen threshold correctly produces one mismatch on confirmation.

Requiring zero confirmation error would implicitly demand retuning the threshold on confirmation data, which would violate the discovery/freeze/confirmation separation.

Correction:

- evaluator code unchanged
- discovery grid unchanged
- confirmation data unchanged
- frozen threshold unchanged
- only the verification expectation changed from 0 mismatches to 1 mismatch

The corrected assertion is:

`threshold_confirmation_frozen_parameter_preserved`
