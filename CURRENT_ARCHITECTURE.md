# Current Architecture — Canonical Boundary

> Status: CURRENT / CANONICAL
> Date: 2026-10-05
>
> This file governs the current architecture together with DIRECTION.md and SOCRATIC_DAIMONION.md.
> Older conceptual documents remain research history. If an older passage conflicts with this file, this file wins.

## 1. The central compression

Noepedia is not intended to become a larger thinking machine.

Its purpose is to move useful knowledge toward a more stable, addressable, cheap, inspectable state.

A useful high-level analogy is:

~~~text
library / literature
        ↓
LLM
distributed neural knowledge, easier to summon than books
        ↓
Noepedia
explicit semiotic structure, cheaper to address, inspect, reuse, and transfer
~~~

The intended direction is therefore:

> **diffuse knowledge → explicit relations → stable reusable structure → minimal sufficient task package**

Noepedia should reduce repeated reconstruction, not create a new permanent layer of expensive cognition.

---

## 2. Noepedia is the LSM

**Noepedia as a whole is the LSM — the Large Semiotic Model.**

LSM is not a fifth worker beside the field and Daimonion. It is the name of the whole semiotic knowledge system.

~~~text
NOEPEDIA / LSM
│
├─ persistent homoiconic semiotic field
├─ semantic boundary adapter(s), including LLMs where useful
├─ Socratic Daimonion — SLM-type neural network
└─ deterministic services compiled from stabilized operations
~~~

The internal roles must remain separate even though together they constitute one LSM.

**SLM means Small Semiotic Model** in this repository. It does **not** mean Small Language Model. The Socratic Daimonion is SLM-type because it is a compact neural operator trained on semiotic placement, retrieval, procedure selection, and task-cut construction; it is not required to speak or model human language.

### Noepedia Field

The field is the persistent homoiconic semiotic substrate.

It stores addressable objects, triplet relation tables, predicates, network handles, provenance/source tokens, status, scope, time/context, versions, OPEN, and other explicit structures.

Its responsibility is database-like:

- store well;
- return well;
- address cheaply;
- traverse cheaply;
- preserve provenance and history where required.

> **The field is structure. It does not think by itself.**

### LLM Adapter

The LLM works at the semantic boundary.

It converts human semantic material into candidate semiotic structures and converts structured results back into human language.

The LLM is not the Daimonion.

Its fluent completion is not automatically a fact.

### Socratic Daimonion

The Daimonion is an **SLM-type neural network** resident inside the LSM. It manages the learned logistics of semiotic structure.

The warehouse analogy is deliberate:

> **The Daimonion is the warehouse manager and loader, not the consumer of the warehouse contents.**

It learns where material belongs, how to retrieve the needed cuts, what procedure should be invoked, how to assemble a temporary task package, and when a case cannot be resolved with the available machinery.

It does not need to speak human language.

It does not need to privately "believe" the claims it routes.

It does not author a fact merely by producing an internal interpretation.

### Deterministic Algorithms

When a Daimonion operation becomes stable and repetitive enough, it should be extracted into a deterministic procedure.

Algorithms are crystallized operational habits.

Once compiled, their desired properties are not human morality or vigilance. They are:

- explicit input contract;
- explicit output contract;
- isolation from unintended direct mutation;
- deterministic or otherwise precisely specified behavior;
- regression testing;
- versioned scope.

> **For deterministic machinery, trust is primarily sterility and transparency.**

The revision subsystem is one such organ. It is not the whole Noepedia core.

---

## 3. Tokens come from contact or procedure results

A token is not a decorative confidence sticker and not the Daimonion's opinion.

A token records that something actually happened:

~~~text
source contact
measurement
comparison procedure
reconstruction test
structural match
structural mismatch
transfer test
other explicit operation
        ↓
TOKEN
~~~

If two description networks are run through a defined comparison procedure and one structurally contains or matches part of the other, the procedure may emit a MATCH token.

If it does not react, there is no invented support or contradiction token.

> **No reaction → no epistemic result token.**

However, **execution coverage is still recorded**. `NOT_RUN`, `RUN_NO_RESULT`, `MATCH`, `MISMATCH`, and other procedure outcomes must remain distinguishable. A procedure invocation may therefore create an execution/coverage record even when it emits no epistemic result token.

This is important because objectivization should arise from repeated independent contact and operation, not from the operator narrating its own confidence.

Tokens themselves may be related:

~~~text
COPIED_FROM
INDEPENDENT_OF
MEASURED_BY
DERIVED_FROM
SAME_ORIGIN_AS
CONFLICTS_WITH
VALID_IN
~~~

Ten repetitions copied from one origin may still represent one evidential lineage.

A strong mismatch token can rapidly downgrade or REOPEN a previously stable relation.

---

## 4. Ingestion and retrieval

### Ingestion

~~~text
semantic material
→ LLM proposes candidate semiotic decomposition
→ Daimonion selects placement/procedures
→ procedures/source contact emit results and tokens
→ field stores structure + provenance + status + OPEN
~~~

### Retrieval

~~~text
human request
→ LLM expresses structural intent
→ Daimonion selects retrieval/query procedure
→ field returns task-relevant cuts
→ temporary mega-graph / task package
→ LLM verbalizes when human language is needed
~~~

The boundary should preserve the difference between:

~~~text
SOURCE MATERIAL
LLM PARSE / TRANSLATION
DAIMONION ROUTING DECISION
PROCEDURE RESULT
PERSISTENT FIELD RECORD
~~~

---

## 5. Mega-graph = pocketed garment

The mega-graph is not a permanent super-graph.

