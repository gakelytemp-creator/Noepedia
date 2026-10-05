# Real-Data Instrumentation Track — Methodology Status after Experiments 011–016

> **Current architecture precedence:** implementation and new experiments must follow [CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md), [SOCRATIC_DAIMONION.md](SOCRATIC_DAIMONION.md), and [DIRECTION.md](DIRECTION.md). Older metaphors in this document are historical/conceptual where they conflict with that boundary.

> **Status update:** Experiments 011–016 are retained as an exploratory / instrumentation track, not as validation of the Noepedia core architecture.

## Why this status changed

Three methodological limits became clear after the first real-data sequence.

### 1. Experiment 011 used a weak absolute success gate

Experiment 011 froze:

~~~text
window_recall >= 0.50
point_precision >= 0.20
~~~

The recall criterion is weak for this dataset because the labeled anomaly windows occupy a substantial fraction of the timeline and a large number of random detections can hit all windows.

The scientifically informative quantity is enrichment above a matched-count random baseline.

Therefore the original Experiment 011 record is not rewritten, but its interpretation is narrowed:

> Experiment 011 shows a reproducible label-blind detector output on real data. Its precision is potentially informative, but the preregistered gate did not include an explicit null baseline.

No post-hoc replacement of the original gate is performed inside Experiment 011.

### 2. Experiments 012–016 are an adaptive cascade on one dataset

Each experiment was preregistered before its own run, but each next question was chosen after observing the previous result on the same time series.

Therefore:

~~~text
per-experiment preregistration
≠
independent confirmation of the whole sequence
~~~

Experiments 012–016 are retained as exploratory structural findings / hypothesis generation.

In particular, Experiment 014's two-cluster separation is an observation on the development series, not an independently validated family structure.

### 3. The real-data line is instrumentation, not yet Noepedia-core validation

Experiments 011–016 do not execute the relational rule evaluator from Experiment 003.

Their purpose is therefore reclassified as:

~~~text
REAL-DATA INSTRUMENTATION / EXPLORATION TRACK
~~~

They test disciplined contact with external data, blind staging, provenance, reproducibility, OPEN generation, and frozen follow-up analysis.

They do **not** by themselves validate the Noepedia relational core.

## Next methodological gate

Before any further feature hunting on the development series:

> run the frozen pipeline once on a held-out NAB file that has not been inspected for values or labels during pipeline design.

Experiment 017 performs that test.

It adds an explicit matched-count random null baseline and separates:

~~~text
PRIMARY:
detector enrichment above chance

SECONDARY:
whether the previously frozen episode / transition / cluster structure also reproduces
without changing its rules
~~~

No parameter is to be changed after the held-out run is observed.

## Status terminology

For Experiments 011–016:

~~~text
CI PASS / FAIL
    reproducibility status

ORIGINAL SCIENTIFIC GATE PASS / FAIL
    historical preregistered outcome

CURRENT EVIDENCE STATUS
    exploratory / development-series finding
~~~

These three labels must not be collapsed.

## Return to the Noepedia core

A later experiment must write observations, expectations, mismatch events, provenance, and unresolved structure into the relational field and let explicit rule objects participate in evaluation.

Until then, this track should be cited as instrumentation supporting future Noepedia experiments, not as proof of the architecture.
