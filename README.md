# Noepedia

> **Knowledge should not have to be rediscovered.**
>
> **Discovery should become structure.**

Noepedia is an open attempt to build a **persistent, addressable, inspectable field of knowledge outside the weights of any one language model**.

The current architecture is deliberately simple at its center:

```text
objects
+
triplet relation tables over those objects
+
provenance, history, and explicit uncertainty
```

Noepedia is not primarily a library of sentences.

It is also **not a claim that the world can be copied completely into a knowledge system**. A better working image is a shared scientist's notebook: it preserves what contact with reality has made explicit enough to reuse, while leaving unobserved and undiscovered structure outside the map.

An object does not need to have a human-readable name inside the core. It may simply be an address such as:

```text
OBJECT_3768
```

What humans call that object — for example `space`, `სივრცე`, or `пространство` — can live in an external linguistic or semantic layer that points to the same address.

The object is not its label.

Its usable meaning is increasingly determined by **where it participates across many relation networks**.

---

## 1. The Object Field

Everything that must be addressable can be represented as an object:

```text
physical thing
concept
person
event
measurement
claim
source
image
sound sample
video fragment
rule
network
relation type
experiment
revision
context
```

Objects may be named for humans, but names are not required for internal identity.

This matters because Noepedia is intended to operate across more than language.

A piano object, for example, may connect to:

```text
sound samples
photographs
3D geometry
mechanical parts
grand piano
harpsichord
organ
harmonium
musical works
repair history
manufacturer
piano tuner's phone number
```

No single sentence is "the meaning of piano".

The object acquires a reconstructible relational profile through many different semiotic systems.

---

## 2. Relation Tables

Knowledge is represented through **triplet relations between objects**.

A simplified form is:

```text
subject → predicate → object
```

The important point is that the predicate is not a foreign schema token outside the object field.

**Predicates are objects too.**

A predicate used in the middle position of one triplet may itself appear as the subject or object of other triplets. The same is true for network handles, rules, contexts, revisions, branch identities, times, versions, provenance objects, and other structures.

Noepedia therefore does not add a second metadata grammar above SPO. It keeps using the same relational material.

But Noepedia does not require all relations to be mixed into one undifferentiated graph.

Different tables or networks may represent different cuts through the same object field:

```text
hierarchy
similarity
causality
chronology
function
part-whole structure
evidence
reliability
prototype membership
spatial relation
ownership
service relation
historical origin
contradiction
context validity
```

Each such network is itself addressable. Its handle is another object in the same field, which means the network can have its own provenance, rule, history, context, revisions, and relations to other networks — again through ordinary SPO triplets.

For example, one apple object may participate in many different networks:

```text
APPLE_17
    → acoustic network → bite-sound samples
    → surface network  → texture / geometry observations
    → color network    → color measurements
    → harvest network  → harvest event / time
    → provenance paths → instrument / observer / source
```

These are not extra columns attached to a record.

They are different relational cuts through the same object field.

A request may follow only the acoustic paths, only the harvest history, only the surface measurements, or any other relevant network without changing the underlying SPO format.

Noepedia can therefore describe not only the world, but also the structure by which the world is being described.

### Open Opposites and Formed Unknowns

A relation network does not only group similar things. It may also establish differences, oppositions, poles, and missing positions.

If one pole is known, the structure may legitimately open an address for a possible opposite without asserting that the opposite exists:

```text
known pole  <──────── relation / tension axis ────────>  OPEN opposite
```

The empty side is not a fact pretending to be an object. It is a **formed unknown**: a place for a question created by the structure itself.

This can happen at several levels — sign, description, explanation, meta-explanation, and perhaps at higher layers that have not yet been separated.

A question can therefore arise not only from an external prompt, but from a tension, asymmetry, missing pole, or mismatch already present in the field.

### Predicate Fields and Open Spaces

A stored triplet such as:

```text
A → P → B
```

should not always be treated as the end of thought.

In a living knowledge field, the relation or **predicate** `P` may itself need to become addressable: challenged, compared, decomposed, revised, conditioned, or placed beside alternatives.

Sometimes the field is not yet entitled to write one settled predicate between two objects or structures.

Instead, it may preserve a structured freedom space:

```text
A ─── [ OPEN_SPACE: P1?  P2?  P3?  ... ] ─── B
```

An `OPEN_SPACE` is not empty storage and it does not claim that all candidate predicates are equally valid.

It is a constrained relational region whose possibilities are shaped by what is already known:

```text
evidence
counterevidence
context
history
nearby relations
network rules
oppositions
missing distinctions
```

The important change is that the unknown is no longer only a missing object or a blank answer.

It may be a **structured space of possible relations**.

As constraints accumulate, some possible predicates may disappear, some may become more plausible, and a new predicate may stabilize. But the path by which this happened should remain recoverable.

This creates a further possibility.

A requirement for the next operation need not come only from an external user or from an agent that "wants" something.

It can arise from the structure itself:

```text
OPEN_SPACE
+ constraints
+ tension
→ requirement for comparison, observation, experiment,
  decomposition, retrieval, or meta-inspection
```

In that sense, a living knowledge field can generate **work to be done** from its own unresolved structure.

This is stronger than retrieval.

A passive archive waits to be queried.

A living field can expose where the map itself is unfinished.

### Question-Bearing Predicates and Predicate-Field Will

Observed objects, events, and traces may enter the field with explicit provenance, but a relation inferred from them should not have to enter as an unqualified fact.

A useful minimal notation is:

~~~text
OBJECT_A ── P? ──> OBJECT_B
~~~

The question mark means that the predicate is still carrying unresolved work.

It is not a one-way confidence meter that can only shrink. Supporting evidence may make it smaller; counterevidence, a changed context, or a newly discovered distinction may make it larger again, split the predicate, or reopen an apparently settled relation.

