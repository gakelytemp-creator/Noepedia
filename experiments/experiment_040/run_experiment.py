#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, statistics, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

CAL_COUNT=50_000
DISC_START=950_001
DISC_COUNT=5_000
CONF_START=1_000_001
CONF_COUNT=5_000
HISTORY=401
LAG_MIN=1
LAG_MAX=400
SHIFTS=[500,1000,1500,2000]
LOW="STATE_LOW"
HIGH="STATE_HIGH"

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
RESULT=WORK/"result.json"

FAMILIES=[
    {"id":"F1","source":"DV_pressure","target":"TP2"},
    {"id":"F2","source":"COMP","target":"Motor_current"},
    {"id":"F3","source":"Towers","target":"TP3"},
    {"id":"F4","source":"LPS","target":"Reservoirs"},
]


def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def download(url,dest):
    with urllib.request.urlopen(url,timeout=120) as r,dest.open("wb") as out:
        while True:
            b=r.read(1<<20)
            if not b:
                break
            out.write(b)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        matches=[n for n in z.namelist() if Path(n).name==basename]
        if len(matches)!=1:
            raise RuntimeError(f"expected one member, got {matches}")
        with z.open(matches[0]) as src,dest.open("wb") as out:
            while True:
                b=src.read(1<<20)
                if not b:
                    break
                out.write(b)


def fit_1d_kmeans(vals):
    c0,c1=min(vals),max(vals)
    for _ in range(100):
        g0=[]; g1=[]
        for x in vals:
            (g0 if abs(x-c0)<=abs(x-c1) else g1).append(x)
        if not g0 or not g1:
            return min(vals),max(vals),(min(vals)+max(vals))/2
        n0=sum(g0)/len(g0)
        n1=sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1
    lo,hi=min(c0,c1),max(c0,c1)
    return lo,hi,(lo+hi)/2


def state(x,thr):
    return HIGH if x>thr else LOW


def load_data():
    needed=set()
    for f in FAMILIES:
        needed.add(f["source"])
        needed.add(f["target"])

    cal={c:[] for c in needed}
    rows={}
    min_start=DISC_START-HISTORY
    max_end=CONF_START+CONF_COUNT-1

    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        missing=needed-set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing columns: {sorted(missing)}")

        for i,row in enumerate(reader,start=1):
            if i<=CAL_COUNT:
                for c in needed:
                    cal[c].append(float(row[c]))
            if min_start<=i<=max_end:
                rows[i]={c:float(row[c]) for c in needed}
            if i>max_end:
                break

    return cal,rows


def choose_orientation(source_vals,target_states):
    def map_source(x,flip):
        b=1 if x>=0.5 else 0
        if not flip:
            return HIGH if b==1 else LOW
        return LOW if b==1 else HIGH

    mm_a=sum(map_source(x,False)!=t for x,t in zip(source_vals,target_states))
    mm_b=sum(map_source(x,True)!=t for x,t in zip(source_vals,target_states))
    flip=(mm_b<mm_a)
    return {
        "flip":flip,
        "mapping":"0->HIGH,1->LOW" if flip else "0->LOW,1->HIGH",
        "mismatches_A":mm_a,
        "mismatches_B":mm_b,
        "mismatches_selected":min(mm_a,mm_b),
        "mismatch_fraction_selected":min(mm_a,mm_b)/len(target_states)
    }


def calibration_screen(cal):
    screened=[]
    for idx,fam in enumerate(FAMILIES):
        target_vals=cal[fam["target"]]
        lo,hi,thr=fit_1d_kmeans(target_vals)
        target_states=[state(x,thr) for x in target_vals]
        orient=choose_orientation(cal[fam["source"]],target_states)
        frac=orient["mismatch_fraction_selected"]
        eligible=0.05<=frac<=0.40
        screened.append({
            **fam,
            "order":idx,
            "target_low_centroid":lo,
            "target_high_centroid":hi,
            "target_threshold":thr,
            "orientation":orient,
            "calibration_mismatch_fraction":frac,
            "eligible":eligible,
            "distance_to_target_0_20":abs(frac-0.20)
        })
    elig=[x for x in screened if x["eligible"]]
    if not elig:
        return screened,None
    elig.sort(key=lambda x:(x["distance_to_target_0_20"],x["order"]))
    return screened,elig[0]


