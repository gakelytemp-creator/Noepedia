#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Focused GW01 training-scene regression for gw04_candidate_overlay.py.

This is not a fresh scientific test.  GW01 is training material.
It checks only that the three frozen candidate mechanisms implement the
GW02_VS_ANSWER_BOOK needs without turning every unresolved state into ASK.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from demon_core import Network, Record, ASK, NEED
from gw04_candidate_overlay import CandidateOverlay


def add(net, rec, state=None):
    net.records[rec.addr] = rec
    rec.committed = True
    if state:
        net.mark(rec.addr, state)
    return rec


net = Network()

for addr, s, p, o in [
    ("RP1", "X", "P4", "O8"),
    ("RP2", "X", "P1", "O1"),
    ("RP3", "X", "P5", "TRUE"),
]:
    add(net, Record(addr, {
        "TYPE": "TRIPLET_PATTERN",
        "SUBJECT": s,
        "PREDICATE": p,
        "OBJECT": o,
    }))

add(net, Record("RQ1", {
    "TYPE": "REQUIREMENT_CONCEPT",
    "REQUIREMENT": ["RP1", "RP2", "RP3"],
}), "OPEN")


def gw01_supported(pattern):
    return pattern.f("PREDICATE") == "P1"


overlay = CandidateOverlay(net)
out = overlay.requirement_asks("RQ1", gw01_supported)
assert len(out.created_asks) == 2
assert {s.query for s in net.stops if s.stop_class == ASK} == {
    "resolve (X P4 O8)",
    "resolve (X P5 TRUE)",
}

# C2 positive control: metadata is NOT hand-written on the OPEN.
# The producer sees one machine-readable missing fact-pattern on a NEED STOP.
s_fact = net.stop(
    "E8/multiplicity",
    "determine current O4/P3 value",
    "multiplicity unresolved",
    ("O4", "P3", "?V"),
    NEED,
)
made = overlay.open_from_stop(s_fact)
assert len(made.created_opens) == 1
out = overlay.promote_resolvable_opens()
assert len(out.created_asks) == 1
assert any(
    s.query == "resolve (O4 P3 ?V)" and s.stop_class == ASK
    for s in net.stops
)

# Negative control: missing structure/rule is not a single fact-pattern.
ask_count = len([s for s in net.stops if s.stop_class == ASK])
s_struct = net.stop(
    "NEG/structure",
    "continue construction",
    "dependency visible",
    "cardinality policy for P3",
    NEED,
)
made = overlay.open_from_stop(s_struct)
assert not made.created_opens
overlay.promote_resolvable_opens()
assert len([s for s in net.stops if s.stop_class == ASK]) == ask_count

net.stop(
    "E2/identity",
    "bind v1 to an O-id",
    "candidates [O4, O11]",
    "discriminating evidence",
    ASK,
    can_ask=True,
    query="which of [O4, O11] is v1?",
)

registry = overlay.final_open_registry()
assert any(a.startswith("OPEN_NEED_") for a in registry)
assert any(a.startswith("OPEN_ASK_") for a in registry)

print("PASS — GW01 focused candidate regression")
print("ASKS:", [(s.where, s.query) for s in net.stops if s.stop_class == ASK])
print("OPEN_REGISTRY:", registry)
