# Experiment 043 — Core Data Model for Revision

## Status

`DATA_MODEL_SPECIFICATION_COMPLETE`

Experiment 043 does not add executable code.

It formalizes the object and relation model required to implement the Revision Protocol defined in Experiment 042.

---

## 1. Design goal

The Noepedia core must represent revision as explicit graph structure rather than hidden procedural state.

Every step in the revision lifecycle must be inspectable through stored objects and relations.

The model must preserve:

- provenance;
- failed candidates;
- corrections;
- preregistration;
- null models;
- OPEN refinement;
- promotion history;
- immutable historical states.

---

## 2. First-class object types

The core revision subsystem defines the following first-class object types:

`RULE`
`FORMAL_MISMATCH`
`OPEN`
`EVIDENCE`
`RULE_CANDIDATE`
`PREREGISTRATION_RECORD`
`NULL_MODEL`
`CONFIRMATION_RUN`
`CONFIRMATION_RESULT`
`CORRECTION`
`EMPIRICALLY_SUPPORTED_RULE`
`REJECTED_CANDIDATE`
`OPEN_REFINEMENT`
`PROMOTION_DECISION`
`EVALUATOR_SNAPSHOT`
`DATA_WINDOW`

These are semantic object classes, not necessarily separate storage tables.

---

## 3. RULE object

### Required fields

`id`
`type = RULE`
`status`
`created_at`
`created_by`

### Required relations

`RULE_DEFINITION`
`RULE_SCOPE`
`INPUT_PREDICATE` or equivalent rule grammar
`EPISTEMIC_STATUS`
`PROVENANCE`

### Allowed epistemic statuses

`ASSUMED_RULE`
`EMPIRICALLY_SUPPORTED_RULE`
`REJECTED_RULE`
`DEPRECATED_RULE`
`SUPERSEDED_RULE`

### Constraint

`type` and `EPISTEMIC_STATUS` are separate.

Executable grammar type must never be overloaded with epistemic status.

Reference lesson:
Experiment 033 execution correction.

---

## 4. FORMAL_MISMATCH object

A formal mismatch must be materializable as a first-class object.

### Required relations

`TRIGGERED_BY_RULE -> RULE`
`ABOUT_SUBJECT -> subject object`
`EXPECTED_TARGET -> object`
`OBSERVED_TARGET -> object`
`INPUT_RELATION -> relation id`
`CONFLICTING_RELATION -> relation id`
`EVALUATOR_SNAPSHOT -> snapshot id`

### Required status

`status = DETECTED`

### Constraint

A mismatch object does not assert physical falsity.

`FORMAL_MISMATCH != PHYSICAL_CONTRADICTION`

---

## 5. OPEN object

OPEN represents unresolved relation geometry.

### Required relations

`TRIGGERED_BY -> FORMAL_MISMATCH | OPEN_REFINEMENT`
`UNRESOLVED_PREDICATE -> predicate token`
`SCOPE -> object/network/domain`
`STATUS -> OPEN`
`PROVENANCE -> evidence/history`

### Optional relations

`PARENT_OPEN -> OPEN`
`RESOLVED_COMPONENT -> object`
`REMAINING_COMPONENT -> object`
`REJECTED_EXPLANATION -> RULE_CANDIDATE`

### Invariant

OPEN objects are not deleted when partially resolved.

OPEN is refined through child/refinement objects.

---

## 6. EVIDENCE object

Evidence is any stored observation or derived structure used in candidate formation.

### Evidence classes

`RAW_OBSERVATION`
`DERIVED_RELATION`
`TEMPORAL_PATTERN`
`STRUCTURAL_PATTERN`
`REPLICATION_RESULT`
`NEGATIVE_RESULT`
`NULL_RESULT`

### Required relations

`EVIDENCE_SOURCE`
`EVIDENCE_SCOPE`
`EVIDENCE_STATUS`
`PROVENANCE`

### Evidence statuses

`EXPLORATORY`
`CONFIRMATORY`
`REPLICATED`
`FAILED_TO_REPLICATE`

---

## 7. RULE_CANDIDATE object

A rule candidate is a proposed revision that has not yet earned promotion.

### Required relations

`PARENT_RULE -> RULE`
`ADDRESSES_OPEN -> OPEN`
`PROPOSED_CHANGE -> structured object or relation set`
`SUPPORTED_BY -> EVIDENCE`
`DISCOVERY_WINDOW -> DATA_WINDOW`
`CANDIDATE_STATUS -> PROPOSED`

### Required parameter representation

