# Noepedia

> **Knowledge should not have to be rediscovered.**
>
> **Discovery should become structure.**

Noepedia is an open attempt to build a **persistent, addressable, inspectable model of knowledge outside the weights of any one language model**.

It is not only a store of facts.

It is also a field of **many explicit evaluative networks** built over shared objects: networks of similarity, difference, hierarchy, function, evidence, chronology, causality, reliability, prototype membership, context, and other forms of relation.

A fact can be inserted as an object before we know what it means in the larger field.

The harder operation is deciding **where that object belongs, under which rule, and why**.

That distinction is central to Noepedia.

> **Object insertion is cheap. Meaningful implantation is arguable.**

Noepedia therefore tries to preserve not only knowledge objects, but the publicly inspectable argument for where those objects belong in meaning.

---

## The Core Cycle

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

---

## Three Layers

A simple working picture of Noepedia has three layers.

### 1. Object field

What exists or has been observed:

```text
object
measurement
document
person
board
component
event
experiment
claim
source
```

An object may enter the field with very little interpretation.

### 2. Semiotic and evaluative networks

The same object may participate in many independent projections:

```text
IS-PART-OF
IS-INSTANCE-OF
RESEMBLES
DIFFERS-FROM
SUPPORTS
CONTRADICTS
PRECEDES
CAUSES
FUNCTIONS-AS
VALID-IN-CONTEXT
BELONGS-TO-PROTOTYPE
RANKED-BY-RELIABILITY
```

The object does not have one final, universal shelf.

It may occupy different places in different networks because the networks ask different questions.

### 3. Evaluation process

Why is an object placed there?

Why should the relation be trusted?

What would move it?

Which alternative placements were considered?

What evidence is missing?

This third layer makes implantation inspectable instead of mystical.

---

## Every Network Has a Rule Card

A Noepedia network is not merely a bag of links.

It has a rule describing what the network evaluates and how objects are placed or ranked within it.

For example:

```text
NETWORK: functional_similarity
RULE: rank objects by similarity of performed function,
      ignoring manufacturer and historical origin
```

or:

```text
NETWORK: evidence_strength
RULE: rank claims by quality, independence,
      reproducibility, and relevance of supporting evidence
```

The rule belongs to the network.

It does not need to be memorized inside the navigator's neural weights.

The navigator can read the rule when it enters the network.

This leads to a basic invariant:

> **A network must remain faithful to the rule by which it evaluates its objects.**

If one object is judged by rule X and another is quietly judged by rule Y, the network is no longer internally coherent.

Changing a rule is allowed.

Changing it silently is not.

A rule change should itself become an inspectable revision:

```text
old rule
↓
problem discovered
↓
argument
↓
new rule
↓
re-evaluation of affected placements
```

---

## Large Semiotic Model — LSM

**Large Semiotic Model (LSM)** is the working name for a learned system that operates over this field of explicit, rule-governed projections.

Noepedia and LSM are not the same thing.

```text
Noepedia
    persistent external field of objects,
    networks, rules, evidence, history

LSM
    learned system that navigates,
    compares, tests and coordinates that field
```

Our proposed Noepedia implementation of an LSM is called **Socrates**.

So the naming is:

> **LSM — the general class.**
>
> **Socrates — Noepedia's experimental LSM navigator.**

---

## Socrates

Socrates is not intended to be another model that memorizes the world.

Its main competence is to operate correctly among knowledge structures.

It should learn skills such as:

```text
identify the relevant network
read its rule
apply the same rule consistently
find candidate placements
compare placements
move up and down hierarchy
find prototypes
find analogies
find discriminating differences
locate supporting evidence
locate counterevidence
detect contradiction
detect weak implantation
identify missing tests
compare alternative networks
estimate coverage
preserve OPEN when closure is unjustified
```

The important point is that **facts can remain outside Socrates, networks can remain outside Socrates, and even the rules of those networks can remain outside Socrates**.

Socrates needs to learn how to work with them.

A useful minimal formula is:

```text
Network = objects + relations + rule card + history

Socrates = learned ability to move among networks
           without letting them quietly violate their own rules
```

