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
