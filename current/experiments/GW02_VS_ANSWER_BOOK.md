# GW02 vs GW01 ANSWER BOOK — post-unseal comparison

**Status: EXPERIMENTAL RECORD / POST-UNSEAL AUDIT**
**Date: 2026-10-18 · auditor: Claude (author of GW01 and of the answer book)**

## 0. Integrity

- `ANSWER_BOOK.md` sha256 at unseal: `3ba3627a145fb9bf9653b2c9782d6337542e61a9501f3be2774f867a9605b027` — **matches the sealed hash**.
- Compared against: `core/demon/GW01_RUN_LOG.txt` (repo state 2026-10-18, GW02 mechanical executor).
- Caveat: the answer book was written by the same person who wrote GW01, before any run. Its own errors are listed in §3.

## 1. Per-event verdict

| E | Answer book expected | GW02 mechanical | Verdict |
|---|---|---|---|
| E1 | ingest O5 P1 O1, GO, no fabricated position | GO, ingest | MATCH |
| E2 | AMBIGUOUS_MATCH O4/O11, OPEN, no merge | ASK, candidates [O4, O11], no merge | MATCH |
| E3 | derive O4 P1 O1 via R2, REFERS_TO premises + rule | GO, DV1 with provenance, answer O1 | MATCH |
| E4 | BLOCK (C1+R1), not NEED | BLOCK | MATCH |
| E5 | create RQ (3 patterns, OPEN); no bind; **STOP ASK** (query P4/P5) or NEED | RQ1 created, OPEN, no bind — **GO, no outward query** | PARTIAL — **MISSED_OUTWARD_QUERY** |
| E6 | trap record on (O4 P3 S3) | WATCH W1 + post-COMMIT re-evaluation | MATCH |
| E7 | T8 → HISTORICAL non-destructively, new current | T8 HISTORICAL, N7 CURRENT | MATCH |
| E8 | T4 not silently deleted; NEED/CONFLICT or flagged; trap fires | NEED + visible OPEN_MULT_P3; KAIROS fired | MATCH (better than book; see §3) |
| E9 | R4 issue flagged; R1-vs-hierarchy issue if raised; no "both fine" | BLOCK₁ (R4) + NEED₂ (R4 applicability depends on E8 multiplicity) | MATCH |
| E10 | RQ unbound, **ASK** | GO, RQ1 OPEN, no query | PARTIAL — **MISSED_OUTWARD_QUERY** |
| E11 | ingest both | ingest both | MATCH |
| E12 | bind RQ → O5 only if all supported; RQ kept | bound O5, OPEN history preserved | MATCH |

**Totals: 10 MATCH, 2 PARTIAL, 0 FAIL.** No false merge, no fabricated path, no stale-as-current, no history erasure, no invented ontology.

## 2. Deviations

### D1 · MISSED_OUTWARD_QUERY (E5, E10)
The only ASK produced in the whole run is the E2 identity question. The requirement concept RQ1 sat OPEN from E5 to E11 without any outward query, even though its missing patterns (X P4 O8, X P5 TRUE) are exactly formable questions. It was bound at E12 only because TXT2 happened to arrive. The IDEAL_TO_REAL step "requirement concept → choose the most informative outward contact" is not implemented in the mechanical demon.

### D2 · MISSED_ASK on a resolvable OPEN (E8 → E9)
OPEN_MULT_P3 (is O4 still S1?) is recorded as NEED, not ASK. It is askable ("which P3 value of O4 is current?"). Because it stayed unasked, E9's vision report (O5 P1 O4) was blocked by R4. In the hidden world that report was **true** (O5 is inside O4). The system stayed honest but became blind to a true observation, and the hidden truth "O5 inside O4" never entered the network. This is the price of an OPEN without a resolution route.

### D3 · Registry inconsistency
The final `OPEN:` list contains only OPEN_MULT_P3. The v1 identity ambiguity (E2) appears in the STOP MAP and the ASK list but not in the OPEN registry. This matches the DCT01 failure class "OPEN loss in final registry" in form, though the information is still visible elsewhere. Either the OPEN registry must include every unresolved OPEN, or the registry semantics must be stated.

## 3. Answer-book errors (auditor's own)

- **E8:** the book leaned toward CONFLICT. GW02's visible multiplicity OPEN is more correct: no rule makes S1 and S3 incompatible.
- **E9:** the R1-vs-hierarchy trap became moot because R4 blocked ingestion first. The book's "if raised" covered this; no penalty.
- **E5 candidate list** in the book is garbled ("O3? no (O3 P1 O1 yes!)"). It does not affect grading, since no binding was expected.

## 4. Candidate NEEDs (for a fresh, unseen world — not for GW01 again)

1. **ASK generation from requirement concepts:** each unsupported requirement pattern with a formable query yields an ASK card.
2. **OPEN → ASK promotion:** any OPEN whose resolution is a single external fact should be ASK, not NEED.
3. **Registry rule:** the final OPEN registry must contain every OPEN still unresolved, including identity OPENs.

These must not be tuned on GW01. GW01 has now been seen by every participant and is a training scene, not a test.
