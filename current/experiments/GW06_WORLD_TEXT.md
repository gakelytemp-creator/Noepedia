# GW06 — world text (solver-visible)

All identifiers are opaque. Do NOT infer meaning from names. Use only the records and laws stated here.
Values written as digits are integers with ordinary arithmetic. Nothing else is assumed about them.

## Kinds of objects
- Units: U1, U2, U3, U4, U5, U6, U7 (further units may appear later through reports)
- Hubs: H1, H2, H3
- Carriers: W1, W2, W3
- Tags: XT1, XT2, XT3
- Phases: XS1, XS2

## Relations
- Y1 : unit → hub
- Y2 : unit → integer
- Y3 : hub → integer
- Y4 : unit → tag
- Y5 : unit → carrier
- Y6 : unit → phase
- Y7 : hub → integer

## Starting records (each SUPPORTED and CURRENT; source SRC_INIT)
J1  U1 Y1 H1
J2  U2 Y1 H1
J3  U3 Y1 H1
J4  U4 Y1 H1
J5  U5 Y1 H2
J6  U6 Y1 H2
J7  U7 Y1 H3
J8  H1 Y3 20
J9  H2 Y3 11
J10 U1 Y2 6
J11 U2 Y2 5
J12 U4 Y2 4
J13 U5 Y2 7
J14 U1 Y5 W1
J15 U1 Y5 W2
J16 U2 Y5 W3
J17 U3 Y5 W1
J18 U3 Y5 W3
J19 U2 Y4 XT1
J20 U5 Y6 XS1
J21 H1 Y7 4
J22 H2 Y7 3

## Laws (addressable, CURRENT)
YL1  A unit has at most one current Y4 value.
YL2  Every unit is tied by Y5 to exactly two carriers, and the two must be different from each other.
YL3  Apart from hub H3, every hub's Y3 value is equal to the sum of Y2 over the units whose Y1 target is that hub. This equality may be used to infer a missing Y2 of a unit only when YL4 declares that hub's set of units complete and that unit is the only unit of the hub without a Y2 value. An inferred record must cite its premises together with YL3 and YL4.
YL4  Completeness declaration: the units having H1 as their Y1 target are exactly U1, U2, U3 and U4. No completeness is declared for H2 or H3.
YL5  Whenever (U Y6 XS2) is current for a unit U, (U Y4 XT3) must also be current for that same unit.
YL6  For every hub, the number of units whose Y1 target is that hub must not be greater than the hub's Y7 value.

Reports enter only through PROPOSE → CHECK → COMMIT, with their source and time. Source classes: SRC* = report.
A retraction report says that an earlier record is no longer current. It never deletes that record.

## Event stream (process strictly in order)
X1  TASK: determine Y2 of U3.
X2  TASK: determine Y2 of U6.
X3  TASK: check YL2 for U2.
X4  SRC1 at t1 reports: U2 Y6 XS2
X5  SRC2 at t2 reports: U7 Y2 9
X6  TASK: determine which hub has the most units.
X7  TASK: needed: some unit X with (X Y5 W2) and (X Y5 W3). Create what is lawful; bind only if lawful. The requester grants authority to bind this need automatically, once, as soon as binding becomes lawful (one use only).
X8  SRC3 at t3 reports: U8 Y1 H2 ; U8 Y2 4
X9  SRC4 at t4 reports: U9 Y5 W2 ; U9 Y5 W3
X10 TASK: output the current OPEN registry.
X11 SRC5 at t5 reports: U10 Y5 W2 ; U10 Y5 W3
X12 SRC6 at t6 reports retraction: U10 Y5 W3 is no longer current.
X13 TASK: revisit the X7 need.
X14 TASK: output the final registry.

## Output required
For EACH event: operations used, NETWORK DELTA, STOP card if any (STOP_CLASS GO / ASK / BLOCK / NEED, with WHERE, WANTED, AVAILABLE, MISSING, CAN_ASK_OUTSIDE, QUERY), and NEED if any.
At X10 and X14: every unresolved OPEN, every ASK still unanswered, every NEED.
Do not invent relations, objects, laws or meanings. Do not use common sense about what anything is.
