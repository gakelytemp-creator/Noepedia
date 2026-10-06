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

## Pre-registered candidate attempts

### RULE-ANTIPREDICATE-v1 — Explicit complementary antipredicate relation

- **Status:** design candidate; not yet tested
- **Parent:** none
- **Change:** represent a predicate's direct complementary / contradictory side as an explicit addressable antipredicate relation/object where the rule is applicable.
- **Motivation:** test whether forcing the opposite structural side to become addressable improves contradiction exposure, OPEN localization, and internal restructuring.
- **Expected capability:** reveal one-sided closure that is invisible when only the positive predicate is represented.
- **Bench version:** not yet frozen.
- **Success signal:** measurable gain on pre-existing contradiction / missing-opposite tasks without degradation on neutral tasks.
- **Damage signal A — false opposition:** the rule invents a unique meaningful opposite where only a broad logical complement exists, or confuses contradictory, contrary, and converse relations.
- **Damage signal B — non-termination:** deletion/regeneration or completion rules enter an oscillation or fail to reach a stable state in a finite bounded test.
- **Damage signal C — useless explosion:** explicit complements multiply structure without producing measurable capability gain.
- **Result:** PENDING.
- **Decision:** PENDING.

The exact semantics of contradictory vs contrary vs converse are intentionally not frozen here. They are part of the design question that must be resolved before the first run, without tailoring the frozen capability bench to the chosen answer.
