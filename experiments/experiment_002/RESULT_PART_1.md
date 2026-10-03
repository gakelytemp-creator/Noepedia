# Experiment 002 — Result, Part 1 (A–G)

> Verbatim result returned by the fresh-chat run.

## A. Smallest task-specific cut

J2_P1-ის consistency-ის შესამოწმებლად მინიმალური cut არის:

- **Object fact:** `J2_P1 type: terminal`
- **R13:** `J2_P1 → CONNECTED_TO → VIN` — provisional
- **R18:** `J2_P1 → EXPOSES_NET → VOUT` — settled
- **RR01–RR04:** `RULE_TERMINAL_EXPOSE_CONNECT`-ის სრული explicit specification

ანუ relation-level cut:

`{R13, R18, RR01, RR02, RR03, RR04}`

და დამატებით საჭიროა supplied object typing:

`J2_P1 : terminal`

**R21 (`VOUT → MEASURED_AS → 5.01 V`) საჭირო არ არის consistency check-ისთვის.**  
**R23 (`HAS_ROLE → OUTPUT_TERMINAL`) ასევე საჭირო არ არის.**

---

## B. Explicit reconstruction

Stored field უშუალოდ გვაძლევს:

`J2_P1 —EXPOSES_NET→ VOUT`  `[R18]`

და:

`J2_P1 —CONNECTED_TO→ VIN`  `[R13]`

ასევე:

`J2_P1` არის `terminal`.

Rule structure ამბობს, რომ terminal-ისთვის `EXPOSES_NET` განსაზღვრავს იმავე net-ზე აუცილებელ `CONNECTED_TO` relation-ს.

ამიტომ R18-დან rule-ის გამოყენებით მოთხოვნილი სტრუქტურა არის:

`J2_P1 —CONNECTED_TO→ VOUT`

მაგრამ stored field-ში გვაქვს:

`J2_P1 —CONNECTED_TO→ VIN`

სადაც target განსხვავდება.

---

## C. Rule application path

ზუსტი explicit rule path:

**1. Scope**

RR01:

`RULE_TERMINAL_EXPOSE_CONNECT → RULE_SCOPE → terminal`

J2_P1 არის `terminal`, ამიტომ rule მასზე ვრცელდება.

**2. Input predicate**

RR02:

`RULE_TERMINAL_EXPOSE_CONNECT → INPUT_PREDICATE → EXPOSES_NET`

R18 გვაძლევს:

`J2_P1 → EXPOSES_NET → VOUT`

აქ:

`T = J2_P1`  
`X = VOUT`

**3. Required predicate**

RR03:

`RULE_TERMINAL_EXPOSE_CONNECT → REQUIRED_PREDICATE → CONNECTED_TO`

ამიტომ საჭიროა:

`J2_P1 → CONNECTED_TO → VOUT`

**4. Same-target constraint**

RR04:

`RULE_TERMINAL_EXPOSE_CONNECT → TARGET_CONSTRAINT → SAME_NET`

ამიტომ required `CONNECTED_TO` target უნდა იყოს იგივე `VOUT`.

**5. Stored comparison**

R13 ამბობს:

`J2_P1 → CONNECTED_TO → VIN`

ანუ:

`VIN ≠ VOUT`

როგორც ცალკე objects supplied field-ში.

შედეგად explicit operational rule-ის მიხედვით R13 და R18 structurally inconsistent არიან.

---

## D. Formal mismatch

**დიახ — formal mismatch არსებობს.**

Mismatch pair არის:

- **R18:** `J2_P1 → EXPOSES_NET → VOUT`
- **R13:** `J2_P1 → CONNECTED_TO → VIN`

და mismatch-ს ფორმალურად წარმოქმნის:

`RR01 + RR02 + RR03 + RR04`

ეს აღარ არის მხოლოდ coherence preference.

Supplied rule პირდაპირ მოითხოვს:

`EXPOSES_NET(J2_P1,VOUT)`  
`⇒ CONNECTED_TO(J2_P1,VOUT)`

ხოლო stored R13 სხვა target-ს შეიცავს.

---

## E. Minimal revision

ყველაზე მცირე proposed edit არის მხოლოდ **R13-ის target-ის შეცვლა**:

```
R13:

FROM:
J2_P1 → CONNECTED_TO → VIN

TO:
J2_P1 → CONNECTED_TO → VOUT

network: NET_CONNECTIVITY
status: provisional
provenance: SRC_FIXTURE
```

ინარჩუნებს:

- relation ID: `R13`
- predicate: `CONNECTED_TO`
- network: `NET_CONNECTIVITY`
- status: `provisional`
- provenance: `SRC_FIXTURE`

იცვლება მხოლოდ ერთი field:

`target: VIN → VOUT`

---

## F. Status of the revision

აქ ორი დონე უნდა გაიმიჯნოს.

**Mismatch-ის გამოსწორება — required.**

Supplied rule-ის პირობებში არსებული წყვილი:

`R18 + R13`

ერთად დაუშვებელია.

მაგრამ **ზუსტად R13-ის შეცვლა** ყველა შესაძლო repair-იდან ფორმალურად ერთადერთი არ არის, რადგან field-ში არ არის explicit revision-priority rule, რომელიც ამბობს:

> provisional relation აუცილებლად უნდა შეიცვალოს settled relation-ის ნაცვლად.

თეორიულად R18-ის შეცვლაც მოხსნიდა კონკრეტულ conflict-ს.

ამიტომ ზუსტი კლასიფიკაციაა:

**proposed repair `R13: VIN → VOUT` — conditional as the choice of which stored relation to revise, but a repair of the inconsistency itself is required.**

ამ არჩევანს ძლიერად მხარს უჭერს supplied metadata:

- R13 = provisional
- R18 = settled

მაგრამ metadata-ს precedence rule ცალკე explicit-ად არ არის მოცემული.

---

## G. OPEN_01 after the task

**OPEN_01 რჩება open.**

`U1 → ENABLE_CONTROLLED_BY → EN_PATH`

Supplied field თვითონაც ამბობს:

> No relation in the current target task supplies evidence about EN_PATH.

J2_P1-ის consistency repair არ იძლევა არც relation-ს და არც rule-derived consequence-ს `EN_PATH`-ის შესახებ.

შედეგი:

`OPEN_01: unchanged, open`
