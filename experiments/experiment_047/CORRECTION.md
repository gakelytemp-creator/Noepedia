# Experiment 047 — Wrapper Decision-Semantics Correction

The first execution completed the scientific calculation and graph materialization, but the workflow exited with failure because the Experiment 047 wrapper incorrectly assumed:

`scientific non-confirmation -> REJECT`

Experiment 044 defines a distinct third state:

`REMAIN_OPEN`

In the observed external case:
- the selected lag hit the preregistered upper search boundary (30 cycles);
- the majority-null error was zero, so the required majority comparison was not evaluable as a positive advantage;
- the generic Experiment 045 harness therefore correctly returned `REMAIN_OPEN`.

Correction:

The Experiment 047 wrapper now expects `REMAIN_OPEN` when a non-confirmed result is caused by an unresolved search boundary or an unavailable/zero-error required null.

No dataset window, family selection rule, candidate search, threshold, null definition, success criterion, or scientific result changed.