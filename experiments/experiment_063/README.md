# Experiment 063 — Regression Watch and Versioned Rollback

Purpose: monitor a newly active meta-policy against a frozen prior baseline and create rollback only as a new version when preregistered degradation gates are crossed.

Pass criteria:
- clear regression is detected;
- rollback is authorized only on confirmed regression;
- rollback creates META_POLICY_V3 rather than overwriting V2;
- V1 and V2 remain preserved in history;
- stable V2 does not rollback;
- insufficient sample remains NOT_EVALUABLE.
