# Experiment 052 — End-to-End Revision Pipeline

Purpose:
validate the reusable `core/revision/pipeline.py` end to end.

The pipeline must connect:
- structural candidate generation;
- candidate ranking;
- null selection;
- preregistration template creation;
- generic parameter search/evaluation;
- gate-case construction;
- PROMOTE / REJECT / REMAIN_OPEN decision;
- append-only graph materialization.

Validation cases:
- strong temporal structure -> PROMOTE -> one new rule version;
- unknown structure -> OPEN_DECOMPOSITION -> REMAIN_OPEN -> no invented rule.
