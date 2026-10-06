# Noepedia Experiments

This directory contains the executable and archived experiment sequence.

## Sequence

- [Experiment 001](experiment_001/) — first synthetic dry-run; candidate mismatch and structural OPENs
- [Experiment 002](experiment_002/) — explicit terminal granularity and consistency rule
- [Experiment 003](experiment_003/) — deterministic detection-only evaluator
- [Experiment 004](experiment_004/) — multiple rules under one grammar
- [Experiment 005](experiment_005/) — two-input same-subject antecedent
- [Experiment 006](experiment_006/) — cross-subject shared-object join
- [Experiment 007](experiment_007/) — derived relation consumed by a later rule
- [Experiment 008](experiment_008/) — multi-round derived-relation closure
- [Experiment 009](experiment_009/) — branching and explicit competition
- [Experiment 010](experiment_010/) — evidence-driven branch discrimination without branch deletion

See [Experiments 001–009 — State of Evidence](../EXPERIMENTS_001_009_SUMMARY.md) for the consolidated claim/evidence/limitation view.

## Reproduction

Experiments 004 onward include automatic verifiers and are included in the repository GitHub Actions workflow.

The audit rule is:

~~~text
frozen input
+ frozen expectation
+ committed evaluator
→ independent verifier
→ PASS / FAIL
~~~

Corrections after observing a run must be recorded explicitly rather than silently rewriting history.

- [Experiment 011](experiment_011/) — first external real sensor trace with label-blind deterministic detection

- [Experiment 012](experiment_012/) — label-blind temporal decomposition of real-data mismatches

- [Experiment 013](experiment_013/) — label-blind PRE/POST baseline transition test for outside-only COLD episodes

- [Experiment 014](experiment_014/) — deterministic label-blind clustering of COLD episode structure

- [Experiment 015](experiment_015/) — label-blind time-of-day context test for the two COLD families

- [Experiment 016](experiment_016/) — label-blind pre-onset drift comparison between the two COLD families

- [Experiment 017](experiment_017/) — one-shot held-out NAB replication with exact matched-count null baseline

Methodology note for Experiments 011–016: [Real-Data Instrumentation Track Status](../REAL_DATA_TRACK_STATUS.md).

- [Experiment 018](experiment_018/) — real observations projected into the relational field and evaluated by the existing Noepedia core evaluator

- [Experiment 019](experiment_019/) — MetroPT-3 two-path real-data consistency inference inside the Noepedia core

- [Experiment 020](experiment_020/) — third independent MetroPT-3 relation refines core-derived disagreement into structural support subclasses


## Sequence continuation — 021–073

The individual experiment directories preserve their own README / briefing / result records. This index intentionally keeps the continuation neutral rather than rewriting historical titles after later reinterpretation.

- [Experiment 021](experiment_021/)
- [Experiment 022](experiment_022/)
- [Experiment 023](experiment_023/)
- [Experiment 024](experiment_024/)
- [Experiment 025](experiment_025/)
- [Experiment 026](experiment_026/)
- [Experiment 027](experiment_027/)
- [Experiment 028](experiment_028/)
- [Experiment 029](experiment_029/)
- [Experiment 030](experiment_030/)
- [Experiment 031](experiment_031/)
- [Experiment 032](experiment_032/)
- [Experiment 033](experiment_033/)
- [Experiment 034](experiment_034/)
- [Experiment 035](experiment_035/)
- [Experiment 036](experiment_036/)
- [Experiment 037](experiment_037/)
- [Experiment 038](experiment_038/)
- [Experiment 039](experiment_039/)
- [Experiment 040](experiment_040/)
- [Experiment 041](experiment_041/)
- [Experiment 042](experiment_042/)
- [Experiment 043](experiment_043/)
- [Experiment 044](experiment_044/)
- [Experiment 045](experiment_045/)
- [Experiment 046](experiment_046/)
- [Experiment 047](experiment_047/)
- [Experiment 048](experiment_048/)
- [Experiment 049](experiment_049/)
- [Experiment 050](experiment_050/)
- [Experiment 051](experiment_051/)
- [Experiment 052](experiment_052/)
- [Experiment 053](experiment_053/)
- [Experiment 054](experiment_054/)
- [Experiment 055](experiment_055/)
- [Experiment 056](experiment_056/)
- [Experiment 057](experiment_057/)
- [Experiment 058](experiment_058/)
- [Experiment 059](experiment_059/)
- [Experiment 060](experiment_060/)
- [Experiment 061](experiment_061/)
- [Experiment 062](experiment_062/)
- [Experiment 063](experiment_063/)
- [Experiment 064](experiment_064/)
- [Experiment 065](experiment_065/)
- [Experiment 066](experiment_066/)
- [Experiment 067](experiment_067/)
- [Experiment 068](experiment_068/)
- [Experiment 069](experiment_069/)
- [Experiment 070](experiment_070/)
- [Experiment 071](experiment_071/)
- [Experiment 072](experiment_072/)
- [Experiment 073](experiment_073/)

## New experimental phase — structural rules before Daimonion architecture

Experiments 001–073 are preserved unchanged as historical evidence, instrumentation, failures, and local mechanisms, but they are **not treated as sufficient tests of the current LSM philosophy**. Much of that sequence tested operator behavior before the structural requirements of the field itself were explicit enough.

The new program starts with tiny rule-level ablations:

~~~text
one LSM structural rule
→ one predicted intellectual capability
→ same field with rule OFF / ON
→ keep / modify / reject / REOPEN
~~~

The first candidates include name-independent object identity, predicates as objects, predicate hierarchy, provisional fundamental predicates, explicit antipredicate relations, antipredicate lifecycle/regeneration, orphan cleanup, OPEN preservation, DREAM-style internal reprocessing, and interchangeable parallel Daimonion workers.

See [Experimental Phase Reset — LSM Structural Rules Before Daimonion Architecture](PHASE_RESET_LSM_STRUCTURAL_RULES.md) and the [Philosophy and Rule Attempt Registry](PHILOSOPHY_RULE_ATTEMPT_REGISTRY.md).

The philosophical architecture is explicitly provisional. If it does not produce measurable operational capabilities, it will be replaced as many times as necessary rather than defended.

### Current interpretation note

Experiments 042–064 progressively built the reusable revision subsystem. Experiments 067–073 tested later real-data transfer and stopping behavior. Experiment 071 produced real promotions and shuffled promotions in the same comparator family, demonstrating that the blind-mining path was not null-protected. Experiments 072–073 therefore belong to the stopping/repair discipline rather than to a claim of validated autonomous discovery.
