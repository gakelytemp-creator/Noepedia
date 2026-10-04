# Experiment 033 — Preregistered Noepedia Knowledge-Revision Loop

> Status: core experiment preregistered before inspecting rows 450,001..455,000.

## Purpose

This experiment tests the full Noepedia revision cycle:

old rule -> formal mismatch -> OPEN -> evidence gathering -> revised provenance-bearing rule -> new field evaluation

## Untouched window

rows 450,001..455,000

## Frozen Motor_current regimes

LOW: Motor_current < 0.8821033735279131
HIGH: Motor_current > 3.4159886439831877
MID: otherwise

MID remains unresolved and is never silently forced LOW or HIGH.

## OLD rule

DV_eletric = 1 -> expected HIGH
DV_eletric = 0 -> expected LOW

This reproduces the original direct cross-path mapping assumption.

## REVISED rule

Derived from Experiments 027, 030, 031, and 032.

DV 0->1: expected HIGH immediately.

DV 1->0: let d be rows since the most recent LOAD_OFF transition.

d = 0..40: expected HIGH
d = 41..52: TRANSITION_OPEN; no HIGH/LOW equality verdict is asserted
d > 52: expected LOW

If the current DV state is 0 but no LOAD_OFF transition is present in available history, expected LOW.

The 41..52 zone is not treated as success; it is explicit unresolved tolerance.

## Core evaluator use

For every assessment with definite raw-current state, OLD_EXPECTED_CURRENT_STATE vs CURRENT_CANDIDATE_STATE is evaluated through the frozen Experiment 003 SAME_NET evaluator.

For every assessment outside TRANSITION_OPEN, REVISED_EXPECTED_CURRENT_STATE vs CURRENT_CANDIDATE_STATE is evaluated by the same frozen evaluator.

No verdict is inserted in the input.

## Provenance

The revised rule object cites EXP027, EXP030, EXP031, EXP032 and has epistemic status EMPIRICALLY_SUPPORTED_RULE, not FACT.

## Primary measurements

Report old and revised mismatch counts/fractions, TRANSITION_OPEN rows, MID unresolved rows, and mismatch reduction on the common evaluable subset.

## Preregistered result classes

REVISION_IMPROVES_FIELD iff revised mismatch fraction < old mismatch fraction on the common evaluable subset.

REVISION_DOES_NOT_IMPROVE_FIELD otherwise.

Strong descriptive flag: REVISION_REDUCES_MISMATCH_BY_90_PERCENT if relative mismatch reduction >= 90%.

No requirement of zero residual mismatch is preregistered.

## OPEN closure criterion

The original broad OPEN is refined, not deleted.

RESOLVED_COMPONENT: direction-dependent LOAD_OFF temporal exception.

REMAINING_OPEN: residual mismatches, transition-zone interpretation, minority long-tail events, physical mechanism.

## Claim boundary

Experiment 033 tests whether a learned provenance-bearing rule improves the Noepedia field on untouched data. It does not establish causal mechanism, fault, anomaly, or universal compressor law.