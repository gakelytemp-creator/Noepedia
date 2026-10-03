# Experiment 012 — Verified Run Result

> **Status:** repository CI reproduction passed.
>
> **Scientific result:** PASS under the preregistered structural gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37162405606
job: verify
conclusion: success
head commit: aa20fb777fa9d408351b7b9d15b8d217b5053699
~~~

## Pipeline

~~~text
pinned NAB real sensor trace
→ unchanged Experiment 011 detector
→ 967 mismatch events
→ label-blind temporal episode decomposition
→ 24 episodes
→ only then load NAB anomaly windows
→ structural evaluation
~~~

The episode decomposition was completed before the label file was downloaded.

## Frozen decomposition rule

~~~text
same episode if consecutive mismatch gap <= 30 minutes
persistent outside-only episode if mismatch_count >= 6
~~~

## Observed structural result

~~~text
total mismatches                         967
temporal episodes                         24
NAB anomaly windows                        4

outside-label mismatch points             699
outside-only episodes                      20
isolated outside-only episodes              2
persistent outside-only episodes           14

outside points in persistent outside-only
episodes                                  537

persistent outside fraction             0.7682403433
maximum outside-only episode duration     485 minutes
top-10 outside-episode concentration    0.7210300429
~~~

## Sign structure of outside-only episodes

~~~text
HOT      1
COLD    19
MIXED    0
~~~

The sign classification was created without using anomaly labels.

## Preregistered gate

~~~text
persistent_outside_fraction >= 0.50
max_outside_episode_duration_minutes >= 60
~~~

Observed:

~~~text
persistent_outside_fraction ≈ 0.768
max_outside_episode_duration = 485 minutes
~~~

Therefore:

~~~text
scientific_result = PASS
~~~

## Interpretation

The 699 mismatch points outside NAB anomaly windows are not predominantly isolated detections.

Under the frozen 30-minute episode rule:

- only 2 outside-only episodes are singletons;
- 14 outside-only episodes contain at least 6 mismatch events;
- those persistent outside-only episodes contain 537 mismatch points;
- the longest outside-only episode lasts 485 minutes;
- the ten largest outside-only episodes account for about 72.1% of all outside-label mismatch points.

This supports a narrow structural conclusion:

> **Most unexplained mismatch points are temporally organized rather than scattered independently.**

It does **not** establish that these episodes are unlabeled faults.

## New structural observation

Nineteen of twenty outside-only episodes are classified COLD.

That creates a stronger next OPEN than the generic “false positive or unlabeled anomaly?” question:

> **Why does the frozen local expectation generate predominantly negative-residual outside-label episodes?**

Candidate explanations remain open:

- ordinary downward operating-regime transitions;
- slow baseline adaptation after a level change;
- real unlabeled cold excursions;
- one-sided weakness of the trailing local model;
- another missing contextual variable.

No explanation is selected by Experiment 012.

## Boundary

Experiment 012 does not retune:

- Experiment 011 detector threshold;
- trailing window;
- episode gap;
- persistence threshold.

Any change to those values must become a later experiment.
