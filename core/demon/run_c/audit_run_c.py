#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RUN C static audit: LOC, component breakdown and generality gates."""
from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[3]
HANDLER_FILE = ROOT / "core/demon/run_c/family_executor.py"
TEST_FILE = ROOT / "core/demon/run_c/test_family_executor.py"
AUDIT_FILE = ROOT / "core/demon/run_c/audit_run_c.py"
DICTIONARY = ROOT / "current/experiments/GW05_RUN_C_FAMILY_DICTIONARY.json"
DECISIONS = ROOT / "current/experiments/GW05_RUN_C_DECISION_LOG.json"
OUT = ROOT / "current/experiments/GW05_RUN_C_STATIC_AUDIT.json"

BANNED_TOKEN = re.compile(
    r"\b(?:(?:N|K|Q|Z|I|B|G|V|S|R)|N\d+|K\d+|Q\d+|Z\d+|I\d+|B\d+|G\d+|V\d+|S\d+|R\d+|"
    r"A\d+|E\d+|L\d+|D\d+|F\d+|M\d+|TXT\d+|SEN\d+|SRC\d+)\b"
)

GENERIC_OPERATION_NAMES = [
    "current record selection",
    "current triple matching",
    "current value projection",
    "dependency-path expansion",
    "dependency signature matching",
    "relation-slice subject selection",
    "numeric expression evaluation",
    "equality-side evaluation",
    "closure lookup",
    "rule lookup",
    "UNCHECKED marker construction",
]

GENERIC_FUNCTIONS = {
    "current_records", "current_matches", "current_values", "rule_dict", "rule_addr",
    "rule_type", "network_rules", "resolve_paths", "dependency_predicates",
    "dependency_match", "unchecked_marker", "_filter_subjects", "_eval_expression",
    "_equality_sides", "_closure_rule_for", "_closed_members",
}
HANDLER_FUNCTIONS = {
    "handle_exact_cardinality", "handle_balance", "handle_closure",
    "handle_at_most_one", "handle_implication",
}


def docstring_lines(tree):
    out = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if body and isinstance(body, list):
            first = body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                out.update(range(first.lineno, getattr(first, "end_lineno", first.lineno) + 1))
    return out


def code_line_set(path):
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    docs = docstring_lines(tree)
    lines = set()
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s and not s.startswith("#") and i not in docs:
            lines.add(i)
    return text, tree, lines


def loc_counts(path):
    text, _, core = code_line_set(path)
    return {"LOC_TOTAL": len(text.splitlines()), "LOC_CORE": len(core)}


def function_core_lines(path, names):
    _, tree, core = code_line_set(path)
    selected = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names:
            selected.update(i for i in range(node.lineno, getattr(node, "end_lineno", node.lineno) + 1) if i in core)
    return selected


def dispatcher_core_lines(path):
    _, tree, core = code_line_set(path)
    selected = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "FamilyExecutor":
            selected.update(i for i in range(node.lineno, getattr(node, "end_lineno", node.lineno) + 1) if i in core)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "HANDLERS":
                    selected.update(i for i in range(node.lineno, getattr(node, "end_lineno", node.lineno) + 1) if i in core)
    return selected


def ast_constants(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if BANNED_TOKEN.search(node.value):
                bad.append({"line": node.lineno, "value": node.value})
    return bad


def text_gate(path):
    return [{"token": m.group(0)} for m in BANNED_TOKEN.finditer(path.read_text(encoding="utf-8"))]


def main():
    family = json.loads(DICTIONARY.read_text(encoding="utf-8"))
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))

    text_hits = [{"file": str(HANDLER_FILE.relative_to(ROOT)), **h} for h in text_gate(HANDLER_FILE)]
    ast_hits = [{"file": str(HANDLER_FILE.relative_to(ROOT)), **h} for h in ast_constants(HANDLER_FILE)]

    total_handler = loc_counts(HANDLER_FILE)
    _, _, all_core = code_line_set(HANDLER_FILE)
    generic = function_core_lines(HANDLER_FILE, GENERIC_FUNCTIONS)
    handlers = function_core_lines(HANDLER_FILE, HANDLER_FUNCTIONS)
    dispatcher = dispatcher_core_lines(HANDLER_FILE)
    classified = generic | handlers | dispatcher

    report = {
        "FAMILY_TYPE_COUNT": len(family["families"]),
        "GENERIC_OPERATION_COUNT": len(GENERIC_OPERATION_NAMES),
        "GENERIC_OPERATIONS": GENERIC_OPERATION_NAMES,
        "HANDLER_COUNT": len(HANDLER_FUNCTIONS),
        "AUTHOR_DECISION_COUNT": len(decisions["entries"]),
        "LOC": {
            "family_executor": total_handler,
            "family_executor_breakdown_core": {
                "GENERIC_OPERATIONS_LOC_CORE": len(generic),
                "HANDLERS_LOC_CORE": len(handlers),
                "DISPATCHER_LOC_CORE": len(dispatcher),
                "OTHER_INTERFACE_AND_TYPES_LOC_CORE": len(all_core - classified),
            },
            "tests": loc_counts(TEST_FILE),
            "audit_tool": loc_counts(AUDIT_FILE),
            "family_dictionary": {
                "LINES_TOTAL": len(DICTIONARY.read_text(encoding="utf-8").splitlines())
            },
            "decision_log": {
                "LINES_TOTAL": len(DECISIONS.read_text(encoding="utf-8").splitlines())
            }
        },
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
