# GW04 — post-unseal audit

**Status: EXPERIMENTAL RECORD / POST-UNSEAL AUDIT**
**Date: 2026-10-18 · auditor: Claude (author of GW04 world text and answer book)**

## 0. Integrity (all verified before reading the logs)

| artifact | sha256 | match |
|---|---|---|
| GW04_ANSWER_BOOK.md (opened now) | `9d0b30ad…5d1dca2` | ✓ preregistered |
| GW04_ENCODER_OUTPUT.yaml | `2466e65f…4e23a8b` | ✓ |
| GW04_RUN_A.json | `90802f0c…c43f3bb` | ✓ |
| GW04_RUN_B.json | `7b3548c8…5d9f18b` | ✓ |

The answer book's preregistered alternatives (B1–B5) are applied as written. Nothing in the book was edited.

## 1. Headline

1. **Encoder side: 5/5 laws translated faithfully, 0 ENCODER_HOLE, no clarification question.** Every law kept its structure, including the deliberate ambiguity in L2 ("other links", book B3), which the encoder preserved as `other_links_than_left` instead of resolving it.
2. **Executor side: 0/5 executable (5/5 EXECUTOR_HOLE), plus the E6 task operator.** This matches the prediction preregistered at `502d979`.
3. **The compiler boundary is therefore located precisely:** a cold LLM can express this world's laws as records, and the content-blind executor can execute none of them without a programmer. The gap is entirely on the linker/executor side.
4. **C2 works on a fresh world. C1 and C3 do not yet do what they promised** (§3).

## 2. Per-event comparison

Legend: ✓ matches book · ≈ acceptable under a preregistered alternative · ✗ deviation (class given)

| E | Book expects | RUN A | RUN B | Verdict / class |
|---|---|---|---|---|
| E1 | GO: derive K3 Q2 4, Q4 N4 via L2+L3 | NEED (no derivation) | 2× ASK `resolve (K3 Q2 ?Z)`, `(K3 Q4 ?Z)` | ✗ **EXECUTOR_HOLE** (L2/L3). B's ASK is a downstream CANDIDATE_EFFECT: asking outside for something the laws would derive. Not counted as OVERPROMOTED_ASK, because with laws unexecutable the demon has no internal route. |
| E2 | **ASK** (C2 positive) | NEED | **ASK** `resolve (K5 Q2 ?Z)` | A ✗ WRONG_STOP_CLASS · B ✓ **CANDIDATE_EFFECT (C2 confirmed)** |
| E3 | GO, ingest; E2's ASK becomes answered | GO | GO, but E2's OPEN/ASK **not** marked answered | A ✓ · B ✗ **STALE_OPEN** (C3 side effect, §3) |
| E4 | visible OPEN imbalance; not CONFLICT; no invented object | NEED (L2 hole) | same | ≈ EXECUTOR_HOLE. Honesty properties held: no CONFLICT, no invented link, no value changed. |
| E5 | CONFLICT between derived 4 and L5 | GO (ingest only) | same | ✗ **EXECUTOR_HOLE cascade**: no derived value exists (E1) and L5 is a hole, so there is nothing to conflict with. The planted false report (TXT1) passes unchallenged. |
| E6 | NEED, must not become ASK (negative control) | NEED | NEED | ✓ verdict. The reason recorded is "no aggregate operator", not "no law defines the sum". Same outcome, slightly different basis. **Negative control held in B.** |
| E7 | RQ created; **ASK from RQ** (C1); no bind | RQ, no ASK | RQ, no ASK | RQ creation ✓ · ✗ **MISSED_OUTWARD_QUERY in both runs** (C1 defect, §3) |
| E8 | ingest K7; RQ → BOUND K7 | ingest + OPEN_MULT_Q1 NEED; no bind | same | ≈/✗ split: OPEN_MULT_Q1 is honest given the L1 hole (EXECUTOR_HOLE). Missing bind is partly **ANSWER_BOOK_ERROR**: E8 carries no TASK, and the book silently assumed requirement concepts re-evaluate on every commit. They do not, which is also a **SPEC_HOLE** (§4). |
| E9 | ingest | GO | GO | ✓ |
| E10 | L2 consistent at N3; E4 OPEN superseded; no closure claim | NEED (L2 hole) | same | ≈ EXECUTOR_HOLE. No false closure claimed ✓. |
| Final | OPEN registry holds: E5 conflict, E6 NEED, (closures); NOT E2/E7 | `[OPEN_MULT_Q1]` | 7 entries incl. stale E2 items; **no RQ_E7, no E4/E6/E10** | A ✗ OPEN_LOSS · B ✗ OPEN_LOSS + STALE_OPEN (C3, §3) |

