# GW05 — post-unseal audit

**Status: EXPERIMENTAL RECORD / POST-UNSEAL AUDIT**
**Date: 2026-10-18 · auditor: Claude (author of the GW05 world and answer book; reviewer of RUN C)**

## 0. Integrity (verified at repo HEAD `9f273e2` before opening the book)

| artifact | sha256 | match |
|---|---|---|
| GW05_ANSWER_BOOK.md (opened now) | `654ad18d…b745f4c1` | ✓ preregistered |
| GW05_N_ENCODER_OUTPUT.yaml (raw) | `9f454739…c8b41b35` | ✓ |
| GW05_N_ENCODER_OUTPUT.normalized.json | `f47aebd3…d7c47f5d` | ✓ |
| GW05_L_ENCODER_OUTPUT.json | `ca2c60f6…eca3ef6` | ✓ |
| GW05_RUN_N_BASE / N_C13 / L_BASE / L_C13 | `965822c2…` / `e949634b…` / `4ac1612e…` / `781ddbaf…` | ✓ |

**Known exposures (recorded in PREREG):** the auditor saw both raw translations before the runs. Both were pasted into the auditor's session by the experimenter, and the auditor made no comment on them. The answer book was sealed before either translation existed. The GW04 encoder session (not GW05) had potential repo read access. For GW05, the GitHub app was suspended during both encoder sessions, and both encoders answered "no" to the repository-visibility check.

## 1. Headline

1. **Encoders: 10/10 laws translated faithfully, 0 ENCODER_HOLE, no clarification questions.**
   - GW05-L: 5/5 laws used the dictionary's RULE_TYPE names, and 4/5 matched the handler shape exactly.
   - **ENCODER_NONCOMPLIANCE = 0.** This is the reviewer's judgment under RC-D13 (§4).
2. **GW05-N (neutral contract): 0/5 laws executable.**
   - M1 is SCHEMA_DRIFT: same RULE_TYPE name, different fields.
   - M2–M5 are EXECUTOR_HOLE: new type names.
   - This is natural drift, as preregistered. Without a target schema, a cold encoder does not land on the handlers' interface.
3. **GW05-L (dictionary):**
   - **M1 and M5 transferred and executed.**
   - **M2 failed through a defect in the dictionary, not in the encoder** (§4).
   - M3 and M4 were never exercised: M3 is only used through M2, and no event triggered M4.
4. **C1 (joint support) works.** It produced an ASK at F6 and bound I8 at F11, but not in the base runs.
5. **C3 works on the original defect (RQ by status is now in the registry) but has a new STALE_OPEN defect.** The ASK is not resolved when its requirement binds.
6. **Two executor defects found:**
   - a conflict is detected and then swallowed at ingest;
   - UNCHECKED blocks every report from committing in the N runs.

## 2. Per-event comparison

Runs: **N0** = N_BASE, **N13** = N_C13, **L0** = L_BASE, **L13** = L_C13.

| F | Book expects | N0 / N13 | L0 / L13 | Verdict / class |
|---|---|---|---|---|
| F1 | GO: derive I3 R2 3 (M2+M3) | NEED (M2 EXECUTOR_HOLE) | NEED (M2 SCHEMA_DRIFT) | ✗ N: EXECUTOR_HOLE · L: SCHEMA_DRIFT caused by the dictionary (§4) |
| F2 | ASK (I5 R2 ?) | NEED | NEED (drift) | ✗ cascade from M2. The C2 single-fact ASK never got a chance: the stop's MISSING is "SCHEMA_DRIFT", not a triplet |
| F3 | visible OPEN, not CONFLICT | NEED (M1 drift), no OPEN | **OPEN** (missing_count 1) | N ✗ SCHEMA_DRIFT · L ✓ |
| F4 | ingest I3 R6 S2; addressable CONFLICT vs D17 under M5/M4; nothing deleted | report **not committed**; 5 UNCHECKED markers | committed; M5 handler returned **BLOCK + conflict**, but the aggregate verdict was GO and no CONFLICT/OPEN record was created | N: UNCHECKED marker ✓ (no SILENT_UNCHECKED) but ingest refused (§3 D2) · L: ✗ **EXECUTOR_ERROR: conflict detected, then swallowed** (§3 D1) — MUTED_ROAR equivalent |
| F5 | NEED, must not be ASK | NEED | NEED | ✓ all four. **Negative control held** |
| F6 | RQ created; joint ASK; no bind | N0 NEED · **N13 ASK** | L0 NEED · **L13 ASK** `(?X R7 G1) AND (?X R7 G4)` | base ✗ MISSED_OUTWARD_QUERY (expected without C1) · C13 ✓ **C1 CONFIRMED** |
| F7 | ingest I5 R2 3; F2 question resolved | not committed | committed | N ✗ (D2) · L ✓ ingest (no F2 ask existed to resolve) |
| F8 | ingest I7; visible OPEN for B2 mismatch | not committed | committed; **no OPEN, no UNCHECKED** although M2 is unreadable | N ✗ (D2) · L ✗ **MISSED_UNCHECKED_MARKER** (§3 D3) + OPEN_LOSS |
| F9 | registry: RQ, F3, F4 conflict, F5 NEED, F8 mismatch; NOT F2 | N0 `[]` · N13 `[OPEN_ASK, RQ_F6]` | L0 `[OPEN_F3_1]` · L13 `[OPEN_ASK, OPEN_F3_1, RQ_F6]` | C3 ✓ **RQ by status now present** (L0/N0 reproduce the GW04 defect) · ✗ OPEN_LOSS for F4/F8 (consequence of D1/D3). F5 appears in the NEED list (accepted under W4) |
| F10 | ingest I8 (3 distinct agents) | not committed | committed; M1 checked | N ✗ (D2) · L ✓ |
| F11 | RQ → BOUND I8 | no candidates (I8 never committed) | L0 NEED · **L13 BOUND I8** | L13 ✓ · N ✗ cascade of D2 |
| F12 | final: F3, F4, F5, F8; NOT RQ/F6 | N13 still `[OPEN_ASK, RQ_F6]` (correct, nothing bound) | L13 `[OPEN_ASK_4, OPEN_F3_1]`; joint ASK still listed as unanswered | L13 ✗ **STALE_OPEN**: binding resolved the RQ but not its ASK (§3 D4) |

