# Experiment 033 — Noepedia Rule Revision and OPEN Closure Test

Experiment 033 returns the learned LOAD_OFF temporal structure to the Noepedia core.

New untouched window: rows 450,001..455,000.

The field contains both:

OLD RULE: DV binary state must equal Motor_current binary state.

REVISED RULE:
- LOAD_ON requires HIGH current immediately.
- After LOAD_OFF, rows 0..40: HIGH expected.
- Rows 41..52: explicit TRANSITION_OPEN zone.
- Rows >52: LOW expected.

The revised rule carries provenance from Experiments 027, 030, 031, and 032.