# Experiment 041 — Master Summary and Experiment Index

## Purpose

Experiment 041 closes the current Noepedia experimental line by summarizing Experiments 019–040 with explicit status, corrections, negative results, OPENs, and claim boundaries.

---

## Executive summary

The experimental line established one strong full knowledge-revision loop in Experiment 033 and a second strong null-protected revision procedure in Experiment 040.

Experiments 034–035 demonstrated disciplined rejection of an attractive but non-general residual pattern.

Experiments 036–037 initially appeared to generalize the revision mechanism, but Experiment 038 showed that both failed explicit null-baseline protection and their strong interpretation was downgraded.

Experiment 039 provided a further negative control: a discovery correction failed transfer and was correctly rejected.

The strongest supported claim at the end of this line is:

> Noepedia can detect a formal mismatch, preserve OPEN uncertainty, gather structured evidence, revise a rule with provenance, and improve untouched-data performance; however, candidate revisions must survive explicit transfer and null-baseline checks before being promoted to knowledge.

---

## Status table

| Experiment | Main question | Final status | Key result |
|---|---|---|---|
| 019 | Can the core derive mismatch from two independent real-data paths? | PASS | Core-derived mismatch appears without verdict labels in inputs |
| 020 | Does a third path refine disagreement shape? | PASS | TP2 strongly aligns with DV side on most AB mismatches |
| 021 | Do mismatches have temporal structure? | PASS | Dominant mismatches cluster near DV transitions |
| 022 | Does one global fixed offset explain the pattern? | NEGATIVE | NO_CONFIRMED_OFFSET_EFFECT |
| 023 | Does mismatch geometry transfer to a new window? | PASS | Shape transfers strongly |
| 024 | Is the pattern a threshold-placement artifact? | PASS | THRESHOLD_INVARIANT across frozen threshold family |
| 025 | Is there a raw Motor_current gap supporting 024? | PASS | RAW_BAND_SPARSE |
| 026 | What do raw trajectories look like around transitions? | PASS | LOAD_ON immediate; LOAD_OFF delayed |
| 027 | What are per-transition response times? | PASS | LOAD_ON=0 rows; LOAD_OFF median=42 rows |
| 028 | Which covariates might explain LOAD_OFF tail? | EXPLORATORY | TP3+10 strongest candidate |
| 029 | Does TP3+10 replicate? | NEGATIVE | NOT_REPLICATED |
| 030 | Does primary directional timing replicate? | PASS | DIRECTIONAL_ASYMMETRY_REPLICATED |
| 031 | Is row timing stable enough to interpret physically? | PASS | Median cadence ~10 s; gaps audited |
| 032 | Does 42 rows correspond to physical time? | PASS | Median physical response ~416 s |
| 033 | Can evidence revise the rule and re-enter the core? | STRONG POSITIVE | 99.565% mismatch reduction on common untouched subset |
| 034 | What are the 6 residual mismatches? | PASS | SINGLE_RESIDUAL_PATTERN |
| 035 | Does the residual pre-LOAD_ON pattern generalize? | NEGATIVE | PRE_LOAD_ON_PATTERN_WEAK |
| 036 | Second revision loop on TP2↔TP3? | DOWNGRADED | Historical transfer success; later NOT_NULL_PROTECTED |
| 037 | Third revision loop on H1↔Reservoirs? | DOWNGRADED | Historical transfer success; later NOT_NULL_PROTECTED |
| 038 | Do 036/037 survive explicit null baselines? | NEGATIVE / CORRECTIVE | NO_FAMILY_NULL_PROTECTED |
| 039 | Can Pressure_switch↔Reservoirs produce a second strong loop? | NEGATIVE | NULL_PROTECTED_REVISION_NOT_CONFIRMED |
| 040 | Can a calibration-selected family pass full null protection? | STRONG POSITIVE | COMP→Motor_current revised rule: 1982→26 mismatches |

---

