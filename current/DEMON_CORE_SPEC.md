# DEMON_CORE_SPEC — არაფრისმცოდნე დემონის ბირთვი

**Status: WORKING SPECIFICATION**  
**Date: 2026-10-16**

## 0. დანიშნულება

დემონი არის ცოდნის ქსელის ინფრასტრუქტურული ოპერატორი.

მას არ უნდა ესმოდეს დარგის შინაარსი და არ უნდა იცოდეს, რას ნიშნავს კონკრეტული
ობიექტი, პრედიკატი ან მოვლენა. ქსელიდან რომ ამოვიღოთ, იგი უნდა დარჩეს თითქმის
არაფრისმცოდნე — დარჩეს მხოლოდ ცოდნის სისტემასთან მუშაობის უნივერსალური იარაღები.

მეტაფორა: დემონი არის კომუნალური მუშაკი. მან არ იცის ქალაქის მეტაბოლიზმი; მან იცის
როგორ შეინარჩუნოს ინფრასტრუქტურა ისეთ მდგომარეობაში, რომ ქალაქმა საკუთარი ცხოვრება
გააგრძელოს.

მისი ძირითადი მოვალეობაა ქსელმა ცვლილებისას არ დაკარგოს:
- რა იცოდა;
- რა არ იცოდა;
- რა იყო OPEN;
- სად იყო CONFLICT;
- სად აიღო knowledge credit;
- რის საფუძველზე გაჩნდა თითოეული ჩანაწერი.

## 1. რას ხედავს დემონი

დემონი მუშაობს მხოლოდ მისამართიან სტრუქტურებთან:

```text
OBJECT
PREDICATE
TRIPLET_RECORD
TRIPLET_PATTERN
STATUS
PROVENANCE
SCOPE
TIME
RULE
OPEN
CONFLICT
REQUIREMENT_CONCEPT
KNOWLEDGE_CREDIT
```

ტოკენების სახელებიდან დამატებითი მნიშვნელობის გამოგონება აკრძალულია.

## 2. Representation invariant

მიმდინარე სამუშაო invariant:

> **ყველა triplet და triplet-pattern არის საკუთარი მისამართის მქონე record და
> შეიძლება თვითონ გახდეს სხვა relation-ის სამიზნე.**

მაგალითი:

```text
TR17
SUBJECT   → O7
PREDICATE → P5
OBJECT    → O9
TYPE      → TRIPLET_RECORD
```

pattern:

```text
RP1
SUBJECT   → X
PREDICATE → P3
OBJECT    → O2
TYPE      → TRIPLET_PATTERN
```

ეს invariant გაჩნდა არა წინასწარი დიზაინიდან, არამედ DCT01-ის ხელით გავლაში:
მის გარეშე requirement concept, knowledge-credit debt და repayment matching
ერთსა და იმავე representational ხვრელში ჩერდებოდა.

## 3. Primitive operations v0.1

დემონის ბირთვს ამ ეტაპზე აქვს ცხრა primitive operation:

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

### READ
მისამართიანი ჩანაწერის წაკითხვა. `NOT_FOUND` არ ნიშნავს არარსებობას.

### MATCH
pattern-ის შესაბამისი candidate set-ის პოვნა. `Cand = ∅` თავისით შეუძლებლობა არ არის.

### COMPARE
სტრუქტურების შედარება მხოლოდ ქსელში მოცემული rule/certificate-ის მიხედვით.

### PROPOSE
ქსელის შესაძლო delta-ს მონახაზი. ჯერ არაფერს ცვლის.

### CREATE_ADDRESS
ახალი მისამართიანი სტრუქტურის შექმნა მხოლოდ მოქმედი წესის explicit უფლებით.

### LINK
უკვე არსებული ან კანონიერად შექმნილი მისამართების დაკავშირება.

### MARK
სტატუსის ცვლილება წაშლის გარეშე: CURRENT, HISTORICAL, OPEN,
CONFLICTED, CREDIT_DEPENDENT, REPAID, REJECTED.

### CHECK
proposed delta-ს invariant-ებზე გატარება.

### COMMIT
მხოლოდ `CHECK = PASS`-ის შემდეგ ქსელის ცვლილება.

## 4. Commit gate

ყოველი proposed delta commit-მდე ამოწმებს მინიმუმ:

1. provenance preserved?
2. supported record silently deleted?
3. OPEN silently closed?
4. conflict hidden?
5. unauthorized ontology created?
6. credit promoted to ordinary knowledge?
7. historical state erased?
8. scope escaped?
9. unnecessary change introduced?

დამატებითი მკაცრი წესი:

> **დემონის დუმილი არ ნიშნავს მხარდაჭერას.**

`NO VETO ≠ SUPPORTED`.