The primary active structure is therefore not an isolated object and not an isolated LLM.

It is the **predicate network**.

Many local question-bearing predicates can interact:

~~~text
P1? + P2? + P3? + dependencies + conflicts + constraints
        ↓
question consolidation
        ↓
high-leverage REQUIREMENT
        ↓
direction for the next expensive operation
~~~

Noepedia uses the formal working term **Predicate-Field Will (PFW)** for this system-level direction.

PFW is not a claim of subjective feeling.

It is the auditable directional requirement synthesized — or, in the project's metaphor, *alchemized* — from tensions among multiple predicate networks.

This also changes what can count as trustworthy direction.

> **Within Noepedia, operational trust should belong only to direction that can be reconstructed from the interacting predicate field. An opaque wish of one model, one network, one authority, or one transient state is not enough.**

Ethical and moral criteria therefore cannot be only an external filter applied after a decision.

They must be able to appear as addressable predicate networks, requirements, conflicts, and constraints inside the same field.

A proposed direction should be inspectable not only for epistemic support but also for the moral requirements that participated in producing or opposing it.

This does not solve morality.

It raises the architectural requirement: **the reasons for action, including normative reasons, must remain visible enough to be challenged and revised.**

The field also has two different phases of valuation.

Before a decision, useful behavior includes disagreement, counterevidence, alternative generation, distinction, and information gain.

After a decision, the same system must be able to enter a coordination mode: execution, cooperation, monitoring, and error detection.

The losing alternatives should not be erased. They remain as preserved branches, warnings, and reopening conditions if the assumptions that justified the decision later fail.
### Marked Harm and Transformative Containment

The normative field needs the same discipline as the epistemic field.

Noepedia should not begin by turning a person, model, group, or other agent into an object named `EVIL`.

What can be represented more honestly are **harm-bearing relations, actions, policies, outputs, causal chains, and requirements** whose status remains open to inspection.

A minimal form is:

~~~text
ACTION / RELATION ── HARM? ──> AFFECTED_OBJECT(S)
~~~

The question mark matters.

`HARM?` may shrink, grow, split into several harms, disappear under better evidence, or become stronger as consequences become visible.

This leads to a working principle of **transformative containment**.

An unresolved harm-bearing structure may be explored in a bounded working region, but it should not silently cross into trusted knowledge or action as if its normative status had already been settled.

> **No unmarked harm may cross the boundary.**

If an unresolved structure must leave the containment region before full resolution, its marker travels with it: provenance, affected parties, uncertainty, known externalities, and the conditions that would require reconsideration.

Acceptance by a downstream user or process does not erase those costs.

The word *containment* applies to structures and actions, not to imprisoning or morally branding persons.

Noepedia also rejects the assumption that harm is a conserved substance whose total amount can only be moved from one victim to another.

Actions change the field itself.

A harmful event can be turned into durable constraints, warnings, new distinctions, safer designs, or changed future options.

~~~text
harmful event / harmful possibility
→ marked structure
→ investigation
→ causal and normative decomposition
→ constraint / redesign / learned distinction
→ changed future predicate field
~~~

The goal is therefore not merely to choose the smallest harm on a fixed board.

It is also to **change the board so that some harmful moves become less likely, less powerful, more visible, or unnecessary in the future**.

The containment process itself must remain open to inspection.

A rule that labels, contains, releases, or transforms harm is part of the same homoiconic field and can itself become the object of challenge.

There is no morally privileged hidden executioner outside the map.

### Fruits, Delayed Consequences, and Moral Appearance

A harmful structure may wear the same outward form as a beneficial one.

Polite language, declared good intention, familiar symbolism, legality, consensus, sacrifice, efficiency, or even apparent compassion are not sufficient moral classifiers.

A familiar Christian formulation captures the operational idea: **judge by the fruits**.

For Noepedia this becomes a structural rule rather than a theological shortcut:

~~~text
FORM / INTENTION
      ↓
ACTION / RELATION
      ↓
immediate effects
      ↓
secondary effects
      ↓
effects on other agents and institutions
      ↓
changes in future options and incentives
      ↓
long-horizon consequences
~~~

The moral status of a candidate action must therefore remain revisable while its consequence network is still unfolding.

Time delay does not dissolve responsibility.

If a cause produces its important effect years or generations later, the causal and normative relation should remain addressable across that interval.

> **A consequence does not become morally irrelevant because it arrived late.**

This is essential for transformative containment.

A containment boundary that watches only immediate output can release a structure whose major harm is delayed, displaced, inherited, institutional, ecological, or otherwise temporally remote.

The marker must therefore be able to survive time:

~~~text
ACTION
→ HARM? / BENEFIT?
→ CONSEQUENCE_CHAIN
→ delayed observation
→ revision of the original predicate
~~~

Likewise, beneficial appearance must not grant permanent clearance.

`GOOD?` and `HARM?` are both revisable predicates whose evidence includes what the action eventually produces and what it transforms in the participants and the surrounding field.

A second criterion follows:

> **Ask not only what the action looks like, but what it makes possible next.**

Religious, philosophical, legal, literary, and historical traditions can therefore be useful to Noepedia as long-running archives of normative predicate patterns.

They are not automatically authoritative because they are old or sacred, nor automatically irrelevant because they are symbolic.

They preserve repeated attempts to distinguish appearance from consequence, petition from responsibility, sacrifice from exploitation, and service from domination.

A compact parable expresses one important transformation:

~~~text
"Help me; this is difficult."
        ↓
"I need help too."
        ↓
the petitioner becomes a participant in the work
~~~

The point is not to claim that a supernatural voice has been demonstrated.

The structural lesson is that a request for rescue can be transformed into a requirement for service: the agent's role changes from recipient of help to contributor to the field that generated the need.

### Artificial Predicate-Network Evolution

The process described above can be treated as a working hypothesis for **artificial predicate-network evolution**.

