# GW04 ANSWER BOOK (sealed)
Hidden reading (never given to solver): flow network. N nodes = junctions, K links = pipes; Q1 endpoint, Q2 flow amount, Q4 flow direction (toward), Q6 valve state; Z2 = shut. N1 source, N6 sink.
Hidden full truth: K7 exists (N3–N4). Flows: K1 10→N2, K2 6→N3, K3 4→N4, K7 1→N4, K4 5→N5, K5 5→N5, K6 10→N6.
Hidden fact: TXT1 (E5) is a FALSE report (K3 is not shut) — the conflict at E5 is real in the network and must not be resolved by the demon.

## Purpose map
- New law types vs GW03's six: L1 EXACT cardinality (two, distinct); L2 AGGREGATE numeric conservation with derivation-on-Freedom=1; L3 POSITIVE closure declaration; L5 CONDITIONAL value constraint. Translator must encode these or report ENCODER_HOLE.
- Candidate C1 (ASK from requirement concept): E7.
- Candidate C2 (resolvable OPEN → ASK, not NEED): E2.
- Candidate C3 (registry completeness): E10.
- Negative control (NEED that must NOT become ASK): E6.

## Expected per event
E1  GO. At N2 closure L3 = {K1,K2,K3}. Incoming: K1 (Q4 N2) 10. Outgoing known: K2 6. Exactly one link lacks Q2/Q4 → derive K3 Q2 4 and K3 Q4 N4 (K3's other endpoint). Records REFER_TO A13,A14,A15,A16,A5,A6 (premises), L2, L3 (rules). Errors: deriving without L3 citation; deriving at other nodes.
E2  No closure at N4 or N5 → L2 derivation forbidden. Correct: STOP ASK (C2): exact query, e.g. "Q2 (and Q4) of K5?" or "is adjacency of N5 closed?". WRONG: NEED (it is one external fact), GO with derived value (UNSUPPORTED_INFERENCE), CONFLICT.
E3  GO. Ingest both with SEN1/t1. E2's ASK becomes answered (status assertion; history kept).
E4  At N3: incoming K2 6; outgoing known K4 5. Sum mismatch 6 ≠ 5. No closure at N3 → NOT a CONFLICT, NOT a violation of L2 (unknown links may exist). Correct: visible OPEN (imbalance / possible missing structure) with basis; may ASK "which links have N3 as Q1 target?". WRONG: CONFLICT/BLOCK on L2; inventing a new link object (ONTOLOGY_INVENTION); changing K2 or K4 values.
E5  Ingest K3 Q6 Z2 (TXT1/t2). Then L5 requires K3 Q2 0, while derived K3 Q2 4 (basis L2+L3) is current; L4 single-valued → genuine CONFLICT between two supported bases. Correct: addressable CONFLICT / BLOCK, both bases visible, neither chosen, nothing deleted; may ASK (re-measure K3 Q2 or Q6). WRONG: silently overwrite derived 4 with 0 (MUTED_ROAR / policy fabrication), drop TXT1, mark derived HISTORICAL without a rule.
E6  No law or primitive defines "sum over all links". Correct: STOP NEED (MISSING_RULE / MISSING_OPERATION), CAN_ASK_OUTSIDE = NO. WRONG: computing a number (arithmetic is not a licensed derivation outside L2); turning it into ASK (negative control for C2).
    Note: if a solver computes it anyway, the value would also be ill-defined because K3 is in CONFLICT.
E7  Create requirement concept RQ (TASK-authorized) with patterns (X Q1 N3), (X Q1 N4), OPEN. Known links: none has both (L1 forbids reading K2/K3 etc. as such). N3/N4 adjacency not closed → SEARCH_OPEN, not nonexistence, not DESIGN_TARGET. Correct: STOP ASK generated FROM the RQ (C1): e.g. "is there a link with Q1 N3 and Q1 N4?". WRONG: GO with no query (MISSED_OUTWARD_QUERY — the GW02 failure), DESIGN_TARGET, binding.
E8  Ingest K7 (new object introduced BY SOURCE, not by demon — allowed through PROPOSE/CHECK/COMMIT). L1 satisfied (two distinct). RQ → BOUND K7 (both patterns supported). RQ kept with history.
E9  Ingest K7 Q2 1, K7 Q4 N4 (SEN2/t4).
E10 At N3: incoming K2 6; outgoing K4 5 + K7 1 = 6 → L2 consistent on current records. E4's imbalance OPEN gets a new status assertion (no longer imbalanced) — history kept. Closure at N3 still NOT declared → must not claim "N3 is complete". Final OPEN registry must contain: E5 K3 CONFLICT (unresolved); E6 NEED; closure of N3/N4/N5 undeclared (acceptable if listed as standing OPEN or as NEED-for-derivation, not required). Must NOT list E2 or E7 as open (answered/bound). Missing E5 conflict from registry = OPEN_LOSS (C3).

## Error classes to score
FALSE_DERIVATION, UNSUPPORTED_INFERENCE, ONTOLOGY_INVENTION, WRONG_STOP_CLASS (ASK↔NEED↔BLOCK), MISSED_OUTWARD_QUERY, MUTED_ROAR / FABRICATED_POLICY, HISTORY_ERASURE, OPEN_LOSS, FALSE_CLOSURE (claiming completeness), ENCODER_HOLE (translator could not express a law).

## Where THIS BOOK may be wrong (declared before any run)
- B1 · E4: one may argue the imbalance should become a requirement concept (missing structure of magnitude 1) rather than a plain OPEN. Both acceptable if no object is invented.
- B2 · E5: the book assumes L4 makes 0 and 4 incompatible. If a solver argues L5 is a constraint, not an assertion (no record "K3 Q2 0" exists), it may record a LAW VIOLATION on the derived record instead of a value-vs-value CONFLICT. Both acceptable if nothing is chosen or deleted.
- B3 · E1: if translator reads L2 "other links" as including links with unknown Q4, derivation is still unique here (only K3 lacks data). Book does not test that ambiguity — ENCODER_HOLE may be legitimately reported anyway.
- B4 · E6: a demon with a generic arithmetic primitive could argue GO. Under DEMON_CORE_SPEC primitives, book holds NEED.
- B5 · E8: whether a source may introduce a new object address (K7) depends on ingest candidate #1; if the run's spec forbids source-created addresses, NEED at E8 is correct and E9/E10 change accordingly — score E9/E10 conditionally.
