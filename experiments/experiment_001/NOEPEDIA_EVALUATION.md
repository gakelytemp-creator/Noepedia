# Experiment 001 — Noepedia-Condition Evaluation

> **Status:** evaluation against the frozen pre-run criteria.

## 1. Headline result

The Noepedia-condition run reproduced the core diagnosis of the blind baseline but did so with a stricter structural distinction.

It correctly:

- selected the minimal task cut `{R11, R18, R16}`;
- identified R11 as a **mismatch candidate**, not a proven error;
- proposed the minimal conditional revision;
- preserved OPEN_01;
- preserved provenance;
- separated stored facts from inference;
- explicitly discovered the missing bridge between `EXPOSES_NET` and `CONNECTED_TO`;
- independently rediscovered the connector/pin granularity gap.

The most important result is that the run did **not** collapse "coherence repair" into "physical truth".

---

## 2. Frozen-criterion check

| Criterion | Result | Notes |
|---|---|---|
| Small task-specific cut | PASS | {R11,R18,R16} |
| Mismatch localization | PASS | R11 candidate |
| Minimal revision | PASS | only R11 object proposed to change |
| OPEN preservation | PASS | OPEN_01 untouched |
| Provenance preservation | PASS | SRC_SYNTH retained |
| Direct fact / inference separation | PASS | explicit |
| Missing structural constraint detection | PASS | EXPOSES_NET ↔ CONNECTED_TO bridge |
| Hidden granularity assumption detection | PASS | pin-level structure missing |
| Unsupported closure avoided | PASS | no claim of proven physical error |

---

## 3. Baseline vs Noepedia-condition comparison

Both runs found:

- R11 as the likely mismatch;
- VOUT as the coherent repair;
- OPEN_01 must remain open;
- connector granularity is unresolved.

The Noepedia-condition run was stricter in one important way:

> It explicitly refused to treat R11 as a logically proven error because the field lacks the relation-semantics bridge needed to derive contradiction.

This matters because the architecture is supposed to distinguish:

```text
coherence pressure
from
proof
```

The run did that successfully.

---

## 4. New structural result

The experiment now reveals **two distinct unresolved structures**:

### OPEN_STRUCT_01 — Predicate bridge

Question:

> Under the relevant output role, must `EXPOSES_NET(J2,X)` imply or constrain `CONNECTED_TO(J2,X)`?

This is a missing relation-semantics rule.

### OPEN_STRUCT_02 — Connector granularity

Question:

> Is J2 an atomic one-net terminal, or a container with multiple pins / terminals?

This is a missing object-decomposition / cardinality rule.

These are related but not identical.

One concerns **predicate semantics**.
The other concerns **object granularity**.

The experiment should keep them separate.

---

## 5. What this experiment demonstrates — and what it does not

### Demonstrates at dry-run level

The explicit relation-field discipline can:

- preserve OPEN while solving a local task;
- isolate a candidate mismatch;
- keep revision local;
- expose missing structural requirements instead of inventing them;
- distinguish coherent repair from established truth.

### Does not yet demonstrate

- real Noepedia computational advantage;
- deterministic task-cut extraction;
- autonomous Daimonion behavior;
- energy savings;
- real-world electronics validation;
- better performance than a strong LLM baseline.

This remains a synthetic fixture interpreted by language models.

---

## 6. Experimental value

The strongest result is not "the model found R11".

The strongest result is:

> **The experiment generated new structure about what the field itself was missing.**

The fixture began with one explicit OPEN.
The runs exposed two additional structural OPENs.

That is consistent with the intended research mechanism:

```text
task
→ reconstruction
→ tension
→ missing constraint
→ new OPEN
```

The next experiment should test whether this can happen through an implemented traversal mechanism rather than through an LLM reading the packet.

---

## 7. Next step

Do **not** patch Experiment 001 and rerun it as if nothing happened.

Preserve it.

Create Experiment 002 with:

1. explicit connector-terminal objects or an explicit atomic-terminal constraint;
2. explicit relation semantics linking output-role exposure to connectivity;
3. one different hidden mismatch;
4. one genuine unrelated OPEN;
5. deterministic JSON traversal before any LLM interpretation.

Experiment 002 should test whether the system can find the same class of structural tension algorithmically.
