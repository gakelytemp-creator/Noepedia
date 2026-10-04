# Experiment 018 — Real Observations Re-enter the Noepedia Relational Core

> **Status:** preregistered architecture-integration experiment.
>
> Experiment 018 is **not** an anomaly-detector validation experiment.

## Purpose

Experiments 011–017 were reclassified as a real-data instrumentation / exploration track.

Experiment 018 returns to the Noepedia core.

The question is:

> **Can real observations and detector outputs be represented as explicit field objects/relations with provenance and OPEN structure, then evaluated by the existing generic rule evaluator without embedding temperature or anomaly semantics in that evaluator?**

## Source

Experiment 018 reuses the pinned real sensor source from Experiment 011:

~~~text
NAB
realKnownCause/machine_temperature_system_failure.csv
~~~

It also reuses the unchanged Experiment 011 detector only as an **instrumentation adapter** that produces a real-data classification boundary.

No NAB anomaly labels are used in Experiment 018.

## Boundary between instrumentation and Noepedia core

Instrumentation stage:

~~~text
raw CSV
→ Experiment 011 detector
→ mismatch timestamps
~~~

Field-construction stage:

~~~text
real reading
+ detector classification
+ source row
+ timestamp
+ local expectation token
→ explicit Noepedia objects and relations
~~~

Noepedia-core stage:

~~~text
FIELD_INPUT.json
→ experiment_003/evaluator.py
→ CONSISTENT / FORMAL_MISMATCH
→ OPEN preserved
~~~

The evaluator receives no temperature values, no rolling-MAD code, no threshold, and no NAB label.

## Frozen task-specific cut

Build a deterministic 40-assessment cut:

~~~text
20 earliest detector mismatches
20 earliest scored non-mismatch controls
~~~

If fewer than 20 detector mismatches exist, the experiment is not evaluable.

The control points are selected from scored timestamps only, in chronological order, excluding all detector-mismatch timestamps.

## Field representation

For each selected timestamp create addressable objects:

~~~text
ASSESSMENT_i
MEASUREMENT_i
EXPECTATION_i
TIME_i
SOURCE_ROW_i
STATE_WITHIN_LOCAL_EXPECTATION
STATE_OUTSIDE_LOCAL_EXPECTATION
~~~

Relations include:

~~~text
ASSESSMENT_i → EXPECTED_STATE → STATE_WITHIN_LOCAL_EXPECTATION
ASSESSMENT_i → OBSERVED_STATE → STATE_...

ASSESSMENT_i → SUPPORTED_BY → MEASUREMENT_i
ASSESSMENT_i → DERIVED_FROM → EXPECTATION_i

MEASUREMENT_i → AT_TIME → TIME_i
MEASUREMENT_i → FROM_SOURCE_ROW → SOURCE_ROW_i
EXPECTATION_i → AT_TIME → TIME_i
EXPECTATION_i → BASED_ON_PREVIOUS_SAMPLES → WINDOW_288
~~~

The state relation is an adapter projection of the frozen detector result.

## Explicit rule object

Use the existing one-input generic evaluator grammar:

~~~text
RULE_SCOPE = assessment
INPUT_PREDICATE = EXPECTED_STATE
REQUIRED_PREDICATE = OBSERVED_STATE
TARGET_CONSTRAINT = SAME_NET
~~~

The evaluator therefore asks only:

> for this assessment, does the stored OBSERVED_STATE equal the explicitly required EXPECTED_STATE?

No temperature-specific branch is allowed.

## OPEN structure

Every detector-mismatch assessment creates an OPEN record:

~~~text
ASSESSMENT_i → CAUSE_OF_MISMATCH → UNKNOWN_CAUSE
~~~

The evaluator must preserve these OPEN records unchanged.

A mismatch event is not allowed to close or explain its cause.

## Frozen expected structural outcome

For the 40-assessment cut:

~~~text
20 detector mismatch assessments
→ 20 FORMAL_MISMATCH

20 detector non-mismatch controls
→ 20 CONSISTENT

20 OPEN cause records
→ all preserved unchanged
~~~

No repair event is permitted.

## Scientific/architectural claim boundary

A PASS supports only this claim:

> real observations can be projected into the Noepedia field so that the existing generic relational evaluator reproduces an externally supplied local expectation-vs-observation distinction while preserving provenance and unresolved causal OPENs.

It does **not** show:

- anomaly-detection superiority;
- held-out transfer;
- causal diagnosis;
- automated repair;
- that the rolling-MAD detector is part of the Noepedia core.

## Failure conditions

Experiment 018 fails if:

- the field builder cannot encode the real cut without ad hoc evaluator changes;
- evaluator event counts differ from the frozen 20/20 split;
- any OPEN cause record is altered or closed;
- evaluator code must inspect temperature values, threshold values, or human labels;
- provenance links are absent from the generated field.
