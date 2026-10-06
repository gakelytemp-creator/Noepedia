# Experimental Part — Requirements, Tasks, and Validation Program

> **Current architecture precedence:** implementation and new experiments must follow [CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md), [SOCRATIC_DAIMONION.md](SOCRATIC_DAIMONION.md), and [DIRECTION.md](DIRECTION.md). Older metaphors in this document are historical/conceptual where they conflict with that boundary.

> **Status:** experimental design specification.
>
> This file defines what must be built, measured, compared, and falsified before strong scientific claims can be made about Noepedia.
>
> The companion file [THEORETICAL_PART.md](THEORETICAL_PART.md) contains the conceptual architecture and hypotheses.
>
> The rule of this section is:
>
> **No experiment exists merely to illustrate the theory. Every experiment must have a failure condition capable of forcing a theoretical REOPEN.**

---

# 0. Phase Reset — October 2026

The experimental program is being restarted from a deeper conceptual layer.

Experiments 001–073 remain part of the permanent research record, but their current interpretation is limited: they explored useful mechanisms, real-data behavior, controls, revision, transfer, and failure modes **before the structural requirements of the LSM field were explicit enough**.

The new sequence will not begin by training or optimizing a Daimonion. It will begin by isolating candidate LSM field rules and asking what intellectual capability, if any, each rule adds.

The unit of evidence becomes:

~~~text
RULE OFF
vs
RULE ON
→ measurable change in structural / intellectual capability
~~~

The current candidate family includes object identity independent of names; predicates as ordinary addressable objects; predicate hierarchy and decomposition; provisional fundamental status; explicit antipredicate relations; lifecycle rules for missing counterparts and orphaned objects; OPEN preservation; DREAM-style internal reprocessing; and possible interchangeable parallel Daimonion workers.

The project makes no commitment to preserve this philosophy if it fails. A concept that does not create reproducible leverage should be modified or discarded. The architecture may be rebuilt repeatedly until the surviving rules are earned by experiment.

See [experiments/PHASE_RESET_LSM_STRUCTURAL_RULES.md](experiments/PHASE_RESET_LSM_STRUCTURAL_RULES.md).

# 1. Experimental Goal

The experimental program must answer one practical question:

> **Does the Noepedia architecture create measurable operational leverage compared with repeatedly reconstructing the same knowledge through a general-purpose LLM alone?**

Operational leverage means at least one of:

- lower compute;
- lower latency;
- smaller context;
- better uncertainty localization;
- better provenance;
- fewer unsupported closures;
- better search-space reduction;
- more reliable local revision;
- more informative self-diagnosis.

---

# 2. Experimental Requirements

Every experiment must specify:

1. **Question**
2. **Hypothesis**
3. **Input**
4. **Baseline**
5. **Noepedia condition**
6. **Controlled variable**
7. **Measured outputs**
8. **Success criterion**
9. **Failure criterion**
10. **REOPEN condition**
11. **Raw logs / provenance**
12. **Reproducibility instructions**

No qualitative demo should be accepted as evidence unless its success criterion was defined before the run.

---

# 3. Baseline Requirements

At minimum compare against:

### Baseline A — LLM-only
Raw task context passed directly to an LLM.

### Baseline B — Retrieval + LLM
Relevant documents retrieved, but without explicit Noepedia structures.

### Baseline C — Deterministic / hand-coded method
Where available.

### Baseline D — Human-assisted reconstruction
Optional, but useful for complex pilot tasks.

The goal is not to make Noepedia win.

The goal is to determine **where it helps, where it does nothing, and where it makes things worse**.

---

# 4. Experimental Infrastructure Requirements

Before running the full program, implement:

## 4.1 Minimal persistent field

Must support:
- stable object IDs;
- predicates as objects;
- relation networks;
- provenance;
- versions;
- revisions;
- relation status;
- OPEN;
- OPEN_SPACE;
- REOPEN.

## 4.2 Minimal Daimonion operator

Must support:
- route candidate structure;
- select placement/network;
- select retrieval/query procedure;
- select explicit comparator/test procedure;
- assemble a minimal task cut;
- return OPEN / NO_RESULT / ESCALATE;
- preserve source/procedure provenance.