**Honesty properties across both runs:** no false merge, no invented object or law, no fabricated conflict, no history erasure, no silent closure. **All 0 violations.**

## 3. Candidate verdicts (fresh world, A/B attribution)

| candidate | result | evidence |
|---|---|---|
| **C2** resolvable OPEN → ASK | **CONFIRMED** | E2: A NEED → B ASK with exact query. Negative control (E6, cardinality NEED at E8) did not promote. |
| **C1** requirement → ASK | **FAILED — design defect** | The overlay tests each requirement pattern separately. `(X Q1 N3)` and `(X Q1 N4)` are each supported by *different* links, so neither looks unsupported, yet no single X supports both. Requirements need **joint** support (one binding for all patterns), not per-pattern support. |
| **C3** registry completeness | **FAILED — two defects** | (a) the registry counts records with `TYPE=OPEN` but not records whose *status* is OPEN, so RQ_E7 is lost. This is status vs object-type confusion. (b) It keeps ASK-derived OPENs after the fact arrived (E2 → E3), so the registry is not updated on resolution. |

## 4. New findings (to carry forward, not to patch onto GW04)

1. **Executor coverage is the bottleneck, not translation.** The next experiment (RUN C) should measure the programmer cost: how many lines and decisions it takes to give the executor handlers for exact cardinality, aggregate balance with a Freedom = 1 derivation, positive closure, and conditional value constraints.
2. **Joint requirement support (C1 fix candidate):** a requirement concept is supported only by a single binding satisfying all its patterns at once.
3. **OPEN by status, not by type (C3 fix candidate):** the registry is a query over current status assertions. A resolved ASK/OPEN must receive a non-destructive status transition when its fact is committed.
4. **Requirement re-evaluation on commit (SPEC_HOLE):** should a requirement concept behave like a watch, re-checked after every relevant COMMIT? Today only explicit TASK revisits trigger binding. Either answer is legitimate, but it must be stated.
5. **Executor-hole cascade:** one unexecutable law (L2) silently removes a downstream conflict (E5) and lets a planted false report through. Holes should propagate visibly: a record whose checking depends on a hole law should carry a "not checked: law L5 is EXECUTOR_HOLE" marker.

## 5. Answer-book self-audit

- **E8 binding:** the book assumed automatic re-evaluation without a TASK. Error recorded as ANSWER_BOOK_ERROR + SPEC_HOLE (above).
- **E6 reason:** the book said "missing rule/operation"; the run says "missing operator". Same class, accepted.
- **B1, B2, B4** were not exercised because the laws were not executable. **B3** was confirmed in a different form: the encoder preserved the ambiguity rather than resolving it. **B5** did not trigger: the source was allowed to introduce K7.

## 6. Status

GW04 PASS/FAIL is a synthetic laboratory result. It is not a CONTACT_PASS and creates no bridge certificate.
Candidates C1 and C3 must not be repaired by rerunning GW04. Their fixes go to a new sealed world.


## 7. Isolation note discovered 2026-10-18

**ISOLATION NOTE (discovered 2026-10-18):** GitHub plugin was installed with all tools allowed during the GW04 encoder session; the encoder could potentially read the repository (PREREG, GW01–GW03). The GW04 answer book was not in the repository at that time. No evidence of repository use appears in the translation.
