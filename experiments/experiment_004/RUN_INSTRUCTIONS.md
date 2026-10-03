# Experiment 004 — Independent Reproduction Instructions

## Goal

Reproduce Experiment 004 directly from the committed repository files, without using any prior chat context.

## Requirements

- Python 3.10+
- No external Python packages
- No LLM API
- No network access required after cloning/downloading the repository

## Files used

- `experiments/experiment_003/evaluator.py`
- `experiments/experiment_004/INPUT.json`
- `experiments/experiment_004/EXPECTED_OUTPUT.json`

## Run the evaluator

From the repository root:

~~~bash
python experiments/experiment_003/evaluator.py experiments/experiment_004/INPUT.json
~~~

The command prints one JSON document to stdout.

## Verify automatically

From the repository root:

~~~bash
python experiments/experiment_004/verify_output.py
~~~

Expected terminal result:

~~~text
Experiment 004 verification: PASS
~~~

If any required event is missing, an unexpected event appears, the rule count differs, or OPEN_01 is not preserved, verification fails with a non-zero exit code.

## Expected structural result

The evaluator should produce exactly five rule-evaluation events:

~~~text
J2_P1  → FORMAL_MISMATCH
J2_P2  → CONSISTENT
C1     → CONSISTENT
C2     → FORMAL_MISMATCH
U1     → CONSISTENT
~~~

Summary:

~~~text
rule_count = 3
FORMAL_MISMATCH = 2
CONSISTENT = 3
~~~

OPEN state:

~~~text
OPEN_01 preserved
open_records_unchanged = true
~~~

## Reproducibility boundary

The verification checks the **structural result**, not byte-for-byte JSON formatting or event ordering.

This matters because formatting changes should not count as scientific disagreement.

A failure means at least one expected structural event or preservation condition no longer holds.
