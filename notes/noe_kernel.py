"""noe_kernel — Block 0: object field + triplet tables. stdlib only."""
import sqlite3

class Field:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS field(
            addr INTEGER PRIMARY KEY,   -- მისამართი
            tag  TEXT NOT NULL,         -- 'atom' | 'table' | 'triplet' | ...
            tbl  INTEGER,               -- რომელი ცხრილის წევრია (ტრიპლეტებისთვის)
            a INTEGER, b INTEGER, c INTEGER,  -- S,P,O; NULL = OPEN პოზიცია
             val  TEXT)""")  # ატომის მნიშვნელობა / ცხრილის სახელი
        self.db.commit()

    # --- სამი ოპერაცია, რომელიც ნამდვილად უნდა შეეძლოს ---
    def add_object(self, val, tag="atom"):
        cur = self.db.execute(
            "INSERT INTO field(tag, val) VALUES(?,?)", (tag, str(val)))
        self.db.commit()
        return cur.lastrowid

    def new_table(self, name):
        return self.add_object(name, tag="table")

    def add_triplet(self, tbl, s, p, o):          # s/p/o შეიძლება None იყოს = OPEN
        cur = self.db.execute(
            "INSERT INTO field(tag, tbl, a, b, c) VALUES('triplet',?,?,?,?)",
            (tbl, s, p, o))
        self.db.commit()
        return cur.lastrowid

    # --- ორი წაკითხვა, რომელსაც ზემოთა სამი აზრიანს ხდის ---
    def get(self, addr):
        r = self.db.execute(
            "SELECT addr,tag,tbl,a,b,c,val FROM field WHERE addr=?", (addr,)).fetchone()
        return dict(zip(("addr","tag","tbl","s","p","o","val"), r)) if r else None

    def find(self, tbl, s=None, p=None, o=None):  # None = ნებისმიერი
        q, args = "SELECT addr,a,b,c FROM field WHERE tag='triplet' AND tbl=?", [tbl]
        for col, v in (("a",s),("b",p),("c",o)):
            if v is not None: q += f" AND {col}=?"; args.append(v)
        return self.db.execute(q, args).fetchall()


if __name__ == "__main__":
    # პირველი ტესტი: ივლისის megafield-ის RUN-ი, ბლოკირებული შემთხვევის ჩათვლით
    f = Field()
    knowledge  = f.new_table("knowledge")
    apple17    = f.add_object("APPLE-17")
    apple18    = f.add_object("APPLE-18")
    descr_by   = f.add_object("described-by")
    desc17     = f.add_object("DESC-APPLE-17")

    f.add_triplet(knowledge, apple17, descr_by, desc17)
    blocked = f.add_triplet(knowledge, apple18, descr_by, None)   # OPEN პოზიცია

    # RUN 1: (APPLE-17) -[described-by]-> ?      → უნდა იპოვოს
    hit = f.find(knowledge, s=apple17, p=descr_by)
    assert hit and hit[0][3] == desc17, "RUN-1 FAILED"
    print("RUN 1: OK ->", f.get(hit[0][3])["val"])

    # RUN 2: (APPLE-18) -[described-by]-> ?      → OPEN, REQUEST უნდა დაიბადოს
    hit = f.find(knowledge, s=apple18, p=descr_by)
    assert hit and hit[0][3] is None, "RUN-2 FAILED"
    print("RUN 2: BLOCKED, open position at addr", hit[0][0])

    # ჰომოიკონურობის ტესტი: provenance როგორც ტრიპლეტი ტრიპლეტზე
    meta    = f.new_table("meta")
    src     = f.add_object("source")
    session = f.add_object("session-2026-08-24")
    f.add_triplet(meta, blocked, src, session)
    assert f.find(meta, s=blocked), "META FAILED"
    print("META: OK — triplet about a triplet, one address space")