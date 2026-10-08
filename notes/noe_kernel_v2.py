"""noe_kernel v2 — ჰომოიკონური საცავი (ნაწილი 1, დემონის გარეშე). stdlib only.

რა უდევს საფუძვლად (თითო წესს თავისი მიზეზი აქვს):
  D1  ობიექტი = შიშველი ID. ის შეხვედრის წერტილია, ამიტომ თავად არაფერს ატარებს.
  D2  ტრიპლეტი = (id, s, p, o); s/o = NULL -> OPEN. id საერთო სივრციდანაა,
      რომ კავშირზეც შეიძლებოდეს კავშირის დადება.
  D3  თითო პრედიკატს თავისი ცხრილი t_<ID>, რომ მასზე მოხვედრისას ქსელი მაშინვე ხელთ იყოს.
      p სვეტი ზედმეტია და ამიტომ საკონტროლოდ რჩება.
  D4  ids(id, kind, home): ტრიპლეტიდან ან ნიმუშიდან მის ცხრილამდე (შებრუნებული სახელური).
  D5  მოდალობა = ველი m_<P>(id, pattern) + ბმის პრედიკატი P (ნიმუში -> ობიექტი).
      სახელები (P = 3) პირველი მოდალობაა; ხმა, სუნი და გაზომვა იმავე ფორმისაა.
  D6  ყოველი პრედიკატი NOT-წყვილით იბადება; ბმა "ანტი"-ს ცხრილში იწერება.
  D7  networks_of = ცხრილების გადახედვა (ინდექსი მერე, თუ ნელი გახდება).
  D8  ხელმოწერა გადადებულია. journal ველის გარეთაა, ცოდნა არ არის:
      ის ნაწილი 2-ისთვისაა, როცა დემონები ჩვენ ვართ და ჩვენი სვლები იწერება.
  +   გამოთვლადი პრედიკატი: იმავე ID-ის უკან ფუნქცია დგას (ALU). მნიშვნელობები
      ნაკადიდან მოდის (V) და ველში არ ინახება.
  +   ask(): შენახულ სამყაროში არყოფნა = უცნობი (None);
      გამოთვლად სამყაროში არყოფნა = უარყოფა (False).
  +   disable/enable: ცხრილის დროებით გათიშვა (თრობა / RULE OFF), წაშლის გარეშე.
  +   verify/repair: აღდგება მხოლოდ ის, რაც დუბლირებულია; დანარჩენს მხოლოდ ვაჩვენებთ.
"""
import json
import re
import sqlite3
import time

ANTI, NOT_ANTI, NAME, NOT_NAME = 1, 2, 3, 4   # დაბადების მისამართები


class V:
    """მნიშვნელობა ნაკადიდან (მაგ. 15). ველში არ ინახება."""
    __slots__ = ("x",)

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"V({self.x})"


