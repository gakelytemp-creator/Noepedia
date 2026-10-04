# Experiment 031 — RUN RESULT

## Status

```text
reproducibility = PASS
cross-window median cadence = MATCH
per-window cadence class    = VARIABLE_CADENCE
```

GitHub Actions:

```text
Noepedia Experiment Verification
run_id = 37196103808
conclusion = success
```

## Windows

```text
W027 = rows 250,001..255,000
W030 = rows 350,001..355,000
W031 = rows 400,001..405,000
```

## W027 cadence

```text
intervals = 4999
median dt = 10 s
p25       = 10 s
p75       = 10 s
p95       = 10 s
min       = 9 s
max       = 4850 s

dt counts:
9 s     = 440
10 s    = 4555
11 s    = 1
12 s    = 1
283 s   = 1
4850 s  = 1

gaps > 2 * median = 2
cadence class      = VARIABLE_CADENCE
```

## W030 cadence

```text
intervals = 4999
median dt = 10 s
p25       = 10 s
p75       = 10 s
p95       = 10 s
min       = 9 s
max       = 33535 s

dt counts:
9 s      = 435
10 s     = 4563
33535 s  = 1

gaps > 2 * median = 1
cadence class      = VARIABLE_CADENCE
```

## W031 untouched cadence-check window

```text
intervals = 4999
median dt = 10 s
p25       = 10 s
p75       = 10 s
p95       = 10 s
min       = 9 s
max       = 10 s

dt counts:
9 s   = 436
10 s  = 4563

gaps > 2 * median = 0
cadence class      = VARIABLE_CADENCE
```

The preregistered class is technically VARIABLE_CADENCE because 9 s and 10 s are not identical and their range exceeds 1% of the 10 s median.

Operationally, however, the ordinary cadence is strongly concentrated at 10 s with a minority of 9 s intervals.

## Cross-window cadence

All three medians are:

```text
10 s
```

Therefore:

```text
CROSS_WINDOW_CADENCE_MATCH
```

## Row-to-time conversion

Using the frozen median-cadence conversion:

```text
41 rows = 410 s = 6 min 50 s
42 rows = 420 s = 7 min
52 rows = 520 s = 8 min 40 s
99 rows = 990 s = 16 min 30 s
```

Thus the replicated central LOAD_OFF response:

```text
median = 42 rows
```

corresponds approximately to:

```text
420 s
= 7 minutes
```

under the typical 10 s sampling cadence.

## Important correction

The timestamps reveal rare but very large acquisition gaps:

```text
W027:
283 s
4850 s

W030:
33535 s
```

Therefore:

```text
42 rows != necessarily exactly 420 physical seconds
for every individual event
```

if an event-response interval crosses one of these timestamp gaps.

The 7-minute value is a median-cadence conversion, not yet an event-wise physical-time measurement.

## Epistemic consequence

Before Experiment 031 we had:

```text
LOAD_OFF response ~= 42 rows
```

After Experiment 031 we can say:

```text
typical sampling cadence ~= 10 seconds per row
so 42 rows ~= 7 minutes
```

but the presence of rare acquisition gaps prevents us from replacing the row-based response with physical time by multiplication alone.

## Claim boundary

Experiment 031 establishes:

- the typical source cadence is about 10 s;
- the median cadence matches across W027, W030, and W031;
- rare large timestamp gaps exist in W027 and W030.

It does not yet establish the exact physical response-time distribution event by event.

## OPEN after Experiment 031

The next clean experiment is:

> Recompute the already frozen Experiment 027/030 LOAD_OFF response events in actual timestamp time, using

```text
physical_response_seconds =
timestamp[t + response_rows] - timestamp[t]
```

for each event individually.

It should also flag any event whose response interval crosses an abnormal acquisition gap.

That experiment will determine whether the replicated ~42-row object is truly a tightly clustered ~7-minute physical-time object, or whether row-space regularity partly hides timestamp discontinuities.
