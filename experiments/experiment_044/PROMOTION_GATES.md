# Experiment 044 — Promotion Gates

## Status

`PROMOTION_GATES_SPECIFICATION_COMPLETE`

Experiment 044 defines the mandatory and optional gates that control transitions from RULE_CANDIDATE to:

`EMPIRICALLY_SUPPORTED_RULE`
`REJECTED_CANDIDATE`
`REMAIN_OPEN`

This specification builds directly on:
- Experiment 042 — Revision Protocol
- Experiment 043 — Core Revision Data Model

---

## 1. Promotion principle

A candidate rule is not promoted because it fits discovery data better.

Promotion requires a complete, preregistered, provenance-bearing confirmation path.

Canonical decision sequence:

`CANDIDATE`
`-> GATE CHECKS`
`-> CONFIRMATION`
`-> NULL CHECKS`
`-> DECISION`

Allowed final decisions:

`PROMOTE`
`REJECT`
`REMAIN_OPEN`

---

## 2. Gate classes

Promotion gates are divided into four classes:

`A. STRUCTURAL GATES`
`B. EVIDENCE GATES`
`C. CONFIRMATION GATES`
`D. GOVERNANCE / HISTORY GATES`

Mandatory gates must all pass.

Optional domain-specific gates may be added but may not weaken mandatory gates.

---

## 3. Gate A1 — Parent rule exists

Requirement:

`RULE_CANDIDATE PARENT_RULE -> RULE`

Failure result:

`REMAIN_OPEN`

Reason:

`MISSING_PARENT_RULE`

No candidate may be promoted without an explicit prior rule or prior relation state.

---

## 4. Gate A2 — OPEN exists

Requirement:

`RULE_CANDIDATE ADDRESSES_OPEN -> OPEN`

Failure result:

`REMAIN_OPEN`

Reason:

`MISSING_OPEN_CONTEXT`

Promotion must resolve or refine a known uncertainty, not create an untracked rule mutation.

---

## 5. Gate A3 — Complete provenance path

Required path:

`PARENT_RULE`
`-> FORMAL_MISMATCH`
`-> OPEN`
`-> EVIDENCE`
`-> RULE_CANDIDATE`
`-> PREREGISTRATION_RECORD`
`-> CONFIRMATION_RESULT`
`-> PROMOTION_DECISION`

Failure result:

`REMAIN_OPEN`

Reason:

`PROMOTION_PATH_INCOMPLETE`

---

## 6. Gate A4 — Candidate parameters explicit

All discovery-selected parameters must be stored as graph relations or immutable candidate fields.

Examples:

`PARAMETER_LAG_ROWS`
`PARAMETER_DIRECTION`
`PARAMETER_THRESHOLD`
`PARAMETER_CHANNEL`
`PARAMETER_RELATION_ORIENTATION`

Failure result:

`REMAIN_OPEN`

Reason:

`HIDDEN_OR_UNRECORDED_PARAMETER`

---

## 7. Gate A5 — Preregistration frozen

Required:

`PREREGISTRATION_RECORD status = FROZEN`

and it must freeze:

- confirmation window;
- candidate parameters;
- primary metric;
- null models;
- pass/fail criteria;
- evaluator snapshot;
- tie-breaking rules;
- claim boundary.

Failure result:

`REMAIN_OPEN`

Reason:

`PREREGISTRATION_INCOMPLETE`

---

## 8. Gate B1 — Discovery / confirmation separation

Requirement:

`DISCOVERY_WINDOW != CONFIRMATION_WINDOW`

for the same candidate.

Failure result:

`REJECT`

Reason:

`DISCOVERY_CONFIRMATION_LEAKAGE`

Exception:

None for confirmatory promotion.

---

## 9. Gate B2 — Untouched confirmation

Confirmation data must not have been used for:

- parameter tuning;
- candidate selection;
- channel selection;
- threshold selection;
- model selection;
- rule-shape selection.

Failure result:

`REJECT`

Reason:

`CONFIRMATION_NOT_UNTOUCHED`

---

## 10. Gate B3 — Evidence role explicit

Evidence objects must be labeled at least as one of:

`EXPLORATORY`
`CONFIRMATORY`
`REPLICATED`
`FAILED_TO_REPLICATE`

Failure result:

`REMAIN_OPEN`

Reason:

`EVIDENCE_ROLE_UNCLEAR`

---

## 11. Gate C1 — Confirmation evaluable

Confirmation must satisfy all preregistered evaluability conditions.

Examples:

- minimum sample count;
- minimum event count;
- required classes present;
- evaluator executed successfully;
- required metrics computable;
- required nulls computable.

If not:

`REMAIN_OPEN`

Reason:

`NOT_EVALUABLE`

Important:

`NOT_EVALUABLE != REJECTED`

---

## 12. Gate C2 — Revised rule improves primary metric

Requirement:

The revised rule must outperform the parent rule according to the preregistered primary metric.

Examples:

`revised_mismatch_fraction < old_mismatch_fraction`

or another domain-specific frozen metric.

Failure result:

