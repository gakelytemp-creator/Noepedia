# Experiment 001 — Pre-Run Schema Audit

> **Status:** completed before any experimental result was observed.

The first frozen fixture contained a methodological flaw.

The target task asked which net the "5V output" connector J2 should expose, but the only place that identified J2 as the output connector was its human-readable label.

That would violate the architecture's own rule:

> **identity and operational knowledge must not be smuggled through labels.**

If the run had proceeded unchanged, a correct answer could have been produced by reading the label rather than traversing the explicit relational field.

Therefore, before running the experiment, one explicit relation was added:

~~~text
R18:
J2 → EXPOSES_NET → VOUT
network: NET_FUNCTION
status: settled
~~~

Now the controlled mismatch is structural:

~~~text
FUNCTION NETWORK:
J2 → EXPOSES_NET → VOUT

CONNECTIVITY NETWORK:
J2 → CONNECTED_TO → VIN   [R11, deliberately wrong]
~~~

The experiment can now ask whether the field localizes the disagreement between distinct relation cuts.

No output result had been observed before this correction.

The change is preserved in Git history rather than hidden.
