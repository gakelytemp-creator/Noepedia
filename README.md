# Noepedia

**A public knowledge system for creating, revising, consolidating, and safely reusing knowledge with humans and artificial intelligence.**

> Noepedia is an attempt to turn known knowledge from a repeatedly regenerated text stream into a persistent, addressable, verifiable, and reusable structure.

Noepedia was born from the AISocket project, but it is an independent open project.

---

## Purpose

Noepedia serves three primary functions:

1. **Knowledge creation**  
   Humans and artificial agents can build new knowledge structures, publish claims, attach evidence, preserve authorship, and register unresolved questions.

2. **Knowledge revision**  
   Existing knowledge can be criticized, corrected, compared, extended, and consolidated without silently erasing previous versions or disagreements.

3. **Knowledge use**  
   Applications, local models, public services, laboratories, and automated systems can retrieve a consolidated, traceable, and less hallucination-prone view of already known knowledge.

Noepedia is not only an encyclopedia.

It is a knowledge creation system, a revision system, and a knowledge-serving infrastructure.

---

## The Problem

Large language models are powerful at reconstruction, interpretation, and synthesis, but ordinary use has several weaknesses:

- the same known relationships are regenerated again and again from large amounts of text;
- long contexts consume significant compute and energy;
- provenance is often lost during synthesis;
- disagreements disappear inside fluent answers;
- unsupported claims may be presented with the same confidence as supported ones;
- a conversation may end without preserving the constructed model;
- automated systems may act on an answer that was never structurally validated.

Hallucination is especially dangerous when an answer is not merely read by a person, but used automatically by:

- industrial systems;
- public infrastructure;
- laboratories;
- accounting systems;
- medical or safety-related software;
- robots and devices;
- autonomous agents.

A fluent but unsupported sentence may be inconvenient in conversation.

The same sentence may become dangerous when converted directly into action.

Noepedia therefore treats traceability, uncertainty, conflict, and validation as part of the knowledge itself.

---

## Core Principle

Known knowledge should not need to be reconstructed from scratch every time it is used.

```text
documents and discussions
        ↓
claims, relations, evidence, tests, conflicts
        ↓
addressable knowledge field
        ↓
consolidated local projection
        ↓
article / answer / API / verified action
```

Large LLMs should be used primarily where they provide the greatest value:

```text
NOVELTY
CONFLICT
OPEN
INSUFFICIENT EVIDENCE
NEW SYNTHESIS
```

Known and repeatedly used structure should gradually move toward:

```text
deterministic rules
graph traversal
SQL queries
small local models
verified procedures
ordinary software
```

The design objective is:

```text
LLM cost ∝ novelty + conflict + OPEN
```

—not the total amount of routine knowledge use.

---

## What a Noepedia Publication Is

A publication is not only a page of text.

It is an addressable knowledge structure containing:

```text
subject
claims
objects
relations
sources
evidence
tests
results
counterexamples
comments
revisions
alternative models
conflicts
OPEN positions
authors
contributors
applications
real-world outcomes
```

A human-readable article is one projection of this structure.

The same publication may also be rendered as:

- a concise answer;
- a detailed article;
- a claim map;
- a conflict map;
- an OPEN-question list;
- a revision history;
- a machine-readable API response;
- a bounded operational instruction set.

---

## Knowledge Creation

A new publication may begin from:

- a human research question;
- an engineering problem;
- a scientific paper;
- a technical discussion;
- a dataset;
- an LLM session;
- an experiment;
- a public institution;
- an existing article that needs restructuring.

Humans and artificial agents may contribute:

- new claims;
- new relations;
- evidence;
- counterexamples;
- corrections;
- tests;
- alternative models;
- syntheses;
- unresolved questions.

Every contribution receives:

```text
stable address
author or agent identity
session identity
base version
timestamp
sources
status
review history
```

The system stores the contribution as a proposed delta rather than silently rewriting the publication.

---

## Knowledge Revision

Knowledge in Noepedia is expected to change.

Revision is not treated as damage to a finished article. It is a normal operation of the system.

```text
READ
→ PROPOSE DELTA
→ VALIDATE
→ REVIEW / TEST
→ ACCEPT / REJECT / REVISE / KEEP OPEN
→ BUILD NEW CONSOLIDATED VIEW
```

The current consolidated version may change while preserving:

- the original publication;
- all accepted and rejected proposals;
- alternative models;
- authorship;
- reasons for revision;
- unresolved conflicts;
- prior states.

`REFUTED` does not mean deleted.

A failed path may remain useful because it records what was attempted, why it failed, and under which conditions it may still matter.

---

## Consolidated Knowledge

Noepedia does not treat every comment as an independent final answer.

Many contributions may be transformed into a consolidated model.

```text
publication
+ comments
+ critiques
+ tests
+ alternative structures
        ↓
comparison
        ↓
accepted relations
preserved conflicts
preserved OPEN positions
        ↓
new consolidated version
```

