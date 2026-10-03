# Experiments 001–009 — State of Evidence

> **Purpose:** consolidate what the current experiment series supports, what each step added, and what remains unvalidated.

This document is not a replacement for the individual experiment folders. It is an index of claims, evidence, and limits.

## Evidence ladder

| Experiment | Added capability / observation | What the result supports | Main limitation |
|---|---|---|---|
| 001 | LLM identifies a candidate relation mismatch and exposes missing structure | Structured fields can make hidden ontology/rule gaps visible | Synthetic; LLM-mediated; mismatch was not formally provable because granularity and predicate-bridge semantics were missing |
| 002 | Terminal granularity + explicit consistency rule | An explicit relation plus explicit rule can make mismatch formally derivable | Repair selection remained underdetermined; revision precedence became a new OPEN |
| 003 | Deterministic evaluator | Formal mismatch detection can be executed without LLM/domain knowledge | Narrow one-input rule grammar |
| 004 | Multiple rule objects and object types | One generic rule grammar can be reused across multiple field regions | Still one structural rule form |
| 005 | Two-input same-subject antecedent | A requirement can depend on a matched relational pattern rather than one edge | Join form remains narrow: same subject + SAME_OBJECT |
| 006 | Cross-subject shared-object join | A required relation between different subjects can be derived from explicit topology | Still a fixed cross-subject pattern; no recursive derivation |
| 007 | Derived relation consumed by a later rule | Temporary derived working relations can become inputs to later deterministic evaluation | One derivation stage followed by checking |
| 008 | Multi-round fixpoint closure | Derived relations can activate further derivation rules in later rounds | No branch competition |
| 009 | Branching + explicit competition | Multiple justified derived branches can coexist and competition can be exposed without forced winner selection | No evidence-driven discrimination between branches yet |

## Current executable core

The deterministic path demonstrated by Experiments 003–009 is:

~~~text
stored relations
+ explicit rule objects
        ↓
pattern matching
        ↓
derived working relations
        ↓
recursive / multi-round derivation
        ↓
branching
        ↓
explicit competition detection
        ↓
NO automatic winner selection
~~~

Derived working relations are not written back into the frozen input field.

OPEN records remain read-only in these experiments.

## What is supported now

The present evidence supports these limited claims:

1. Explicit rule semantics can move mismatch detection from interpretive LLM judgment into deterministic execution.
2. The same evaluator can apply rules described in field data rather than electronics-specific code branches.
3. Small relational patterns can be matched across one or multiple subjects.
4. Derived relations can participate in later inference rounds.
5. Competing derived branches can remain simultaneously represented.
6. Competition can be exposed as an event without forcing repair, deletion, or winner selection.
7. The executable sequence is independently checked by repository verifiers and GitHub Actions for Experiments 004–009.

## What is not supported yet

The series does **not** yet establish:

- a general-purpose rule language;
- arbitrary graph inference;
- probabilistic reasoning;
- negation / absence semantics;
- repair governance;
- evidence weighting;
- provenance weighting;
- branch ranking;
- trustworthy automatic branch selection;
- scalable task-specific cuts;
- local revision propagation at realistic scale;
- computational advantage over LLM-only baselines;
- real-world architecture validation.

Most importantly, Experiments 001–009 are still synthetic controlled fixtures.

## Audit lessons

Two failures are intentionally preserved in the history:

- Experiment 006 exposed a dispatcher bug and records it in `experiment_006/CORRECTION.md`.
- Experiment 007 first failed CI because the frozen expected-output contract omitted derived-input provenance; the correction is preserved in `experiment_007/CORRECTION.md`.

These are part of the evidence trail, not noise to be erased.

## Next gate

The next synthetic step should not add a longer chain merely for complexity.

The next question is:

> **Can new explicit discriminating evidence reduce a preserved branch competition without deleting history or selecting a winner by hidden policy?**

That is the purpose of Experiment 010.

After that, the program should move toward a real-object experiment rather than indefinitely expanding synthetic grammar.
