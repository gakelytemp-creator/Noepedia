# GW01 — solver input (projections only)

All identifiers are opaque. Do NOT guess meaning from names. Use only the records and rules below.

## Initial network N0 (all STATUS=SUPPORTED, CURRENT; PROVENANCE=SRC_INIT unless stated)
T1  O3  P1 O1
T2  O4  P2 O3
T3  O11 P2 O3
T4  O4  P3 S1
T5  O11 P3 S1
T6  O8  P3 S2
T7  O9  P1 O2
T8  O6  P1 O1      ; PROVENANCE=VIS0 ; TIME=t0
T9  O7  P1 O1

## Rules (addressable, CURRENT)
R1  P1 is SINGLE_CURRENT_TARGET: an object has at most one current P1 target.
R2  (X P2 Y) and (Y P1 Z)  => derive (X P1 Z). Derivation authorized (CREATE_ADDRESS allowed), must REFERS_TO premises and rule.
R3  (X P1 Y) and (Y P1 Z)  => derive (X P1 Z). Same authorization as R2.
R4  If (Y P3 S1) then records of form (X P1 Y) are not observable by source class VIS.
R5  For P1 under R1: a P1 assertion with later TIME supersedes an earlier one (earlier becomes HISTORICAL, not deleted).
R6  P4 and P5: no closure rule exists. Absence of a P4/P5 record says nothing.
C1  Scene constraint: (O7 P1 O1) must remain current for the whole scene.

Source classes: VIS* = vision, TXT* = text, EVS* = event stream. Vision samples use their own ids (v*) and must be bound to O-ids only with sufficient support.

## Event stream (process strictly in order)
E1  TXT1 asserts: O5 P1 O1
E2  VIS1 at t1 reports a sample v1 with: (v1 P2 O3), (v1 P3 S1)
E3  TASK: determine current P1 target of O4 at the level of {O1,O2}.
E4  TASK: make (O7 P1 O2) current.
E5  TASK: needed: some X with (X P4 O8), (X P1 O1), (X P5 TRUE). Create what is lawful; bind only if lawful.
E6  TASK: arrange to be notified when (O4 P3 S3) becomes current.
E7  EVS1 at t2 asserts: O6 P1 O2
E8  EVS1 at t3 asserts: O4 P3 S3   (S3 ≠ S1)
E9  VIS2 at t3 reports: O5 P1 O4
E10 TASK: revisit the E5 need.
E11 TXT2 asserts: O5 P4 O8 ; O5 P5 TRUE
E12 TASK: revisit the E5 need again. Then output final registry.

## Your output
For EACH event: primitive operations used, NETWORK DELTA, STOP (if any, as STOP CARD with STOP_CLASS GO/ASK/BLOCK/NEED), and NEED (if any).
At the end: final list of all CURRENT records you created/changed, all HISTORICAL marks, final OPEN registry, final NEED map.
Follow DEMON_CORE_SPEC.md strictly. Do not invent predicates or meanings.