`REJECT`

Reason:

`NO_PRIMARY_METRIC_IMPROVEMENT`

---

## 13. Gate C3 — Minimum effect gate

Optional by default, mandatory if preregistered.

Examples:

`relative mismatch reduction >= 0.10`
`effect size >= frozen threshold`

If a minimum effect threshold was preregistered and not met:

`REJECT`

Reason:

`EFFECT_TOO_SMALL`

---

## 14. Gate C4 — Required null models passed

If null models were preregistered, all required null gates must pass.

Examples:

`revised_error <= 0.90 * majority_null_error`

`revised_error <= 0.90 * permutation_null_error`

Failure result:

`REJECT`

Reason:

`NULL_NOT_BEATEN`

Important lesson:

Experiments 036–038 demonstrate that beating the old rule without beating nulls is insufficient.

---

## 15. Gate C5 — Search-boundary safety

If candidate parameters are selected from a bounded search grid, boundary optima must be handled explicitly.

Possible preregistered policies:

`BOUNDARY_HIT -> REJECT`

or

`BOUNDARY_HIT -> REMAIN_OPEN`

Default policy:

`REMAIN_OPEN`

Reason:

`SEARCH_BOUNDARY_UNRESOLVED`

unless a wider search has already resolved the boundary.

---

## 16. Gate C6 — Residual unresolved rows not counted as success

Rows/events explicitly marked unresolved must not be included as successful matches.

Examples:

`TRANSITION_OPEN`
`MID_UNRESOLVED`

Failure result:

`REJECT`

Reason:

`UNRESOLVED_COUNTED_AS_SUCCESS`

Reference:
Experiment 033 transition-zone discipline.

---

## 17. Gate C7 — Direction consistency

If the preregistered claim includes an expected direction, confirmation must not reverse it.

Failure result:

`REJECT`

Reason:

`DIRECTION_REVERSED`

Reference:
Experiment 029.

---

## 18. Gate C8 — No degradation against simpler valid rule

If a simpler preregistered baseline performs equally or better, the candidate cannot be promoted.

Failure result:

`REJECT`

Reason:

`SIMPLER_RULE_NOT_BEATEN`

This is distinct from generic null failure when the comparator is a meaningful simpler model.

---

## 19. Gate D1 — Evaluator identity frozen

Required:

`PREREGISTRATION_RECORD EVALUATOR_SNAPSHOT -> EVALUATOR_SNAPSHOT`

and evaluator code hash must match at confirmation.

If execution fails because of implementation incompatibility:

`REMAIN_OPEN`

Reason:

`EVALUATOR_INCOMPATIBLE`

An implementation-only correction may be allowed if:

- semantics unchanged;
- criteria unchanged;
- data unchanged;
- parameters unchanged;
- correction recorded explicitly.

Reference:
Experiment 033 correction.

---

## 20. Gate D2 — Corrections documented

Any post-freeze implementation or interpretation correction must exist as a CORRECTION object/file.

If an undocumented correction affects execution or interpretation:

`REMAIN_OPEN`

Reason:

`UNDOCUMENTED_CORRECTION`

---

## 21. Gate D3 — Historical records preserved

Promotion or rejection must not overwrite:

- parent rule;
- rejected candidates;
- earlier result;
- prior correction;
- OPEN history.

Failure result:

`REMAIN_OPEN`

Reason:

`HISTORY_NOT_PRESERVED`

---

## 22. Gate D4 — OPEN refinement prepared

A promotion decision must specify:

`RESOLVED_COMPONENT`
`REMAINING_COMPONENT`

A rejection decision must specify:

`REJECTED_COMPONENT`
`REMAINING_COMPONENT`

If no OPEN refinement can be represented:

`REMAIN_OPEN`

Reason:

`OPEN_REFINEMENT_UNSPECIFIED`

---

## 23. Promotion decision table

### PROMOTE

All mandatory structural, evidence, confirmation, null, and governance gates pass.

Output:

`PROMOTION_DECISION = PROMOTE`

Then create:

`EMPIRICALLY_SUPPORTED_RULE`

and link:

`PROMOTED_FROM -> RULE_CANDIDATE`
`DERIVED_FROM_RULE -> PARENT_RULE`
`SUPPORTED_BY -> CONFIRMATION_RESULT`
`PREREGISTERED_BY -> PREREGISTRATION_RECORD`

---

## 24. Rejection decision table

Use `REJECT` when the candidate has been fairly tested and fails scientific gates.

Typical reasons:

`NO_PRIMARY_METRIC_IMPROVEMENT`
`NULL_NOT_BEATEN`
`DIRECTION_REVERSED`
`DEGRADED_PERFORMANCE`
`SIMPLER_RULE_NOT_BEATEN`
`DISCOVERY_CONFIRMATION_LEAKAGE`

Output:

`REJECTED_CANDIDATE`

Candidate remains connected to:

`PARENT_RULE`
`OPEN`
`CONFIRMATION_RESULT`
`REJECTION_REASON`

---

## 25. REMAIN_OPEN decision table

