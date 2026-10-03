# Experiment 001 — Dry-Run Task

Use only the frozen fixture in `field.json`.

## Target task

Determine:

1. which net J2 should be connected to for the recorded 5V output interpretation to be coherent;
2. which stored relation is the mismatch candidate;
3. which minimal revision is required;
4. whether OPEN_01 should be closed by this task.

## Rules

- Do not add new evidence.
- Do not redefine the object.
- Preserve provenance.
- Do not close OPEN_01 merely because the task can be answered without it.
- Count the smallest relation subset sufficient to justify the answer.

## Expected evaluation outputs

- task cut relation IDs;
- mismatch relation ID;
- proposed replacement relation;
- OPEN state after revision;
- unrelated relations touched;
- provenance retained.
