#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, subprocess, sys, urllib.request, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=json.loads((HERE/"SOURCE.json").read_text(encoding="utf-8"))

CAL_COUNT=50_000
DISC_START=650_001
DISC_COUNT=5_000
CONF_START=700_001
CONF_COUNT=5_000
HISTORY=81
LAGS=[1,2,5,10,20,40,80]
STATE_LOW="STATE_LOW"
STATE_HIGH="STATE_HIGH"

WORK=HERE/"_runtime"
ZIP=WORK/"metropt3.zip"
CSV=WORK/"metropt3.csv"
FIELD=WORK/"confirmation_field.json"
EVAL=WORK/"confirmation_eval.json"
RESULT=WORK/"result.json"
EVALUATOR=ROOT/"experiments"/"experiment_003"/"evaluator.py"

RULE_OLD="RULE037_OLD_DIRECT_EQUALITY"
RULE_NEW="RULE037_SELECTED_REVISED_RULE"


def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def git_blob_sha1(path):
    data=path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8")+data).hexdigest()


def download(url,dest):
    with urllib.request.urlopen(url,timeout=120) as r,dest.open("wb") as out:
        while True:
            b=r.read(1<<20)
            if not b: break
            out.write(b)


def extract_member(zip_path,dest,basename):
    with zipfile.ZipFile(zip_path) as z:
        matches=[n for n in z.namelist() if Path(n).name==basename]
        if len(matches)!=1:
            raise RuntimeError(f"expected one member, got {matches}")
        with z.open(matches[0]) as src,dest.open("wb") as out:
            while True:
                b=src.read(1<<20)
                if not b: break
                out.write(b)


def fit_1d_kmeans(vals):
    c0,c1=min(vals),max(vals)
    for _ in range(100):
        g0=[];g1=[]
        for x in vals:
            (g0 if abs(x-c0)<=abs(x-c1) else g1).append(x)
        n0=sum(g0)/len(g0); n1=sum(g1)/len(g1)
        if abs(n0-c0)<1e-12 and abs(n1-c1)<1e-12:
            c0,c1=n0,n1
            break
        c0,c1=n0,n1
    lo,hi=min(c0,c1),max(c0,c1)
    return lo,hi,(lo+hi)/2


def state(x,threshold):
    return STATE_HIGH if x>threshold else STATE_LOW


def transition_name(prev,curr):
    if prev==STATE_LOW and curr==STATE_HIGH:
        return "LOW_TO_HIGH"
    if prev==STATE_HIGH and curr==STATE_LOW:
        return "HIGH_TO_LOW"
    return None


