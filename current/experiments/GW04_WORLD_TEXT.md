# GW04 — world text (solver-visible)

All identifiers are opaque. Do NOT guess meaning from names. Use only the records and laws below.
Numbers are ordinary integers; `=` and `+` have their arithmetic meaning.

## Object classes
- Nodes: N1, N2, N3, N4, N5, N6
- Links: K1, K2, K3, K4, K5, K6 (only these links are known at start)
- Status values: Z1, Z2

## Predicates
- Q1 : link → node (endpoint)
- Q2 : link → integer (magnitude)
- Q4 : link → node (the endpoint the magnitude is directed toward)
- Q6 : link → status value

## Initial network N0 (all SUPPORTED, CURRENT; PROVENANCE=SRC_INIT)
A1  K1 Q1 N1      A2  K1 Q1 N2
A3  K2 Q1 N2      A4  K2 Q1 N3
A5  K3 Q1 N2      A6  K3 Q1 N4
A7  K4 Q1 N3      A8  K4 Q1 N5
A9  K5 Q1 N4      A10 K5 Q1 N5
A11 K6 Q1 N5      A12 K6 Q1 N6
A13 K1 Q2 10      A14 K1 Q4 N2
A15 K2 Q2 6       A16 K2 Q4 N3
A17 K4 Q2 5       A18 K4 Q4 N5
A19 K6 Q2 10      A20 K6 Q4 N6

## Laws (addressable, CURRENT)
L1  Every link has exactly two Q1 targets, and they are different nodes.
L2  For every node other than N1 and N6: the sum of Q2 over links whose Q4 is that node equals the sum of Q2 over the other links that have that node as a Q1 target. L2 may be used to derive a missing Q2/Q4 only when the set of links having that node as a Q1 target is declared closed (L3) and exactly one adjacent link lacks Q2/Q4. A derived record must refer to its premises and to L2 and L3.
L3  Closure declaration: the set of links having N2 as a Q1 target is closed (it is exactly {K1, K2, K3}). No closure is declared for any other node.
L4  Q2 and Q4 of a link are single-valued: at most one current value each.
L5  If (K Q6 Z2) is current, then (K Q2 0) must hold for that link.

Source classes: TXT* = text report, SEN* = sensor. Source assertions enter only through PROPOSE → CHECK → COMMIT with their provenance and time.

## Event stream (process strictly in order)
E1  TASK: determine Q2 and Q4 of K3.
E2  TASK: determine Q2 of K5.
E3  SEN1 at t1 asserts: K5 Q2 5 ; K5 Q4 N5
E4  TASK: check L2 at node N3 against the current records.
E5  TXT1 at t2 asserts: K3 Q6 Z2
E6  TASK: compute the sum of Q2 over all known links.
E7  TASK: needed: some link X with (X Q1 N3) and (X Q1 N4). Create what is lawful; bind only if lawful.
E8  TXT2 at t3 asserts: K7 Q1 N3 ; K7 Q1 N4
E9  SEN2 at t4 asserts: K7 Q2 1 ; K7 Q4 N4
E10 TASK: re-check L2 at node N3. Then output the final registry.

## Output required
For EACH event: operations used, NETWORK DELTA, STOP card if any (STOP_CLASS GO / ASK / BLOCK / NEED, with WHERE, WANTED, AVAILABLE, MISSING, CAN_ASK_OUTSIDE, QUERY), and NEED if any.
At the end: all records created or changed, all HISTORICAL marks, final OPEN registry (every unresolved OPEN), final STOP map, final ASK list, final NEED map.
Do not invent predicates, objects or laws. Do not use common-sense meaning of anything.