def map_source_value(x,flip):
    b=1 if x>=0.5 else 0
    if not flip:
        return HIGH if b==1 else LOW
    return LOW if b==1 else HIGH


def build_series(rows,start,count,selected):
    out={}
    src=selected["source"]
    tgt=selected["target"]
    flip=selected["orientation"]["flip"]
    thr=selected["target_threshold"]

    for i in range(start-HISTORY,start+count):
        out[i]={
            "source":map_source_value(rows[i][src],flip),
            "target":state(rows[i][tgt],thr)
        }
    return out


def transition(prev,curr):
    if prev==LOW and curr==HIGH:
        return "LOW_TO_HIGH"
    if prev==HIGH and curr==LOW:
        return "HIGH_TO_LOW"
    return None


def temporal_predictions(series,start,count,direction,lag):
    preds={}
    last_t=None
    prev_before=None

    for i in range(start-HISTORY+1,start+count):
        prev=series[i-1]["source"]
        curr=series[i]["source"]
        d=transition(prev,curr)
        if d==direction:
            last_t=i
            prev_before=prev

        if i<start:
            continue

        expected=curr
        if last_t is not None and 0<=i-last_t<=lag:
            expected=prev_before
        preds[i]=expected

    return preds


def mismatch_count(series,start,count,preds):
    return sum(preds[i]!=series[i]["target"] for i in range(start,start+count))


def old_predictions(series,start,count):
    return {i:series[i]["source"] for i in range(start,start+count)}


def discovery_search(series):
    old=old_predictions(series,DISC_START,DISC_COUNT)
    old_mm=mismatch_count(series,DISC_START,DISC_COUNT,old)
    directions=["LOW_TO_HIGH","HIGH_TO_LOW"]
    candidates=[]

    for direction in directions:
        for lag in range(LAG_MIN,LAG_MAX+1):
            preds=temporal_predictions(series,DISC_START,DISC_COUNT,direction,lag)
            mm=mismatch_count(series,DISC_START,DISC_COUNT,preds)
            candidates.append({
                "direction":direction,
                "lag":lag,
                "mismatches":mm,
                "net_reduction_vs_old":old_mm-mm
            })

    candidates.sort(key=lambda c:(
        c["mismatches"],
        c["lag"],
        directions.index(c["direction"])
    ))
    return old_mm,candidates[0],candidates


def majority_state(series,start,count):
    vals=[series[i]["target"] for i in range(start,start+count)]
    high=sum(v==HIGH for v in vals)
    low=count-high
    return HIGH if high>=low else LOW


def circular_shift_states(states,shift):
    n=len(states)
    s=shift % n
    return list(states) if s==0 else states[-s:]+states[:-s]


def temporal_predictions_from_states(source_states,direction,lag):
    n=len(source_states)
    transition_points=[]
    for i in range(n):
        prev=source_states[(i-1)%n]
        curr=source_states[i]
        if transition(prev,curr)==direction:
            transition_points.append((i,prev))

    preds=list(source_states)
    if not transition_points:
        return preds

    for i in range(n):
        best=None
        best_prev=None
        for t,prev_before in transition_points:
            d=(i-t)%n
            if best is None or d<best:
                best=d
                best_prev=prev_before
        if best is not None and best<=lag:
            preds[i]=best_prev
    return preds


