# Noepedia Pilot: Everett Portal

> **Purpose:** use Everett Portal as the third Noepedia stress test — a test of branch-scoped knowledge, temporal continuity, causal dependency, persistent identity, lazy world expansion, and consistency under multiple mutually incompatible but internally coherent worlds.

AISocket tests contact with new physical experience.

OpenPCB Commons tests heterogeneous shared storage and relational search.

Everett Portal tests whether Noepedia can preserve **several different world-histories without allowing one history to leak into another**.

A relation may be perfectly valid inside one Everett branch and false in our recorded world.

Noepedia must therefore know not only what relation is stored, but **where, when, under which world version, and with what status that relation is valid**.

---

## 1. The central distinction

Everett Portal contains generated counterfactual worlds.

A canonical Everett fact is not thereby a factual claim about our world.

The system must preserve:

~~~text
CANON_IN_BRANCH
        ≠
OBSERVED_IN_OUR_WORLD
~~~

This boundary is non-negotiable.

A branch statement can be internally binding while remaining explicitly synthetic / counterfactual in origin.

Therefore provenance must preserve at least:

~~~text
origin class
world
branch
world version
time / interval
generator or admitting process
causal parents
admission history
~~~

The portal mark Ǝ is the human-visible sign of this separation.

Noepedia must preserve the machine-readable equivalent.

---

## 2. Why Everett Portal is a Noepedia requirement generator

Everett's four current white papers already impose concrete requirements.

### WP-001 — Causal Morphing Field

Noepedia must support causal dependence that changes over time and across nodes.

The same date does not imply the same degree of branch divergence everywhere.

### WP-002 — Discrete Facts and Continuous Causality

Event commitment is discrete inside a branch.

Causal influence may propagate gradually.

This means the field must distinguish:

~~~text
event identity / branch commitment
from
strength / reach / propagation of causal dependence
~~~

### WP-003 — World State and Generative Artifacts

Persistent world state must remain upstream of rendered artifacts.

An LLM-generated newspaper, song, interview, or radio script cannot silently rewrite the world it refers to.

### WP-004 — Consistency Gate

The gate that admits a candidate into branch canon is fallible and measurable.

Typed structure can make part of consistency checking exact.

The semantic remainder remains approximate.

This is an especially useful Noepedia research problem.

---

## 3. Scope must become first-class

A bare triplet is not enough for Everett.

~~~text
SUBJECT ── PREDICATE ──> OBJECT
~~~

needs an explicit validity scope.

Conceptually:

~~~text
ASSERTION
    relation: SUBJECT ── PREDICATE ──> OBJECT
    scope:
        world
        branch
        time / interval
        world_version
        ruleset_version
    status
    provenance
~~~

The triplet remains the local relational unit.

The scope tells us **which world gives that relation meaning**.

This should not be implemented by copying every object into every branch when a shared object identity can remain common.

Instead, branch-specific assertions and state should carry branch scope.

---

## 4. Shared trunk and branch-relative continuation

Everett requires a shared historical trunk up to a Point of Divergence.

Conceptually:

~~~text
SHARED_TRUNK
        ↓ POD
   ┌────┴────┐
OUR_BRANCH   EVERETT_BRANCH
~~~

Before the POD, both branches may reference the same historical substrate.

After the POD, branch-relative relations may diverge.

Noepedia therefore needs to preserve:

- shared identity where justified;
- branch-local state after divergence;
- explicit Point of Divergence;
- causal paths from POD to later branch-specific facts;
- no silent back-propagation of alternate facts into the shared trunk.

---

## 5. Canon is not epistemic certainty

Everett WP-002 uses a useful operational transition:

~~~text
LATENT
→ CANDIDATE
→ CANON
~~~

For Noepedia, CANON must be interpreted carefully.

It means:

> **This world version is now committed to treating this object/event as part of its internal history.**

It does **not** mean:

> **The admission was epistemically infallible.**

Therefore two statuses should remain separate:

~~~text
BRANCH_COMMITMENT_STATUS
    latent / candidate / canon / superseded

ADMISSION_EPISTEMIC_STATUS
    support / uncertainty / conflict / confidence / review history
~~~

A canonical branch event can remain revisable through explicit world-version correction.

The earlier admission history must not disappear.

---

## 6. One Birth Rule

Everett's "one birth" rule is a strong identity test for Noepedia.

A canonical artifact may later have:

- remix;
- translation;
- cover;
- remaster;
- quotation;
- reproduction;
- derivative work.

But these do not create a second original.

The system therefore needs an addressable birth event and derivation relations:

~~~text
ARTIFACT ── BORN_AT ──> BIRTH_EVENT
DERIVED_ARTIFACT ── DERIVED_FROM ──> ARTIFACT
~~~

Identity cannot be reconstructed from title, date, filename, or performer label alone.

This is a direct stress test for Noepedia object identity.

---

## 7. The Consistency Gate is not the Daimonion

The Everett **Consistency Gate** and Noepedia **Socratic Daimonion** should not be merged into one concept.

The Daimonion is the general transaction and reflective boundary of the Noepedia field.

The Everett Consistency Gate is a **domain-specific admission service** used when a candidate event or artifact seeks entry into a branch's canon.

Conceptually:

~~~text
candidate artifact / event
        ↓
DAIMONION transaction boundary
        ↓
Everett Consistency / Novelty services
        ├─ exact typed checks
        ├─ causal-neighborhood retrieval
        ├─ identity / birth comparison
        ├─ semantic comparison
        ├─ confidence / unresolved checks
        └─ escalation if needed
        ↓
admit / reject / hold open / request clarification
        ↓
