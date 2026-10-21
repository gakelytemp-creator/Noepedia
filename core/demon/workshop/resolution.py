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


def _latest(net, addr):
    r = net.read(addr)
    return r.status_log[-1].state if r is not None and r.status_log else None


def effective_ask_state(net, ask_addr):
    """WS08: an ASK's state is read through its support, not only its last stored status.

    ANSWERED holds only while what answered it still stands:
      * answered by a binding  -> the binding's support graph must be SUPPORTED;
      * answered by a candidacy or another record -> that record must be CURRENT.
    A binding with no recorded SUPPORTED_BY edges (pre-WS07 shape) keeps the
    stored status: there is no support graph to read.
    """
    stored = _latest(net, ask_addr)
    from watch import binding_state, supersession_holds   # local import: watch does not import us
    for r in net.records.values():                     # superseded while the supersession's own basis holds
        if r.f("OBJECT") == ask_addr and r.f("ROLE") == "SUPERSEDES" and supersession_holds(net, r):
            return "SUPERSEDED"
    rec = net.read(ask_addr)
    origin = rec.f("ORIGIN_WHERE", "") if rec is not None else ""
    if stored == "OPEN" and origin.startswith("candidate/ambiguity/"):
        basis = origin.split("/", 2)[2]               # the ambiguity record that raised this ASK
        if _latest(net, basis) != "OPEN":
            return "OBSOLETE"                          # its question no longer exists
    if stored != ANSWERED:
        return stored
    answers = [r.f("OBJECT") for r in net.records.values()
               if r.f("SUBJECT") == ask_addr and r.f("ROLE") == "ANSWERED_BY"]
    for a in answers:
        rec = net.read(a)
        if rec is not None and rec.f("ROLE") == "BOUND_CANDIDATE":
            st = binding_state(net, a)
            if st in ("SUPPORTED", "UNSUPPORTED"):
                return ANSWERED
        elif _latest(net, a) == "CURRENT":
            return ANSWERED
    return "OPEN_BY_SUPPORT_LOSS" if answers else ANSWERED


def effectively_open_asks(net):
    """ASKs whose effective state is open (OPEN or OPEN_BY_SUPPORT_LOSS); SUPERSEDED ones excluded."""
    return sorted(r.addr for r in net.records.values()
                  if r.f("TYPE") == "OPEN" and r.f("OPEN_KIND") == "ASK"
                  and effective_ask_state(net, r.addr) in ("OPEN", "OPEN_BY_SUPPORT_LOSS"))


def unanswered_ask_stops(net):
    """ASK stop cards whose materialized OPEN_ASK_<idx> is effectively open.

    Stop cards are history and are never removed; this is only a view.
    """
    out = []
    for idx, s in enumerate(net.stops, 1):
        if s.stop_class != "ASK":
            continue
        rec = net.read(f"OPEN_ASK_{idx}")
        if rec is not None and effective_ask_state(net, rec.addr) not in ("OPEN", "OPEN_BY_SUPPORT_LOSS"):
            continue
        out.append(s)
    return out
