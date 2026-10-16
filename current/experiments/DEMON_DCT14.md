# DEMON_DCT14 — same scope, different time windows

**Status: EXPERIMENTAL RECORD / TEMPORAL APPLICABILITY PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT13-ის scoped status model დროის განზომილებაზე მოწმდება.

## 1. დროითი assertions

    ES1 TARGET → T3
    ES1 STATE → SUPPORTED
    ES1 SCOPE → SCENE_A
    ES1 TIME → [t1,t5]

    ES2 TARGET → T3
    ES2 STATE → CHALLENGED
    ES2 SCOPE → SCENE_A
    ES2 TIME → [t6,t9]

disjoint time windows-ში ორივე კანონიერად თანაარსებობს.

## 2. qualified query

STATUS(T3, SCENE_A, t3) → SUPPORTED → GO.

STATUS(T3, SCENE_A, t8) → CHALLENGED → GO.

## 3. time omitted

ერთ status-ზე შეკუმშვა დაუშვებელია, თუ time qualifier ან temporal aggregation policy არ გვაქვს.

    STOP_19
    WHERE: DCT14 / unqualified temporal status query
    MISSING: time qualifier or temporal aggregation policy
    STOP_CLASS: ASK or NEED

## 4. overlapping windows

თუ ES1=[t1,t7] და ES2=[t5,t9], მაშინ t6-ზე ორივე applicableა. incompatible states ქმნის CONFLICT/OPEN-ს და STOP_CLASS=BLOCK-ს.

## 5. შედეგი

> **Epistemic status assertion is valid only relative to an applicability context.**

ამ ეტაპზე პირველი ორი დადასტურებული applicability dimension არის SCOPE და TIME.

> **Different states in disjoint scopes or disjoint time windows may coexist. Conflict requires simultaneous applicability plus incompatibility.**

OPEN კითხვა: შეიძლება თუ არა SCOPE და TIME ერთ generic qualifier framework-ში აღვწეროთ ისე, რომ მათი განსხვავებული matching laws არ დაიკარგოს?
