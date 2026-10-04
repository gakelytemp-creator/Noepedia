# Experiment 055 — Relation Pair Discovery / Megagraph Scan

Purpose:
validate automatic relation-pair discovery before revision.

Component:
`core/revision/scanner.py`

The scanner ranks candidate relation pairs using only discovery-window structure:
- mismatch geometry;
- temporal alignment;
- directional asymmetry;
- local residual structure;
- class imbalance risk;
- non-triviality of the direct relation.

The top eligible pair is then passed to the observation-driven revision pipeline.

Pass criteria:
- meaningful temporal pair ranks above trivial and noisy pairs;
- no pair is selected when every pair is structurally uninformative;
- selected pair proceeds through the existing pipeline without manual feature or candidate-family selection.
