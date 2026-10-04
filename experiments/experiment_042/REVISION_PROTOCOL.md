# Experiment 042 — Revision Protocol Specification

## Status

`SPECIFICATION_COMPLETE`

Experiment 042 does not test a new physical relation.

Its purpose is to convert the experimentally validated workflow from Experiments 019–041 into a reusable Noepedia revision protocol.

---

## 1. Protocol goal

The protocol governs what Noepedia must do when a stored rule produces a formal mismatch.

The protocol must prevent three failure modes:

1. silently rewriting the rule to fit observed data;
2. promoting a discovery-window pattern directly into knowledge;
3. confusing repeated structure with truth.

The protocol therefore separates:

`DETECTION`
`OPEN CREATION`
`CANDIDATE GENERATION`
`PREREGISTRATION`
`CONFIRMATION`
`NULL COMPARISON`
`PROMOTION OR REJECTION`
`OPEN REFINEMENT`

---

## 2. Core sequence

Canonical revision sequence:

`RULE`
`-> FORMAL_MISMATCH`
`-> OPEN`
`-> EVIDENCE_COLLECTION`
`-> RULE_CANDIDATE`
`-> PREREGISTRATION`
`-> UNTOUCHED_CONFIRMATION`
`-> NULL_COMPARISON`
`-> PROMOTE | REJECT | REMAIN_OPEN`
`-> OPEN_REFINEMENT`

No step may be silently skipped.

---

## 3. Stage A — Formal mismatch detection

### Input

A stored rule and relations already present in the field.

### Requirement

The evaluator derives the mismatch.

Input relations must not insert verdict labels such as:

`MISMATCH`
`ANOMALY`
`FAULT`
`CORRECT`
`WRONG`

unless those labels are themselves the explicit object of a separate experiment.

### Output

A `FORMAL_MISMATCH` event with explicit provenance:

- rule id
- subject
- input relation ids
- conflicting relation id
- expected target
- observed/stored target

### Claim boundary

`FORMAL_MISMATCH != PHYSICAL_CONTRADICTION`

A formal mismatch means only that the stored rule and stored relations cannot all be satisfied simultaneously under the active rule grammar.

---

## 4. Stage B — OPEN creation

Every unresolved formal mismatch must create or refine an OPEN object.

Minimum OPEN fields:

`OPEN_ID`
`SUBJECT`
`UNRESOLVED_PREDICATE`
`CURRENT_HYPOTHESIS_SCOPE`
`TRIGGERING_MISMATCHES`
`PROVENANCE`
`STATUS = OPEN`

Example:

`OPEN_DOMAIN_VALIDITY_OF_RULE_X`

### OPEN semantics

OPEN means:

> existing relation geometry requires further distinction, but the missing distinction is not yet known.

OPEN must not be interpreted as:

- missing database value;
- error message;
- placeholder for the most likely answer;
- permission to guess.

### Rule

OPEN is refined, not erased.

A successful revision resolves a component of OPEN while preserving unresolved components.

---

## 5. Stage C — Evidence collection

Evidence collection may be exploratory.

It may inspect:

- temporal structure;
- alternative relation paths;
- raw measurements;
- transition geometry;
- structural neighborhoods;
- candidate covariates;
- other relation networks.

Exploratory evidence must be labeled:

`EXPLORATORY_EVIDENCE`

It cannot directly promote a rule.

### Separation rule

`candidate generation != confirmation`

The same data used to generate a candidate must not be reused as untouched confirmation data.

---

## 6. Stage D — Rule candidate construction

A `RULE_CANDIDATE` must contain:

`CANDIDATE_ID`
`PARENT_RULE_ID`
`PROPOSED_CHANGE`
`SOURCE_EVIDENCE_IDS`
`DISCOVERY_WINDOW`
`PARAMETERS`
`EXPECTED_FAILURE_MODE_ADDRESSED`
`STATUS = CANDIDATE`

### Candidate discipline

A candidate should make the smallest change needed to address the observed mismatch structure.

Do not add multiple corrections if one simpler relation explains the same evidence.

### Candidate provenance

Every parameter chosen from discovery data must be recorded.

Examples:

- lag length;
- threshold;
- transition direction;
- relation orientation;
- selected channel;
- selected structural path.

---

## 7. Stage E — Preregistration

Before confirmation data are inspected, freeze:

1. confirmation dataset/window;
2. candidate rule;
3. all candidate parameters;
4. evaluator version/hash when relevant;
5. primary metric;
6. null baselines;
7. success/failure gates;
8. tie-breaking rules;
9. OPEN handling;
10. claim boundary.

### Required artifact

