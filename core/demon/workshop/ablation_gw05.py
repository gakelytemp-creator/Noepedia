#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WORKSHOP WS06 — method ablation matrix on scene GW05 (ATTIC 01 A12.13).

Runs gw05_scene.execute() under every combination of the workshop switches
and records the resulting network state. Scope: GW05's task class only. A
zero contribution here means "zero on this scene", not "zero in general".

Output: ablation_gw05.json (all runs) and a printed summary.
"""
from pathlib import Path
import itertools, json, sys
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "run_c"), str(HERE)]
import gw05_scene as scene
from admission import PER_RULE_DEBT, PER_FACT_MARKER

V3 = HERE / "dictionary_v0_3.json"
INGEST = ("F4", "F7", "F8", "F10")


def metrics(out):
    ev = {e["EVENT"]: e for e in out["EVENTS"]}
    f12 = ev["F12"]["NOTE"]
    committed = sum(r["COMMITTED"] for k in INGEST for r in ev[k]["NOTE"])
    total = sum(len(ev[k]["NOTE"]) for k in INGEST)
    reg = f12["OPEN_REGISTRY"]
    return {
        "facts_committed": f"{committed}/{total}",
        "bound": ev["F11"]["NOTE"].get("BOUND"),
        "registry_size": len(reg),
        "signals_in_network": len(f12.get("OPEN_SIGNALS", [])),
        "conflicts_open": sum("CONFLICT" in r for r in reg),
        "debt_open": sum(("UNCHECKED" in r) or r.startswith("DEBT_") for r in reg),
        "asks_unanswered": len(f12["ASK_UNANSWERED"]),
        "need_stops": len(f12["NEED"]),
        "verdicts": "".join(ev[f"F{i}"]["VERDICT"][0] for i in range(1, 13)),
    }


def run_all():
    rows = []
    for enc, c13, adm, res, shape, dct in itertools.product(
            "NL", (False, True), (False, True), (False, True),
            (PER_FACT_MARKER, PER_RULE_DEBT), (None, V3)):
        if not adm and shape == PER_RULE_DEBT:
            continue                      # debt shape is meaningless without admission
        out = scene.execute(enc, c13, adm, res, shape, dct)
        rows.append({"encoder": enc, "c13": c13, "admission": adm, "resolve_asks": res,
                     "debt_shape": "rule" if shape == PER_RULE_DEBT else "fact",
                     "dictionary": "V0.3" if dct else "V0.2", **metrics(out)})
    return rows


def main():
    rows = run_all()
    (HERE / "ablation_gw05.json").write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")
    keys = ("facts_committed", "bound", "registry_size", "signals_in_network", "conflicts_open", "debt_open",
            "asks_unanswered", "need_stops", "verdicts")
    print("enc c13 adm res debt dict |", " ".join(keys))
    for r in rows:
        print(r["encoder"], int(r["c13"]), int(r["admission"]), int(r["resolve_asks"]),
              r["debt_shape"], r["dictionary"], "|", " ".join(str(r[k]) for k in keys))


if __name__ == "__main__":
    main()
