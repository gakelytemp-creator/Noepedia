# Experiment 011 — Real Sensor Trace

This is the first Noepedia experiment in this sequence that uses an external real sensor trace rather than a synthetic fixture.

Source: Numenta Anomaly Benchmark (NAB), pinned in `SOURCE.json`.

## Run

~~~bash
python experiments/experiment_011/run_experiment.py
~~~

The runner:

1. downloads and hash-verifies the pinned CSV;
2. runs the label-blind detector;
3. only then downloads and verifies NAB labels;
4. evaluates predictions against anomaly windows;
5. prints a reproducibility status and a separate scientific PASS/FAIL.

## Important distinction

~~~text
CI / reproducibility PASS
≠
scientific success PASS
~~~

The scientific gate is frozen in `BRIEFING.md`.

If the detector misses the gate, Experiment 011 remains a valid failed real-data experiment. Parameters are not retuned in place.