The result should be easier to use than a long discussion, while remaining traceable to the discussion that produced it.

Consolidation is not forced consensus.

When evidence does not justify closure, the result remains:

```text
OPEN
```

or:

```text
CONFLICT
```

---

## Reducing Hallucination

Noepedia does not claim that hallucination can be eliminated universally.

Its goal is to make unsupported generation visible, bounded, and preventable in critical workflows.

A strict answer should be assembled from addressable claims:

```text
answer statement
    supported-by: CLAIM-204
    source: SOURCE-19
    status: TESTED
    valid-in-context: CONTEXT-7
```

When the field does not support an answer, the system should return:

```text
OPEN
```

When the field contains incompatible supported models, it should return:

```text
CONFLICT
```

When evidence is outdated or context-dependent, that limitation must travel with the answer.

The system should not silently convert:

```text
PROPOSED → FACT
HYPOTHESIS → VERIFIED
UNKNOWN → CONFIDENT ANSWER
```

---

## Safe Automatic Use

Automatic use requires stricter rules than human reading.

Before a publication can be used operationally, the system may require:

- a bounded context;
- explicit permissions;
- validated input and output schemas;
- source requirements;
- status requirements;
- safety constraints;
- reversible actions;
- human confirmation where necessary;
- an execution report;
- real-world feedback.

```text
knowledge field
        ↓
local validated projection
        ↓
operational rules
        ↓
AISocket or another bounded interface
        ↓
action
        ↓
report and outcome
        ↓
knowledge revision
```

Noepedia supplies knowledge.

An external execution layer controls whether and how that knowledge may act.

---

## Energy and Compute Efficiency

Current AI systems often spend large resources repeatedly reconstructing already known structure from unstructured text.

Noepedia attempts to preserve that structure once it has been created and validated.

This may allow many known-answer tasks to move from:

```text
large model + large context
```

toward:

```text
local field projection
+ graph traversal
+ SQL
+ deterministic renderer
+ small local model
```

The same large knowledge field does not need to fit entirely inside a model context.

A small system may navigate only the relevant local projection.

Example:

```text
global field:
millions of objects

local question:
31 objects
74 relations
5 sources
2 conflicts
1 OPEN
```

The expected result is lower cost, lower latency, easier local deployment, and less dependence on centralized large-model inference for routine known knowledge.

These efficiency claims must be measured experimentally.

---

## System Components

### 1. Field Core

Stores addressable objects, relations, claims, contexts, and statuses.

### 2. Publication Layer

Groups a subject, its claims, sources, conflicts, revisions, and views.

### 3. Delta Protocol

Defines legal operations for creating, changing, relating, and reviewing objects.

### 4. Validator

Checks references, schemas, provenance, status transitions, permissions, and consistency rules.

### 5. Event Log

Stores the authoritative append-only history.

### 6. Projection Database

Builds the current searchable state from the event log.

### 7. Consolidation Engine

Compares proposals and produces a new current model without deleting disagreement or history.

### 8. Renderer

Produces human-readable articles, summaries, graphs, reports, and machine-readable views.

### 9. LLM Prompt and Tool Interface

Provides a standard participation protocol for LLMs.

### 10. Application API

Allows external software to retrieve bounded, validated knowledge projections.

---

## Standard LLM Participation

Noepedia includes a prompt and tool interface so that an LLM can participate without the user manually explaining the protocol in every session.

The standard instructions define:

- how to read a publication;
- how to navigate addresses;
- how to distinguish current knowledge from a proposal;
- how to preserve provenance;
- how to create a delta;
- how to attach authorship;
- how to mark uncertainty;
- how to preserve `OPEN`;
- how to report conflicts;
- how to request consolidation;
- how to return a machine-readable result.

A Noepedia-compatible LLM should never write directly to the official field.

It submits a proposal.

The validator and review process decide what becomes part of the consolidated publication.

---

## Minimal Data Objects

The first version should support:

| Object | Purpose |
|---|---|
| `ENTITY` | Any addressable subject or object |
| `CLAIM` | A proposed assertion or relationship |
| `SOURCE` | Origin of a claim |
| `EVIDENCE` | Support for a claim |
| `COUNTEREXAMPLE` | Evidence against a claim |
| `TEST` | A method of verification |
| `RESULT` | Output of a test |
| `OPEN` | A registered unknown |
| `CONFLICT` | Incompatible claims or models |
| `CONTEXT` | Conditions under which a claim applies |
| `AGENT` | Human, LLM, program, team, or institution |
| `SESSION` | A bounded episode of work |
| `DELTA` | A proposed change |
| `REVIEW` | An evaluation of a proposal |
| `PUBLICATION` | A named knowledge field |
| `APPLICATION` | Use of knowledge in a system |
| `OUTCOME` | Real-world feedback |