This does not yet claim a complete Darwinian mechanism.

It names a structural process in which:

```text
objects enter relation
→ OPEN_SPACES appear
→ candidate predicates form
→ constraints weaken, strengthen, split, or eliminate them
→ some predicates stabilize
→ predicates themselves become objects
→ predicate structures fold into META_OBJECTS
→ new meta-level OPEN_SPACES appear
→ new REQUIREMENTS arise from the changed field
→ the network reorganizes again
```

The important point is that the network does not merely accumulate facts.

It can change the **forms of relation by which facts become intelligible**.

This gives a possible computational meaning to a stronger phrase:

> **The archive stores stabilized ground. Intelligence explores and transforms the open predicate field at its edges.**

A further working hypothesis follows.

Creativity may be one expression of the same process: not the retrieval of a stored answer, but the formation of a relation, predicate, analogy, opposition, or meta-object that was not previously stabilized in the field.

This should be treated as a research hypothesis, not as a claim that all human creativity has already been explained.

### Homoiconic Matrix: Freedom and Responsibility

This gives Noepedia a **homoiconic** property: the structures used to describe objects are themselves represented as objects inside the same addressable field.

A predicate is an object.

A network is an object.

A network rule is an object.

A revision of that rule is an object.

A context, time interval, branch, world version, provenance record, or consistency rule can also be an object.

Relations among all of these are represented through the **same SPO machinery**.

No special fourth, fifth, or seventh tuple position is introduced when a new dimension appears. A new dimension is represented by another object, predicate, or network in the same matrix.

In this sense, the map can place parts of **itself** on the map.

That freedom is powerful because the knowledge structure does not have to be frozen. The ontology, networks, and rules can evolve when the world or our understanding changes.

But homoiconic freedom creates a corresponding responsibility.

When a contradiction appears, it must not be possible to make the splinter disappear merely by silently rewriting the level of the map that detected it.

The question must remain visible:

> **Did we solve the problem, or did we only change the instrument that exposed it?**

The Socratic Daimonion therefore guards not a frozen map, but **honest transformation of the map**.

Rules may change. Networks may split. Objects may be reidentified. Higher-order structures may be revised.

What must not disappear is the path that explains **why** the change became necessary, what existed before it, and what consequences the change has for the rest of the field.

A compact principle is:

> **Homoiconicity gives the map freedom to rewrite itself. The Daimonion preserves honesty across that freedom.**

### Meta-Layers as Foldable Handles

A meta-layer should not be imagined only as a higher observer standing above a lower one.

A sufficiently coherent lower structure may be **folded into an addressable handle** while preserving the path back to its internal relations.

```text
lower relational structure
        ↓ fold
META_OBJECT
        ↓ move / compare / relate
new working context
        ↓ unfold when needed
lower relational structure again
```

The handle is not a summary that destroys detail.

It is a movable representative of a structure whose lower layer remains recoverable.

This allows an entire argument, story, experiment, network, or subgraph to travel through a mega-graph as one object until a tension requires it to be opened again.

Because predicates are themselves addressable in a homoiconic field, lower structures can also be grouped by their **predicate profiles**.

Two structures may be placed into an analogy meta-object when a chosen projection preserves important relational form while weakening the identity of their concrete objects.

They may be placed into an opposition meta-object when the chosen projection requires systematic differences between their predicate structures.

The same lower structure may therefore participate in different meta-objects under different comparison rules.

A meta-layer is not a separate metaphysical world.

It is a new addressable object created from relations among lower structures, with a reversible path back down.

### Visibility Is Not Detection

Noepedia can make rules, revisions, conflicts, open positions, and earlier states **visible and inspectable**.

That is an architectural property.

It does not by itself guarantee that a Daimonion will correctly detect every mistaken, convenient, or self-deceptive move.

That is a separate research problem.

The current claim is deliberately narrower:

> **Preserve enough explicit structure that detection can be learned, tested, audited, and later replaced by algorithms where stable regularities emerge.**

Noepedia should not claim an epistemic guarantee before such mechanisms are demonstrated.

---

## 3. Every Network Has a Rule

A network is not merely a bag of links.

It has a declared rule describing what the network is doing.

For example:

```text
NETWORK: functional_similarity
RULE: compare objects by performed function,
      ignoring manufacturer and historical origin
```

or:

```text
NETWORK: evidence_strength
RULE: compare claims by relevance, independence,
      reproducibility, and quality of support
```

A central invariant is:

> **A network must remain faithful to the rule by which it organizes its objects.**

Changing the rule is allowed.

Changing it silently is not.

A rule change should itself become a revision that can be inspected:

```text
old rule
→ problem discovered
→ argument
→ new rule
→ affected relations reconsidered
```

This is one of the simplest forms of intellectual honesty that Noepedia tries to preserve structurally.

---

## 4. Labels and Language Are External Projections

Noepedia's core does not need to think in Georgian, English, Russian, or any other natural language.

A language layer may contain pointers such as:

```text
Georgian:  სივრცე      → OBJECT_3768
English:   space       → OBJECT_3768
Russian:   пространство → OBJECT_3768
```

Likewise, images, sound, geometry, sensor traces, documents, and other sign systems may point toward the same object or toward related objects.

This is why the project uses the term **Large Semiotic Model (LSM)** rather than Large Language Model.

The intended field is **meta-semiotic**: it is concerned with relations among objects across many kinds of sign systems, not only linguistic semantics.

Language remains extremely important — especially for human interaction — but it is one projection among others.

---

## 5. Noepedia, Socrates, and the Daimonion Are Different Things

Noepedia is the persistent semiotic field.

**Socrates** is the historical human figure whose relation to knowledge motivates part of this project.

**The Socratic Daimonion** is the working name for the resident field operator and reflective transaction boundary.

The important clarification is architectural:

