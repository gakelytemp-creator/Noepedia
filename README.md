# Noepedia

> **Knowledge should not have to be rediscovered.**
>
> **Discovery should become structure.**

Noepedia is an open attempt to build a **persistent, addressable, inspectable model of knowledge outside the weights of any one language model**.

The working term for this idea is **Large Semiotic Model (LSM)**.

A Large Language Model is powerful because enormous cultural experience leaves a distributed trace in its parameters, from which useful meaning can often be reconstructed. Noepedia asks a different question:

> Once knowledge has already been discovered, tested, distinguished, and named, why should every future intelligence have to reconstruct it again from text or from neural weights?

Noepedia tries to preserve that knowledge explicitly: as addressable objects, relations, prototypes, hierarchies, evidence, contexts, conflicts, tests, replications, revisions, and open questions.

The goal is not to replace LLMs.

The goal is to change the division of labor between **memory, navigation, reasoning, and discovery**.

```text
known structure      → preserve it
known relation       → address it
known evidence       → attach it
known uncertainty    → keep it visible
known conflict       → do not erase it
unknown relation     → investigate it
new discovery        → turn it into structure
```

A language model should not need to carry the whole world in its internal memory in order to work intelligently with the world.

It should be able to enter a structured field, find what is already known, inspect why it is believed, see what remains uncertain, and spend expensive reasoning only where something new must actually be understood.

---

## The Core Principle

Noepedia begins from one simple refusal:

> **Already acquired knowledge should not repeatedly pay the full cost of rediscovery.**

Today, much knowledge exists only in forms that must be reconstructed each time it is used:

- prose documents;
- scientific papers;
- forum threads;
- old chats;
- source code comments;
- scattered measurements;
- model weights;
- private notebooks;
- institutional memory;
- human memory.

These forms are valuable, but they often force the next user or model to repeat the same work:

```text
find sources
→ rebuild context
→ infer relations
→ separate fact from interpretation
→ detect disagreement
→ reconstruct the current model
→ answer
```

Noepedia tries to preserve the result of that work so that the next intelligence can begin **where the previous one stopped**.

```text
experience / source / experiment
            ↓
        discovery
            ↓
 explicit semiotic structure
            ↓
    reusable knowledge
            ↓
      navigation / use
            ↓
 gap, conflict, novelty, OPEN
            ↓
       new discovery
            ↓
        structure again
```

This cycle is the center of the project.

---

## Why “Large Semiotic Model”?

The phrase is intentionally different from **Large Language Model**.

Language is one way knowledge is carried. It is not the only one.

A scientific result may be represented by:

- a relation;
- a hierarchy;
- a causal structure;
- a prototype;
- a similarity pattern;
- a graph;
- a geometric form;
- an experimental trace;
- a table of replications;
- a rule;
- a counterexample;
- a temporal history;
- a boundary condition;
- an unresolved contradiction.

Noepedia treats these as first-class knowledge structures rather than forcing all of them to disappear into prose.

The term **LSM** is a working architectural idea, not a claim that the final implementation is known.

Its essential distinction is this:

```text
LLM:
meaning is largely distributed inside learned parameters
and reconstructed through generation

LSM:
meaning is also preserved outside the model
as explicit, addressable, inspectable structure
```

The two can work together.

An LLM may be excellent at interpretation, synthesis, analogy, hypothesis generation, explanation, and invention.

An LSM should make it unnecessary to repeatedly regenerate what has already become stable knowledge.

---

## The Socratic Navigator

Noepedia also suggests a different kind of learned intelligence.

Call it, for now, the **Socratic Navigator**.

It does not need to know every fact.

It needs to know how to relate to knowledge.

Its skills are closer to:

```text
What do I know?
What do I not know?
What is the evidence?
What differs?
What is similar?
What is repeated?
What is only an inference?
What is contradicted?
What is stale?
What should be tested next?
Where does a new result belong?
```

Such a system could be much smaller than a frontier LLM because it does not need to carry the full factual content of the world in its weights.

Its competence would be **navigation, discrimination, comparison, checking, and placement**.

This is only a research direction. Noepedia does not assume that the correct navigator architecture has already been found.

But it changes the design question from:

> How do we make one model remember everything?

into:

> How do we let many kinds of intelligence live effectively inside a shared external knowledge structure?

---

## A Knowledge Node Is Not Just a Sentence

A central Noepedia object should not be only a statement such as:

> X is true.

A useful knowledge node should be able to answer two different questions:

1. **What is the current usable conclusion?**
2. **Why are we allowed to say it?**

These are different layers.

A compact current node might say:

