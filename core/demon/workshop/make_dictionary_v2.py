#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WORKSHOP WS05 — derive dictionary V0.3 from the frozen GW05 dictionary V0.2.

The frozen file current/experiments/GW05_RUN_C_FAMILY_DICTIONARY.json is not
touched. Every change is a named, reproducible transformation below, so the
diff between contracts is itself an addressable record (CHANGELOG).

Repairs (GW05 audit §4):
  R1  filter variants get explicit shapes, not just names;
  R2  the GW04 world token adjacent_links_lacking_Q2_or_Q4 is replaced by a
      parameterized generic condition members_lacking_value;
  R3  the GW04-encoder alias other_links_than_left becomes a declared,
      deprecated alias of the canonical other_members_than_other_side.
The identifier gate (dictionary_gate.py) must pass on the output.
"""
from pathlib import Path
import copy, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / "current/experiments/GW05_RUN_C_FAMILY_DICTIONARY.json"
OUT = HERE / "dictionary_v0_3.json"
FAM = "CONDITIONAL_NODE_BALANCE_AND_UNIQUE_MISSING_DERIVATION"
OLD_TOKEN = "adjacent_links_lacking_Q2_or_Q4"
NEW_TOKEN = "members_lacking_value"


def build(src):
    d = copy.deepcopy(src)
    d["version"] = "RUN_C_FAMILY_DICTIONARY_V0.3_WORKSHOP"
    d["source_basis"] = ("V0.2 (GW05 frozen) + workshop repairs R1-R3 after GW05 post-unseal audit §4; "
                         "not evidence of transfer until a new cold translation is run against it")
    d["placeholder_convention"] = {
        "<PREDICATE>": "a predicate identifier of the world being encoded",
        "<TARGET>": "an object identifier of the world, or the token scoped_node",
        "<COUNT>": "a non-negative integer",
        "<FILTER>": "any filter shape listed in filter_variant_shapes",
    }
    f = d["families"][FAM]

    # R1 — shapes, written as literal JSON templates; the variant name is NOT a key.
    f["filter_variant_shapes"] = {
        "predicate_target": {
            "shape": {"predicate": "<PREDICATE>", "target": "<TARGET>"},
            "placement": "the object itself is the value of link_filter; there is no 'predicate_target' key",
        },
        "all": {
            "shape": {"all": ["<FILTER>", "..."]},
            "placement": "value of link_filter; members are filter shapes or the relation clause below",
        },
        "other_members_than_other_side": {
            "shape": {"relation": "other_members_than_other_side"},
            "placement": "only as a member of an 'all' list",
        },
    }
    f["expression_variant_shapes"] = {
        "aggregate": {"shape": {"aggregate": "sum", "value_predicate": "<PREDICATE>", "link_filter": "<FILTER>"}},
        "lookup": {"shape": {"lookup": {"subject": "scoped_node", "predicate": "<PREDICATE>"}}},
    }
    f["condition_shapes"] = {
        "adjacent_link_set": {"shape": {"adjacent_link_set": {
            "relation": {"predicate": "<PREDICATE>", "target": "scoped_node"},
            "closure_declared_by": "<RULE_ADDR>"}}},
        NEW_TOKEN: {"shape": {NEW_TOKEN: {
            "value_predicate": "<PREDICATE>", "count": "<COUNT>", "constraint": "exactly"}},
            "meaning": "number of scoped members that lack a current value of value_predicate"},
    }

    # R2 — replace the world token everywhere it occurs.
    f["optional_paths"] = [p.replace(OLD_TOKEN, NEW_TOKEN) for p in f["optional_paths"]]
    f["optional_paths"].append(f"derivation.conditions[].{NEW_TOKEN}.value_predicate")
    f["literal_tokens"] = [NEW_TOKEN if t == OLD_TOKEN else t for t in f["literal_tokens"]]

    # R3 — declare the alias instead of listing it as an equal token.
    f["literal_tokens"] = [t for t in f["literal_tokens"] if t != "other_links_than_left"]
    f["deprecated_aliases"] = {"other_links_than_left": "other_members_than_other_side"}

    d["CHANGELOG"] = [
        {"id": "R1", "family": FAM, "change": "added filter_variant_shapes, expression_variant_shapes, condition_shapes"},
        {"id": "R2", "family": FAM, "change": f"{OLD_TOKEN} -> {NEW_TOKEN} (parameterized by value_predicate)"},
        {"id": "R3", "family": FAM, "change": "other_links_than_left moved to deprecated_aliases"},
    ]
    return d


def main():
    out = build(json.loads(SRC.read_text(encoding="utf-8")))
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    sys.exit(main())
