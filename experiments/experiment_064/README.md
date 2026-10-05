# Experiment 064 — Revision Lineage / Policy Time-Travel

Purpose: verify historical reconstruction and read-only checkout across versioned meta-policy history.

Pass criteria:
- lineage V1 -> V2 -> V3 is reconstructed;
- ancestors and descendants are queryable;
- V1, V2 and V3 can be checked out read-only;
- V3 records that its definition was restored from V1;
- V1 -> V3 path is traceable;
- version definitions can be compared without changing the active policy.
