# Experiment 013 — Label-Blind Baseline-Transition Test for COLD Episodes

> **Status:** preregistered real-data follow-up to Experiment 012.

## Motivation

Experiment 012 found that 19 of 20 outside-only episodes were classified COLD.

The next question is:

> **Do these COLD episodes resemble persistent downward level changes, or transient excursions that return toward the previous baseline?**

Experiment 013 does not change the Experiment 011 detector and does not change the Experiment 012 episode decomposition.

## Label-blind analysis boundary

Before NAB labels are loaded, the analyzer receives:

- the pinned real temperature trace;
- Experiment 012 episode boundaries;
- no anomaly-window information.

For every episode it computes local level descriptors from the raw trace.

Only after `TRANSITIONS.json` is written are NAB labels loaded.

## Frozen local windows

Sampling interval is approximately five minutes.

Use:

~~~text
PRE window  = 12 raw samples immediately before episode start
POST window = 12 raw samples immediately after episode end
~~~

This corresponds to approximately one hour before and one hour after.

Episodes without a full PRE or POST window are marked `INSUFFICIENT_CONTEXT`.

## Frozen robust scale

For the PRE window:

~~~text
pre_median = median(PRE)
pre_mad = median(abs(x - pre_median))
pre_scale = max(1.4826 * pre_mad, 1e-6)
~~~

Also compute:

~~~text
episode_raw_median
post_median
post_shift_z = (post_median - pre_median) / pre_scale
episode_shift_z = (episode_raw_median - pre_median) / pre_scale
~~~

## Frozen structural classification

For episodes whose Experiment 012 sign class is COLD:

### DOWNWARD_LEVEL_SHIFT

~~~text
post_shift_z <= -2.0
~~~

### RECOVERED_COLD_EXCURSION

~~~text
episode_shift_z <= -2.0
AND
abs(post_shift_z) < 1.0
~~~

### OTHER_COLD

all other COLD episodes.

For non-COLD episodes:

~~~text
NOT_COLD
~~~

These are descriptive structural classes only.

## External evaluation

After transition classes are frozen, load NAB labels and restrict the scientific test to outside-only COLD episodes.

Report:

- outside-only COLD episode count;
- DOWNWARD_LEVEL_SHIFT count;
- RECOVERED_COLD_EXCURSION count;
- OTHER_COLD count;
- fraction of outside-only COLD episodes classified DOWNWARD_LEVEL_SHIFT;
- mismatch-point fraction contained in DOWNWARD_LEVEL_SHIFT episodes;
- median post_shift_z among outside-only COLD episodes;
- median episode_shift_z among outside-only COLD episodes.

## Preregistered scientific gate

A positive structural result requires:

~~~text
downward_level_shift_episode_fraction >= 0.50
AND
downward_level_shift_point_fraction >= 0.50
~~~

Interpretation of PASS:

> most outside-only COLD episodes, and most mismatch points inside them, are associated with a post-episode level that remains robustly below the pre-episode baseline.

This does not establish that the regime change is faulty or anomalous.

## Forbidden reinterpretation

If the gate fails, do not change:

- PRE/POST window length;
- z thresholds;
- Experiment 011 detector;
- Experiment 012 episode gap.

Any changed analysis becomes a new experiment.

## OPEN produced by the experiment

If persistent downward shifts dominate, the next OPEN is:

> **Is the detector flagging genuine operating-regime transitions rather than point anomalies, and what contextual variable would distinguish normal from abnormal transitions?**

If recovered excursions dominate, the next OPEN is:

> **What mechanism produces transient cold departures without baseline relocation?**