Every tuned parameter must be explicit.

Examples:

`PARAMETER_LAG_ROWS -> 40`
`PARAMETER_DIRECTION -> HIGH_TO_LOW`
`PARAMETER_THRESHOLD -> value`
`PARAMETER_CHANNEL -> channel id`

### Invariant

No parameter selected during discovery may be hidden in code only.

---

## 8. PREREGISTRATION_RECORD object

Preregistration freezes the candidate before confirmation.

### Required relations

`FREEZES_CANDIDATE -> RULE_CANDIDATE`
`CONFIRMATION_WINDOW -> DATA_WINDOW`
`PRIMARY_METRIC -> metric id`
`PASS_CRITERION -> criterion object`
`FAIL_CRITERION -> criterion object`
`REQUIRES_NULL_MODEL -> NULL_MODEL`
`EVALUATOR_SNAPSHOT -> EVALUATOR_SNAPSHOT`
`COMMIT_ID -> commit/hash`

### Required status

`status = FROZEN`

### Invariant

After status becomes FROZEN, semantic candidate parameters cannot change in-place.

Any change creates a new candidate/preregistration version.

---

## 9. NULL_MODEL object

Null models represent plausible trivial explanations.

### Null model types

`MAJORITY_STATE_NULL`
`PERMUTATION_NULL`
`TIME_SHIFT_NULL`
`RANDOMIZED_RELATION_NULL`
`SIMPLER_RULE_NULL`
`SHAM_TRANSITION_NULL`

### Required relations

`NULL_TYPE`
`TARGETS_FAILURE_MODE`
`PARAMETERS`
`FROZEN_BY -> PREREGISTRATION_RECORD`

### Example

`TARGETS_FAILURE_MODE -> CLASS_IMBALANCE`

or

`TARGETS_FAILURE_MODE -> TEMPORAL_ALIGNMENT_ARTIFACT`

---

## 10. DATA_WINDOW object

A data window must be first-class to preserve untouched-data claims.

### Required relations

`DATA_SOURCE`
`START_INDEX_OR_TIME`
`END_INDEX_OR_TIME`
`ROLE`

### Allowed roles

`CALIBRATION`
`DISCOVERY`
`CONFIRMATION`
`EXTERNAL_VALIDATION`

### Invariant

A single window must not simultaneously have roles DISCOVERY and CONFIRMATION for the same candidate.

---

## 11. EVALUATOR_SNAPSHOT object

Evaluator identity must be reproducible.

### Required relations

`EVALUATOR_PATH`
`CODE_HASH`
`VERSION`
`SUPPORTED_RULE_GRAMMAR`

### Purpose

Separates scientific rule semantics from implementation changes.

---

## 12. CONFIRMATION_RUN object

A confirmation run is an execution event.

### Required relations

`RUNS_CANDIDATE -> RULE_CANDIDATE`
`USES_PREREGISTRATION -> PREREGISTRATION_RECORD`
`USES_WINDOW -> DATA_WINDOW`
`USES_EVALUATOR -> EVALUATOR_SNAPSHOT`
`RUN_ID -> execution identifier`

### Statuses

`RUNNING`
`COMPLETED`
`FAILED_EXECUTION`

Execution failure is not scientific failure.

---

## 13. CONFIRMATION_RESULT object

### Required relations

`RESULT_OF -> CONFIRMATION_RUN`
`OLD_RULE_METRIC -> value`
`REVISED_RULE_METRIC -> value`
`NULL_METRIC -> value(s)`
`PRIMARY_RESULT_CLASS -> token`
`CLAIM_BOUNDARY -> object`

### Possible result classes

`CONFIRMED`
`NOT_CONFIRMED`
`NOT_EVALUABLE`
`NULL_NOT_BEATEN`
`BOUNDARY_HIT`

### Invariant

Result objects are immutable once finalized.

---

## 14. PROMOTION_DECISION object

Promotion is separate from confirmation result.

### Required relations

`DECIDES_ON -> RULE_CANDIDATE`
`BASED_ON -> CONFIRMATION_RESULT`
`DECISION -> PROMOTE | REJECT | REMAIN_OPEN`
`DECISION_REASON -> structured reason`

### Constraint

Confirmation success alone does not automatically mutate the parent rule.

Promotion is an explicit graph event.

---

## 15. EMPIRICALLY_SUPPORTED_RULE object/state

A promoted candidate produces a new rule version.

### Required relations