def main():
    WORK.mkdir(exist_ok=True)

    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")
    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    cal,rows=load_data()
    screened,selected=calibration_screen(cal)

    out={
        "experiment":"NOEPEDIA_EXP_040_CALIBRATION_SELECTED_NULL_PROTECTED_REVISION",
        "calibration_screen":screened
    }

    if selected is None:
        out["result_class"]="NO_ELIGIBLE_FAMILY"
        RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print(json.dumps(out,indent=2,ensure_ascii=False))
        print("Experiment 040 reproducibility: PASS")
        print("Experiment 040 result: NO_ELIGIBLE_FAMILY")
        return 0

    out["selected_family"]={
        k:v for k,v in selected.items()
        if k not in {"order","distance_to_target_0_20"}
    }

    discovery=build_series(rows,DISC_START,DISC_COUNT,selected)
    confirmation=build_series(rows,CONF_START,CONF_COUNT,selected)

    old_disc_mm,best,candidates=discovery_search(discovery)
    majority=majority_state(discovery,DISC_START,DISC_COUNT)

    old_preds=old_predictions(confirmation,CONF_START,CONF_COUNT)
    revised_preds=temporal_predictions(
        confirmation,CONF_START,CONF_COUNT,best["direction"],best["lag"]
    )

    old_mm=mismatch_count(confirmation,CONF_START,CONF_COUNT,old_preds)
    revised_mm=mismatch_count(confirmation,CONF_START,CONF_COUNT,revised_preds)

    majority_mm=sum(
        majority!=confirmation[i]["target"]
        for i in range(CONF_START,CONF_START+CONF_COUNT)
    )

    source_states=[confirmation[i]["source"] for i in range(CONF_START,CONF_START+CONF_COUNT)]
    target_states=[confirmation[i]["target"] for i in range(CONF_START,CONF_START+CONF_COUNT)]

    perm=[]
    for shift in SHIFTS:
        shifted=circular_shift_states(source_states,shift)
        pp=temporal_predictions_from_states(shifted,best["direction"],best["lag"])
        mm=sum(pp[j]!=target_states[j] for j in range(CONF_COUNT))
        perm.append({"shift":shift,"mismatches":mm})

    perm_median=statistics.median([x["mismatches"] for x in perm])

    beats_old=revised_mm<old_mm
    beats_majority=(revised_mm<=0.90*majority_mm) if majority_mm>0 else False
    beats_perm=(revised_mm<=0.90*perm_median) if perm_median>0 else False
    boundary=(best["lag"]==LAG_MAX)
    passed=beats_old and beats_majority and beats_perm and not boundary

    out["discovery"]={
        "old_mismatches":old_disc_mm,
        "selected_candidate":best,
        "lag_boundary_hit":boundary,
        "local_curve":[
            c for c in candidates
            if c["direction"]==best["direction"] and abs(c["lag"]-best["lag"])<=10
        ]
    }
    out["frozen_majority_state"]=majority
    old_frac=old_mm/CONF_COUNT
    out["confirmation"]={
        "old_mismatches":old_mm,
        "old_mismatch_fraction":old_frac,
        "old_near_chance_balance":0.45<=old_frac<=0.55,
        "revised_mismatches":revised_mm,
        "majority_mismatches":majority_mm,
        "permutation_mismatches":perm,
        "permutation_median_mismatches":perm_median,
        "relative_reduction_vs_old":((old_mm-revised_mm)/old_mm) if old_mm else None,
        "relative_reduction_vs_majority":((majority_mm-revised_mm)/majority_mm) if majority_mm else None,
        "relative_reduction_vs_permutation_median":((perm_median-revised_mm)/perm_median) if perm_median else None,
        "beats_old":beats_old,
        "beats_majority_by_10_percent":beats_majority,
        "beats_permutation_by_10_percent":beats_perm
    }
    out["result_class"]="NULL_PROTECTED_REVISION_CONFIRMED" if passed else "NULL_PROTECTED_REVISION_NOT_CONFIRMED"
    out["claim_boundary"]={
        "causality_established":False,
        "physical_independence_established":False
    }

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 040 reproducibility: PASS")
    print("Experiment 040 result:",out["result_class"])
    return 0


if __name__=="__main__":
    raise SystemExit(main())
