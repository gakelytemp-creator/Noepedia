#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WORKSHOP WS05 — identifier gate on the dictionary itself.

RUN C's generality gate scanned handler code only. The world token Q2/Q4 then
entered through the dictionary. This gate scans every key and string value of
a dictionary (except the free-text meta fields) for world-identifier-shaped
parts: one or two capital letters followed by digits (R1, Q2, B3, M2, I13),
taken as a whole word or as an underscore-separated part of a token.

It also re-runs the RUN C completeness criterion (F2): every schema literal
the frozen handler code reads must be declared by the dictionary. Declared
here includes deprecated_aliases and the keys of the *_shapes templates.

Exit code 0 = PASS, 1 = FAIL. Usage: dictionary_gate.py <dictionary.json>
"""
from pathlib import Path
import json, re, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "run_c"))
from audit_run_c import schema_vocabulary_literals, dictionary_vocabulary, HANDLER_FILE

WORLD_ID = re.compile(r"^[A-Z]{1,2}\d+$")
META_KEYS = {"version", "source_basis", "CHANGELOG", "placeholder_convention", "meaning", "placement"}


def _parts(s):
    for word in re.split(r"[^A-Za-z0-9]+", s):
        if WORLD_ID.match(word):
            yield word


def scan(node, path="$"):
    hits = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k in META_KEYS:
                continue
            hits += [(f"{path}.<key>", k, p) for p in _parts(k)]
            hits += scan(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hits += scan(v, f"{path}[{i}]")
    elif isinstance(node, str):
        hits += [(path, node, p) for p in _parts(node)]
    return hits


def _keys(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if not k.startswith("<"):
                out.add(k)
            _keys(v, out)
    elif isinstance(node, list):
        for v in node:
            _keys(v, out)
    elif isinstance(node, str) and not node.startswith("<") and " " not in node:
        out.add(node)


def declared(d):
    out = dictionary_vocabulary(d)
    for spec in d["families"].values():
        out.update(spec.get("deprecated_aliases", {}).keys())
        for k, v in spec.items():
            if k.endswith("_shapes"):
                _keys(v, out)
    return out


def main(argv):
    d = json.load(open(argv[1], encoding="utf-8"))
    hits = scan(d)
    for where, token, part in hits:
        print(f"WORLD_ID {part!r} in {token!r} at {where}")
    undeclared = sorted(schema_vocabulary_literals(HANDLER_FILE) - declared(d))
    for t in undeclared:
        print(f"UNDECLARED handler literal {t!r}")
    print("DICTIONARY_IDENTIFIER_GATE", "PASS" if not hits else f"FAIL ({len(hits)} hits)")
    print("DICTIONARY_COMPLETENESS_GATE", "PASS" if not undeclared else f"FAIL ({len(undeclared)})")
    return 0 if not hits and not undeclared else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
