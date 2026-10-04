# Experiment 058 — RUN RESULT

## Status

reproducibility = PASS
architectural result = PASS

Focused verification:
run_id = 37245297184
conclusion = success

## Strategy objects validated

- RelationScopePolicy
- TimelinePolicy
- SplitPolicy
- SearchPolicy
- RevisionStrategy

## Default strategy

The default policy bundle resolved:
- relation scope
- event-derived common timeline
- discovery/buffer/confirmation split
- lag-search range
- permutation shifts
- pair-score threshold
- forward-fill limit
- null-improvement gate

The known temporal relation was selected and the default strategy reached:

`PROMOTE`

## Custom strategy

A stricter custom strategy used:
- explicit relation scope and pair set
- different discovery/buffer allocation
- capped lag search
- different permutation-shift fractions

The same meaningful pair remained selectable.

Its epistemic decision was accepted as policy-dependent, while graph invariants remained valid.

## Correction

The first verification incorrectly assumed:
1. an event-derived timeline should equal the hidden synthetic array length;
2. every valid custom strategy should reproduce the default PROMOTE decision.

Both assumptions were wrong.

Strategy policies are allowed to change evidential allocation and therefore may legitimately change the final epistemic decision.

See `CORRECTION.md`.

## Architectural conclusion

The graph-native revision subsystem no longer requires per-run manual specification of relation scope, timeline construction, split indices, or search/null configuration.

Those decisions are now represented by reusable, inspectable strategy policy objects and their resolved form is preserved in output provenance.