Use `REMAIN_OPEN` when evidence is insufficient to make a scientific rejection or promotion.

Typical reasons:

`NOT_EVALUABLE`
`MISSING_OPEN_CONTEXT`
`PROMOTION_PATH_INCOMPLETE`
`PREREGISTRATION_INCOMPLETE`
`SEARCH_BOUNDARY_UNRESOLVED`
`EVALUATOR_INCOMPATIBLE`
`INSUFFICIENT_SAMPLE`
`REQUIRED_NULL_UNAVAILABLE`

Important:

`REMAIN_OPEN != FAILURE`

It means:

> no justified epistemic transition is available yet.

---

## 26. Default mandatory gate set

Unless a domain explicitly adds stricter conditions, promotion requires all:

`A1 Parent rule exists`
`A2 OPEN exists`
`A3 Complete provenance path`
`A4 Candidate parameters explicit`
`A5 Preregistration frozen`
`B1 Discovery/confirmation separated`
`B2 Confirmation untouched`
`B3 Evidence role explicit`
`C1 Confirmation evaluable`
`C2 Revised rule improves primary metric`
`C4 Required nulls passed`
`C6 Unresolved not counted as success`
`D1 Evaluator identity frozen`
`D2 Corrections documented`
`D3 Historical records preserved`
`D4 OPEN refinement prepared`

Domain-specific gates may add:

`C3 Minimum effect`
`C5 Search-boundary rule`
`C7 Direction consistency`
`C8 Simpler-rule comparison`

---

## 27. Gate result object

Every promotion attempt should produce a gate audit object:

`PROMOTION_GATE_AUDIT`

Minimum structure:

`{`
`  candidate_id,`
`  gates: [`
`    {gate_id, status, evidence, reason},`
`    ...`
`  ],`
`  final_decision,`
`  decision_reason`
`}`

Allowed gate statuses:

`PASS`
`FAIL`
`NOT_APPLICABLE`
`NOT_EVALUABLE`

---

## 28. Exact candidate-to-rule transition

Candidate promotion must create a new rule object.

Example:

`RULE_X_V1`
`-> candidate CAND_X_01`
`-> PROMOTION_DECISION = PROMOTE`
`-> RULE_X_V2`

Relations:

`RULE_X_V2 DERIVED_FROM_RULE RULE_X_V1`
`RULE_X_V2 PROMOTED_FROM CAND_X_01`
`RULE_X_V1 SUPERSEDED_BY RULE_X_V2`

Never mutate RULE_X_V1 in-place.

---

## 29. Promotion status is not truth status

`EMPIRICALLY_SUPPORTED_RULE` means:

> this rule passed the specified evidence, confirmation, and null gates in the tested domain.

It does not mean:

`FACT`
`CAUSAL_LAW`
`UNIVERSAL_RULE`
`CERTAIN_TRUTH`

Domain transfer requires new evidence.

---

## 30. Negative promotion examples

### Experiment 035

Candidate residual pattern failed generalization.

Decision:
`REJECT`

Reason:
`INSUFFICIENT_TRANSFER / EFFECT_TOO_SMALL`

### Experiment 038

Candidates beat old rules but not nulls.

Decision:
`REJECT`

Reason:
`NULL_NOT_BEATEN`

### Experiment 039

Discovery revision degraded confirmation.

Decision:
`REJECT`

Reason:
`DEGRADED_PERFORMANCE`

---

## 31. Positive promotion examples

### Experiment 033

Promotion supported because:

- complete mismatch-to-OPEN path;
- replicated temporal evidence;
- frozen revised rule;
- untouched confirmation;
- unresolved transition zone not counted as success;
- very large improvement;
- correction documented;
- provenance preserved.

### Experiment 040

Promotion supported because:

- family selection frozen on calibration only;
- discovery/confirmation separated;
- lag minimum interior to search grid;
- revised rule strongly beat old rule;
- revised rule strongly beat majority null;
- revised rule strongly beat permutation null;
- all preregistered gates passed.

---

## 32. Core invariant

Noepedia must never perform this transition:

`candidate looks good -> overwrite rule`

The only valid transition is:

`candidate`
`-> audited gates`
`-> explicit decision`
`-> new versioned rule OR rejected candidate OR remain-open state`

---

## 33. Final promotion rule

Canonical shorthand:

`PROMOTE = COMPLETE_PATH + FROZEN_TEST + UNTOUCHED_CONFIRMATION + REQUIRED_NULLS_PASS + HISTORY_PRESERVED + OPEN_REFINED`

`REJECT = FAIR_TEST_PERFORMED + SCIENTIFIC_GATE_FAILED`

`REMAIN_OPEN = DECISION_NOT_YET_JUSTIFIED`

---

## Next step

Experiment 045 should specify and implement the Automated Revision Harness:

- ingest mismatch/Open/candidate records;
- validate preregistration;
- run frozen evaluator;
- compute required nulls;
- emit PROMOTION_GATE_AUDIT;
- create PROMOTE / REJECT / REMAIN_OPEN decision records;
- never mutate historical rules in-place.