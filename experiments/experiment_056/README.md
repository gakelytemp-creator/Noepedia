# Experiment 056 — Megagraph Series Adapter

Purpose:
validate conversion of sparse megagraph relation history into aligned state series consumable by the relation-pair scanner.

Component:
`core/revision/megagraph_adapter.py`

Behaviors under test:
- deterministic duplicate-update collapse;
- common timeline construction;
- leading-unknown handling;
- bounded forward-fill;
- aligned equal-length state series;
- discovery/buffer/confirmation splitting;
- downstream pair scanning on adapted discovery series.
