# Experiment 002 — Result, Part 2 (H–N)

> Verbatim result returned by the fresh-chat run.

## H. Directly stored facts used

უშუალოდ supplied field-იდან გამოვიყენეთ:

- `J2_P1 type: terminal`
- **R13:** `J2_P1 → CONNECTED_TO → VIN`
- R13 status = `provisional`
- R13 provenance = `SRC_FIXTURE`
- **R18:** `J2_P1 → EXPOSES_NET → VOUT`
- R18 status = `settled`
- **RR01:** rule scope = terminal
- **RR02:** input predicate = EXPOSES_NET
- **RR03:** required predicate = CONNECTED_TO
- **RR04:** target constraint = SAME_NET
- OPEN_01 status = open

---

## I. Rule-derived consequences

Rule-ით უშუალოდ მიღებული consequence არის:

R18:

`J2_P1 → EXPOSES_NET → VOUT`

plus RR01–RR04

yields required structure:

`J2_P1 → CONNECTED_TO → VOUT`

შემდეგ stored R13-თან შედარება:

`CONNECTED_TO → VIN`

აჩვენებს explicit SAME_NET constraint-ის დარღვევას.

ეს consequence rule-derived არის და არა ახალი evidence.

---

## J. Other inference

Rule application-ის გარეთ მხოლოდ შემდეგი inference გვჭირდება:

1. **R13 არის პრაქტიკულად უკეთესი revision candidate**, რადგან ის provisional-ია, ხოლო R18 settled.
2. ერთი target-ის შეცვლა R13-ში არის უფრო მცირე edit, ვიდრე უფრო ფართო field-ის გადაკეთება.

მაგრამ მეორე პუნქტიც მნიშვნელოვანია:

**field-ში არ არსებობს explicit rule `settled > provisional` revision precedence-ისთვის.**

ამიტომ ეს repair-selection inference-ია და არა rule-derived fact.

---

## K. Remaining structural uncertainty / new OPENs

J2_P1 mismatch-ის დასადგენად **დამატებითი structural constraint აღარ აკლია.**

წინა ტიპის კითხვები აქ უკვე explicit-ადაა დახურული:

- terminal granularity არსებობს;
- `EXPOSES_NET ↔ CONNECTED_TO` consistency rule არსებობს;
- SAME_NET მოთხოვნაც explicit-ია.

მაგრამ დარჩა ერთი სხვა, repair governance-ის structural uncertainty:

> როცა inconsistent relations განსხვავებული status-ებითაა (`settled` vs `provisional`), რომელი relation უნდა შეიცვალოს?

შეიძლება აღინიშნოს ახალი unresolved requirement, მაგალითად:

```
OPEN_STRUCT_01:

Need explicit revision-precedence policy for conflicting relations
with different statuses.

Example question:
Does settled relation take precedence over provisional relation?

status: unresolved
```

ეს **არ არის საჭირო mismatch-ის დასამტკიცებლად**.

ეს საჭიროა მხოლოდ იმისათვის, რომ repair-ის არჩევანიც გახდეს სრულად deterministic.

---

## L. Relations changed

Proposed revision-ში იცვლება მხოლოდ:

**R13**

```
FROM:
J2_P1 → CONNECTED_TO → VIN

TO:
J2_P1 → CONNECTED_TO → VOUT
```

უცვლელი metadata:

`network: NET_CONNECTIVITY`  
`status: provisional`  
`provenance: SRC_FIXTURE`

---

## M. Relations explicitly untouched

უცვლელი რჩება:

- **R01–R12**
- **R14–R24**
- **RR01–RR04**
- **OPEN_01**

განსაკუთრებით untouched:

`R18: J2_P1 → EXPOSES_NET → VOUT`

`R19: J2_P2 → EXPOSES_NET → GND`

`R14: J2_P2 → CONNECTED_TO → GND`

`R21: VOUT → MEASURED_AS → M_VOUT`

`R23: J2_P1 → HAS_ROLE → OUTPUT_TERMINAL`

და:

`OPEN_01: U1 → ENABLE_CONTROLLED_BY → EN_PATH`

---

## N. Final compact verdict

**Smallest cut:**

`{J2_P1:type=terminal, R13, R18, RR01–RR04}`

**Formal rule path:**

`terminal`  
`+ EXPOSES_NET(J2_P1,VOUT)`  
`+ REQUIRED_PREDICATE(CONNECTED_TO)`  
`+ SAME_NET`  
`⇒ CONNECTED_TO(J2_P1,VOUT)`

Stored:

`CONNECTED_TO(J2_P1,VIN)`

Therefore:

**R13 and R18 are formally inconsistent under RULE_TERMINAL_EXPOSE_CONNECT.**

**Minimal proposed repair:**

`R13 target: VIN → VOUT`

**Repair of the inconsistency:** required.  
**Choice to modify R13 specifically:** conditional on an unstated revision-precedence policy, although its `provisional` status makes it the natural minimal candidate.

**OPEN_01:** remains open.

**No additional constraint is needed to prove the mismatch.**

**One new structural requirement remains only for deterministic repair selection:** an explicit precedence rule for conflicting `settled` and `provisional` relations.