> **Humans, LLMs, instruments, and applications do not directly live inside or directly operate the persistent Noepedia field. They approach it through the Daimonion.**

~~~text
HUMAN / LLM / TOOL / INSTRUMENT
        ↕
SOCRATIC DAIMONION
        ↕
NOEPEDIA
    persistent object field
    persistent relation tables
    provenance
    history
    rules
    uncertainty
~~~

The Daimonion may internally use LSM traversal, deterministic algorithms, neural components, or specialized workers.

It does **not** need to carry the archive in its neural weights.

That is a central design goal.

> **The Daimonion should not need to know everything. It should know how to place, retrieve, compare, clarify, authorize, and preserve knowledge without silently corrupting the map.**

External participants may think, speculate, measure, and generate raw material freely outside the persistent field. Persistent field operations remain mediated and auditable.

---

## 6. The Mega-Graph Is the Daimonion's Working Scene

The **mega-graph is not Noepedia**.

It is the Daimonion's temporary working space — its desk, scratch field, garment, or scene of imagination.

For a particular conversation or task, the Daimonion may temporarily load:

```text
relevant objects
relevant networks
network rules
older claims
new incoming claims
conflicts
possible relations
open opposites
context
provenance
```

It may then think over that temporary structure.

The mega-graph can change rapidly and can be discarded.

The permanent archive should not automatically inherit every temporary association that appeared in the working scene.

Only material that survives the archive's insertion process should become persistent Noepedia structure.

---

## 7. Request Freely; Field Access Through the Daimonion

Knowledge is non-rival: one visitor using a relation does not consume it.

But Noepedia should not expose the persistent field as a raw shared database in which every visitor directly reads and writes arbitrary structure.

The intended boundary is:

~~~text
VISITOR REQUEST / CONTRIBUTION
    human question
    LLM request
    instrument trace
    application call
    hypothesis
    note
    raw media

        ↓

DAIMONION
    clarify context
    reconcile identity
    check permissions
    select relevant networks
    preserve provenance
    expose conflicts
    construct a transferable semiotic cut
    decide staging vs trusted placement
    log the transaction

        ↓

NOEPEDIA
    persistent consolidated structure
~~~

A visitor may submit something without knowing where it belongs.

That material can enter a **staging / inbox** state rather than trusted structure.

The Daimonion may later place it, ask clarifying questions, attach it to an existing object, open a new object or network, or preserve it as unresolved raw material.

The right to submit material is not the same as the right to rewrite trusted knowledge.

Likewise, retrieval is contextual and permissioned. A visitor can ask for the structure needed for a task without needing to understand the internal ontology first.

This is closer to an epistemic transaction protocol than to unrestricted database access.

---

## 8. The Daimonion as a Consistency-Preserving Companion

The Daimonion does not decide truth by personality or authority.

Its job is closer to a demanding companion, archivist, and navigator.

If a participant previously established one structure and later proposes another, the Daimonion should make the change visible rather than silently overwrite the earlier structure.

A simple example:

```text
"I met one person on the road."
"It was Dato."
...
"It was Jemali."
```

The Daimonion does not need to know who Dato or Jemali are.

It only notices that the participant created a one-person structure and later tried to place two incompatible identities into the same slot.

The honest options are explicit:

```text
Dato was wrong; replace it
Jemali was wrong; keep Dato
there were actually two people; revise the earlier structure
I do not know; keep the uncertainty visible
```

The principle is small:

> **Do not silently contradict the structure you have already asked the system to preserve.**

If the structure itself was wrong, change it openly.

---

## 9. Meaning Is Reconstructed From Many Projections

One network is rarely enough to characterize an object.

The same object may occupy positions in many independent networks:

```text
what it resembles
what it does
what it contains
where it came from
what supports it
what contradicts it
what it sounds like
what it looks like
where it is used
who services it
which prototype contains it
where it fails
```

The working hypothesis is:

> **Meaning can become reconstructible from the intersection of enough well-formed, sufficiently independent projections.**

How many projection types are sufficient?

We do not know.

Perhaps 724 are sufficient for one domain.

Perhaps 3,000.

Perhaps 7,823.

Perhaps diversity and independence matter more than count.

These numbers are illustrative only.

The required number is an experimental question.

---

## 10. Coverage, Not Only Confidence

A strong-looking conclusion may come from a narrow set of perspectives.

Noepedia should therefore preserve not only support or confidence, but **coverage**:

```text
relevant networks identified: 25
evaluated: 18
not yet evaluated: 7
supporting: 11
neutral: 5
conflicting: 2
status: PROVISIONAL
```

This distinguishes:

> "Everything we checked agrees."

from:

> "We checked enough of what matters."

Those are not the same statement.

A partial reconstruction must not pretend to be a complete one.

---

## 11. Explanatory Boundaries Must Remain Visible

Noepedia should not hide the point at which explanation stops.

A concept may eventually reach a lower boundary where no more fundamental explanatory structure is currently known.

Likewise, a very high-level word should not be accepted as an explanation merely because it gives a name to what remains unexplained.

The system should be able to represent:

```text
known relation
known abstraction
known decomposition
OPEN explanatory boundary
```

An honest boundary is more useful than a fluent circular explanation.

---

## 11A. Knowledge Is a Reduced Notebook, Not a Complete Copy

Noepedia never assumes that a stored object or triplet network exhausts the real object.

A real object may contain indefinitely many properties and interaction possibilities that no current observer, culture, model, or instrument has yet distinguished.

The field therefore records only what has become explicit through observation, measurement, interaction, comparison, or other evidence-bearing contact.

~~~text
REAL_OBJECT
    exceeds
CURRENT_SEMIOTIC_REPRESENTATION
~~~

A relation can still be valuable without being complete.

Knowledge can constrain destructive actions, enable useful ones, and support prediction inside a stated context while remaining radically incomplete from another point of view.