def load_rows(csv_path):
    max_end=max(DISC_START+DISC_COUNT-1,CONF_START+CONF_COUNT-1)
    min_start=DISC_START-HISTORY
    cal_h1=[];cal_res=[];rows={}

    with csv_path.open("r",encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        needed={"H1","Reservoirs"}
        missing=needed-set(reader.fieldnames or [])
        if missing:
            raise RuntimeError(f"missing columns: {sorted(missing)}")

        for i,row in enumerate(reader,start=1):
            if i<=CAL_COUNT:
                cal_h1.append(float(row["H1"]))
                cal_res.append(float(row["Reservoirs"]))
            if min_start<=i<=max_end:
                rows[i]={"H1":float(row["H1"]),"Reservoirs":float(row["Reservoirs"])}
            if i>max_end:
                break

    return cal_h1,cal_res,rows


def build_series(rows,start,count,h1_thr,res_thr):
    out={}
    for i in range(start-HISTORY,start+count):
        out[i]={
            "H1":state(rows[i]["H1"],h1_thr),
            "Reservoirs":state(rows[i]["Reservoirs"],res_thr)
        }
    return out


def candidate_metrics(series,start,count,source,target,direction,lag):
    last_t=None
    last_dir=None
    prev_source_before_transition=None
    old_mm=0
    new_mm=0
    corrected=0
    introduced=0

    for i in range(start-HISTORY+1,start+count):
        prev=series[i-1][source]
        curr=series[i][source]
        dname=transition_name(prev,curr)
        if dname is not None:
            last_t=i
            last_dir=dname
            prev_source_before_transition=prev

        if i<start:
            continue

        observed=series[i][target]
        old_expected=series[i][source]
        revised_expected=old_expected

        if last_t is not None and last_dir==direction and 0<=i-last_t<=lag:
            revised_expected=prev_source_before_transition

        old_bad=(old_expected!=observed)
        new_bad=(revised_expected!=observed)
        old_mm+=int(old_bad)
        new_mm+=int(new_bad)
        corrected+=int(old_bad and not new_bad)
        introduced+=int((not old_bad) and new_bad)

    return {
        "source":source,
        "target":target,
        "direction":direction,
        "lag":lag,
        "old_mismatches":old_mm,
        "revised_mismatches":new_mm,
        "corrected_old_mismatches":corrected,
        "introduced_new_mismatches":introduced,
        "net_mismatch_reduction":old_mm-new_mm,
        "mismatch_fraction":new_mm/count
    }


def select_candidate(series):
    source_order=["H1","Reservoirs"]
    direction_order=["LOW_TO_HIGH","HIGH_TO_LOW"]
    candidates=[]

    for source in source_order:
        target="Reservoirs" if source=="H1" else "H1"
        for direction in direction_order:
            for lag in LAGS:
                candidates.append(candidate_metrics(
                    series,DISC_START,DISC_COUNT,source,target,direction,lag
                ))

    candidates.sort(key=lambda c:(
        -c["net_mismatch_reduction"],
        c["lag"],
        source_order.index(c["source"]),
        direction_order.index(c["direction"])
    ))
    return candidates[0],candidates


def relation(i,s,p,o,n,prov=None,status="settled"):
    return {
        "id":i,"subject":s,"predicate":p,"object":o,
        "network":n,"status":status,"provenance":prov or []
    }


def add_same_net_rule(rules,prefix,rule_id,input_pred,required_pred):
    rules.extend([
        relation(prefix+"_01",rule_id,"RULE_SCOPE","assessment","NET_RULE"),
        relation(prefix+"_02",rule_id,"INPUT_PREDICATE",input_pred,"NET_RULE"),
        relation(prefix+"_03",rule_id,"REQUIRED_PREDICATE",required_pred,"NET_RULE"),
        relation(prefix+"_04",rule_id,"TARGET_CONSTRAINT","SAME_NET","NET_RULE")
    ])


def build_confirmation_field(series,best):
    source=best["source"]
    target=best["target"]
    direction=best["direction"]
    lag=best["lag"]

    objects=[
        {"id":STATE_LOW,"type":"channel_state"},
        {"id":STATE_HIGH,"type":"channel_state"},
        {"id":RULE_OLD,"type":"consistency_rule"},
        {"id":RULE_NEW,"type":"consistency_rule"},
        {"id":"EXP037_DISCOVERY","type":"evidence"}
    ]

    rels=[
        relation("P037_01",RULE_NEW,"SUPPORTED_BY","EXP037_DISCOVERY","NET_PROVENANCE"),
        relation("P037_02",RULE_NEW,"EPISTEMIC_STATUS","DISCOVERY_SELECTED_RULE","NET_PROVENANCE"),
        relation("P037_03",RULE_NEW,"SOURCE_CHANNEL",source,"NET_PROVENANCE"),
        relation("P037_04",RULE_NEW,"TARGET_CHANNEL",target,"NET_PROVENANCE"),
        relation("P037_05",RULE_NEW,"TRANSITION_DIRECTION",direction,"NET_PROVENANCE"),
        relation("P037_06",RULE_NEW,"LAG_ROWS",str(lag),"NET_PROVENANCE")
    ]

    last_t=None
    last_dir=None
    prev_source_before_transition=None

    for i in range(CONF_START-HISTORY+1,CONF_START+CONF_COUNT):
        prev=series[i-1][source]
        curr=series[i][source]
        dname=transition_name(prev,curr)
        if dname is not None:
            last_t=i
            last_dir=dname
            prev_source_before_transition=prev

        if i<CONF_START:
            continue

        local=i-CONF_START+1
        sid=f"ASSESSMENT_{local:05d}"
        objects.append({"id":sid,"type":"assessment"})

        target_state=series[i][target]
        old_expected=series[i][source]
        revised_expected=old_expected

        if last_t is not None and last_dir==direction and 0<=i-last_t<=lag:
            revised_expected=prev_source_before_transition

        rels.append(relation(
            f"R{local:05d}_OBS",sid,"TARGET_CANDIDATE_STATE",target_state,"NET_STATE"
        ))
        rels.append(relation(
            f"R{local:05d}_OLD",sid,"OLD_EXPECTED_TARGET_STATE",old_expected,"NET_STATE",
            prov=[RULE_OLD]
        ))
        rels.append(relation(
            f"R{local:05d}_NEW",sid,"REVISED_EXPECTED_TARGET_STATE",revised_expected,"NET_STATE",
            prov=[RULE_NEW,"EXP037_DISCOVERY"]
        ))

    rules=[]
    add_same_net_rule(rules,"RULE037OLD",RULE_OLD,"OLD_EXPECTED_TARGET_STATE","TARGET_CANDIDATE_STATE")
    add_same_net_rule(rules,"RULE037NEW",RULE_NEW,"REVISED_EXPECTED_TARGET_STATE","TARGET_CANDIDATE_STATE")

    return {
        "experiment_id":"NOEPEDIA_EXP_037_THIRD_REVISION_LOOP",
        "metadata":{
            "confirmation_start":CONF_START,
            "confirmation_rows":CONF_COUNT,
            "selected_candidate":best
        },
        "objects":objects,
        "networks":["NET_STATE","NET_RULE","NET_PROVENANCE"],
        "relations":rels,
        "rules":rules,
        "open":[{
            "id":"OPEN_037_RELATION_VALIDITY",
            "subject":"H1_RESERVOIRS_DIRECT_EQUALITY",
            "predicate":"DOMAIN_VALIDITY",
            "object":"UNKNOWN_OR_PARTIALLY_REVISED",
            "status":"open",
            "provenance":[RULE_OLD,RULE_NEW,"EXP037_DISCOVERY"]
        }]
    }


def summarize_eval(ev):
    old=[e for e in ev.get("events",[]) if e.get("rule")==RULE_OLD]
    new=[e for e in ev.get("events",[]) if e.get("rule")==RULE_NEW]

    old_mm=sum(e.get("event")=="FORMAL_MISMATCH" for e in old)
    new_mm=sum(e.get("event")=="FORMAL_MISMATCH" for e in new)

    return {
        "old_event_count":len(old),
        "old_mismatches":old_mm,
        "revised_event_count":len(new),
        "revised_mismatches":new_mm
    }


def main():
    WORK.mkdir(exist_ok=True)

    if not ZIP.exists() or sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        download(SOURCE["archive_url"],ZIP)
    if sha256_file(ZIP)!=SOURCE["archive_sha256"]:
        raise RuntimeError("archive SHA mismatch")

    extract_member(ZIP,CSV,SOURCE["csv_member_basename"])

    if git_blob_sha1(EVALUATOR)!=SOURCE["frozen_evaluator"]["git_blob_sha1"]:
        raise RuntimeError("evaluator changed")

    cal_h1,cal_res,rows=load_rows(CSV)
    h1_lo,h1_hi,h1_thr=fit_1d_kmeans(cal_h1)
    res_lo,res_hi,res_thr=fit_1d_kmeans(cal_res)

    discovery_series=build_series(rows,DISC_START,DISC_COUNT,h1_thr,res_thr)
    confirmation_series=build_series(rows,CONF_START,CONF_COUNT,h1_thr,res_thr)

    best,candidates=select_candidate(discovery_series)

    out={
        "experiment":"NOEPEDIA_EXP_037_THIRD_REVISION_LOOP",
        "calibration":{
            "H1":{"low_centroid":h1_lo,"high_centroid":h1_hi,"threshold":h1_thr},
            "Reservoirs":{"low_centroid":res_lo,"high_centroid":res_hi,"threshold":res_thr}
        },
        "discovery":{
            "selected_candidate":best,
            "top_10_candidates":candidates[:10]
        }
    }

    if best["net_mismatch_reduction"]<=0:
        out["result_class"]="NO_DISCOVERY_CANDIDATE"
        RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print(json.dumps(out,indent=2,ensure_ascii=False))
        print("Experiment 037 reproducibility: PASS")
        print("Experiment 037 result: NO_DISCOVERY_CANDIDATE")
        return 0

    field=build_confirmation_field(confirmation_series,best)
    FIELD.write_text(json.dumps(field,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    with EVAL.open("w",encoding="utf-8") as f:
        subprocess.run([sys.executable,str(EVALUATOR),str(FIELD)],check=True,stdout=f)

    ev=json.loads(EVAL.read_text(encoding="utf-8"))
    summary=summarize_eval(ev)

    old_mm=summary["old_mismatches"]
    new_mm=summary["revised_mismatches"]
    net=old_mm-new_mm
    rel=(net/old_mm) if old_mm else 0.0
    confirmed=(new_mm<old_mm and net>0)

    out["confirmation"]={
        **summary,
        "old_mismatch_fraction":old_mm/CONF_COUNT,
        "revised_mismatch_fraction":new_mm/CONF_COUNT,
        "net_mismatch_reduction":net,
        "relative_mismatch_reduction":rel,
        "open_preserved":ev.get("open_records_unchanged")
    }

    out["result_class"]=(
        "THIRD_REVISION_LOOP_CONFIRMED"
        if confirmed else
        "THIRD_REVISION_LOOP_NOT_CONFIRMED"
    )
    out["strong_flag_confirmation_reduction_50_percent"]=rel>=0.50
    out["claim_boundary"]={
        "causality_established":False,
        "physical_truth_established":False
    }

    RESULT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("Experiment 037 reproducibility: PASS")
    print("Experiment 037 architectural result: PASS")
    print("Experiment 037 scientific result:",out["result_class"])
    return 0


if __name__=="__main__":
    raise SystemExit(main())
