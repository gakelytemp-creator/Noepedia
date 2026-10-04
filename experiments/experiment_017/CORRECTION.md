# Experiment 017 — Interpretation Correction

> This correction preserves the original preregistered run and verdict. It does not rewrite history.

## What happened

The held-out file used in Experiment 017 had a different sampling cadence from the development file.

~~~text
Experiment 011 development series:
machine_temperature_system_failure.csv
approximately 5-minute cadence
288 samples ≈ 24 hours

Experiment 017 held-out series:
ambient_temperature_system_failure.csv
approximately 1-hour cadence
288 samples ≈ 12 days
~~~

The frozen detector was defined in **sample count**, not physical time. Therefore the nominally unchanged 288-sample rule represented a very different physical window.

## Audit status

~~~text
CI / reproducibility status       = PASS
original preregistered verdict    = FAIL
current transfer interpretation   = NOT_EVALUABLE
~~~

The original FAIL remains part of the experiment history because the preregistered procedure was executed correctly.

However, it should not be interpreted as evidence that the detector failed to transfer between compatible series. The held-out compatibility criterion itself was underspecified.

## Methodological lesson

Before pinning a future transfer dataset, compatibility criteria must be frozen, including at minimum:

- sampling cadence / physical window equivalence;
- signal class and measurement semantics;
- required observation density;
- detector input assumptions.

Changing the Experiment 017 file after seeing the result would invalidate the held-out test, so no replacement is made inside Experiment 017.