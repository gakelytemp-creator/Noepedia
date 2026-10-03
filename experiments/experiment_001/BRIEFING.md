# Experiment 001 — Conceptual Briefing

> **Status:** FROZEN PRE-RUN BRIEFING
>
> This briefing must not be rewritten after observing the result. If the interpretation changes, add a dated post-run note instead.
>
> This first pass is a **dry-run of the experimental machinery**, not yet the publishable real-object Experiment A. The repository does not yet contain a fully documented physical OpenPCB object with ground truth, so the first fixture is an explicitly synthetic low-voltage power-stage example used only to test the JSON field, task-cut logic, OPEN handling, MISMATCH handling, and local revision path.

---

## 1. What are we testing today?

We are testing whether a very small Noepedia-style explicit relational field can:

1. represent one bounded technical object through several distinct relation networks;
2. preserve one genuine unresolved relation as OPEN rather than silently filling it;
3. reconstruct a task-relevant cut without loading the whole fixture;
4. expose a deliberately injected wrong relation as a MISMATCH candidate;
5. revise that relation locally while preserving unrelated relations and provenance.

We are **not** testing the full Noepedia architecture.

---

## 2. Which theoretical mechanisms are under test?

The dry run directly probes:

- addressable objects;
- predicates as addressable relation labels;
- distinct relation networks;
- provenance;
- OPEN;
- task-specific cut / proto-mega-graph;
- MISMATCH localization;
- local revision.

It does **not** yet test:

- autonomous Daimonion intelligence;
- layer birth;
- meta-layer closure;
- lens learning;
- semantic parallelism;
- multi-agent structural handoff;
- real energy savings;
- AGI safety.

---

## 3. Expected observable result if the mechanism is useful

If the mechanism is useful, then for the target task:

- only a small subset of the field should be needed;
- the OPEN should remain unresolved rather than be hallucinated closed;
- the injected wrong relation should be localizable from conflict with explicit evidence;
- correcting it should touch only the dependency region that actually depends on it;
- provenance should remain intact after revision.

---

## 4. What would weaken or falsify this mechanism?

This dry run counts against the current representation if:

- the target task cannot be reconstructed without ad hoc fields outside the model;
- OPEN behaves no differently from a null value;
- the wrong relation cannot be isolated without reading essentially the entire fixture;
- correcting one relation forces broad unrelated rewrites;
- provenance is lost during correction;
- the JSON becomes more complex than the technical object it represents.

---

## 5. What remains fixed during the run?

Frozen before interpretation:

- object set;
- relation-network names;
- raw evidence;
- one OPEN;
- one injected wrong relation;
- target task;
- success / failure criteria.

No new evidence may be added after seeing the result unless the run is explicitly restarted as a new experiment version.

---

## 6. What are we forbidden to reinterpret after seeing the result?

We may not:

- relabel a failure as a success by changing the target task;
- call an unsupported completion "implicit knowledge";
- redefine OPEN after the result;
- hide a global rewrite by calling it local;
- remove the baseline because it performs well;
- claim real-world validation from this synthetic dry run.

---

## 7. REOPEN triggers

REOPEN the theoretical representation if:

1. the same fact must be duplicated across several networks because cross-addressing is insufficient;
2. OPEN cannot participate in a useful task cut;
3. relation status and provenance cannot be represented without schema sprawl;
4. mismatch localization requires a new hidden meta-grammar;
5. local revision cannot be defined from explicit dependencies.

---

## 8. Required logged outputs

For each run preserve:

- fixture version;
- target task;
- selected task cut;
- OPEN state;
- injected mismatch;
- reconstruction result;
- relations traversed;
- revision operations;
- unaffected relations touched;
- provenance before and after;
- interpretation;
- any REOPEN decision.

---

## 9. Dry-run fixture

The fixture is a synthetic low-voltage DC regulator stage:

- input connector;
- regulator IC;
- input capacitor;
- output capacitor;
- output connector;
- VIN / GND / VOUT nets;
- measured input and output voltage;
- one unresolved enable-path relation;
- one deliberately wrong connectivity relation.

This fixture is not evidence for Noepedia. It is a controlled test object for the experimental method.

---

## 10. Frozen question

> **Can the JSON field preserve the difference between known, OPEN, and wrong relations strongly enough that a task-specific reconstruction can expose the wrong relation without silently closing the OPEN, and can the wrong relation then be revised locally?**
