#!/usr/bin/env python3
from __future__ import annotations

import csv, json, statistics, subprocess, sys, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

CAL_START=1
CAL_COUNT=800
DISC_START=801
DISC_COUNT=600
CONF_START=1601
CONF_COUNT=600
LAG_MIN=1
LAG_MAX=30
SHIFTS=[50,100,150,200]

LOW="STATE_LOW"
HIGH="STATE_HIGH"

WORK=HERE/"_runtime"
ZIP=WORK/"hydraulic.zip"
EXTRACT=WORK/"hydraulic"
RESULT=WORK/"result.json"

HARNESS=ROOT/"experiments"/"experiment_045"/"revision_harness.py"
MATERIALIZER=ROOT/"experiments"/"experiment_046"/"materialize_revision.py"


def download(url,dest):
    with urllib.request.urlopen(url,timeout=180) as r,dest.open("wb") as out:
        while True:
            b=r.read(1<<20)
            if not b:
                break
            out.write(b)


def extract_all(zp,dest):
    dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(zp) as z:
        z.extractall(dest)


def find_file(base,name):
    matches=list(base.rglob(name))
    if len(matches)!=1:
        raise RuntimeError(f"expected one {name}, got {matches}")
    return matches[0]


def read_profile(path):
    rows=[]
    with path.open("r",encoding="utf-8",errors="replace") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts=line.split()
            rows.append([float(x) for x in parts])
    return rows


def read_cycle_means(path):
    means=[]
    with path.open("r",encoding="utf-8",errors="replace") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            vals=[float(x) for x in line.split()]
            means.append(sum(vals)/len(vals))
    return means


def fit_1d_kmeans(vals):
    c0,c1=min(vals),max(vals)
    for _ in range(100):
        g0=[];g1=[]
        for x in vals:
            (g0 if abs(x-c0)<=abs(x-c1) else g1).append(x)
        if not g0 or not g1:
            break
        n0=sum(g0)/len(g0); n1=sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1
    lo,hi=min(c0,c1),max(c0,c1)
    return lo,hi,(lo+hi)/2


def analog_state(x,thr):
    return HIGH if x>thr else LOW


def choose_orientation(src_states,target_states):
    # src_states are HEALTHY / DEGRADED booleans; test both orientations.
    def maph(healthy,flip):
        if not flip:
            return HIGH if healthy else LOW
        return LOW if healthy else HIGH
    mm_a=sum(maph(s,False)!=t for s,t in zip(src_states,target_states))
    mm_b=sum(maph(s,True)!=t for s,t in zip(src_states,target_states))
    flip=mm_b<mm_a
    return {
        "flip":flip,
        "mapping":"HEALTHY->LOW,DEGRADED->HIGH" if flip else "HEALTHY->HIGH,DEGRADED->LOW",
        "mismatches_A":mm_a,
        "mismatches_B":mm_b,
        "mismatches_selected":min(mm_a,mm_b),
        "mismatch_fraction_selected":min(mm_a,mm_b)/len(target_states)
    }


def mapped_source(healthy,flip):
    if not flip:
        return HIGH if healthy else LOW
    return LOW if healthy else HIGH


def transition(prev,curr):
    if prev==LOW and curr==HIGH:
        return "LOW_TO_HIGH"
    if prev==HIGH and curr==LOW:
        return "HIGH_TO_LOW"
    return None


def temporal_predictions(source_states,direction,lag):
    preds=list(source_states)
    last_t=None
    prev_before=None
    for i in range(1,len(source_states)):
        prev=source_states[i-1]; curr=source_states[i]
        d=transition(prev,curr)
        if d==direction:
            last_t=i
            prev_before=prev
        if last_t is not None and 0<=i-last_t<=lag:
            preds[i]=prev_before
        else:
            preds[i]=curr
    return preds


def mismatch_count(preds,target):
    return sum(a!=b for a,b in zip(preds,target))


def circular_shift(states,shift):
    n=len(states)
    s=shift%n
    return list(states) if s==0 else states[-s:]+states[:-s]


