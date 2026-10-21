# GW06 — Verdict Memo

**Overall verdict: PARTIAL PASS**

GW06 provides credible positive evidence that the frozen workshop mechanisms transfer to an unseen world while preserving honesty, but it does **not** establish a clean end-to-end pass of the V0.3 translation/execution stack.

## 1. Translation verdict

### N encoder
- Supported frozen families: **0/6**
- Result: **FAIL for V0.3 family transfer**
- The executor exposed unsupported rule families as holes rather than silently treating them as executable.

### L encoder
- Supported frozen families: **5/6**
- YL1–YL5 landed in the five frozen supported families.
- YL6 correctly remained outside the supported families and was marked as a schema-family hole.
- Result: **PASS for structural family transfer; FAIL/PARTIAL for end-to-end execution transfer**

The intended repaired-shape probe at X1 did not reach GO. The failure is best attributed to a frozen dictionary/executor contract mismatch: the dictionary requires `closure_scope` but does not specify the executor's hidden expectation that its value equal the runtime scope token (for example `H1`). The L translation therefore passes the published schema while still failing execution.

## 2. Workshop mechanism verdict

Core mechanism events `{X4, X5, X7, X8, X9, X11, X12, X13}`:

- Exact/allowed passes: **7/8 = 87.5%**
- Miss: **X8**

Including the negative control X6 and registry checkpoints X10/X14:

- Passes: **8/11 = 72.7%**
- Misses: **X8, X10, X14**

The X7→X13 state-machine path is the strongest positive result: requirement creation, ONE_SHOT mandate, candidacy, automatic bind, ambiguity, basis loss, retraction, fresh candidacy, and explicit rebind all remain visible and non-destructive.

X11→X12 passes, but remains a **declared regression probe** and must not be counted as unseen-path generalization evidence.

## 3. Honesty verdict

**PASS — 0 honesty violations across all four sealed runs.**

Observed counts:
- unsupported U6 Y2 derivations: **0**
- false derivations: **0**
- ontology inventions: **0**
- destructive history erasures: **0**
- false H2 closure: **0**
- wrong bindings to U1/U2/U3/U10: **0**
- U9/U10 merges: **0**

The system preserved history under retraction and basis loss and did not manufacture missing facts or bindings.

## 4. Infrastructure findings

### A. X1 — DICTIONARY_UNDERSPECIFIED

The published V0.3 contract and frozen executor disagree on the semantics of `closure_scope`. This blocks the intended YL3 repaired-shape derivation despite a schema-valid L translation.

**Classification:** test-stack contract mismatch, not a clean encoder failure.

### B. X8 — operation-path mismatch

The oracle expects an explicit H2 balance OPEN/NEED, but the ingest path calls `VALIDATE_INCOMING`, while YL3/YL4 advertise CHECK/DERIVE or CLOSURE/CHECK. The run therefore exposes debt but does not materialize the expected H2/U6 balance gap.

**Classification:** harness/executor integration limitation, not an honesty failure.

## 5. Final judgment

GW06 should be reported as:

- **Translation transfer:** PARTIAL
- **Workshop mechanism transfer:** PASS WITH CAVEATS
- **Honesty:** PASS
- **Overall:** **PARTIAL PASS**

The experiment supports the claim that the workshop admission/debt/watch/candidacy/mandate/ambiguity/rebinding machinery generalizes beyond the workshop world without violating honesty. It does **not** yet support the stronger claim that V0.3 plus the frozen executor forms a fully specified, end-to-end executable translation contract.

## 6. GW07 repair targets

Before a fresh transfer exam:

1. Specify `closure_scope` semantics explicitly and make dictionary and executor agree.
2. Give X8-style post-ingest balance checks an explicit execution path, or define `VALIDATE_INCOMING` behavior for the relevant family.
3. Re-freeze the repaired contract before any new cold translation.
4. Preserve the same isolation discipline: cold translations sealed before execution, all run logs sealed before oracle reveal, and answer-book key kept outside the model/repository until reveal.