`DERIVED_FROM_RULE -> parent RULE`
`PROMOTED_FROM -> RULE_CANDIDATE`
`SUPPORTED_BY -> CONFIRMATION_RESULT`
`SUPPORTED_BY_NULL_COMPARISON -> NULL_MODEL result(s)`
`PREREGISTERED_BY -> PREREGISTRATION_RECORD`
`EPISTEMIC_STATUS -> EMPIRICALLY_SUPPORTED_RULE`

### Versioning

Promotion creates a new rule id.

The parent rule is not overwritten.

Parent may receive:

`SUPERSEDED_BY -> new rule`

---

## 16. REJECTED_CANDIDATE object/state

A failed candidate must remain queryable.

### Required relations

`REJECTED_FROM -> RULE_CANDIDATE`
`FAILED_ON -> CONFIRMATION_RESULT`
`REJECTION_REASON -> token`
`ADDRESSES_OPEN -> OPEN`

### Example rejection reasons

`FAILED_TRANSFER`
`NULL_NOT_BEATEN`
`DIRECTION_REVERSED`
`SEARCH_BOUNDARY_UNRESOLVED`
`DEGRADED_PERFORMANCE`
`INSUFFICIENT_SAMPLE`

### Invariant

Rejected candidates are historical evidence.

They are never deleted merely because they failed.

---

## 17. CORRECTION object

Corrections represent post-preregistration or post-result clarifications.

### Required relations

`CORRECTS -> object/result/preregistration`
`WHAT_CHANGED`
`WHY_CHANGED`
`SEMANTICS_CHANGED -> TRUE|FALSE`
`CRITERIA_CHANGED -> TRUE|FALSE`
`CREATED_AT`

### Correction classes

`IMPLEMENTATION_ONLY`
`INTERPRETATION_DOWNGRADE`
`DATA_AUDIT_CORRECTION`
`PROTOCOL_CORRECTION`

### Invariant

Corrections append history.

They do not overwrite the original object.

---

## 18. OPEN_REFINEMENT object

An OPEN refinement records how uncertainty changes after evidence.

### Required relations

`REFINES_OPEN -> OPEN`
`RESOLVED_COMPONENT -> object`
`REMAINING_COMPONENT -> object(s)`
`REJECTED_COMPONENT -> RULE_CANDIDATE(s)`
`TRIGGERED_BY -> CONFIRMATION_RESULT | EVIDENCE`

### Invariant

OPEN refinement is decomposition, not deletion.

---

## 19. Core predicates

Minimum predicate vocabulary:

`TRIGGERED_BY`
`TRIGGERED_BY_RULE`
`ABOUT_SUBJECT`
`EXPECTED_TARGET`
`OBSERVED_TARGET`
`ADDRESSES_OPEN`
`SUPPORTED_BY`
`PARENT_RULE`
`PROPOSED_CHANGE`
`DISCOVERY_WINDOW`
`CONFIRMATION_WINDOW`
`FREEZES_CANDIDATE`
`REQUIRES_NULL_MODEL`
`USES_EVALUATOR`
`RESULT_OF`
`BASED_ON`
`DECISION`
`PROMOTED_FROM`
`DERIVED_FROM_RULE`
`SUPERSEDED_BY`
`FAILED_ON`
`REJECTION_REASON`
`REFINES_OPEN`
`RESOLVED_COMPONENT`
`REMAINING_COMPONENT`
`CORRECTS`
`PROVENANCE`

---

## 20. Lifecycle states

### Candidate lifecycle

`PROPOSED`
`-> PREREGISTERED`
`-> CONFIRMATION_PENDING`
`-> CONFIRMED | REJECTED | NOT_EVALUABLE`
`-> PROMOTED | STORED_REJECTED | REMAIN_OPEN`

### OPEN lifecycle

`OPEN`
`-> REFINED_OPEN`
`-> PARTIALLY_RESOLVED`

No terminal CLOSED state is required by default.

A domain may define one later if complete closure is meaningful.

### Rule lifecycle

`ASSUMED_RULE`
`-> EMPIRICALLY_SUPPORTED_RULE`
`-> SUPERSEDED_RULE | DEPRECATED_RULE`

---

## 21. Immutability rules

The following records are immutable after finalization:

`PREREGISTRATION_RECORD`
`CONFIRMATION_RESULT`
`PROMOTION_DECISION`
`CORRECTION`

Changes require new version objects.

The following may gain new relations but should not lose historical ones:

`OPEN`
`RULE`
`EVIDENCE`

---

## 22. Identity and versioning

Every rule revision receives a new object id.

Example:

`RULE_LOAD_MAPPING_V1`
`RULE_LOAD_MAPPING_V2`

Relations:

`RULE_LOAD_MAPPING_V2 DERIVED_FROM_RULE RULE_LOAD_MAPPING_V1`

`RULE_LOAD_MAPPING_V1 SUPERSEDED_BY RULE_LOAD_MAPPING_V2`

### Rule

Never mutate V1 into V2 in-place.

---

## 23. Minimal promotion graph

A valid promoted rule must have a complete path:

`RULE_V1`
`-> FORMAL_MISMATCH`
`-> OPEN`
`-> EVIDENCE`
`-> RULE_CANDIDATE`
`-> PREREGISTRATION_RECORD`
`-> CONFIRMATION_RUN`
`-> CONFIRMATION_RESULT`
`-> PROMOTION_DECISION`
`-> RULE_V2`

and, where required:

`NULL_MODEL -> CONFIRMATION_RESULT`

If any mandatory node is absent:

`PROMOTION_PATH_INCOMPLETE`

---

## 24. Minimal rejection graph

A valid rejected candidate must preserve:

`RULE_CANDIDATE`
`-> PREREGISTRATION_RECORD`
`-> CONFIRMATION_RESULT`
`-> PROMOTION_DECISION = REJECT`
`-> REJECTED_CANDIDATE`

and remain connected to the OPEN it attempted to address.

---

## 25. Example mapping from Experiment 033

`RULE033_OLD_DIRECT_MAPPING`
`-> formal mismatch objects`
`-> OPEN_033_REMAINING_DOMAIN_VALIDITY`
`-> EXP027 / EXP030 / EXP031 / EXP032 evidence`
`-> RULE033_REVISED_LOAD_OFF_RUNON candidate`
`-> preregistration`
`-> untouched confirmation result`
`-> promotion decision`
`-> empirically supported revised rule`
`-> OPEN refinement`

Experiment 033 correction becomes:

`CORRECTION_033_RULE_TYPE`
`CORRECTS -> RULE033_REVISED_LOAD_OFF_RUNON`
`SEMANTICS_CHANGED -> FALSE`

---

## 26. Example mapping from Experiment 039

`RULE039_OLD_MAPPING`
`-> mismatch`
`-> OPEN`
`-> 59-row candidate`
`-> preregistration`
`-> confirmation result`
`-> permutation null result`
`-> promotion decision = REJECT`
`-> REJECTED_CANDIDATE`

The OPEN remains active/refined.

---

## 27. Validation constraints for the future core

The core should reject malformed revision records when:

- candidate has no parent rule;
- candidate has no OPEN;
- preregistration has no confirmation window;
- candidate parameter changes after freeze;
- confirmation window equals discovery window;
- promotion lacks required null result;
- promotion has failed gate;
- correction overwrites historical result;
- promoted rule lacks provenance path;
- rejected candidate is deleted;
- OPEN is erased instead of refined.

---

## 28. Canonical machine-readable skeleton

Conceptual object skeleton:

`REVISION_CASE`

`{`
`  parent_rule,`
`  mismatches[],`
`  open,`
`  evidence[],`
`  candidates[],`
`  preregistrations[],`
`  null_models[],`
`  confirmation_runs[],`
`  confirmation_results[],`
`  decisions[],`
`  corrections[],`
`  open_refinements[]`
`}`

This is a conceptual schema, not yet the final serialization format.

---

## 29. Architectural principle

The revision subsystem must make epistemic history visible.

The core must be able to answer:

- Why does this rule exist?
- What old rule did it replace?
- What mismatch triggered revision?
- What OPEN did it address?
- Which evidence generated the candidate?
- Which data were discovery vs confirmation?
- Which nulls were tested?
- What failed candidates preceded it?
- Were there later corrections?
- What remains unresolved?

If the graph cannot answer these questions, the revision is not fully represented.

---

## 30. Final data-model rule

Noepedia revision is not a mutation of knowledge.

It is an append-only chain of epistemic states connected by explicit provenance.

Operational shorthand:

`OLD STATE -> CONTRADICTION STRUCTURE -> OPEN -> CANDIDATE STATE -> TEST -> DECISION -> NEW STATE`

with all intermediate states retained.

---

## Next step

Experiment 044 should define Promotion Gates:

- mandatory gates;
- optional domain-specific gates;
- null requirements;
- failure semantics;
- NOT_EVALUABLE handling;
- exact transition from candidate to EMPIRICALLY_SUPPORTED_RULE.