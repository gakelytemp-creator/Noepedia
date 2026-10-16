# DEMON_DCT15 — generic applicability qualifier

**Status: EXPERIMENTAL RECORD / QUALIFIER-FRAMEWORK PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT14-ის OPEN: SCOPE და TIME შეიძლება თუ არა ერთ generic addressable qualifier framework-ში ცხოვრობდეს ისე, რომ მათი განსხვავებული matching algebra არ დაიკარგოს.

## 1. generic representation

    Q1 TYPE → APPLICABILITY_QUALIFIER
    Q1 VALUE → SCENE_A

    Q2 TYPE → APPLICABILITY_QUALIFIER
    Q2 VALUE → [t1,t10]

    ES1 REFERS_TO Q1 ; ROLE QUALIFIER
    ES1 REFERS_TO Q2 ; ROLE QUALIFIER

## 2. matching law stays local

qualifier representation ერთია, მაგრამ matching policy განსხვავდება:

    Q1 REFERS_TO R_SCOPE_MATCH ; ROLE MATCH_POLICY
    Q2 REFERS_TO R_TIME_MATCH ; ROLE MATCH_POLICY

დემონს არ სჭირდება hard-coded scope/time semantics; იგი პოულობს qualifier-ის matching policy-ს და COMPARE-ს ქსელის rule-ის მიხედვით ატარებს.

## 3. applicability filtering

თუ ყველა required qualifier match-დება query context-ს, assertion APPLICABLE ხდება.

თუ რომელიმე qualifier კანონიერად არ match-დება, assertion არის NOT_APPLICABLE.

> **NOT_APPLICABLE ≠ FALSE ≠ CHALLENGED.**

## 4. missing matching policy

    STOP_21
    WHERE: DCT15 / applicability evaluation
    WANTED: determine whether assertion applies
    AVAILABLE: qualifier attached
    MISSING: matching policy for qualifier
    STOP_CLASS: NEED
    CAN_ASK_OUTSIDE: NO

## 5. შედეგი

> **Applicability qualifiers share a generic addressable representation, not necessarily a generic matching algebra.**

> **Each qualifier may reference its own matching policy.**

> **Conflict/resolution is evaluated only after applicability filtering.**

მოკლე pipeline:

    QUALIFY → MATCH → APPLICABLE → only then COMPARE / CONFLICT
