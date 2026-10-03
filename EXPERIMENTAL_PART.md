# Experimental Part — Requirements, Tasks, and Validation Program

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

## 4.2 Minimal Daimonion transaction layer

Must support:
- read;
- stage;
- compare;
- propose;
- validate;
- commit;
- reject;
- reopen.

## 4.3 Mega-graph constructor

Must be able to assemble a task-specific cut.

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

