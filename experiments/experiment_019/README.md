# Experiment 019 — Cross-Path Real-Data Core Inference

Experiment 019 tests whether the Noepedia core can create a cross-source consistency verdict that neither real-data input path asserts directly.

Real source: MetroPT-3.

~~~text
DV_eletric path ─────────────┐
                            ├→ Noepedia explicit consistency rule → CONSISTENT / FORMAL_MISMATCH
Motor_current path ──────────┘
~~~

Path A never reads Motor_current.

Path B calibrates and classifies from Motor_current only and never reads DV_eletric.

Failure/anomaly labels are not used.

## Run

~~~bash
python experiments/experiment_019/run_experiment.py
~~~

Success means the existing generic evaluator produces both agreement and disagreement events from the combination of two independently constructed relations, while the input field itself contains no mismatch/consistency verdict.