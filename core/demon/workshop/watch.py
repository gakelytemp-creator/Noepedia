#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WORKSHOP WS07 — watch, candidacy, mandate, bind (ATTIC 01 §12).

    COMMIT -> WATCH -> SOLE_KNOWN_CANDIDATE_ON(N, scope, method)
           -> mandate check -> optional BIND (SUPPORTED_BY candidacy)

* watch_requirement(): discovery. Runs after a commit. Monotone reading of the
  current facts; writes a candidacy record (class 2, carries N). If the
  candidate set changes, old candidacy records become HISTORICAL (never deleted).
* issue_mandate(): authority is a separate record (A12.7). The issuer may not
  be the operation it authorizes (A12.8, DCT09). Lifecycle is fixed at issue
  (A12.9): ONE_SHOT (default) or STANDING_WHILE.
* bind(): a separate action, with its basis recorded as SUPPORTED_BY edges.
  A ONE_SHOT mandate becomes HISTORICAL after use.
* binding_state(): a VIEW over the support graph (A12.6). No status is
  rewritten on the binding itself.
* on_basis_lost(): requirement reopens non-destructively; a used ONE_SHOT
  mandate is NOT revived; an ASK goes to its issuer.
"""
from demon_core import Record, GO, ASK

METHOD = "C1_JOINT_BINDINGS"
SCOPE = "CURRENT_FACTS"
AUTO_BIND = "AUTO_BIND"
ONE_SHOT, STANDING_WHILE = "ONE_SHOT", "STANDING_WHILE"


def _latest(net, addr):
    r = net.read(addr)
    return r.status_log[-1].state if r is not None and r.status_log else None


def network_state(net):
    """N: the commit counter of the ledger."""
    return len(net.commit_log)


def candidacy_addr(rq, cand, n, scope=SCOPE, method=METHOD):
    """Snapshot identity (A12.3): (rq, candidate, N, scope, method).

    A claim made on N10 and a later claim on N14 are different claims; an old
    HISTORICAL claim is never re-activated.
    """
    return f"CAND_{rq}_{cand}_{scope}_{method}_N{n}"


def current_candidacies(net, rq):
    return sorted(r.addr for r in net.records.values()
                  if r.f("TYPE") == "SOLE_KNOWN_CANDIDATE_ON" and r.f("REQUIREMENT") == rq
                  and _latest(net, r.addr) == "CURRENT")


# ── discovery ──
def requirement_variable(patterns):
    """The single variable shared by all requirement patterns (e.g. ?X); else error."""
    vs = [{t for t in p if isinstance(t, str) and t.startswith("?")} for p in patterns]
    shared = set.intersection(*vs) if vs else set()
    if len(shared) != 1:
        raise ValueError(f"requirement needs exactly one shared variable, got {sorted(shared)}")
    return shared.pop()


def watch_requirement(net, demon, c13, rq):
    rq_rec = net.read(rq)
    if rq_rec is None:
        return {"created": [], "historical": []}
    patterns = c13._requirement_patterns(rq_rec)
    var = requirement_variable(patterns)
    cands = []
    for b, _ in c13.joint_bindings(patterns):
        if b[var] not in cands:
            cands.append(b[var])
    n = network_state(net)
    created, historical = [], []
    kept = None
    for a in current_candidacies(net, rq):
        if len(cands) == 1 and net.read(a).f("CANDIDATE") == cands[0]:
            kept = a                                   # same claim still holds; no new record per commit
            continue
        demon.commit(demon.propose(mark=[(a, "HISTORICAL", None, None,
                                          f"candidate set on N{n}: {cands}")]))
        historical.append(a)
    if len(cands) == 1 and kept is None:               # (re-)established -> a NEW snapshot claim
        a = candidacy_addr(rq, cands[0], n)
        rec = Record(a, {"TYPE": "SOLE_KNOWN_CANDIDATE_ON", "REQUIREMENT": rq, "VARIABLE": var,
                         "CANDIDATE": cands[0], "N": n, "SCOPE": SCOPE, "METHOD": METHOD})
        demon.commit(demon.propose(add=[rec], mark=[(a, "CURRENT", None, None, f"N{n}")]))
        created.append(a)
    amb = _track_ambiguity(net, demon, c13, rq, var, cands, n, created)
    return {"created": created, "historical": historical, "candidates": cands, "N": n, **amb}


# ── WS08: ambiguity is a record, and it asks a question that cuts the set ──
def ambiguity_addr(rq, n, scope=SCOPE, method=METHOD):
    return f"AMB_{rq}_{scope}_{method}_N{n}"


def current_ambiguities(net, rq):
    return sorted(r.addr for r in net.records.values()
                  if r.f("TYPE") == "AMBIGUOUS_CANDIDATES_ON" and r.f("REQUIREMENT") == rq
                  and _latest(net, r.addr) == "OPEN")


def _ask_for(net, amb_addr):
    where = f"candidate/ambiguity/{amb_addr}"
    for r in net.records.values():
        if r.f("TYPE") == "OPEN" and r.f("OPEN_KIND") == "ASK" and r.f("ORIGIN_WHERE") == where:
            return r.addr
    return None


def _track_ambiguity(net, demon, c13, rq, var, cands, n, sole_created):
    made, closed, asks, answered = [], [], [], []
    current = current_ambiguities(net, rq)
    same = [a for a in current if len(cands) > 1 and net.read(a).f("CANDIDATES") == sorted(cands)]
    for a in current:
        if a in same:
            continue
        demon.commit(demon.propose(mark=[(a, "HISTORICAL", None, None, f"candidate set on N{n}: {cands}")]))
        closed.append(a)
        ask = _ask_for(net, a)
        if ask and _latest(net, ask) == "OPEN" and sole_created:      # answered by the new sole claim
            edge = Record(f"{ask}_ANSWERED_BY", {"SUBJECT": ask, "PREDICATE": "REFERS_TO",
                                                 "OBJECT": sole_created[0], "ROLE": "ANSWERED_BY"})
            demon.commit(demon.propose(add=[edge], mark=[(ask, "ANSWERED", None, None, sole_created[0])]))
            answered.append(ask)
    if len(cands) > 1 and not same:
        a = ambiguity_addr(rq, n)
        rec = Record(a, {"TYPE": "AMBIGUOUS_CANDIDATES_ON", "REQUIREMENT": rq, "VARIABLE": var,
                         "CANDIDATES": sorted(cands), "N": n, "SCOPE": SCOPE, "METHOD": METHOD})
        demon.commit(demon.propose(add=[rec], mark=[(a, "OPEN", None, None, f"N{n}")]))
        made.append(a)
        net.stop(where=f"candidate/ambiguity/{a}", wanted=f"single binding of {var} for {rq}",
                 available=f"candidates {sorted(cands)} on N{n}", missing=tuple(sorted(cands)),
                 stop_class=ASK, can_ask=True,
                 query=f"which of {sorted(cands)} is {var} for {rq}? (any answer leaves 1 of {len(cands)})")
        c13.materialize_ask_opens()
        new_ask = _ask_for(net, a)
        asks.append(new_ask)
        # the joint "find any X" question is no longer the right one: X is known, the choice is not
        joint = f"candidate/joint-requirement/{rq}"
        sup = [Record(f"{new_ask}_SUPERSEDES_{r.addr}", {"SUBJECT": new_ask, "PREDICATE": "REFERS_TO",
                                                          "OBJECT": r.addr, "ROLE": "SUPERSEDES",
                                                          "REQUIREMENT": rq,
                                                          "BASIS": "at least one known candidate for REQUIREMENT"})
               for r in sorted(net.records.values(), key=lambda r: r.addr)
               if r.f("TYPE") == "OPEN" and r.f("OPEN_KIND") == "ASK" and r.f("ORIGIN_WHERE") == joint]
        if sup:
            demon.commit(demon.propose(add=sup))
    return {"ambiguity_created": made, "ambiguity_closed": closed,
            "disambiguation_asks": asks, "disambiguation_answered": answered}


# ── authority ──
def issue_mandate(net, demon, addr, task, issuer, op=AUTO_BIND, scope=None,
                  lifecycle=ONE_SHOT, condition=None):
    """condition (STANDING_WHILE only): {"RECORD": addr, "STATE_IN": [states]}, evaluated
    against the record's latest status every time authority is checked."""
    if lifecycle == STANDING_WHILE and not (isinstance(condition, dict)
                                            and condition.get("RECORD") and condition.get("STATE_IN")):
        raise ValueError("STANDING_WHILE needs a machine-checkable condition")
    if issuer == op:
        raise PermissionError("an operation cannot issue its own mandate (DCT09)")
    rec = Record(addr, {"TYPE": "MANDATE", "TASK": task, "ISSUER": issuer, "PERMITS": op,
                        "SCOPE": scope, "LIFECYCLE": lifecycle, "CONDITION": condition})
    demon.commit(demon.propose(add=[rec], mark=[(addr, "CURRENT")]))
    return addr