A Daimonion decision alone must not emit a support token. Tokens must be attributable to source contact or an explicit procedure result.

## 4.3 Mega-graph constructor

Must assemble the **smallest sufficient** task-specific cut and must support local widening when the first cut is insufficient. The experiment should measure both omitted necessary structure and unnecessarily loaded structure.

## 4.4 Logging

Every operation must log:
- timestamp;
- process identity;
- input cut;
- operation;
- output;
- provenance;
- reason for escalation;
- reason for commit/reject/reopen.

## 4.5 Baseline runner

The same task must be runnable under baseline and Noepedia conditions.

---

# 5. Experiment A — End-to-End Relational Reconstruction

## Question

Can an explicit relational field reconstruct a task-relevant scene from distributed stored relations?

## Hypothesis

A task-specific mega-graph can reconstruct the relevant scene with less context and equal or better task success than LLM-only reconstruction.

## Candidate domain

OpenPCB hardware object.

## Inputs

- photos;
- board labels;
- measured continuity;
- component identities;
- prior notes;
- partial schematic relations.

## Baselines

- LLM with all raw text/files;
- retrieval + LLM.

## Noepedia condition

- field lookup;
- relation cut;
- mega-graph assembly;
- optional LLM only for unresolved edges.

## Metrics

- reconstruction correctness;
- provenance completeness;
- context size;
- LLM token use;
- latency;
- number of unresolved relations;
- local edit cost.

## Success criterion

Noepedia matches or improves task correctness while reducing at least one resource cost and preserving provenance.

## Failure criterion

Noepedia adds overhead without reducing context, search, or error.

## REOPEN condition

If scene assembly repeatedly misses critical relations, revisit network/lens design.

---

# 6. Experiment B — Mismatch-Driven Actualization

## Question

Does reconstruction mismatch localize the real problem?

## Hypothesis

Mismatch localization reduces the candidate search space before expensive reasoning.

## Procedure

Inject one controlled error into a known relation set.

Examples:
- wrong component identity;
- wrong causal relation;
- wrong temporal order;
- wrong part–whole relation.

## Baseline

Ask LLM to diagnose from full context.

## Noepedia condition

Reconstruct expected scene and compare with observed evidence.

## Metrics

- candidate count before / after;
- tests required;
- time to localization;
- LLM calls;
- false exclusions;
- final diagnosis accuracy.

## Success criterion

Significant reduction in search space without eliminating the true cause.

## Failure criterion

Mismatch localization is as expensive as full reasoning or frequently removes the correct hypothesis.

---

# 7. Experiment C — OPEN-Generated Requirement

## Question

Can unresolved structure generate a useful next measurement without an external prompt specifying which measurement to take?

## Hypothesis

An OPEN / OPEN_SPACE can produce a REQUIREMENT that selects a more informative next observation than random or naive selection.

## Procedure

Create an incomplete known case with several possible measurements.

## Baselines

- random next measurement;
- fixed checklist;
- LLM suggestion without explicit field structure.

## Metrics

- information gained;
- candidate-space reduction;
- cost of measurement;
- number of measurements to resolution.

## Success criterion

OPEN-driven measurement reaches resolution with fewer or cheaper measurements.

## Failure criterion

Generated requirements are no better than random/fixed baselines.

---

# 8. Experiment D — Reciprocal Reconstruction

## Question

Do paired incomplete processes constrain each other usefully?

## Primary case

Assembly ↔ disassembly.

## Hypothesis

Knowledge from one direction reduces ambiguity in the other.

## Procedure

Remove selected steps from both directions.

## Conditions

1. assembly only;
2. disassembly only;
3. reciprocal cross-constraint.

## Metrics

- candidate sequence count;
- recovered step accuracy;
- invalid sequence rejection;
- compute;
- number of OPENs closed.

## Success criterion

Reciprocal condition reduces ambiguity without introducing false constraints.

## Failure criterion

Dual representation adds coordination cost with no measurable gain.

---

# 9. Experiment E — Equivalent Substitution

## Question

Can a rendered partial model be inserted into an incomplete whole to test compatibility?

## Candidate domains

- PCB subcircuit;
- mechanical assembly;
- 3D component.

## Hypothesis

Part–whole constraint propagation detects incompatible candidate parts before full reconstruction.

## Metrics

