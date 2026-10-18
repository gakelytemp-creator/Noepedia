# GW04 — cold encoder rule-record format contract

**Status: FROZEN INPUT CONTRACT**  
**Date: 2026-10-18**

This file may be shown to the cold encoder together with `GW04_WORLD_TEXT.md`.

Its purpose is to define **record shape**, not to suggest how any GW04 law should be interpreted.

## Record shape

Each law becomes one addressable rule record.

Minimum fields:

```text
addr        — opaque address of the law record
RULE_TYPE   — symbolic rule-family label
QUOTE       — exact source sentence/span from GW04_WORLD_TEXT.md
```

Additional fields may be introduced when needed to represent the law structurally.

A translation must remain **data only**:

- no executable functions;
- no branches;
- no hidden calls into the answer book;
- no derived event answers;
- no GW04-specific procedural code.

## RULE_TYPE is open, not a closed six-type vocabulary

The six GW03 rule families are examples of previous encodings, **not** the allowed ontology of GW04.

If a GW04 law cannot be represented faithfully by an existing RULE_TYPE, the cold encoder may create a new descriptive RULE_TYPE and the minimum structural fields needed to preserve the source law.

That is preferable to forcing a new law into an old type.

If the generic evaluator has no handler for the resulting type, the A/B run records an **EXECUTOR_HOLE** and continues without extending the evaluator.

If the encoder cannot produce a faithful structural record at all, record **ENCODER_HOLE**.

## Provenance

Every rule record must keep its source text in `QUOTE`.

The post-run audit must therefore be able to compare:

```text
WORLD TEXT
→ ENCODER RECORD
→ EVALUATOR BEHAVIOR / HOLE
```

without reconstructing the translator's intention.

## Example bias policy

`rules_gw01.py` is **not part of this neutral contract**.

If the cold-encoder session is nevertheless given `rules_gw01.py` as an example, that fact must be recorded before translation and the audit must treat possible attraction toward the GW03 six-type vocabulary as a known encoder-context bias.
