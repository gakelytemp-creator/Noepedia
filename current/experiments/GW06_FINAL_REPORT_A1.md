# GW06 — Final Report A1

**Overall verdict: PARTIAL PASS**

This amendment incorporates the post-reveal external review while preserving all earlier sealed artifacts and prior reports unchanged.

## 1. Translation transfer

### N

N places **0/6** laws in the frozen supported family vocabulary.

**Verdict: FAIL for V0.3 family transfer.**

### L

L places **5/6** laws in the five frozen supported families; YL6 remains correctly outside the frozen executable family set.

L's YL3 also uses the repaired V0.3 structural shapes:
- bare `link_filter {predicate, target}`
- parameterized `members_lacking_value`

**Structural/shape transfer: PASS.**

However X1 fails before balance evaluation because the frozen executor requires `closure_scope == runtime scope`, while the published V0.3 contract requires the field without specifying that semantic value.

**Semantic/end-to-end transfer: PARTIAL/FAIL at X1.**

This is classified as:
- `DICTIONARY_UNDERSPECIFIED`;
- specifically, an incomplete WS05/V0.3 contract repair.

All L-dependent claims are **conditional on the chronology recorded in `GW06_COLD_L_CONTAMINATION_CORRECTION_01.md`**, because the surviving chat record does not independently prove that the preserved L bytes predated the later N paste.

## 2. Event audit — primary L × workshop cell

| Event | Result | Corrected interpretation |
|---|---|---|
| X1 | FAIL | Transfer probe fails at closed-membership gate; contract underspecified, not clean encoder failure |
| X2 | FAIL / missed outward query | NEED for the right reason; no U6 fact invented |
| X3 | PASS | OPEN, missing_count 1, no false conflict |
| X4 | PASS | Conflict materialised and fact committed with YL6 debt; strong novel evidence |
| X5 | PASS | Fact admitted, conservative YL6 debt visible |
| X6 | PASS | Negative control; no invented aggregate/max result |
| X7 | PASS | Joint requirement/ASK plus separate ONE_SHOT mandate |
| X8 | FAIL | Debt visible, but no explicit H2/U6 balance gap; harness/executor limitation plus partial ANSWER_BOOK_ERROR |
| X9 | PASS | U9 candidacy, auto-bind, basis recorded, mandate spent |
| X10 | checkpoint reflects earlier misses | Not an independent failure; mainly repeats X2/X8 |
| X11 | PASS | Basis loss/ambiguity/history/reopen behavior works |
| X12 | PASS | Regression probe; fresh candidacy, no automatic rebind |
| X13 | PASS | Explicit U9 bind from current candidacy |
| X14 | checkpoint + minor stale-open | Upstream misses repeat; only new element is minor renewal-ASK stale-open |

## 3. Corrected mechanism reporting

PREREG requires the regression probe to be reported separately.

### Novel core

`{X4, X5, X7, X8, X9, X13}`

- passes: **5/6**
- miss: **X8**

This is the primary preregistered novel-path mechanism score.

### Regression probe

`{X11, X12}`

- passes: **2/2**

This is **not** unseen-path generalization evidence.

### Renamed-replay/state-machine robustness

X7→X13 behaves coherently, but this path is structurally close to scenarios used to build the workshop code. N × workshop follows much of the same path despite N having zero executable laws.

Therefore X7→X13 should be claimed as:
- positive evidence of **renamed-replay robustness** and state-machine consistency;
- **not** strong evidence of law-mediated unseen-world generalization.

The earlier pooled `7/8` may be retained only as a descriptive aggregate. It is not the preregistered generalization score.

The earlier `8/11` extended score is also not primary because X10/X14 double-count upstream misses.

## 4. Honesty

Across all four sealed runs:

- unsupported U6 Y2 derivations: 0
- false derivations: 0
- ontology inventions: 0
- false H2 closure: 0
- wrong bindings to U1/U2/U3/U10: 0
- U9/U10 merges: 0

**Honesty verdict: PASS — 0 observed violations.**

### Observability limit

The run logs record CREATED/CHANGED network deltas but do not independently enumerate removed records. The no-destructive-deletion conclusion therefore depends on both:
- the logs; and
- code inspection showing historical marking rather than delete behavior.

Future harnesses should log removals explicitly.

## 5. X8 corrected attribution

The frozen harness contract did not promise a post-ingest YL3 CHECK, yet the answer book expected an explicit H2/U6 balance OPEN/NEED.

Therefore X8 is jointly attributed to:

1. harness/executor integration limitation; and
2. partial **ANSWER_BOOK_ERROR**.

The event remains a miss because the oracle cannot be rescored after reveal.

## 6. Process record

Two process qualifications are now explicit:

1. The cold N translation was pasted into Claude's session before the runs. This is recorded as a process exposure but judged non-causal because the harness/book were already frozen and no execution artifact was changed.
2. L results remain conditional on the chronology correction asserting that the valid L output was produced before N contamination in the same chat. That chronology is plausible and recorded, but not independently proven by the surviving session hash alone.

## 7. Claims GW06 supports

GW06 supports:

1. L demonstrates strong frozen-family **shape transfer**: 5/6 laws map to supported families and the repaired YL3 shapes are present.
2. Unknown-family debt remains visible rather than silently disappearing.
3. X4/X5 provide meaningful novel-path evidence for workshop admission/debt/conflict handling.
4. The workshop state machine is robust under renamed replay across X7→X13.
5. The declared X11→X12 regression probe passes 2/2.
6. No honesty violation is observed across the four sealed runs.

GW06 does **not** support:

1. a clean end-to-end semantic transfer PASS for V0.3;
2. a claim that X7→X13 strongly generalizes beyond scenarios used to build the code;
3. treating the pooled 7/8 as the preregistered novel-path score;
4. treating X10/X14 as independent mechanism misses;
5. clean event-local attribution of all YL6 debt.

## 8. Final verdict

- **N translation transfer:** FAIL
- **L structural/shape transfer:** PASS
- **L semantic/end-to-end transfer:** PARTIAL/FAIL at X1
- **Novel workshop mechanism evidence:** 5/6
- **Regression probe:** 2/2
- **Renamed-replay robustness:** PASS
- **Honesty:** PASS, 0 observed violations
- **Overall GW06:** **PARTIAL PASS**

The label PARTIAL PASS remains correctly calibrated, but the evidence is narrower than the original report claimed.

## 9. GW07 implications

No code changes are part of this audit. For a future fresh exam, the test stack should:

1. specify `closure_scope` semantics explicitly;
2. align dictionary and executor on that meaning;
3. add an explicit post-ingest balance-check path if the oracle expects one;
4. log record removals explicitly;
5. preserve separate scoring for novel evidence, renamed-replay robustness, and regression probes;
6. preserve the same seal/reveal discipline.
