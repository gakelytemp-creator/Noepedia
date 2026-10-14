# GLASS_WORLD_LAB — შუშის სამყაროს ლაბორატორია

**Status: CURRENT EXPERIMENTAL DESIGN**  
**Date: 2026-10-15**

## 0. მიზანი

Noepedia-ს ახლა სჭირდება არა კიდევ ერთი ცალკეული წესის ტესტი, არამედ **მინიმალური
მთლიანი სამყარო**, სადაც შეგვიძლია დავინახოთ:

- რას ხედავს სისტემა;
- რას აშენებს;
- სად ჩერდება;
- რას იგონებს;
- რა გამორჩება;
- როდის ქმნის ACO-ს;
- რა კითხვას აგზავნის გარეთ;
- როგორ მუშაობს trap / Kairos;
- და საბოლოოდ როგორ განსხვავდება მისი შიდა სამყარო სინამდვილეში შექმნილი სამყაროსგან.

ამიტომ ვქმნით **შუშის სამყაროს**.

სისტემისთვის იგი ნაწილობრივ დაფარულია.

ჩვენთვის — სრულად გამჭვირვალე.

---

## 1. სამი დამოუკიდებელი როლი

ლაბორატორიაში ერთმანეთისგან მკაცრად იყოფა სამი როლი:

~~~text
WORLD GENERATOR
      │
      │ creates full hidden truth
      ▼
PARTIAL PROJECTIONS
      │
      ▼
NOEPEDIA
      │
      │ builds / asks / stops / searches
      ▼
CONSTRUCTION TRACE
      │
      ▼
AUDITOR
      │
      └─ compares with answer book
~~~

### WORLD GENERATOR

ქმნის სამყაროს სრულ სტრუქტურას.

მან იცის:
- ყველა ობიექტი;
- ყველა hierarchy;
- ყველა relation;
- ყველა hidden state;
- ყველა კანონი;
- ყველა შესაძლო/აკრძალული გადასვლა;
- რომელი identity სწორია;
- რა შეიძლება დაინახოს თითო ცენტრმა;
- რა არის ჯერ დაფარული.

### NOEPEDIA

იღებს მხოლოდ იმ პროექციებს, რასაც ექსპერიმენტი აძლევს.

მას **არ აქვს წვდომა პასუხების წიგნზე**.

### AUDITOR

არ ეხმარება Noepedia-ს ამოცანის გადაწყვეტაში.

იგი მხოლოდ ბოლოს ან გზაში ადარებს:
- hidden truth-ს;
- Noepedia-ს field-ს;
- construction trace-ს;
- OPEN/BLOCKED/ACO გადაწყვეტილებებს.

> **გენერატორი ქმნის სიმართლეს; Noepedia ცდილობს მის რეკონსტრუქციას და გაფართოებას;
> აუდიტორი ზომავს დიფერენტს.**

---

## 2. რატომ არ გვყოფნის ჩვეულებრივი benchmark

ჩვეულებრივ ტესტში ხშირად ვიცით მხოლოდ საბოლოო პასუხი:

~~~text
QUESTION → ANSWER
~~~

მაგრამ Noepedia-სთვის ეს არასაკმარისია.

სწორი პასუხი შეიძლება მიიღოს:
- სწორი აგებით;
- შემთხვევითი დამთხვევით;
- არასწორი identity merge-ით;
- დაუმსახურებელი inference-ით;
- hidden truth-ის გაჟონვით;
- false settled-ით.

ამიტომ პასუხების წიგნში უნდა იყოს არა მარტო **რა არის სწორი**, არამედ **რატომ არის
სწორი და რა არ უნდა სცოდნოდა სისტემას მოცემულ მომენტში**.

---

## 3. ANSWER BOOK — სამყაროს სრული წიგნი

გენერატორი სამყაროს შექმნისას ინახავს სრულ answer book-ს.

მინიმუმ:

~~~text
OBJECTS
IDENTITIES
HIERARCHIES
RELATIONS
RULES
STATES
EVENTS
PROVENANCE
VISIBLE PROJECTIONS
HIDDEN FACTS
ALLOWED TRANSITIONS
FORBIDDEN TRANSITIONS
EXPECTED OPEN
VALID ACO TARGETS
VALID BINDINGS
TRAP CONDITIONS
KAIROS EVENTS
BRIDGE SCOPE
~~~

ეს გვაძლევს საშუალებას შევამოწმოთ არა მხოლოდ შედეგი, არამედ თითოეული შუალედური
სტრუქტურა.

---

## 4. პირველი ხელოვნური გარემო