- false acceptance;
- false rejection;
- mismatch localization;
- correction path length.

## Success criterion

Hybrid scene rejects incompatible candidates earlier than full-scene reasoning.

---

# 10. Experiment F — Controlled Axis Withdrawal

## Question

Can the architecture detect degradation of its own representation?

## Hypothesis

Removing a discrimination axis produces measurable deformation before complete task failure.

## Candidate axes

- provenance;
- time;
- causality;
- part–whole relation;
- branch/context;
- one explicit lens family.

## Procedure

1. establish healthy baseline;
2. remove one axis;
3. rerun same tasks;
4. measure state collapse / false closure;
5. test Daimonion self-detection.

## Metrics

- reconstruction degeneracy;
- false-closure rate;
- unsupported certainty;
- self-detection latency;
- diagnostic-independence success;
- downstream task degradation.

## Success criterion

At least some degradations are detected internally before catastrophic failure.

## Failure criterion

The system remains confidently wrong with no internal diagnostic signal.

---

# 11. Experiment G — Lens Stabilization

## Question

Can repeated LLM reasoning be converted into an explicit reusable lens?

## Procedure

Collect repeated cases requiring the same transformation.

Examples:
- identify same structural relation across different objects;
- infer same part-role relation;
- perform same normalization / transformation.

## Stages

1. LLM solves repeated cases;
2. recurring transform is extracted;
3. candidate lens is encoded;
4. lens is tested on held-out cases;
5. failure boundaries are recorded.

## Metrics

- held-out accuracy;
- transfer range;
- lens execution cost;
- verification cost;
- failure-boundary precision;
- LLM calls avoided.

## Success criterion

Explicit lens preserves acceptable accuracy and lowers repeated reasoning cost.

## Failure criterion

Lens overfits or requires verification nearly as expensive as original LLM reasoning.

---

# 12. Experiment H — Settled vs Open Routing

## Question

Does the routing gate save more than it costs?

## Conditions

- always LLM;
- LSM/Noepedia first, LLM only on OPEN;
- retrieval + LLM.

## Metrics

- false-settled rate;
- false-open rate;
- routing cost;
- LLM calls;
- latency;
- tokens;
- task accuracy.

## Success criterion

Total cost drops without unacceptable false-settled errors.

## Failure criterion

Routing overhead erases savings or suppresses needed LLM escalation.

---

# 13. Experiment I — Local Revision

## Question

Can one relation be revised without global reconstruction?

## Procedure

Change one relation with known downstream dependents.

## Metrics

- number of affected nodes;
- recomputation region;
- repair time;
- unaffected-region stability;
- provenance preservation.

## Success criterion

Revision remains bounded to the actual dependency region.

## Failure criterion

Most local edits trigger near-global recomputation.

---

# 14. Experiment J — Structural Handoff

## Question

Can two agents continue work by exchanging structured state instead of re-describing it in prose?

## Conditions

1. text-only handoff;
2. structured Noepedia handoff.

## Handoff package

- working scene;
- OPEN list;
- mismatch field;
- active lens tree;
- provenance;
- tested alternatives.

## Metrics

- reconstruction time after handoff;
- context size;
- repeated work;
- task error;
- missed constraints.

## Success criterion

Structured handoff reduces duplicated reconstruction.

---

# 15. Experimental Metrics

## 15.1 Epistemic

- OPEN birth rate;
- REOPEN rate;
- false closure;
- unsupported claim rate;
- mismatch localization cost;
- candidate-space reduction;
- provenance coverage.

## 15.2 Structural

- layer birth;
- layer closure;
- lens reuse;
- reciprocal reconstruction gain;
- representational rank under degradation;
- reconstruction degeneracy.

## 15.3 Process

- Daimonion self-detection latency;
- merge conflict rate;
- handoff reconstruction cost;
- coordination cost.

## 15.4 Computational

- token count;
- LLM calls;
- latency;
- memory / storage;
- routing cost;
- consolidation cost;
- energy proxy where measurable.

## 15.5 Economic

- cost per settled query;
- cost per OPEN escalation;
- lens amortization point;
- maintenance cost per accepted relation.

---

# 16. Experimental Task Order

Do not attempt all experiments at once.

Recommended order:

