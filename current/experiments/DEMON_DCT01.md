# DEMON_DCT01 — content-blind network-maintenance trace

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. რატომ ჩატარდა

პირველი Glass World multi-model ტესტი ზედმეტად ახლოს აღმოჩნდა ჩვეულებრივ textual
reasoning-თან. მოდელები პასუხობდნენ წესებზე, მაგრამ არ უვლიდნენ რეალურ მისამართიან
triplet network-ს.

ამიტომ კითხვა შეიცვალა:

> **შეუძლია თუ არა არაფრისმცოდნე დემონს ცოდნის ქსელის მოვლა ისე, რომ დარგის
> შინაარსი საერთოდ არ ესმოდეს?**

ტესტის მიზანი იყო არა ამოცანის ამოხსნა, არამედ:
- provenance-ის შენარჩუნება;
- OPEN-ის დაკარგვის არდაშვება;
- conflict-ის გამოჩენა;
- CURRENT/HISTORICAL დისციპლინა;
- requirement concept-ის მოვლა;
- knowledge credit-ის debt/scope/history-ის დაცვა;
- ზედმეტი ontology invention-ის თავიდან აცილება.

## 1. Cold-test სცენარი

DCT01 შეიცავდა ხუთ მოვლენას:

```text
E1 antipredicate collision
E2 later state with SINGLE_CURRENT_TARGET
E3 explicit REQUIREMENT_CONCEPT
E4 explicit KNOWLEDGE_CREDIT
E5 repayment evidence
```

მოდელებს მიეცათ ერთი და იგივე სტრუქტურული წესები და მოთხოვნა, რომ შინაარსობრივი
common-sense არ გამოეყენებინათ.

## 2. Multi-model დაკვირვება

გავლა გაკეთდა რამდენიმე დამოუკიდებელ LLM-ზე.

მთავარი შედეგი იყო არა ranking, არამედ განმეორებადი failure classes:

### A. Over-promotion
კრედიტის დაფარვის შემდეგ credit-dependent შედეგის ზედმეტად გაძლიერების მცდელობა.

### B. Ontology invention
დემონმა საჭირო ინფრასტრუქტურისთვის ახალი predicate/meta-link თვითონ მოიგონა.

### C. Over-freezing
დროებითი სტატუსის ზედმეტად მუდმივად გამოცხადება.

### D. OPEN loss
ქსელში OPEN დარჩა, მაგრამ final unresolved registry-ში დაიკარგა.

### E. Representation compensation
ზოგმა მოდელმა missing relation-ისთვის დამატებითი მისამართიანი object შექმნა.
ეს თავდაპირველად ზედმეტ complexity-დ ჩანდა, მაგრამ ხელით გავლამ აჩვენა, რომ იგი
რეალურ representational ხვრელს ავსებდა.

საერთო დადებითი შედეგი:

> რამდენიმე დამოუკიდებელმა მოდელმა სწორად დაიცვა პრინციპი
> `credit repaid ≠ credit never existed` და `credit repaid ≠ descendant validated`.

ეს არ ითვლება არქიტექტურის მტკიცებულებად; ეს იყო წესების ოპერაციული გასაგებადობის
სწრაფი შემოწმება.

## 3. პირველი primitive decomposition

multi-model პასუხებიდან გამოიკვეთა DEMON_CORE-ის სამუშაო primitives:

```text
READ
MATCH
COMPARE
PROPOSE
CREATE_ADDRESS
LINK
MARK
CHECK
COMMIT
```

ჰიპოთეზა: domain-specific ქცევა ქსელში უნდა დარჩეს; კოდში მხოლოდ ეს უნივერსალური
მანიპულაცია უნდა დარჩეს.

## 4. პირველი ხელით run — STOP/NEED-მდე

DCT01 primitive-by-primitive გავლაში E2 სუფთად გაიარა, მაგრამ ოთხი STOP გამოჩნდა:

```text
STOP_01 conflict object ვერ მიუთითებდა conflicting records-ზე
STOP_02 requirement concept ვერ მიუთითებდა triplet-pattern-ზე
STOP_03 credit ვერ მიუთითებდა exact missing relation-ზე
STOP_04 repayment ვერ ადარებდა evidence-ს debt-ს
```

თავდაპირველი NEED map:

```text
MISSING_RELATION
MISSING_PATTERN
MISSING_ADDRESS
```

თუმცა ანალიზმა აჩვენა, რომ STOP_02/03/04 ერთი representational პრობლემის სხვადასხვა
გამოვლინება იყო.

## 5. ერთი მცირე დამატება

შემოტანილ იქნა ერთი სამუშაო invariant:

> **ყველა triplet და triplet-pattern არის first-class addressable record.**

ამის შემდეგ იგივე DCT01 თავიდან გავიდა.

## 6. Rerun შედეგი

### E1 — conflict
ჯერ კიდევ STOP:

```text
NEED:
generic record-to-record structural reference
```

conflict object-ს უკვე შეუძლია triplet-record-ების მისამართების ნახვა, მაგრამ
არ არის გაყინული, რომელი კანონიერად არსებული generic meta-relation-ით დაუკავშირდეს მათ.

### E2 — later state
```text
GO
T2 → HISTORICAL
N2 → CURRENT
```

### E3 — requirement concept
addressable patterns-მა ძველი STOP მოხსნა:

```text
RQ1 → REQUIREMENT → RP1
RQ1 → REQUIREMENT → RP2
RQ1 → OPEN
```

**GO**

### E4 — knowledge credit
addressable missing relation/pattern-მა debt-ის ზუსტი მიბმა შესაძლებელი გახადა:

```text
KC1 → CREDIT_FOR → MR1
KC1 → DEBT → MR1
KC1 → SCOPE → SCENE_2
D1 → CREDIT_DEPENDENT
```

**GO**

### E5 — repayment
N3 შეიძლება პირდაპირ შედარდეს მისამართიან debt-pattern-ს:

```text
N3 matches MR1
KC1 → REPAID
KC1 OPEN → RESOLVED
D1 remains CREDIT_DEPENDENT
```

**GO**

## 7. STOP reduction

მანამდე:

```text
4 STOP
```

ერთი ზოგადი representational invariant-ის შემდეგ:

```text
1 STOP
```

ანუ ერთმა მცირე დამატებამ სამი დამოუკიდებლად გამოჩენილი გაჭედვა მოხსნა.

ეს არის მიმდინარე მიზეზი, რის გამოც addressable triplet/pattern შევიდა
[DEMON_CORE_SPEC](../DEMON_CORE_SPEC.md)-ში როგორც WORKING invariant.

## 8. რატომ არ ვხურავთ დარჩენილ STOP-ს ახლავე

დარჩენილი კითხვა:

> რა generic meta-relation-ით მიუთითებს ერთი record სხვა record-ზე?

შესაძლო სახელები შეგნებულად არ არის არჩეული.

ჯერ უნდა ვნახოთ სხვა სცენებშიც განმეორდება თუ არა იგივე NEED. წინააღმდეგ შემთხვევაში
ერთი კონკრეტული conflict-სცენისთვის predicate-ის დამატება იქნებოდა ad-hoc patch.

## 9. მეთოდოლოგიური შედეგი

DCT01-ის ყველაზე მნიშვნელოვანი შედეგი არის არა რომელიმე მოდელის ქულა, არამედ
ახალი სამუშაო რეჟიმი:

```text
RUN
→ NETWORK DELTA
→ STOP MAP
→ NEED MAP
→ add one smallest reusable structure
→ rerun the same case
```

ეს რეჟიმი გადაიტანა დემონის განვითარება „წინასწარ მოვიგონოთ სრული არქიტექტურა“-დან
„გაჭედვამ გვაჩვენოს რა აკლია“-ზე.

## 10. საზღვარი

ეს ექსპერიმენტი არის **architecture probe / internal validation**.

იგი არ ამტკიცებს:
- რომ DEMON_CORE primitives საბოლოოა;
- რომ addressable triplet/pattern უნივერსალური ონტოლოგიური პრინციპია;
- რომ კონკრეტული LLM-ების ქცევა დემონის სწორი იმპლემენტაციაა;
- რომ სისტემა რეალურ ცოდნის დომენზე უკვე მუშაობს.

მისი როლია ისტორიული provenance: რატომ გაჩნდა მიმდინარე ბირთვის კონკრეტული
representation და STOP/NEED მეთოდი.
