# Experiment 004 — Multi-Rule Deterministic Field

Experiment 004 tests whether the deterministic evaluator can apply multiple explicit rule objects across multiple object types without domain-specific branches.

## Files

- `BRIEFING.md` — purpose and frozen expectation
- `INPUT.json` — three-rule synthetic field
- `RUN_RESULT.md` — observed local execution result

## Expected outcomes

~~~text
J2_P1  → FORMAL_MISMATCH
J2_P2  → CONSISTENT
C1     → CONSISTENT
C2     → FORMAL_MISMATCH
U1     → CONSISTENT
OPEN_01 preserved
~~~

## Current boundary

The evaluator now supports multiple rule instances, but all rules still share the same structural form:

~~~text
scope + input predicate + required predicate + SAME_NET
~~~

This experiment therefore tests **generic reuse of one rule grammar**, not arbitrary rule semantics.


## Independent verification

For a complete reproduction procedure, see [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md).

Expected structural output is frozen in [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json).

Automatic verification:

~~~bash
python experiments/experiment_004/verify_output.py
~~~

Expected result:

~~~text
Experiment 004 verification: PASS
~~~
