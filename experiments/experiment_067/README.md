# Experiment 067 — Blind Real-System Discovery Challenge

Experiment class: SCIENTIFIC / REAL-DATA DISCOVERY

This experiment is intentionally separated from Experiments 042–066, which primarily validate the revision machinery itself.

Goal:
test whether the frozen Noepedia revision pipeline can discover at least one null-protected relation on a new real physical system while producing zero promotions on a shuffled control.

External system:
NASA / UC Berkeley Milling Wear data.

Frozen core revision commit:
`85ec973cf4b38fce9a6aa41fedd77f123ebfd6bc`

Primary scientific safety criterion:
`shuffled promotion count = 0`

A zero real-data promotion count is a valid null result.