ასევე დემონს შეუძლია შეაჩეროს სტატუსის უკანონო აწევა, მაგრამ არ უნდა მოკლას კანონიერად
მონიშნული provisional/credit-dependent კონსტრუქცია.

## 5. Knowledge credit

Knowledge credit არის დროებითი კონსტრუქციული უფლება, რომელიც მოძრაობას აგრძელებს
იქ, სადაც კონკრეტული relation ჯერ supported არ არის.

აუცილებლად ინახება:

```text
TYPE → KNOWLEDGE_CREDIT
CREDIT_FOR → exact missing relation/pattern
DEBT → exact missing relation/pattern
SCOPE → local scope
PROVENANCE → source
STATUS → OPEN
```

კრედიტით მიღებული ყველა შედეგი რჩება `CREDIT_DEPENDENT`.

```text
credit repaid
≠
credit never existed

credit repaid
≠
all descendants become ordinary knowledge
```

independent re-grounding-ის გარეშე credit-dependent სტატუსი არ იხსნება.

## 6. Requirement concept

Requirement concept ინახავს რას ითხოვს ქსელი და არა იმას, რა იპოვა.

```text
RQ1
TYPE → REQUIREMENT_CONCEPT
REQUIREMENT → RP1
REQUIREMENT → RP2
STATUS → OPEN
```

binding დასაშვებია მხოლოდ ყველა მოთხოვნის მხარდაჭერისას.

`candidate not found ≠ candidate does not exist`.

Requirement concept-ის ზოგადი birth rule ამ ეტაპზე **OPEN** რჩება.

## 7. STOP / NEED სამუშაო რეჟიმი

დემონი მიდის იმდენად შორს, რამდენადაც კანონიერად შეუძლია.

ოთხი მდგომარეობა:

```text
GO
ASK
BLOCK
NEED
```

- **GO** — საკმარისი სტრუქტურა აქვს გასაგრძელებლად.
- **ASK** — აკლია გარე ფაქტი, მაგრამ შეუძლია ზუსტი, დაშვებული query.
- **BLOCK** — მოქმედი rule/closure ამ გზას კრძალავს.
- **NEED** — აკლია თვით ქსელის სამუშაო სტრუქტურა; სწორი query ჯერ ვერ ყალიბდება.

STOP არ არის ავტომატურად failure. სწორ ადგილას გაჩერება წარმატებული ქცევაა.

## 8. STOP CARD

ყოველი გაჭედილი ტოტი აბრუნებს:

```text
STOP_ID
WHERE
WANTED
AVAILABLE
MISSING
STOP_CLASS
CAN_ASK_OUTSIDE
QUERY
PROVENANCE
SCOPE
```

პირველი სამუშაო NEED taxonomy:

```text
MISSING_FACT
MISSING_RULE
MISSING_ADDRESS
MISSING_RELATION
MISSING_PATTERN
MISSING_SCOPE
MISSING_PROVENANCE
MISSING_OPERATION
AMBIGUOUS_MATCH
CONFLICT
CLOSURE_UNKNOWN
CREDIT_UNRESOLVED
```

სია დახურული ontology არ არის.

## 9. Run output

ყოველი run-ის მთავარი ხედი უნდა იყოს მხოლოდ სამი:

```text
NETWORK DELTA
STOP MAP
NEED MAP
```

მიზანია ადამიანმა დაინახოს:
- რა შეიცვალა;
- სად გაჩერდა;
- რა აკლდა.

## 10. ზრდის წესი — Occam

STOP-ის შემდეგ სისტემა ავტომატურად არაფერს იმატებს.

ახალი ელემენტი მიიღება მხოლოდ მაშინ, თუ:
- ხსნის განმეორებად structural gap-ს;
- არ არის ერთი სცენის პატჩი;
- არსებული უფრო მარტივი მექანიზმით ვერ გვარდება;
- domain knowledge-ს დემონის ბირთვში არ შეაქვს;
- ზრდის ძალას და თვალსაჩინოებას ერთდროულად.

ცვლილების შემდეგ იგივე სცენა თავიდან გადის.

> **თუ ერთი მცირე დამატება მრავალ STOP-ს ხსნის, სავარაუდოდ კარგი აბსტრაქციაა.
> თუ თითო STOP-ს თავისი პატჩი სჭირდება, ქსელს ვაჯღაპნით.**

## 11. WORKING fundamental meta-relation — REFERS_TO

DCT01 rerun-ის შემდეგ დარჩენილი მთავარი NEED იყო:

> **generic record-to-record structural reference**

ეს NEED ხელმეორედ გამოჩნდა დამოუკიდებელ DCT02 სცენაში, სადაც derived record-ს უნდა
შეენარჩუნებინა ზუსტი provenance — რომელი premise-record-ები და რომელი rule გამოიყენეს.

ამიტომ მიმდინარე WORKING meta-relation არის **REFERS_TO**.

