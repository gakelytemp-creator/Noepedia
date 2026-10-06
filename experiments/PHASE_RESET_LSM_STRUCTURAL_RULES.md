# Experimental Phase Reset — LSM Structural Rules Before Daimonion Architecture

> **Status:** NEW EXPERIMENTAL DIRECTION
> **Date:** 2026-10-06

## Why the direction changes

Experiments 001–073 are preserved as an honest research record. They produced useful instrumentation, null controls, revision machinery, transfer tests, failures, and local mechanisms.

However, they were not sufficiently well aimed at the deepest conceptual layer of Noepedia. In retrospect, much of the sequence tried to discover, train, or validate Daimonion behavior before the structural requirements of the LSM field itself had been made explicit enough.

The new dependency is:

~~~text
LSM structural requirements
→ invariants and obligations
→ allowed transformations
→ Daimonion architecture
→ implementation
→ experiment
~~~

The old sequence must therefore not be read as validation of the present LSM philosophy. It is an exploratory phase that revealed a missing prerequisite.

## No protected philosophy

The present structural ideas are hypotheses, not doctrine. If they fail, they must be replaced. If the replacement fails, it must be replaced again.

> **We will change the philosophy as many times as necessary until we find structural rules that produce real, reproducible operational intelligence.**

A failed philosophy is useful if its failure reveals what must change. The project fails only if it protects its vocabulary from experiment.

## Current starting picture

1. The LSM contains addressable objects.
2. Predicates are also addressable objects, not a privileged second species.
3. A predicate object may itself be subject or object in another relation network.
4. Names remain attached to objects, but identity is not defined by the name string.
5. Therefore same name does not guarantee same object, and different name does not guarantee different object.
6. Predicates themselves can be hierarchized, decomposed, compared, and related.
7. A fundamental object or predicate means only: at the current resolution, no accepted lower decomposition is available. It is not a metaphysical claim of indivisibility.

## Antipredicate structure as a candidate field law

When a predicate object appears, the field may require an explicit antipredicate counterpart and an explicit relation recording which predicate it opposes.

~~~text
PREDICATE_P
    ↕ ANTIPREDICATE_RELATION
PREDICATE_NOT_P
~~~

The antipredicate is an ordinary object in the field.

Candidate lifecycle rule:

- if an antipredicate object loses its antipredicate relation and has no participation in any other relation network, it becomes structurally orphaned and may be removed;
- if an active predicate exists but lacks a required antipredicate relation, the missing counterpart becomes a structural requirement and may be generated again.

This suggests a candidate principle: a structurally required position may be more persistent than the particular object occupying it. This is not yet accepted as a law; it must be tested.

## DREAM — internal restructuring without new external facts

For now, DREAM names internal work in which no new external fact is introduced. Existing structure is re-run through a newly available distinction, relation, or constraint.

Example:

~~~text
new distinction appears
→ antipredicate side is created or linked
→ old relations are revisited
→ contradictions become visible
→ unresolved positions remain OPEN
→ possible finer distinctions appear
~~~

DREAM must not fabricate external evidence. Its question is whether new organization can be extracted from already stored structure.

## Daimonion identity may be irrelevant

If a Daimonion only executes field rules, individual worker identity may carry no epistemic importance. Many indistinguishable workers may operate on the same field. Provenance may need to preserve the source, measurement, or explicit procedure result without preserving which interchangeable Daimonion performed housekeeping.

This creates a possible path to parallelism, but it must be tested rather than assumed.

## New experimental unit: one rule at a time

The next experiments should be tiny. Do not begin by asking whether Noepedia works. Ask:

> **What new intellectual capability appears when one structural rule is added?**

For each rule compare the same field with the rule OFF and ON.

~~~text
RULE
→ STRUCTURAL CHANGE
→ NEW CAPABILITY?
→ COST?
→ FAILURE MODE?
→ KEEP / MODIFY / REJECT / REOPEN
~~~

Initial candidate map:

| Candidate rule | Candidate capability to test |
|---|---|
| Object identity separated from name | synonym, multilingual, and homonym stability |
| Predicates are objects | relations about relations; predicate hierarchy |
| Predicate hierarchy | decomposition and reuse of relation structure |
| Provisional fundamental status | increasing resolution without pretending past resolution was final |
| Explicit antipredicate relation | forced examination of the opposing structural side |
| Antipredicate lifecycle/regeneration | structural self-repair |
| Orphan-object removal | self-cleaning |
| OPEN instead of forced closure | localized ignorance without fabrication |
| DREAM after a new distinction | internal restructuring without new external facts |
| Interchangeable Daimonion workers | parallel structural maintenance without author identity |

## Minimal experimental style

Prefer small synthetic worlds first: roughly 10–30 objects, a handful of predicates and relation networks, one ambiguity, one contradiction, one missing counterpart, and one new distinction introduced after the initial field is built.

Every rule should be ablated against the same field without that rule. Measure what becomes distinguishable, which contradictions appear, which OPENs appear, what unsupported closures disappear, what extra cost is introduced, and whether pathological loops or useless expansion occur.

## Reinterpretation of Experiments 001–073

The old experiments remain valuable as:

1. historical exploratory evidence;
2. instrumentation and audit methods;
3. local mechanisms and failure modes;
4. evidence that algorithmic activity can look meaningful while being conceptually mis-aimed;
5. a warning against expanding one successful subsystem into the definition of the whole project.

They are not sufficient evidence for the new LSM philosophy. Some may later be reused as lower-level instruments. No result should be retroactively rewritten to pretend that an old experiment tested concepts that had not yet been formulated.

## Working commitment

> **Structure first. Operator second.**
>
> **Rule first. Capability second. Measurement third.**
>
> **No protected philosophy.**
>
> **If the current picture fails, replace it. If the replacement fails, replace it again. Continue until the surviving structure earns its place experimentally.**
