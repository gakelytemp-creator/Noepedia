# Experiment 003 — Minimal Deterministic Evaluator Specification

> **Status:** design specification; no implementation yet.

## 1. Input

Single JSON document containing:

- objects;
- relations;
- rules;
- OPEN records.

The initial input is Experiment 002's `INPUT.json`.

---

## 2. Minimal data assumptions

### Object

Required fields:

~~~text
id
type
~~~

### Relation

Required fields:

~~~text
id
subject
predicate
object
network
status
provenance
~~~

### Rule relation

The rule itself is represented through ordinary relations:

~~~text
RULE_SCOPE
INPUT_PREDICATE
REQUIRED_PREDICATE
TARGET_CONSTRAINT
~~~

### OPEN

Required fields:

~~~text
id
subject
predicate
object
status = open
~~~

---

## 3. Evaluator stages

### Stage A — Index

Build read-only lookup indexes:

~~~text
object_by_id
relations_by_subject
relations_by_subject_predicate
rules_by_rule_id
open_by_id
~~~

No semantic conclusions are produced here.

### Stage B — Reconstruct rule object

For each object of type `consistency_rule`, collect its rule-defining relations.

For `RULE_TERMINAL_EXPOSE_CONNECT`, reconstruct:

~~~text
scope_type = terminal
input_predicate = EXPOSES_NET
required_predicate = CONNECTED_TO
target_constraint = SAME_NET
~~~

If any required rule field is absent, emit `RULE_INCOMPLETE` rather than guessing.

### Stage C — Find scope-matching subjects

Find objects whose explicit type equals the rule scope.

For the fixture:

~~~text
J2_P1 : terminal
J2_P2 : terminal
~~~

### Stage D — Match input relation

For each scoped subject, find relations using the rule's input predicate.

Example:

~~~text
J2_P1 → EXPOSES_NET → VOUT
~~~

### Stage E — Derive requirement

From the input relation and rule, construct an **expected relation object** in memory:

~~~text
subject = J2_P1
predicate = CONNECTED_TO
target = VOUT
derived_from = [R18, RR01, RR02, RR03, RR04]
~~~

This expected relation is not stored as evidence.

It is a rule-derived requirement.

### Stage F — Compare with stored relation

Find stored relations matching:

~~~text
subject = J2_P1
predicate = CONNECTED_TO
~~~

Three possible outcomes:

#### F1 — exact target exists

~~~text
CONNECTED_TO → VOUT
~~~

Result:

~~~text
CONSISTENT
~~~

#### F2 — same predicate exists with different target

~~~text
CONNECTED_TO → VIN
~~~

Under `SAME_NET`:

~~~text
FORMAL_MISMATCH
~~~

#### F3 — no required relation exists

Result:

~~~text
REQUIRED_RELATION_MISSING
~~~

This is not the same as a mismatch against an existing conflicting relation.

---

## 4. Output event types

The evaluator should emit structured events.

### CONSISTENT

Required relation exists exactly.

### FORMAL_MISMATCH

Existing relation violates explicit rule.

### REQUIRED_RELATION_MISSING

Rule requires a relation that is absent.

### RULE_INCOMPLETE

Rule cannot execute because its own specification is incomplete.

### SCOPE_UNRESOLVED

Subject type needed by rule is missing or ambiguous.

No other event type is needed for Experiment 003.

---

## 5. Mismatch event schema

~~~json
{
  "event": "FORMAL_MISMATCH",
  "rule": "RULE_TERMINAL_EXPOSE_CONNECT",
  "subject": "J2_P1",
  "input_relation": "R18",
  "derived_requirement": {
    "predicate": "CONNECTED_TO",
    "target": "VOUT"
  },
  "conflicting_relation": "R13",
  "stored_target": "VIN",
  "constraint": "SAME_NET",
  "rule_path": ["RR01", "RR02", "RR03", "RR04"]
}
~~~

---

## 6. OPEN preservation

OPEN records are read-only in Experiment 003.

The evaluator may report:

~~~json
{
  "open_preserved": ["OPEN_01"]
}
~~~

but must not:

- close;
- rewrite;
- interpret;
- rank;
- delete

any OPEN.

---

## 7. No repair logic

Experiment 003 must not implement:

~~~text
settled > provisional
~~~

or any other repair-precedence rule.

Reason:

Experiment 002 explicitly showed that mismatch proof and repair selection are separate problems.

The evaluator may report statuses of conflicting relations, but may not choose which one to edit.

---

## 8. Test cases

The first implementation should include at least four fixtures.

### Test 1 — Known mismatch

Experiment 002 as-is.

Expected:

~~~text
FORMAL_MISMATCH
J2_P1
R18
R13
expected VOUT
stored VIN
~~~

### Test 2 — Corrected field

Change only R13 target:

~~~text
VIN → VOUT
~~~

Expected:

~~~text
CONSISTENT
~~~

### Test 3 — Missing CONNECTED_TO

Remove R13.

Expected:

~~~text
REQUIRED_RELATION_MISSING
~~~

### Test 4 — Incomplete rule

Remove RR04.

Expected:

~~~text
RULE_INCOMPLETE
~~~

These four cases test four distinct states and prevent the evaluator from being a one-case mismatch detector.

---

## 9. Non-goals

Do not add:

- database;
- UI;
- graph library;
- ontology engine;
- inference engine beyond this rule type;
- LLM API;
- automatic repair;
- plugin system;
- optimization;
- concurrency.

The first evaluator should be small enough that its behavior can be inspected line by line.

---

## 10. Scientific requirement

The implementation must make it impossible to obtain the expected Experiment 002 result from a special-case check such as:

~~~text
if subject == "J2_P1": mismatch
~~~

or:

~~~text
if target == "VIN": wrong
~~~

The result must arise only from:

~~~text
object type
+ explicit relation
+ explicit rule
+ explicit constraint
~~~

---

## 11. Implementation acceptance gate

Before any code is accepted, confirm:

- input schema is sufficient;
- event types are sufficient;
- rule reconstruction is unambiguous;
- no repair semantics have leaked into detection;
- OPEN handling is read-only;
- four test fixtures are agreed.

Only after that should implementation begin.