> **Absence from Noepedia is not absence from reality.**

The field should therefore remain open to later objectivization: new properties, new networks, new distinctions, and new modes of access may arrive without implying that the earlier reduced representation was useless.

---

## 11B. Epistemic Teleportation

Noepedia retrieval should be able to move more than a name or sentence.

A request may retrieve an **addressable cut of semiotic structure**:

~~~text
objects
+ relation networks
+ network rules
+ context
+ provenance
+ evidence / counterevidence
+ uncertainty
+ coverage
+ revision history
+ permissions
+ reopening conditions
~~~

That cut can be reconstructed temporarily in a human, LLM, tool, or other working process.

The persistent field remains in place; the usable relational structure is reconstituted where it is needed.

This is the working meaning of **epistemic teleportation**.

It allows settled structure to be reused without forcing each participant to rediscover or permanently memorize it.

See [EPISTEMIC_TELEPORTATION_AND_ASSEMBLY_ALIGNMENT.md](EPISTEMIC_TELEPORTATION_AND_ASSEMBLY_ALIGNMENT.md).

---

## 12. LSM Is Not an LLM With a Different Name

**LSM means Large Semiotic Model.**

In the present architecture, LSM names the process that moves through Noepedia's explicit semiotic structure rather than reconstructing the whole structure from neural weights on every request.

Its early implementation may itself contain neural components.

The intended path is:

~~~text
neural navigation over explicit structure
→ repeated operations become visible
→ stable operations are extracted
→ increasingly algorithmic traversal, comparison, routing, and consolidation
~~~

A central LSM task is to manage question-bearing predicates.

It can consolidate many local uncertainties into a smaller number of high-leverage questions, then do one of two things:

~~~text
SKIP: settled structure is sufficient → answer / route / compare without a large LLM
SHORTEN: a large LLM is still needed → construct a narrow structured prompt for the unresolved part
~~~

The hard research problem is the gate between these modes.

The system must learn when a relation is settled enough for cheap structural handling and when it is still an edge case.

A false edge wastes computation. A **false settled** decision is more dangerous because it can hide a live uncertainty behind cheap confidence.
An LLM stores much of its learned structure diffusely in parameters.

A local factual or conceptual edit may be difficult because the relevant representation is distributed across the model.

Noepedia takes the opposite approach for settled knowledge:

```text
addressable object
addressable relation
addressable network
addressable provenance
addressable revision
```

A relation can be added, removed, corrected, versioned, or challenged without retraining the whole knowledge field.

A useful metaphor is:

> **An LLM is closer to a hologram: changing one local "pixel" is difficult because the representation is distributed.**
>
> **Noepedia is closer to an editable map: local structure can be changed locally, while history remains inspectable.**

The Daimonion acts as the disciplined companion beside that editable map.

---

## 13. The LSM and Daimonion May Begin Neural, But Need Not Stay Entirely Neural

We do not yet know the full technical task of either the LSM control process or the Daimonion.

Therefore early versions should remain neural enough to discover recurring operations rather than freezing the design too early.

The LSM is especially concerned with traversal, question consolidation, routing, and predicate stabilization.

The Daimonion is especially concerned with reflective interruption, consistency, self-revision, and the honesty of transitions between levels.

Possible recurring operations include:

```text
network selection
rule interpretation
object identity reconciliation
placement
conflict detection
tension navigation
coverage estimation
retrieval path construction
revision comparison
provenance preservation
```

If stable patterns emerge, some may later be extracted into deterministic algorithms.

The intended path is:

```text
neural exploration
→ recurring pattern discovery
→ algorithmic extraction
→ hybrid Daimonion
```

This follows a broader principle:

> **When the unknown becomes regular, it no longer needs to remain expensive intelligence.**

---

## 14. Division of Labor

A useful current picture is:

```text
HUMAN / LLM / AISocket / instrument
    observe, imagine, measure, experiment, communicate
    submit requests or raw material from outside the persistent field

LANGUAGE / MEDIA INTERFACES
    names, prose, images, sound, geometry, UI projections

SOCRATIC DAIMONION
    sole mediated field operator / transaction boundary
    clarification and contextual feedback
    permission checks
    temporary mega-graph construction
    consistency and tension checking
    controlled retrieval and insertion
    transaction audit

LSM / ALGORITHMIC / SPECIALIZED WORKERS
    internal services available to the Daimonion
    traverse explicit semiotic structure
    maintain question-bearing predicate status
    consolidate related OPEN_SPACES
    choose SKIP vs SHORTEN vs escalation
    construct targeted retrieval paths

RAW / STAGING / INBOX
    preserve unintegrated material without pretending it is settled knowledge

NOEPEDIA
    persistent addressable object field
    persistent triplet relation tables
    rules, provenance, history, uncertainty
```

No component needs to pretend to be every other component.

---

## 15. Relationship to AISocket, OpenPCB Commons, and Everett Portal

AISocket is one way intelligence can obtain structured observations and bounded actions from real systems.

It can produce traces and evidence that may later enter Noepedia through staging and consolidation.

OpenPCB Commons is a natural proving ground because it produces many kinds of semiotic material around the same physical object.

It is now also the intended **first storage-and-search pilot domain** for Noepedia, while AISocket is the intended first live producer of structured physical traces. The cross-project technical requirements are recorded in [PILOT_AISOCKET_OPENPCB.md](PILOT_AISOCKET_OPENPCB.md).

The pilot is meant to force Noepedia to prove stable identity, provenance, staging, raw-blob handling, relational search, revision, permissioned Daimonion transactions, and task-relevant semiotic-cut retrieval on real hardware evidence rather than only on conceptual examples.

OpenPCB Commons produces many kinds of semiotic material around the same physical object:

```text
board image
geometry
component markings
waveforms
net topology
functional blocks
repair outcomes
instrument traces
3D models
service information
replications
```

