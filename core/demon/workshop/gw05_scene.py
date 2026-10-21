#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WORKSHOP scene: GW05 event stream with the A3.1/A3.4 admission pipeline.

GW05 is public (a training scene). This is not a test and makes no fresh-world
claim. The sealed harness run_c/gw05_runner.py is untouched; its helpers are
imported and execute() is copied here with only ingest() and the registry
read-out changed. --admission off reproduces the frozen ingest behaviour.
"""
from pathlib import Path
import argparse, json, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent/"run_c")); sys.path.insert(0,str(HERE))
from gw05_runner import (j, stop_dict, snapshot, delta, add_fact, load_initial, load_rules, rule,
                         materialize_signals, commit_markers, commit_derivation, event,
                         DICT_PATH, ENCODERS, ROOT)
from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED
from family_executor import FamilyExecutor
from c1_c3_overlay import C1C3Overlay
from admission import admit, install_default_policy, PER_RULE_DEBT, PER_FACT_MARKER
from resolution import answer_on_bind, unanswered_ask_stops

def execute(encoder,use_c13,admission,resolve_asks=False,debt_shape=PER_FACT_MARKER):
    net=Network(); demon=Demon(net)
    dictionary=json.loads(DICT_PATH.read_text(encoding="utf-8"))
    ex=FamilyExecutor(dictionary)
    c13=C1C3Overlay(net) if use_c13 else None
    load_initial(net); rules=load_rules(net,ENCODERS[encoder])
    if admission: install_default_policy(net,demon,debt_shape=debt_shape)
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
            if not admission:   # frozen GW05 behaviour, kept for A/B
                commit_markers(net,demon,vr); materialize_signals(net,demon,f"{ev}_{idx}",vr)
                committed=False
                if vr.verdict==GO:
                    v,_=demon.commit(demon.propose(add=[incoming],mark=[(incoming.addr,"CURRENT")]))
                    committed=(v==GO); verdicts.append(v)
                else:
                    net.stop(f"{ev}/{idx}",f"validate incoming ({s} {p} {o})",j(vr.details),
                             j(vr.unchecked_dependencies),vr.verdict)
                    verdicts.append(vr.verdict)
                adm=None
            else:               # workshop: A3.1 + A3.4
                adm=admit(net,demon,incoming,vr,prefix=f"{ev}_{idx}")
                committed=adm.fact_committed; verdicts.append(adm.verdict)
                if adm.verdict!=GO:
                    net.stop(f"{ev}/{idx}",f"admit incoming ({s} {p} {o})",j(adm.evidence),adm.reason,adm.verdict)
            if committed and c13 is not None: c13.resolve_from_fact(incoming)
            results.append({"VALIDATION":j(vr),"COMMITTED":committed,
                            "ADMISSION":None if adm is None else {"VERDICT":adm.verdict,"REASON":adm.reason,
                                "EVIDENCE":j(adm.evidence),"RECORDS":adm.records,"POLICY":adm.policy}})
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
        signals=sorted(r.addr for r in net.records.values()
            if r.f("TYPE") in ("CONFLICT","CHECK_STATUS","UNEXECUTABLE_RULE_DEBT") and r.status_log and r.status_log[-1].state=="OPEN")
        asks=([stop_dict(s) for s in unanswered_ask_stops(net)] if resolve_asks
              else [stop_dict(s) for s in net.stops if s.stop_class==ASK])
        needs=[stop_dict(s) for s in net.stops if s.stop_class==NEED]
        return GO,{"OPEN_REGISTRY":list(opens),"OPEN_SIGNALS":signals,"ASK_UNANSWERED":asks,"NEED":needs}
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
            note={"CANDIDATES":candidates,"BOUND":candidates[0]}
            if resolve_asks and v==GO:   # WS03 / D4
                note["ASKS_ANSWERED"]=answer_on_bind(net,demon,"RQ_F6","RQ_F6_BIND")
            return v,note
        out=c13.requirement_ask("RQ_F6"); c13.materialize_ask_opens()
        return (ASK if candidates or out.created_asks else NEED),{"CANDIDATES":candidates,"C1":j(out)}
    event(events,net,"F11",["READ","MATCH","LINK","MARK"],f11)
    event(events,net,"F12",["READ","OPEN_REGISTRY"],registry)

    return {"GW05_ENCODER":encoder,"C1_C3_ENABLED":use_c13,"ADMISSION_ENABLED":admission,"ASK_RESOLUTION_ENABLED":resolve_asks,"DEBT_SHAPE":debt_shape if admission else None,
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
    ap.add_argument("--admission",choices=["off","on"],required=True)
    ap.add_argument("--resolve-asks",choices=["off","on"],default="off")
    ap.add_argument("--debt-shape",choices=["fact","rule"],default="fact")
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    out=execute(a.encoder,a.c13=="on",a.admission=="on",a.resolve_asks=="on",
              PER_RULE_DEBT if a.debt_shape=="rule" else PER_FACT_MARKER)
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
