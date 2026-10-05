# Experiment 070 — Gate Coverage Repair & Validation

Experiment class: ARCHITECTURE CORRECTION / VALIDATION

Purpose:
repair the three pipeline coverage defects identified by Experiment 069, then validate them on frozen synthetic positive and negative controls before any new real-data blind challenge.

Repairs:
1. temporal/directional evaluators expose SIMPLER_RULE_NULL;
2. null metric None is missing, while null metric 0 is valid and unbeatable by nonnegative error;
3. observation-pair revision filters candidate families by evaluator-input compatibility before ranking.

No Experiment 068 or 069 result is reinterpreted.

Validation requirements:
- positive temporal control still promotes;
- shuffled/negative control does not promote;
- class-imbalance temporal candidate no longer stops on missing SIMPLER_RULE_NULL;
- zero-valued null is rejected as NULL_NOT_BEATEN rather than marked unavailable;
- incompatible threshold/local-exception families are filtered from state-pair observation runs.
