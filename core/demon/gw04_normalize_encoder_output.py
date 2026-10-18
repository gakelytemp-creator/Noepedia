#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GW04 raw encoder-output normalizer.

Mechanical only:
  YAML safe_load -> JSON dump preserving list/map order.
No RULE_TYPE names, world predicates, or event semantics are inspected here.

This script is not used by RUN A/B. Its output is sealed before the runs;
the runner consumes the sealed JSON artifact.
"""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "current/experiments/GW04_ENCODER_OUTPUT.yaml"
OUT = ROOT / "current/experiments/GW04_ENCODER_OUTPUT.normalized.json"

obj = yaml.safe_load(RAW.read_text(encoding="utf-8"))
OUT.write_text(
    json.dumps(obj, ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n",
    encoding="utf-8",
)
print(OUT)
