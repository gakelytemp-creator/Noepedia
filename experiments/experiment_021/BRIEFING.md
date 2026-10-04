# Experiment 021 — Explicit Temporal Relation Around Core-Derived Disagreement

> **Status:** preregistered real-data core experiment.

## Starting point

Experiment 020 used three independently constructed real-data paths:

```text
Path A: DV_eletric
Path B: Motor_current
Path C: TP2
```

On the frozen 5,000-row cut:

```text
AB FORMAL_MISMATCH = 1165

among those:
A=C, B differs = 1163
B=C, A differs =    2
```

These are continuity facts from Experiment 020, not new claims in Experiment 021.

## Question

The OPEN carried forward from 020 is refined to:

> Are the 1,163 cases in which DV_eletric and TP2 agree while Motor_current differs concentrated near a DV_eletric state transition, or does a substantial mismatch residue remain in regions far from any such transition?

The experiment is descriptive. It preregisters no expected temporal distribution.

## Why DV_eletric defines the temporal reference

The temporal reference is Path A only.

Using Motor_current to define its own transition proximity would be circular because Motor_current is the path whose disagreement geometry is being tested.

TP2 is retained as the independent third path that identifies the dominant 020 subclass.

Therefore the temporal reference is:

```text
DV_eletric state change between adjacent source rows
```

## Frozen data construction

Calibration rows:

```text
1 .. 50,000
```

Evaluation rows:

```text
50,001 .. 55,000
```

Additional future context:

```text
101 rows after the evaluation cut
```

The future context is read only to determine whether the final evaluation rows lie within 100 rows *before* the next digital transition. It is not evaluated by the three-path rules.

Path construction is unchanged from Experiment 020:

```text
Path A:
DV_eletric = 1 -> STATE_LOADED
DV_eletric = 0 -> STATE_NOT_LOADED

Path B:
first 50,000 Motor_current values
-> deterministic 1-D k-means
-> low cluster STATE_NOT_LOADED
-> high cluster STATE_LOADED

Path C:
first 50,000 TP2 values
-> independent deterministic 1-D k-means
-> low cluster STATE_NOT_LOADED
-> high cluster STATE_LOADED
```

## Explicit temporal relations

For every evaluation assessment, the field stores two raw bounded row-distance relations derived from Path A alone:

```text
ROWS_SINCE_PREVIOUS_DIGITAL_TRANSITION
ROWS_UNTIL_NEXT_DIGITAL_TRANSITION
```

Each distance is an integer in:

```text
0 .. 101
```

where:

```text
0   = the current row itself is a digital transition row
1   = one source row away
...
100 = one hundred rows away
101 = more than one hundred rows away, or no such transition is observed
      in the available frozen history/lookahead
```

No mismatch, support, anomaly, fault, normality, lag, or causal label is inserted into these temporal input relations.

## Core rules

The same three equality rules are used:

```text
AB: DIGITAL_CANDIDATE_STATE vs CURRENT_CANDIDATE_STATE
AC: DIGITAL_CANDIDATE_STATE vs PRESSURE_CANDIDATE_STATE
BC: CURRENT_CANDIDATE_STATE vs PRESSURE_CANDIDATE_STATE
```

The frozen Experiment 003 evaluator remains unchanged.

## Frozen 020 continuity gate

Before temporal analysis, Experiment 021 must reproduce:

```text
AB mismatch total                  = 1165
pressure supports digital subclass = 1163
pressure supports current subclass = 2
```

Failure to reproduce these counts makes the temporal result NOT EVALUABLE.

## Frozen temporal bins

For the 1,163 dominant-subclass assessments only, define:

```text
nearest_distance = min(
    rows_since_previous_digital_transition,
    rows_until_next_digital_transition
)
```

Histogram bins:

```text
0
1
2-5
6-10
11-25
26-50
51-100
>100
```

Three coarse regions are also reported:

```text
NEAR        : nearest_distance <= 10
INTERMEDIATE: 11 <= nearest_distance <= 100
STABLE_FAR  : both bounded distances == 101
```

Direction relative to the nearest digital transition is reported as:

```text
AT_TRANSITION
AFTER_TRANSITION
BEFORE_TRANSITION
EQUIDISTANT
```

These are geometric descriptors only.

## Evaluability gate

The experiment is evaluable only if:

- exactly 5,000 assessments are built;
- Path A, B, and C each contain both candidate states;
- the two analog calibration centroid pairs are distinct;
- every assessment receives exactly one event from AB, AC, and BC;
- the Experiment 020 continuity counts reproduce exactly;
- every assessment has exactly one previous-distance and one next-distance temporal relation;
- all temporal distances are integers in 0..101;
- no input relation asserts a forbidden verdict token;
- all OPEN records remain unchanged.

## Success criterion

Architectural PASS means only:

> The Noepedia experiment can join a previously core-derived disagreement subclass with an independently constructed explicit temporal relation and produce a reproducible temporal geometry without closing the physical interpretation.

There is **no preregistered minimum NEAR fraction**.

Therefore all of the following are legitimate outcomes:

- strong concentration near transitions;
- a mixed distribution;
- predominantly stable-far disagreement.

## Claim boundary

Even a strong near-transition concentration would not by itself establish:

```text
Motor_current is lagging
DV_eletric is truth
TP2 is truth
Motor_current is faulty
the disagreements are normal
the disagreements are anomalies
a causal direction
```

Those remain OPEN unless separately tested.
