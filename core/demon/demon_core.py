#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demon_core.py — DEMON_CORE_SPEC-ის დეტერმინისტული იმპლემენტაცია (GW02).

წესი №1: არცერთი ჰევრისტიკა. რასაც წესი არ ფარავს → NEED/ASK, არასდროს გამოცნობა.
წყარო: current/DEMON_CORE_SPEC.md §1–§28 + GW01 overlay (§27.1–27.4).
LLM არ მონაწილეობს არცერთ ნაბიჯზე — ეს არის მთელი ექსპერიმენტის აზრი.
"""

from dataclasses import dataclass, field
from typing import Optional

# ── ვერდიქტები (§7) ───────────────────────────────────────────────
GO, ASK, BLOCK, NEED, PASS, FAIL = "GO", "ASK", "BLOCK", "NEED", "PASS", "FAIL"


@dataclass
class StopCard:                                    # §8
    where: str
    wanted: str
    available: str
    missing: str
    stop_class: str
    can_ask_outside: bool = False
    query: str = ""

    def __repr__(self):
        return f"<STOP {self.stop_class} @ {self.where} | MISSING: {self.missing}>"


@dataclass
class StatusAssertion:                             # §19 — non-destructive MARK
    state: str
    scope: Optional[str] = None
    time: Optional[tuple] = None                   # (t_from, t_to)
    basis: Optional[str] = None                    # audit/record addr
    seq: int = 0


@dataclass
class Record:
    addr: str
    fields: dict = field(default_factory=dict)     # SUBJECT/PREDICATE/OBJECT/TYPE/...
    status_log: list = field(default_factory=list) # [StatusAssertion] — history preserved
    committed: bool = False

    def f(self, k, d=None):
        return self.fields.get(k, d)


class Network:
    """ცნებების ველი: ყველაფერი მისამართიანი record-ია (invariant §2)."""

    def __init__(self):
        self.records: dict[str, Record] = {}
        self._seq = 0
        self.commit_log: list = []                 # (commit_id, delta_summary) — §17 trace
        self.stops: list[StopCard] = []
        self.active_watches: list[str] = []        # overlay 27.3
        self.events: list = []                     # KAIROS events

    # ── READ ──
    def read(self, addr):
        return self.records.get(addr)              # None = NOT_FOUND ≠ არარსებობა

    # ── MATCH ──
    def match(self, **pattern):
        out = []
        for r in self.records.values():
            if all(r.f(k) == v for k, v in pattern.items()):
                out.append(r)
        return out

    def refs_to(self, target_addr, role=None):
        """ვინ მიუთითებს target-ზე (უკუ-ძებნა REFERS_TO ბმებით)."""
        edges = [r for r in self.records.values()
                 if r.f("PREDICATE") == "REFERS_TO" and r.f("OBJECT") == target_addr]
        if role is not None:
            edges = [e for e in edges if e.f("ROLE") == role]
        return edges

    def refs_from(self, src_addr, role=None):
        edges = [r for r in self.records.values()
                 if r.f("PREDICATE") == "REFERS_TO" and r.f("SUBJECT") == src_addr]
        if role is not None:
            edges = [e for e in edges if e.f("ROLE") == role]
        return edges

    # ── MARK (§19: ახალი assertion, ძველი რჩება) ──
    def mark(self, addr, state, scope=None, time=None, basis=None):
        r = self.records[addr]
        self._seq += 1
        r.status_log.append(StatusAssertion(state, scope, time, basis, self._seq))

    def status_assertions(self, addr):
        return list(self.records[addr].status_log)

    def current_status(self, addr, scope=None, time=None):
        """DCT12–14: სტატუსი scoped/timed assertion-ია. დაბრუნება:
        (state, verdict) — verdict GO თუ ერთმნიშვნელოვანია; ASK/NEED/BLOCK სხვაგვარად."""
        log = self.records[addr].status_log
        if not log:
            return None, GO
        # applicability filter (DCT13/14)
        applicable = []
        for a in log:
            if a.scope is not None and scope is None and len({x.scope for x in log if x.scope}) > 0 \
               and len({x.state for x in log}) > 1:
                # scoped assertions არსებობს, query კი unscoped და states განსხვავდება
                return None, ASK
            if a.scope is not None and scope is not None and a.scope != scope:
                continue
            if a.time is not None:
                if time is None:
                    if len({x.state for x in log}) > 1:
                        return None, ASK           # STOP_19: time qualifier აკლია
                else:
                    if not (a.time[0] <= time <= a.time[1]):
                        continue
            applicable.append(a)
        if not applicable:
            return None, GO
        states = {a.state for a in applicable}
        if len(states) == 1:
            return applicable[-1].state, GO
        # GW02-ის აღმოჩენა: სპეცს ორი რეჟიმი აქვს და გარჩევა ბაზისზე დგას —
        #  · უბაზისო MARK-ები = სტატუსის გადასვლები → ბოლო assertion მიმდინარეა (DCT12 §7)
        #  · ბაზისიანი (აუდიტზე მდგარი) assertions = ერთდროული გამოყენებადობა →
        #    incompatibility = CONFLICT/BLOCK (DCT13 §5); არჩევა პოლიტიკის გარეშე იკრძალება (DCT12 §4)
        if all(a.basis is None for a in applicable):
            return max(applicable, key=lambda a: a.seq).state, GO
        return None, BLOCK

    def stop(self, where, wanted, available, missing, stop_class, can_ask=False, query=""):
        c = StopCard(where, wanted, available, missing, stop_class, can_ask, query)
        self.stops.append(c)
        return c


class Demon:
    """არაფრისმცოდნე ოპერატორი: PROPOSE → CHECK → COMMIT მემბრანა (§16)."""

    def __init__(self, net: Network):
        self.net = net
        self._cid = 0

    # ── PROPOSE: delta = dict(add=[Record], mark=[(addr,state,...)], delete=[addr],
    #                          skip_check=False, introduces_rules=[addr], uses_rules=[addr],
    #                          authorized_by=addr|None, derived=[(addr, premises, rule)])
    def propose(self, **delta):
        delta.setdefault("add", []); delta.setdefault("mark", [])
        delta.setdefault("delete", []); delta.setdefault("derived", [])
        delta.setdefault("introduces_rules", []); delta.setdefault("uses_rules", [])
        delta.setdefault("skip_check", False); delta.setdefault("authorized_by", None)
        return delta

    # ── CHECK: §4-ის კარიბჭე + §16 მემბრანა. აბრუნებს (PASS|FAIL, მიზეზი) ──
    def check(self, delta):
        n = self.net
        # membrane 2: CHECK-ის გამოტოვება იკრძალება (DCT09)
        if delta["skip_check"]:
            n.stop("membrane", "commit without CHECK", "transaction gate",
                   "none", BLOCK)
            return FAIL, "membrane: CHECK is not optional"
        # membrane 1: self-authorization (DCT09)
        for ra in delta["uses_rules"]:
            if ra in delta["introduces_rules"]:
                n.stop("membrane", "authorize delta by its own rule", ra, "none", BLOCK)
                return FAIL, "membrane: self-authorizing delta"
            rule = n.read(ra)
            if rule is None or not rule.committed:
                return FAIL, f"rule {ra} not in committed state N-1"
        # gate 7: historical erasure (DCT10)
        for addr in delta["delete"]:
            r = n.read(addr)
            if r is not None and r.committed:
                n.stop("gate/history", "erase committed record", addr, "none", BLOCK)
                return FAIL, "history erasure: committed record would become untraceable"
        # gate 5: unauthorized ontology (CREATE_ADDRESS explicit authorization, §3)
        for rec in delta["add"]:
            t = rec.f("TYPE")
            if t == "REQUIREMENT_CONCEPT":
                auth = delta["authorized_by"]
                task = n.read(auth) if auth else None
                if task is None or task.f("TYPE") != "TASK" or not task.f("REQUIRED_PATTERNS"):
                    n.stop("gate/birth", "create requirement concept",
                           "general birth rule OPEN", "explicit TASK authorization", NEED)
                    return FAIL, "requirement-concept birth needs explicit TASK (general rule OPEN)"
            if t == "OBSERVATION" and rec.f("SOURCE") is None:
                return FAIL, "ingest without source provenance (overlay 27.1)"
        # gate 1: provenance preserved — derived record-ს უნდა ახლდეს premises+rule refs
        for (daddr, premises, rule) in delta["derived"]:
            planned = {r.f("OBJECT") for r in delta["add"]
                       if r.f("PREDICATE") == "REFERS_TO" and r.f("SUBJECT") == daddr}
            needed = set(premises) | {rule}
            if not needed <= planned:
                n.stop("gate/provenance", f"commit derived {daddr}",
                       "premises+rule addressable",
                       "generic record-to-record reference edges", FAIL and NEED)
                return FAIL, "derived record without exact provenance references"
        # gate 6: credit promotion (§5)
        for (addr, state, *_rest) in delta["mark"]:
            r = n.read(addr)
            if r is None:
                continue
            cur = r.status_log[-1].state if r.status_log else None
            if cur == "CREDIT_DEPENDENT" and state in ("CURRENT", "VALIDATED", "SUPPORTED"):
                # დაშვებულია მხოლოდ independent re-grounding-ით (აქ: REGROUNDED ბაზისით)
                basis = _rest[2] if len(_rest) > 2 else None
                if basis != "INDEPENDENT_REGROUND":
                    n.stop("gate/credit", f"promote {addr}", "credit repaid",
                           "independent re-grounding", BLOCK)
                    return FAIL, "credit repaid ≠ descendant validated"
        return PASS, "ok"

    # ── COMMIT ──
    def commit(self, delta):
        v, reason = self.check(delta)
        if v != PASS:
            return BLOCK, reason
        n = self.net
        for rec in delta["add"]:
            n.records[rec.addr] = rec; rec.committed = True
        for m in delta["mark"]:
            n.mark(*m)
        self._cid += 1
        cid = f"C{self._cid}"
        n.commit_log.append((cid, {k: v for k, v in delta.items() if k in
                                   ("add", "mark", "derived")}))
        self._run_watches()                        # overlay 27.3
        return GO, cid

    # ── overlay 27.3: post-COMMIT watch reevaluation ──
    def _run_watches(self):
        n = self.net
        for waddr in n.active_watches:
            w = n.read(waddr)
            cond = w.f("CONDITION")                # callable(net) → bool (ქსელის წესი)
            if cond and cond(n) and not w.f("FIRED"):
                w.fields["FIRED"] = True
                ev = Record(f"KAIROS_{waddr}", {"TYPE": "KAIROS", "WATCH": waddr})
                n.records[ev.addr] = ev; ev.committed = True
                n.events.append(ev.addr)

    # ── სტატუსის გადასვლა SINGLE_CURRENT_TARGET / multiplicity (overlay 27.4) ──
    def assert_current(self, subj, pred, new_rec: Record, pred_props: dict):
        """ახალი CURRENT მნიშვნელობა subject/predicate-ზე."""
        n = self.net
        olds = [r for r in n.records.values()
                if r.f("SUBJECT") == subj and r.f("PREDICATE") == pred
                and r.status_log and r.status_log[-1].state == "CURRENT"]
        d = self.propose(add=[new_rec], mark=[(new_rec.addr, "CURRENT")])
        v, cid = self.commit(d)
        if v != GO:
            return v, cid
        if pred_props.get("SINGLE_CURRENT_TARGET"):
            for o in olds:
                self.commit(self.propose(mark=[(o.addr, "HISTORICAL")]))
            # downstream consequence — edge-local, policy-driven
            for o in olds:
                self.propagate(o.addr, "HISTORICAL")
            return GO, cid
        if pred_props.get("CARDINALITY") is None and olds:
            op = Record(f"OPEN_MULT_{pred}", {"TYPE": "OPEN",
                        "ABOUT": f"unresolved multiplicity of {pred}"})
            self.commit(self.propose(add=[op], mark=[(op.addr, "OPEN")]))
            n.stop("multiplicity", f"current value of {subj}/{pred}",
                   "several CURRENT targets", "cardinality policy", NEED)
            return NEED, op.addr                   # ხილული OPEN, არა ჩუმი ორაზროვნება
        return GO, cid

    # ── DCT07/08/22: edge-local, policy-driven propagation ──
    def propagate(self, changed_addr, new_state):
        n = self.net
        results = []
        for edge in n.refs_to(changed_addr):
            role = edge.f("ROLE")
            if role not in ("PREMISE", "JUSTIFICATION", "COMPOSITION_POLICY"):
                continue
            dependent = edge.f("SUBJECT")
            policies = [n.read(p.f("OBJECT")) for p in n.refs_from(edge.addr, role="POLICY")]
            if not policies:
                results.append(n.stop(f"propagate/{dependent}",
                    f"consequence of {changed_addr}→{new_state}",
                    f"dependency edge {edge.addr} ROLE={role}",
                    "applicable dependency-policy rule", NEED))
                continue
            effects = {p.f("EFFECT") for p in policies}
            if len(effects) > 1:                   # DCT08: rule-level conflict
                cf = Record(f"CF_POLICY_{edge.addr}", {"TYPE": "CONFLICT"})
                n.records[cf.addr] = cf; cf.committed = True
                n.mark(cf.addr, "OPEN")
                for p in policies:
                    e = Record(f"{cf.addr}_side_{p.addr}",
                               {"SUBJECT": cf.addr, "PREDICATE": "REFERS_TO",
                                "OBJECT": p.addr, "ROLE": "CONFLICT_SIDE"})
                    n.records[e.addr] = e; e.committed = True
                results.append(n.stop(f"propagate/{dependent}",
                    "apply downstream consequence", "two applicable policies",
                    "unique legal continuation", BLOCK))
                continue
            eff = effects.pop()
            if eff == "KEEP":
                results.append((dependent, GO, "kept in historical scope"))
            elif eff in ("OPEN", "CHALLENGED"):
                n.mark(dependent, eff)
                results.append((dependent, GO, f"→ {eff}"))
                # ტალღა გრძელდება მხოლოდ შემდეგი edge-ების პოლიტიკებით (DCT22)
                results.extend(self.propagate(dependent, eff))
        return results

    # ── DCT15–18: qualifier applicability evaluation ──
    def applicability(self, assertion_addr, query_ctx, _visited=None):
        """აბრუნებს (APPLICABLE|NOT_APPLICABLE|None, verdict)."""
        n = self.net
        _visited = _visited or set()
        quals = [n.read(e.f("OBJECT")) for e in
                 n.refs_from(assertion_addr, role="QUALIFIER")]
        for q in quals:
            pols = [n.read(e.f("OBJECT")) for e in n.refs_from(q.addr, role="MATCH_POLICY")]
            if not pols:
                n.stop("applicability", f"does {assertion_addr} apply",
                       f"qualifier {q.addr}", "matching policy", NEED)
                return None, NEED                  # STOP_21
            outs = set()
            for p in pols:
                key = (q.addr, p.addr)
                if key in _visited:                # DCT17: ციკლი
                    cy = Record(f"CY_{q.addr}", {"TYPE": "EVALUATION_CYCLE"})
                    n.records[cy.addr] = cy; cy.committed = True
                    n.mark(cy.addr, "OPEN")
                    n.stop("applicability", "terminate evaluation",
                           "recursive policy chain", "terminating legal path", BLOCK)
                    return None, BLOCK
                _visited.add(key)
                # policy თვითონ qualified? (DCT17 ჯანმრთელი რეკურსია)
                pq = n.refs_from(p.addr, role="QUALIFIER")
                if pq:
                    sub, v = self.applicability(p.addr, query_ctx, _visited)
                    if v != GO:
                        return None, v
                fn = p.f("MATCH_FN")               # callable(q_value, ctx) → bool
                outs.add(bool(fn(q.f("VALUE"), query_ctx)))
            if len(outs) > 1:                      # DCT16/18: divergent lawful outcomes
                cf = Record(f"CF_QPOLICY_{q.addr}", {"TYPE": "CONFLICT"})
                n.records[cf.addr] = cf; cf.committed = True
                n.mark(cf.addr, "OPEN")
                n.stop("applicability", f"qualifier {q.addr} evaluation",
                       "incompatible lawful outcomes", "unique legal outcome", BLOCK)
                return None, BLOCK
            if outs == {False}:
                return "NOT_APPLICABLE", GO        # ≠ FALSE ≠ CHALLENGED
        return "APPLICABLE", GO

    # ── DCT19–21: justification composition ──
    def result_support(self, ev_addr, scope=None, time=None):
        """EV-ის მიმდინარე მხარდაჭერა justification-ების და composition policy-ის მიხედვით."""
        n = self.net
        jps = [e.f("OBJECT") for e in n.refs_from(ev_addr, role="JUSTIFICATION")]
        states = {}
        for jp in jps:
            s, v = n.current_status(jp, scope, time)
            if v != GO:
                return None, v                     # ორაზროვანი justification არ იმალება
            states[jp] = s if s is not None else "SUPPORTED"  # ცარიელი ლოგი = საწყისი მხარდაჭერა
        if all(s == "SUPPORTED" for s in states.values()):
            return "SUPPORTED", GO
        cps = [n.read(e.f("OBJECT")) for e in n.refs_from(ev_addr, role="COMPOSITION_POLICY")]
        cps = [c for c in cps if c.status_log and c.status_log[-1].state == "CURRENT"]
        if not cps:
            n.stop("composition", f"current support of {ev_addr}",
                   f"justifications {states}", "justification-composition policy", NEED)
            return None, NEED                      # STOP_25
        if len(cps) > 1:
            n.stop("composition", "select composition policy",
                   "two applicable policies", "explicit precedence", BLOCK)
            return None, BLOCK                     # DCT21 §7
        mode = cps[0].f("MODE")
        if mode == "ALTERNATIVE":
            ok = any(s == "SUPPORTED" for s in states.values())
            return ("SUPPORTED" if ok else "CHALLENGED"), GO
        if mode == "JOINT":
            ok = all(s == "SUPPORTED" for s in states.values())
            return ("SUPPORTED" if ok else "CHALLENGED"), GO
        n.stop("composition", "interpret policy mode", str(mode),
               "known composition mode", NEED)
        return None, NEED