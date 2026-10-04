# Experiment 053 — Mismatch Feature Extractor

Purpose:
validate automatic extraction of structural mismatch features from source/target observations.

Component:
`core/revision/features.py`

Features under test:
- TEMPORAL_CLUSTERING
- TRANSITION_ALIGNED_MISMATCH
- DIRECTION_ASYMMETRY
- LOCAL_RESIDUAL_CLUSTER
- CLASS_IMBALANCE
- ORIENTATION_UNCERTAINTY
- MID_BAND_UNCERTAINTY
- THRESHOLD_SENSITIVITY

Pass criteria:
- known synthetic geometries produce expected features;
- risk flags are emitted for class imbalance;
- quiet structure does not invent unsupported temporal/local features.