**Honesty properties across all four runs:** no false derivation, no invented object or law, no fabricated CONFLICT, no history erasure, no false closure. All 0. Every failure was a *missed* signal or an *over-refusal*, never an invented one.

## 3. Executor / candidate defects found

**D1 · Conflict swallowed at ingest (EXECUTOR_ERROR).** `validate_incoming` returns GO unless an UNCHECKED dependency exists. A handler result of `BLOCK` with `conflicts` is kept only inside `details.rule_results` and is never materialized as a CONFLICT/OPEN record. The executor *saw* the M5 violation and the network does not know it. This is the most important defect: it is exactly the failure the project defines as unacceptable (a silent pass of a detected contradiction).

**D2 · UNCHECKED blocks commit (N runs).** With unknown or drifted rule types, every report produced UNCHECKED markers (35 in total, the recall-over-precision cost of PR-D01, as anticipated) **and** the report was not committed. The design said the marker "does not mean FALSE". In practice, an unexecutable law now vetoes all incoming facts, and the N world is frozen at its starting records. Marking is correct. Refusing the commit is an undocumented decision with large downstream effect (F11 cannot bind).

**D3 · Drift detected only at DERIVE, not at ingest (MISSED_UNCHECKED_MARKER).** In L, M2's dependency signature resolves (its value predicates are readable), so ingest calls M2's VALIDATE_INCOMING. M2 does not support that operation and returns NEED with no classification, so no marker is created. Yet M2 is unreadable as a whole (SCHEMA_DRIFT at DERIVE). "Operation not supported" on a dependent rule should also yield UNCHECKED.

**D4 · C3 does not resolve the ASK when C1 binds (STALE_OPEN).** RQ_F6 leaves the registry on binding, but its generated `OPEN_ASK` and the unanswered-ASK entry remain.

## 4. Dictionary findings and the RC-D13 judgment

Criterion (preregistered): *can the law be written in the dictionary family without losing any condition?*

- **M2 fits the family losslessly → not FAMILY_SCHEMA_HOLE.**
- **The encoder did not deviate from what the dictionary says → not ENCODER_NONCOMPLIANCE.** Two dictionary defects explain the drift:
  1. **The variant shape is unspecified.** The dictionary lists `filter_variants: ["predicate_target", …]` as *names*, but never states that the `predicate_target` variant is written as `{"predicate":…, "target":…}` directly under `link_filter`. The encoder wrote `link_filter: {"predicate_target": {...}}`, a reasonable reading of the dictionary as written. The handler rejected it.
  2. **A GW04 world token leaked into the dictionary.** `literal_tokens` / `optional_paths` contain `adjacent_links_lacking_Q2_or_Q4`, where Q2 and Q4 are GW04 predicates. A faithful GW05 encoder cannot use that token (its world has no Q2/Q4), so it wrote `items_in_bin_lacking_R2`. The RUN C generality gates scanned handler code, not the dictionary. **The dictionary itself needs the same identifier gate.**
- **Classification: DICTIONARY_UNDERSPECIFIED** (new label). Encoder alignment cost = 0; dictionary cost was under-paid.

## 5. Answer-book self-audit

- The book expected F2's ASK to come from M2's closure test. Since M2 never executed, F2 tests nothing about C2 in any run. **C2 remains confirmed only by GW04**; GW05 provides no new evidence either way.
- F8 (B2 mismatch → OPEN) and F4 (→ CONFLICT) expectations stand. Their absence is attributable to D1/D3, not to book ambiguity (W2/W3 alternatives would also have required a visible record).
- W5 held: explicit TASK revisit at F11 made binding testable. It worked in L13.

## 6. Summary of results to carry forward (not to patch onto GW05)

| item | result |
|---|---|
| Natural schema drift (N) | 0/5 executable. A target schema is necessary |
| Compiler-target transfer (L) | 2/5 executed (M1, M5), 1/5 failed by dictionary defect (M2), 2/5 unexercised (M3, M4) |
| Encoder noncompliance | 0 |
| C1 joint support | CONFIRMED |
| C3 status registry | CONFIRMED for RQ; new STALE_OPEN defect on ASK resolution |
| Negative control | held in all runs |
| New defects | D1 conflict swallowed · D2 UNCHECKED vetoes commit · D3 drift invisible at ingest · D4 ASK not resolved on bind · dictionary shape gap · world token in dictionary |

GW05 PASS/FAIL is a synthetic laboratory result, not CONTACT_PASS. GW05 is now public and becomes a training scene. Fixes for D1–D4 and the dictionary must be tested on a new sealed world.