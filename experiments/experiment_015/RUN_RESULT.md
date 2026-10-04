# Experiment 015 — Verified Run Result

> **Status:** repository CI reproduction passed.
>
> **Scientific result:** FAIL under the preregistered temporal-context gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37173453304
job: verify
conclusion: success
head commit: d6c28e06516be50fd2724a82b0b04fc3bf9936cf
~~~

## Pipeline

~~~text
pinned NAB real sensor trace
→ unchanged Experiment 011 detector
→ unchanged Experiment 012 episode decomposition
→ unchanged Experiment 013 transition descriptors
→ unchanged Experiment 014 clusters
→ label-blind time-of-day relation
→ temporal_context.json
→ only then load NAB labels
→ circular phase evaluation
~~~

## Observed temporal structure

~~~text
outside-only COLD episodes = 19
~~~

### CLUSTER_0

~~~text
episodes                15
resultant length R   0.3521
circular mean start   12:13
~~~

### CLUSTER_1

~~~text
episodes                 4
resultant length R   0.1973
circular mean start   04:16
~~~

Cross-cluster circular mean separation:

~~~text
7.961 hours
~~~

Difference in concentration:

~~~text
R(CLUSTER_1) - R(CLUSTER_0)
= -0.1548
~~~

## Preregistered gate

~~~text
CLUSTER_1 resultant_length >= 0.70
phase_separation_hours >= 2.0
CLUSTER_1 resultant_length - CLUSTER_0 resultant_length >= 0.20
~~~

Observed:

~~~text
0.1973 < 0.70
7.961  >= 2.0
-0.1548 < 0.20
~~~

Therefore:

~~~text
scientific_result = FAIL
~~~

## Interpretation

The two families have circular mean start times separated by nearly eight hours, but the long/deep family is **not concentrated** at one daily phase.

With only four outside-only CLUSTER_1 episodes, their resultant length is low:

~~~text
R = 0.1973
~~~

so it would be incorrect to interpret the 04:16 circular mean as a stable daily schedule.

The preregistered hypothesis:

> **the long/deep family is strongly concentrated in a distinct time-of-day phase**

is not supported.

## What this failure removes

Experiment 015 weakens a simple explanation:

~~~text
long/deep COLD family
≈ one recurring clock-time event
~~~

At least under the current data and frozen circular test, that explanation is not justified.

## New OPEN

Experiment 014 established structural separation, while Experiment 015 shows that simple time-of-day phase does not explain it.

The next OPEN is therefore narrower:

> **Which non-clock contextual relation distinguishes the long/deep persistent family from the short/recovering family?**

Possible relations are not yet evidence:

- local rate of change before episode onset;
- duration of the preceding stable regime;
- recovery slope;
- recurrence relative to earlier similar states;
- an external operational/ambient variable absent from this single-channel dataset.

Any one of these must be preregistered before testing.