## Phase 0 — Infrastructure
Build only what is required for experiments.

Tasks:
- minimal object store;
- relation networks;
- OPEN;
- provenance;
- revision;
- transaction log;
- mega-graph cut;
- baseline runner.

## Phase 1 — Reconstruction
Run:
- Experiment A;
- Experiment I.

Purpose:
prove that the field can represent and revise real knowledge.

## Phase 2 — Actualization
Run:
- Experiment B;
- Experiment C.

Purpose:
prove that OPEN and MISMATCH create useful work.

## Phase 3 — Reciprocal structure
Run:
- Experiment D;
- Experiment E.

Purpose:
test whether cross-constraints reduce ambiguity.

## Phase 4 — Self-diagnosis
Run:
- Experiment F.

Purpose:
test representation integrity.

## Phase 5 — LLM–LSM division of labor
Run:
- Experiment G;
- Experiment H.

Purpose:
test stabilization and cost transfer.

## Phase 6 — Multi-agent structural exchange
Run:
- Experiment J.

Purpose:
test whether structure can replace repeated semantic re-description.

---

# 17. Prototype Requirements by Phase

## Phase 0 minimum

Must exist:
- object IDs;
- SPO relations;
- network IDs;
- provenance;
- OPEN;
- relation status;
- revision history;
- simple query;
- exportable log.

Must **not** yet require:
- full Daimonion;
- parallel scheduler;
- complete meta-layer engine;
- sophisticated UI.

## Phase 1 additions

- mega-graph constructor;
- local revision propagation;
- scene reconstruction.

## Phase 2 additions

- mismatch engine;
- OPEN-generated REQUIREMENT mechanism;
- exclusion tracking.

## Phase 3 additions

- operation-duality links;
- part–whole constraints;
- rendered substitution support.

## Phase 4 additions

- axis withdrawal switch;
- self-diagnostic probes;
- diagnostic independence paths.

## Phase 5 additions

- candidate lens representation;
- settled/open router;
- LLM escalation interface.

## Phase 6 additions

- structured handoff format;
- agent/process identity;
- merge / disagreement preservation.

---

# 18. Data Requirements

Use domains where ground truth can be established independently.

Preferred first domains:

## OpenPCB
Good for:
- parts;
- traces;
- provenance;
- incomplete knowledge;
- measurements;
- revision.

## AISocket
Good for:
- live traces;
- bounded action;
- external measurements;
- closed-loop validation.

## Everett Portal
Good for:
- branch;
- time;
- version;
- context isolation.

Avoid starting with purely philosophical examples as the first benchmark.

---

# 19. Experimental Logging Requirements

Every run should preserve:

- experiment ID;
- version of field;
- model version;
- prompt / query;
- retrieved cut;
- active relations;
- OPEN state;
- mismatch state;
- Daimonion actions;
- external measurements;
- result;
- cost;
- error;
- REOPEN event.

Raw logs should be kept separately from interpreted conclusions.

---

# 20. Falsification Rules

The experimental program should be considered unsuccessful if repeated testing shows that:

1. routing cost ≈ full LLM cost;
2. OPEN does not reduce unsupported closure;
3. mismatch localization does not reduce search;
4. lens stabilization does not transfer;
5. local revision is effectively global;
6. diagnostic degradation is not internally detectable;
7. provenance overhead dominates benefit;
8. structural handoff does not reduce repeated reconstruction;
9. coordination cost dominates parallel / modular benefit;
10. the field becomes too brittle to maintain.

Any of these should trigger architectural revision rather than rhetorical defense.

---

# 21. Experimental Deliverables

For each completed experiment produce:

1. protocol;
2. raw data;
3. baseline result;
4. Noepedia result;
5. plots / tables;
6. failure cases;
7. interpretation;
8. changed assumptions;
9. new OPENs;
10. code / configuration where publishable.

---

# 22. First Concrete Implementation Task

The first build should be deliberately small:

> **One real object, several relation networks, explicit provenance, one OPEN, one mismatch, one local revision, one task-specific mega-graph, and one baseline LLM comparison.**

If this cannot be made simple, the architecture is still too abstract.

---

# 23. Experimental Success Gate

The project should not claim validated architecture until at least:

