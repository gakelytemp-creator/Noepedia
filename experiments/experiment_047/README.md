# Experiment 047 — External Transfer to UCI Hydraulic Systems

Experiment 047 tests the Noepedia revision protocol and automated decision/materialization architecture outside MetroPT-3.

External dataset:
UCI Condition Monitoring of Hydraulic Systems (dataset 447).

The dataset contains 2205 repeated 60-second hydraulic test-rig cycles with multi-rate pressure, flow, temperature, power, vibration and virtual-efficiency measurements, plus component-condition labels.

Frozen candidate relation families:
- cooler condition -> CE cycle mean
- valve condition -> PS2 cycle mean
- pump leakage -> SE cycle mean
- accumulator condition -> PS1 cycle mean

Calibration-only family selection is followed by separate discovery and untouched confirmation.

Candidate temporal revision is challenged against majority-state and circular-shift null baselines.

Final decision is passed through the Experiment 045 revision harness and materialized with the Experiment 046 graph materializer.