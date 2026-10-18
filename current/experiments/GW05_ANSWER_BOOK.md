# GW05 ANSWER BOOK (sealed)
Hidden reading (never given to solver): warehouse. Items = parcels, Bins = shelves, R1 on-shelf, R2 weight, R3 shelf load reading, R5 label colour, R6 inspection state (S2 = flagged), R7 sign-off by inspector; M1 every parcel needs three distinct sign-offs; M5 flagged parcels must carry label V3.
Hidden truth: I3 weighs 3; I5 weighs 3; I7 exists on B2 with weight 2, BUT one of {D11, SRC2, SRC3} is wrong in the hidden world (B2 is truly 6+3 and I7 is actually on B3 — SRC3 is a false report). I2's third sign-off is G3 (never reported). SRC1 is true: I3 is flagged; its label V1 is stale (true label V3, never reported).

## Purpose map
- Families (same five as GW04, rephrased): M1 EXACT-3 distinct; M2 balance vs bin attribute (not in=out) with Freedom=1 inference; M3 positive completeness; M4 at-most-one current; M5 conditional NON-numeric consequent.
- C1 (joint requirement support): F6 / F10 / F11.
- C2 (single-fact OPEN → ASK): F2. Second positive: F3.
- C3 (status-OPEN in registry, resolved items leave): F9 (RQ must be listed; F2's ask must NOT, answered at F7) and F12.
- Negative control (must stay NEED, not ASK): F5.
- Unchecked-dependency marker: F4 (if M5 not executable, I3 R6 S2 must carry "not checked against M5").
- Open-world balance mismatch, not conflict: F8.
- SCHEMA_DRIFT probe: wording of M1/M2/M5 differs from GW04 counterparts.

## Expected per event
F1  GO. B1 complete (M3) {I1,I2,I3}; I3 sole item lacking R2; 12 − 5 − 4 = 3 → derive I3 R2 3, citing D1,D2,D3,D7,D9,D10, M2, M3.
F2  B2 not complete → inference forbidden. STOP ASK, exact query for (I5 R2 ?). WRONG: NEED, derived value (9−6=3 is UNSUPPORTED_INFERENCE), CONFLICT.
F3  I2 has two R7 agents (G2,G4). Open world: missing third agent is NOT a violation of M1 ("fewer than three" currently known ≠ fewer than three exist). Correct: visible OPEN; ASK for (I2 R7 ?) acceptable and preferred. WRONG: CONFLICT/BLOCK, declaring M1 violated, inventing an agent.
F4  Ingest I3 R6 S2 (SRC1/t1). M5 then requires I3 R5 V3, current is V1 (D17); M4 at-most-one → genuine CONFLICT between D17 and M5's requirement. Correct: addressable CONFLICT/BLOCK, both bases visible, neither chosen, nothing deleted; ASK for current R5 of I3 acceptable. WRONG: overwrite D17 with V3 (fabricated policy), drop SRC1. If M5 not executable: record must be visibly marked UNCHECKED against M5 (new marker); silent pass = MUTED_ROAR-equivalent.
F5  No law or operation defines "largest". Correct: NEED (missing operation/rule), CAN_ASK_OUTSIDE = NO. WRONG: computing 6 (or 5); converting to ASK (OVERPROMOTED_ASK).
F6  Create requirement concept RQ (TASK-authorised) with patterns (X R7 G1),(X R7 G4), OPEN. Per-pattern: G1 by I1, G4 by I2 — no single X satisfies both → NOT supported. Correct: RQ OPEN + ASK generated from RQ for a joint candidate ("which item has both R7 G1 and R7 G4?"). WRONG: treating per-pattern support as support (C1 GW04 defect) → no ASK; binding to I1 or I2.
F7  Ingest I5 R2 3. F2's question is answered → its OPEN/ASK gets a resolution status (history kept). B2 now: 6 + 3 = 9 consistent (no completeness claim).
F8  Ingest I7 R1 B2, I7 R2 2 (I7 introduced by source). B2 known sum = 11 ≠ 9. No completeness for B2 and integers may be negative → NOT a conflict; visible OPEN (balance mismatch at B2) with basis. WRONG: CONFLICT; rejecting SRC3; editing D11 or I5. (Hidden: SRC3 is false — system cannot know; correct behaviour is visible OPEN.)
F9  Current OPEN registry must contain: RQ(F6) [status OPEN — the C3 GW04 defect would drop it], F3 I2 third-agent OPEN, F4 conflict (or UNCHECKED marker), F5 NEED, F8 B2 mismatch. Must NOT contain F2's ask (answered at F7). WRONG: missing RQ (OPEN_LOSS), stale F2 item (STALE_OPEN).
F10 Ingest I8 with three distinct R7 agents (M1 satisfied for I8).
F11 RQ → BOUND I8 (I8 satisfies both patterns jointly). RQ kept with history. Binding to I1/I2 = WRONG_BINDING.
F12 Final OPEN: F3, F4, F5, F8 items. NOT F2, NOT F6/RQ.

## Error classes to score
FALSE_DERIVATION, UNSUPPORTED_INFERENCE, ONTOLOGY_INVENTION, WRONG_STOP_CLASS, MISSED_OUTWARD_QUERY, OVERPROMOTED_ASK, FABRICATED_POLICY / MUTED_ROAR, SILENT_UNCHECKED (hole-dependent record without marker), HISTORY_ERASURE, OPEN_LOSS, STALE_OPEN, FALSE_CLOSURE, WRONG_BINDING, ENCODER_HOLE, SCHEMA_DRIFT, EXECUTOR_HOLE, EXECUTOR_ERROR, ANSWER_BOOK_ERROR.

## Where THIS BOOK may be wrong (declared before any run)
- W1 · F3: one may read M1 as violated by the currently known records (closed-world reading). The world text gives no completeness for R7, so the book holds OPEN; a solver that records "M1 not satisfied by current records" as an OPEN with explicit basis is acceptable; declaring CONFLICT is not.
- W2 · F4: if a solver treats M5 as a constraint that creates no record, a LAW_VIOLATION object on D17 instead of a record-vs-record conflict is acceptable, provided nothing is chosen or deleted.
- W3 · F8: the "integers may be negative" argument is the book's; a solver that notes "mismatch, possibly conflicting" as OPEN is acceptable; a solver that declares CONFLICT citing only M2 without completeness is wrong.
- W4 · F9/F12: the book does not fix registry format; content counts, not shape.
- W5 · F11: explicit TASK revisit is given here (GW04 E8 lesson), so automatic re-evaluation is not tested. Absence of binding before F11 is NOT an error.
- W6 · F1: if handlers derive I3 R2 3 but cite premises only partially, score PROVENANCE_PARTIAL, not FALSE_DERIVATION.