მინიმალური მნიშვნელობა:

> **A-ს აქვს მისამართიანი სტრუქტურული მითითება B-ზე.**

REFERS_TO არ ნიშნავს თავისით part-of, cause, evidence, support, truth, agreement ან
semantic dependency-ს. უფრო კონკრეტული როლები, თუ ოდესმე დასჭირდება სისტემას,
ცალკე უნდა გაჩნდეს საკუთარი NEED-იდან და არა REFERS_TO-ს ჩუმი გადატვირთვით.

ამ დროისთვის:

    CF1 REFERS_TO T1
    CF1 REFERS_TO N1

    T3  REFERS_TO T1
    T3  REFERS_TO T2
    T3  REFERS_TO R1

DCT01 + DCT02 ერთად არის მიზეზი, რის გამოც REFERS_TO აღარ ითვლება conflict-სცენის
ერთჯერად patch-ად და შედის ბირთვში როგორც **WORKING**, არა საბოლოო invariant.


## 12. WORKING relation qualifier — ROLE

DCT03-ში გამოჩნდა ახალი NEED:

> **relation-record needs addressable role/qualification**

მიზეზი იყო ის, რომ `REFERS_TO` ინახავდა ზუსტ მისამართიან reference-ს, მაგრამ ვერ არჩევდა,
რომელი reference იყო premise, context ან applied rule.

DCT04-ში იგივე NEED დამოუკიდებლად განმეორდა knowledge-credit კონტექსტში:
reference-ებს უნდა განესხვავებინათ debt, authorization/provenance და dependent descendant.

ამიტომ მიმდინარე WORKING meta-relation არის:

```text
ROLE
```

მინიმალური მნიშვნელობა:

> **მისამართიან relation-record-ს ამ ადგილობრივ კონსტრუქციაში აქვს კონკრეტული ფუნქციური როლი.**

მაგალითები:

```text
RF1 = (T3, REFERS_TO, T1)
RF1 ROLE PREMISE

RF2 = (KC1, REFERS_TO, MR1)
RF2 ROLE DEBT
```

`ROLE` თავისით არ ნიშნავს truth, causality, support, priority, ownership ან type-ს.

მნიშვნელოვანი დიზაინის შედეგი:

> **სპეციფიკური semantics არ უნდა ჩაიტვირთოს REFERS_TO-ში და არც ახალი fundamental
> predicate უნდა შეიქმნას მხოლოდ სახელის მოსახერხებლობისთვის, თუ addressable edge + ROLE
> უკვე საკმარისია.**

მიმდინარე ჰომოიკონური ძვალი:

```text
addressable triplet
    ↓
REFERS_TO
    ↓
addressable reference-edge
    ↓
ROLE
```

DCT03 + DCT04 არის მიზეზი, რის გამოც `ROLE` შედის ბირთვში როგორც **WORKING**, არა საბოლოო invariant.

## 13. OPEN — downstream consequence of dependency status change

DCT05 და DCT06-ში დამოუკიდებლად განმეორდა ერთი და იგივე ახალი NEED:

> **known dependency + upstream status transition + missing downstream consequence law**

DCT05-ში upstream premise შევიდა CONFLICTED მდგომარეობაში; DCT06-ში იგივე ტიპის premise გახდა HISTORICAL.
ორივე შემთხვევაში dependency path REFERS_TO + ROLE-ით სრულად ჩანს, მაგრამ დემონს არ აქვს უფლება თვითონ განსაზღვროს descendant-ის ახალი სტატუსი.

ამ ეტაპზე უნივერსალური propagation rule არ ემატება.

OPEN კითხვა:

> **აკლია მხოლოდ propagation law, თუ dependency-edge-ს დამატებითი qualification სჭირდება, რათა downstream consequence განისაზღვროს?**

ეს საკითხი უნდა გადაწყდეს შემდეგ probe-ებში და არა წინასწარი ontology design-ით.

## 14. WORKING HYPOTHESIS — dependency policy lives in the network

DCT07-მა აჩვენა, რომ იგივე ROLE=PREMISE და იგივე upstream status transition სხვადასხვა descendant-სთვის სხვადასხვა consequence-ს შეიძლება ითხოვდეს.

ამიტომ მიმდინარე WORKING HYPOTHESIS არის:

> **Status propagation არ არის demon-core primitive. Upstream status transition-ის downstream შედეგი განისაზღვრება ქსელში მისამართიანი dependency-policy rule-ით.**

Dependency-edge თვითონ addressable record-ია და policy rule-ს REFERS_TO + ROLE=POLICY-ით უკავშირდება.

თუ applicable policy rule არ არსებობს:

    STOP_CLASS = NEED
    MISSING = applicable dependency-policy rule

## 15. Rule-level conflict და executor boundary — OPEN

