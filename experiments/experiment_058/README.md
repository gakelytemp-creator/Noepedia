# Experiment 058 — Revision Strategy Policies

Purpose:
validate reusable strategy objects for graph-native revision.

Policies:
- RelationScopePolicy
- TimelinePolicy
- SplitPolicy
- SearchPolicy
- RevisionStrategy

The strategy-driven graph pipeline must resolve:
- relation scope and candidate pairs
- common timeline
- discovery/buffer/confirmation split
- lag/search/null configuration
- minimum pair score
- forward-fill limit
- null-improvement gate

Pass criteria:
- default strategy resolves all four policy classes;
- default strategy reaches PROMOTE on the known graph-native temporal case;
- custom strategy also reaches the same scientific decision with different split/search settings;
- strategy resolution is recorded in output provenance.
