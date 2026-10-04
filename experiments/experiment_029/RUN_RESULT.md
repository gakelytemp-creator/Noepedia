# Experiment 029 — RUN RESULT

## Status

```text
reproducibility = PASS
result          = NOT_REPLICATED
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37192859275
conclusion = success
```

## Frozen confirmatory window

```text
rows 300,001..305,000
```

The only confirmatory candidate was frozen from Experiment 028:

```text
TP3 at t=+10 after LOAD_OFF
expected direction:
CORE > TAIL
```

No replacement channel or offset was selected on the confirmation window.

## Response-class counts

```text
LOAD_OFF events total = 35
resolved              = 35
censored              =  0

CORE <=50 rows        = 32
TAIL >50 rows         =  3
```

The preregistered minimum of three TAIL events was met, so the class comparison was evaluable.

## Confirmatory result

```text
CORE TP3(+10) median = 9.890
TAIL TP3(+10) median = 9.904
```

Difference:

```text
TAIL - CORE = +0.014
```

Cliff's delta:

```text
CORE vs TAIL = -0.27083
```

The exploratory direction from Experiment 028 did not reproduce.

Experiment 028 had:

```text
CORE median = 9.914
TAIL median = 9.602
delta       = +0.90698
```

Experiment 029 produced:

```text
CORE median = 9.890
TAIL median = 9.904
delta       = -0.27083
```

Therefore:

```text
result = NOT_REPLICATED
```

## Interpretation

TP3 at +10 should not be treated as an explanatory relation for the long-tail LOAD_OFF response class.

The strong Experiment 028 effect was an exploratory-window association that failed untouched-window confirmation.

This is exactly the purpose of the 028 -> 029 separation:

```text
candidate generation
!=
knowledge
```

The failure does not weaken the already established direction-dependent Motor_current response itself.

It only removes one proposed secondary covariate.

## What remains supported

The evidence chain through Experiment 027 remains:

```text
LOAD_ON:
raw Motor_current reaches the frozen high regime immediately

LOAD_OFF:
raw Motor_current reaches the frozen low regime after tens of rows,
with a minority long tail
```

Experiment 029 does not test or reject that primary temporal asymmetry.

## Claim boundary

The failed TP3 candidate does not imply that no observable channel can explain response-time variation.

It means only:

```text
TP3 at +10
as selected by the exploratory 028 ranking
did not transfer.
```

## OPEN after Experiment 029

The next scientifically clean move is not to walk down the Experiment 028 ranked list one candidate at a time.

That would recreate a multiple-testing / forking-path problem.

Instead, the next experiment should first replicate the primary LOAD_ON / LOAD_OFF response-time distribution itself on another untouched window before searching for secondary predictors again.
