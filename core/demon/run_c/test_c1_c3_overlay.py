#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Neutral tests for C1/C3. No GW05 scene data is used."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "core/demon"))
sys.path.insert(0, str(HERE))

from demon_core import Network, Record
from c1_c3_overlay import C1C3Overlay


def add_current(net, addr, s, p, o):
    r = Record(addr, {"SUBJECT": s, "PREDICATE": p, "OBJECT": o})
    net.records[addr] = r
    r.committed = True
    net.mark(addr, "CURRENT")
    return r


def add_requirement(net):
    p1 = Record("pat_left", {
        "TYPE": "TRIPLET_PATTERN",
        "SUBJECT": "?candidate",
        "PREDICATE": "rel_left",
        "OBJECT": "target_alpha",
    })
    p2 = Record("pat_right", {
        "TYPE": "TRIPLET_PATTERN",
        "SUBJECT": "?candidate",
        "PREDICATE": "rel_right",
        "OBJECT": "target_beta",
    })
    rq = Record("rq_joint", {
        "TYPE": "REQUIREMENT_CONCEPT",
        "REQUIREMENT": ["pat_left", "pat_right"],
    })
    for r in (p1, p2, rq):
        net.records[r.addr] = r
        r.committed = True
    net.mark("rq_joint", "OPEN")
    return rq


def test_c1_requires_one_joint_binding():
    net = Network()
    add_requirement(net)
    add_current(net, "fact_left", "object_one", "rel_left", "target_alpha")
    add_current(net, "fact_right", "object_two", "rel_right", "target_beta")

    overlay = C1C3Overlay(net)
    assert overlay.requirement_joint_supported("rq_joint") is False
    out = overlay.requirement_ask("rq_joint")
    assert len(out.created_asks) == 1

    add_current(net, "fact_join", "object_one", "rel_right", "target_beta")
    assert overlay.requirement_joint_supported("rq_joint") is True


def test_c3_registry_uses_status_not_type():
    net = Network()
    add_requirement(net)
    ordinary = Record("status_only_open", {"TYPE": "NOTE"})
    net.records[ordinary.addr] = ordinary
    ordinary.committed = True
    net.mark(ordinary.addr, "OPEN")

    overlay = C1C3Overlay(net)
    registry = overlay.current_open_registry()
    assert "rq_joint" in registry
    assert "status_only_open" in registry


def test_c3_resolution_is_non_destructive():
    net = Network()
    overlay = C1C3Overlay(net)

    net.stop(
        where="neutral/query",
        wanted="one external fact",
        available="not yet known",
        missing=("entity_a", "rel_value", "?value"),
        stop_class="ASK",
        can_ask=True,
        query="resolve (entity_a rel_value ?value)",
    )
    made = overlay.materialize_ask_opens()
    assert len(made.created_opens) == 1
    open_addr = made.created_opens[0]
    assert open_addr in overlay.current_open_registry()

    fact = add_current(net, "answer_fact", "entity_a", "rel_value", 17)
    resolved = overlay.resolve_from_fact(fact)
    assert resolved.resolved_opens == (open_addr,)
    assert open_addr not in overlay.current_open_registry()

    states = [s.state for s in net.read(open_addr).status_log]
    assert states == ["OPEN", "RESOLVED"]


def main():
    test_c1_requires_one_joint_binding()
    test_c3_registry_uses_status_not_type()
    test_c3_resolution_is_non_destructive()
    print("C1/C3 neutral tests: PASS")


if __name__ == "__main__":
    main()