```text
CLAIM:
    Interface P uses protocol Q under conditions C.

STATUS:
    REPLICATED

VALID IN:
    hardware revision B

CONFLICT:
    revision C behaves differently
```

Below it sits the evidence structure:

| Evidence | Method | Conditions | Result | Independence | Status |
|---|---|---|---|---|---|
| E1 | direct measurement | C1 | supports | original | TESTED |
| E2 | independent replication | C1 | supports | independent | REPLICATED |
| E3 | independent replication | C1 | supports | independent | REPLICATED |
| E4 | independent replication | C1 | supports | independent | REPLICATED |
| E5 | test on revision C | C2 | contradicts | independent | CONFLICT |

The upper node allows fast use.

The evidence layer allows inspection.

This separation is crucial.

A person or small model should not need to reread forty documents to use a settled result. But at any moment it should be possible to descend from the conclusion to the evidence that supports, limits, or contradicts it.

---

## Replication Is an Operation, Not Decoration

Noepedia treats replication as part of the knowledge grammar.

A claim may move through states such as:

```text
PROPOSED
→ SUPPORTED
→ TESTED
→ REPLICATED ×1
→ REPLICATED ×2
→ REPLICATED ×3
→ reusable knowledge
```

The exact thresholds should depend on domain and consequence. Three replications are not a universal law of science.

But the architecture should be able to represent **independent repetition explicitly**.

This matters because popularity, authority, confidence, and eloquence are not substitutes for repetition.

```text
money can express demand
reputation can guide attention
confidence can guide search

but evidence and replication determine support
```

This principle is especially important for integrations such as OpenPCB Commons, where a black-box result may be claimed, independently reproduced, and only then promoted into a trusted reusable node.

---

## Knowledge Grows in More Than One Direction

Noepedia should not be imagined as a flat database.

A living knowledge field grows in at least three directions.

### 1. Breadth

More cases, objects, domains, experiments, failures, exceptions, and observations are added.

```text
one motor
→ many motors
→ many controller families
→ many machines
```

### 2. Height

Concrete cases are compared and abstracted into higher structures.

```text
instance
→ pattern
→ prototype
→ family
→ class
→ general relation
```

This is where knowledge becomes more than accumulation.

### 3. Length

Knowledge has a history.

```text
we believed A
→ evidence E appeared
→ A split into A1 and A2
→ new context C was discovered
→ old result remained valid only locally
```

Noepedia should preserve this genealogy rather than overwriting yesterday with today.

The history of how a model changed is itself knowledge.

---

## Hierarchy and Analogy

Two relations are particularly important.

### Hierarchy asks:

> What is this part of?

```text
device
→ board
→ functional block
→ circuit motif
→ component
→ physical effect
```

### Analogy asks:

> What does this resemble?

An unknown circuit may not be identical to any known design, but parts of it may resemble known prototypes:

```text
power stage resembles prototype P
protection block resembles prototype Q
connector topology resembles family R
failure pattern resembles case S
```

Hierarchy tells us **where something belongs**.

Analogy and prototype structure tell us **what it is like**.

Both are necessary for useful knowledge navigation.

A Noepedia implementation therefore should not be limited to ordinary subject-predicate facts. It must eventually support structural similarity, prototype membership, differences, inheritance, and competing classifications.

---

## Observation, Inference, and Knowledge Must Not Collapse Together

Noepedia should preserve the difference between:

```text
OBSERVATION
INFERENCE
HYPOTHESIS
TEST
RESULT
REPLICATION
CURRENT KNOWLEDGE
```

For example:

```text
OBSERVATION:
    pad A toggles at 50 kHz

INFERENCE:
    pad A may be a clock

TEST:
    hold pad A low and observe downstream behavior

RESULT:
    downstream transfer stops

REPLICATION:
    repeated independently on three boards

CURRENT KNOWLEDGE:
    pad A functions as the transfer clock on revision B
```

The final sentence is useful.

The path that created it must remain inspectable.

---

## Provenance Is Part of the Knowledge

Every meaningful contribution should retain its origin.

At minimum:

```text
who or what proposed it
which session or experiment produced it
which sources were used
which instrument or method was used
under what conditions
which version of the field existed at the time
what was changed
how it was reviewed or tested
what later happened to it
```

This is not paperwork added around knowledge.

It is part of what makes knowledge reusable.

A measurement without conditions is often not reusable.

A claim without provenance may be impossible to inspect.

A synthesis that erases disagreement may be easier to read but less useful for future reasoning.

---

## OPEN and CONFLICT Are Legal Knowledge States

