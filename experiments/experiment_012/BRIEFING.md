# Experiment 012 — Label-Blind Temporal Decomposition of Real-Data Mismatches

> **Status:** preregistered real-data follow-up to Experiment 011.

## Motivation

Experiment 011 produced:

~~~text
967 total FORMAL_MISMATCH events
268 inside NAB anomaly windows
699 outside NAB anomaly windows
~~~

The next question is not whether to retune the detector.

The next question is:

> **Are the mismatch events structurally organized into coherent temporal episodes, or are they mostly isolated points?**

Experiment 012 keeps the Experiment 011 detector unchanged.

## Epistemic boundary

The decomposition stage is label-blind.

It receives only Experiment 011 mismatch events and their local statistics.

It does **not** receive NAB anomaly windows.

Labels are loaded only after `EPISODES.json` has been written.

Therefore the experiment separates:

~~~text
mismatch detection
→ label-blind structural decomposition
→ later ground-truth comparison
~~~

## Frozen episode rule

Mismatch events are sorted by timestamp.

Two consecutive mismatch events belong to the same episode when:

~~~text
time_gap <= 30 minutes
~~~

Otherwise a new episode begins.

No value threshold is added beyond the frozen Experiment 011 detector.

## Frozen episode descriptors

For each episode record:

- episode ID;
- start timestamp;
- end timestamp;
- mismatch count;
- duration minutes;
- mean robust-z;
- maximum robust-z;
- positive-residual count;
- negative-residual count;
- sign class.

Signed residual is reconstructed from the Experiment 011 event:

~~~text
residual = observed_value - trailing_median
~~~

Sign class:

~~~text
HOT   if positive_fraction >= 0.80
COLD  if negative_fraction >= 0.80
MIXED otherwise
~~~

These labels are descriptive only.

## External evaluation

Only after episodes are frozen, load NAB anomaly windows.

Each episode is then classified as:

~~~text
OVERLAPS_LABEL
OUTSIDE_LABEL
~~~

For outside-label mismatch points calculate:

- total outside-label mismatch points;
- number of outside-only episodes;
- number of isolated outside episodes (1 mismatch);
- number of persistent outside episodes (>= 6 mismatches);
- fraction of outside-label mismatch points contained in persistent episodes;
- maximum duration of any outside-only episode;
- top-10 outside-episode concentration.

## Preregistered scientific gate

Experiment 012 counts as a positive structural result when both are true:

~~~text
persistent_outside_fraction >= 0.50
max_outside_episode_duration_minutes >= 60
~~~

Interpretation of a PASS is narrow:

> at least half of the outside-label mismatch points participate in multi-event temporal structures, and at least one outside-only structure persists for at least one hour.

This does **not** mean those episodes are real anomalies.

## Forbidden reinterpretation

If the gate fails:

- do not change the 30-minute gap;
- do not change the >=6-event persistence definition;
- do not change the Experiment 011 detector.

Any changed decomposition becomes a later experiment.

## What this experiment does not test

It does not determine whether outside-label episodes are:

- false positives;
- unlabeled faults;
- normal operating regimes;
- sensor artifacts;
- maintenance periods.

It tests only whether the unexplained mismatches have temporal structure.

## OPEN produced by the experiment

If coherent outside-label episodes exist, the next OPEN is:

> **Which additional relation or measurement would discriminate detector error from a real but unlabeled regime change?**
