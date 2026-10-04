# Experiment 032 — RUN RESULT

## Status

reproducibility = PASS
result = PHYSICAL_TIME_CLUSTER_REPLICATED

GitHub Actions: run_id = 37197772182, conclusion = success

## Event-wise physical time

W027:
- events = 48
- gap-crossing events = 0
- min = 406 s
- median = 416 s
- p25 = 416 s
- p75 = 417 s
- p90 = 509.5 s
- p95 = 910.5 s
- max = 981 s

W030:
- events = 30
- gap-crossing events = 0
- min = 406 s
- median = 416 s
- p25 = 416 s
- p75 = 417 s
- p90 = 437.9 s
- p95 = 452.05 s
- max = 516 s

Combined:
- events = 78
- median = 416 s
- p25 = 416 s
- p75 = 417 s
- 71/78 events lie in 301–450 s

Therefore PHYSICAL_TIME_CLUSTER_REPLICATED.

The replicated 42-row object is a real physical-time cluster near 416 s ≈ 6 min 56 s ≈ 7 minutes, not an artifact of the rare timestamp gaps found in Experiment 031.

The five W027 long-tail events remain real, reaching up to 981 s. The result supports a dominant ~7-minute class with a minority long tail, not an exact universal timer.

OPEN after Experiment 032: return this learned temporal structure to the Noepedia field as a provenance-bearing revised rule and test it on untouched data.