class Field:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS ids("
                        "id INTEGER PRIMARY KEY, kind TEXT NOT NULL, home INTEGER)")
        self.db.execute("CREATE TABLE IF NOT EXISTS journal("
                        "seq INTEGER PRIMARY KEY, ts REAL, op TEXT, args TEXT, result TEXT, note TEXT)")
        self.computed = {}   # P -> fn(s, o) -> bool   (ALU; კოდი ბაზის გარეთ ცხოვრობს)
        self.off = set()     # გათიშული პრედიკატები
        self.preds = {int(m.group(1)) for (n,) in self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")
            for m in [re.fullmatch(r"t_(\d+)", n)] if m}
        if not self.db.execute("SELECT 1 FROM ids WHERE id=1").fetchone():
            self._genesis()
        self.db.commit()

    # ------------------------------------------------------------ შიდა
    def _new_id(self, kind, home=None):
        return self.db.execute("INSERT INTO ids(kind, home) VALUES(?,?)", (kind, home)).lastrowid

    def _make_table(self, P):
        P = int(P)
        self.db.execute(f"CREATE TABLE t_{P}(id INTEGER PRIMARY KEY, s INTEGER, "
                        f"p INTEGER NOT NULL, o INTEGER)")
        self.db.execute(f"CREATE INDEX ix_t_{P}_s ON t_{P}(s)")
        self.db.execute(f"CREATE INDEX ix_t_{P}_o ON t_{P}(o)")
        self.preds.add(P)

    def _put(self, s, p, o):
        if p not in self.preds:
            raise ValueError(f"{p} პრედიკატი არ არის (ცხრილი არ აქვს)")
        tid = self._new_id("tri", home=p)
        self.db.execute(f"INSERT INTO t_{int(p)}(id, s, p, o) VALUES(?,?,?,?)", (tid, s, p, o))
        return tid

    def _log(self, op, args, result=None, note=None):
        self.db.execute("INSERT INTO journal(ts, op, args, result, note) VALUES(?,?,?,?,?)",
                        (time.time(), op, json.dumps(args, default=repr, ensure_ascii=False),
                         json.dumps(result, default=repr, ensure_ascii=False), note))

    def _exists(self, x):
        return self.db.execute("SELECT 1 FROM ids WHERE id=?", (x,)).fetchone() is not None

    def _pattern_id(self, M, pattern):
        r = self.db.execute(f"SELECT id FROM m_{int(M)} WHERE pattern=?", (pattern,)).fetchone()
        if r:
            return r[0]
        pid = self._new_id("pat", home=M)
        self.db.execute(f"INSERT INTO m_{int(M)}(id, pattern) VALUES(?,?)", (pid, pattern))
        return pid

    def _genesis(self):
        a, na = self._new_id("obj"), self._new_id("obj")      # 1 ანტი, 2 NOT_ანტი
        self._make_table(a); self._make_table(na)
        n, nn = self._new_id("obj"), self._new_id("obj")      # 3 არის-სახელი, 4 NOT_
        self._make_table(n); self._make_table(nn)
        self.db.execute(f"CREATE TABLE m_{n}(id INTEGER PRIMARY KEY, pattern TEXT NOT NULL)")
        self.db.execute(f"CREATE INDEX ix_m_{n}_pat ON m_{n}(pattern)")
        self._put(a, a, na)                                   # 5: ანტი იკეტება თავის თავზე
        self._put(n, a, nn)                                   # 6
        assert (a, na, n, nn) == (ANTI, NOT_ANTI, NAME, NOT_NAME)
        for obj, text in ((a, "ანტი"), (n, "არის-სახელი")):
            self._put(self._pattern_id(n, text), n, obj)
        self._log("genesis", [], "1-6")

    # ------------------------------------------------------------ ჩაწერა
    def new_object(self, note=None):
        oid = self._new_id("obj")
        self._log("new_object", [], oid, note)
        self.db.commit()
        return oid

    def new_predicate(self, name=None, note=None):
        P, NP = self._new_id("obj"), self._new_id("obj")
        self._make_table(P); self._make_table(NP)
        self._put(P, ANTI, NP)
        if name is not None:
            self._put(self._pattern_id(NAME, name), NAME, P)
        self._log("new_predicate", [name], [P, NP], note)
        self.db.commit()
        return P

    def add(self, s, p, o, note=None):
        """s/o = None -> OPEN პოზიცია."""
        tid = self._put(s, p, o)
        self._log("add", [s, p, o], tid, note)
        self.db.commit()
        return tid

    def new_modality(self, name, note=None):
        """ახალი ველი (ხმა, სუნი, გაზომვა...) + მისი ბმის პრედიკატი."""
        M = self.new_predicate(name, note)
        self.db.execute(f"CREATE TABLE m_{M}(id INTEGER PRIMARY KEY, pattern TEXT NOT NULL)")
        self.db.execute(f"CREATE INDEX ix_m_{M}_pat ON m_{M}(pattern)")
        self.db.commit()
        return M

    def add_pattern(self, M, pattern, obj=None, note=None):
        """ნიმუში -> ობიექტი. obj = None: "მოვისმინე, ობიექტი უცნობია" (OPEN).
        ერთი და იგივე ნიშანი ერთი ნიმუშია; ბმები კი იმდენი, რამდენიც საჭიროა (ომონიმი)."""
        pid = self._pattern_id(M, pattern)
        tid = self._put(pid, M, obj)
        self._log("add_pattern", [M, pattern, obj], [pid, tid], note)
        self.db.commit()
        return pid

    def bind_name(self, obj, text, note=None):
        return self.add_pattern(NAME, text, obj, note)

    def register_computed(self, P, fn):
        """P-ს უკან ფუნქცია (ALU). NOT_P ავტომატურად მისი უარყოფაა."""
        self.computed[P] = fn
        self._log("register_computed", [P, getattr(fn, "__name__", "fn")])

    def disable(self, P, note=None):
        self.off.add(P); self._log("disable", [P], None, note)

    def enable(self, P, note=None):
        self.off.discard(P); self._log("enable", [P], None, note)

    # ------------------------------------------------------------ წაკითხვა
    def get(self, x):
        r = self.db.execute("SELECT kind, home FROM ids WHERE id=?", (x,)).fetchone()
        if not r:
            return None
        kind, home = r
        d = {"id": x, "kind": kind, "home": home}
        if kind == "tri":
            row = self.db.execute(f"SELECT s, p, o FROM t_{int(home)} WHERE id=?", (x,)).fetchone()
            if row:
                d.update(zip(("s", "p", "o"), row))
        elif kind == "pat":
            row = self.db.execute(f"SELECT pattern FROM m_{int(home)} WHERE id=?", (x,)).fetchone()
            if row:
                d["pattern"] = row[0]
        d["predicate"] = x in self.preds
        return d

    def find(self, p, s=None, o=None, note=None):
        """(s, p, o) ნიმუშით; None = ნებისმიერი. გათიშულ ცხრილს არაფერი ამოაქვს."""
        if p in self.off or p not in self.preds:
            rows = []
        else:
            q, args = f"SELECT id, s, o FROM t_{int(p)} WHERE 1=1", []
            if s is not None: q += " AND s=?"; args.append(s)
            if o is not None: q += " AND o=?"; args.append(o)
            rows = self.db.execute(q, args).fetchall()
        self._log("find", [p, s, o], rows, note)
        return rows

    def anti_of(self, P):
        r = self.db.execute(f"SELECT o FROM t_{ANTI} WHERE s=?", (P,)).fetchone()
        if r:
            return r[0]
        r = self.db.execute(f"SELECT s FROM t_{ANTI} WHERE o=?", (P,)).fetchone()
        return r[0] if r else None

    def ask(self, p, s, o, note=None):
        """True / False / None.
        მნიშვნელობები (V): გამოთვლა, დახურული სამყარო — არყოფნა = False.
        ობიექტები: შენახული სამყარო — P-ს რიგი True, NOT_P-ს რიგი False, არცერთი = None (უცნობი)."""
        if isinstance(s, V) or isinstance(o, V):
            if p in self.computed:
                ans = bool(self.computed[p](s.x, o.x))
            else:
                np_ = self.anti_of(p)
                ans = (not bool(self.computed[np_](s.x, o.x))) if np_ in self.computed else None
        elif p in self.off:
            ans = None
        elif self.db.execute(f"SELECT 1 FROM t_{int(p)} WHERE s=? AND o=?", (s, o)).fetchone():
            ans = True
        else:
            np_ = self.anti_of(p)
            hit = np_ is not None and np_ not in self.off and self.db.execute(
                f"SELECT 1 FROM t_{int(np_)} WHERE s=? AND o=?", (s, o)).fetchone()
            ans = False if hit else None
        self._log("ask", [p, s, o], ans, note)
        return ans

    def lookup(self, M, pattern, note=None):
        """ზუსტი დამთხვევით ნიმუში -> ობიექტები (None = OPEN ბმა).
        მსგავსებით ცნობა აქ არ არის: ის დემონის საქმეა (ნაწილი 2)."""
        r = self.db.execute(f"SELECT id FROM m_{int(M)} WHERE pattern=?", (pattern,)).fetchone()
        objs = [o for (_, _, o) in self.find(M, s=r[0])] if r else []
        self._log("lookup", [M, pattern], objs, note)
        return objs

    def names_of(self, obj):
        return [self.db.execute(f"SELECT pattern FROM m_{NAME} WHERE id=?", (s,)).fetchone()[0]
                for (_, s, _) in self.db.execute(f"SELECT id, s, o FROM t_{NAME} WHERE o=?", (obj,))]

    def networks_of(self, obj, note=None):
        nets = [P for P in sorted(self.preds) if P not in self.off and self.db.execute(
            f"SELECT 1 FROM t_{P} WHERE s=? OR o=? LIMIT 1", (obj, obj)).fetchone()]
        self._log("networks_of", [obj], nets, note)
        return nets

    # ------------------------------------------------------------ მთლიანობა
    def verify(self):
        """რას ვხედავთ: საკონტროლო (p ≠ ცხრილი), სახლი (ids.home ≠ ცხრილი),
        ჩამოკიდებული მისამართი, დაკარგული ტრიპლეტი, უწყვილო პრედიკატი.
        რისი დანახვა არ შეგვიძლია: s/o-ს შეცვლა სხვა არსებულ ID-ზე — ის ერთ ძაფზე კიდია."""
        problems, present = [], set()
        for P in sorted(self.preds):
            for tid, s, p, o in self.db.execute(f"SELECT id, s, p, o FROM t_{P}"):
                present.add(tid)
                if p != P:
                    problems.append(("checksum", P, tid, p))
                r = self.db.execute("SELECT kind, home FROM ids WHERE id=?", (tid,)).fetchone()
                if r != ("tri", P):
                    problems.append(("home", P, tid, r))
                for x in (s, o):
                    if x is not None and not self._exists(x):
                        problems.append(("dangling", P, tid, x))
            if self.anti_of(P) is None:
                problems.append(("unpaired", P))
        for tid, home in self.db.execute("SELECT id, home FROM ids WHERE kind='tri'").fetchall():
            if tid not in present:                 # ids ამბობს "არსებობს", არცერთ ცხრილში არ არის
                problems.append(("lost", home, tid))
        return problems

    def repair(self):
        """აღადგენს მხოლოდ დუბლირებულს: p-ს და home-ს ცხრილის ფიზიკური ადგილიდან.
        დანარჩენი (dangling, lost, unpaired) რჩება და ბრუნდება როგორც აღუდგენელი."""
        fixed, left = [], []
        for prob in self.verify():
            kind, P, tid = prob[0], prob[1], (prob[2] if len(prob) > 2 else None)
            if kind == "checksum":
                self.db.execute(f"UPDATE t_{P} SET p=? WHERE id=?", (P, tid)); fixed.append(prob)
            elif kind == "home":
                self.db.execute("UPDATE ids SET kind='tri', home=? WHERE id=?", (P, tid)); fixed.append(prob)
            else:
                left.append(prob)
        self._log("repair", [], {"fixed": len(fixed), "left": len(left)})
        self.db.commit()
        return fixed, left

    def label(self, x):
        if x is None:
            return "OPEN"
        n = self.names_of(x)
        return f"{x}:{'/'.join(n)}" if n else f"{x}"


