# Experiment 060 — Meta-Policy Self-Audit / Strategy Learning

Purpose:
validate evidence-based self-audit of strategy outcomes without directly mutating the live meta-policy.

Component:
`core/revision/meta_audit.py`

The audit consumes prior strategy-run records containing:
- strategy_name
- decision
- graph_valid
- optional profile_class
- optional run_id

Audit outputs:
- per-strategy outcome summary
- KEEP / REVIEW recommendations
- META_POLICY_CANDIDATE proposals
- explicit `policy_mutated = false`

Pass criteria:
- well-performing strategy is kept;
- insufficient-sample strategy is not changed;
- low-promotion/high-REMAIN_OPEN strategy becomes a candidate for boundary review;
- candidate proposal requires preregistered confirmation;
- live policy is never mutated by the audit.
