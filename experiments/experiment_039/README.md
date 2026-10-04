# Experiment 039 — Second Null-Protected Knowledge-Revision Loop Attempt

Experiment 039 tests a new relation family from the start with null protection.

Relation family:
Pressure_switch ↔ Reservoirs

Windows:
- calibration/orientation = rows 1..50,000
- discovery = rows 850,001..855,000
- confirmation = rows 900,001..905,000

The old rule maps the binary Pressure_switch state to a Reservoirs LOW/HIGH state.
The mapping orientation is frozen from calibration only.

Discovery searches a directional transition-lag correction.
Confirmation compares OLD, REVISED, majority-state null, and circular-shift temporal nulls.