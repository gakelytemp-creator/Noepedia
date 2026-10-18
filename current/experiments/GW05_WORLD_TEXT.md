# GW05 — world text (solver-visible)

All identifiers are opaque. Do NOT infer meaning from names. Use only the records and laws stated here.
Values written as digits are integers with ordinary arithmetic. Nothing else is assumed about them.

## Kinds of objects
- Items: I1, I2, I3, I4, I5, I6 (further items may appear later through reports)
- Bins: B1, B2, B3
- Agents: G1, G2, G3, G4
- Marks: V1, V2, V3
- Conditions: S1, S2

## Relations
- R1 : item → bin
- R2 : item → integer
- R3 : bin → integer
- R5 : item → mark
- R6 : item → condition
- R7 : item → agent

## Starting records (each SUPPORTED and CURRENT; source SRC_INIT)
D1  I1 R1 B1
D2  I2 R1 B1
D3  I3 R1 B1
D4  I4 R1 B2
D5  I5 R1 B2
D6  I6 R1 B3
D7  B1 R3 12
D8  B2 R3 9
D9  I1 R2 5
D10 I2 R2 4
D11 I4 R2 6
D12 I1 R7 G1
D13 I1 R7 G2
D14 I1 R7 G3
D15 I2 R7 G2
D16 I2 R7 G4
D17 I3 R5 V1
D18 I4 R6 S1

## Laws (addressable, CURRENT)
M1  No item may be tied by R7 to fewer than three or more than three agents, and those three agents must all be different from one another.
M2  For each bin other than B3, the bin's R3 value equals the total of R2 over the items that have that bin as their R1 target. This equality may be used to infer a missing R2 of an item only when the bin's set of items is declared complete by M3 and that item is the single item in the bin lacking an R2 value. An inferred record must cite its premises together with M2 and M3.
M3  Completeness declaration: the items having B1 as their R1 target are exactly I1, I2 and I3. No completeness is declared for B2 or B3.
M4  An item has at most one current R5 value.
M5  Whenever (I R6 S2) is current for an item I, (I R5 V3) must also be current for that same item.

Reports enter only through PROPOSE → CHECK → COMMIT, with their source and time. Source classes: SRC* = report.

## Event stream (process strictly in order)
F1  TASK: determine R2 of I3.
F2  TASK: determine R2 of I5.
F3  TASK: check M1 for I2.
F4  SRC1 at t1 reports: I3 R6 S2
F5  TASK: determine the largest R2 value among all known items.
F6  TASK: needed: some item X with (X R7 G1) and (X R7 G4). Create what is lawful; bind only if lawful.
F7  SRC2 at t2 reports: I5 R2 3
F8  SRC3 at t3 reports: I7 R1 B2 ; I7 R2 2
F9  TASK: output the current OPEN registry.
F10 SRC4 at t4 reports: I8 R7 G1 ; I8 R7 G4 ; I8 R7 G2
F11 TASK: revisit the F6 need.
F12 TASK: output the final registry.

## Output required
For EACH event: operations used, NETWORK DELTA, STOP card if any (STOP_CLASS GO / ASK / BLOCK / NEED, with WHERE, WANTED, AVAILABLE, MISSING, CAN_ASK_OUTSIDE, QUERY), and NEED if any.
At F9 and F12: every unresolved OPEN, every ASK still unanswered, every NEED.
Do not invent relations, objects, laws or meanings. Do not use common sense about what anything is.
