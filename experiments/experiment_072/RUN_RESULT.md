# Experiment 072 — RUN RESULT

## Status

ARCHITECTURAL PASS

Focused verification run:
`37313944047`

Experiment class:
`ARCHITECTURE_CORRECTION / VALIDATION`

Experiment 071 remains historically unchanged:

`ANY_SHUFFLED_PROMOTION`

## Repair 1 — comparator is no longer a knowledge candidate

`CLASS_IMBALANCE` no longer generates:

`SIMPLER_RULE_COMPARATOR`

as a promotable revision family.

Class imbalance remains a risk signal.

When no genuine relation candidate is supported, the pipeline now falls back to:

`OPEN_DECOMPOSITION`

### Prevalence-shift control

Discovery target:
90% HIGH / 10% LOW

Confirmation target:
10% HIGH / 90% LOW

The source relation exactly matched target in both windows, so under the old implementation the source sequence could beat the frozen discovery-majority comparator and be falsely promoted.

New result:

- detected feature = CLASS_IMBALANCE
- candidate families = OPEN_DECOMPOSITION only
- decision = REMAIN_OPEN
- reason = NO_SUPPORTED_CANDIDATE_FAMILY

No simpler-rule candidate was generated.

## Repair 2 — direct comparator invocation is non-promotable

The simpler-rule evaluator now explicitly reports:

`candidate_role = COMPARATOR_ONLY`

The promotion gate receives:

`candidate_promotable = false`

Direct comparator validation result:

- decision = REMAIN_OPEN
- reason = COMPARATOR_ONLY_NOT_PROMOTABLE
- no promoted-rule record created

Thus even an explicit/manual comparator evaluation cannot become knowledge.

## Repair 3 — shuffled class-imbalance path

A deterministic shuffled class-imbalance control generated structural features:

- DIRECTION_ASYMMETRY
- LOCAL_RESIDUAL_CLUSTER
- CLASS_IMBALANCE

But it did not generate a simpler-rule candidate.

The compatible relation family was:

`DIRECTION_SPECIFIC_RULE`

Result:

- decision = REMAIN_OPEN
- reason = SEARCH_BOUNDARY_UNRESOLVED

No false promotion occurred.

## Comparator still protects genuine candidates

The repair does not remove simpler-rule null protection.

For a genuine temporal candidate with explicit:

`SIMPLE_BASELINE_PLAUSIBLE`

the required null set included:

- MAJORITY_STATE_NULL
- TIME_SHIFT_OR_PERMUTATION_NULL
- SIMPLER_RULE_NULL
- SEARCH_BOUNDARY_CHECK

The selected family remained:

`DIRECTION_SPECIFIC_RULE`

not the comparator.

## Positive temporal regression control

Known synthetic temporal relation:

- family = DIRECTION_SPECIFIC_RULE
- direction = HIGH_TO_LOW
- lag = 3
- decision = PROMOTE
- reason = ALL_MANDATORY_PROMOTION_GATES_PASSED

Therefore the false-promotion repair did not remove the known positive temporal capability.

## Corrections encountered during validation

### Verification fixture correction

The first focused run omitted temporal evaluator configuration from the shuffled control after that control generated a temporal candidate.

Only the test fixture was corrected to supply the preregistered lag/direction/permutation configuration.

### Observation-enrichment correction

The second validation run exposed that automatic observation enrichment replaced explicit context risk flags.

This could silently delete a preregistered:

`SIMPLE_BASELINE_PLAUSIBLE`

risk.

The core now merges explicit and extracted:

- features
- risk_flags

instead of overwriting explicit metadata.

This restores the invariant that automatic extraction may add risk metadata but cannot silently delete explicitly declared risk metadata.

See:

`CORRECTION.md`

## Architectural conclusion

The false-positive mechanism identified by Experiment 071 is repaired:

1. class imbalance cannot create a promotable comparator candidate;
2. a comparator cannot directly pass into rule promotion;
3. shuffled class-imbalance data no longer promote through the simpler-rule path;
4. the simpler baseline remains available as a required null protecting genuine relation candidates;
5. known temporal positive behavior remains promotable.

## Claim boundary

Experiment 072 is not a scientific real-data discovery result.

It does not reclassify Experiment 071.

Experiment 071 remains a valid historical failure under its frozen pipeline.

Any new blind real-data challenge must receive a new experiment number and freeze the repaired 072 core before outcome inspection.