`PREREGISTRATION_RECORD`

Minimum fields:

`CANDIDATE_ID`
`CONFIRMATION_SOURCE`
`FROZEN_PARAMETERS`
`FROZEN_EVALUATOR_ID`
`PRIMARY_METRIC`
`NULL_MODELS`
`PASS_CRITERIA`
`FAIL_CRITERIA`
`TIMESTAMP_OR_COMMIT`

### Rule

Any post-preregistration implementation-only correction must be recorded separately in `CORRECTION.md` or equivalent.

Such a correction may not silently change:

- semantic rule;
- data window;
- threshold;
- candidate parameter;
- success criterion;
- null model;
- claim boundary.

---

## 8. Stage F — Untouched confirmation

Confirmation data must be untouched by candidate selection.

Allowed use:

- evaluation only.

Disallowed use before freeze:

- parameter tuning;
- channel selection;
- threshold selection;
- direction selection;
- model selection;
- rule-shape selection.

### Required comparison

At minimum report:

`OLD_RULE_ERROR`
`REVISED_RULE_ERROR`

and where applicable:

`COMMON_EVALUABLE_SUBSET`

Unresolved rows must not be silently counted as success.

---

## 9. Stage G — Null comparison

A candidate cannot be promoted merely because it beats the old rule.

It must also beat appropriate null models.

### Null model classes

At least one null is required whenever a trivial alternative could explain the gain.

Possible nulls include:

`MAJORITY_STATE_NULL`
- always predict the target majority state;

`PERMUTATION_NULL`
- destroy true alignment while preserving marginal structure;

`TIME_SHIFT_NULL`
- circularly or deterministically shift source timing;

`RANDOMIZED_RELATION_NULL`
- preserve counts/degrees while destroying specific pairing;

`SIMPLER_RULE_NULL`
- compare against a strictly simpler explanation;

`SHAM_TRANSITION_NULL`
- use transitions at incorrect times while preserving transition frequency.

### Null selection rule

Nulls must target the most plausible trivial explanation of candidate success.

### Gate

Promotion requires a preregistered advantage over all required nulls.

No universal numeric threshold is imposed by this protocol.

The threshold must be frozen before confirmation.

---

## 10. Stage H — Promotion classes

After confirmation, every candidate receives exactly one status:

### A. `EMPIRICALLY_SUPPORTED_RULE`

Requirements:

- candidate improves the preregistered primary metric;
- confirmation data were untouched;
- all required null gates pass;
- no preregistered exclusion gate fails;
- provenance is complete;
- OPEN is refined, not erased.

### B. `REJECTED_CANDIDATE`

Use when:

- confirmation fails;
- direction reverses;
- null baseline performs equally or better;
- benefit disappears;
- candidate degrades performance;
- selected parameter sits on an unresolved search boundary when boundary failure was preregistered.

Rejected candidates remain stored.

They are evidence against repeating the same unsupported revision.

### C. `REMAIN_OPEN`

Use when:

- evidence is insufficient;
- experiment is not evaluable;
- confirmation sample is too small;
- a required null cannot be computed;
- result is ambiguous under preregistered rules.

---

## 11. Stage I — OPEN refinement

After a result, OPEN must be updated by decomposition.

Example:

Before:

`OPEN: DOMAIN_VALIDITY_OF_DIRECT_MAPPING`

After supported revision:

`RESOLVED_COMPONENT: directional temporal exception`

`REMAINING_OPEN:`
- residual mismatches;
- transition-zone interpretation;
- physical mechanism;
- external transfer.

After rejected candidate:

`REJECTED_COMPONENT: candidate relation X`

`REMAINING_OPEN:`
- original unexplained mismatch structure;
- alternative candidate classes.

### Rule

`FAILED_CANDIDATE != CLOSED_OPEN`

Rejecting one explanation does not close the underlying uncertainty.

---

## 12. Provenance requirements

Every promoted or rejected candidate must preserve a complete path:

`OLD_RULE`
`-> TRIGGERING_MISMATCH`
`-> OPEN`
`-> EVIDENCE`
`-> CANDIDATE`
`-> PREREGISTRATION`
`-> CONFIRMATION_RESULT`
`-> NULL_RESULT`
`-> PROMOTION_STATUS`

### Minimum provenance rule

No `EMPIRICALLY_SUPPORTED_RULE` may exist without direct links to:

- parent rule;
- evidence;
- preregistration;
- confirmation result;
- null comparison result.

---

## 13. Historical corrections

Corrections are first-class history.

A correction must state:

`WHAT_CHANGED`
`WHY_CHANGED`
`WHEN_CHANGED`
`WHETHER_SEMANTICS_CHANGED`
`WHETHER_PREREGISTERED_CRITERIA_CHANGED`