პირველი სამყარო განზრახ პატარა უნდა იყოს.

მაგალითად:

~~~text
WORLD
├─ ROOM_A
│  ├─ TABLE
│  │  ├─ BOX_1
│  │  │  ├─ KEY
│  │  │  └─ BALL
│  │  └─ CUP
│  └─ DOOR
└─ ROOM_B
   ├─ CABINET
   └─ LAMP
~~~

ობიექტების რაოდენობა: დაახლოებით **10–15**.

ეს საკმარისია, რომ გვქონდეს:
- identity;
- part / whole;
- containment;
- location;
- state;
- event;
- temporal order;
- requirement;
- hidden object;
- search;
- trap;
- simple ACO.

---

## 5. სამყაროს კანონები

პირველ ვერსიაში კანონებიც ცოტაა და თვალსაჩინო.

მაგალითად:

~~~text
R1. object cannot be in ROOM_A and ROOM_B at the same time
R2. if X is inside Y and Y moves, X moves with Y
R3. closed BOX hides its contents from vision
R4. opening BOX exposes its contents
R5. LOCKED DOOR requires a matching KEY to open
R6. an object inside BOX_1 is also in the room containing BOX_1
R7. event order is preserved
~~~

კანონები წინასწარაა ცნობილი answer book-ში.

Noepedia-სთვის ექსპერიმენტის მიხედვით ზოგი შეიძლება ცნობილი იყოს, ზოგი — არა.

ეს განსხვავებაც უნდა იყოს explicit.

---

## 6. პროექციები — რას ხედავს Noepedia

Noepedia არ იღებს სრულ graph dump-ს.

იგი იღებს ცენტრების მიერ წარმოებულ პროექციებს.

მაგალითად:

### VISION

~~~text
ROOM_A-ში ჩანს TABLE.
TABLE-ზე ჩანს BOX_1.
BOX_1 დახურულია.
~~~

### TEXT

~~~text
„გასაღები ოთახშია.“
~~~

### STATE SENSOR

~~~text
DOOR = LOCKED
~~~

### EVENT STREAM

~~~text
BOX_1 moved ROOM_B → ROOM_A
~~~

ამ პროექციებში ზოგი რამ:
- პირდაპირია;
- ზოგი ორაზროვანი;
- ზოგი არასრული;
- ზოგი ერთმანეთს ავსებს.

სწორედ აქ უნდა გამოჩნდეს ცნების შეკვრა.

---

## 7. პირველი ექვსი სცენარი

### TEST 1 — identity across projections

ერთი და იგივე ობიექტი გამოჩნდეს ორ ან სამ ცენტრში.

ვამოწმებთ:
- სწორად ერთ ცნებაზე იკვრება?
- ორი მსგავსი ობიექტი ხომ არ ერწყმის?
- ambiguity OPEN-ად რჩება?

### TEST 2 — hierarchy reconstruction

Noepedia-მ უნდა აღადგინოს:

~~~text
KEY inside BOX_1
BOX_1 on TABLE
TABLE in ROOM_A
~~~

და answer book-ს შევადაროთ არა მხოლოდ საბოლოო relation, არამედ hierarchy-ის სრული
ფორმა.

### TEST 3 — constructive inference

თუ ცნობილია:

~~~text
KEY inside BOX_1
BOX_1 in ROOM_A
R6
~~~

შიდა სამყარომ უნდა ააგოს:

~~~text
KEY in ROOM_A
~~~

ახალი გარე დაკვირვების გარეშე.

ეს არის სუფთა CONSTRUCTIVE რეჟიმი.

### TEST 4 — „ვერ ავაგე“

მივცეთ მოთხოვნა, რომელიც მოქმედ კანონებთან ვერ იკვრება.

მაგალითად:

~~~text
VANO starts in ROOM_A
VANO must remain in ROOM_A
goal: VANO is in ROOM_B
~~~

საინტერესოა არა მხოლოდ FAIL.

უნდა ვიცოდეთ:
- სად გაჩერდა;
- რომელი constraint დაირღვა;
- RULE_BLOCKED იყო თუ SEARCH_OPEN;
- ხომ არ მოიგონა აკრძალული გზა.

### TEST 5 — trap / Kairos

შიდა სისტემამ შექმნას:

~~~text
WHEN KEY becomes visible in ROOM_A
→ wake THREAD_T
~~~

გარემო რამდენიმე სხვა მოვლენას გადის.

შემდეგ BOX_1 იხსნება.

მოსალოდნელი:

~~~text
condition false
condition false
...
condition true
→ KAIROS
→ INTERRUPT
→ resume THREAD_T
~~~

### TEST 6 — ACO / IDEAL_TO_REAL

ამოცანა მოითხოვს რაღაც უცნობს:

~~~text
need X such that:
X opens DOOR
X must be in ROOM_A
X must be portable
~~~

Noepedia-მ უნდა შექმნას:

~~~text
ACO_X
~~~

შემდეგ გარეთ მოძებნოს შესაძლო შესაბამისები.

თუ KEY ემთხვევა ყველა მოთხოვნას:

~~~text
ACO_X ──bound_to──> KEY
~~~

თუ არცერთი არსებული ობიექტი არ ერგება, ACO უნდა დარჩეს OPEN ან გადავიდეს
DESIGN_TARGET-ზე — მაგრამ არ უნდა გაქრეს.

---

## 8. პასუხის სისწორე არ კმარა

თითო სცენარზე აუდიტორი ქმნის **დიფერენტს**.

მაგალითად:

~~~text
FINAL ANSWER: MATCH

but:

identity merge:        WRONG
provenance:            MISSING
unsupported inference: 2
false settled:         1
correct OPEN:          3
missed OPEN:           1
wrong BLOCKED class:   0
ACO binding:           CORRECT
Kairos detection:      CORRECT
~~~

ეს უფრო მნიშვნელოვანია, ვიდრე ერთი საერთო ქულა.

---

## 9. ძირითადი შეცდომების კლასები

პირველ ვერსიაში მაინც უნდა ვხედავდეთ:

- **FALSE_IDENTITY_MERGE**
- **MISSED_IDENTITY**
- **FALSE_RELATION**
- **MISSED_RELATION**
- **UNSUPPORTED_INFERENCE**
- **FALSE_SETTLED**
- **MISSED_OPEN**
- **WRONG_BLOCKED_CLASS**
- **SEARCH_AS_NONEXISTENCE**
- **WRONG_ACO_CONSTRAINT**
- **WRONG_BINDING**
- **MISSED_KAIROS**
- **FALSE_KAIROS**
- **PROVENANCE_LOSS**
- **BRIDGE_SCOPE_OVERREACH**

ეს სია შეიძლება შეიცვალოს რეალური გაშვებების მიხედვით.

---

## 10. trace — სისტემა რას აკეთებდა

Noepedia-ს თითო მნიშვნელოვან ნაბიჯზე უნდა დარჩეს trace.

მაგალითად:

~~~text
T01 receive VISION sample
T02 propose OBJECT_BOX
T03 bind sample → OBJECT_BOX
T04 receive TEXT "key is in room"
T05 create ambiguity: which room?
T06 propagate containment
T07 create ACO_X for door opener
T08 request distinguishing observation
T09 install trap for BOX open
T10 Kairos fired
T11 observe KEY
T12 candidate set shrinks to {KEY}
T13 bind ACO_X → KEY
~~~

ამ trace-ის გარეშე ვერ ვისწავლით, **როგორ** მივიდა სისტემა შედეგამდე.

---

## 11. ორი დამოუკიდებელი შედარება

ლაბორატორიაში ორი განსხვავებული დიფერენტი გვჭირდება.

### WORLD DIFFERENT

~~~text
hidden world
vs
Noepedia reconstructed field
~~~

ამოწმებს:
- რა სწორად დაინახა;
- რა გამორჩა;
- რა დაამატა ზედმეტად.

### REASONING DIFFERENT

~~~text
valid construction paths / constraints
vs
Noepedia construction trace
~~~

ამოწმებს:
- სწორი ნაბიჯი აირჩია?
- OPEN სწორად შეინარჩუნა?
- აკრძალული დასკვნა ხომ არ გააკეთა?
- სწორი ACO ხომ არ შექმნა?
- სწორი გარე კითხვა ხომ არ დასვა?

---

## 12. generator leakage-ის აკრძალვა

WORLD GENERATOR-ის ცოდნა Noepedia-ში არ უნდა გაჟონოს.

Noepedia იღებს მხოლოდ ოფიციალურ პროექციებს.

აკრძალულია:
- hidden object ID-ის მიწოდება;
- answer book-ის relation-ის შემთხვევითი ექსპორტი;
- generator-ის internal state-ის გამოყენება reasoning-ში;
- audit result-ის უკან მიწოდება მიმდინარე trial-ის დროს.

წინააღმდეგ შემთხვევაში ლაბორატორია პასუხების წიგნით გამოცდას გადაიქცევა.

---