A working metaphor is a spider moving through many webs.

The metaphor is optional; the technical idea is not.

---

## Socratic Argument as a Meaning-Edit Protocol

Changing an object's meaning is not forbidden.

But a proposed change should survive questions.

If someone wants to move an object inside a network, or attach it to a different prototype, Socrates should be able to ask:

```text
Why this network?
Which rule applies?
Which features support this placement?
Which features do not match?
What alternative placements were considered?
What evidence supports the move?
What evidence contradicts it?
What test would separate the alternatives?
Does this new placement contradict an earlier placement
under the same rule?
```

This is not authority by personality.

It is an attempt to make **meaning edits auditable**.

A participant may disagree with the current structure.

The system should make disagreement possible without allowing silent rule changes or silent erasure of prior reasoning.

---

## Implantation Quality Must Be Inspectable

A relation should not receive a mysterious confidence number and stop there.

A proposed implantation should expose its support structure.

For example:

```text
OBJECT: BOARD-742
PROPOSED NETWORK: power_topology_family
PROPOSED PLACEMENT: prototype P17

SUPPORTING FEATURES:
    F1, F2, F4

IMPORTANT DIFFERENCES:
    D2

ALTERNATIVE PLACEMENTS:
    P11, P23

EVIDENCE:
    E51, E63

MISSING TEST:
    T8

COUNTEREVIDENCE:
    none known

STATUS:
    PROVISIONAL
```

Anyone should be able to descend into this structure and inspect why the placement exists.

The system should therefore support both:

```text
What do we currently think?
```

and:

```text
Why do we currently think it?
```

---

## Meaning Can Be Reconstructed From Many Projections

One network is usually a poor description of an object.

A few networks may still be too weak.

But the same object viewed through many independent, disciplined projections can become increasingly reconstructible.

For example:

```text
network A → what it resembles
network B → what it does
network C → where it came from
network D → what evidence supports it
network E → what it contradicts
network F → which prototype contains it
network G → where it fails
...
```

The working hypothesis is that **meaning can emerge from the intersection of enough well-formed projections**.

How many are enough?

We do not know.

Perhaps a domain needs 724 useful projection types.

Perhaps 3,000.

Perhaps 7,823.

Perhaps the number matters less than independence, quality, and coverage.

These numbers are illustrative only.

> **The required number and diversity of semiotic projections is an experimental question.**

We do not know the answer, and Noepedia should record that ignorance rather than hide it.

---

## A Working Hypothesis About Intelligence

Noepedia uses the following as a research hypothesis, not a settled definition:

> **High intelligence may depend less on possessing many isolated facts and more on the ability to coordinate many different evaluative projections of the same world without destroying their rules, while keeping the resulting reconstruction inspectable and testable.**

This does not mean forcing every network to agree.

Two networks may legitimately produce different evaluations because they measure different things.

For example:

```text
network A → excellent strength
network B → poor weight efficiency
```

The intelligent operation is not to average them into "neutral".

It is to know **what each network evaluates, when each matters, and how their results combine in the current context**.

---

## Coverage, Not Only Confidence

A conclusion can look strong simply because only one relevant perspective has been consulted.

Noepedia should therefore be able to record **coverage** as well as confidence or support.

For example:

```text
CURRENT CONCLUSION: C17

relevant networks identified: 25
evaluated: 18
not yet evaluated: 7
supporting: 11
neutral / unrelated: 5
conflicting: 2

status: PROVISIONAL
```

This allows the system to distinguish:

> "The evaluated networks agree."

from:

> "The relevant networks have been sufficiently surveyed."

Those are not the same statement.

A related research hypothesis is that some apparently abrupt human changes of interpretation may resemble **serial dominance over a larger parallel set of evaluative networks**: one projection temporarily dominates before other relevant projections are brought into the active reconstruction.

Noepedia does not assume that this is a complete psychological theory.

It is useful here as an architectural warning:

> **A partial reconstruction must not pretend to be a complete one.**

---

## Socrates Begins Neural

