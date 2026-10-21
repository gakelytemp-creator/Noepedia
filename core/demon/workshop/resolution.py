#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WORKSHOP WS03 — D4: a requirement's ASK is answered when the requirement binds.

Status: workshop code. "Works on scene S", not a demonstration claim.

Root cause on GW05: the C1 joint ASK is materialized by the frozen C3 overlay
as OPEN_ASK_n with ORIGIN_WHERE = "candidate/joint-requirement/<RQ>". Its
`missing` is a tuple of patterns, not one triplet, so it gets no
RESOLUTION_PATTERN and resolve_from_fact() can never close it. Binding the RQ
changed the RQ, but nothing told its ASK.

Fix (A2.1, A8.6): a non-destructive status transition OPEN -> ANSWERED with
basis = the binding edge, plus an addressable REFERS_TO edge (role
ANSWERED_BY). Nothing is deleted. The OPEN record, the stop card and the
binding all stay readable. Only the current view changes.

Scope: this is triggered by an explicit bind. Re-evaluating requirements on
every commit (watch semantics, ATTIC 01 O7) is not decided and not done here.
"""
from demon_core import Record, GO

ASK_ORIGIN = "candidate/joint-requirement/{rq}"
ANSWERED = "ANSWERED"


def requirement_ask_opens(net, rq_addr):
    where = ASK_ORIGIN.format(rq=rq_addr)
    return sorted(
        r.addr for r in net.records.values()
        if r.f("TYPE") == "OPEN" and r.f("OPEN_KIND") == "ASK"
        and r.f("ORIGIN_WHERE") == where
        and r.status_log and r.status_log[-1].state == "OPEN")


def answer_on_bind(net, demon, rq_addr, bind_edge_addr):
    """Mark every still-OPEN ASK of rq_addr as ANSWERED by bind_edge_addr."""
    bind = net.read(bind_edge_addr)
    if bind is None or not bind.committed or bind.f("SUBJECT") != rq_addr:
        return []                                   # no committed binding -> nothing to answer
    answered = []
    for a in requirement_ask_opens(net, rq_addr):
        edge = Record(f"{a}_ANSWERED_BY", {"SUBJECT": a, "PREDICATE": "REFERS_TO",
                                           "OBJECT": bind_edge_addr, "ROLE": "ANSWERED_BY"})
        v, _ = demon.commit(demon.propose(
            add=[edge], mark=[(a, ANSWERED, None, None, bind_edge_addr)]))
        if v == GO:
            answered.append(a)
    return answered


def unanswered_ask_stops(net):
    """ASK stop cards whose materialized OPEN_ASK_<idx> is not answered/resolved.

    Stop cards are history and are never removed; this is only a view.
    """
    out = []
    for idx, s in enumerate(net.stops, 1):
        if s.stop_class != "ASK":
            continue
        rec = net.read(f"OPEN_ASK_{idx}")
        if rec is not None and rec.status_log and rec.status_log[-1].state != "OPEN":
            continue
        out.append(s)
    return out
