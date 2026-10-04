# Experiment 019 — Cross-Path Real-Data Inference in the Noepedia Core

> **Status:** preregistered real-data core-inference experiment.

## Purpose

Experiment 018 proved plumbing: one external detector verdict could be represented in the field and checked by the generic evaluator.

Experiment 019 asks the stronger question:

> **Can two independent real evidence paths enter the field without asserting mismatch, and can the generic evaluator derive agreement or mismatch only by combining them with an explicit rule object?**

## Real multichannel source

MetroPT-3, UCI DOI `10.24432/C5VW3R`.

The source contains analog and digital telemetry from a Metro do Porto train Air Production Unit.

Experiment 019 uses only:

~~~text
Path A: DV_eletric      (digital control/state channel)
Path B: Motor_current   (analog motor-current channel)
~~~

No failure labels or anomaly annotations are used.

## Independence boundary

### Path A — documented digital state

Published source semantics describe `DV_eletric` as active while the compressor operates under load.

Frozen mapping:

~~~text
DV_eletric = 1 → STATE_LOADED
DV_eletric = 0 → STATE_NOT_LOADED
~~~

Path A uses no Motor_current values.

### Path B — analog state derived without DV_eletric

Use the first 50,000 rows as a calibration prefix.

Fit deterministic 1-D k-means with `k=2` to `Motor_current` only:

~~~text
initial centroids = min and max calibration Motor_current
distance = absolute distance
maximum iterations = 100
low centroid  → STATE_NOT_LOADED
high centroid → STATE_LOADED
threshold = midpoint of final centroids
~~~

Path B uses no DV_eletric values during calibration or classification.

## Evaluation cut

After the 50,000-row calibration prefix, use the next 5,000 rows in source order.

For each row, create two candidate-state relations:

~~~text
ASSESSMENT_i → DIGITAL_CANDIDATE_STATE → STATE_*
ASSESSMENT_i → ANALOG_CANDIDATE_STATE  → STATE_*
~~~

Neither path may emit `MISMATCH`, `CONSISTENT`, `AGREEMENT`, or any equivalent verdict.

## Explicit Noepedia rule

The field contains the rule object:

~~~text
RULE_SCOPE = assessment
INPUT_PREDICATE = DIGITAL_CANDIDATE_STATE
REQUIRED_PREDICATE = ANALOG_CANDIDATE_STATE
TARGET_CONSTRAINT = SAME_NET
~~~

The generic evaluator therefore performs the cross-path comparison.

## Provenance

Each candidate-state relation must preserve independent provenance:

~~~text
digital path provenance
→ SOURCE_CHANNEL_DV_ELETRIC
→ source row

analog path provenance
→ SOURCE_CHANNEL_MOTOR_CURRENT
→ source row
→ MOTOR_CURRENT_CALIBRATION_MODEL
~~~

## Frozen evaluability gate

The run is `NOT_EVALUABLE` if any of these is false:

- exactly 5,000 evaluation assessments are built;
- Path A produces both candidate states at least once;
- Path B produces both candidate states at least once;
- the calibration centroids are distinct;
- no input relation/object asserts mismatch or consistency.

## Frozen architectural success gate

If evaluable, PASS requires:

~~~text
CONSISTENT count + FORMAL_MISMATCH count = 5000
CONSISTENT count > 0
FORMAL_MISMATCH count > 0
all FORMAL_MISMATCH events combine one digital-path relation
with one analog-path relation
all input OPEN records are preserved unchanged
~~~

## What PASS means

A PASS supports the narrow claim:

> **A new cross-source consistency distinction can be produced inside the Noepedia core from two independently constructed real-data relations plus an explicit field rule, even though neither input path asserts the verdict itself.**

This is information addition by explicit rule application, not proof of superior anomaly detection or causal diagnosis.

## OPEN

The field carries one explicit structural OPEN:

~~~text
RULE019 → DOMAIN_VALIDITY_OF_CROSS_PATH_MAPPING → UNKNOWN_VALIDITY
~~~

The evaluator must preserve it unchanged.

Even if the two paths disagree, Experiment 019 does not decide which path is correct.