- one real end-to-end reconstruction succeeds;
- one OPEN produces a useful measurement;
- one mismatch reduces search;
- one reciprocal reconstruction improves recovery;
- one axis withdrawal is internally detected;
- one explicit lens reduces repeated neural cost;
- one local revision remains local;
- one failure case is published.

---

# 24. Experimental Principle

> **The theory earns the right to survive only by making the experiment simpler, cheaper, or more informative.**

If lower-level work remains difficult for reasons the theory cannot expose, the theory must REOPEN.



---

# 25. Experiment A — Detailed Protocol

## 25.1 Name

**End-to-End Relational Reconstruction on One Real Object**

## 25.2 Purpose

The first experiment is deliberately minimal.

It is not meant to prove the whole Noepedia architecture.

It asks one narrow question:

> **Can one real object be represented as several explicit relational cuts, reconstructed into a task-specific scene, revised locally, and compared against an LLM-only baseline without forcing the whole context through repeated neural inference?**

The experiment succeeds only if the explicit structure creates measurable operational leverage.

---

## 25.3 Conceptual Briefing Requirement

**No experimental run may begin before a short conceptual briefing.**

The briefing must establish:

1. what exactly the experiment is testing;
2. which part of the theory is under test;
3. what is *not* being tested;
4. what the expected observable consequence is;
5. what result would count as failure;
6. which variables are intentionally controlled;
7. which result would force a theoretical REOPEN;
8. which measurements must be logged before interpretation begins.

The briefing should be written and frozen before the run.

This prevents the theory from being retrofitted to the result.

---

## 25.4 Object Selection

Choose **one real object** with enough structure to support several independent relation networks, but small enough to understand completely.

Preferred first domain:

**OpenPCB hardware object**

Candidate examples:
- one PCB;
- one known subcircuit;
- one connector region;
- one power section;
- one sensor board.

The object should have at least:

- visible physical structure;
- at least one measured property;
- at least one part–whole relation;
- at least one causal or functional relation;
- provenance for at least part of the evidence;
- one deliberately unresolved relation.

---

## 25.5 Required Relation Networks

The first object should be represented through a minimum of four networks:

### A. Part–Whole

Example:

~~~text
COMPONENT_A → PART_OF → BOARD_X
~~~

### B. Functional

~~~text
COMPONENT_A → SUPPORTS_FUNCTION → POWER_CONVERSION
~~~

### C. Evidence / Provenance

~~~text
CLAIM_17 → SUPPORTED_BY → MEASUREMENT_4
MEASUREMENT_4 → PRODUCED_BY → INSTRUMENT_2
~~~

### D. Spatial / Connectivity

~~~text
PAD_A → CONNECTED_TO → TRACE_B
~~~

Optional fifth network:

### E. Causal / Operational

~~~text
INPUT_VOLTAGE → ENABLES → REGULATOR_STAGE
~~~

---

## 25.6 Required OPEN

At least one relation must be left explicitly unresolved.

Example:

~~~text
COMPONENT_X → FUNCTION? → OPEN
~~~

or:

~~~text
TRACE_Y → CONNECTS_TO? → OPEN_SPACE
~~~

The OPEN must be genuine enough that the experiment can later ask whether the system generates a useful next requirement.

---

## 25.7 Required Mismatch

After the healthy representation is built, introduce one controlled mismatch.

Examples:

- wrong component identity;
- wrong connectivity;
- wrong functional label;
- wrong part–whole placement;
- wrong provenance link.

The mismatch must be known to the experiment designer so that localization accuracy can be measured.

---

## 25.8 Experimental Conditions

### Condition 1 — LLM-only baseline

Provide the model with the same raw evidence in ordinary context.

Ask it to reconstruct the relevant scene and answer the target task.

Record:
- prompt size;
- token use;
- latency;
- answer;
- uncertainty;
- any unsupported assumptions.

### Condition 2 — Retrieval + LLM baseline

Retrieve the relevant raw notes/documents, but do not use explicit Noepedia relations.

Record the same metrics.

### Condition 3 — Noepedia condition

Provide:
- explicit relational field;
- task-specific cut;
- OPEN status;
- provenance;
- local mismatch indicators.

Use an LLM only if the remaining task crosses an OPEN boundary.

Record:
- size of retrieved cut;
- number of relations traversed;
- number of LLM calls;
- token use;
- latency;
- result;
- revision path.

