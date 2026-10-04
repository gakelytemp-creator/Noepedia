# Experiment 036 — Preregistered Second Independent Knowledge-Revision Loop

> Status: preregistered before inspecting rows 550,001..605,000.

## Purpose

Experiment 033 completed one knowledge-revision loop for DV_eletric ↔ Motor_current.
Experiment 036 asks whether the same architecture can work on a second, independent relation family.

The rule under test uses only TP2 and TP3.
No DV_eletric or Motor_current relation participates in candidate construction or evaluation.

## Frozen calibration

Use rows 1..50,000.
Fit separate deterministic 1-D k-means (k=2) to TP2 and TP3.
Each channel is mapped independently to PRESSURE_LOW / PRESSURE_HIGH using its own midpoint threshold.

## OLD rule

TP2_STATE == TP3_STATE

The frozen Noepedia SAME_NET evaluator generates CONSISTENT or FORMAL_MISMATCH.

## Windows

discovery = rows 550,001..555,000
confirmation = rows 600,001..605,000

The confirmation window must not affect candidate selection.

## Frozen candidate family

Candidate model: one pressure channel changes first; the other remains in the previous source state for a short lag interval.

Candidate dimensions:
- source channel: TP2 or TP3
- transition direction: LOW->HIGH or HIGH->LOW
- lag N: 1, 2, 5, 10, 20, 40, 80 rows

For a candidate:
- outside candidate lag interval: expected TARGET state = current SOURCE state
- within rows 0..N after selected SOURCE transition: expected TARGET state = SOURCE state immediately before transition

The candidate never reads current target state to construct its prediction.

## Discovery selection

For each candidate on discovery window report mismatch_count, mismatch_fraction, corrected_old_mismatches, introduced_new_mismatches, net_mismatch_reduction.

Select by:
1. maximum net mismatch reduction
2. smaller N
3. source order TP2 then TP3
4. transition order LOW_TO_HIGH then HIGH_TO_LOW

If selected candidate net mismatch reduction <= 0: NO_DISCOVERY_CANDIDATE.

## Confirmation evaluation

If candidate exists, freeze it unchanged and construct a confirmation field containing OLD direct-equality rule and SELECTED revised rule.
Both are evaluated through frozen Experiment 003 evaluator.

## Preregistered scientific classes

SECOND_REVISION_LOOP_CONFIRMED:
selected candidate exists AND confirmation revised mismatch fraction < old mismatch fraction AND confirmation net mismatch reduction > 0.

SECOND_REVISION_LOOP_NOT_CONFIRMED:
selected candidate exists but confirmation does not improve.

NO_DISCOVERY_CANDIDATE:
no discovery candidate has positive net reduction.

Strong descriptive flag CONFIRMATION_MISMATCH_REDUCTION_50_PERCENT if relative mismatch reduction >= 50%.

## OPEN handling

Initial OPEN:
OPEN_036_RELATION_VALIDITY: TP2_TP3_DIRECT_EQUALITY -> DOMAIN_VALIDITY -> UNKNOWN

A successful confirmation refines OPEN into:
- RESOLVED_COMPONENT: selected directional lag relation
- REMAINING_OPEN: residual mismatches, other transition classes, physical interpretation

The OPEN is never deleted.

## Claim boundary

A positive result would show that a second relation family can pass the structural cycle:
old rule -> mismatch -> candidate relation from evidence -> frozen revised rule -> untouched confirmation -> core re-evaluation.

It would not establish causal mechanism or physical truth.