# Experiment 056 — Test Setup Correction

The first focused run failed before scientific/architectural evaluation because the sparse history adapter was allowed to derive its timeline only from event timestamps.

Sparse histories contain only change-points, so the derived timeline had fewer positions than the preregistered discovery/buffer/confirmation split expected.

The adapter already supports an explicit common timeline.

Correction:
- adapter code unchanged;
- event history unchanged;
- split indices unchanged;
- scanner logic unchanged;
- only the verification setup now supplies the full timeline 1..48.

This is an implementation/test-fixture correction, not a semantic change.
