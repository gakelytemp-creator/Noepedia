# Policy branching and counterfactual replay helpers.

def create_branch(parent_id, branch_id, definition, rationale):
    if not parent_id or not branch_id or parent_id==branch_id:
        raise ValueError("invalid branch ids")
    return {
        "id":branch_id,
        "type":"META_POLICY_BRANCH",
        "parent_id":parent_id,
        "definition":dict(definition),
        "rationale":rationale,
        "status":"CANDIDATE_BRANCH"
    }

def replay_branch(branch, cases, evaluator):
    rows=[]
    for case in cases:
        outcome=evaluator(branch["definition"],case)
        rows.append({
            "case_id":case["case_id"],
            "preferred_outcome":case["preferred_outcome"],
            "observed_outcome":outcome,
            "correct":outcome==case["preferred_outcome"],
            "graph_valid":bool(case.get("graph_valid",True))
        })
    n=len(rows)
    return {
        "branch_id":branch["id"],
        "sample_count":n,
        "accuracy":sum(r["correct"] for r in rows)/n if n else None,
        "graph_valid_rate":sum(r["graph_valid"] for r in rows)/n if n else None,
        "rows":rows
    }

def compare_branches(results, minimum_samples=6, minimum_accuracy_margin=0.10, minimum_graph_valid_rate=1.0):
    eligible=[]
    for r in results:
        if r["sample_count"]<minimum_samples:
            continue
        if r["graph_valid_rate"]<minimum_graph_valid_rate:
            continue
        eligible.append(r)
    eligible=sorted(eligible,key=lambda x:(-x["accuracy"],x["branch_id"]))
    if not eligible:
        return {"status":"NOT_EVALUABLE","winner":None,"reason":"NO_ELIGIBLE_BRANCH"}
    if len(eligible)==1:
        return {"status":"BRANCH_WINNER_CANDIDATE","winner":eligible[0]["branch_id"],"reason":"ONLY_ELIGIBLE_BRANCH"}
    margin=eligible[0]["accuracy"]-eligible[1]["accuracy"]
    if margin<minimum_accuracy_margin:
        return {"status":"REMAIN_OPEN","winner":None,"reason":"MARGIN_BELOW_GATE","accuracy_margin":margin}
    return {
        "status":"BRANCH_WINNER_CANDIDATE",
        "winner":eligible[0]["branch_id"],
        "runner_up":eligible[1]["branch_id"],
        "accuracy_margin":margin,
        "reason":"FROZEN_REPLAY_MARGIN_PASSED"
    }

def materialize_branch_comparison(parent_id, branches, comparison):
    objects=[
        {"id":parent_id,"type":"META_POLICY","status":"PRESERVED"}
    ]
    relations=[]
    for b in branches:
        objects.append(dict(b))
        relations.append({
            "subject":b["id"],
            "predicate":"BRANCHED_FROM_META_POLICY",
            "object":parent_id
        })
    return {
        "record_type":"META_POLICY_BRANCH_COMPARISON",
        "objects":objects,
        "relations":relations,
        "comparison":comparison,
        "active_policy_mutated":False
    }