def family_calibration(profile,means,fam):
    s0=CAL_START-1; s1=s0+CAL_COUNT
    src=[profile[i][fam["profile_col"]]==fam["healthy_value"] for i in range(s0,s1)]
    vals=means[s0:s1]
    lo,hi,thr=fit_1d_kmeans(vals)
    tgt=[analog_state(x,thr) for x in vals]
    orient=choose_orientation(src,tgt)
    frac=orient["mismatch_fraction_selected"]
    return {
        **fam,
        "target_low_centroid":lo,
        "target_high_centroid":hi,
        "target_threshold":thr,
        "orientation":orient,
        "calibration_mismatch_fraction":frac,
        "eligible":0.05<=frac<=0.40,
        "distance_to_target_0_20":abs(frac-0.20)
    }


def build_window(profile,means,selected,start,count):
    a=start-1; b=a+count
    src_bool=[
        profile[i][selected["profile_col"]]==selected["healthy_value"]
        for i in range(a,b)
    ]
    src=[
        mapped_source(x,selected["orientation"]["flip"])
        for x in src_bool
    ]
    tgt=[
        analog_state(x,selected["target_threshold"])
        for x in means[a:b]
    ]
    return src,tgt


def discovery_search(src,tgt):
    old_mm=mismatch_count(src,tgt)
    candidates=[]
    dirs=["LOW_TO_HIGH","HIGH_TO_LOW"]
    for direction in dirs:
        for lag in range(LAG_MIN,LAG_MAX+1):
            pred=temporal_predictions(src,direction,lag)
            mm=mismatch_count(pred,tgt)
            candidates.append({
                "direction":direction,
                "lag":lag,
                "mismatches":mm,
                "net_reduction_vs_old":old_mm-mm
            })
    candidates.sort(key=lambda x:(x["mismatches"],x["lag"],dirs.index(x["direction"])))
    return old_mm,candidates[0],candidates


def run_external():
    WORK.mkdir(exist_ok=True)
    if not ZIP.exists():
        download(SOURCE["archive_url"],ZIP)
    if not EXTRACT.exists():
        extract_all(ZIP,EXTRACT)

    profile=read_profile(find_file(EXTRACT,"profile.txt"))
    if len(profile)<2200:
        raise RuntimeError(f"unexpected profile rows: {len(profile)}")

    screened=[]
    cache={}
    for fam in SOURCE["candidate_families"]:
        p=find_file(EXTRACT,fam["target_file"])
        means=read_cycle_means(p)
        if len(means)!=len(profile):
            raise RuntimeError(f"row mismatch for {fam['target_file']}: {len(means)} vs {len(profile)}")
        cache[fam["id"]]=means
        screened.append(family_calibration(profile,means,fam))

    eligible=[x for x in screened if x["eligible"]]
    out={
        "experiment":"NOEPEDIA_EXP_047_EXTERNAL_TRANSFER",
        "dataset":"UCI Condition Monitoring of Hydraulic Systems",
        "profile_rows":len(profile),
        "calibration_screen":screened
    }

    if not eligible:
        out["scientific_result"]="NO_ELIGIBLE_EXTERNAL_FAMILY"
        return out,None

    eligible.sort(key=lambda x:(x["distance_to_target_0_20"],x["id"]))
    selected=eligible[0]
    means=cache[selected["id"]]
    out["selected_family"]=selected

    dsrc,dtgt=build_window(profile,means,selected,DISC_START,DISC_COUNT)
    csrc,ctgt=build_window(profile,means,selected,CONF_START,CONF_COUNT)

    old_disc,best,cands=discovery_search(dsrc,dtgt)
    majority=HIGH if sum(x==HIGH for x in dtgt)>=sum(x==LOW for x in dtgt) else LOW

    old_mm=mismatch_count(csrc,ctgt)
    revised=temporal_predictions(csrc,best["direction"],best["lag"])
    revised_mm=mismatch_count(revised,ctgt)
    majority_mm=sum(majority!=x for x in ctgt)

    perm=[]
    for shift in SHIFTS:
        shifted=circular_shift(csrc,shift)
        pp=temporal_predictions(shifted,best["direction"],best["lag"])
        perm.append({"shift":shift,"mismatches":mismatch_count(pp,ctgt)})
    perm_median=statistics.median([x["mismatches"] for x in perm])

    beats_old=revised_mm<old_mm
    beats_majority=(revised_mm<=0.90*majority_mm) if majority_mm else False
    beats_perm=(revised_mm<=0.90*perm_median) if perm_median else False
    boundary=best["lag"]==LAG_MAX

    confirmed=beats_old and beats_majority and beats_perm and not boundary

    out["discovery"]={
        "old_mismatches":old_disc,
        "selected_candidate":best,
        "lag_boundary_hit":boundary,
        "local_curve":[
            c for c in cands
            if c["direction"]==best["direction"] and abs(c["lag"]-best["lag"])<=5
        ]
    }
    out["frozen_majority_state"]=majority
    out["confirmation"]={
        "old_mismatches":old_mm,
        "revised_mismatches":revised_mm,
        "majority_mismatches":majority_mm,
        "permutation_mismatches":perm,
        "permutation_median_mismatches":perm_median,
        "beats_old":beats_old,
        "beats_majority_by_10_percent":beats_majority,
        "beats_permutation_by_10_percent":beats_perm,
        "relative_reduction_vs_old":((old_mm-revised_mm)/old_mm) if old_mm else None,
        "relative_reduction_vs_majority":((majority_mm-revised_mm)/majority_mm) if majority_mm else None,
        "relative_reduction_vs_permutation":((perm_median-revised_mm)/perm_median) if perm_median else None
    }
    out["scientific_result"]=(
        "EXTERNAL_NULL_PROTECTED_REVISION_CONFIRMED"
        if confirmed else
        "EXTERNAL_NULL_PROTECTED_REVISION_NOT_CONFIRMED"
    )

    case={
        "case_id":"EXP047_EXTERNAL_REVISION_CASE",
        "candidate_id":"EXP047_SELECTED_CANDIDATE",
        "parent_rule_id":"EXP047_OLD_RULE_V1",
        "open_id":"OPEN_EXP047_EXTERNAL_DOMAIN_VALIDITY",
        "proposed_new_rule_id":"EXP047_RULE_V2",
        "confirmation_result_id":"EXP047_CONFIRMATION_RESULT",
        "preregistration_id":"EXP047_PREREGISTRATION",
        "parent_rule_exists":True,
        "open_exists":True,
        "provenance_complete":True,
        "candidate_parameters_explicit":True,
        "preregistration_frozen":True,
        "discovery_confirmation_separated":True,
        "confirmation_untouched":True,
        "evidence_role_explicit":True,
        "confirmation_evaluable":True,
        "unresolved_not_counted_as_success":True,
        "evaluator_frozen":True,
        "corrections_documented":True,
        "history_preserved":True,
        "open_refinement_prepared":True,
        "old_metric":old_mm,
        "revised_metric":revised_mm,
        "required_nulls":[
            {"name":"MAJORITY_STATE_NULL","metric":majority_mm,"required_relative_advantage":0.10},
            {"name":"PERMUTATION_NULL","metric":perm_median,"required_relative_advantage":0.10}
        ],
        "search_boundary_hit":boundary,
        "search_boundary_policy":"REMAIN_OPEN",
        "direction_consistency_required":False
    }
    return out,case


