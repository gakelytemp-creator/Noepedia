# Experiment 028 — RUN RESULT

## Status

```text
reproducibility = PASS
role            = EXPLORATORY CANDIDATE GENERATION
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37192681846
conclusion = success
```

## Event classes

Frozen from Experiment 027:

```text
CORE response <= 50 rows = 43 events
TAIL response > 50 rows  =  5 events
```

## Top exploratory candidate

The preregistered ranking rule was:

1. larger absolute Cliff's delta;
2. larger absolute median difference;
3. channel / offset deterministic tie break.

Top result:

```text
channel = TP3
offset  = +10 rows

CORE median = 9.914
TAIL median = 9.602

TAIL - CORE median difference = -0.312
Cliff's delta CORE vs TAIL    = +0.90698
```

The next two ranked effects were highly similar:

```text
H1 @ +10         delta = +0.90698
Reservoirs @ +10 delta = +0.90698
```

Oil_temperature also showed a large exploratory separation:

```text
t=0
CORE median = 70.425
TAIL median = 74.825
delta CORE vs TAIL = -0.84186
```

## Interpretation boundary

Experiment 028 is not confirmatory.

The TAIL class contains only five events and many channel/offset combinations were scanned.

Therefore the TP3 +10 relation is only a candidate for untouched-window confirmation.

Experiment 029 freezes exactly that candidate before examining a new window.
