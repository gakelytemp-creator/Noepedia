# DEMON_DCT13 — simultaneous scoped epistemic states

**Status: EXPERIMENTAL RECORD / APPLICABILITY PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT12-ის შემდეგ მოწმდება შეუძლია თუ არა ერთსა და იმავე record-ს ერთდროულად ჰქონდეს განსხვავებული epistemic states სხვადასხვა scope-ში ისე, რომ ისინი ერთ global scalar status-ად არ შეიკუმშოს.

## 1. ორი scoped assertion

    ES1 TARGET → T3
    ES1 STATE → SUPPORTED
    ES1 SCOPE → SCENE_A
    ES1 REFERS_TO → A1 ; ROLE BASIS

    ES2 TARGET → T3
    ES2 STATE → CHALLENGED
    ES2 SCOPE → SCENE_B
    ES2 REFERS_TO → A2 ; ROLE BASIS

თუ SCENE_A და SCENE_B disjoint არის, ორივე assertion კანონიერად თანაარსებობს.

## 2. scoped query

STATUS(T3, SCENE_A) → ES1 → SUPPORTED → GO.

STATUS(T3, SCENE_B) → ES2 → CHALLENGED → GO.

## 3. unscoped query

თუ query scope არ არის მოცემული, ერთი scalar პასუხის არჩევა დაუშვებელია.

გარე query-ს შემთხვევაში დემონი შეიძლება გადავიდეს ASK-ზე; შიდა პროცესში, რომელსაც ერთი სტატუსი სჭირდება და aggregation policy არ აქვს — NEED.

## 4. overlapping scopes

თუ query-context-ში ES1 და ES2 ორივე applicable არის და states incompatibleა, იქმნება addressable conflict:

    CF_STATUS_1 TYPE → CONFLICT
    CF_STATUS_1 STATUS → OPEN
    CF_STATUS_1 REFERS_TO ES1 ; ROLE CONFLICT_SIDE
    CF_STATUS_1 REFERS_TO ES2 ; ROLE CONFLICT_SIDE

    STOP_18
    WHERE: DCT13 / overlapping epistemic assertions
    WANTED: determine epistemic state in one shared scope
    AVAILABLE: two applicable incompatible assertions
    MISSING: unique legal resolution
    STOP_CLASS: BLOCK

## 5. შედეგი

> **Epistemic status is not a scalar property of a record; it is an addressable, scoped, provenance-bearing assertion.**

> **Different scopes may carry different epistemic states without conflict. Conflict appears only when incompatible assertions are simultaneously applicable to the same query context.**
