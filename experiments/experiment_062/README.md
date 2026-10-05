# Experiment 062 — Confirmed Meta-Policy Application Gate

Purpose: verify that only a confirmed selector change can be applied, and that application creates a new version instead of overwriting the current meta-policy.

Pass criteria:
- confirmed candidate is authorized;
- new meta-policy version is created;
- previous version is preserved and linked by SUPERSEDED_BY / DERIVED_FROM_META_POLICY;
- unconfirmed candidate is blocked;
- history is never mutated in place.
