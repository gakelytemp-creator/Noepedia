# RUN C / GW05 — frozen design before handler implementation

**Status: DESIGN FROZEN / HANDLER IMPLEMENTATION MAY BEGIN**  
**Date: 2026-10-18**

## 1. Experimental split

RUN C uses public GW04 material only to measure programmer cost. GW04 is not a correctness benchmark after unseal.

GW05 is the transfer/correctness benchmark. Its world and answer-book hash were sealed before this design and before handler implementation.

Measured programmer-share components:

1. family dictionary / instruction-set design;
2. reusable generic operations;
3. family-specific handlers;
4. interpretation decisions;
5. encoder alignment cost observed later on GW05.

## 2. Frozen family dictionary as compiler target

The RUN C author derives a canonical family dictionary from the public GW04 cold translation.

The dictionary contains:

- canonical RULE_TYPE names;
- required and optional structural fields;
- permitted structural variants where generalization is explicitly chosen;
- dependency signatures used to decide which rule families are relevant to validation of an incoming record;
- the handler operation contract.

Every abstraction not mechanically present in the GW04 record is a programmer decision and must appear in the decision log.

Handlers target this frozen dictionary, not a specific event stream and not a tested-world object/predicate name.

## 3. Handler interface

A handler receives only:

```text
rule_record
network
operation_request
```

The operation request is structural. Permitted operation names in v0.1:

```text
CHECK
DERIVE
VALIDATE_INCOMING
CLOSURE
```

No event identifier or expected event answer is part of the handler interface.

A handler returns a structural result with fields drawn from:

```text
verdict
proposed_delta
derived_records
provenance_requirements
opens
conflicts
stops
unchecked_dependencies
details
```

## 4. Programmer-share metrics

Freeze and report:

- FAMILY_TYPE_COUNT
- GENERIC_OPERATION_COUNT
- HANDLER_COUNT
- LOC_CORE: executable source lines excluding blank lines, comments and docstrings
- LOC_TOTAL: source lines including comments/docstrings
- LOC breakdown for dictionary/operations/handlers/dispatcher/audit/tests
- AUTHOR_DECISION_COUNT
- REVIEWER_DECISION_COUNT
- DECISION_UNDERCOUNT = reviewer - author

Decision-log entry contract:

```text
DECISION_ID
RULE_OR_INTERFACE
RECORD_FIELDS
UNDERSPECIFIED_POINT
ALTERNATIVES
CHOICE
RATIONALE
EXECUTABLE_SEMANTICS_CHANGED = YES | NO
CODE_LOCUS
```

The independent reviewer supplies REVIEWER_DECISION_COUNT and any missed loci before any GW05 translation exists.

## 5. Dependency signatures and UNCHECKED

The family dictionary declares a dependency signature for each family.

An incoming fact depends on a rule when its structural predicate matches one of the predicate-bearing roles declared in that family's dependency signature.

This is not inferred by scanning arbitrary rule text or arbitrary fields.

If a relevant rule cannot be executed because of EXECUTOR_HOLE, SCHEMA_DRIFT, ENCODER_NONCOMPLIANCE, or another explicitly classified executor boundary, the system must preserve an addressable marker:

```text
TYPE = CHECK_STATUS
STATUS = UNCHECKED
DEPENDENCY = <rule address>
REASON = <classified boundary>
```

UNCHECKED is neither FALSE nor CONFLICT.

## 6. Generality gates

Handler implementation may contain canonical RULE_TYPE names and structural field names from the frozen dictionary.

It must not contain implementation logic keyed to any tested-world:

- object identifier;
- predicate identifier;
- status-value identifier;
- source identifier;
- law address;
- event address;
- expected answer;
- hidden-world fact.

Mechanical review has two layers:

1. text/token scan;
2. Python AST scan of string/numeric constants used in comparisons, dispatch maps, match/case patterns and hard-coded tuple/list/dict literals.

The gate report is frozen with handler code.

## 7. Family responsibilities

### EXACT_DISTINCT_TARGET_CARDINALITY

Check exact distinct target cardinality using the rule record's subject/predicate/count/distinctness fields. Absence of enough observed targets is not by itself a closed-world contradiction unless closure/completeness is structurally supplied.

### CONDITIONAL_NODE_BALANCE_AND_UNIQUE_MISSING_DERIVATION

