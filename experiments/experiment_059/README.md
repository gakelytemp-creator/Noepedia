# Experiment 059 — Strategy Selection / Meta-Policy

Purpose: validate automatic revision-strategy selection from observable history properties.

Presets:
- DENSE
- SPARSE
- CONSERVATIVE

Selection inputs:
- relation count
- event count
- event density
- time span
- transition-density proxy

Pass criteria:
- dense history selects DENSE;
- sparse change-event history selects SPARSE;
- small/insufficient history selects CONSERVATIVE;
- meaningful sparse history runs through the automatic strategy pipeline and records strategy provenance.
