#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static isolation audit for frozen C1/C3 candidates."""
from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / "core/demon/run_c/c1_c3_overlay.py"
TEST = ROOT / "core/demon/run_c/test_c1_c3_overlay.py"
OUT = ROOT / "current/experiments/GW05_C1_C3_STATIC_AUDIT.json"

BANNED = re.compile(
    r"\b(?:N\d+|K\d+|Q\d+|Z\d+|I\d+|B\d+|G\d+|V\d+|S\d+|R\d+|"
    r"A\d+|E\d+|L\d+|D\d+|F\d+|M\d+|TXT\d+|SEN\d+|SRC\d+)\b"
)


def scan(path):
    text = path.read_text(encoding="utf-8")
    text_hits = sorted(set(BANNED.findall(text)))
    tree = ast.parse(text)
    ast_hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if BANNED.search(node.value):
                ast_hits.append({"line": node.lineno, "value": node.value})
    return {
        "TEXT_HITS": text_hits,
        "AST_HITS": ast_hits,
        "LINES_TOTAL": len(text.splitlines()),
    }


def main():
    report = {
        "C1_C3_AUTHOR_EXPOSURE": "GW05 world text seen (public); answer book not seen",
        "SPEC_BASIS": [
            "GW04 audit: one binding for all requirement patterns",
            "GW04 audit: OPEN by status with resolution transition",
        ],
        "CODE": scan(CODE),
        "TEST": scan(TEST),
    }
    report["ISOLATION_GATE"] = (
        "PASS"
        if not report["CODE"]["TEXT_HITS"]
        and not report["CODE"]["AST_HITS"]
        and not report["TEST"]["TEXT_HITS"]
        and not report["TEST"]["AST_HITS"]
        else "FAIL"
    )
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["ISOLATION_GATE"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
