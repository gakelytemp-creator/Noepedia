# Experiment 017 — One-Shot Held-Out Replication with Exact Null Baseline

> **Status:** preregistered held-out real-data replication.
>
> The held-out file was selected from NAB directory metadata only. Its values and anomaly-window entry were not inspected before this preregistration.

## Purpose

Experiments 011–016 formed an adaptive exploratory cascade on one development series.

Experiment 017 stops feature hunting and asks a harder question:

> **Does the frozen real-data pipeline produce detector enrichment above chance on a different NAB series, without changing any detector parameter?**

A secondary question is whether the previously frozen episode / transition / clustering stages are even structurally reproducible on the held-out series.

## Held-out dataset

~~~text
Numenta Anomaly Benchmark
data/realKnownCause/ambient_temperature_system_failure.csv
~~~

Pinned source details are in `SOURCE.json`.

## Frozen primary detector

Experiment 017 reuses **Experiment 011 detector.py unchanged**:

~~~text
trailing window = 288 samples
robust scale = 1.4826 × MAD
FORMAL_MISMATCH when robust_z >= 6.0
future samples used = false
label input = false
~~~

No threshold, window, or detector logic may be changed after the held-out run.

## Exact matched-count null baseline

After predictions are frozen and only then labels are loaded, define:

~~~text
N = number of scored timestamps
K = number of scored timestamps inside NAB anomaly windows
n = detector mismatch count
X = number of detector mismatches inside NAB anomaly windows
~~~

Null model:

> choose exactly `n` distinct scored timestamps uniformly at random from the `N` scored timestamps.

Then:

~~~text
X_null ~ Hypergeometric(N, K, n)
~~~

Compute exactly/deterministically:

- null mean precision;
- null p99 hit count;
- null p99 precision;
- one-sided tail probability P(X_null >= X).

## Frozen primary scientific gate

A positive held-out detector replication requires both:

~~~text
observed_precision > null_p99_precision
one_sided_null_p < 0.01
~~~

No absolute recall gate is used.

This directly addresses the weakness identified in Experiment 011.

## Secondary frozen-pipeline replication

Without changing their code, attempt:

~~~text
Experiment 011 detector
→ Experiment 012 episode decomposition
→ Experiment 013 transition descriptors
→ Experiment 014 k=2 clusterer
~~~

If clustering succeeds, evaluate it using the **unchanged Experiment 014 gate**:

~~~text
each outside-only cluster >= 3 episodes
silhouette_score >= 0.35
centroid_distance >= 2.0
~~~

Secondary outcome may be:

~~~text
PASS
FAIL
NOT_EVALUABLE
~~~

It is not allowed to influence the primary detector verdict.

## Reproducibility vs scientific result

~~~text
CI PASS
≠
PRIMARY SCIENTIFIC PASS
≠
SECONDARY STRUCTURAL PASS
~~~

CI PASS only means the preregistered process reproduced.

## Forbidden reinterpretation

After the first held-out result, do not change:

- held-out file;
- detector threshold;
- detector window;
- null model;
- primary p-value threshold;
- primary p99 criterion;
- episode rule;
- transition descriptors;
- cluster features;
- k;
- cluster gate.

Any change requires a new experiment.

## Relation to Noepedia

Experiment 017 remains in the **real-data instrumentation track**.

It does not validate the Noepedia relational core because the relational evaluator is not yet the mechanism producing the result.

A later experiment must re-enter the core by representing observations, expectations, mismatch events, provenance, and OPEN state as field relations consumed by explicit rule objects.
