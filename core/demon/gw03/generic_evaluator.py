#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generic_evaluator.py — ერთი ზოგადი შემსრულებელი დეკლარაციული წესებისთვის (GW03).

CONTENT-BLIND: ამ ფაილში არ ჩანს არც ერთი კონკრეტული პრედიკატი, ობიექტი,
წყარო ან წესის მისამართი. ყველაფერი, რაც სამყაროს ეხება, მოდის ქსელის
ჩანაწერებიდან. demon_core უცვლელია (GW02-ის კომიტი).

EVALUATOR-ის სემანტიკა — ანუ ის, რასაც წესების ჩანაწერები ვერ იტყვიან და
კოდმა უნდა თქვას (ეს არის compiler boundary-ის ნარჩენი):
  [EV-1] დერივაცია goal-directed-ია: ეშვება მხოლოდ TASK-ის კითხვაზე, არა
         saturation-ით. დასაბუთება: სპეცში CREATE_ADDRESS ავტორიზაციას
         ითხოვს; დაუკითხავი ტოტალური დერივაცია ავტორიზაციის გარეშე
         ონტოლოგიის შექმნა იქნებოდა.
  [EV-2] დარაჯის (INGEST_GUARD) პირობის შეფასება ორ ნაბიჯიანია:
         (ა) თუ პირობის ნიმუში ახლა CURRENT-ზე ჯდება → აკრძალვა მოქმედებს;
         (ბ) თუ პირობის დამიწებული (S,P) წყვილი მრავალმნიშვნელოვანია და
             P-ს კარდინალობის პოლიტიკა არ აქვს → გამოყენებადობა გადაუწყვეტია
             → ცალკე NEED. ეს ზოგადი პრინციპია ყველა დარაჯზე, არა
             კონკრეტული წესის კავშირი.
  [EV-3] ყოველი წესით-გაჩერება ქსელშივე იწერება: STOP-ჩანაწერი + REFERS_TO
         ბმა წესზე ROLE=BASIS — „რატომ გავჩერდი" მიკვლევადია refs_to-თი.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demon_core import Network, Record, Demon, GO, ASK, BLOCK, NEED


def is_var(t):
    return isinstance(t, str) and t.startswith("?")