Support an equality between structural numeric expressions, closure-gated unique-missing derivation, arithmetic over integers, and exact provenance requirements. Open-universe mismatch must remain non-conflicting when completeness required for a contradiction is unavailable.

The canonical expression vocabulary may generalize a side from GW04's aggregate expression to a direct value lookup. That generalization is programmer work and must be logged.

### EXPLICIT_CLOSED_RELATION_SET

Provide exact member-set closure for the declared relation slice and scope only. Do not generalize closure to other scopes.

### CURRENT_VALUE_AT_MOST_ONE

Check at-most-one current value for configured predicates. Do not erase or silently overwrite competing current records.

### CURRENT_STATUS_IMPLIES_MAGNITUDE

Despite the historical name inherited from GW04, semantics are field-driven: current antecedent pattern implies a current consequent pattern with declared subject binding. Consequent object type is unrestricted.

## 8. Two GW05 cold translations

After dictionary, handlers, decision log, audit reports, and C1/C3 candidate code are separately frozen, GW05 is translated twice in two fresh isolated sessions.

### GW05-N — neutral control

Input: solver-visible GW05 material + neutral format contract, without the family dictionary.

Purpose: measure natural schema drift.

A faithful but handler-incompatible schema is:

```text
SCHEMA_DRIFT
```

### GW05-L — dictionary-targeted compiler test

Input: solver-visible GW05 material + neutral format contract + frozen family dictionary.

Instruction: when a law fits a frozen family without information loss, use that family and its fields; otherwise preserve the law faithfully and emit a new type or explicit hole rather than forcing it.

The two encoder sessions must not see each other's outputs.

## 9. Transfer taxonomy

```text
TRANSFER_OK
SCHEMA_DRIFT
FAMILY_SCHEMA_HOLE
ENCODER_NONCOMPLIANCE
ENCODER_HOLE
EXECUTOR_HOLE
EXECUTOR_ERROR
SPEC_HOLE
```

Definitions:

- **SCHEMA_DRIFT**: GW05-N faithfully represents the law but its schema does not fit the frozen handler interface.
- **FAMILY_SCHEMA_HOLE**: the fresh law cannot be represented by a frozen family type without losing at least one condition of the law.
- **ENCODER_NONCOMPLIANCE**: on GW05-L, the law can be represented by the frozen family without information loss, but the encoder nevertheless fails to use the required type/fields.
- **ENCODER_HOLE**: the encoder cannot produce a faithful representation at all.
- **EXECUTOR_HOLE**: a canonical representation exists but required executable capability is absent.
- **EXECUTOR_ERROR**: handler accepts the representation/path but executes it incorrectly.
- **SPEC_HOLE**: required behavior is not determined by the frozen specification.

### Reviewer classification rule

The independent reviewer decides FAMILY_SCHEMA_HOLE versus ENCODER_NONCOMPLIANCE during post-run audit.

Single criterion:

> Can this law be represented by the frozen family type without losing any condition of the law?

For every such classification the reviewer records a written justification. This is an explicit evaluation judgment, not a mechanical classifier.

## 10. C1/C3 isolation

RUN C handler development does not repair C1 or C3.

Any C1/C3 candidate code intended for GW05 must be:

- separately preregistered;
- implemented after handler freeze if desired;
- frozen before either GW05 translation;
- attributed in separate runs.

No C1/C3 code may be changed after observing GW05-N or GW05-L.

## 11. Frozen order

1. GW05 world + answer-book hash sealed — complete.
2. Freeze this RUN C design.
3. Build family dictionary from public GW04 translation.
4. Implement generic operations + family handlers.
5. Freeze author decision log, LOC report, AST/text generality report, tests, dictionary, handler interface and hashes.
6. Independent reviewer inspects dictionary, code and author decision log; reviewer count/delta are recorded.
7. Freeze any C1/C3 candidate code intended for GW05, separately.
8. Start GW05-N cold encoder; seal output.
9. Start independent GW05-L cold encoder with dictionary; seal output.
10. No handler/dictionary/adapter/candidate repair after either translation is observed.
11. Execute planned GW05 runs and seal logs.
12. Only then open GW05 answer book and perform audit.

## 12. Current gate

After this design is committed, handler implementation is permitted.

No GW05 translation exists at design-freeze time.
