#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, statistics, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

CAL_COUNT=50_000
DISC_START=850_001
DISC_COUNT=5_000
CONF_START=900_001
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
    cal_res=[]
    cal_ps=[]
    rows={}
    min_start=DISC_START-HISTORY
    max_end=CONF_START+CONF_COUNT-1

    with CSV.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        needed={"Pressure_switch","Reservoirs"}
        missing=needed-set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing columns: {sorted(missing)}")

        for i,row in enumerate(reader,start=1):
            ps=int(float(row["Pressure_switch"]))
            res=float(row["Reservoirs"])

            if i<=CAL_COUNT:
                cal_ps.append(ps)
                cal_res.append(res)

            if min_start<=i<=max_end:
                rows[i]={"ps":ps,"res":res}

            if i>max_end:
                break

    return cal_ps,cal_res,rows


def choose_orientation(cal_ps,cal_res,res_thr):
    target=[state(x,res_thr) for x in cal_res]

    def mapped(ps,flip):
        if not flip:
            return HIGH if ps==1 else LOW
        return LOW if ps==1 else HIGH

    mm_a=sum(mapped(ps,False)!=t for ps,t in zip(cal_ps,target))
    mm_b=sum(mapped(ps,True)!=t for ps,t in zip(cal_ps,target))

    flip=(mm_b<mm_a)
    return {
        "mapping":"0->HIGH,1->LOW" if flip else "0->LOW,1->HIGH",
        "flip":flip,
        "calibration_mismatches_mapping_A":mm_a,
        "calibration_mismatches_mapping_B":mm_b
    }


def map_ps(ps,flip):
    if not flip:
        return HIGH if ps==1 else LOW
    return LOW if ps==1 else HIGH


def build_series(rows,start,count,res_thr,flip):
    out={}
    for i in range(start-HISTORY,start+count):
        out[i]={
            "source":map_ps(rows[i]["ps"],flip),
            "target":state(rows[i]["res"],res_thr)
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

    candidates=[]
    directions=["LOW_TO_HIGH","HIGH_TO_LOW"]

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
    if s==0:
        return list(states)
    return states[-s:]+states[:-s]


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

    cal_ps,cal_res,rows=load_data()
    res_lo,res_hi,res_thr=fit_1d_kmeans(cal_res)
    orient=choose_orientation(cal_ps,cal_res,res_thr)

    discovery=build_series(rows,DISC_START,DISC_COUNT,res_thr,orient["flip"])
    confirmation=build_series(rows,CONF_START,CONF_COUNT,res_thr,orient["flip"])

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

    source_states=[
        confirmation[i]["source"]
        for i in range(CONF_START,CONF_START+CONF_COUNT)
    ]
    target_states=[
        confirmation[i]["target"]
        for i in range(CONF_START,CONF_START+CONF_COUNT)
    ]

    perm=[]
    for shift in SHIFTS:
        shifted=circular_shift_states(source_states,shift)
        pp=temporal_predictions_from_states(
            shifted,best["direction"],best["lag"]
        )
        mm=sum(pp[j]!=target_states[j] for j in range(CONF_COUNT))
        perm.append({"shift":shift,"mismatches":mm})

    perm_median=statistics.median([x["mismatches"] for x in perm])

    beats_old=revised_mm<old_mm
    beats_majority=(revised_mm<=0.90*majority_mm) if majority_mm>0 else False
    beats_perm=(revised_mm<=0.90*perm_median) if perm_median>0 else False
    boundary=(best["lag"]==LAG_MAX)

    passed=beats_old and beats_majority and beats_perm and not boundary

    old_frac=old_mm/CONF_COUNT

    out={
        "experiment":"NOEPEDIA_EXP_039_NULL_PROTECTED_REVISION_ATTEMPT",
        "calibration":{
            "Reservoirs":{
                "low_centroid":res_lo,
                "high_centroid":res_hi,
                "threshold":res_thr
            },
            "Pressure_switch_orientation":orient
        },
        "discovery":{
            "old_mismatches":old_disc_mm,
            "selected_candidate":best,
            "lag_boundary_hit":boundary,
            "local_curve":[
                c for c in candidates
                if c["direction"]==best["direction"] and abs(c["lag"]-best["lag"])<=10
            ]
        },
        "frozen_majority_state":majority,
        "confirmation":{
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
        },
        "result_class":"NULL_PROTECTED_REVISION_CONFIRMED" if passed else "NULL_PROTECTED_REVISION_NOT_CONFIRMED",
        "claim_boundary":{
            "causality_established":False,
            "physical_independence_established":False
        }
    }

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 039 reproducibility: PASS")
    print("Experiment 039 result:",out["result_class"])
    return 0


if __name__=="__main__":
    raise SystemExit(main())
