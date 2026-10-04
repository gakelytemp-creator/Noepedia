# Experiment 036 — Second Independent Knowledge-Revision Loop

Experiment 036 tests whether the Noepedia knowledge-revision cycle repeats on a different relation family.

This experiment does not use DV_eletric or Motor_current in the rule under test.

Relation family:
TP2 pressure state vs TP3 pressure state.

Two separate windows are used:
- discovery window = rows 550,001..555,000
- confirmation window = rows 600,001..605,000

The discovery window may select one rule candidate from a preregistered finite candidate family.
The selected candidate is then frozen and evaluated on the untouched confirmation window through the frozen Noepedia evaluator.