# DEMON_DCT21 — composition policy changes over time

**Status: EXPERIMENTAL RECORD / POLICY-TEMPORALITY PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT20-ის შემდეგ მოწმდება რა ხდება, როცა justification-composition policy თვითონ იცვლება დროში.

## 1. საწყისი მდგომარეობა

    JP1 RESULT → MATCH
    JP2 RESULT → MATCH
    EV1 RESULT → MATCH

მოქმედი composition policy:

    CP1 TYPE → JUSTIFICATION_COMPOSITION_POLICY
    CP1 MODE → ALTERNATIVE
    EV1 REFERS_TO CP1 ; ROLE COMPOSITION_POLICY

CP1-ის ქვეშ ერთი complete supported justification საკმარისია.

## 2. ერთი path challenged

    JP1 → CHALLENGED
    JP2 → SUPPORTED

CP1 კვლავ ALTERNATIVE არის, ამიტომ EV1 current support survives.

## 3. policy transition

შემოდის ახალი policy:

    CP2 TYPE → JUSTIFICATION_COMPOSITION_POLICY
    CP2 MODE → JOINT

და:

    CP1 → HISTORICAL
    CP2 → CURRENT

ახლა JP1 CHALLENGED + JP2 SUPPORTED CP2-ის ქვეშ აღარ აკმაყოფილებს joint support-ს, ამიტომ EV1 current epistemic status შეიძლება გახდეს CHALLENGED შესაბამისი policy-ის მიხედვით.

## 4. history is not rewritten

ისტორია რჩება:

    at t1 EV1 supported under CP1
    at t2 EV1 still supported under CP1
    at t3 EV1 challenged under CP2

> **Support validity is policy-relative in time.**

## 5. retroactive re-audit

CP2-ს შეუძლია ძველი EV1-ს re-audit გაუკეთოს, მაგრამ არ შეუძლია თქვას, რომ EV1 არასოდეს ყოფილა supported CP1-ის ქვეშ.

სწორი ფორმა:

    historical: EV1 supported at t2 under CP1
    later re-audit: EV1@t2 would fail under CP2

## 6. missing precedence/applicability

თუ არ ვიცით როდის ხდება CP2 applicable ან როგორ ურთიერთობს CP1-თან:

    STOP_26
    WHERE: DCT21 / composition-policy transition
    WANTED: determine current support of EV1
    AVAILABLE: CP1=ALTERNATIVE; CP2=JOINT; JP1 CHALLENGED; JP2 SUPPORTED
    MISSING: policy applicability / precedence over time
    STOP_CLASS: NEED

## 7. overlapping policy windows

თუ CP1 და CP2 ერთსა და იმავე query context-ში ერთდროულად applicableა და incompatible outcomes-ს იძლევა, იქმნება addressable policy conflict და STOP_CLASS=BLOCK.

## 8. შედეგი

> **Composition semantics itself is time/scope-qualified knowledge.**

> **Changing policy may change current support without rewriting historical support.**

> **Policy applicability and precedence must be explicit; newest-wins is not implicit.**
