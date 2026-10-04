# Experiment 019 — Verified Cross-Path Real-Data Core Inference

> **Status:** repository CI reproduction passed.
>
> **Architectural result:** PASS under the preregistered gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37184455722
job: verify
conclusion: success
head commit: 69085275bb40c9ed0706845be09b6a4ecca85861
~~~

## Real source

MetroPT-3, UCI DOI `10.24432/C5VW3R`.

Used channels:

~~~text
Path A: DV_eletric
Path B: Motor_current
~~~

No failure/anomaly labels were used.

## Independent path construction

Path A used only the documented binary `DV_eletric` state:

~~~text
1 → STATE_LOADED
0 → STATE_NOT_LOADED
~~~

Path B used only `Motor_current`.

The first 50,000 rows were used for deterministic one-dimensional k-means calibration (`k=2`). The resulting midpoint threshold was:

~~~text
Motor_current threshold = 2.1490460087555503
~~~

The next 5,000 rows were used for evaluation.

Both paths produced both candidate states, so the experiment was evaluable.

## Field construction

The input field contained, for every assessment:

~~~text
ASSESSMENT_i → DIGITAL_CANDIDATE_STATE → STATE_*
ASSESSMENT_i → ANALOG_CANDIDATE_STATE  → STATE_*
~~~

Each relation carried separate channel/source-row provenance.

The input field contained no `MISMATCH`, `CONSISTENT`, or `AGREEMENT` verdict.

Generated field size:

~~~text
evaluation assessments   5000
stored relations        35005
OPEN records                1
~~~

## Explicit core rule

~~~text
RULE_SCOPE = assessment
INPUT_PREDICATE = DIGITAL_CANDIDATE_STATE
REQUIRED_PREDICATE = ANALOG_CANDIDATE_STATE
TARGET_CONSTRAINT = SAME_NET
~~~

The evaluator itself remained the frozen `experiment_003/evaluator.py` blob preregistered in `SOURCE.json`.

## Evaluator result

~~~text
CONSISTENT        3835
FORMAL_MISMATCH   1165

total             5000
mismatch fraction 0.233
~~~

Every FORMAL_MISMATCH was verified to combine:

~~~text
one DIGITAL_CANDIDATE_STATE relation
+
one conflicting ANALOG_CANDIDATE_STATE relation
~~~

with the expected independent provenance paths.

The structural OPEN concerning the domain validity of the cross-path mapping was preserved unchanged.

## Architectural interpretation

Experiment 019 is the first real-data experiment in this series where the core output is **not copied from either instrumentation path**.

Neither Path A nor Path B asserts disagreement.

Instead:

~~~text
real digital evidence
+
real analog evidence
+
explicit relational consistency rule
↓
core-derived CONSISTENT / FORMAL_MISMATCH
~~~

This supports the narrow claim that Noepedia can add a new **relational consistency distinction** by combining two independently constructed real-data relations.

## What the 23.3% mismatch fraction does not mean

The 1,165 mismatches are **not** established faults, anomalies, or errors.

`DV_eletric` and Motor_current encode related but not necessarily perfectly synchronous physical aspects of the APU. The explicit mapping rule is itself still represented as epistemically open.

Therefore:

~~~text
FORMAL_MISMATCH
≠ fault
≠ anomaly
≠ proof that either channel is wrong
~~~

It means only that the two explicit candidate-state relations disagree under the frozen rule.

## Why this is stronger than Experiment 018

Experiment 018:

~~~text
one adapter verdict
→ field
→ evaluator restates equality / inequality
~~~

Experiment 019:

~~~text
Path A produces state A
Path B independently produces state B
neither produces a verdict
→ field rule combines them
→ evaluator creates the verdict
~~~

So the information-gain test that was not performed in Experiment 018 is performed here, in the limited structural sense defined above.

## Next OPEN

The next question is no longer whether the core can generate a cross-source mismatch.

It can.

The next question is:

> **Do the core-derived mismatches organize into reproducible physical contexts, and can additional independent relations discriminate normal transition lag from genuinely unusual disagreement without hiding that semantics in Python?**