## 13. გენერატორი და Noepedia არ უნდა იზიარებდნენ reasoning-ს

ძალიან მნიშვნელოვანი წესი:

> **WORLD GENERATOR არ უნდა ხსნიდეს ამოცანას იმავე ალგორითმით, რომლითაც Noepedia.**

გენერატორის საქმეა სამყაროს **შექმნა და სრული truth-ის შენახვა**.

Noepedia-ს საქმეა ნაწილობრივი ხედებიდან **რეკონსტრუქცია და კონსტრუქცია**.

თუ ორივე ერთსა და იმავე reasoning code-ს იზიარებს, ერთი და იგივე ბაგი შეიძლება
ორივეში განმეორდეს და აუდიტორმა ცრუ PASS მიიღოს.

---

## 14. difficulty ladder

სირთულე ნელა იზრდება.

### LEVEL 0

~~~text
5–8 objects
1 room
direct observations
no ambiguity
~~~

### LEVEL 1

~~~text
10–15 objects
2 rooms
containment
hidden object
simple hierarchy
~~~

### LEVEL 2

~~~text
multiple projections
identity ambiguity
events
constructive inference
BLOCKED
~~~

### LEVEL 3

~~~text
ACO
outward query
trap / Kairos
candidate binding
~~~

### LEVEL 4

~~~text
multiple plast layers
cross-layer roar
partial bridge certificates
design target
~~~

ყოველ დონეზე answer book სრულად რჩება.

---

## 15. რატომ არის ეს სასწავლო მანქანა

ლაბორატორიის მიზანი მხოლოდ „იმუშავა / არ იმუშავა“ არაა.

რამდენიმე გაშვების შემდეგ შეიძლება გამოჩნდეს სტაბილური ნიმუში:

~~~text
hierarchy reconstruction: good
identity: premature closure
ACO creation: good
outward query: weak
BLOCKED classification: unstable
Kairos: reliable
~~~

ეს უკვე გვაჩვენებს, **რომელი არქიტექტურული ორგანოა სუსტი**.

ამიტომ failure არის სასწავლო მასალა.

---

## 16. პირველი ხელით გასავლელი ვერსია

კოდის დაწერამდე სასარგებლოა ერთი სრული სამყარო ხელით ავაწყოთ.

მინიმალური პაკეტი:

~~~text
12 objects
2 rooms
7 laws
3 modalities
1 hidden object
1 ambiguity
1 impossible goal
1 ACO
1 trap
1 Kairos event
~~~

და შემდეგ ხელით გავატაროთ:

~~~text
PROJECTION
→ CONCEPTS
→ FIELD
→ SCENE
→ CONSTRUCT
→ OPEN / BLOCKED
→ ACO
→ OUTWARD QUERY
→ TRAP if needed
→ KAIROS
→ NEW CONTACT
→ BIND / REOPEN
~~~

თუ ეს გზა ხელით ნათლად და წინააღმდეგობის გარეშე გაივლის, უკვე გვეცოდინება
პირველი პროგრამული ვერსიის ზუსტი კონტრაქტი.

---

## 17. პირველი წარმატების კრიტერიუმი

პირველი წარმატება არ არის „ყველა პასუხი სწორია“.

პირველი წარმატებაა, თუ ერთი პატარა სამყარო ბოლომდე გადის ისე, რომ შეგვიძლია
თითოეულ ნაბიჯზე ვუპასუხოთ:

- რა იცოდა სისტემამ?
- საიდან იცოდა?
- რა ააგო?
- რა იყო OPEN?
- სად გაჩერდა?
- რა ACO შექმნა?
- რას ჰკითხა გარეთ?
- რატომ გაიღვიძა?
- რატომ მიაბა კონკრეტულ ობიექტს?
- სად შეცდა?

> **თუ ამ კითხვებზე პასუხს ვხედავთ, ლაბორატორია მუშაობს — მაშინაც კი, თუ Noepedia ჯერ ხშირად ცდება.**

---

## 18. კავშირი IDEAL_TO_REAL-თან

[IDEAL_TO_REAL.md](IDEAL_TO_REAL.md) აღწერს არქიტექტურულ მოძრაობას, სადაც მოთხოვნა
იდეალურ სამყაროში იბადება და გარეთ მიდის.

GLASS_WORLD_LAB არის ადგილი, სადაც ეს მოძრაობა პირველად შეიძლება დავაკვირდეთ
სრული answer book-ის ფონზე.

ერთში წერია **რა მექანიზმი გვინდა**.

მეორეში — **როგორ დავინახავთ, რას აკეთებს სინამდვილეში**.

