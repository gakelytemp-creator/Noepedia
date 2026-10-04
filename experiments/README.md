# Noepedia Experiments

This directory contains the executable and archived experiment sequence.

## Sequence

- [Experiment 001](experiment_001/) — first synthetic dry-run; candidate mismatch and structural OPENs
- [Experiment 002](experiment_002/) — explicit terminal granularity and consistency rule
- [Experiment 003](experiment_003/) — deterministic detection-only evaluator
- [Experiment 004](experiment_004/) — multiple rules under one grammar
- [Experiment 005](experiment_005/) — two-input same-subject antecedent
- [Experiment 006](experiment_006/) — cross-subject shared-object join
- [Experiment 007](experiment_007/) — derived relation consumed by a later rule
- [Experiment 008](experiment_008/) — multi-round derived-relation closure
- [Experiment 009](experiment_009/) — branching and explicit competition
- [Experiment 010](experiment_010/) — evidence-driven branch discrimination without branch deletion

See [Experiments 001–009 — State of Evidence](../EXPERIMENTS_001_009_SUMMARY.md) for the consolidated claim/evidence/limitation view.

## Reproduction

Experiments 004 onward include automatic verifiers and are included in the repository GitHub Actions workflow.

The audit rule is:

~~~text
frozen input
+ frozen expectation
+ committed evaluator
→ independent verifier
→ PASS / FAIL
~~~

Corrections after observing a run must be recorded explicitly rather than silently rewriting history.

- [Experiment 011](experiment_011/) — first external real sensor trace with label-blind deterministic detection

- [Experiment 012](experiment_012/) — label-blind temporal decomposition of real-data mismatches

- [Experiment 013](experiment_013/) — label-blind PRE/POST baseline transition test for outside-only COLD episodes

- [Experiment 014](experiment_014/) — deterministic label-blind clustering of COLD episode structure

- [Experiment 015](experiment_015/) — label-blind time-of-day context test for the two COLD families

- [Experiment 016](experiment_016/) — label-blind pre-onset drift comparison between the two COLD families

- [Experiment 017](experiment_017/) — one-shot held-out NAB replication with exact matched-count null baseline

Methodology note for Experiments 011–016: [Real-Data Instrumentation Track Status](../REAL_DATA_TRACK_STATUS.md).

- [Experiment 018](experiment_018/) — real observations projected into the relational field and evaluated by the existing Noepedia core evaluator

- [Experiment 019](experiment_019/) — MetroPT-3 two-path real-data consistency inference inside the Noepedia core

- [Experiment 020](experiment_020/) — third independent MetroPT-3 relation refines core-derived disagreement into structural support subclasses
