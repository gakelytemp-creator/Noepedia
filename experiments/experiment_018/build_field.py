#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

DETECTOR_WINDOW = 288
MISMATCH_COUNT = 20
CONTROL_COUNT = 20

STATE_WITHIN = "STATE_WITHIN_LOCAL_EXPECTATION"
STATE_OUTSIDE = "STATE_OUTSIDE_LOCAL_EXPECTATION"
UNKNOWN_CAUSE = "UNKNOWN_CAUSE"
WINDOW_288 = "WINDOW_288"
SOURCE_DATASET = "SOURCE_NAB_MACHINE_TEMPERATURE"
RULE_ID = "RULE_EXPECTED_STATE_EQUALS_OBSERVED_STATE"


def load_rows(path: Path):
    rows=[]
    with path.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        for row_number,row in enumerate(reader,start=2):
            rows.append({
                "row_number":row_number,
                "timestamp":row["timestamp"],
                "value":float(row["value"]),
            })
    return rows


def relation(rid,subject,predicate,obj,network,status="settled",provenance=None):
    return {
        "id":rid,
        "subject":subject,
        "predicate":predicate,
        "object":obj,
        "network":network,
        "status":status,
        "provenance":provenance or [],
    }


def main(argv):
    if len(argv)!=4:
        print(
            f"Usage: {Path(argv[0]).name} DATA.csv PREDICTIONS.json FIELD_INPUT.json",
            file=sys.stderr,
        )
        return 2

    rows=load_rows(Path(argv[1]))
    predictions=json.loads(Path(argv[2]).read_text(encoding="utf-8"))

    mismatch_by_ts={m["timestamp"]:m for m in predictions["mismatches"]}
    mismatch_rows=[r for r in rows[DETECTOR_WINDOW:] if r["timestamp"] in mismatch_by_ts]
    control_rows=[r for r in rows[DETECTOR_WINDOW:] if r["timestamp"] not in mismatch_by_ts]

    if len(mismatch_rows)<MISMATCH_COUNT or len(control_rows)<CONTROL_COUNT:
        raise RuntimeError("insufficient mismatch/control rows for frozen 20+20 cut")

    selected=[
        ("MISMATCH",r) for r in mismatch_rows[:MISMATCH_COUNT]
    ] + [
        ("CONTROL",r) for r in control_rows[:CONTROL_COUNT]
    ]

    objects=[
        {"id":STATE_WITHIN,"type":"state"},
        {"id":STATE_OUTSIDE,"type":"state"},
        {"id":UNKNOWN_CAUSE,"type":"unknown_cause"},
        {"id":WINDOW_288,"type":"history_window"},
        {"id":SOURCE_DATASET,"type":"source"},
        {"id":RULE_ID,"type":"consistency_rule"},
    ]
    relations=[]
    open_records=[]

    for n,(kind,row) in enumerate(selected, start=1):
        suffix=f"{n:03d}"
        assessment=f"ASSESSMENT_{suffix}"
        measurement=f"MEASUREMENT_{suffix}"
        expectation=f"EXPECTATION_{suffix}"
        time_obj=f"TIME_{suffix}"
        source_row=f"SOURCE_ROW_{row['row_number']}"

        objects.extend([
            {"id":assessment,"type":"assessment"},
            {"id":measurement,"type":"measurement"},
            {"id":expectation,"type":"expectation"},
            {"id":time_obj,"type":"time"},
            {"id":source_row,"type":"source_row"},
        ])

        observed_state=STATE_OUTSIDE if kind=="MISMATCH" else STATE_WITHIN
        prov=[SOURCE_DATASET,source_row]

        relations.extend([
            relation(f"R_{suffix}_EXP",assessment,"EXPECTED_STATE",STATE_WITHIN,"NET_STATE",provenance=[expectation]),
            relation(f"R_{suffix}_OBS",assessment,"OBSERVED_STATE",observed_state,"NET_STATE",provenance=[measurement]),
            relation(f"R_{suffix}_SUP",assessment,"SUPPORTED_BY",measurement,"NET_PROVENANCE",provenance=prov),
            relation(f"R_{suffix}_DRV",assessment,"DERIVED_FROM",expectation,"NET_PROVENANCE",provenance=prov),
            relation(f"R_{suffix}_MT",measurement,"AT_TIME",time_obj,"NET_TIME",provenance=prov),
            relation(f"R_{suffix}_MS",measurement,"FROM_SOURCE_ROW",source_row,"NET_PROVENANCE",provenance=[SOURCE_DATASET]),
            relation(f"R_{suffix}_MV",measurement,"OBSERVED_VALUE_LITERAL",repr(row["value"]),"NET_MEASUREMENT",provenance=prov),
            relation(f"R_{suffix}_ET",expectation,"AT_TIME",time_obj,"NET_TIME",provenance=prov),
            relation(f"R_{suffix}_EW",expectation,"BASED_ON_PREVIOUS_SAMPLES",WINDOW_288,"NET_EXPECTATION",provenance=prov),
        ])

        if kind=="MISMATCH":
            mismatch=mismatch_by_ts[row["timestamp"]]
            relations.append(
                relation(
                    f"R_{suffix}_DZ",
                    assessment,
                    "DETECTOR_ROBUST_Z_LITERAL",
                    repr(mismatch["robust_z"]),
                    "NET_INSTRUMENTATION",
                    provenance=prov,
                )
            )
            open_records.append({
                "id":f"OPEN_CAUSE_{suffix}",
                "subject":assessment,
                "predicate":"CAUSE_OF_MISMATCH",
                "object":UNKNOWN_CAUSE,
                "status":"open",
                "provenance":[f"R_{suffix}_OBS",f"R_{suffix}_EXP"],
            })

    rules=[
        relation("RULE018_01",RULE_ID,"RULE_SCOPE","assessment","NET_RULE",provenance=[]),
        relation("RULE018_02",RULE_ID,"INPUT_PREDICATE","EXPECTED_STATE","NET_RULE",provenance=[]),
        relation("RULE018_03",RULE_ID,"REQUIRED_PREDICATE","OBSERVED_STATE","NET_RULE",provenance=[]),
        relation("RULE018_04",RULE_ID,"TARGET_CONSTRAINT","SAME_NET","NET_RULE",provenance=[]),
    ]

    field={
        "experiment_id":"NOEPEDIA_EXP_018_REAL_FIELD_INTEGRATION",
        "source":{
            "dataset":SOURCE_DATASET,
            "selection":{
                "mismatch_count":MISMATCH_COUNT,
                "control_count":CONTROL_COUNT,
                "mismatch_policy":"earliest detector mismatches",
                "control_policy":"earliest scored non-mismatch timestamps",
            },
        },
        "objects":objects,
        "networks":[
            "NET_STATE","NET_PROVENANCE","NET_TIME",
            "NET_MEASUREMENT","NET_EXPECTATION","NET_INSTRUMENTATION","NET_RULE"
        ],
        "relations":relations,
        "rules":rules,
        "open":open_records,
    }

    Path(argv[3]).write_text(
        json.dumps(field,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "assessments":len(selected),
        "mismatch_assessments":MISMATCH_COUNT,
        "control_assessments":CONTROL_COUNT,
        "open_records":len(open_records),
        "relations":len(relations),
    },indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main(sys.argv))
