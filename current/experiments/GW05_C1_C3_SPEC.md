# GW05 — C1/C3 candidate freeze specification

**Status: PRE-TRANSLATION CANDIDATE SPEC**
**Basis:** GW04 post-unseal audit only.
**Author exposure:** GW05 world text seen (public); GW05 answer book not seen.

## C1 — joint requirement support

A requirement concept with multiple triplet patterns is supported only when there exists at least one single variable binding that satisfies all of its patterns together.

Per-pattern support by different records/subjects is insufficient.

C1 may emit an outward ASK when no joint binding exists. The ASK is about the explicit requirement as a whole; it must not treat separately supported patterns as jointly satisfied.

C1 does not add automatic re-evaluation-on-commit. Requirement revisit timing remains outside this candidate and may be explicit.

## C3 — OPEN by status + resolution transition

The OPEN registry is a query over records whose latest status assertion is OPEN, regardless of record TYPE.

An ASK may be materialized as an addressable OPEN record. If it carries a machine-readable single-fact resolution pattern and a committed fact matches that pattern, the OPEN receives a new non-destructive status assertion RESOLVED. The earlier OPEN assertion remains in history.

Resolved OPENs are excluded from the current OPEN registry because their latest status is no longer OPEN.

C3 does not delete STOP cards or historical status assertions.

## Isolation

Tests are neutral hand-built mini-scenes. They contain no GW05 identifiers, facts, law addresses, event names, or event order.

No GW05 translation exists at candidate-freeze time.