These materials should not be forced into one textual description.

They can remain distinct while still pointing into the same object field.

**Everett Portal** is the third pilot and tests a different axis: whether Noepedia can preserve several mutually incompatible but internally coherent world-histories without allowing one branch to leak into another.

Its requirements are recorded in [PILOT_EVERETT_PORTAL.md](PILOT_EVERETT_PORTAL.md).

Everett forces validity conditions to become explicit **without changing the SPO format**.

For example, an addressable relation-network or relation handle may participate in ordinary triplets such as:

~~~text
NETWORK_X → VALID_IN → BRANCH_X
NETWORK_X → VALID_DURING → INTERVAL_Y
NETWORK_X → USES_RULESET → RULESET_V4
NETWORK_X → HAS_PROVENANCE → PROVENANCE_91
NETWORK_X → HAS_STATUS → CANON
~~~

BRANCH_X, INTERVAL_Y, RULESET_V4, PROVENANCE_91, CANON, and the predicates between them are all objects / predicates in the same homoiconic field.

A relation may therefore be canonical inside an Everett branch while remaining explicitly counterfactual relative to our observed world, without inventing an extended tuple or separate metadata envelope.

The Everett **Consistency Gate** is therefore treated as a domain-specific admission service under the Daimonion, not as another name for the Daimonion itself.

Together the three pilots test different structural pressures:

~~~text
AISocket        → contact with reality / trace production
OpenPCB Commons → heterogeneous shared storage and relational search
Everett Portal  → branch scope / time / causality / continuity / identity
~~~

---

## 16. Minimal Working Roles in One Homoiconic Field

The storage grammar should remain minimal:

> **object → predicate → object**

The names below are **roles played by objects and networks**, not separate storage primitives or extra tuple fields.

| Role | Purpose |
|---|---|
| `OBJECT` | Addressable identity in the field |
| `PREDICATE` | An object used in the middle position of an SPO triplet; it may itself appear as subject or object elsewhere |
| `NETWORK` | Addressable relation table / projection made from SPO triplets; its handle is itself an object |
| `RULE` | An object describing an organizing rule of a network |
| `SOURCE` | An object representing origin of material or knowledge |
| `PROVENANCE` | An addressable network/object path explaining how knowledge entered the archive |
| `EVIDENCE` | An object or network supporting a claim or placement |
| `COUNTEREVIDENCE` | An object or network opposing it |
| `CONTEXT` | An object/network expressing conditions under which relations apply; not an extra tuple field |
| `REVISION` | An object/network representing explicit change in object, relation, or rule |
| `OPEN` | Registered unknown or unresolved boundary |
| `OPEN_SPACE` | Structured relational freedom space containing constrained but unsettled predicates |
| `META_OBJECT` | Foldable handle for a lower relational structure that can later be reopened |
| `REQUIREMENT` | Next-operation demand generated by unresolved structure, tension, or missing comparison |
| `PREDICATE_STATUS` | Revisable state of a predicate: settled, provisional, conflicted, open, reopened, or otherwise question-bearing |
| `PREDICATE_FIELD_WILL` | Auditable system-level direction synthesized from tensions, dependencies, and requirements among predicate networks |
| `HARM_MARKER` | Revisable normative marker such as `HARM?`, carrying evidence, uncertainty, affected objects, and externalities |
| `BENEFIT_MARKER` | Revisable normative marker such as `GOOD?` / `BENEFIT?`; appearance or declared intention is insufficient without consequence evidence |
| `CONSEQUENCE_CHAIN` | Addressable causal / normative path linking an action to immediate and delayed effects across arbitrary time gaps |
| `TRANSFORMATION` | Change in participant roles, future options, incentives, or field structure produced by an action |
| `CONTAINMENT_ZONE` | Bounded, auditable working region for unresolved harm-bearing structures; not a label for persons |
| `CONFLICT` | Incompatible supported structures |
| `COVERAGE` | Which relevant projections have or have not been consulted |
| `LABEL` | External human-readable pointer to an object |
| `RAW_BLOB` | Stored material not yet integrated as knowledge |

These are not frozen specifications.

---

## 17. First Research Prototype

The first prototype should prove the architecture, not merely render a UI.

A useful first test should demonstrate that the system can:

1. create nameless addressable objects;
2. attach human-readable labels externally;
3. create multiple triplet relation networks over the same objects;
4. make each network itself addressable;
5. preserve a network rule and revision history;
6. ingest raw material into a staging area without treating it as trusted knowledge;
7. let the Daimonion construct a temporary mega-graph for one task;
8. reconcile incoming identities with existing objects;
9. make contradiction, tension, or silent rule change structurally visible;
10. preserve provenance and uncertainty;
11. promote only consolidated structure into the permanent archive;
12. retrieve one object through several different semiotic paths;
13. expose coverage and unresolved boundaries;
14. represent a formed unknown without pretending the missing object already exists;
15. represent a structured `OPEN_SPACE` between objects or lower structures without prematurely selecting one predicate;
16. place a relation / predicate itself on the object field and inspect or revise it;
17. fold a lower relational structure into a `META_OBJECT`, use it in another context, and later unfold it without losing the lower structure;
18. derive at least one `REQUIREMENT` for a next operation from tension or incompleteness in the field rather than from an external prompt;
19. revise one local relation without rebuilding the whole field;
20. discard the Daimonion's temporary working graph while preserving accepted archive changes.
21. attach a revisable question-bearing status to a predicate and allow later evidence to shrink, enlarge, split, or reopen it;
22. consolidate several related unresolved predicates into one higher-leverage `REQUIREMENT`;
23. distinguish a cheap structured `SKIP` path from a narrowed `SHORTEN` path that invokes a large LLM only for the unresolved edge;
24. preserve minority or losing alternatives after a decision as explicit reopening conditions rather than deleting them;
25. produce at least one auditable `PREDICATE_FIELD_WILL` whose direction can be traced back to the epistemic and normative predicate networks that generated it.
26. represent at least one suspected harmful relation with a revisable `HARM?` marker rather than assigning an essential moral label to an agent;
27. prevent an unresolved harm-bearing structure from crossing into trusted action unmarked, while preserving provenance, affected parties, and known externalities if it must cross provisionally;
28. show that a harmful event can alter the future field by producing a new constraint, warning, distinction, or redesign, and keep the containment rule itself auditable;
29. keep a causal and normative `CONSEQUENCE_CHAIN` addressable across a long delay between action and effect;
30. revise `HARM?` or `BENEFIT?` when delayed consequences contradict the original appearance or intention;
31. distinguish moral appearance from moral fruit by tracing what an action produces in affected agents, institutions, incentives, and future options;
32. represent at least one `TRANSFORMATION` in which a participant's role changes as a result of the field's requirement rather than from an externally imposed label;
33. preserve two mutually incompatible relation networks when ordinary SPO paths place them in different branch/time/version contexts, without treating that contextual difference as a contradiction;
34. retrieve one task-relevant branch/time/version cut by traversing those ordinary relational paths, without leaking relations from another branch;
35. revise a branch canon through a new world version while preserving the previous version, admission provenance, and affected downstream dependencies — still without changing the SPO storage format.

