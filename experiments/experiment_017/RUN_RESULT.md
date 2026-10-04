# Experiment 017 — Verified Held-Out Replication Result

> **Status:** repository CI reproduction passed.
>
> **Primary scientific result:** FAIL.
>
> **Secondary structural result:** NOT_EVALUABLE.

## CI record

~~~text
workflow: Noepedia Experiment Verification
run id: 37176950102
job: verify
conclusion: success
head commit: 3669971509f4e9e00c4ef093df183e41478f9bef
~~~

## Held-out source

~~~text
NAB
realKnownCause/ambient_temperature_system_failure.csv
~~~

The file was selected from NAB directory/file metadata before its values or anomaly-window entry were inspected for Experiment 017.

## Frozen primary detector

Experiment 011 detector reused unchanged:

~~~text
trailing window = 288 samples
robust scale = 1.4826 × MAD
FORMAL_MISMATCH when robust_z >= 6.0
~~~

## Observed detector result

~~~text
scored samples N                  6979
scored samples inside windows K   726

detector mismatches n                0
mismatches inside windows X          0
observed precision                 0.0

null mean precision             0.1040263648
one-sided null p                        1.0
~~~

Because the detector emitted no mismatch events, there is no detector enrichment above chance.

Therefore:

~~~text
PRIMARY SCIENTIFIC RESULT = FAIL
~~~

## Secondary frozen-pipeline result

The frozen downstream sequence was attempted:

~~~text
Experiment 011 detector
→ Experiment 012 episode decomposition
→ Experiment 013 transition descriptors
→ Experiment 014 clusterer
~~~

Observed:

~~~text
mismatches          0
episodes            0
transition records  0
~~~

The unchanged Experiment 014 clusterer cannot form two clusters from an empty eligible set and raised an empty-data error.

The Experiment 017 runner treated this as a scientific/structural non-evaluability condition rather than a CI infrastructure failure.

Therefore:

~~~text
SECONDARY STRUCTURAL RESULT = NOT_EVALUABLE
~~~

## Interpretation

The development-series detector did **not** transfer to this held-out NAB series under the frozen parameters.

This is stronger evidence than another development-series feature analysis would have been.

The result directly limits the earlier real-data claims:

> the Experiment 011 detector was useful on the original machine-temperature development series, but its fixed threshold/window combination is not a generally transferable anomaly detector across NAB real-known-cause series.

The result also blocks replication of the Experiment 012–014 cascade on this held-out series because the first stage produced no events.

## Null-baseline lesson

Experiment 017 confirms why the null baseline belongs in the protocol.

On the held-out file:

~~~text
null mean precision ≈ 0.104
~~~

but the frozen detector produced no candidate points at all.

No recall-style window gate can rescue this result.

## Audit rule

Do **not** now:

- lower the robust-z threshold;
- change the trailing window;
- choose another held-out file and call it the same replication;
- alter the episode or cluster rules.

Doing so would convert the held-out test into another development cycle.

The failed replication is preserved as the result.

## Consequence for project direction

The correct next step is not Experiment 018 as another anomaly-detector tweak.

The real-data instrumentation track has done its job:

~~~text
development signal found
→ adaptive structure explored
→ held-out transfer tested
→ transfer failed
~~~

The next high-value step is to return to the Noepedia relational core and use real observations as explicit field objects/relations with provenance and OPEN structure.
