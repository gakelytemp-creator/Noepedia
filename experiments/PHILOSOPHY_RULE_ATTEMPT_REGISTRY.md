# Philosophy and Rule Attempt Registry

> Status: ACTIVE EXPERIMENTAL AUDIT
> Opened: 2026-10-06
>
> Purpose: preserve every tried structural philosophy and rule variant, not only the variants that later succeed.

## Rule

A new structural rule or philosophical variant must receive an entry **before** its result is known.

Do not delete failed entries.

Do not rename a failed version into a successful one.

A modification creates a new version.

## Required fields

| Field | Meaning |
|---|---|
| ID | Stable attempt identifier |
| Parent | Prior attempt, if this is a modification |
| Change | Exact structural rule or philosophical change |
| Motivation | Why this attempt is being introduced |
| Expected capability | What new behavior is predicted before the run |
| Bench version | Frozen capability bench used |
| Success signal | Predeclared evidence that would support keeping it |
| Damage signal | Predeclared unwanted behavior |
| Result | Observed result |
| Decision | KEEP / MODIFY / REJECT / REOPEN |
| Notes | Failure boundary, cost, new OPENs |

## Initial entries

### PHIL-000 — Pre-reset operator-first direction

- **Status:** historical
- **Change:** Daimonion/operator behavior was treated as the next primary experimental target.
- **Result:** experiments produced useful local machinery and failures, but did not establish the deeper LSM field laws.
- **Decision:** REOPEN.
- **Successor:** PHIL-001.

### PHIL-001 — Field rules before operator architecture

- **Status:** active candidate philosophy
- **Change:** derive and test LSM structural rules before fixing Daimonion internals.
- **Expected capability:** isolate which field rules actually create useful structural/intellectual behavior.
- **Bench version:** not yet frozen.
- **Decision:** PENDING.

## Candidate rule queue

The following are candidates only; each must receive its own versioned entry before testing:

- name-independent object identity;
- predicates as ordinary objects;
- predicate hierarchy / decomposition;
- provisional fundamental status;
- explicit antipredicate relation;
- antipredicate lifecycle / regeneration;
- orphan-object cleanup;
- OPEN preservation;
- DREAM reprocessing;
- interchangeable parallel Daimonion workers.

A candidate appearing in this queue is not evidence that it works.