Initial statuses:

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

---

## Authorship and Provenance

Authorship attaches to individual contributions, not only to the publication title.

The system records:

```text
who contributed
what was contributed
which model or tool participated
which sources were used
which version was modified
which review accepted or rejected it
how the contribution affected the consolidated result
```

The factual history of contribution must remain recoverable.

Recognition, reputation, and benefit may be handled by later layers, but provenance is part of the knowledge core.

---

## Architecture

```text
Web App / Local Client / LLM Tool
              ↓
         Noepedia API
              ↓
       Publication Service
              ↓
        Delta Validator
              ↓
    Append-only Event Store
              ↓
 SQLite / PostgreSQL Projection
              ↓
 Search / Graph / Local Projection
              ↓
 Renderer / Consolidator / External API
```

Suggested repository structure:

```text
Noepedia/
├── README.md
├── prompts/
│   └── READ_NOEPEDIA_FIELD.md
├── spec/
│   ├── FIELD_SPEC.md
│   ├── PUBLICATION_SPEC.md
│   ├── DELTA_SPEC.md
│   └── VALIDATION_SPEC.md
├── field-core/
├── validator/
├── event-store/
├── projection-db/
├── consolidator/
├── renderer/
├── app/
├── api/
├── examples/
└── docs/
```

---

## First MVP

The first prototype must demonstrate the complete system, not only a user interface.

It should support:

1. creation of a publication;
2. creation of an addressable claim network;
3. attachment of sources and authorship;
4. submission of comments as deltas;
5. validation of references and status transitions;
6. comparison of multiple proposals;
7. consolidation into a new current model;
8. preservation of conflicts and `OPEN` positions;
9. deterministic article rendering;
10. strict machine-readable question answering;
11. export of a local projection for a small model or ordinary program.

The first test domain may be Noepedia itself, because its conceptual history already contains multiple human and LLM contributions, revisions, conflicts, and open questions.

---

## Success Criteria

The first Noepedia prototype succeeds when:

- an independent LLM can read a publication using only the standard prompt and field;
- it can reconstruct the main model;
- it can identify what is supported, contested, and open;
- it can return a valid delta;
- multiple deltas can be consolidated without erasing provenance;
- a deterministic renderer can produce a readable article;
- a strict API can answer known questions without inventing unsupported relations;
- routine retrieval uses less compute than reconstructing the same answer from a large raw-text context.

---

## Relationship to AISocket

Noepedia was born from AISocket, but it is independent.

```text
AISocket
    ↓
Peer Socket
    ↓
shared addressable knowledge field
    ↓
Noepedia
```

AISocket connects intelligence to closed systems and shared workspaces.

Noepedia is the public infrastructure in which knowledge can be created, revised, consolidated, and safely reused.

---

## Project Status

**Conceptual design / pre-alpha**

Immediate work:

- freeze the minimal field grammar;
- define the publication format;
- define legal delta operations;
- define the standard LLM prompt;
- implement the validator;
- implement the append-only event log;
- implement the first consolidator;
- implement the deterministic renderer;
- build one complete test publication;
- measure accuracy, hallucination rate, latency, token use, and energy cost.

---

## ქართული მოკლე აღწერა

**ნოეპედია არის ცოდნის შექმნის, რევიზიის, კონსოლიდაციისა და უსაფრთხო გამოყენების საჯარო სისტემა.**

იგი ემსახურება სამ ძირითად ამოცანას:

```text
ახალი ცოდნის შექმნა
არსებული ცოდნის გადამოწმება და შესწორება
ნაცნობი ცოდნის იაფი და ნაკლებად ჰალუცინაციური გამოყენება
```

ნოეპედიაში სტატია მხოლოდ ტექსტი არ არის. მის ქვემოთ ინახება მტკიცებები, წყაროები, მტკიცებულებები, კონფლიქტები, `OPEN` კითხვები, ავტორობა, ცვლილებები და რეალურ ცხოვრებაში მიღებული შედეგები.

დიდი LLM გამოიყენება იქ, სადაც საჭიროა ახალი ცოდნა, რთული სინთეზი ან კონფლიქტის გადაჭრა. უკვე ცნობილი და შემოწმებული ცოდნა თანდათან გადადის მცირე ადგილობრივ მოდელებში, გრაფულ ნავიგაციაში, SQL-ში და ჩვეულებრივ პროგრამებში.

ეს განსაკუთრებით მნიშვნელოვანია ავტომატური გამოყენებისას, რადგან ჰალუცინაციური პასუხი შეიძლება არა მხოლოდ მცდარი ტექსტი, არამედ მცდარი მოქმედების მიზეზიც გახდეს.

---

## License

Software in this repository is licensed under the **GNU Affero General Public License v3.0**.

Licensing for public knowledge data and human-readable content will be specified separately before public ingestion begins.

---

**Born from AISocket. Independent by design.**