# ================================================================ ტესტები
if __name__ == "__main__":
    f = Field()
    ok = lambda name, cond: print(("OK   " if cond else "FAIL ") + name) or cond
    results = []

    # T1 დაბადება
    results.append(ok("T1 დაბადება: 1-6, ანტი იკეტება თავის თავზე, verify სუფთაა",
        f.anti_of(ANTI) == NOT_ANTI and f.anti_of(NAME) == NOT_NAME
        and f.names_of(ANTI) == ["ანტი"] and f.names_of(NAME) == ["არის-სახელი"]
        and f.verify() == []))

    # T2 ძველი ბირთვის სამი ტესტი ახალ სქემაზე
    apple17, apple18, desc17 = f.new_object(), f.new_object(), f.new_object()
    described_by = f.new_predicate("აღწერილია")
    f.add(apple17, described_by, desc17)
    blocked = f.add(apple18, described_by, None)
    source = f.new_predicate("წყარო")
    session = f.new_object()
    f.add(blocked, source, session)          # ტრიპლეტი ტრიპლეტზე
    results.append(ok("T2 RUN1 / RUN2(OPEN) / META",
        f.find(described_by, s=apple17)[0][2] == desc17
        and f.find(described_by, s=apple18)[0][2] is None
        and f.find(source, s=blocked) != []))

    # T3 ომონიმი და სინონიმი: "თითი" = ხელის თითი და ფეხის თითი
    finger, toe, hand, phalanx, belly = (f.new_object() for _ in range(5))
    f.bind_name(finger, "თითი"); f.bind_name(toe, "თითი"); f.bind_name(finger, "finger")
    results.append(ok("T3 ერთი სიტყვა -> ორი ობიექტი; ერთ ობიექტს -> ორი სახელი",
        sorted(f.lookup(NAME, "თითი")) == sorted([finger, toe])
        and sorted(f.names_of(finger)) == ["finger", "თითი"]))

    # T4 ქსელში სიარული და ობიექტის ყველა ქსელი
    part_of = f.new_predicate("არის-ნაწილი")
    f.add(finger, part_of, hand); f.add(phalanx, part_of, finger)
    up = [o for (_, _, o) in f.find(part_of, s=finger)]
    down = [s for (_, s, _) in f.find(part_of, o=finger)]
    results.append(ok("T4 თითი -> ზემოთ ხელი, ქვემოთ ფალანგა; networks_of",
        up == [hand] and down == [phalanx] and f.networks_of(finger) == [NAME, part_of]))

    # T5 შენახული და გამოთვლადი სამყარო
    lt = f.new_predicate("ნაკლებია")
    f.register_computed(lt, lambda a, b: a < b)
    results.append(ok("T5 ALU: 15<16 True, NOT(15<16) False; შენახულში 'თითი მუცლის ნაწილი' = None (უცნობი)",
        f.ask(lt, V(15), V(16)) is True
        and f.ask(f.anti_of(lt), V(15), V(16)) is False
        and f.ask(part_of, finger, belly) is None))
    f.add(finger, f.anti_of(part_of), belly)
    results.append(ok("T5b NOT_-ცხრილში ჩაწერის შემდეგ იგივე კითხვა = False",
        f.ask(part_of, finger, belly) is False))

    # T6 თრობა: ცხრილის გათიშვა წაშლის გარეშე
    f.disable(part_of)
    off_view = (f.find(part_of, s=finger), f.networks_of(finger))
    f.enable(part_of)
    results.append(ok("T6 გათიშვისას ქსელი არ ჩანს, ჩართვისას ბრუნდება ხელუხლებლად",
        off_view == ([], [NAME, f.anti_of(part_of)]) and f.find(part_of, s=finger) != []))

    # T7 იუპიტერი: დაზიანება და აღდგენა
    row = f.find(part_of, s=finger)[0][0]
    f.db.execute(f"UPDATE t_{part_of} SET p=999 WHERE id=?", (row,))       # p დაზიანდა
    f.db.execute("UPDATE ids SET home=777 WHERE id=?", (row,))             # home დაზიანდა
    seen = f.verify()
    fixed, left = f.repair()
    results.append(ok("T7 დუბლირებული აღდგა: p და home ცხრილის ადგილიდან",
        {p[0] for p in seen} == {"checksum", "home"} and len(fixed) == 2 and f.verify() == []))
    f.db.execute(f"UPDATE t_{part_of} SET o=? WHERE id=?", (belly, row))   # o შეიცვალა სხვა არსებულ ID-ზე
    results.append(ok("T7b ერთ ძაფზე დაკიდებული (o) ვერ დავინახეთ — ეს ღიად ჩაწერილი საზღვარია",
        f.verify() == []))
    f.db.execute(f"UPDATE t_{part_of} SET o=? WHERE id=?", (hand, row))    # ხელით ვაბრუნებთ ტესტისთვის

    # T8 ხმის მოდალობა: მოვისმინე, ობიექტი უცნობია
    sound = f.new_modality("ხმა")
    f.add_pattern(sound, "კრა-კრა")                                        # obj = None -> OPEN
    results.append(ok("T8 ხმის ველი: 'კრა-კრა' -> OPEN ბმა",
        f.lookup(sound, "კრა-კრა") == [None]))

    # T9 ჟურნალი
    n = f.db.execute("SELECT COUNT(*) FROM journal").fetchone()[0]
    results.append(ok(f"T9 ჟურნალში {n} სვლაა (ნაწილი 2-ის ფირი)", n > 30))

    print()
    print("ყველა მწვანეა" if all(results) else "ზოგი ტესტი ჩავარდა")