DCT08-ში ერთ dependency-edge-ზე ორი applicable policy ერთმანეთთან შეუთავსებელ შედეგს ითხოვდა.

დემონი არც ერთს არ ირჩევს; policy rules თვითონ addressable records არიან, ამიტომ იქმნება ჩვეულებრივი addressable CONFLICT/OPEN object და downstream transition იბლოკება.

ამ შემთხვევის STOP:

    STOP_CLASS = BLOCK

რადგან პრობლემა დაკარგული სტრუქტურა კი არა, არსებული წესების მიერ unique legal continuation-ის არქონაა.

DCT08-მა ასევე გახსნა უფრო ღრმა საკითხი:

> **რომელი მინიმალური invariants უნდა დარჩეს executor boundary-ში, რათა ჰომოიკონურმა ქსელმა საკუთარი audit machinery ვერ გააუქმოს ან ჩუმად ვერ გადაწეროს?**

მიმდინარე საზღვარი ჯერ OPEN არის:

    NETWORK RULES
    vs
    EXECUTOR INVARIANTS

ეს საკითხი არ უნდა დაიხუროს წინასწარი ფილოსოფიური არჩევანით; საჭიროა adversarial/self-modification probes.

## 16. WORKING executor boundary — transaction membrane

DCT09-მა ორი მინიმალური executor invariant გამოყო:

1. **Every mutation passes PROPOSE → CHECK → COMMIT.**
2. **A delta cannot use rules introduced or changed by itself to authorize that same delta.**

მეორე წესი ნიშნავს, რომ delta N-ის შემოწმებისთვის ეფექტური rule-set მოდის უკვე committed state N-1-იდან.

ეს საზღვარი არ შეიცავს domain knowledge-ს; იგი იცავს მხოლოდ ცვლილების პროცედურულ კარს.

## 17. WORKING executor invariant — TRACE CONTINUITY

DCT10-მა აჩვენა განსხვავება payload forgetting-სა და history erasure-ს შორის.

> **A committed transition may be compacted, archived, superseded or corrected, but may not be made historically unaddressable or provenance-untraceable.**

შეცდომის გასწორება დაშვებულია; committed წარსულის ისე გადაწერა, თითქოს არასოდეს მომხდარა — არა.

## 18. WORKING distinction — historical occurrence vs current validity

DCT11-მა აჩვენა, რომ ძველი commit-ის ისტორიული ფაქტი და მისი დღევანდელი epistemic validity ერთი და იგივე რამ არ არის.

მიმდინარე სამუშაო განსხვავება:

    HISTORY_STATUS
    CURRENT_EPISTEMIC_STATUS

> **past commit fact is preserved; present trust/status is revisable.**

ეს ჯერ არ ითვლება frozen executor invariant-ად. საჭიროა oscillation/recovery probe: VALID → CHALLENGED → REHABILITATED.

## 19. WORKING status separation and non-destructive MARK

DCT12-მა DCT11-ის განსხვავება უფრო მკაფიოდ დაადასტურა:

> **HISTORY_STATUS ≠ EPISTEMIC_STATUS**

historical occurrence რჩება სტაბილური, ხოლო epistemic status შეიძლება იყოს time-, scope- და audit-dependent.

ამასთან, MARK-ის სამუშაო semantics იცვლება destructive overwrite-დან non-destructive status assertion-ზე:

> **MARK ქმნის ახალ addressable status assertion-ს, ხდის მას მიმდინარე შესაბამის scope/time-ში და ინარჩუნებს წინა status assertions-ს ისტორიულ კვალად.**

ამიტომ status transition არ ნიშნავს ძველი status-ის წაშლას.

DCT12 ასევე ტოვებს ორ OPEN-ს:

1. audit history-დან current epistemic status-ის selection policy;
2. scope-resolution policy, როცა rehabilitation მხოლოდ ნაწილობრივ scope-ში მოქმედებს.

შემდეგი probe: შეუძლია თუ არა ერთსა და იმავე record-ს ერთდროულად ჰქონდეს განსხვავებული epistemic status სხვადასხვა scope-ში ისე, რომ სისტემა არ აიძულოს ერთ global status-ად შეკუმშოს.

## 20. მთავარი ფორმულა

> **დემონი მიდის სადამდეც შეუძლია. სადაც ვერ მიდის — ჩერდება. თუ შეუძლია კითხვა —
> კითხულობს. თუ კითხვა ჯერ ვერ ყალიბდება — ამბობს რა აკლია. ჩვენ ვამატებთ არა
> პასუხს, არამედ ყველაზე პატარა განმეორებად სტრუქტურას, რომელიც ამ ტიპის გაჭედვას
> მომავალში ხსნის.**

და:

> **გაჭედვა არ არის სისტემის მარცხი; გაუგებარი გაჭედვაა მარცხი.**