Socrates should begin as a neural system because **we do not yet know the full shape of its task**.

If we freeze the task too early into hand-written algorithms, we may formalize only the operations we already know how to name.

The neural stage is therefore also a discovery stage.

We can expose Socrates to many cases of:

```text
network selection
rule interpretation
object implantation
competing placements
analogy
hierarchy
contradiction
missing evidence
rule revision
successful argument
failed argument
new test selection
```

Then we can observe which operations recur.

Stable recurring patterns may later be extracted into deterministic algorithms.

The intended development path is therefore:

```text
Stage 1 — Neural Socrates
learn the still-unknown task

Stage 2 — Pattern discovery
identify recurring semiotic operations

Stage 3 — Algorithmic extraction
move stable operations into explicit software

Stage 4 — Hybrid Socrates
algorithms handle known operations
neural components handle ambiguity and novelty
```

This mirrors the broader Noepedia principle:

> **When the unknown becomes regular, it no longer needs to remain expensive intelligence.**

---

## LLM and Socrates Have Different Jobs

Socrates is not a replacement for an LLM.

The two systems solve different problems.

A useful division of labor is:

```text
LLM
    language
    explanation
    broad synthesis
    hypothesis generation
    novel semantic construction
    interaction with humans

Socrates / LSM
    network selection
    rule reading
    placement
    comparison
    consistency checking
    evidence routing
    contradiction detection
    coverage checking
    navigation through explicit knowledge

Noepedia
    persistent external objects
    networks
    rules
    evidence
    history

AISocket
    observation
    experiment
    bounded action in the real world
```

A frontier LLM is especially valuable when existing structure is insufficient and something genuinely new must be proposed or understood.

Socrates should help determine **when that expensive step is actually necessary**.

---

## A Knowledge Node Is Not Just a Sentence

A central Noepedia object should not be only a statement such as:

> X is true.

A useful knowledge node should answer two different questions:

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

The exact thresholds should depend on domain and consequence.

Three replications are not a universal law of science.

The architecture should simply be able to represent **independent repetition explicitly**.

Popularity, authority, confidence, and eloquence are not substitutes for repetition.

---

## Knowledge Grows in More Than One Direction

Noepedia should not be imagined as a flat database.

A living knowledge field grows in at least three directions.

### Breadth

More cases, objects, domains, experiments, failures, exceptions, and observations are added.

### Height

Concrete cases are compared and abstracted into higher structures:

```text
instance
→ pattern
→ prototype
→ family
→ class
→ general relation
```

### Length

Knowledge has a history:

```text
we believed A
→ evidence E appeared
→ A split into A1 and A2
→ new context C was discovered
→ old result remained valid only locally
```

Noepedia should preserve this genealogy rather than overwrite yesterday with today.

The history of how a model changed is itself knowledge.

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

The final reusable conclusion is useful.

The path that created it must remain inspectable.

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
PARTIAL COVERAGE → COMPLETE UNDERSTANDING
```

---

## Relationship to AISocket

AISocket and Noepedia operate at different boundaries of the same larger architecture.

Noepedia stores explicit reusable knowledge.

Socrates navigates and checks that knowledge.

AISocket gives an authorized intelligence a bounded way to observe, test, and act in a local physical or software world.

```text
Noepedia
    ↓
Socrates selects relevant knowledge and unresolved gaps
    ↓
AISocket
    ↓
bounded observation / experiment / action
    ↓
real-world evidence
    ↓
