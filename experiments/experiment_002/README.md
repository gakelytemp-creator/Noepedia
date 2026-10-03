# Experiment 002 — Reproducibility Package

This directory preserves Experiment 002 as a frozen structured-relation-field run.

## Files

- `BRIEFING.md` — frozen conceptual purpose and scope before the run
- `INPUT.json` — exact structured field used for the run
- `PROMPT.txt` — exact prompt supplied to the fresh chat
- `RUN_METADATA.json` — known run metadata; unknown fields are explicitly marked
- `RESULT_PART_1.md` — verbatim result sections A–G
- `RESULT_PART_2.md` — verbatim result sections H–N
- `EVALUATION.md` — post-run evaluation
- `OPENs.md` — unresolved structures exposed by the run

## Reproduction rule

To reproduce:

1. Start a fresh chat/session.
2. Do not provide Experiment 001 results or evaluations.
3. Supply the exact contents of `PROMPT.txt`.
4. Preserve the full returned answer before interpretation.
5. Compare the result against `EVALUATION.md`.
6. Do not rewrite the frozen input after observing the result.

## Scientific status

This is a synthetic dry-run.

It demonstrates that an explicit relation + explicit rule structure can support formal mismatch derivation in an LLM-mediated read of the field.

It does **not** yet demonstrate deterministic code-level field execution or computational advantage.
