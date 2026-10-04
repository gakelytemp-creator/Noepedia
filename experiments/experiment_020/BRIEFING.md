# Experiment 020 — Third Independent Real Relation Resolves the Shape of Core-Derived Disagreement

> **Status:** preregistered real-data core experiment.

## Motivation

Experiment 019 produced 1,165 core-derived disagreements between two independent real-data paths:

~~~text
Path A: DV_eletric
Path B: Motor_current
~~~

Neither input path asserted `MISMATCH`; the Noepedia rule created that distinction.

Experiment 020 asks the next question:

> **When A and B disagree, does a third independent real-data relation systematically support one side or the other?**

This experiment does not yet call either class `normal transition lag` or `fault`.

## Third independent path

Path C uses `TP2`, a compressor-discharge pressure channel.

Published dataset semantics describe TP2 as approximately zero when the unit is not loaded.

Path C is constructed without reading `DV_eletric` or `Motor_current`.

## Frozen path construction

### Path A — digital outlet-valve state

~~~text
DV_eletric = 1 → STATE_LOADED
DV_eletric = 0 → STATE_NOT_LOADED
~~~

### Path B — Motor_current state

Use first 50,000 rows and deterministic 1-D k-means (`k=2`).

~~~text
low centroid  → STATE_NOT_LOADED
high centroid → STATE_LOADED
threshold = midpoint
~~~

### Path C — TP2 pressure state

Use the same first 50,000 rows, but fit independently to TP2 only.

~~~text
low centroid  → STATE_NOT_LOADED
high centroid → STATE_LOADED
threshold = midpoint
~~~

Path C may not read Path A or Path B during calibration or classification.

## Evaluation cut

Use rows 50,001–55,000 exactly, as in Experiment 019.

For each assessment store three candidate-state relations:

~~~text
ASSESSMENT_i → DIGITAL_CANDIDATE_STATE  → STATE_*
ASSESSMENT_i → CURRENT_CANDIDATE_STATE  → STATE_*
ASSESSMENT_i → PRESSURE_CANDIDATE_STATE → STATE_*
~~~

No input path may assert verdict words such as mismatch, consistent, agreement, support, normal, anomaly, or fault.

## Explicit rules

The field contains three generic equality constraints:

~~~text
RULE_AB: DIGITAL_CANDIDATE_STATE  vs CURRENT_CANDIDATE_STATE
RULE_AC: DIGITAL_CANDIDATE_STATE  vs PRESSURE_CANDIDATE_STATE
RULE_BC: CURRENT_CANDIDATE_STATE  vs PRESSURE_CANDIDATE_STATE
~~~

Each uses the existing one-input evaluator grammar:

~~~text
RULE_SCOPE
INPUT_PREDICATE
REQUIRED_PREDICATE
TARGET_CONSTRAINT = SAME_NET
~~~

## Frozen mismatch-shape classification

After the evaluator produces its events, consider only assessments where Rule AB emits `FORMAL_MISMATCH`.

Because all three paths are binary, Path C must equal either A or B on each AB disagreement.

Classify from evaluator events only:

~~~text
PRESSURE_SUPPORTS_DIGITAL_SIDE
    Rule AB = mismatch
    Rule AC = consistent
    Rule BC = mismatch

PRESSURE_SUPPORTS_CURRENT_SIDE
    Rule AB = mismatch
    Rule AC = mismatch
    Rule BC = consistent
~~~

Any other event pattern on an AB disagreement is a structural failure.

## Frozen evaluability gate

The experiment is evaluable only if:

- exactly 5,000 assessments are built;
- all three paths each produce both states at least once;
- both analog calibration centroid pairs are distinct;
- Rule AB produces at least one mismatch;
- no input relation contains a verdict/classification token.

## Frozen architectural success gate

PASS requires:

~~~text
every assessment receives exactly one event from each of RULE_AB, RULE_AC, RULE_BC
every RULE_AB mismatch falls into exactly one of the two frozen third-path support classes
both support classes occur at least once
all OPEN records remain unchanged
~~~

No minimum class fraction is preregistered.

## OPEN structure

The field carries:

~~~text
OPEN_020_INTERPRETATION:
THIRD_PATH_SUPPORT_CLASS → PHYSICAL_INTERPRETATION → UNKNOWN
~~~

The experiment must not close it.

## Claim boundary

A PASS supports only:

> **A third independently constructed real relation can refine a core-derived two-path disagreement into reproducible structural subclasses without either input stream directly asserting those subclasses.**

It does not establish that either subclass is normal, faulty, causal, or anomalous.