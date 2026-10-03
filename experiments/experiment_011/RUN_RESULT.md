# Experiment 011 — Verified Real-Data Run Result

> **Status:** repository CI reproduction passed.
>
> **Scientific result:** PASS under the preregistered success gate.

## External source

Numenta Anomaly Benchmark:

~~~text
data/realKnownCause/machine_temperature_system_failure.csv
~~~

Pinned source commit:

~~~text
ea702d75cc2258d9d7dd35ca8e5e2539d71f3140
~~~

Pinned data blob:

~~~text
7ac97fb6ef587efaf8770bfe7346e077da58ceb7
~~~

Pinned labels blob:

~~~text
2f1be355750a2fefa8d781215d3275fda3d83d23
~~~

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37161823800
job: verify
conclusion: success
head commit: b9fb50b7d4668cebcfb7a15e9912fcba8cd47cf9
~~~

## Frozen detector

~~~text
trailing window = 288 samples
robust scale = 1.4826 × MAD
FORMAL_MISMATCH when robust_z >= 6.0
future samples used = false
label input = false
~~~

The detector produced predictions before the label file was downloaded.

## Observed result

~~~text
total samples                 22695
scored samples                22407
mismatch count                  967
ground-truth anomaly windows      4
anomaly windows hit               4
window recall                  1.00
mismatch points in windows      268
mismatch points outside         699
point precision              0.2771458118
~~~

## Preregistered gate

~~~text
window_recall >= 0.50
point_precision >= 0.20
~~~

Observed:

~~~text
window_recall = 1.00
point_precision ≈ 0.277
~~~

Therefore:

~~~text
scientific_result = PASS
~~~

## Interpretation

This is the first experiment in the current sequence using an external real sensor trace rather than a synthetic fixture.

The positive result is narrow:

> A fixed, label-blind, trailing robust mismatch rule detected at least one event inside all four NAB anomaly windows and exceeded the preregistered point-precision floor.

The detector also produced many mismatch points outside labeled windows:

~~~text
699 / 967
~~~

so the result does **not** establish a high-quality anomaly detector.

The useful architectural result is that real observations can pass through:

~~~text
external trace
→ deterministic local expectation
→ explicit mismatch events
→ later external ground-truth evaluation
~~~

without labels entering the detector.

## Important blindness limitation

The detector is mechanically label-blind, but the human/model operator was already aware that NAB provides anomaly windows for this dataset.

This run therefore must not be described as a perfectly human-blind discovery experiment.

## Next OPEN

The large outside-window mismatch count creates the next question:

> Are these false positives, unlabeled but structurally meaningful regime changes, or evidence that the one-dimensional local expectation is too weak?

This should be investigated without retuning Experiment 011 in place.
