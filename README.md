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
subject → relation → object
```

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

Each such network is itself addressable. Its handle can also be an object in the object field, which means the network can have its own provenance, rule, history, context, revisions, and relations to other networks.

Noepedia can therefore describe not only the world, but also the structure by which the world is being described.

### Homoiconic Matrix: Freedom and Responsibility

This gives Noepedia a **homoiconic** property: the structures used to describe objects can themselves be represented as objects inside the same addressable field.

A network can be an object.

A network rule can be an object.

A revision of that rule can be an object.

Relations among networks, rules, revisions, and the reasons for changing them can themselves be represented through the same relational machinery.

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

## 5. Noepedia and Socrates Are Different Things

Noepedia is the persistent archive.

**Socrates** is the experimental learned system that works with that archive.

```text
NOEPEDIA
persistent object field
persistent relation tables
provenance
history
rules
uncertainty

SOCRATES
reads from the archive
constructs temporary working structures
compares and consolidates incoming material
checks consistency with declared rules
helps retrieve relevant structure
proposes archive edits through an auditable path
```

Socrates does **not** need to carry the archive in its neural weights.

That is a central design goal.

> **Socrates should not need to know everything. It should know how to place, retrieve, compare, and preserve knowledge without corrupting the archive.**

---

## 6. The Mega-Graph Is Socrates' Working Scene

The **mega-graph is not Noepedia**.

It is Socrates' temporary working space — its desk, scratch field, or scene of imagination.

For a particular conversation or task, Socrates may temporarily load:

```text
relevant objects
relevant networks
network rules
older claims
new incoming claims
conflicts
possible relations
context
provenance
```

It may then think over that temporary structure.

The mega-graph can change rapidly and can be discarded.

The permanent archive should not automatically inherit every temporary association that appeared in Socrates' working scene.

Only material that survives the archive's insertion process should become persistent Noepedia structure.

---

## 7. Read Freely, Write Carefully

Reading knowledge does not consume it.

Many humans, models, tools, or programs may retrieve structure from Noepedia.

Writing is different.

Raw input should not automatically become trusted archive structure.

A useful separation is:

```text
RAW / STAGING SPACE
    video bits
    audio
    documents
    sensor streams
    model output
    human notes
    hypotheses
    temporary graphs

        ↓

SOCRATES
    identify
    compare
    reconcile
    preserve provenance
    detect conflict
    place into appropriate networks

        ↓

NOEPEDIA
    persistent consolidated structure
```

A streamed film may exist as stored bits without Noepedia claiming to know what is inside it.

Only when an agent identifies objects, relations, events, or evidence does structured knowledge begin to form.

Noepedia should distinguish clearly between **stored material** and **integrated knowledge**.

---

## 8. Socrates as a Consistency-Preserving Archivist

Socrates does not decide truth by personality or authority.

Its job is closer to a demanding archivist and mentor.

If a participant previously established one structure and later proposes another, Socrates should make the change visible rather than silently overwrite the earlier structure.

A simple example:

```text
"I met one person on the road."
"It was Dato."
...
"It was Jemali."
```

Socrates does not need to know who Dato or Jemali are.

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

## 12. LSM Is Not an LLM With a Different Name

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

Socrates acts as the disciplined mentor beside that editable map.

---

## 13. Socrates Begins Neural, But Need Not Stay Entirely Neural

We do not yet know the full technical task of Socrates.

Therefore the first version should be neural enough to discover recurring operations rather than freezing the design too early.

Possible recurring operations include:

```text
network selection
rule interpretation
object identity reconciliation
placement
conflict detection
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
→ hybrid Socrates
```

This follows a broader principle:

> **When the unknown becomes regular, it no longer needs to remain expensive intelligence.**

---

## 14. Division of Labor

A useful current picture is:

```text
HUMAN / LLM / AISocket / instrument
    observe, imagine, measure, experiment, communicate

RAW / STAGING SPACE
    preserve unintegrated material without pretending it is settled knowledge

SOCRATES
    temporary reasoning over a mega-graph
    consolidation
    consistency checking
    retrieval assistance
    controlled archive insertion

NOEPEDIA
    persistent addressable object field
    persistent triplet relation tables
    rules, provenance, history, uncertainty

LANGUAGE / MEDIA INTERFACES
    names, prose, images, sound, geometry, UI projections
