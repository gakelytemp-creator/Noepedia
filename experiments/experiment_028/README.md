# Experiment 028 — Exploratory Covariate Scan of LOAD_OFF Response Classes

Experiment 028 reuses the preregistered Experiment 027 response labels on the same 48 LOAD_OFF events.

This experiment is explicitly exploratory.

Classes:

```text
CORE: response_rows <= 50
TAIL: response_rows > 50
```

For every other numeric MetroPT-3 channel, report simple event-level differences at frozen offsets:

```text
t=-1, t=0, t=+1, t=+10
```

No classifier is trained and no candidate is declared confirmed.
