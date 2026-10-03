# Experiment 011 — Real Sensor Trace, Label-Blind Deterministic Mismatch Detection

> **Status:** preregistered real-data experiment.
>
> This experiment uses a public real-world sensor trace from the Numenta Anomaly Benchmark (NAB).

## Research question

Can the current Noepedia-style deterministic boundary:

~~~text
stored observation
→ explicit local expectation
→ mismatch event
→ external ground-truth comparison
~~~

operate on a real sensor stream without anomaly labels entering the detector?

## External source

Dataset:

~~~text
Numenta Anomaly Benchmark
data/realKnownCause/machine_temperature_system_failure.csv
~~~

NAB describes this file as temperature sensor data from an internal component of a large industrial machine.

The external source is pinned in `SOURCE.json` by repository commit and Git blob SHA.

Ground truth comes from NAB's independently maintained:

~~~text
labels/combined_windows.json
~~~

## Important blindness boundary

The detector code is mechanically label-blind:

- it receives only timestamp + value;
- it does not receive anomaly windows;
- it does not import the evaluator;
- it does not read `combined_windows.json`;
- no detector parameter is selected at runtime from labels.

The human/model operator has already seen that NAB provides anomaly windows for this dataset. Therefore this experiment must **not** be described as a perfectly human-blind discovery trial.

The valid claim is narrower:

> the committed deterministic detector is label-blind, and its output is compared with external labels only after detection.

## Frozen detector rule

Sampling is expected at approximately five-minute intervals.

For every sample after the first 288 observations:

1. take only the previous 288 values;
2. compute their median;
3. compute median absolute deviation (MAD);
4. convert MAD to robust scale with factor 1.4826;
5. calculate:

~~~text
robust_z = abs(current - median) / max(1.4826 * MAD, 1e-6)
~~~

6. emit `FORMAL_MISMATCH` when:

~~~text
robust_z >= 6.0
~~~

No future sample is used to score the current sample.

## Event representation

Every mismatch must preserve:

- timestamp;
- observed value;
- trailing median;
- trailing MAD;
- robust z-score;
- source row number;
- rule identifier.

This makes the detector output an inspectable relational event rather than only a binary anomaly label.

## External evaluation

Only after `predictions.json` has been produced may the evaluator load NAB anomaly windows.

Metrics:

- total samples;
- scored samples;
- mismatch count;
- anomaly-window count;
- anomaly windows hit by at least one mismatch;
- window recall;
- mismatch points inside labeled windows;
- mismatch points outside labeled windows;
- point precision.

## Frozen scientific success gate

A **positive first real-data result** requires both:

~~~text
window_recall >= 0.50
point_precision >= 0.20
~~~

This gate is intentionally modest.

If it fails, the failure is preserved. Parameters must not be retuned inside Experiment 011.

Any changed threshold/window/rule becomes a new experiment.

## What this experiment does not test

It does not test:

- multichannel reconstruction;
- causal diagnosis;
- repair selection;
- predictive maintenance;
- LLM advantage;
- branch ranking;
- production readiness.

## Reproducibility boundary

The CI job verifies:

1. pinned source bytes by Git blob SHA;
2. detector runs without labels;
3. predictions are written before label evaluation;
4. evaluation metrics are deterministic;
5. the scientific gate is reported independently from CI execution success.

A CI PASS means the experiment reproduced correctly.

It does **not** automatically mean the scientific success gate passed.
