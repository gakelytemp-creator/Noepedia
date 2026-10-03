# Experiment 010 — Evidence-Driven Branch Discrimination

> **Status:** preregistered executable experiment.

## Purpose

Experiment 009 preserved competing candidate branches without forcing a winner.

Experiment 010 asks the next question:

> **Can new explicit discriminating evidence reduce a preserved branch competition while keeping the original candidate history intact?**

The experiment must distinguish evidence-driven compatibility from hidden winner selection.

## Structure

First, two independent derivation paths create candidate branches:

~~~text
L --CANDIDATE--> A
L --CANDIDATE--> B
~~~

Then new explicit observation and candidate-feature relations are introduced:

~~~text
L --OBSERVED_FEATURE--> E1
A --HAS_FEATURE-------> E1
B --HAS_FEATURE-------> E2
~~~

An explicit evidence-filter rule may derive:

~~~text
L --SUPPORTED_CANDIDATE--> A
~~~

and mark B as incompatible with the observed evidence.

The original CANDIDATE relations must remain present.

## Two controlled cases

### L1 — discriminating evidence

~~~text
L1 candidates: A1, B1
observed: RED
A1 feature: RED
B1 feature: BLUE
~~~

Expected:
- original candidate competition remains historically represented;
- A1 becomes SUPPORTED_CANDIDATE;
- B1 receives CANDIDATE_REJECTED_BY_EVIDENCE;
- supported-candidate cardinality becomes UNIQUE_CANDIDATE.

### L2 — non-discriminating evidence

~~~text
L2 candidates: A2, B2
observed: GREEN
A2 feature: GREEN
B2 feature: GREEN
~~~

Expected:
- both A2 and B2 become SUPPORTED_CANDIDATE;
- supported-candidate competition remains unresolved.

## Epistemic boundary

Experiment 010 does **not** authorize deletion or winner selection.

It only allows explicit evidence to produce compatibility/incompatibility structure.

~~~text
candidate generation
≠
evidence compatibility
≠
winner selection
~~~

A supported candidate is not automatically written back as settled truth.

## Scientific requirement

The evaluator must not contain fixture-specific logic for L1/L2, A1/B1/A2/B2, RED/BLUE/GREEN, or the predicates used by this fixture.

The result must arise only from explicit rule fields and stored/derived relations.

OPEN_01 must remain unchanged.
