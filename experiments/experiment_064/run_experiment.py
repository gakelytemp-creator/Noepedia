import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT))

from core.revision.lineage import build_lineage, ancestors, descendants, checkout_policy, compare_policy_definitions, trace_lineage

def main():
    objects=[
      {"id":"META_POLICY_V1","type":"META_POLICY","status":"HISTORICAL_SOURCE","definition":{"small_history_strategy":"CONSERVATIVE","minimum_samples":5}},
      {"id":"META_POLICY_V2","type":"META_POLICY","status":"SUPERSEDED","definition":{"small_history_strategy":"SPARSE","minimum_samples":5}},
      {"id":"META_POLICY_V3","type":"META_POLICY","status":"ACTIVE","definition":{"small_history_strategy":"CONSERVATIVE","minimum_samples":5}}
    ]
    relations=[
      {"subject":"META_POLICY_V2","predicate":"DERIVED_FROM_META_POLICY","object":"META_POLICY_V1"},
      {"subject":"META_POLICY_V3","predicate":"DERIVED_FROM_META_POLICY","object":"META_POLICY_V2"},
      {"subject":"META_POLICY_V3","predicate":"RESTORES_DEFINITION_FROM","object":"META_POLICY_V1"}
    ]
    lineage=build_lineage(objects,relations)
    co1=checkout_policy(lineage,"META_POLICY_V1")
    co2=checkout_policy(lineage,"META_POLICY_V2")
    co3=checkout_policy(lineage,"META_POLICY_V3")
    diff12=compare_policy_definitions(lineage,"META_POLICY_V1","META_POLICY_V2")
    diff23=compare_policy_definitions(lineage,"META_POLICY_V2","META_POLICY_V3")
    path=trace_lineage(lineage,"META_POLICY_V1","META_POLICY_V3")
    checks={
      "v3_ancestors":ancestors(lineage,"META_POLICY_V3")==["META_POLICY_V2","META_POLICY_V1"],
      "v1_descendants":descendants(lineage,"META_POLICY_V1")==["META_POLICY_V2","META_POLICY_V3"],
      "v1_read_only":co1["read_only"] is True and co1["live_policy_mutated"] is False,
      "v2_read_only":co2["read_only"] is True and co2["live_policy_mutated"] is False,
      "v3_read_only":co3["read_only"] is True and co3["live_policy_mutated"] is False,
      "v3_restore_source":co3["restore_source"]=="META_POLICY_V1",
      "path_v1_v3":path==["META_POLICY_V1","META_POLICY_V2","META_POLICY_V3"],
      "v1_v2_diff":diff12["change_count"]==1,
      "v2_v3_diff":diff23["change_count"]==1,
      "v3_matches_v1":co3["policy"]["definition"]==co1["policy"]["definition"]
    }
    out={
      "experiment":"NOEPEDIA_EXP_064_POLICY_LINEAGE_TIME_TRAVEL",
      "path_v1_v3":path,
      "diffs":{"v1_v2":diff12,"v2_v3":diff23},
      "checks":checks,
      "architectural_pass":all(checks.values())
    }
    (HERE/"_runtime").mkdir(exist_ok=True)
    (HERE/"_runtime"/"result.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["architectural_pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