It is a temporary task-specific assembly of only the field cuts required now.

The working metaphor is a coat with pockets.

One task may need hierarchy, time, provenance, and function.

Another may need geometry, diagnostics, and repair history.

The whole field should not be rendered merely because a small cut is needed.

~~~text
REQUEST
→ retrieve minimal sufficient cut
→ perform task
→ if boundary crossed, load another cut
→ discard temporary package when finished
~~~

This is both an epistemic and computational principle:

> **Intelligence is partly the ability to know what not to load.**

---

## 6. Minimal sufficient specialists

A small autonomous machine should not carry the whole Noepedia.

A lawn-mowing robot may receive only:

~~~text
grass / cutting knowledge
local map and forbidden zones
machine-control procedures
minimal interaction protocol with owner
required safety constraints
~~~

If it develops a fault:

~~~text
FAULT / UNKNOWN
→ temporarily load self-diagnostic garment
→ diagnose / identify OPEN
→ repair or escalate
→ unload diagnostic garment
→ return to mowing package
~~~

The robot does not become a general thinker merely to cut grass.

Autonomy does not require maximum knowledge.

> **A good autonomous specialist carries the minimum sufficient stable knowledge for its job and knows how to request another bounded package when its competence boundary is crossed.**

The same rule applies to other task agents.

Capabilities, knowledge, interfaces, and authority should be reduced to the minimum necessary stable form rather than inflated by default.

---

## 7. Daimonion training

The first Daimonion should be trained on the **smallest possible sealed synthetic polygon** where the hidden ground truth is known. This is the next research step, not permission for another large architecture build.

Training cases should include:

- one object under many names;
- one name for several objects;
- missing predicates and missing objects;
- duplicated evidence copied from one origin;
- genuinely independent evidence;
- contradictory sources;
- time/context dependent relations;
- incomplete hierarchies;
- retrieval requiring several networks;
- narrow single-path solutions;
- many-path solutions;
- underdetermined cases;
- inconsistent formulations;
- cases where OPEN is correct;
- cases where no solution exists in the current formulation;
- cases where a procedure should emit MATCH;
- cases where it should emit MISMATCH;
- and cases where it should emit nothing.

The first polygon should begin with a deliberately tiny sealed set containing positive cases, negative cases, `CORRECT_OPEN`, `RUN_NO_RESULT`, and `NOT_RUN` cases before any expansion.

The fitness target is not eloquence.

It is correct semiotic logistics:

~~~text
decompose
route
place
retrieve
select procedure
assemble minimal cut
stop
escalate
preserve provenance
~~~

---

## 8. Neural-to-algorithmic descent

The Daimonion begins where the correct operational mapping is not yet explicit.

Repeated stable success should create pressure toward compilation:

~~~text
learned operation
→ repeated stable behavior
→ explicit boundary conditions
→ deterministic procedure
→ regression tests
→ cheap reusable service
~~~

The neural operator should shrink wherever repeated structure earns an algorithm.

If a deterministic procedure later fails outside its earned scope, preserve the failure, downgrade the scope, and return the unresolved region to learned exploration.

This is not punishment or moral supervision.

It is ordinary engineering boundary management.

---

## 9. Knowledge condition and objectivization

Noepedia does not need a metaphysical rank of superior and inferior knowledge.

A relation can instead carry its current condition, evidence biography, scope, and next justified action.

Repeated independent tokens may move a relation toward a stable-for-current-scope state.

A strong contradiction may return it rapidly to ordinary unresolved status.

The important question is not:

> "Who believes this?"

but:

> **"What contacts and operations have reacted to this structure, with what independence, under what scope?"**

---

## 10. Status of the revision line

Experiments 042 onward produced a substantial auditable revision subsystem.

That work remains useful as one compiled organ.

Experiments in blind automatic pair mining later showed why one local organ must not redefine the whole architecture by momentum.

The next central research direction is therefore not unrestricted correlation discovery.

It is:

> **train a learned semiotic warehouse operator on controlled input/output and retrieval tasks, then progressively compile repeated operations into sterile deterministic machinery.**

---

## 11. Non-negotiable anti-drift rules

Future work must not silently replace this architecture with any of the following:

1. LSM = a separate traversal worker instead of the whole Noepedia system;
2. revision subsystem = whole Noepedia core;
3. Daimonion = conversational LLM;
4. Daimonion = private author of facts;
5. fluent semantic completion = evidence;
6. recurrence = independent support;
7. mega-graph = permanent global working memory;
8. every agent carries the whole Noepedia;
9. autonomy = maximal generality;
10. deterministic algorithms require anthropomorphic moral policing;
11. every request must end in an answer rather than OPEN / no-result / boundary escalation;
12. experimental failure justifies adding another architecture layer;
13. a new implementation path may redefine the goal without explicitly reopening this file.

If an experiment appears to require one of these changes, the experiment must stop and explicitly propose a conceptual REOPEN before implementation continues.

---

## 12. Canonical compact form

> **Noepedia as a whole is the LSM. The persistent field is one structural part of that LSM.**
>
> **The LLM translates semantics at the boundary.**
>
> **The Daimonion manages semiotic logistics; it does not consume or invent the warehouse contents.**
>
> **Tokens are produced by source contact or explicit procedures, not by narrative confidence.**
>
> **The mega-graph is a temporary minimal sufficient garment.**
>
> **Stable repeated operations descend into isolated deterministic algorithms.**
>
> **Agents receive only the smallest sufficient knowledge package and load extra garments only when needed.**
>
> **OPEN, no-result, and escalation are legitimate outcomes.**

That is the current architectural center.
