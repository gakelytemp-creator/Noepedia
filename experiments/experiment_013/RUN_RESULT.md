# Experiment 013 — Verified Run Result

> **Status:** repository CI reproduction passed.
>
> **Scientific result:** FAIL under the preregistered gate.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37162908404
job: verify
conclusion: success
head commit: 9360960ed821a2516b6c6f7de54d84240d3a2446
~~~

## Pipeline

~~~text
pinned NAB real sensor trace
→ unchanged Experiment 011 detector
→ unchanged Experiment 012 episode decomposition
→ label-blind PRE/POST baseline transition analysis
→ transitions.json
→ only then load NAB labels
→ evaluate outside-only COLD episodes
~~~

## Frozen transition rule

~~~text
PRE window  = 12 raw samples
POST window = 12 raw samples

DOWNWARD_LEVEL_SHIFT
    post_shift_z <= -2.0

RECOVERED_COLD_EXCURSION
    episode_shift_z <= -2.0
    and abs(post_shift_z) < 1.0

OTHER_COLD
    otherwise
~~~

## Observed result

~~~text
outside-only COLD episodes                 19

DOWNWARD_LEVEL_SHIFT                        9
RECOVERED_COLD_EXCURSION                    2
OTHER_COLD                                  8

downward-level-shift episode fraction     0.4736842105

outside-only COLD mismatch points          480
points in DOWNWARD_LEVEL_SHIFT episodes    318
downward-level-shift point fraction       0.6625

median post_shift_z                      -1.4531936555
median episode_shift_z                   -3.1683675326
~~~

## Preregistered gate

~~~text
downward_level_shift_episode_fraction >= 0.50
AND
downward_level_shift_point_fraction >= 0.50
~~~

Observed:

~~~text
0.4736842105 < 0.50
0.6625       >= 0.50
~~~

Therefore:

~~~text
scientific_result = FAIL
~~~

## Interpretation

The preregistered hypothesis that persistent downward baseline relocation dominates the outside-only COLD structure is **not supported**.

The result is close in episode count but still fails the frozen gate and must remain a failure.

At the same time, the point-weighted result is asymmetric:

- only 9 of 19 outside-only COLD episodes satisfy the strict downward-level-shift definition;
- those 9 episodes contain 318 of 480 mismatch points, or 66.25%.

This means the longer or denser COLD episodes are disproportionately represented among the downward-shift class, while many shorter episodes fall into OTHER_COLD or recovered-excursion categories.

## New OPEN

The failed binary hypothesis exposes a better question:

> **Are there at least two structurally distinct families of outside-only COLD episodes: long/dense downward regime shifts and shorter non-persistent excursions?**

Experiment 013 does not answer that question.

## Audit rule

Do not relax the 0.50 episode-fraction gate, change the z thresholds, or redefine the classes inside Experiment 013.

Any clustering, duration-weighting, or alternative regime model must be a new experiment.
