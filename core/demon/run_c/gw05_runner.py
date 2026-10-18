#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GW05 deterministic post-translation run harness.

This harness does not modify the frozen executor, dictionary, or C1/C3 code.
It mechanically transcribes the public GW05 event stream and exposes raw
HandlerResult objects in the log. Candidate-off/on runs keep C1/C3 attribution
separate.
"""
from pathlib import Path
from dataclasses import asdict, is_dataclass
import argparse, json, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/"core/demon"))
sys.path.insert(0,str(HERE))

from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED
from family_executor import FamilyExecutor
from c1_c3_overlay import C1C3Overlay

DICT_PATH=ROOT/"current/experiments/GW05_RUN_C_FAMILY_DICTIONARY.json"
ENCODERS={
 "N":ROOT/"current/experiments/GW05_N_ENCODER_OUTPUT.normalized.json",
 "L":ROOT/"current/experiments/GW05_L_ENCODER_OUTPUT.json",
}

def j(x):
    if is_dataclass(x): return j(asdict(x))
    if isinstance(x,Record):
        return {"addr":x.addr,"fields":j(x.fields),"status":[j(s) for s in x.status_log],"committed":x.committed}
    if isinstance(x,dict): return {str(k):j(v) for k,v in x.items()}
    if isinstance(x,(list,tuple,set)): return [j(v) for v in x]
    return x

def stop_dict(s):
    return {"WHERE":s.where,"WANTED":s.wanted,"AVAILABLE":j(s.available),"MISSING":j(s.missing),
            "STOP_CLASS":s.stop_class,"CAN_ASK_OUTSIDE":s.can_ask_outside,"QUERY":s.query}

def snapshot(net):
    return {a:(repr(r.fields),[(s.state,s.scope,s.time,s.basis,s.seq) for s in r.status_log],r.committed)
            for a,r in net.records.items()}

def delta(before,net):
    after=snapshot(net)
    return {"CREATED":sorted(a for a in after if a not in before),
            "CHANGED":sorted(a for a in after if a in before and after[a]!=before[a])}

def add_fact(net,addr,s,p,o,source="SRC_INIT",time=None):
    fields={"SUBJECT":s,"PREDICATE":p,"OBJECT":o,"PROVENANCE":source}
    if time is not None: fields["TIME"]=time
    r=Record(addr,fields); net.records[addr]=r; r.committed=True
    net.mark(addr,"SUPPORTED"); net.mark(addr,"CURRENT")
    return r

def load_initial(net):
    rows=[
      ("D1","I1","R1","B1"),("D2","I2","R1","B1"),("D3","I3","R1","B1"),
      ("D4","I4","R1","B2"),("D5","I5","R1","B2"),("D6","I6","R1","B3"),
      ("D7","B1","R3",12),("D8","B2","R3",9),("D9","I1","R2",5),
      ("D10","I2","R2",4),("D11","I4","R2",6),("D12","I1","R7","G1"),
      ("D13","I1","R7","G2"),("D14","I1","R7","G3"),("D15","I2","R7","G2"),
      ("D16","I2","R7","G4"),("D17","I3","R5","V1"),("D18","I4","R6","S1")]
    for r in rows: add_fact(net,*r)

def load_rules(net,path):
    data=json.loads(path.read_text(encoding="utf-8"))
    for rd in data:
        fields=dict(rd); addr=fields.pop("addr")
        rec=Record(addr,{"TYPE":"RULE",**fields}); net.records[addr]=rec; rec.committed=True; net.mark(addr,"CURRENT")
    return [r["addr"] for r in data]

def rule(net,addr): return net.read(addr)

def materialize_signals(net,demon,event,result):
    made=[]
    for i,o in enumerate(result.opens,1):
        a=f"OPEN_{event}_{i}"
        if net.read(a) is None:
            rec=Record(a,{"TYPE":"OPEN","ORIGIN":event,"DETAILS":j(o)})
            demon.commit(demon.propose(add=[rec],mark=[(a,"OPEN")]))
            made.append(a)
    for i,c in enumerate(result.conflicts,1):
        a=f"CONFLICT_{event}_{i}"
        if net.read(a) is None:
            rec=Record(a,{"TYPE":"CONFLICT","ORIGIN":event,"DETAILS":j(c)})
            demon.commit(demon.propose(add=[rec],mark=[(a,"OPEN")]))
            made.append(a)
    for st in result.stops:
        net.stop(f"{event}/handler",event,j(st),"handler stop",result.verdict,
                 can_ask=(result.verdict==ASK),query="")
    return made

def commit_markers(net,demon,result):
    made=[]
    for rec in result.proposed_delta:
        if isinstance(rec,Record) and net.read(rec.addr) is None:
            demon.commit(demon.propose(add=[rec]))
            made.append(rec.addr)
    return made

def commit_derivation(net,demon,result,event):
    if not result.derived_records: return []
    made=[]
    for rec in result.derived_records:
        refs=[]
        for i,target in enumerate(result.provenance_requirements,1):
            refs.append(Record(f"{rec.addr}_REF{i}",{"SUBJECT":rec.addr,"PREDICATE":"REFERS_TO",
                                                    "OBJECT":target,"ROLE":"PREMISE_OR_RULE"}))
        premises=[x for x in result.provenance_requirements if x!=result.provenance_requirements[-1]]
        used_rule=result.provenance_requirements[-1] if result.provenance_requirements else None
        derived=[(rec.addr,premises,used_rule)] if used_rule else []
        v,_=demon.commit(demon.propose(add=[rec]+refs,mark=[(rec.addr,"CURRENT")],derived=derived))
        if v==GO: made.append(rec.addr)
    return made

def event(log,net,name,ops,fn):
    before=snapshot(net); n=len(net.stops)
    verdict,note=fn()
    log.append({"EVENT":name,"OPERATIONS":ops,"VERDICT":verdict,"NOTE":j(note),
                "NETWORK_DELTA":delta(before,net),
                "STOPS":[stop_dict(s) for s in net.stops[n:]],
                "NEED":[stop_dict(s) for s in net.stops[n:] if s.stop_class==NEED]})

def execute(encoder,use_c13):
    net=Network(); demon=Demon(net)
    dictionary=json.loads(DICT_PATH.read_text(encoding="utf-8"))
    ex=FamilyExecutor(dictionary)
    c13=C1C3Overlay(net) if use_c13 else None
    load_initial(net); rules=load_rules(net,ENCODERS[encoder])
    events=[]

    def derive(ev,subject,pred):
        res=ex.execute(rule(net,"M2"),net,{"OP":"DERIVE","SCOPE":"B1" if subject=="I3" else "B2",
                                          "SUBJECT":subject,"PREDICATE":pred,"DERIVED_ADDR":f"{ev}_DERIVED"})
        commit_markers(net,demon,res); materialize_signals(net,demon,ev,res)
        committed=commit_derivation(net,demon,res,ev)
        if res.verdict!=GO:
            net.stop(f"{ev}/derive",f"determine {pred} of {subject}",j(res.details),
                     res.classification or "executable derivation",NEED)
        return res.verdict,{"HANDLER_RESULT":j(res),"COMMITTED_DERIVED":committed}
    event(events,net,"F1",["READ","MATCH","DERIVE"],lambda:derive("F1","I3","R2"))
    event(events,net,"F2",["READ","MATCH","DERIVE"],lambda:derive("F2","I5","R2"))

    def f3():
        res=ex.execute(rule(net,"M1"),net,{"OP":"CHECK","SUBJECT":"I2"})
        commit_markers(net,demon,res); made=materialize_signals(net,demon,"F3",res)
        return res.verdict,{"HANDLER_RESULT":j(res),"MATERIALIZED":made}
    event(events,net,"F3",["READ","CHECK"],f3)

    def ingest(ev,rows):
        results=[]; verdicts=[]
        for idx,(s,p,o,source,time) in enumerate(rows,1):
            incoming=Record(f"{ev}_IN_{idx}",{"SUBJECT":s,"PREDICATE":p,"OBJECT":o,
                                              "TYPE":"OBSERVATION","SOURCE":source,"TIME":time})
            vr=ex.validate_incoming(net,incoming,marker_prefix=f"{ev}_UNCHECKED_{idx}")
            commit_markers(net,demon,vr); materialize_signals(net,demon,f"{ev}_{idx}",vr)
            committed=False
            if vr.verdict==GO:
                v,_=demon.commit(demon.propose(add=[incoming],mark=[(incoming.addr,"CURRENT")]))
                committed=(v==GO); verdicts.append(v)
                if committed and c13 is not None: c13.resolve_from_fact(incoming)
            else:
                net.stop(f"{ev}/{idx}",f"validate incoming ({s} {p} {o})",j(vr.details),
                         j(vr.unchecked_dependencies),vr.verdict)
                verdicts.append(vr.verdict)
            results.append({"VALIDATION":j(vr),"COMMITTED":committed})
        verdict=BLOCK if BLOCK in verdicts else NEED if NEED in verdicts else ASK if ASK in verdicts else GO
        return verdict,results

    event(events,net,"F4",["PROPOSE","CHECK","COMMIT"],lambda:ingest("F4",[("I3","R6","S2","SRC1","t1")]))

    def f5():
        net.stop("F5/task","determine largest R2 among known items",
                 "current records are addressable","frozen aggregate-max task operator",NEED)
        return NEED,{"CLASS":"EXECUTOR_HOLE","REASON":"no frozen aggregate-max task operator"}
    event(events,net,"F5",["READ","AGGREGATE_MAX"],f5)

    patterns=[("?X","R7","G1"),("?X","R7","G4")]
    def f6():
        p_addrs=[]
        for i,(s,p,o) in enumerate(patterns,1):
            a=f"F6_PAT{i}"; p_addrs.append(a)
            rec=Record(a,{"TYPE":"TRIPLET_PATTERN","SUBJECT":s,"PREDICATE":p,"OBJECT":o})
            demon.commit(demon.propose(add=[rec]))
        task=Record("TASK_F6",{"TYPE":"TASK","REQUIRED_PATTERNS":p_addrs})
        demon.commit(demon.propose(add=[task]))
        rq=Record("RQ_F6",{"TYPE":"REQUIREMENT_CONCEPT","REQUIREMENT":p_addrs})
        v,_=demon.commit(demon.propose(add=[rq],mark=[("RQ_F6","OPEN")],authorized_by="TASK_F6"))
        note={"RQ_COMMIT":v}
        if c13 is not None:
            out=c13.requirement_ask("RQ_F6"); note["C1"]=j(out)
            c13.materialize_ask_opens()
            return (ASK if out.created_asks else v),note
        net.stop("F6/requirement","satisfy joint requirement","requirement concept created",
                 "C1 joint-support mechanism disabled in base run",NEED)
        return NEED,note
    event(events,net,"F6",["CREATE_ADDRESS","MATCH","LINK","MARK"],f6)

    event(events,net,"F7",["PROPOSE","CHECK","COMMIT"],lambda:ingest("F7",[("I5","R2",3,"SRC2","t2")]))
    event(events,net,"F8",["PROPOSE","CHECK","COMMIT"],lambda:ingest("F8",[
        ("I7","R1","B2","SRC3","t3"),("I7","R2",2,"SRC3","t3")]))

    def registry():
        opens=(c13.current_open_registry() if c13 is not None else tuple(sorted(
            r.addr for r in net.records.values()
            if r.f("TYPE")=="OPEN" and r.status_log and r.status_log[-1].state=="OPEN")))
        asks=[stop_dict(s) for s in net.stops if s.stop_class==ASK]
        needs=[stop_dict(s) for s in net.stops if s.stop_class==NEED]
        return GO,{"OPEN_REGISTRY":list(opens),"ASK_UNANSWERED":asks,"NEED":needs}
    event(events,net,"F9",["READ","OPEN_REGISTRY"],registry)

    event(events,net,"F10",["PROPOSE","CHECK","COMMIT"],lambda:ingest("F10",[
        ("I8","R7","G1","SRC4","t4"),("I8","R7","G4","SRC4","t4"),("I8","R7","G2","SRC4","t4")]))

    def f11():
        if c13 is None:
            net.stop("F11/requirement","revisit F6 need","RQ_F6 remains addressable",
                     "C1 joint-support mechanism disabled in base run",NEED)
            return NEED,{"C1":"disabled"}
        branches=c13.joint_bindings(patterns)
        candidates=[]
        for b,_ in branches:
            x=b.get("?X")
            if x not in candidates: candidates.append(x)
        if len(candidates)==1:
            edge=Record("RQ_F6_BIND",{"SUBJECT":"RQ_F6","PREDICATE":"REFERS_TO",
                                     "OBJECT":candidates[0],"ROLE":"BOUND_CANDIDATE"})
            v,_=demon.commit(demon.propose(add=[edge],mark=[("RQ_F6","BOUND")]))
            return v,{"CANDIDATES":candidates,"BOUND":candidates[0]}
        out=c13.requirement_ask("RQ_F6"); c13.materialize_ask_opens()
        return (ASK if candidates or out.created_asks else NEED),{"CANDIDATES":candidates,"C1":j(out)}
    event(events,net,"F11",["READ","MATCH","LINK","MARK"],f11)
    event(events,net,"F12",["READ","OPEN_REGISTRY"],registry)

    return {"GW05_ENCODER":encoder,"C1_C3_ENABLED":use_c13,
            "ENCODER_INPUT":str(ENCODERS[encoder].relative_to(ROOT)),
            "FROZEN_DICTIONARY":str(DICT_PATH.relative_to(ROOT)),
            "RULES":rules,"EVENTS":events,
            "FINAL":{"OPEN_REGISTRY":registry()[1]["OPEN_REGISTRY"],
                     "STOP_MAP":[stop_dict(s) for s in net.stops],
                     "UNCHECKED_RECORDS":sorted(r.addr for r in net.records.values()
                                                if r.f("TYPE")=="CHECK_STATUS" and r.f("STATUS")=="UNCHECKED")}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--encoder",choices=["N","L"],required=True)
    ap.add_argument("--c13",choices=["off","on"],required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    out=execute(a.encoder,a.c13=="on")
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