## The first strong knowledge-revision loop — Experiment 033

### Old assumption

`DV_eletric = 1 -> Motor_current HIGH`
`DV_eletric = 0 -> Motor_current LOW`

This direct mapping produced substantial formal mismatch.

### Evidence path

Experiments 019–032 established:
- mismatch was reproducible
- mismatch was temporally structured
- one global fixed offset failed
- threshold placement did not explain the pattern
- LOAD_ON and LOAD_OFF had asymmetric timing
- LOAD_ON was effectively immediate
- LOAD_OFF clustered around 42 rows
- event-wise physical time clustered near 416 s

### Revised rule

LOAD_ON:
- HIGH immediately

LOAD_OFF:
- 0..40 rows -> HIGH expected
- 41..52 rows -> TRANSITION_OPEN
- >52 rows -> LOW expected

### Untouched evaluation

Common evaluable subset:
- OLD mismatches = 1380
- REVISED mismatches = 6
- relative mismatch reduction = 99.565%

384 TRANSITION_OPEN rows were not counted as successful matches.

### Correction

Experiment 033 required one execution-only correction:
- executable object type changed from `empirically_supported_rule` to `consistency_rule`
- epistemic status remained `EMPIRICALLY_SUPPORTED_RULE`
- no semantic rule, window, threshold, OPEN, or criterion changed

See `experiments/experiment_033/CORRECTION.md`.

### Meaning

Experiment 033 is the strongest demonstration of the full Noepedia loop:

`RULE -> MISMATCH -> OPEN -> EVIDENCE -> REVISED RULE -> FROZEN CORE RE-EVALUATION -> OPEN REFINEMENT`

---

## Residual discipline — Experiments 034–035

Experiment 034 found that all six residual mismatches formed one compact pre-LOAD_ON pattern.

It would have been easy to add a second exception to the rule.

Experiment 035 tested that candidate on untouched data.

Result:
- only 3/28 LOAD_ON events had the proposed pre-HIGH pattern
- preregistered threshold was 50%
- result = PRE_LOAD_ON_PATTERN_WEAK

Therefore the rule was not expanded.

Operational lesson:

> local repeated structure != general rule

This pair is an important anti-overfitting demonstration.

---

## Apparent generalization and later downgrade — Experiments 036–038

Experiments 036 and 037 initially produced large mismatch reductions on new relation families:
- TP2 ↔ TP3
- H1 ↔ Reservoirs

However both selected lag=80 at the upper search boundary.

Experiment 038 addressed two concerns:
- expanded lag search to 1..400
- added majority-state and circular-shift temporal nulls

The expanded search found an interior optimum near 75 rows, removing the boundary concern.

But neither family survived null protection:

F036:
- revised vs majority improvement ~0.87%
- revised vs permutation median improvement ~1.04%
- NOT_NULL_PROTECTED

F037:
- revised mismatches = 1022
- majority mismatches = 1022
- all tested permutation nulls = 1022
- NOT_NULL_PROTECTED

Therefore 036/037 are retained historically but downgraded to:

`TRANSFERRED_TEMPORAL_PATTERN_NOT_NULL_PROTECTED`

See:
- `experiments/experiment_036/CORRECTION.md`
- `experiments/experiment_037/CORRECTION.md`

---

## Strong negative control — Experiment 039

Relation family:
`Pressure_switch ↔ Reservoirs`

Discovery suggested a 59-row HIGH_TO_LOW correction.

But untouched confirmation showed:
- OLD rule mismatches = 21 / 5000 = 0.42%
- REVISED mismatches = 1226 / 5000
- permutation-null median = 1226

Therefore:

`NULL_PROTECTED_REVISION_NOT_CONFIRMED`

Meaning:

> a discovery-window correction can look useful and still be non-transferable.

The correct action was to retain the old rule and preserve OPEN about domain variation.

---

## Second strong null-protected revision example — Experiment 040

Experiment 040 was designed after the lessons of 038 and 039.

