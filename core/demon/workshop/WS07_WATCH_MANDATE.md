# WS07 — watch → candidacy → mandate → bind (ATTIC 01 §12)

**Status: WORKSHOP RESULT, works on scene GW05, plus one SYNTHETIC extension (P1/P2) that is not part of GW05.**
Files: `watch.py`, `test_watch.py` (10 tests). `gw05_scene.py` gains `--watch off|on`, `--mandate none|one_shot|standing` and `--probe-damage off|on`.

## Mechanism

| step | implementation | ATTIC |
|---|---|---|
| discovery | after **every committed fact** (inside ingest), `watch_requirement()` re-reads C1 joint bindings for RQ_F6, using the requirement's single shared variable | A12.2 |
| candidacy | `CAND_<rq>_<x>_<scope>_<method>_N<n>` (`TYPE = SOLE_KNOWN_CANDIDATE_ON`). The identity is the snapshot (rq, candidate, N, scope, method). If the candidate set changes, the record becomes HISTORICAL; it is never deleted and never re-activated. Re-establishing the same sole candidate later creates a **new** claim with the new N | A12.3 |
| authority | `MANDATE_F6` is issued at F6 by `UPPER_LAYER` for `AUTO_BIND`, with the lifecycle fixed at issue. An issuer equal to the operation raises `PermissionError`. `STANDING_WHILE` requires a machine-checkable condition (`{RECORD, STATE_IN}`; here `RQ_F6 ∈ {OPEN}`). Authority in force = record CURRENT **and** condition true now; it is computed, never stored | A12.7–A12.9 |
| decision | `bind()` writes `RQ_F6_BIND` plus `RQ_F6_BIND_SUPPORTED_BY_1 → CAND_…`. A ONE_SHOT mandate becomes HISTORICAL after use | A12.5 |
| damage | `binding_state()` is a view over SUPPORTED_BY edges. `on_basis_lost()` reopens RQ non-destructively; a used ONE_SHOT mandate is not revived, and an ASK goes to the issuer | A12.6, A12.9 |

## Scene results (C1/C3, admission, resolve-asks on; debt = rule; dictionary V0.2; identical for N and L in this part)

| | no mandate | ONE_SHOT | STANDING_WHILE |
|---|---|---|---|
| F7, F8 watch | no candidate | same | same |
| **F10 watch** | candidacy `CAND_RQ_F6_I8_…_N<n>` created at the second I8 commit; **RQ stays OPEN** | candidacy + **AUTO_BIND at F10** by `MANDATE_F6`; mandate → HISTORICAL | candidacy + AUTO_BIND at F10; mandate record stays CURRENT but **not in force** (RQ is BOUND, so the condition is false) |
| **F11 revisit** | binds using the existing candidacy, authorized by TASK_F6; ASK answered | already bound; binding_state SUPPORTED | same |
| F12 registry | as WS05 (no RQ, no ASK) | same | same |
| **P1 (synthetic: I9 with G1, G4)** | candidacy → HISTORICAL (candidates I8, I9); binding **REVIEW_REQUIRED**, record kept; RQ reopened | same, and **ASK → UPPER_LAYER**: "binding RQ_F6_BIND lost its basis; renew AUTO_BIND?"; mandate not revived | same; RQ reopens → condition true again → mandate **in force** without any revival, so no ASK |

## Checks

- `--watch off` leaves every earlier result unchanged: `ablation_gw05.json` regenerates byte-identical, and `--admission off` still reproduces the sealed N/L C13 logs.
- Tests: admission 11/11, resolution 4/4, dictionary 7/7, watch 10/10.

## Revision after GPT review (same WS07)

1. **Snapshot identity.** The candidacy address now includes N, scope and method. A sole → ambiguous → sole-again sequence produces a new claim with a later N. The old claim stays HISTORICAL. Test: `test_sole_ambiguous_sole_again_makes_a_new_claim`.
2. **STANDING_WHILE is evaluated.** The condition is structured and checked at every authority lookup. After the bind it is false (the mandate is not in force), and after the reopen it is true again. Tests: `test_standing_condition_false_after_bind_true_after_reopen`, `test_standing_mandate_needs_checkable_condition`.
3. **Variable.** The candidate is read from the single variable shared by all patterns, not from the first binding value. A requirement without exactly one shared variable raises. Test: `test_variable_is_the_shared_one`.
4. **Granularity.** The watch runs after every committed fact. It does not run after the internal commits of signal records, markers and edges, because C1 reads only current facts and those records cannot change the candidate set. This is the honest scope of "every commit" here.
5. **Unchanged candidate set → no new record.** The existing claim stays (`test_unchanged_set_keeps_one_claim`), so the ledger does not grow one record per commit.

## What the scene exposed (new, open)

1. **Two candidates produce no disambiguation ASK.** After P1, RQ is OPEN with candidates I8 and I9, but nothing asks "I8 or I9?". The watch records ambiguity only by the *absence* of a sole-candidate record. An explicit `AMBIGUOUS_CANDIDATES_ON(N, {I8, I9})` record and a C2-style ASK would be the honest form (A8.5: a question that cuts the candidate set).
2. **An answered ASK keeps ANSWERED after its answer loses its basis.** `OPEN_ASK_4` was ANSWERED by `RQ_F6_BIND`; after P1 that binding reads REVIEW_REQUIRED, yet the ASK still reads ANSWERED. By A12.6 the ASK's state should also be read through its support (`ANSWERED_BY → binding → candidacy`). Today it is a stored status. This is the same masking pattern WS06 found: correct records, stale view.
3. **Under STANDING_WHILE after P1, the mandate is in force but has nothing to bind.** That is correct (two candidates). It does show that a standing mandate without a disambiguation route (item 1) just waits.

These are the remaining workshop items before exam mode.
