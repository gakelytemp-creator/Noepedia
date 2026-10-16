# DEMON_DCT20 — surviving provenance after one convergent path fails

**Status: EXPERIMENTAL RECORD / JUSTIFICATION-REDUNDANCY PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT19-ში ერთი MATCH result-ს ორი განსხვავებული lawful justification path ჰქონდა. DCT20 ამოწმებს რა ხდება, თუ მოგვიანებით ერთ-ერთი path challenged/invalidated ხდება, ხოლო მეორე უცვლელად survives.

## 1. საწყისი result

    JP1 RESULT → MATCH
    JP2 RESULT → MATCH

    EV1 TYPE → EVALUATION_RESULT
    EV1 RESULT → MATCH
    EV1 REFERS_TO JP1 ; ROLE JUSTIFICATION
    EV1 REFERS_TO JP2 ; ROLE JUSTIFICATION

ორივე path საწყის მომენტში lawful და terminating არის.

## 2. one path is challenged

მოგვიანებით R_SUBSCOPE, რომელზეც JP1 დგას, re-audit-ზე FAIL/CHALLENGED ხდება.

ამიტომ:

    JP1 CURRENT_EPISTEMIC_STATE → CHALLENGED
    JP2 CURRENT_EPISTEMIC_STATE → SUPPORTED

EV1-ის ისტორიული MATCH result არ იშლება.

## 3. პირველი ცდუნება — ავტომატური survival

შეიძლება გვინდოდეს ვთქვათ: 'JP2 დარჩა, ამიტომ EV1 კვლავ MATCH'. მაგრამ არსებული representation მხოლოდ იმას ამბობს, რომ JP1 და JP2 EV1-ის JUSTIFICATION-ებია.

იგი ჯერ არ ამბობს, ეს ორი justification:

    ALTERNATIVE / each individually sufficient

თუ:

    JOINT / both required together

ამ განსხვავების გარეშე demon-ს არ აქვს უფლება current result-ის survival გამოიგონოს.

## 4. STOP

    STOP_25
    WHERE: DCT20 / one convergent justification challenged
    WANTED: determine whether EV1 remains currently supported
    AVAILABLE: JP1 challenged; JP2 supported; both recorded as JUSTIFICATION
    MISSING: justification-composition policy
    STOP_CLASS: NEED
    CAN_ASK_OUTSIDE: NO

ეს მნიშვნელოვანი ახალი NEED-ია: provenance multiplicity თავისით redundancy semantics არ არის.

## 5. explicit alternative-support policy

თუ ქსელში წინასწარ გვაქვს addressable policy:

    R_ALT_SUPPORT:
    any one currently supported COMPLETE_JUSTIFICATION is sufficient for EV1

და JP1/JP2 შესაბამის policy-ს ექვემდებარება, rerun იძლევა:

    JP1 challenged
    JP2 supported
    R_ALT_SUPPORT satisfied by JP2
    EV1 current epistemic support → preserved
    GO

JP1-ის ისტორია მაინც რჩება provenance-ში; იგი უბრალოდ აღარ არის current surviving basis.

## 6. joint-support countercase

თუ policy ამბობს:

    R_JOINT_SUPPORT:
    all listed justification components are required

მაშინ JP1-ის challenge EV1-ის current support-საც challenge-ს უკეთებს.

იგივე graph shape-ს სხვადასხვა consequence აქვს composition policy-ის მიხედვით.

## 7. შედეგი

> **Multiple justifications do not automatically mean redundancy. Redundancy exists only when the network states that the justifications are alternative sufficient supports.**

> **A result may remain currently supported after one path fails only if a surviving sufficient justification exists under an explicit composition policy.**

> **Historical provenance is preserved even when a path ceases to be a current basis.**

ახალი primitive არ დამატებულა. ახალი NEED არის justification-composition semantics, რომელიც ქსელში უნდა ცხოვრობდეს და არა demon-core-ში.
