# Experiment 032 — Event-wise Physical Response Time Audit

Experiment 032 converts the already frozen LOAD_OFF response events from Experiments 027 and 030 into actual physical time using dataset timestamps.

For each event:

```text
physical_response_seconds =
timestamp[t + response_rows] - timestamp[t]
```

It also flags whether any adjacent timestamp gap inside the response interval exceeds twice the local 10 s median cadence.
