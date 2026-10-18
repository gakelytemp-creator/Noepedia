#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RUN C static audit: LOC and generality gates."""
from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[3]
TARGETS = [
    ROOT / "core/demon/run_c/family_executor.py",
]
DICTIONARY = ROOT / "current/experiments/GW05_RUN_C_FAMILY_DICTIONARY.json"
DECISIONS = ROOT / "current/experiments/GW05_RUN_C_DECISION_LOG.json"
OUT = ROOT / "current/experiments/GW05_RUN_C_STATIC_AUDIT.json"

BANNED_TOKEN = re.compile(
    r"\b(?:N\d+|K\d+|Q\d+|Z\d+|I\d+|B\d+|G\d+|V\d+|S\d+|R\d+|"
    r"A\d+|E\d+|L\d+|D\d+|F\d+|M\d+|TXT\d+|SEN\d+|SRC\d+)\b"
)


def loc_counts(path):
    text = path.read_text(encoding="utf-8")
    total = len(text.splitlines())
    tree = ast.parse(text)
    doc_lines = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if body and isinstance(body, list):
            first = body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                start = first.lineno
                end = getattr(first, "end_lineno", start)
                doc_lines.update(range(start, end + 1))
    core = 0
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or i in doc_lines:
            continue
        core += 1
    return {"LOC_TOTAL": total, "LOC_CORE": core}


def ast_constants(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if BANNED_TOKEN.search(node.value):
                bad.append({"line": node.lineno, "value": node.value})
    return bad


def main():
    text_hits = []
    ast_hits = []
    loc = {}
    for path in TARGETS:
        rel = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8")
        for m in BANNED_TOKEN.finditer(text):
            text_hits.append({"file": rel, "token": m.group(0)})
        for hit in ast_constants(path):
            hit["file"] = rel
            ast_hits.append(hit)
        loc[rel] = loc_counts(path)

    family = json.loads(DICTIONARY.read_text(encoding="utf-8"))
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))
    report = {
        "FAMILY_TYPE_COUNT": len(family["families"]),
        "GENERIC_OPERATION_COUNT": 11,
        "GENERIC_OPERATIONS": [
            "current record selection",
            "current triple matching",
            "current value projection",
            "nested structural field access",
            "dependency-path expansion",
            "dependency signature matching",
            "relation-slice subject selection",
            "numeric expression evaluation",
            "equality-side evaluation",
            "closure lookup",
            "UNCHECKED marker construction"
        ],
        "HANDLER_COUNT": 5,
        "AUTHOR_DECISION_COUNT": len(decisions["entries"]),
        "LOC": loc,
        "TEXT_GATE_HITS": text_hits,
        "AST_GATE_HITS": ast_hits,
        "GENERALITY_GATE": "PASS" if not text_hits and not ast_hits else "FAIL"
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["GENERALITY_GATE"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