Noepedia
```

AISocket therefore does not need to become a knowledge store.

It should return structured traces and evidence that can later become knowledge.

---

## Relationship to OpenPCB Commons

OpenPCB Commons is a natural proving ground for the whole architecture.

OpenPCB can preserve object-specific evidence:

```text
board photo
geometry
component marking
probe position
measurement
waveform
instrument
conditions
replication report
repair outcome
```

Noepedia can preserve reusable structure extracted from that evidence:

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

Socrates can be tested on practical semiotic tasks such as:

```text
board-family recognition
circuit-motif recognition
prototype matching
topology similarity
donor-part search
evidence reconciliation
identifying the next discriminating measurement
```

This makes OpenPCB more than an application example.

It can become an experimental domain that tells us what Socrates must actually learn to do.

---

## Energy and Compute Efficiency

Energy efficiency is an important motivation, but it is **not the definition of Noepedia**.

If a known relation can be retrieved or traversed directly, it should usually be cheaper than asking a large generative model to reconstruct the same relation from a large context.

But the real difference depends on implementation and must be measured.

Even if the eventual energy gain is smaller than hoped, the deeper advantages remain:

- addressability;
- provenance;
- inspectability;
- explicit uncertainty;
- reuse;
- lower rediscovery;
- easier local computation;
- clearer separation between known knowledge and new inference.

---

## Publications Are Views, Not the Ontology

Noepedia may produce publications, articles, reports, or API responses.

But a publication is not the fundamental unit of the system.

Human-readable prose is a **projection**.

It is not the authority layer.

Likewise, LLM weights are not the authority layer for settled Noepedia knowledge.

The authority layer is the inspectable field together with its network rules, evidence, placement history, revisions, and unresolved conflicts.

---

## Minimal Working Objects

The exact grammar remains open, but the current conceptual minimum includes objects such as:

| Object | Purpose |
|---|---|
| `ENTITY` | An addressable thing or concept |
| `CLAIM` | A proposed assertion or relation |
| `RELATION` | A typed connection between objects |
| `NETWORK` | A rule-governed evaluative projection |
| `RULE_CARD` | The declared rule of a network |
| `PLACEMENT` | An object's position or relation inside a network |
| `PLACEMENT_ARGUMENT` | Why that placement is proposed or accepted |
| `COVERAGE` | Which relevant networks have and have not been evaluated |
| `SOURCE` | Origin of information |
| `EVIDENCE` | Support for a claim or placement |
| `COUNTEREVIDENCE` | Evidence against it |
| `OBSERVATION` | A recorded observation |
| `TEST` | A verification procedure |
| `RESULT` | Output of a test |
| `REPLICATION` | An independent repetition of a result |
| `CONTEXT` | Conditions under which knowledge applies |
| `PROTOTYPE` | A reference pattern or family center |
| `SIMILARITY` | A qualified resemblance relation |
| `DIFFERENCE` | A discriminating distinction |
| `OPEN` | A registered unknown |
| `CONFLICT` | Incompatible supported positions |
| `REVISION` | A change in a node, placement, or network rule |
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

## First Research Prototype

The first prototype should prove a **knowledge-and-meaning cycle**, not merely a user interface.

A useful test should demonstrate that the system can:

1. ingest a real object with minimal interpretation;
2. place it into one or more explicit networks;
3. expose each network's rule card;
4. show why each placement was proposed;
5. compare competing placements;
6. detect a rule violation or silent rule change;
7. preserve observation separately from inference;
8. attach evidence, counterevidence, context, and provenance;
9. record which relevant networks have not yet been consulted;
10. preserve `OPEN` and `CONFLICT` without forcing closure;
11. accept independent tests or replications;
12. revise a placement without deleting its history;
13. detect a genuine gap;
14. send that gap to an LLM, human, laboratory, or AISocket tool;
15. return the result to Noepedia as new structure.

The first version of Socrates should be neural enough to discover recurring operations rather than assuming we already know all of them.

The prototype should also record those recurring operations so that later versions can test which ones can be replaced by deterministic algorithms.

---

## What We Explicitly Do Not Know Yet

Noepedia should make its own ignorance visible.

Important open questions include:

- How many distinct network types are sufficient for useful reconstruction in a domain?
- How should network relevance be discovered?
- How should independence between projections be measured?
- How much of Socrates must remain neural?
- Which recurrent Socratic operations can become deterministic algorithms?
- How should implantation quality be measured without collapsing it into one opaque score?
- How should contradictory but individually valid networks be composed for a particular task?
- When is network coverage sufficient to act?
- How should a new network type be proposed and tested?

We do not know these answers yet.

That is not a defect in the project description.

They are part of the research program.

---

## A Short Formula

```text
WORLD
    ↓
