# WS08 — the ASK is a supported object too

**Status: WORKSHOP RESULT, works on scene GW05 + the synthetic P1/P2 extension of WS07.**
Changes: `watch.py` (ambiguity tracking), `resolution.py` (effective ASK state), `gw05_scene.py` (the registry view uses the effective state when resolve-asks is on), `test_watch.py` (+7 tests, 17 in total).

One principle, two invariants (GPT's formulation):

> An ASK is produced from a basis and stands only while its basis stands.
> **I1.** |candidates| > 1 → a disambiguation ASK that cuts the candidate set.
> **I2.** The effective state of an ASK is a function of its support graph, not just its last stored status.

## I1 — ambiguity is a record and asks the cutting question

- When the watch sees more than one candidate, it writes `AMB_<rq>_<scope>_<method>_N<n>` (`TYPE = AMBIGUOUS_CANDIDATES_ON`, `CANDIDATES`, `N`, scope, method; status OPEN). This is a snapshot claim like candidacy (A12.3).
- It raises one ASK: "which of [I8, I9] is ?X for RQ_F6? (any answer leaves 1 of 2)". An unchanged ambiguous set does not ask again.
- When the set becomes sole again, the ambiguity record becomes HISTORICAL. Its ASK is ANSWERED by the new sole-candidacy claim (`ANSWERED_BY` edge).
- **Supersession.** The old joint ASK ("find any X with G1 and G4") is no longer the right question once X is known but not chosen. The new ASK carries a `SUPERSEDES` edge to it. The old one reads SUPERSEDED while at least one candidate is known (its own basis; see WS08b). This was found on the scene (see below), not designed beforehand.

## I2 — effective ASK state

`effective_ask_state(ask)`:

| stored | condition | effective |
|---|---|---|
| any | a SUPERSEDES edge whose own basis holds: at least one candidate known for the requirement | `SUPERSEDED` |
| OPEN | disambiguation ASK whose ambiguity record is no longer OPEN and which got no answer | `OBSOLETE` |
| ANSWERED | answered by a binding whose support graph is SUPPORTED | `ANSWERED` |
| ANSWERED | answered by a binding whose support is lost (REVIEW_REQUIRED) | `OPEN_BY_SUPPORT_LOSS` |
| ANSWERED | answered by another record that is no longer CURRENT | `OPEN_BY_SUPPORT_LOSS` |
| ANSWERED | binding with no SUPPORTED_BY edges (pre-WS07 shape) | `ANSWERED` (no graph to read) |
| other | — | stored |

The stored status is never rewritten. `unanswered_ask_stops()` and the scene registry read the effective state.

## Scene (L; N identical in structure), P2 after the synthetic I9

| | WS07b | WS08 |
|---|---|---|
| open ASKs, no mandate | none (gap 1) | `OPEN_ASK_5`: "which of [I8, I9] …" |
| joint ASK `OPEN_ASK_4` | stuck at ANSWERED (gap 2) | SUPERSEDED by `OPEN_ASK_5` |
| registry | RQ_F6 reopened | + `AMB_RQ_F6_…_N<n>`, `OPEN_ASK_5` |
| ONE_SHOT | renew-mandate ASK | the disambiguation ASK **and** the renew-mandate ASK. They are different questions to different addressees (source vs issuer) |

Without supersession, the first run showed both the reopened joint ASK and the disambiguation ASK as open. That is two questions for one gap, which is exactly the question-efficiency failure A8.4/A8.5 warns about.

## Checks

- F1–F12 are identical to WS07b in all six runs (N/L × three mandate modes); WS08 only acts once two candidates exist.
- `ablation_gw05.json` regenerates byte-identical, and `--admission off` still reproduces the sealed logs.
- Tests: admission 11/11, resolution 4/4, dictionary 7/7, watch 17/17. The new tests are: ambiguity record + cutting ASK; unchanged ambiguity asks once; answered when sole again; support loss with a rival → SUPERSEDED; support loss without a rival → OPEN_BY_SUPPORT_LOSS.

## WS08b — revision after GPT review: supersession needs its own basis

**GPT's edge case.** Supersession was tied to the superseding ASK's *stored* status being OPEN. The failing sequence:
1. the joint ASK is answered by the I8 binding;
2. I9 appears, and the binding loses its basis;
3. the disambiguation ASK supersedes the joint ASK;
4. I9 vanishes, and the disambiguation ASK is ANSWERED by the new sole claim;
5. there is no rebind.

From that point supersession lapsed, and the joint ASK read `OPEN_BY_SUPPORT_LOSS`. The demon was again asking "find X" while X was sole-known.

**Fix (GPT's preferred route).** The `SUPERSEDES` edge now carries its own basis: `REQUIREMENT`, and "at least one known candidate for REQUIREMENT". `supersession_holds()` reads it from the graph: a CURRENT sole candidacy, or an OPEN ambiguity. "Find any X" becomes the right question again only when every candidate is gone.

**Found while testing the fix.** In that all-gone case the disambiguation ASK "z or w?" still read OPEN, although its ambiguity record was HISTORICAL. A disambiguation ASK whose ambiguity is gone and which got no answer now reads `OBSOLETE`. So exactly one right question remains open.

**Regressions.**
- `test_sole_again_without_rebind_keeps_joint_ask_closed` (GPT's test): the joint ASK is SUPERSEDED, and no ASK is effectively open.
- `test_all_candidates_gone_reopens_joint_ask`: the joint ASK is OPEN_BY_SUPPORT_LOSS, the disambiguation ASK is OBSOLETE, and the effectively open set is exactly [joint ASK].

**Scene.** P2 in all six runs: the registry and the open ASKs are as before. F1–F12 are identical to WS07b, ignoring the new watch fields. The ablation JSON is byte-identical.

**Packaging.** The previous archive contained `__pycache__/` because `py_compile` ran after the cleanup. Cleanup now runs last.

## Not done (honest scope)

- The disambiguation ASK lists candidates. It does not rank questions by information gain over *decisions* (A8.5). With two candidates every answer cuts equally, so the scene cannot tell the difference.
- Who answers it (source vs upper layer) is not routed. It is a plain ASK.