def condition_holds(net, mandate_rec):
    c = mandate_rec.f("CONDITION")
    if mandate_rec.f("LIFECYCLE") != STANDING_WHILE:
        return True
    return _latest(net, c["RECORD"]) in c["STATE_IN"]


def current_mandate(net, task, op=AUTO_BIND, scope=None):
    """Authority in force = record CURRENT AND (for STANDING_WHILE) its condition true now."""
    for r in sorted(net.records.values(), key=lambda r: r.addr):
        if (r.f("TYPE") == "MANDATE" and r.f("TASK") == task and r.f("PERMITS") == op
                and r.f("SCOPE") in (None, scope) and _latest(net, r.addr) == "CURRENT"
                and condition_holds(net, r)):
            return r.addr
    return None


# ── decision ──
def bind(net, demon, rq, candidacy, authorized_by, bind_addr=None):
    cand = net.read(candidacy)
    if cand is None or _latest(net, candidacy) != "CURRENT":
        return None
    a = bind_addr or f"{rq}_BIND"
    if net.read(a) is not None:
        return None
    edge = Record(a, {"SUBJECT": rq, "PREDICATE": "REFERS_TO", "OBJECT": cand.f("CANDIDATE"),
                      "ROLE": "BOUND_CANDIDATE", "AUTHORIZED_BY": authorized_by})
    sup = Record(f"{a}_SUPPORTED_BY_1", {"SUBJECT": a, "PREDICATE": "SUPPORTED_BY",
                                         "OBJECT": candidacy, "ROLE": "BIND_BASIS"})
    v, _ = demon.commit(demon.propose(add=[edge, sup], mark=[(rq, "BOUND", None, None, a)]))
    if v != GO:
        return None
    m = net.read(authorized_by)
    if m is not None and m.f("TYPE") == "MANDATE" and m.f("LIFECYCLE") == ONE_SHOT:
        demon.commit(demon.propose(mark=[(authorized_by, "HISTORICAL", None, None, f"used by {a}")]))
    return a


