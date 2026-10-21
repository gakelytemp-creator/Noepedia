# WS01 — D1 + D2 through one admission pipeline

**Status: WORKSHOP RESULT. "Works on scene GW05", not a demonstration claim. GW05 is public; no fresh-world evidence.**
**Implements: ATTIC 01 A3.1, A3.2, A3.4, A3.5 · author: Claude**

## What changed

Frozen code is untouched: `run_c/family_executor.py`, `run_c/gw05_runner.py`, the dictionary, and the sealed logs. Everything new lives in `core/demon/workshop/`.

| file | role |
|---|---|
| `admission.py` | pipeline: compose evidence → materialize → policy → verdict |
| `gw05_scene.py` | GW05 event stream; `--admission off|on` (off = frozen ingest) |
| `test_admission.py` | 5 synthetic tests, no GW content |

One principle, *the signal is recorded; the fact enters with a status*, covers both defects:

- **D1.** A handler `BLOCK` + `conflicts` becomes a committed `CONFLICT` record with status OPEN. It carries `PARTIES` (the incoming fact and the existing current records it clashes with) and `REFERS_TO` edges with roles `CONFLICT_PARTY` and `VIOLATED_RULE`. Nothing is deleted.
- **D2.** An UNCHECKED dependency no longer vetoes ingest. The fact is committed. The UNCHECKED marker is committed with status OPEN and linked to the fact (`CHECKED_RECORD`, role `UNCHECKED_RECORD`), so the debt sits on the dependent record (A6.8).
- **Invariant (A3.2).** The verdict is GO only if every evidence item has a committed record; otherwise BLOCK.
- **Policy is data (A3.5).** `ADMISSION_POLICY_1` is an ordinary network record (`ON_CONFLICT`, `ON_UNCHECKED` = `ADMIT_WITH_RECORD` | `REFUSE`). Under `REFUSE` the fact is not admitted, but the signal is still recorded.

## Checks

- `--admission off` reproduces the sealed `GW05_RUN_N_C13.json` and `GW05_RUN_L_C13.json` exactly, ignoring only the added keys `ADMISSION`, `ADMISSION_ENABLED` and `OPEN_SIGNALS`. The A/B comparison is therefore clean.
- `test_admission.py`: 5/5 pass. Existing `test_family_executor.py`: PASS.

## Scene results (C1/C3 on)

| event | frozen | admission on |
|---|---|---|
| **L · F4** (I3 R6 S2 vs D17 under M5) | committed; BLOCK swallowed, no record | committed + **`F4_1_CONFLICT_1`** (parties `F4_IN_1`, `D17`; rule M5); still in the F12 registry |
| **N · F4, F7, F8, F10** | nothing committed; world frozen | all 7 facts committed, each with 5 linked UNCHECKED markers (35 in total) |
| **N · F11** | no candidates (I8 never entered) | **RQ_F6 → BOUND I8**. The D2 cascade is gone |
| L · F8 | no OPEN, no UNCHECKED | unchanged: this is **D3**, not in scope |
| F12 | stale `OPEN_ASK_*` remains | unchanged: this is **D4**, not in scope |

## What the scene exposed (new, for the workshop)

1. **Marker flood.** In N, every fact gets one marker per unexecutable law: 35 OPEN markers, and they dominate the registry. The debt is honest, but the registry stops being readable. Candidate fix: one debt record per *unexecutable law*, with each dependent fact linked to it, instead of one marker per (fact × law). This is the A6.8 idea that "debt follows dependency" stated in graph form.
2. **The conflict attaches to the clash, not to a cause.** `F4_1_CONFLICT_1` names the parties and the rule. It does not decide which party is wrong, and it should not. Resolving it is an OPEN for an upper layer or a source check (A8.10: grounding ≠ verification).
3. **Under REFUSE, the marker refers to a fact that never entered the network.** The reference is left dangling on purpose, so the refused proposal stays addressable. Whether refused proposals should become their own record type is still open.

## Next in the workshop

D3 (an "operation not supported" result on a dependent rule becomes UNCHECKED) is now one branch in `compose_evidence`. D4 (the ASK status transition on bind) and the marker-flood fix come after that.

---

## WS02 — D3: an unsupported operation becomes UNCHECKED

**Status: WORKSHOP RESULT, works on scene GW05.**

**Change.** In `compose_evidence`, a dependent rule's result counts as `UNCHECKED` with reason `OPERATION_UNSUPPORTED` when its verdict is `NEED` and it has a stop of the form `missing: "operation …"`. Any other `NEED` (missing data, missing consequent) is not about whether the rule can check, so it does not count. A test covers this.

**Checks.**
- `--admission off` still reproduces the sealed N/L C13 logs exactly.
- `test_admission.py`: 7/7 pass.

**Scene results (L, C1/C3 on).**

| event | WS01 | WS02 |
|---|---|---|
| F7 (I5 R2 3) | committed, silent | committed + UNCHECKED by M2 |
| F8 (I7 R1 B2) | committed, silent | committed + UNCHECKED by M3 |
| F8 (I7 R2 2) | committed, silent | committed + UNCHECKED by M2 |
| F12 open signals | 1 (the F4 conflict) | 4 |

N is unchanged, because its rules were already EXECUTOR_HOLE / SCHEMA_DRIFT.

**Honest reading.** The book expected a visible OPEN for the B2 mismatch at F8. That is still not produced: M2 cannot execute in L because of the dictionary defect. What WS02 now makes visible is that the check could not be performed, and that is the correct signal while M2 is unreadable. The B2 mismatch itself needs a working M2, which is the dictionary fix, not D3.

**Next.** D4 (the ASK status transition on bind), then the marker flood (one debt record per unexecutable law).
