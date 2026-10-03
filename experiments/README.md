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