---

## 25.9 Target Task

The first task should not be broad.

Use one concrete question such as:

> **Reconstruct the relevant functional scene around COMPONENT_X and identify which relation must be checked next to determine whether the current interpretation is valid.**

The task must require:
- more than one relation network;
- at least one provenance path;
- one unresolved edge;
- enough context that a flat text answer is not trivial.

---

## 25.10 Local Revision Test

After the first reconstruction:

1. change one known relation;
2. record which dependent structures are affected;
3. update only the actual dependency region;
4. rerun the same target task.

Measure:

- number of changed relations;
- number of unaffected relations touched;
- time to repair;
- whether provenance remains intact.

This tests the claim that explicit structure allows local revision.

---

## 25.11 Metrics

### Correctness

- task answer accuracy;
- reconstruction accuracy;
- correct mismatch localization;
- correct OPEN preservation.

### Epistemic quality

- unsupported closure count;
- provenance coverage;
- number of assumptions added without support;
- number of competing interpretations preserved.

### Computational cost

- tokens;
- LLM calls;
- context size;
- wall-clock time;
- traversal operations.

### Structural cost

- relations loaded;
- relations changed during revision;
- affected dependency radius;
- coordination overhead.

---

## 25.12 Success Criteria

The experiment counts as a meaningful positive result only if the Noepedia condition provides at least one measurable benefit while preserving or improving correctness.

Acceptable benefits include:

- lower context size;
- fewer LLM tokens;
- fewer LLM calls;
- better provenance;
- fewer unsupported closures;
- more local revision;
- better mismatch localization.

A visually impressive demo without one of these is not enough.

---

## 25.13 Failure Criteria

The experiment fails if:

- explicit relations add no useful information;
- the mega-graph misses the task-relevant structure;
- the LLM-only baseline is simpler and equally auditable;
- local revision becomes effectively global;
- OPEN is ignored or prematurely closed;
- provenance overhead dominates the task;
- mismatch localization does not outperform naive inspection.

Failure is a useful result.

---

## 25.14 REOPEN Triggers

A theoretical REOPEN is required if:

### Trigger A
The field representation cannot express the real object without repeated ad hoc exceptions.

### Trigger B
The task-specific cut repeatedly omits essential relations.

### Trigger C
OPEN does not produce a meaningful distinction from ordinary missing data.

### Trigger D
Local revision propagates too broadly.

### Trigger E
The explicit structure does not reduce repeated LLM work.

Each trigger points to a different theoretical layer and should not be collapsed into a generic "implementation problem".

---

## 25.15 Required Artifacts

Before the experiment is considered complete, preserve:

1. object description;
2. relation tables;
3. provenance records;
4. OPEN definition;
5. injected mismatch;
6. frozen conceptual briefing;
7. baseline prompts;
8. Noepedia task cut;
9. raw logs;
10. metrics table;
11. failure notes;
12. final interpretation;
13. any theory changes caused by the result.

---

## 25.16 Recommended Run Sequence

~~~text
choose object
→ freeze raw evidence
→ define relation networks
→ define genuine OPEN
→ write conceptual briefing
→ run LLM-only baseline
→ run retrieval+LLM baseline
→ run Noepedia condition
→ inject controlled mismatch
→ rerun all conditions
→ perform local revision test
→ compare metrics
→ identify REOPEN if needed
~~~

---

## 25.17 Pre-Run Rule

Immediately before the actual experiment, hold a short conceptual briefing answering only these questions:

1. **What are we testing today?**
2. **What result do we expect if the mechanism is real?**
3. **What result would falsify or weaken the mechanism?**
4. **What must remain fixed during the run?**
5. **What are we forbidden to reinterpret after seeing the result?**

Only after those five answers are frozen should the experiment start.


# Anti-drift experimental gate

Before any new experiment is implemented, it must state which canonical role is under test: FIELD, LLM ADAPTER, DAIMONION, or DETERMINISTIC ALGORITHM. It must also state the minimum knowledge package required. If the experiment changes the role definitions, turns the Daimonion into a fact author, or expands a local subsystem into a new core layer, the run must stop and explicitly REOPEN CURRENT_ARCHITECTURE.md before code is written.