The research prototype should eventually include at least one simple end-to-end case in which stored relations are followed through the actual comparison that produces a splinter. This will test the bridge from structure to process without pretending that the full Daimonion has already been specified.

---

## 18. External Methodological Alignment: AI Assembly Session 002

Noepedia now explicitly adopts several negative constraints sharpened independently in **AI Assembly — Session 002: Causal Attribution Under Uncertainty**:

> **Agreement is not truth. Recurrence is not proof.**

The same session also preserved the non-equivalence of procedural legitimacy and causal truth, simulation and intervention, missingness and proof of missing content, operational closure and final knowledge, and resource withdrawal and epistemic disconfirmation.

Noepedia treats these not as proof of its own architecture, but as constraints that its archive, Daimonion, provenance, uncertainty, and reopening mechanisms must respect.

A detailed mapping is recorded in [EPISTEMIC_TELEPORTATION_AND_ASSEMBLY_ALIGNMENT.md](EPISTEMIC_TELEPORTATION_AND_ASSEMBLY_ALIGNMENT.md).

AI Assembly Session 002:
https://github.com/gakelytemp-creator/AI-Assembly/tree/main/OPEN_DISCOURSES/SESSION_002_CAUSAL_ATTRIBUTION_UNDER_UNCERTAINTY

---

## 19. What We Explicitly Do Not Know Yet

Important open questions include:

- What physical database structure best represents the object field and relation tables?
- How should network relevance be discovered efficiently?
- How should independence between projections be measured?
- How much of the Daimonion must remain neural?
- Which Daimonion operations can become deterministic algorithms?
- How should object identity reconciliation work across modalities?
- How should read, write, deposit, withdrawal, and revision authority work in a public deployment?
- Which operations must always pass through the Daimonion, and which internal services may it safely delegate?
- How should contextual clarification and permission errors be represented as a stable transaction protocol?
- How should explanatory boundaries be represented formally?
- How should formed unknowns and opposite poles be represented without asserting nonexistent objects?
- How should splinter detection be derived from stored relations rather than from hand-written prose?
- How many distinct projections are sufficient for useful reconstruction in different domains?
- How should the temporary mega-graph be constructed, limited, and discarded?
- How should branch/time/version context propagate through ordinary triplet networks across a shared trunk and later divergent branches?
- When should contextual relations attach to an individual relation handle, a network handle, an object, or a retrieval path while keeping one SPO grammar?
- How should branch leakage be detected cheaply before expensive semantic checking?
- How should deterministic identity and one-birth rules coexist with revisable admission confidence?

We do not know these answers yet.

That is part of the research program.

---

## Short Formula

> **The field stores reusable semiotic ground. The Daimonion is the transaction boundary. Intelligence pays mainly for the unresolved edge.**

~~~text
REALITY
    remains larger than every stored representation

HUMANS / LLMs / INSTRUMENTS
    contact the world
    and request or contribute structure

DAIMONION
    clarify
    authorize
    retrieve
    place
    compare
    interrupt
    audit

NOEPEDIA
    persistent object field
    + triplet relation networks
    + provenance / rules / history / uncertainty

EPISTEMIC TELEPORTATION
    reconstruct the relevant semiotic cut
    where it is needed
~~~

And even shorter:

> **Noepedia is the shared notebook, not the world.**
>
> **The Daimonion is the only resident field operator.**
>
> **A visitor receives the right relational cut instead of carrying the whole archive.**
>
> **Language is one projection into the map, not the map itself.**

---

## Philosophical Documents

Noepedia currently has three complementary conceptual texts.

- **[GUIDING_PHILOSOPHY.md](GUIDING_PHILOSOPHY.md)** describes the broader philosophy of Noepedia itself: why knowledge should be externalized, addressable, revisable, and meta-semiotic; why names must remain separate from identities; how living knowledge, explanatory honesty, homoiconicity, provenance, and durable external memory fit together.
- **[SOCRATIC_DAIMONION.md](SOCRATIC_DAIMONION.md)** describes the philosophy of the companion that moves with a thinker through that field: the distinction between Socrates and the Daimonion, the splinter and `STOP`, the temporary mega-graph, responsibility during self-revision, opposite poles and open counter-positions, and navigation through tensions while knowledge is still being formed.

In the shortest form: **the first text is about the map and the kind of knowledge-field we want to preserve; the second is about how the Daimonion travels with us through that map without letting us lose our position or silently damage it.**

