# Experiment 018 — Verified Core-Integration Result

> **Status:** repository CI reproduction passed.
>
> **Architectural integration result:** PASS under the preregistered structural gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37178267622
job: verify
conclusion: success
head commit: 5b782565cd8e6e6577910c022db3d10f73a1d8f9
~~~

## Pipeline

~~~text
pinned real NAB machine-temperature trace
→ unchanged Experiment 011 detector as instrumentation adapter
→ deterministic 40-assessment relational cut
→ real measurements + timestamps + source rows + expectations + OPEN causes
→ unchanged Experiment 003 evaluator
→ structural verification
~~~

No NAB anomaly labels were used.

## Generated field

~~~text
assessments              40
detector-mismatch cases  20
control cases            20
OPEN cause records       20
stored relations        380
~~~

## Evaluator result

The existing generic evaluator produced exactly:

~~~text
FORMAL_MISMATCH  20
CONSISTENT       20
~~~

All 20 mismatch-cause OPEN records were preserved unchanged.

No repair or causal closure occurred.

## What the evaluator knew

The evaluator received only field structure and explicit rule objects.

Its active rule was:

~~~text
RULE_SCOPE = assessment
INPUT_PREDICATE = EXPECTED_STATE
REQUIRED_PREDICATE = OBSERVED_STATE
TARGET_CONSTRAINT = SAME_NET
~~~

The evaluator did not execute temperature-domain knowledge, rolling median or MAD, robust-z threshold logic, or NAB anomaly labels. Those belong to the instrumentation adapter before field construction.

## Architectural interpretation

Experiment 018 reconnects the real-data instrumentation track to the relational core:

~~~text
measurement
→ provenance
→ expectation
→ observed state
→ explicit rule
→ formal mismatch
→ unresolved causal OPEN
~~~

The result supports a narrow architecture-integration claim: real external observations can enter the Noepedia field as addressable relational structure, and the already-existing generic evaluator can operate on that structure without acquiring the external detector's domain semantics.

## Important limitation

The mismatch distinction itself was supplied by the Experiment 011 instrumentation adapter.

Therefore Experiment 018 does **not** show that Noepedia independently discovers anomalies. It shows that Noepedia can receive a real external distinction, preserve its provenance and unresolved causal state, and subject it to generic relational consistency machinery.

## Next OPEN

> **Can the relational field itself combine two independent real evidence paths and derive a mismatch that neither instrumentation stream asserted directly?**

That would move beyond importing detector classifications and test whether explicit cross-relational structure creates new real-data inference inside the Noepedia core.