Corrections must not overwrite historical results.

Historical result + later correction must coexist.

Examples from this series:

- Experiment 033: execution-only rule-type correction;
- Experiments 036/037: later interpretation downgrade after null-baseline testing.

---

## 14. Negative-result preservation

Noepedia must preserve negative results as reusable knowledge about failed paths.

Examples:

`GLOBAL_FIXED_OFFSET_REJECTED`
`EXPLORATORY_CANDIDATE_NOT_REPLICATED`
`LOCAL_PATTERN_NOT_GENERAL`
`NOT_NULL_PROTECTED`
`DISCOVERY_REVISION_FAILED_TRANSFER`

### Rule

Negative results must be queryable during future candidate generation.

The system should avoid regenerating an already rejected candidate unless new evidence explicitly justifies reconsideration.

---

## 15. Anti-overfitting rules

1. Discovery and confirmation must be separated.
2. Confirmation may not tune candidate parameters.
3. Multiple candidate search must record the search space.
4. Search-boundary optima must be flagged.
5. Residual patterns require new confirmation before rule expansion.
6. Null models are mandatory where class imbalance or alignment artifacts are plausible.
7. Failed confirmation blocks promotion.
8. Strong discovery effect size does not override failed confirmation.

---

## 16. Noepedia core object vocabulary

This protocol assumes the following semantic object classes will become first-class core objects in a later architecture step:

`RULE`
`FORMAL_MISMATCH`
`OPEN`
`EVIDENCE`
`RULE_CANDIDATE`
`PREREGISTRATION_RECORD`
`NULL_MODEL`
`CONFIRMATION_RESULT`
`CORRECTION`
`EMPIRICALLY_SUPPORTED_RULE`
`REJECTED_CANDIDATE`
`OPEN_REFINEMENT`

Experiment 043 should formalize these as a data model.

---

## 17. Protocol state machine

Allowed primary transitions:

`RULE`
`-> MISMATCH_DETECTED`
`-> OPEN_ACTIVE`
`-> CANDIDATE_PROPOSED`
`-> PREREGISTERED`
`-> CONFIRMATION_RUN`
`-> NULLS_EVALUATED`
`-> PROMOTED | REJECTED | REMAIN_OPEN`
`-> OPEN_REFINED`

Forbidden transitions:

`MISMATCH_DETECTED -> PROMOTED`
`CANDIDATE_PROPOSED -> PROMOTED`
`DISCOVERY_SUCCESS -> PROMOTED`
`NULL_FAILED -> PROMOTED`

---

## 18. Minimum promotion checklist

A rule candidate may be promoted only if all applicable answers are YES:

- Was mismatch derived rather than inserted?
- Is an OPEN object present?
- Is candidate provenance complete?
- Were discovery and confirmation separated?
- Was the candidate frozen before confirmation?
- Were success criteria frozen before confirmation?
- Were required nulls frozen before confirmation?
- Did the revised rule improve the primary metric?
- Did it pass every required null gate?
- Were unresolved rows excluded from success counts?
- Were implementation corrections documented?
- Was OPEN refined rather than erased?

If any required answer is NO:

`DO_NOT_PROMOTE`

---

## 19. Reference experiments

Positive references:

`EXP033`
- full revision loop;
- provenance-bearing revised rule;
- untouched core re-evaluation;
- 99.565% mismatch reduction;

`EXP040`
- calibration-only family selection;
- discovery/freeze/confirmation split;
- explicit majority and permutation null protection;
- 98.688% reduction vs old rule;
- ~99% reduction vs both null baselines;

Negative/corrective references:

`EXP029`
- exploratory candidate failed confirmation;

`EXP035`
- local residual pattern failed generalization;

`EXP038`
- transferred patterns failed null protection;

`EXP039`
- discovery-derived revision degraded untouched confirmation.

---

## 20. Final protocol principle

The Noepedia revision protocol is not:

> find a rule that fits the data better.

It is:

> detect where the current relation structure fails, preserve the uncertainty, propose the smallest evidence-grounded revision, freeze it, challenge it on untouched data and against plausible null explanations, and only then allow the field to treat the revision as empirically supported.

Operational shorthand:

`MISMATCH -> OPEN -> CANDIDATE -> FREEZE -> CONFIRM -> NULLS -> PROMOTE/REJECT -> REFINE OPEN`

---

## Next step

Experiment 043 should define the Core Data Model for Revision:

- object types;
- required predicates;
- provenance edges;
- lifecycle/status fields;
- immutable historical records;
- promotion and rejection relations.