versioned Noepedia branch state
~~~

The gate may use algorithms, retrieval, LLMs, human review, or other specialized workers.

Its errors must be measurable.

The Daimonion must preserve the gate's reasoning path and admission provenance rather than pretending the gate is an oracle.

---

## 8. Lazy world opening

Everett should not require a complete alternate Earth to exist in explicit detail.

A request may open one coordinate:

~~~text
1994 / Manchester / music / interview
~~~

and require only the predecessor structure necessary to support that coordinate.

This maps naturally onto Noepedia's OPEN / OPEN_SPACE concept.

Unopened regions are not missing facts pretending to exist.

They are unresolved structured possibilities.

A request may generate a REQUIREMENT to open enough causal predecessors to make the requested region coherent.

This is a direct Noepedia test of **demand-driven expansion**.

---

## 9. Minimal Everett object families

The pilot may introduce a domain vocabulary such as:

~~~text
WORLD
BRANCH
POINT_OF_DIVERGENCE
WORLD_VERSION
RULESET_VERSION
WORLD_COORDINATE
EVENT
EVENT_BIRTH
ARTIFACT
ARTIFACT_BIRTH
DERIVATION
CAUSAL_PARENT
CAUSAL_LINK
MORPH_FIELD_VALUE
CANON_ASSERTION
CANON_STATUS
ADMISSION
CONSISTENCY_CHECK
NOVELTY_CHECK
GENERATOR
GENERATOR_VERSION
CHECKPOINT
TRANSMISSION
PORTAL_EVENT
OPEN_CELL
~~~

These are pilot/domain objects, not necessarily permanent Noepedia core primitives.

---

## 10. Required provenance

Every canonical Everett object should be able to answer:

~~~text
Which world?
Which branch?
Which world version?
Which ruleset version?
At what branch time?
What was its birth event?
Which causal parents supported it?
Which generator/version produced candidates?
Which gate checks were performed?
What confidence / objections remained?
Who or what admitted it?
Which later artifacts depend on it?
~~~

A transmitted artifact should additionally preserve:

~~~text
origin branch
portal event
transmission event
human-visible Ǝ mark status
machine-readable origin metadata
~~~

---

## 11. Search requirements

Everett makes Noepedia search temporal and branch-relative.

Useful queries include:

~~~text
Show this person's state in our branch and Everett branch at the same date.

Which later artifacts depend causally on this event?

What changed after the Point of Divergence in this city?

Which canonical facts support this 1994 newspaper?

Show all artifacts born from this creator before this date.

Is this candidate a second original or a legitimate derivative?

Which branch facts are shared with our world and which are branch-local?

What remains OPEN around this coordinate?

Which accepted event has the weakest admission confidence?

Which world-version revision invalidated this artifact?
~~~

The query engine must never merge results across branches without making the merge explicit.

---

## 12. Epistemic teleportation across a branch

A generator should not receive the entire alternate world.

The Daimonion should retrieve only the semiotic cut needed for the requested artifact.

For example, a radio generator may receive:

~~~text
active world / branch / version
time and place
relevant people and institutions
recent causal parents
canon events
cultural context
existing artifacts / birth identities
open degrees of freedom
provenance constraints
forbidden contradictions
~~~

This is Everett's direct test of Noepedia's epistemic teleportation.

The generator renders from the cut.

It does not own or mutate the world state.

---

## 13. First end-to-end experiment

A useful first pilot can remain very small.

1. Create a shared trunk with three or four historical objects.
2. Create one Point of Divergence.
3. Create one Everett branch and one world version.
4. Add one branch-local event with explicit causal parents.
5. Generate two candidate cultural artifacts.
6. Admit one and reject or hold the other.
7. Preserve the admission path and uncertainty.
8. Query the same object in both branches without leakage.
9. Generate a later artifact that depends on the accepted earlier event.
10. Correct one canon relation through a new world version while preserving the older world version and downstream dependency history.

This is enough to test the fundamental architecture.

---

## 14. Acceptance tests

The Everett pilot should eventually demonstrate that:

- two incompatible branch assertions can coexist without collision;
- shared pre-POD history can be reused without duplication;
- branch-local facts never silently leak into OUR_WORLD;
- every canon assertion carries world / branch / time / version scope;
- canonical commitment and epistemic confidence remain separate;
- one artifact cannot accidentally acquire two original births;
- derivatives point back to an original birth;
- a generator receives a bounded semiotic cut rather than the whole world;
- a generated artifact cannot silently rewrite upstream world state;
- consistency checks can show which part was exact and which part was semantic;
- low-confidence admissions can remain open or escalate;
- a world-version correction preserves the previous version;
- downstream dependencies affected by a correction can be found;
- unopened cells remain OPEN rather than fabricated;
- the same coordinate under the same frozen world/ruleset version remains reproducible.

---

## 15. What Everett teaches Noepedia

AISocket asks:

> Can Noepedia receive a new trace from reality?

OpenPCB asks:

> Can Noepedia store and find heterogeneous partial knowledge?

Everett asks:

> Can Noepedia preserve identity, causality, time, and truth-scope when several incompatible worlds occupy the same field?

That third question forces a major architectural requirement:

> **Truth and canon must be scoped.**

The field must be able to say not merely:

> "This relation exists."

but:

> **"This relation is asserted here, in this world, in this branch, at this time, under this version, with this provenance and this epistemic status."**

That capability is useful far beyond Everett Portal.

---

## Short formula

> **AISocket tests contact.**
>
> **OpenPCB tests the commons.**
>
> **Everett tests continuity across possible worlds.**
>
> **Noepedia must survive all three without confusing evidence, knowledge, and scope.**
