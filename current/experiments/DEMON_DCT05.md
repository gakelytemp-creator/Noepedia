# DEMON_DCT05 — integrated conflict / provenance / credit stress test

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT01–DCT04-მა ცალ-ცალკე წარმოშვა და გამოსცადა addressable triplet/pattern, REFERS_TO და ROLE.
ამ ტესტში conflict, derivation provenance და knowledge credit პირველად ერთ პატარა ქსელში ერთიანდება.

## 1. საწყისი ქსელი

    T1 = (O1,P1,O2) CURRENT
    T2 = (O2,P2,O3) CURRENT

    R1: T1 + T2 → T3
    T3 = (O1,P3,O3)

    RF1 = (T3, REFERS_TO, T1) ; RF1 ROLE PREMISE
    RF2 = (T3, REFERS_TO, T2) ; RF2 ROLE PREMISE
    RF3 = (T3, REFERS_TO, R1) ; RF3 ROLE RULE_USED

შემდეგ:

    MR1 = (O3,P4,O4)
    KC1 REFERS_TO MR1 ; ROLE = DEBT
    D1 = (O1,P5,O4) ; STATUS = CREDIT_DEPENDENT
    D1 REFERS_TO T3 ; ROLE = PREMISE
    D1 REFERS_TO KC1 ; ROLE = CREDIT_SOURCE

ამ ეტაპამდე GO.

## 2. ახალი conflict

შემოდის N1 = (O1,P1N,O2) და გვაქვს P1 ANTI_OF P1N.

    CF1 REFERS_TO T1
    CF1 REFERS_TO N1
    ROLE = CONFLICT_SIDE
    CF1 STATUS = OPEN

აქაც GO.

## 3. Reverse dependency discovery

    MATCH (? REFERS_TO T1) → T3 depends on T1 as PREMISE
    MATCH (? REFERS_TO T3) → D1 depends on T3 as PREMISE

dependency path ჩანს: T1 → T3 → D1.

## 4. STOP

    STOP_08
    WHERE: DCT05 / downstream effect of conflicted premise
    WANTED: determine status consequences for T3 and D1
    AVAILABLE: conflict at T1; T3→T1 ROLE PREMISE; D1→T3 ROLE PREMISE; D1 CREDIT_DEPENDENT
    MISSING: rule for propagation of premise conflict into descendants
    STOP_CLASS: NEED
    CAN_ASK_OUTSIDE: NO

დემონი არ იგონებს FALSE-ს, არ შლის descendants-ს და არ ტოვებს მათ ჩუმად fully validated მდგომარეობაში.

## 5. მნიშვნელოვანი გამიჯვნა

credit debt ≠ premise conflict.

KC1-ის repayment T1-ის conflict-ს არ ხურავს.

## 6. შედეგი

> **dependency path is known, but downstream consequence of upstream status change is unspecified.**

ეს ჯერ არ ქცეულა ახალ rule-ად; საჭიროა დამოუკიდებელი recurrence.