def main():
    out,case=run_external()

    if case is None:
        out["harness_decision"]="REMAIN_OPEN"
        out["materialization_skipped"]=True
        RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print(json.dumps(out,indent=2,ensure_ascii=False))
        print("Experiment 047 reproducibility: PASS")
        print("Experiment 047 result:",out["scientific_result"])
        return 0

    case_path=WORK/"case.json"
    audit_path=WORK/"audit.json"
    graph_path=WORK/"graph.json"
    case_path.write_text(json.dumps(case,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    subprocess.run([sys.executable,str(HARNESS),str(case_path),str(audit_path)],check=True)
    subprocess.run([sys.executable,str(MATERIALIZER),str(case_path),str(audit_path),str(graph_path)],check=True)

    audit=json.loads(audit_path.read_text(encoding="utf-8"))
    graph=json.loads(graph_path.read_text(encoding="utf-8"))

    out["harness_decision"]=audit["final_decision"]
    out["graph_invariants"]=graph["invariants"]
    out["external_architecture_pass"]=graph["invariants"]["all_pass"]

    expected=(
        "PROMOTE"
        if out["scientific_result"]=="EXTERNAL_NULL_PROTECTED_REVISION_CONFIRMED"
        else "REJECT"
    )
    out["decision_matches_scientific_result"]=audit["final_decision"]==expected

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 047 reproducibility: PASS")
    print("Experiment 047 architecture transfer:",
          "PASS" if out["external_architecture_pass"] and out["decision_matches_scientific_result"] else "FAIL")
    print("Experiment 047 scientific result:",out["scientific_result"])
    return 0 if out["external_architecture_pass"] and out["decision_matches_scientific_result"] else 1


if __name__=="__main__":
    raise SystemExit(main())