Noepedia should never require the world to look more settled than it is.

When evidence is insufficient:

```text
OPEN
```

When supported models remain incompatible:

```text
CONFLICT
```

When evidence is old:

```text
STALE
```

When a result applies only under specific conditions:

```text
VALID-IN-CONTEXT
```

The system should not silently convert:

```text
PROPOSED → FACT
HYPOTHESIS → VERIFIED
POPULAR → TRUE
UNKNOWN → CONFIDENT ANSWER
ONE CONTEXT → EVERY CONTEXT
OLD EVIDENCE → CURRENT EVIDENCE
```

A complete-looking answer is not necessarily a better answer.

---

## The Division of Labor

A useful Noepedia architecture may eventually route work roughly like this:

```text
already known and validated
        → retrieve / traverse / render

routine transformation
        → deterministic software or small model

ambiguous relation
        → stronger reasoning

missing relation
        → investigation

frontier unknown
        → human + LLM + tools + experiment
```

The principle can be summarized as:

> **Use memory for what is known.**
>
> **Use intelligence for what must be understood.**
>
> **Use research for what is not yet known.**

Large LLMs remain extremely important.

Noepedia simply tries to stop using them as an expensive substitute for every other form of memory and computation.

---

## Relationship to AISocket

AISocket and Noepedia operate at different boundaries of the same larger idea.

AISocket gives intelligence a constrained way to interact with real systems.

Noepedia gives intelligence a persistent way to interact with accumulated knowledge.

```text
Noepedia
    ↓
validated local knowledge
    ↓
AISocket
    ↓
bounded experiment or action
    ↓
real-world outcome
    ↓
Noepedia
```

In this loop, the world is not merely a destination for AI answers.

The world returns evidence.

That evidence may revise the knowledge field.

---

## Relationship to OpenPCB Commons

OpenPCB Commons is a natural experimental domain for Noepedia.

OpenPCB can preserve raw, object-specific evidence:

```text
board photo
component marking
probe position
measurement
waveform
instrument
conditions
replication report
repair outcome
```

Noepedia can preserve the reusable structure extracted from that evidence:

```text
functional block
interface relation
prototype family
failure pattern
component equivalence
validated protocol
context limit
reusable second-life knowledge
```

The distinction is useful:

```text
OpenPCB asks:
What happened on this real object?

Noepedia asks:
What reusable knowledge does this become?
```

The boundary does not need to be rigid. The important point is that evidence should remain connected to the knowledge derived from it.

---

## Energy and Compute Efficiency

Energy efficiency is an important motivation, but it is **not the definition of Noepedia**.

If a known relation can be retrieved or traversed directly, it should usually be cheaper than asking a large generative model to reconstruct the same relation from a large context.

But the true end-to-end difference depends on implementation:

- storage;
- networking;
- graph traversal;
- validation;
- local inference;
- indexing;
- rendering;
- hardware;
- workload.

Therefore Noepedia treats energy reduction as an **experimental hypothesis and engineering target**, not a universal constant.

Even if the eventual energy gain were much smaller than hoped, the deeper advantages would remain:

- addressability;
- provenance;
- inspectability;
- explicit uncertainty;
- reuse;
- lower rediscovery;
- easier local computation;
- clearer separation between known knowledge and new inference.

---

## Hallucination and Transparency

Noepedia does not make intelligence infallible.

It tries to make error less able to hide.

A fluent model answer may mix:

```text
retrieved fact
inference
analogy
guess
outdated information
unsupported synthesis
```

Noepedia should make these separable.

A strict answer should be able to expose its support path:

```text
ANSWER
    supported-by: NODE-204
    evidence: E-51, E-63, E-80
    context: C-7
    replication: 3 independent
    conflict: NODE-311
    inference-added: yes/no
```

If the field does not support a requested relation, the system should be able to say:

```text
OPEN
```

instead of manufacturing closure.

---

## No Single Intelligence Owns the Field

Noepedia is compatible with:

- humans;
- LLMs;
- smaller local neural models;
- deterministic programs;
- laboratories;
- sensors;
- institutions;
- future reasoning systems not yet designed.

No central model needs to erase all differences into one final voice.

Participants may disagree.

They may contribute different evidence.

They may use different methods.

They may leave a question unresolved.

The field should outlive any one session, model, laboratory, or contributor.

---

## Publications Are Views, Not the Ontology

Noepedia may produce publications, articles, reports, or API responses.

But a publication is not the fundamental unit of the system.

The underlying knowledge field may also represent structures that are never naturally written as articles:

- a circuit prototype family;
- a similarity neighborhood;
- a causal network;
- a hierarchy;
- a timeline;
- an experiment tree;
- an unresolved conflict;
- a reusable operational package.

Human-readable prose is a **projection**.

It is not the authority layer.

Likewise, LLM weights are not the authority layer for settled Noepedia knowledge.

The authority layer is the inspectable field together with its evidence and history.

---

## Minimal Semiotic Objects

The exact grammar is still open, but the current conceptual minimum includes objects such as:

| Object | Purpose |
|---|---|
| `ENTITY` | An addressable thing or concept |
| `CLAIM` | A proposed assertion or relation |
| `RELATION` | A typed connection between objects |
| `SOURCE` | Origin of information |
| `EVIDENCE` | Support for a claim |
| `COUNTEREVIDENCE` | Evidence against a claim |
| `OBSERVATION` | A recorded observation |
| `TEST` | A verification procedure |
| `RESULT` | Output of a test |
| `REPLICATION` | An independent repetition of a result |
| `CONTEXT` | Conditions under which knowledge applies |
| `HIERARCHY` | Part-of / class / containment structure |
| `PROTOTYPE` | A reference pattern or family center |
| `SIMILARITY` | A qualified resemblance relation |
| `DIFFERENCE` | A discriminating distinction |
| `OPEN` | A registered unknown |
| `CONFLICT` | Incompatible supported positions |
| `REVISION` | A change in the knowledge model |
| `AGENT` | Human, model, program, team, lab, institution |
| `SESSION` | A bounded episode of work |
| `OUTCOME` | Real-world feedback |

Candidate statuses include:

```text
PROPOSED
SUPPORTED
TESTED
REPLICATED
CONTESTED
REFUTED
SUPERSEDED
STALE
OPEN
```

These are not frozen specifications yet.

---

## A Different Kind of Safety

Noepedia's strongest safety property is structural transparency.

Instead of relying only on one model to be wise, calibrated, complete, and correct at the same moment, the system tries to preserve conditions in which claims can be inspected and challenged.

Useful structural conditions include:

- stable addresses;
- preserved sources;
- preserved evidence;
- visible uncertainty;
- visible disagreement;
- explicit context;
- independent replication;
- provenance;
- bounded application projections;
- real-world feedback returning into the field.

This does not eliminate mistakes.

It makes mistakes easier to locate, attribute, test, revise, or keep open.

---

## Implementation Should Follow the Concept, Not Freeze It

Earlier Noepedia drafts described a specific stack involving publication services, validators, append-only logs, SQL projections, and renderers.

Those remain plausible implementation tools.

They are no longer treated as the definition of the project.

The final system may use some combination of:

- graphs;
- relational databases;
- event logs;
- vector or geometric indexes;
- neural similarity models;
- deterministic validators;
- local small models;
- LLMs;
- distributed storage;
- human review;
- experimental instruments.

The architecture should be chosen to preserve the conceptual invariants, not the other way around.

Those invariants are more important than any current software stack.

---

## First Research Prototype

The first prototype should prove a **knowledge cycle**, not merely a user interface.

A useful test would demonstrate that the system can:

1. ingest a real question or object;
2. preserve observations separately from inferences;
3. create addressable claims and relations;
4. attach evidence and context;
5. preserve hierarchy and prototype/analogy relations;
6. register `OPEN` and `CONFLICT` without forcing closure;
7. accept an independent test or replication;
8. update the current knowledge node without erasing its genealogy;
9. answer a known question by traversing stored structure;
10. expose the evidence path behind the answer;
11. detect a genuine gap;
12. send that gap to a human, LLM, laboratory, or AISocket tool for new investigation;
13. return the new result to the field as structure.

A good first domain may be one where physical evidence can be collected and repeated, such as OpenPCB Commons.

Noepedia itself can also remain a useful meta-test because the history of this concept contains successive revisions, competing formulations, and visible conceptual growth.

---

## Success Criteria

The project begins to succeed when:

- knowledge survives the session that created it;
- a later intelligence can enter without reconstructing the whole history from scratch;
- the current conclusion and its evidence remain separately inspectable;
- different participants can disagree without losing their work;
- a known relation can be reused without a large-model reconstruction step;
- a missing relation remains visibly missing rather than being silently hallucinated;
- new evidence can revise the model without deleting its history;
- hierarchy, analogy, prototype, and context improve navigation;
- an independent replication can change the epistemic status of a node;
- a small navigator can perform useful work inside a large field;
- a frontier model is called because something is genuinely unknown, not merely because the system forgot what it already knew.

Claims about energy, latency, accuracy, hallucination reduction, and model-size reduction must be measured experimentally.