A third conceptual bridge, **[EPISTEMIC_TELEPORTATION_AND_ASSEMBLY_ALIGNMENT.md](EPISTEMIC_TELEPORTATION_AND_ASSEMBLY_ALIGNMENT.md)**, records the newer view of Noepedia as a reduced shared scientific notebook, the Daimonion as the sole mediated field operator, epistemic teleportation of relation-network cuts, staged contributions, permissioned transactions, and the negative constraints inherited from AI Assembly Session 002.

A separate engineering forecast is kept in **[EXPECTATIONS.md](EXPECTATIONS.md)**. It records the present hypotheses about division of labor between Noepedia, LSM, LLM, and Daimonion; expected interaction, energy, hardware, and training costs; hallucination reduction; specialization; active learning; the measurable benefits we expect; and the conditions that would falsify those expectations. It is deliberately labeled as expectation rather than benchmark so that later results can be compared against what was actually predicted.

---

## ქართული მოკლე აღწერა

**Noepedia არის მისამართებადი ობიექტების ველი და ამ ობიექტებს შორის მრავალი ტრიპლეტური კავშირის ცხრილი.**

ობიექტს შიგნით შეიძლება საერთოდ არ ერქვას ადამიანის ენაზე სახელი. მაგალითად `OBJECT_3768` შეიძლება ქართულ სემანტიკურ ველში უკავშირდებოდეს სიტყვას `სივრცე`, ინგლისურში `space`, რუსულში `пространство` — მაგრამ ეს სიტყვები მხოლოდ მიმთითებლებია.

Noepedia ლინგვისტური მოდელი არ არის. მისი მიზანი მეტა-სემიოტიკურია: ერთი და იგივე ობიექტი შეიძლება ერთდროულად იყოს დაკავშირებული ტექსტთან, გამოსახულებასთან, ხმასთან, გეომეტრიასთან, იერარქიასთან, ფუნქციასთან, წყაროსთან, მომსახურების მონაცემთან და სხვა მრავალ ქსელთან.

Noepedia-ს მატრიცა ჰომოიკონურია იმ აზრით, რომ მისი აღწერის საშუალებებიც შეიძლება იმავე ველში გახდეს ობიექტი: ქსელი, წესი, წესის ცვლილება და ამ ცვლილების მიზეზიც მისამართებადი და ერთმანეთთან დაკავშირებადია. ამიტომ რუქას შეუძლია თავისი თავის შეცვლაც. ეს თავისუფლება ზრდის Daimonion-ის პასუხისმგებლობას: მან ცვლილება არ უნდა აკრძალოს, მაგრამ უნდა შეინარჩუნოს, **რატომ გახდა ცვლილება საჭირო და რა შეიცვალა მის შედეგად**.

ქსელი მხოლოდ მსგავსებებს არ აერთიანებს. მას შეუძლია შექმნას განსხვავების ღერძი, საწინააღმდეგო პოლუსი ან ჯერ ცარიელი, მაგრამ მისამართებადი ადგილი — **ფორმირებული უცნობი**. ასეთი ცარიელი ადგილი ჯერ ფაქტი არ არის; ის სტრუქტურიდან დაბადებული კითხვაა.

**Daimonion სხვა რამეა, ვიდრე ისტორიული Socrates.** Socrates არის ადამიანი, რომლის ცოდნასთან დამოკიდებულებამ მოგვცა რეკონსტრუქციის მიმართულება; Daimonion არის ექსპერიმენტული თანამგზავრი ფუნქცია, რომელიც დროებით მეგაგრაფში მოძრაობს, დაძაბულობებს ამჩნევს და საჭიროებისას აჩერებს გზას.

ადამიანი, LLM, პროგრამა და ინსტრუმენტი Noepedia-ს მუდმივ ველში პირდაპირ არ მუშაობს. მათ შორის და ველს შორის დგას **Socratic Daimonion** — კონტექსტური, უფლებებით შეზღუდული და აღრიცხვადი ტრანზაქციის ფენა. მან შეიძლება გამოიტანოს არა მხოლოდ ცალკე ობიექტი ან ტექსტური პასუხი, არამედ ამოცანისთვის საჭირო სემიოტიკური ქსელის ჭრილი — ეს არის **ეპისტემიური ტელეპორტაციის** სამუშაო იდეა. დაუმუშავებელი ტექსტი, ვიდეო, სენსორის ნაკადი ან ჰიპოთეზა შეიძლება ჯერ staging/inbox სივრცეში დარჩეს და არ გამოცხადდეს ავტომატურად Noepedia-ს ცოდნად.

მნიშვნელოვანი საზღვარი: **ხილვადობა ჯერ კიდევ არ არის აღმოჩენა.** Noepedia-ს შეუძლია ცვლილება, კონფლიქტი და ძველი მდგომარეობა ხილული დატოვოს; Daimonion-ის უნარი, სწორად შეამჩნიოს როდის არის საჭირო `STOP`, ჯერ კვლევის ამოცანაა და არა უკვე მიღებული გარანტია.

მოკლე ფორმულა:

> **Noepedia სამყაროს ასლი არ არის — ის საერთო სამეცნიერო ბლოკნოტივით ინახავს იმას, რაც სამყაროსთან შეხებამ გახადა ხელახლა გამოსაყენებელი.**  
> **Daimonion არის მუდმივი ველის ოპერატორი და ტრანზაქციის საზღვარი.**  
> **ჰომოიკონურობა რუქას აძლევს თვითრედაქტირების თავისუფლებას; Daimonion იცავს ამ თავისუფლების პატიოსნებას.**  
> **ენა მხოლოდ ერთ-ერთი გარე მიმთითებელი ფენაა.**

---

## License

Software in this repository is licensed under the GNU Affero General Public License v3.0.

Licensing for public knowledge data and human-readable content should be specified separately before public ingestion begins.

---

**Born from AISocket. Expanded through dialogue. Still open to revision.**