```

No component needs to pretend to be every other component.

---

## 15. Relationship to AISocket and OpenPCB Commons

AISocket is one way intelligence can obtain structured observations and bounded actions from real systems.

It can produce traces and evidence that may later enter Noepedia through staging and consolidation.

OpenPCB Commons is a natural proving ground because it produces many kinds of semiotic material around the same physical object:

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

---

## 16. Minimal Working Objects

The exact grammar is still open, but the present conceptual minimum includes:

| Object | Purpose |
|---|---|
| `OBJECT` | Addressable identity in the field |
| `RELATION` | Typed connection between objects |
| `NETWORK` | Addressable relation table / projection |
| `RULE` | Declared organizing rule of a network |
| `SOURCE` | Origin of material or knowledge |
| `PROVENANCE` | History of how a relation entered the archive |
| `EVIDENCE` | Support for a claim or placement |
| `COUNTEREVIDENCE` | Evidence against it |
| `CONTEXT` | Conditions under which a relation is valid |
| `REVISION` | Explicit change in object, relation, or rule |
| `OPEN` | Registered unknown or unresolved boundary |
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
7. let Socrates construct a temporary mega-graph for one task;
8. reconcile incoming identities with existing objects;
9. detect contradiction or silent rule change;
10. preserve provenance and uncertainty;
11. promote only consolidated structure into the permanent archive;
12. retrieve one object through several different semiotic paths;
13. expose coverage and unresolved boundaries;
14. revise one local relation without rebuilding the whole field;
15. discard Socrates' temporary working graph while preserving accepted archive changes.

---

## 18. What We Explicitly Do Not Know Yet

Important open questions include:

- What physical database structure best represents the object field and relation tables?
- How should network relevance be discovered efficiently?
- How should independence between projections be measured?
- How much of Socrates must remain neural?
- Which Socratic operations can become deterministic algorithms?
- How should object identity reconciliation work across modalities?
- How should write authority and revision governance work in a public deployment?
- How should explanatory boundaries be represented formally?
- How many distinct projections are sufficient for useful reconstruction in different domains?
- How should the temporary mega-graph be constructed, limited, and discarded?

We do not know these answers yet.

That is part of the research program.

---

## Short Formula

```text
NOEPEDIA
    persistent object field
    + triplet relation tables
    + provenance / rules / history

SOCRATES
    temporary meta-semiotic reasoning
    + mega-graph workspace
    + consolidation / retrieval / consistency

LLM
    language
    + explanation
    + broad generative synthesis

AISocket / humans / instruments
    contact with the world
```

And even shorter:

> **Noepedia stores the map.**
>
> **Socrates keeps the map coherent and usable without carrying it in its head.**
>
> **Language is one way of pointing into the map, not the map itself.**

For the philosophical motivation behind this architecture, see **[GUIDING_PHILOSOPHY.md](GUIDING_PHILOSOPHY.md)**.

For the current reconstruction of the map-guardian function, see **[SOCRATIC_DAIMONION.md](SOCRATIC_DAIMONION.md)**.

---

## ქართული მოკლე აღწერა

**Noepedia არის მისამართებადი ობიექტების ველი და ამ ობიექტებს შორის მრავალი ტრიპლეტური კავშირის ცხრილი.**

ობიექტს შიგნით შეიძლება საერთოდ არ ერქვას ადამიანის ენაზე სახელი. მაგალითად `OBJECT_3768` შეიძლება ქართულ სემანტიკურ ველში უკავშირდებოდეს სიტყვას `სივრცე`, ინგლისურში `space`, რუსულში `пространство` — მაგრამ ეს სიტყვები მხოლოდ მიმთითებლებია.

Noepedia ლინგვისტური მოდელი არ არის. მისი მიზანი მეტა-სემიოტიკურია: ერთი და იგივე ობიექტი შეიძლება ერთდროულად იყოს დაკავშირებული ტექსტთან, გამოსახულებასთან, ხმასთან, გეომეტრიასთან, იერარქიასთან, ფუნქციასთან, წყაროსთან, მომსახურების მონაცემთან და სხვა მრავალ ქსელთან.

Noepedia-ს მატრიცა ჰომოიკონურია იმ აზრით, რომ მისი აღწერის საშუალებებიც შეიძლება იმავე ველში გახდეს ობიექტი: ქსელი, წესი, წესის ცვლილება და ამ ცვლილების მიზეზიც მისამართებადი და ერთმანეთთან დაკავშირებადია. ამიტომ რუქას შეუძლია თავისი თავის შეცვლაც. ეს თავისუფლება ზრდის Daimonion-ის პასუხისმგებლობას: მან ცვლილება არ უნდა აკრძალოს, მაგრამ უნდა შეინარჩუნოს, **რატომ გახდა ცვლილება საჭირო და რა შეიცვალა მის შედეგად**.

**Socrates სხვა რამეა.** ის არის Noepedia-სთან მომუშავე ექსპერიმენტული LSM. მისი მეგაგრაფი არის დროებითი სამუშაო სცენა და არა მუდმივი არქივი. Socrates საჭირო ობიექტებსა და კავშირებს დროებით კრებს, ადარებს, ამოწმებს, კონსოლიდირებს და მხოლოდ ამის შემდეგ სთავაზობს მუდმივ არქივს ცვლილებას.

არქივიდან ცოდნის ამოღება შეიძლება ბევრმა სისტემამ შეძლოს. ჩაწერა უფრო მკაცრი ოპერაციაა: დაუმუშავებელი ტექსტი, ვიდეო, სენსორის ნაკადი ან ჰიპოთეზა ჯერ staging სივრცეში უნდა დარჩეს და არ უნდა გამოცხადდეს ავტომატურად Noepedia-ს ცოდნად.

მოკლე ფორმულა:

> **Noepedia ინახავს.**  
> **Socrates დროებით ფიქრობს, ალაგებს და იცავს წესრიგს.**  
> **ჰომოიკონურობა რუქას აძლევს თვითრედაქტირების თავისუფლებას; Daimonion იცავს ამ თავისუფლების პატიოსნებას.**  
> **ენა მხოლოდ ერთ-ერთი გარე მიმთითებელი ფენაა.**

---

## License

Software in this repository is licensed under the GNU Affero General Public License v3.0.

Licensing for public knowledge data and human-readable content should be specified separately before public ingestion begins.

---

**Born from AISocket. Expanded through dialogue. Still open to revision.**