---

## What Noepedia Is Not

Noepedia is not:

- an AI-written encyclopedia;
- a wiki with generated prose pasted into pages;
- a long-term chat archive;
- a RAG index that treats every retrieved passage as equivalent;
- a single LLM presented as an oracle;
- a temporary multi-agent conversation producing one disposable answer;
- a popularity-based truth system;
- a database that deletes disagreement;
- a system that confuses confidence with evidence;
- a claim that language models are obsolete.

Noepedia is an attempt to make **knowledge itself** more persistent, explicit, navigable, inspectable, and reusable.

---

## A Short Formula

```text
LLM
    learns language and reconstructs meaning

LSM / Noepedia
    preserves meaning as external structure

Socratic Navigator
    learns how to move through that structure

Human + LLM + tools
    create new knowledge where structure is missing
```

And the full loop:

```text
I do not know
→ search
→ distinguish
→ compare
→ test
→ understand
→ structure
→ preserve
→ reuse
→ detect the next unknown
```

---

## ქართული მოკლე აღწერა

**Noepedia-ს ძირითადი პრინციპია: ცოდნა ხელმეორედ მოსაპოვებელი არ უნდა იყოს.**

ერთხელ მოპოვებული, გარჩეული, შემოწმებული და სახელდებული ცოდნა უნდა გადაიქცეს ისეთ გარე სემიოტიკურ სტრუქტურად, რომელსაც შემდეგი ადამიანი, პროგრამა, პატარა მოდელი ან LLM პირდაპირ დაეყრდნობა.

Noepedia-ს სამუშაო ტერმინია **Large Semiotic Model — LSM**.

LLM-ში ცოდნის დიდი ნაწილი წონებში განაწილებულ კვალად არსებობს და პასუხისას მისი რეკონსტრუქცია ხდება. Noepedia ცდილობს უკვე მოპოვებული ცოდნა გარეთ შეინახოს — მისამართებად, იერარქიებად, ანალოგიებად, პროტოტიპებად, მტკიცებებად, დასტურებად, კონტექსტებად, წინააღმდეგობებად, ტესტებად, გამეორებებად და ისტორიად.

ამიტომ Noepedia მხოლოდ ცოდნის „კარადა“ არ არის. იგი ცოდნის **ჩასადებიც**, **გასაზრდელიც**, **გასარჩევიც** და **ხელახლა გამოსაყენებელი გარემოც** უნდა გახდეს.

ცოდნის ერთი კვანძი უნდა გვაძლევდეს ორ რამეს:

```text
რას ვამბობთ ახლა?
რატომ გვაქვს ამის თქმის უფლება?
```

ზემოთ შეიძლება იყოს ერთიანი მიმდინარე დასკვნა, ქვემოთ კი მისი მტკიცებულებებისა და დამოუკიდებელი გამეორებების ცხრილი.

Noepedia-ს ცოდნა იზრდება:

```text
სიგანეში — ახალი შემთხვევებით;
სიმაღლეში — შემთხვევიდან პროტოტიპამდე და ზოგად სტრუქტურამდე;
სიგრძეში — ცოდნის ცვლილების ისტორიით დროში.
```

იერარქია პასუხობს კითხვას — **რის ნაწილია?**

ანალოგი და პროტოტიპი პასუხობს კითხვას — **რას ჰგავს?**

`OPEN`, `CONFLICT`, `STALE` და კონტექსტური შეზღუდვა ისეთივე კანონიერი ცოდნის მდგომარეობებია, როგორც დადასტურებული მტკიცება.

დიდი LLM უნდა დარჩეს იქ, სადაც მართლაც საჭიროა ახალი მნიშვნელობის, ახალი ჰიპოთეზის, ახალი სინთეზის ან ახალი ცოდნის მოპოვება.

```text
ცნობილი → ამოიღე
რუტინული → პატარა მოდელი ან პროგრამა
გაურკვეველი → იმსჯელე
უცნობი → გამოიკვლიე
ახალი აღმოჩენა → გადააქციე სტრუქტურად
```

მოკლე ფორმულა:

> **Use memory for what is known.**  
> **Use intelligence for what must be understood.**  
> **Use research for what is not yet known.**

და ყველაზე მოკლე ფორმულა:

> **Knowledge should not have to be rediscovered.**
>
> **Discovery should become structure.**

---

## License

Software in this repository is licensed under the GNU Affero General Public License v3.0.

Licensing for public knowledge data and human-readable content should be specified separately before public ingestion begins.

---

**Born from AISocket. Expanded through dialogue. Still open to revision.**
