# Experiment 073 — RUN RESULT

## Final status

`NOT_EVALUABLE_ADAPTER_VALIDATION`

Experiment class:
`SCIENTIFIC / HYPOTHESIS TEST`

Focused verification run:
`37321431519`

Direction constraint:
`DIRECTION.md`

## Frozen human hypothesis

`motor1 temperature state follows motor1 voltage state with a positive fixed lag`

Source:
`motor1_voltage`

Target:
`motor1_temperature`

Untouched robot sequence:
`20240527_100759`

No blind pair search was performed.

## Adapter gate

Calibration window:
first 600 rows.

Minimum preregistered cluster size:
`30`

### Voltage

- low centroid = 6592.25
- high centroid = 7033.4324324324325
- threshold = 6812.841216216217
- low cluster count = 8
- high cluster count = 592

Result:
`FAIL`

### Temperature

- low centroid = 48.0
- high centroid = 49.0
- threshold = 48.5
- low cluster count = 597
- high cluster count = 3

Result:
`FAIL`

## Scientific consequence

The preregistered binary-state adapter is not valid for this hypothesis on this sequence.

Therefore:

- discovery lag search was not executed;
- no direction was selected;
- confirmation was not inspected for hypothesis support;
- no null comparison was interpreted;
- the hypothesis was neither supported nor rejected.

Final outcome:

`NOT_EVALUABLE_ADAPTER_VALIDATION`

## No-rescue integrity

After observing the adapter failure, no change was made to:

- motor identity;
- voltage/temperature variable choice;
- sequence;
- split;
- k-means adapter;
- minimum cluster size;
- lag range;
- null shifts;
- promotion criterion.

Experiment 073 is closed here.

Any alternative representation of voltage or temperature requires a new experiment number.

## Ten-line stop — what do we know now that we did not know before 073?

1. The human-selected motor1 voltage -> temperature lag hypothesis is testable in principle with the Noepedia bookkeeping protocol.
2. On sequence 20240527_100759, the preregistered two-state adapter is not scientifically adequate.
3. Motor1 voltage is overwhelmingly concentrated in one calibration state under this adapter.
4. Motor1 temperature is even more concentrated: only 3 of 600 calibration samples form the high cluster.
5. Therefore a binary transition-lag test would be dominated by state imbalance rather than a well-supported two-state process.
6. No evidence for a fixed thermal lag has been established.
7. No evidence against a fixed thermal lag has been established.
8. The correct epistemic state is NOT_EVALUABLE, not REJECT and not PROMOTE.
9. No new architecture is required to record this result.
10. The next scientific step, if pursued, must be a newly preregistered hypothesis/representation test, not a rescue of Experiment 073.

## Directional conclusion

Experiment 073 follows the post-072 direction:

`human physical hypothesis -> frozen test -> legitimate stop`

rather than:

`blind mining -> pipeline repair -> rerun until something passes`
