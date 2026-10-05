# Experiment 072 — Simpler-Rule False-Promotion Repair

Experiment class: ARCHITECTURE CORRECTION / VALIDATION

Purpose:
repair the false-promotion path exposed by Experiment 071.

Experiment 071 remains historically closed as:
`ANY_SHUFFLED_PROMOTION`

Root cause:
`SIMPLER_RULE_COMPARATOR` was generated as a promotable candidate from `CLASS_IMBALANCE`, even though it is conceptually a comparator/null instrument.

Repair principle:
a comparator may block or contextualize a knowledge candidate, but it must not itself become promoted knowledge.

Validation requirements:
- class-imbalance-only observations select OPEN_DECOMPOSITION, not SIMPLER_RULE_COMPARATOR;
- direct comparator promotion attempts remain non-promotable;
- prevalence-shift shuffled controls do not promote;
- known temporal positive control still promotes;
- temporal candidates continue to be protected by SIMPLER_RULE_NULL when SIMPLE_BASELINE_PLAUSIBLE is present.
