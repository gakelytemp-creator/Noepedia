# Experiment 037 — Preregistered Third Independent Knowledge-Revision Loop

> Status: preregistered before inspecting rows 650,001..705,000.

## Purpose

Experiments 033 and 036 confirmed two knowledge-revision loops.
Experiment 037 asks whether the same architecture transfers to a third relation family.

Rule under test uses only H1 and Reservoirs.

## Frozen calibration

Use rows 1..50,000.
Fit separate deterministic 1-D k-means (k=2) to H1 and Reservoirs.
Map each independently to STATE_LOW / STATE_HIGH using its own midpoint threshold.

## OLD rule

H1_STATE == RESERVOIRS_STATE

## Windows

discovery = rows 650,001..655,000
confirmation = rows 700,001..705,000

## Frozen candidate family

Candidate model: one channel changes first while the other remains in the previous source state for a short interval.

Candidate dimensions:
- source: H1 or Reservoirs
- transition: LOW_TO_HIGH or HIGH_TO_LOW
- lag N: 1, 2, 5, 10, 20, 40, 80 rows

Outside the lag interval expected TARGET = current SOURCE.
Inside rows 0..N after the selected SOURCE transition expected TARGET = SOURCE state immediately before transition.

## Discovery selection

For every candidate report old mismatches, revised mismatches, corrected mismatches, introduced mismatches, and net mismatch reduction.

Select by:
1. maximum net mismatch reduction
2. smaller N
3. source order H1 then Reservoirs
4. transition order LOW_TO_HIGH then HIGH_TO_LOW

If best net reduction <= 0: NO_DISCOVERY_CANDIDATE.

## Confirmation

Freeze selected candidate unchanged.
Build OLD and REVISED rules in one Noepedia field.
Evaluate both using the frozen Experiment 003 evaluator.

## Scientific classes

THIRD_REVISION_LOOP_CONFIRMED:
revised confirmation mismatch fraction < old mismatch fraction and net reduction > 0.

THIRD_REVISION_LOOP_NOT_CONFIRMED:
candidate exists but confirmation does not improve.

NO_DISCOVERY_CANDIDATE:
no positive discovery candidate.

Strong descriptive flag: confirmation relative mismatch reduction >= 50%.

## OPEN handling

OPEN is refined, never deleted.

## Claim boundary

A positive result establishes only that the third relation family passes the same revision architecture on untouched data.
It does not establish causal mechanism or physical truth.