### Calibration-only family selection

Frozen candidate families:
- DV_pressure -> TP2
- COMP -> Motor_current
- Towers -> TP3
- LPS -> Reservoirs

Selection used calibration rows 1..50,000 only.

Eligibility required calibration mismatch fraction between 5% and 40%.

Selected family:

`COMP -> Motor_current`

Calibration mismatch fraction:
`23.706%`

Frozen orientation:
`COMP 0 -> CURRENT_HIGH`
`COMP 1 -> CURRENT_LOW`

### Discovery

OLD mismatches = 1616

Selected candidate:
- transition = HIGH_TO_LOW
- lag = 40 rows
- clear interior minimum
- discovery revised mismatches = 15

### Untouched confirmation

OLD:
- 1982 mismatches / 5000
- 39.64%

REVISED:
- 26 mismatches / 5000

Nulls:
- majority-state null = 2690 mismatches
- permutation-null median = 2635 mismatches

Relative reduction:
- vs OLD = 98.688%
- vs majority null = 99.033%
- vs permutation median = 99.013%

Result:

`NULL_PROTECTED_REVISION_CONFIRMED`

### Important boundary

Experiment 040 is not physically independent of Experiment 033 because Motor_current appears in both.

It is a distinct measurement relation and a separate null-protected confirmation design.

---

## Current evidence state

### Strongly supported

1. Noepedia can derive formal mismatch from stored relations rather than inserted verdict labels.
2. OPEN can be preserved rather than silently forced closed.
3. Evidence can refine a rule and re-enter the frozen core evaluator.
4. Untouched confirmation can sharply improve after a provenance-bearing revision.
5. Null baselines are necessary before promoting revision candidates.
6. Negative results can and should block rule promotion.

### Strong positive demonstrations

Experiment 033:
- full knowledge-revision loop
- 99.565% common-subset mismatch reduction

Experiment 040:
- null-protected revision design
- 98.688% reduction vs OLD
- ~99% reduction vs both null baselines

### Negative / corrective demonstrations

Experiment 022:
- global fixed offset rejected

Experiment 029:
- exploratory TP3 candidate failed replication

Experiment 035:
- residual pre-LOAD_ON pattern failed generalization

Experiment 038:
- 036/037 failed null protection

Experiment 039:
- discovery correction failed untouched transfer

---

## Remaining OPEN

The experimental line does not close the following questions:

1. Physical/controller mechanism behind the ~416 s LOAD_OFF relation.
2. Whether Experiment 040's 40-row temporal relation corresponds to the same controller timing object or a distinct one.
3. Transfer to different machines or different datasets.
4. Transfer to non-compressor domains.
5. Whether the core can automate candidate generation and null selection without manual experiment design.
6. Whether provenance-bearing rule revision can be generalized across non-temporal relation types.

---

## Recommended next phase

The current 019–040 line is complete enough to close as one experimental series.

The next phase should not continue random channel-pair testing.

Recommended future work:

### Phase A — architecture
- formalize automatic revision workflow in the Noepedia core
- make OPEN -> candidate -> null-protected confirmation an explicit reusable protocol
- record provenance and correction history as first-class objects

### Phase B — external generalization
- repeat the protocol on a different dataset or different physical system
- preregister all gates from the start
- use explicit null models before any strong claim

### Phase C — non-temporal relations
- test whether the same revision architecture works on hierarchy, identity, structural joins, or other relation networks

---

## Final status of this series

The 019–040 experimental sequence should be considered:

`SERIES_COMPLETE_WITH_TWO_STRONG_POSITIVE_REVISION_DEMONSTRATIONS_AND_MULTIPLE_NEGATIVE_CONTROLS`

The strongest scientific value is not the number of positive results.

It is the combination of:
- successful revision
- preserved uncertainty
- preregistration
- untouched confirmation
- null comparison
- explicit corrections
- retained negative results

That combination is the operational standard Noepedia should keep.