# Experiment 067 — Parser Correction

The first execution produced calibration RMS thresholds on the order of 10^18 to 10^32.

This is incompatible with the documented numeric scale of the NASA Milling sensor traces and indicates a MATLAB-structure parsing error, not a scientific outcome.

Cause:
the initial implementation loaded `mill.mat` using `squeeze_me=True, struct_as_record=False` and then flattened MATLAB object fields through `mat_struct`.

The source file is a structured MATLAB array whose documented fields are accessed as structured-array fields.

Correction:
- load with `struct_as_record=True, squeeze_me=False`;
- iterate the 1 x 167 structured array directly;
- read each channel from `mill[0, i][channel]`.

Frozen scientific choices remain unchanged:
- dataset;
- six channels;
- RMS feature;
- calibration/discovery/buffer/confirmation split;
- calibration-only 1-D k-means;
- all 15 pairs;
- lag grid;
- permutation nulls;
- shuffled-control seeds;
- promotion gates;
- primary outcome classes.

The first 0-real / 0-shuffled classification is therefore marked NOT_EVALUABLE_IMPLEMENTATION_ERROR and is not interpreted as a scientific null result.