AISocket
    observe / test / act
    ↓
NOEPEDIA
    objects + evidence + rule-governed networks + history
    ↓
SOCRATES / LSM
    read rules + navigate + compare + challenge placements + check coverage
    ↓
LLM
    language + explanation + novel synthesis when existing structure is insufficient
    ↓
new hypothesis / new experiment / new structure
```

And even shorter:

> **Noepedia stores the projections.**
>
> **Socrates learns how to move among them.**
>
> **Meaning is reconstructed from their intersection.**

---

## ქართული მოკლე აღწერა

**Noepedia მხოლოდ ფაქტების საცავი არ არის.**

იგი ინახავს ობიექტებს და მათზე აშენებულ მრავალ დამოუკიდებელ შეფასებით ქსელსაც.

ობიექტის შეტანა შეიძლება მარტივი იყოს. რთული ნაწილი არის მისი **იმპლანტირება მნიშვნელობაში** — რომელ ქსელში უნდა იდგეს, რომელი წესით, რა ნიშნებით და რა მტკიცებულებით.

ყოველ ქსელს აქვს თავისი `RULE_CARD` — რა თვისებას აფასებს და როგორ ალაგებს ობიექტებს.

თუ ეს წესი შეიცვალა, ცვლილებაც ცალკე უნდა გამოჩნდეს და ძველი განლაგებები ხელახლა უნდა შემოწმდეს.

Noepedia-ში შემოთავაზებულ LSM-ს ვარქმევთ **Socrates**.

Socrates-ს არ სჭირდება სამყაროს ყველა ფაქტის, ყველა ქსელის ან ყველა წესის საკუთარ წონებში ტარება. ფაქტები გარეთაა, ქსელები გარეთაა და ქსელების წესებიც გარეთაა. მისი ნეირონული კვალიფიკაციაა ამ წესების წაკითხვა, შესაბამისი ქსელის პოვნა, ობიექტის განლაგების შემოწმება, წინააღმდეგობის აღმოჩენა, ალტერნატივების შედარება და იმის დანახვა, რომელი მნიშვნელოვანი ხედვები ჯერ არ გამოგვიკითხავს.

მთავარი სამუშაო ჰიპოთეზაა:

> **მაღალი ინტელექტი შეიძლება ნიშნავდეს ერთი და იმავე სამყაროს მრავალი განსხვავებული შეფასებითი ქსელის წესების დაურღვევლად, შეთანხმებულად და გადამოწმებადად გამოყენების უნარს.**

რამდენი ასეთი ქსელია საკმარისი — 724, 3000, 7823 თუ სხვა რაოდენობა — არ ვიცით. ეს რიცხვები მხოლოდ მაგალითებია. პასუხი ექსპერიმენტულად უნდა ვიპოვოთ.

Socrates თავიდან ნეირონული უნდა იყოს, რადგან ჯერ თვითონ მისი სრული ტექნიკური დავალებაც არ ვიცით. ნეირონულ ეტაპზე შეიძლება გამოვავლინოთ განმეორებადი ოპერაციები; რაც სტაბილურ პატერნად ჩამოყალიბდება, მოგვიანებით ჩვეულებრივ ალგორითმად გადავიტანოთ.

ამიტომ:

```text
ობიექტი → Noepedia
მნიშვნელობის კანდიდატი → შეფასებითი ქსელები
ქსელის წესი → RULE_CARD
განლაგების კამათი → Socrates
ახალი უცნობი → LLM / ადამიანი / AISocket / ექსპერიმენტი
შედეგი → ისევ Noepedia
```

ყველაზე მოკლე ფორმულა:

> **ობიექტის ჩადება იოლია.**  
> **რას ნიშნავს და სად ეკუთვნის — ეს უნდა იყოს საკამათო, არგუმენტირებადი და გადამოწმებადი.**

---

## License

Software in this repository is licensed under the GNU Affero General Public License v3.0.

Licensing for public knowledge data and human-readable content should be specified separately before public ingestion begins.

---

**Born from AISocket. Expanded through dialogue. Still open to revision.**