def binding_state(net, bind_addr):
    """View: SUPPORTED if any basis is CURRENT, else REVIEW_REQUIRED."""
    bases = [r.f("OBJECT") for r in net.records.values()
             if r.f("SUBJECT") == bind_addr and r.f("PREDICATE") == "SUPPORTED_BY"]
    if not bases:
        return "UNSUPPORTED"
    return "SUPPORTED" if any(_latest(net, b) == "CURRENT" for b in bases) else "REVIEW_REQUIRED"


def on_basis_lost(net, demon, rq, bind_addr):
    """Reopen the requirement; never revive a used ONE_SHOT mandate; ASK the issuer."""
    if binding_state(net, bind_addr) != "REVIEW_REQUIRED" or _latest(net, rq) != "BOUND":
        return None
    demon.commit(demon.propose(mark=[(rq, "OPEN", None, None, f"basis of {bind_addr} lost")]))
    mandate = net.read(bind_addr).f("AUTHORIZED_BY")
    m = net.read(mandate) if mandate else None
    if m is not None and m.f("TYPE") == "MANDATE":
        if m.f("LIFECYCLE") == STANDING_WHILE and _latest(net, mandate) == "CURRENT" \
                and condition_holds(net, m):
            return {"reopened": rq, "mandate": mandate, "still_in_force": True}
        net.stop(f"mandate/{mandate}", f"renew {m.f('PERMITS')} for {m.f('TASK')}",
                 f"{bind_addr} lost its basis", "issuer decision", ASK, can_ask=True,
                 query=f"to {m.f('ISSUER')}: binding {bind_addr} lost its basis; renew {m.f('PERMITS')}?")
        return {"reopened": rq, "mandate": mandate, "still_in_force": False, "ask_to": m.f("ISSUER")}
    return {"reopened": rq, "mandate": None}


def supersession_holds(net, edge_rec):
    """WS08b: a SUPERSEDES edge has its own basis, independent of the superseding ASK's
    stored status: the joint "find any X" question stays superseded while at least
    one candidate for the requirement is known (a CURRENT sole candidacy or an OPEN
    ambiguity). If every candidate vanishes, "find X" is the right question again.
    """
    rq = edge_rec.f("REQUIREMENT")
    return bool(rq) and bool(current_candidacies(net, rq) or current_ambiguities(net, rq))
