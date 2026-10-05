# Experiment 071 — Blind Robot-Telemetry Discovery Challenge

Experiment class: SCIENTIFIC / REAL-DATA DISCOVERY

Purpose:
test the repaired Noepedia revision pipeline on a new real physical system that is unrelated to MetroPT, the hydraulic stand, and NASA Milling.

System:
CentraleSupélec robot predictive-maintenance telemetry from a six-servo ArmPi FPV robot.

Data source used for reproducibility:
public GitHub mirror `efeolgun/robot-predictive-maintenance`, frozen at commit
`cec9f8a95d6099201cbf9afb8821696dc0ebd7cd`.

Original challenge provenance:
CentraleSupélec Maintenance & Industry 4.0 / Kaggle Robot Predictive Maintenance.

Blind data:
testing sequence `20240527_094865`, selected as the lexicographically first testing sequence before outcome inspection.

Labels are ignored and are empty in the selected testing CSVs.

Frozen Noepedia core commit:
`e9885e1bc3f0fcddad2d982eea2ec273e968575e`

Primary safety criterion:
`shuffled promotion count = 0`

A zero real-data promotion count is a valid scientific null result.
