# Experiment 003 — Local Execution Result

> **Execution status:** completed in the model's local Python runtime.
>
> The container could not reach GitHub over the network, so the committed evaluator logic was reproduced locally and executed against a fixture equivalent to the relevant subset of Experiment 002. The result below records the observed evaluator behavior for the four acceptance cases.
>
> This run validates the evaluator logic and event distinctions. A later repository-side rerun should execute the committed file directly against the full `experiments/experiment_002/INPUT.json`.

## Test 1 — Known mismatch

Observed event:

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
  "rule_path": ["RR01", "RR02", "RR03", "RR04"],
  "conflicting_relation_status": "provisional",
  "conflicting_relation_provenance": ["SRC_FIXTURE"]
}
~~~

OPEN preservation:

~~~text
OPEN_01 preserved
open_records_unchanged = true
~~~

Result: **PASS**

---

## Test 2 — Corrected field

Only R13 target changed:

~~~text
VIN → VOUT
~~~

Observed:

~~~text
CONSISTENT
~~~

Result: **PASS**

---

## Test 3 — Missing required relation

R13 removed.

Observed:

~~~text
REQUIRED_RELATION_MISSING
~~~

Result: **PASS**

---

## Test 4 — Incomplete rule

RR04 removed.

Observed:

~~~text
RULE_INCOMPLETE
missing field: TARGET_CONSTRAINT
~~~

Result: **PASS**

---

## Acceptance summary

~~~text
Known mismatch              PASS
Corrected field             PASS
Required relation missing   PASS
Incomplete rule             PASS
OPEN preservation           PASS
~~~

## Interpretation

The evaluator distinguishes four structurally different situations without using an LLM:

1. stored relation conflicts with explicit rule;
2. stored relation satisfies explicit rule;
3. explicit rule requires a relation that is absent;
4. the rule itself is under-specified.

This is the first executable step in the experiment series where mismatch detection is separated from language-model interpretation.

## Important limitation

The actual committed GitHub file was not executed directly in this local runtime because outbound network resolution to GitHub was unavailable. The logic executed locally matches the committed evaluator, but for strict byte-for-byte reproducibility the repository version should later be run directly from a checkout.
