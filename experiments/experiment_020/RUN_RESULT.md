# Experiment 020 — Verified Third-Path Refinement Result

> **Status:** repository CI reproduction passed.
>
> **Architectural result:** PASS under the preregistered gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37185402992
job: verify
conclusion: success
head commit: c6790c8de45867ed3a8b443c70ed7371cacaf221
~~~

## Real source and paths

MetroPT-3, UCI DOI `10.24432/C5VW3R`.

~~~text
Path A: DV_eletric
Path B: Motor_current
Path C: TP2
~~~

No failure/anomaly labels were used.

## Independent calibrations

Path B and Path C were calibrated independently on the first 50,000 rows with deterministic one-dimensional k-means.

~~~text
Motor_current threshold = 2.1490460087555503
TP2 threshold           = 4.640123582876524
~~~

All three paths produced both frozen candidate states during the 5,000-row evaluation cut.

## Field and rule structure

For each assessment the field stored:

~~~text
DIGITAL_CANDIDATE_STATE
CURRENT_CANDIDATE_STATE
PRESSURE_CANDIDATE_STATE
~~~

with separate provenance.

The existing frozen evaluator applied three explicit field rules:

~~~text
AB: digital vs current
AC: digital vs pressure
BC: current vs pressure
~~~

The input field contained no mismatch, consistency, agreement, support, anomaly, fault, or normality verdict.

## Result

Rule AB reproduced the Experiment 019 disagreement count:

~~~text
AB FORMAL_MISMATCH = 1165
~~~

Among those 1,165 disagreements, the third independent pressure relation produced:

~~~text
PRESSURE_SUPPORTS_DIGITAL_SIDE = 1163
PRESSURE_SUPPORTS_CURRENT_SIDE =    2

digital-side support fraction = 0.9982832618
current-side support fraction = 0.0017167382
~~~

Every AB mismatch fell into exactly one of the two preregistered third-path structural classes.

Both classes occurred at least once.

The interpretation OPEN remained unchanged.

## Architectural interpretation

Experiment 020 demonstrates a stronger relational refinement than Experiment 019:

~~~text
Path A and Path B disagree
+
independent Path C
+
three explicit field rules
↓
core-derived structural subclass of the disagreement
~~~

The dominant pattern is extremely asymmetric: TP2 agrees with the digital `DV_eletric` state in 1,163 of the 1,165 cases where `DV_eletric` and Motor_current disagree.

That asymmetry is a real structural observation in the frozen cut.

## What this does not mean

The result does **not** prove that the digital path is correct and Motor_current is wrong.

Possible explanations remain open, including:

- Motor_current state mapping is too coarse;
- current changes lag or lead valve/pressure state;
- TP2 and DV_eletric encode more tightly coupled aspects of loaded operation;
- transient operating states are collapsed by the binary representation.

Therefore:

~~~text
PRESSURE_SUPPORTS_DIGITAL_SIDE
≠ digital truth
≠ motor-current fault
≠ anomaly
~~~

## Important methodological consequence

The next useful experiment should not simply add a fourth vote.

The 99.8% asymmetry gives a much sharper OPEN:

> **Are the 1,163 digital+pressure vs current disagreements concentrated near state transitions, as expected from normal motor-current lag/lead, or do persistent disagreements remain far from transitions?**

That question can be tested using explicit temporal relations while keeping the physical interpretation OPEN.