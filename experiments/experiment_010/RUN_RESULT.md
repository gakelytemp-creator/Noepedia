# Experiment 010 — Verified Run Result

> **Status:** repository CI verification passed.

GitHub Actions run:

~~~text
workflow: Noepedia Experiment Verification
run id: 37160896132
job: verify
conclusion: success
head commit: 0c431f14f5e14935cfc3bc8898a139881e507289
~~~

## Structural result

The frozen Experiment 010 fixture verified the following:

~~~text
L1:
CANDIDATE → A1
CANDIDATE → B1
OBSERVED_FEATURE → RED

A1 HAS_FEATURE RED
B1 HAS_FEATURE BLUE

→ A1 SUPPORTED_CANDIDATE
→ B1 CANDIDATE_REJECTED_BY_EVIDENCE
→ supported set becomes UNIQUE_CANDIDATE
~~~

For L2:

~~~text
L2:
CANDIDATE → A2
CANDIDATE → B2
OBSERVED_FEATURE → GREEN

A2 HAS_FEATURE GREEN
B2 HAS_FEATURE GREEN

→ A2 SUPPORTED_CANDIDATE
→ B2 SUPPORTED_CANDIDATE
→ competition remains unresolved
~~~

## Event counts

~~~text
DERIVED_RELATION                 7
CANDIDATE_SUPPORTED_BY_EVIDENCE 3
CANDIDATE_REJECTED_BY_EVIDENCE  1
COMPETING_DERIVATIONS            3
UNIQUE_CANDIDATE                 1
~~~

## Epistemic interpretation

Experiment 010 does not delete losing candidate history and does not install a hidden winner-selection policy.

It demonstrates a narrower mechanism:

~~~text
preserved branches
+ explicit discriminating evidence
+ explicit compatibility rule
→ reduced compatible candidate set
~~~

When evidence is non-discriminating, competition remains open.

OPEN_01 remains unchanged.

## Boundary

This is still a synthetic controlled fixture.

The experiment does not establish:
- probabilistic evidence weighting;
- conflicting evidence arbitration;
- repair governance;
- automatic commitment of a supported candidate as settled truth;
- real-world validation.
