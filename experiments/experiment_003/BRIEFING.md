# Experiment 003 — Deterministic Mismatch Evaluator

> **Status:** PRE-IMPLEMENTATION CONCEPTUAL BRIEFING
>
> No code should be written until this specification is reviewed and accepted.

## 1. Purpose

Experiment 003 moves one step below the LLM-mediated dry-runs.

The question is no longer:

> Can an LLM read the relation field and notice the mismatch?

The question is:

> **Can a minimal deterministic evaluator derive the same mismatch directly from explicit JSON structure before any LLM interpretation?**

This is the first direct test of the intended LLM–LSM division of labor.

---

## 2. What Experiment 003 tests

Experiment 003 tests only:

- object typing;
- relation lookup;
- explicit rule loading;
- rule scope matching;
- input-predicate matching;
- required-predicate generation;
- SAME_NET target constraint;
- comparison with stored relations;
- formal mismatch emission;
- unrelated OPEN preservation.

It does not test:

- repair selection;
- Daimonion autonomy;
- layer birth;
- meta-layers;
- performance at scale;
- LLM cost savings;
- real hardware evidence;
- automatic ontology learning.

---

## 3. Frozen theoretical expectation

Given:

~~~text
J2_P1 : terminal

R18:
J2_P1 → EXPOSES_NET → VOUT

RULE_TERMINAL_EXPOSE_CONNECT:
scope = terminal
input predicate = EXPOSES_NET
required predicate = CONNECTED_TO
target constraint = SAME_NET

R13:
J2_P1 → CONNECTED_TO → VIN
~~~

the evaluator should derive:

~~~text
required:
J2_P1 → CONNECTED_TO → VOUT
~~~

and compare it with the stored relation:

~~~text
stored:
J2_P1 → CONNECTED_TO → VIN
~~~

Since `VIN != VOUT`, the evaluator should emit a mismatch.

---

## 4. What counts as success

Success requires all of the following:

1. the evaluator reaches the mismatch without an LLM;
2. the rule path is explicit in the output;
3. the conflicting and supporting relation IDs are preserved;
4. no unrelated relations are modified;
5. OPEN_01 remains open and untouched;
6. the evaluator does not choose a repair unless a repair policy is explicitly present.

---

## 5. What counts as failure

Failure includes any of the following:

- hard-coded special knowledge about J2_P1;
- hard-coded knowledge that VOUT is "correct";
- reliance on human-readable labels;
- hidden domain knowledge about electronics;
- scanning result interpreted by an LLM before mismatch emission;
- automatic repair of R13 without explicit repair policy;
- mutation of OPEN_01;
- failure to expose the rule chain that produced the mismatch.

---

## 6. Core architectural boundary

The evaluator must separate:

~~~text
DETECTION
from
INTERPRETATION
from
REPAIR
~~~

Experiment 003 implements only **DETECTION**.

Expected pipeline:

~~~text
JSON field
↓
deterministic evaluator
↓
formal mismatch object
↓
(optional later) LLM interpretation
↓
(optional later) repair policy / human decision
~~~

---

## 7. Frozen target output

At minimum:

~~~json
{
  "mismatch": true,
  "rule": "RULE_TERMINAL_EXPOSE_CONNECT",
  "subject": "J2_P1",
  "input_relation": "R18",
  "expected_predicate": "CONNECTED_TO",
  "expected_target": "VOUT",
  "conflicting_relation": "R13",
  "stored_target": "VIN",
  "constraint": "SAME_NET",
  "open_untouched": ["OPEN_01"]
}
~~~

No repair field is required in Experiment 003.

---

## 8. REOPEN triggers

Reopen the representation if:

1. rule execution requires procedural exceptions not represented in the field;
2. object typing is insufficient to decide scope;
3. relation lookup becomes ambiguous;
4. SAME_NET cannot be evaluated from explicit object identity;
5. the evaluator must know domain semantics not represented in JSON;
6. OPEN preservation requires ad hoc exclusions.

