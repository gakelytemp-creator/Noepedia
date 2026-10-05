# Experiment 072 — Frozen Repair Semantics

## 1. Comparator role

`SIMPLER_RULE_COMPARATOR` is reclassified conceptually as:

`COMPARATOR_ONLY`

It remains executable for diagnostic comparison.

It is not a knowledge-revision family.

## 2. Candidate generation

`CLASS_IMBALANCE` no longer generates `SIMPLER_RULE_COMPARATOR`.

Class imbalance remains a structural risk flag.

If no other supported candidate family exists:

`OPEN_DECOMPOSITION`

is selected.

## 3. Null protection

If `SIMPLE_BASELINE_PLAUSIBLE` is present for a genuine relation candidate, `SIMPLER_RULE_NULL` remains mandatory.

Thus the simpler baseline still protects promotion; it simply cannot itself be promoted.

## 4. Direct comparator invocation

If a comparator is explicitly evaluated and passed into a promotion case, the pipeline must mark it non-promotable.

Required outcome:

`REMAIN_OPEN`

Reason:

`COMPARATOR_ONLY_NOT_PROMOTABLE`

No RULE object may be materialized.

## 5. Validation controls

A. known temporal positive:
must still PROMOTE.

B. class-imbalance-only prevalence-shift control:
must not promote.

C. shuffled class-imbalance control:
must not promote.

D. direct comparator promotion attempt:
must remain open as comparator-only.

## 6. Claim boundary

072 is an architecture repair only.

It does not reinterpret 071 and is not a new real-data discovery experiment.
