# Experiment 025 — Raw Motor-current Gap Test on a New Untouched Window

Experiment 025 asks why Experiment 024 produced identical binary classifications across a wide Motor_current threshold family.

Frozen windows:

```text
Calibration:     rows 1..50,000
Experiment 024:  rows 150,001..155,000
Experiment 025:  rows 200,001..205,000
```

No new classifier is introduced.

The experiment measures raw Motor_current values relative to the frozen threshold band:

```text
low edge  = threshold(alpha=0.20)
high edge = threshold(alpha=0.80)
```

and reports how many raw values lie:

```text
below the band
inside the band
above the band
```

with the same counts split by temporal proximity to DV_eletric transitions.
