# Experiment 051 — Remaining Evaluator Plugins

Purpose: validate generic evaluators for RELATION_ORIENTATION_REVISION, LOCAL_EXCEPTION_CANDIDATE, and SIMPLER_RULE_COMPARATOR.

Pass criteria:
- orientation selected on discovery only and frozen on confirmation;
- local exception replication threshold distinguishes replicate vs weak-transfer cases;
- simpler-rule comparator detects when a proposed rule fails to beat majority baseline;
- outputs expose metrics usable by the common gate engine.
