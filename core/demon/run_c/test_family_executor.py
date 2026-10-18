#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "core/demon"))
sys.path.insert(0, str(HERE))

from demon_core import Network, Record
from family_executor import FamilyExecutor, OPEN

DICT = json.loads((ROOT / "current/experiments/GW05_RUN_C_FAMILY_DICTIONARY.json").read_text())


def add(net, addr, s, p, o):
    r = Record(addr, {"SUBJECT": s, "PREDICATE": p, "OBJECT": o})
    net.records[addr] = r
    r.committed = True
    net.mark(addr, "CURRENT")


def add_rule(net, addr, fields):
    r = Record(addr, {"TYPE": "RULE", **fields})
    net.records[addr] = r
    r.committed = True
    net.mark(addr, "CURRENT")
    return r


def test_cardinality():
    net = Network()
    rule = add_rule(net, "rule_card", {
        "RULE_TYPE": "EXACT_DISTINCT_TARGET_CARDINALITY",
        "subject_class": "thing",
        "predicate": "rel_member",
        "target_class": "agent",
        "target_count": 3,
        "target_count_constraint": "exactly",
        "target_distinctness": "pairwise_distinct",
    })
    add(net, "f_a", "obj_a", "rel_member", "agt_a")
    add(net, "f_b", "obj_a", "rel_member", "agt_b")
    ex = FamilyExecutor(DICT)
    out = ex.execute(rule, net, {"OP": "CHECK", "SUBJECT": "obj_a"})
    assert out.verdict == OPEN
    incoming = Record("incoming", {"SUBJECT": "obj_a", "PREDICATE": "rel_member", "OBJECT": "agt_a"})
    out = ex.execute(rule, net, {"OP": "VALIDATE_INCOMING", "INCOMING": incoming})
    assert out.verdict == "BLOCK"


def test_balance_lookup_and_derivation():
    net = Network()
    closure = add_rule(net, "rule_close", {
        "RULE_TYPE": "EXPLICIT_CLOSED_RELATION_SET",
        "relation": {"subject_class": "thing", "predicate": "rel_in", "target": "scope_a"},
        "set_status": "closed",
        "exact_members": ["obj_a", "obj_b", "obj_c"],
        "closure_scope": "scope_a",
        "other_nodes_closure_declaration": "none",
    })
    rule = add_rule(net, "rule_bal", {
        "RULE_TYPE": "CONDITIONAL_NODE_BALANCE_AND_UNIQUE_MISSING_DERIVATION",
        "balance": {
            "scope_class": "scope",
            "excluded_nodes": [],
            "equality": {
                "left": {"lookup": {"subject": "scoped_node", "predicate": "rel_total"}},
                "right": {
                    "aggregate": "sum",
                    "value_predicate": "rel_value",
                    "link_filter": {"predicate": "rel_in", "target": "scoped_node"}
                }
            }
        },
        "derivation": {
            "missing_fields": ["rel_value"],
            "permission": "only_when",
            "conditions": [{
                "adjacent_link_set": {
                    "relation": {"predicate": "rel_in", "target": "scoped_node"},
                    "closure_declared_by": "rule_close"
                }
            }, {
                "adjacent_links_lacking_Q2_or_Q4": {"count": 1, "constraint": "exactly"}
            }],
            "derived_record_references": ["premises", "rule_bal", "rule_close"]
        }
    })
    add(net, "f_scope", "scope_a", "rel_total", 12)
    add(net, "f_in_a", "obj_a", "rel_in", "scope_a")
    add(net, "f_in_b", "obj_b", "rel_in", "scope_a")
    add(net, "f_in_c", "obj_c", "rel_in", "scope_a")
    add(net, "f_val_a", "obj_a", "rel_value", 5)
    add(net, "f_val_b", "obj_b", "rel_value", 4)
    ex = FamilyExecutor(DICT)
    out = ex.execute(rule, net, {
        "OP": "DERIVE", "SCOPE": "scope_a", "SUBJECT": "obj_c",
        "PREDICATE": "rel_value", "DERIVED_ADDR": "derived_c"
    })
    assert out.verdict == "GO"
    assert out.details["derived"] == ("obj_c", "rel_value", 3)
    assert "rule_close" in out.provenance_requirements


def test_at_most_one_and_implication():
    net = Network()
    card = add_rule(net, "rule_one", {
        "RULE_TYPE": "CURRENT_VALUE_AT_MOST_ONE",
        "subject_class": "thing",
        "predicates": ["rel_mark"],
        "value_cardinality": {"maximum": 1, "scope": "current", "per": ["thing", "predicate"]},
    })
    imp = add_rule(net, "rule_imp", {
        "RULE_TYPE": "CURRENT_STATUS_IMPLIES_MAGNITUDE",
        "antecedent": {"subject": "scoped_subject", "predicate": "rel_state", "object": "state_trigger", "temporal_scope": "current"},
        "consequent": {"subject": "scoped_subject", "predicate": "rel_mark", "object": "mark_required", "modality": "must_hold"},
        "subject_binding": "same_subject",
    })
    add(net, "f_mark", "obj_a", "rel_mark", "mark_old")
    incoming = Record("incoming", {"SUBJECT": "obj_a", "PREDICATE": "rel_state", "OBJECT": "state_trigger"})
    ex = FamilyExecutor(DICT)
    out = ex.execute(imp, net, {"OP": "VALIDATE_INCOMING", "INCOMING": incoming})
    assert out.verdict == "BLOCK"
    incoming2 = Record("incoming2", {"SUBJECT": "obj_a", "PREDICATE": "rel_mark", "OBJECT": "mark_new"})
    out2 = ex.execute(card, net, {"OP": "VALIDATE_INCOMING", "INCOMING": incoming2})
    assert out2.verdict == "BLOCK"


def test_closure_and_dependency_signature():
    net = Network()
    closure = add_rule(net, "rule_close_dep", {
        "RULE_TYPE": "EXPLICIT_CLOSED_RELATION_SET",
        "relation": {"subject_class": "thing", "predicate": "rel_group", "target": "scope_x"},
        "set_status": "closed",
        "exact_members": ["obj_x", "obj_y"],
        "closure_scope": "scope_x",
        "other_nodes_closure_declaration": "none",
    })
    add(net, "f_x", "obj_x", "rel_group", "scope_x")
    add(net, "f_y", "obj_y", "rel_group", "scope_x")
    ex = FamilyExecutor(DICT)
    out = ex.execute(closure, net, {"OP": "CLOSURE", "SCOPE": "scope_x"})
    assert out.verdict == "GO"
    assert out.details["members"] == ["obj_x", "obj_y"]
    incoming = Record("incoming_dep", {"SUBJECT": "obj_z", "PREDICATE": "rel_group", "OBJECT": "scope_x"})
    deps = ex.validation_dependencies(net, incoming)
    assert [r.addr for r in deps] == ["rule_close_dep"]


def main():
    test_cardinality()
    test_balance_lookup_and_derivation()
    test_at_most_one_and_implication()
    test_closure_and_dependency_signature()
    print("RUN C family executor tests: PASS")


if __name__ == "__main__":
    main()
