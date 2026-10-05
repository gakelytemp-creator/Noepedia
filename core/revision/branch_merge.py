# Branch merge helpers.

def diff_from_parent(parent_definition, branch_definition):
    keys=sorted(set(parent_definition)|set(branch_definition))
    changes={}
    for k in keys:
        pv=parent_definition.get(k)
        bv=branch_definition.get(k)
        if pv!=bv:
            changes[k]={"parent":pv,"branch":bv}
    return changes

def analyze_merge(parent_definition, branch_a, branch_b):
    a=diff_from_parent(parent_definition,branch_a["definition"])
    b=diff_from_parent(parent_definition,branch_b["definition"])
    conflicts=[]
    merged=dict(parent_definition)

    for field,change in a.items():
        merged[field]=change["branch"]

    for field,change in b.items():
        if field in a and a[field]["branch"]!=change["branch"]:
            conflicts.append({
                "field":field,
                "branch_a":a[field]["branch"],
                "branch_b":change["branch"]
            })
        else:
            merged[field]=change["branch"]

    status="MERGE_CONFLICT" if conflicts else "MERGEABLE"
    return {
        "status":status,
        "parent_definition":dict(parent_definition),
        "branch_a_changes":a,
        "branch_b_changes":b,
        "conflicts":conflicts,
        "merged_definition":None if conflicts else merged
    }

def create_merged_branch(parent_id, merge_id, branch_a, branch_b, analysis):
    if analysis.get("status")!="MERGEABLE":
        return {
            "type":"META_POLICY_MERGE_CANDIDATE",
            "status":"NOT_CREATED",
            "reason":"MERGE_CONFLICT",
            "conflicts":analysis.get("conflicts",[])
        }
    return {
        "id":merge_id,
        "type":"META_POLICY_MERGE_CANDIDATE",
        "status":"CANDIDATE_BRANCH",
        "parent_id":parent_id,
        "definition":dict(analysis["merged_definition"]),
        "merged_from":[branch_a["id"],branch_b["id"]],
        "active_policy_mutated":False
    }

def compare_merge_with_parents(merge_result, parent_results, minimum_samples=6, max_accuracy_loss=0.0, minimum_graph_valid_rate=1.0):
    if merge_result["sample_count"]<minimum_samples:
        return {"status":"NOT_EVALUABLE","reason":"MINIMUM_SAMPLE_GATE_NOT_MET"}

    if merge_result["graph_valid_rate"]<minimum_graph_valid_rate:
        return {"status":"MERGE_REJECTED","reason":"GRAPH_VALIDITY_BELOW_GATE"}

    best_parent=max(r["accuracy"] for r in parent_results)
    loss=best_parent-merge_result["accuracy"]

    if loss>max_accuracy_loss:
        return {
            "status":"MERGE_REJECTED",
            "reason":"ACCURACY_WORSE_THAN_BEST_PARENT",
            "accuracy_loss":loss
        }

    return {
        "status":"MERGE_WINNER_CANDIDATE",
        "reason":"NO_WORSE_THAN_BEST_PARENT",
        "accuracy_loss":loss,
        "merge_accuracy":merge_result["accuracy"],
        "best_parent_accuracy":best_parent
    }

def materialize_merge(parent_id, branch_a, branch_b, merged_branch, comparison):
    objects=[
        {"id":parent_id,"type":"META_POLICY","status":"PRESERVED"},
        dict(branch_a),
        dict(branch_b)
    ]
    relations=[
        {"subject":branch_a["id"],"predicate":"BRANCHED_FROM_META_POLICY","object":parent_id},
        {"subject":branch_b["id"],"predicate":"BRANCHED_FROM_META_POLICY","object":parent_id}
    ]

    if merged_branch.get("id"):
        objects.append(dict(merged_branch))
        relations.extend([
            {"subject":merged_branch["id"],"predicate":"MERGED_FROM_BRANCH","object":branch_a["id"]},
            {"subject":merged_branch["id"],"predicate":"MERGED_FROM_BRANCH","object":branch_b["id"]},
            {"subject":merged_branch["id"],"predicate":"DERIVED_FROM_META_POLICY","object":parent_id}
        ])

    return {
        "record_type":"META_POLICY_BRANCH_MERGE",
        "objects":objects,
        "relations":relations,
        "comparison":comparison,
        "active_policy_mutated":False
    }
