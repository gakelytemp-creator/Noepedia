# DIRECTION.md — Noepedia Experimental Direction

Status: ACTIVE DIRECTION CONSTRAINT

This file governs new experiments after Experiment 073 and the 2026-10-06 architectural REOPEN.

## 0. Architectural boundary

Noepedia as a whole is the **LSM (Large Semiotic Model)**. Inside it, the persistent field stores homoiconic semiotic structure; LLM/media adapters handle semantic boundaries; the Socratic Daimonion is an **SLM-type neural network** for learned semiotic logistics; stable repeated operations may be compiled into deterministic services. The revision subsystem is one such service family, not the whole Noepedia core.

Canonical architectural reference: CURRENT_ARCHITECTURE.md. Historical experiment files remain historical evidence and do not override that boundary.
The 2026-10-06 REOPEN changes the active experimental order: **field rules before Daimonion architecture**. The Daimonion description remains provisional until rule-level experiments establish what invariants and operations the field actually requires.


## 1. Architecture freeze

Do not add new architectural layers merely because an experiment fails.

A new architecture experiment is allowed only when a concrete defect prevents a preregistered scientific test from being evaluated correctly.

## 2. New-data rule

If a pipeline is repaired after seeing a result, that repaired version may not be used to reinterpret the same scientific experiment.

The repaired system must be tested on a new, previously untouched dataset or sequence.

Historical results remain historical.

## 3. Null and stop are legitimate outcomes

A result of zero justified promotions, REJECT, REMAIN_OPEN, or NOT_EVALUABLE is not a failure to be rescued.

It is a valid epistemic outcome when produced by the frozen protocol.

## 4. Human hypothesis, Noepedia bookkeeping

The default scientific mode is no longer unrestricted blind pair mining.

A human states one physically meaningful hypothesis.

Noepedia then:
- freezes the hypothesis and protocol;
- separates calibration, discovery, buffer, and confirmation;
- applies null/comparator tests;
- records provenance;
- promotes, rejects, or leaves OPEN;
- preserves all prior versions and corrections.

## 5. No hidden rescue

After outcome inspection, do not change:
- the hypothesis;
- the selected physical variables;
- the dataset/sequence;
- the split;
- preprocessing;
- search range;
- null models;
- success criteria.

Any alternative requires a new experiment number.

## 6. Ten-line stop

Every scientific experiment must end with a short statement answering:

What do we know now that we did not know before this experiment?

If the answer is only “the code works,” the next experiment may not be another architecture-expansion experiment.

## 7. Promotion boundary

No scientific claim is promoted unless it survives:
- untouched confirmation;
- relevant null/comparator gates;
- explicit unresolved handling;
- provenance and history preservation.

Agreement is not truth.
Recurrence is not proof.
A null result is allowed.


## 8. Pre-experiment anti-drift gate

Before implementation begins, every new experiment must answer:

1. Which LSM component is being tested: FIELD, SEMANTIC ADAPTER, SLM-DAIMONION, or DETERMINISTIC SERVICE?
2. What is the smallest sufficient knowledge package for the task?
3. Which outputs may create epistemic result tokens, which are only routing decisions, and how is execution coverage recorded even when there is no result token?
4. What explicit procedure or source contact can justify a stored result?
5. What result is allowed to be OPEN / NO_RESULT / NOT_EVALUABLE?
6. What would count as architecture drift rather than experimental failure?
7. What condition would require reopening CURRENT_ARCHITECTURE.md before any more code is written?

The following are STOP conditions, not invitations to add another layer:

- the experiment needs the Daimonion to invent evidence;
- a local subsystem is being generalized into the whole core;
- the whole field is loaded where a bounded garment would suffice;
- an autonomous specialist is being given unrelated knowledge or capabilities;
- a deterministic service is being treated as a moral or intentional agent;
- repeated failure is being repaired by changing the goal after seeing outcomes.

> **Failure may change the experiment. It may not silently change the project.**


## 9. First post-REOPEN experiment scale

The next experiment is **not Daimonion training**.

First freeze a small capability bench whose tasks are written independently of the structural rules to be tested. It must include at least:

- MATCH;
- MISMATCH;
- CORRECT_OPEN;
- RUN_NO_RESULT;
- NOT_RUN;
- synonym / multilingual identity;
- homonym separation;
- contradiction;
- one case where a candidate rule should help;
- one case where it should have no effect;
- one case where over-application should cause measurable damage.

Then test one candidate LSM rule at a time on the same bench:

~~~text
RULE OFF
vs
RULE ON
→ GAIN / NO_EFFECT / DAMAGE / COST
~~~

No Daimonion-training architecture is justified until this rule-level stage has established which field laws are worth maintaining.

### Attempt registry

Every tried rule or philosophical variant must be recorded, including rejected variants.

For each attempt preserve:

- identifier / version;
- exact change;
- reason for introducing it;
- predeclared expected capability;
- bench version used;
- observed gain;
- observed damage / cost;
- failure reason;
- KEEP / MODIFY / REJECT / REOPEN decision.

The winning rule may not erase the failed search path.