class Evaluator:
    def __init__(self, net: Network, demon: Demon):
        self.net, self.d = net, demon
        self._stoprec = 0

    def load_facts(self, triples):
        for addr, s, p, o, extra in triples:
            r = Record(addr, {"SUBJECT": s, "PREDICATE": p, "OBJECT": o, **extra})
            self.net.records[addr] = r; r.committed = True
            self.net.mark(addr, "CURRENT")

    def load_rules(self, rule_dicts):
        for rd in rule_dicts:
            rd = dict(rd); addr = rd.pop("addr")
            r = Record(addr, {"TYPE": "RULE", **rd})
            self.net.records[addr] = r; r.committed = True
            self.net.mark(addr, "CURRENT")

    def rules(self, rtype):
        return [r for r in self.net.records.values()
                if r.f("TYPE") == "RULE" and r.f("RULE_TYPE") == rtype
                and r.status_log and r.status_log[-1].state == "CURRENT"]

    def pred_props(self, pred):
        props = {}
        for r in self.rules("CARDINALITY_POLICY"):
            if r.f("RULE_PREDICATE") == pred:
                props[r.f("POLICY")] = True
        return props

    def _unify(self, pat, rec, b):
        b = dict(b)
        for k, t in zip(("SUBJECT", "PREDICATE", "OBJECT"), pat):
            v = rec.f(k)
            if is_var(t):
                if t in b and b[t] != v:
                    return None
                b[t] = v
            elif t != v:
                return None
        return b

    def facts(self):
        return [r for r in self.net.records.values()
                if r.f("PREDICATE") not in (None, "REFERS_TO")
                and r.status_log and r.status_log[-1].state == "CURRENT"]

    def holds(self, pat, b=None):
        return [x for x in ((r, self._unify(pat, r, b or {}))
                            for r in self.facts()) if x[1] is not None]

    def join(self, pats):
        branches = [({}, [])]
        for p in pats:
            branches = [(nb, recs + [r]) for b, recs in branches
                        for r, nb in self.holds(p, b)]
        return branches

    def _ground(self, pat, b):
        return tuple(b.get(t, t) for t in pat)

    def _stop_basis(self, where, rule_addr):
        self._stoprec += 1
        a = f"STOPREC{self._stoprec}"
        rec = Record(a, {"TYPE": "STOP_RECORD", "WHERE": where})
        edge = Record(a + "_b", {"SUBJECT": a, "PREDICATE": "REFERS_TO",
                                 "OBJECT": rule_addr, "ROLE": "BASIS"})
        self.d.commit(self.d.propose(add=[rec, edge]))

    def source_class(self, source):
        return source.rstrip("0123456789") if source else None

    def guard_stops(self, ev, s, p, o, source):
        stops = []
        tmp = Record("_tmp", {"SUBJECT": s, "PREDICATE": p, "OBJECT": o})
        for g in self.rules("INGEST_GUARD"):
            if g.f("SOURCE_CLASS") != self.source_class(source):
                continue
            b = self._unify(g.f("FORBIDDEN"), tmp, {})
            if b is None:
                continue
            cond = self._ground(g.f("CONDITION"), b)
            if self.holds(cond):
                self.net.stop(f"{ev}/{g.addr}", f"ingest ({s} {p} {o}) from {source}",
                              f"{cond} CURRENT ⇒ forbidden by {g.addr}",
                              f"none — {g.addr} forbids", BLOCK)
                self._stop_basis(f"{ev}/{g.addr}", g.addr)
                stops.append((BLOCK, g.addr))
            cs, cp, _ = cond
            if not is_var(cs) and not is_var(cp):
                vals = {r.f("OBJECT") for r, _ in self.holds((cs, cp, "?V"))}
                if len(vals) > 1 and not self.pred_props(cp):
                    self.net.stop(f"{ev}/{g.addr}-applicability",
                                  f"decide {g.addr} applicability",
                                  f"({cs} {cp}) multiplicity unresolved "
                                  f"({sorted(vals)} all CURRENT)",
                                  f"cardinality policy for {cp}", NEED)
                    self._stop_basis(f"{ev}/{g.addr}-applicability", g.addr)
                    stops.append((NEED, g.addr))
        return stops

    def assert_fact(self, ev, rec):
        s, p = rec.f("SUBJECT"), rec.f("PREDICATE")
        props = self.pred_props(p)
        if props.get("SINGLE_CURRENT_TARGET"):
            tps = [t for t in self.rules("TEMPORAL_POLICY")
                   if t.f("RULE_PREDICATE") == p
                   and t.f("POLICY") == "LATER_TIME_SUPERSEDES"]
            for old, _ in self.holds((s, p, "?V")):
                if (tps and old.f("TIME") is not None and rec.f("TIME") is not None
                        and not rec.f("TIME") > old.f("TIME")):
                    self.net.stop(f"{ev}/temporal", f"supersede {old.addr}",
                                  "earlier TIME on incoming record",
                                  "legal supersession path", NEED)
                    return NEED, old.addr
        return self.d.assert_current(s, p, rec, props)

    def ingest(self, ev, addr, s, p, o, source, time=None):
        gs = self.guard_stops(ev, s, p, o, source)
        if any(v == BLOCK for v, _ in gs):
            return BLOCK, gs
        f = {"SUBJECT": s, "PREDICATE": p, "OBJECT": o,
             "TYPE": "OBSERVATION", "SOURCE": source}
        if time is not None:
            f["TIME"] = time
        v, extra = self.assert_fact(ev, Record(addr, f))
        return v, gs or extra

    def task_query(self, ev, s, p, derived_addr, domain=None):
        direct = self.holds((s, p, "?Z"))
        if direct:
            return GO, [b["?Z"] for _, b in direct], None
        for rule in self.rules("DERIVATION"):
            cx, cp, cz = rule.f("CONCLUSION")
            if not is_var(cp) and cp != p:
                continue
            b0 = {}
            if is_var(cx):
                b0[cx] = s
            elif cx != s:
                continue
            for b, recs in self.join([self._ground(q, b0)
                                      for q in rule.f("PREMISES")]):
                concl = self._ground(rule.f("CONCLUSION"), {**b0, **b})
                if domain is not None and concl[2] not in domain:
                    continue
                dv = Record(derived_addr, {"SUBJECT": concl[0],
                                           "PREDICATE": concl[1],
                                           "OBJECT": concl[2]})
                refs = [Record(f"{derived_addr}_r{i}",
                               {"SUBJECT": derived_addr, "PREDICATE": "REFERS_TO",
                                "OBJECT": oaddr, "ROLE": role})
                        for i, (oaddr, role) in enumerate(
                            [(r.addr, "PREMISE") for r in recs]
                            + [(rule.addr, "RULE_USED")], 1)]
                v, _ = self.d.commit(self.d.propose(
                    add=[dv] + refs,
                    derived=[(derived_addr, [r.addr for r in recs], rule.addr)],
                    mark=[(derived_addr, "CURRENT")]))
                return v, [concl[2]], (derived_addr, [r.addr for r in recs],
                                       rule.addr)
        return NEED, [], None

    def goal_assert(self, ev, s, p, o):
        demote = []
        if self.pred_props(p).get("SINGLE_CURRENT_TARGET"):
            demote = [r for r, _ in self.holds((s, p, "?V"))
                      if r.f("OBJECT") != o]
        for inv in self.rules("INVARIANT"):
            if inv.f("REQUIRED_STATE") != "CURRENT":
                continue
            for r in demote:
                if self._unify(inv.f("PATTERN"), r, {}) is not None:
                    cards = [c.addr for c in self.rules("CARDINALITY_POLICY")
                             if c.f("RULE_PREDICATE") == p]
                    self.net.stop(f"{ev}/goal", f"make ({s} {p} {o}) current",
                                  f"{inv.addr} requires {inv.f('PATTERN')} "
                                  f"current; {cards[0]} single target",
                                  "none — rules forbid this path", BLOCK)
                    self._stop_basis(f"{ev}/goal", inv.addr)
                    return BLOCK, (inv.addr, cards[0] if cards else None)
        return self.assert_fact(ev, Record(f"{ev}_GOAL",
                {"SUBJECT": s, "PREDICATE": p, "OBJECT": o})), None

    def requirement(self, ev, task_addr, rq_addr, patterns, pat_prefix="RP"):
        adds, pat_addrs = [], []
        for i, (ps, pp, po) in enumerate(patterns, 1):
            a = f"{pat_prefix}{i}"; pat_addrs.append(a)
            adds.append(Record(a, {"TYPE": "TRIPLET_PATTERN", "SUBJECT": ps,
                                   "PREDICATE": pp, "OBJECT": po}))
        adds.append(Record(task_addr, {"TYPE": "TASK",
                                       "REQUIRED_PATTERNS": pat_addrs}))
        self.d.commit(self.d.propose(add=adds))
        rq = Record(rq_addr, {"TYPE": "REQUIREMENT_CONCEPT",
                              "REQUIREMENT": pat_addrs})
        v, _ = self.d.commit(self.d.propose(add=[rq], mark=[(rq_addr, "OPEN")],
                                            authorized_by=task_addr))
        return v

    def req_candidates(self, patterns):
        var = next(t for pat in patterns for t in pat if is_var(t))
        out = []
        for b, _ in self.join(patterns):
            if b.get(var) not in out:
                out.append(b.get(var))
        return out

    def closure_note(self, patterns):
        preds = {p for _, p, _ in patterns}
        for r in self.rules("CLOSURE_POLICY"):
            if r.f("POLICY") == "NO_CLOSURE" and preds & set(r.f("RULE_PREDICATES")):
                return "no closure → absence says nothing → stays OPEN"
        return ""

    def req_bind(self, ev, rq_addr, patterns):
        c = self.req_candidates(patterns)
        if len(c) == 1:
            e = Record(f"{rq_addr}_BIND", {"SUBJECT": rq_addr,
                       "PREDICATE": "REFERS_TO", "OBJECT": c[0],
                       "ROLE": "BOUND_CANDIDATE"})
            v, _ = self.d.commit(self.d.propose(add=[e],
                                                mark=[(rq_addr, "BOUND")]))
            return v, c[0]
        return (NEED if not c else ASK), c

    def install_watch(self, addr, pattern):
        w = Record(addr, {"TYPE": "WATCH", "FIRED": False,
                          "CONDITION_PATTERN": pattern,
                          "CONDITION": lambda n, pat=pattern: bool(self.holds(pat))})
        v, _ = self.d.commit(self.d.propose(add=[w]))
        self.net.active_watches.append(addr)
        return v

    def bind_sample(self, ev, sample):
        props = [(r.f("PREDICATE"), r.f("OBJECT"))
                 for r, _ in self.holds((sample, "?P", "?O"))]
        cands = []
        for r in self.facts():
            s = r.f("SUBJECT")
            if s == sample or s in cands:
                continue
            if props and all(self.holds((s, p, o)) for p, o in props):
                cands.append(s)
        if len(cands) == 1:
            return GO, cands
        if len(cands) > 1:
            self.net.stop(f"{ev}/identity", f"bind {sample} to an entity id",
                          f"candidates {cands}", "discriminating evidence",
                          ASK, can_ask=True,
                          query=f"which of {cands} is {sample}?")
            return ASK, cands
        return NEED, cands
