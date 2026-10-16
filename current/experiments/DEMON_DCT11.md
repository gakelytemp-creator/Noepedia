# DEMON_DCT11 — retroactive invalidity without history erasure

**Status: EXPERIMENTAL RECORD / STATUS-SEPARATION PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT10-ის შემდეგ კითხვა იყო: თუ ძველი CHECK მოგვიანებით შეცდომიანი აღმოჩნდა, შეიძლება ძველი commit-ის დღევანდელი ვალიდურობა შეიცვალოს ისე, რომ committed history არ გადაიწეროს?

## 1. საწყისი commit

    T1 CURRENT
    T2 CURRENT
    R_CHECK_V1 active

    PROPOSE T3
    CHECK under R_CHECK_V1 → PASS
    COMMIT C1

C1 historically happened and T3 became current under the then-active rules.

## 2. later bug discovery

შემოდის BUG1: R_CHECK_V1 missed condition X. იქმნება R_CHECK_V2.

    RECHECK(C1, R_CHECK_V2) → FAIL

არ შეიძლება არც C1-ის წაშლა/გადაწერა და არც 'once PASS = forever valid'.

## 3. re-audit record

იქმნება ახალი A1 TYPE REAUDIT, რომელიც მიუთითებს C1-სა და R_CHECK_V2-ზე და ინახავს FAIL შედეგს.

ძველი commit რჩება ისტორიულ ფაქტად; მიმდინარე trust/status შეიძლება შეიცვალოს.

## 4. STOP

თუ descendant consequence policy არ არსებობს:

    STOP_14
    WHERE: DCT11 / retroactive re-audit
    WANTED: determine current status/use of T3
    AVAILABLE: C1 historically committed under V1; re-audit under V2 = FAIL
    MISSING: policy for consequence of retroactive audit failure
    STOP_CLASS: NEED

## 5. მთავარი განსხვავება

> **historical legality-at-time ≠ current validity-under-current-rules**

ანუ:

    past commit fact is preserved
    present epistemic trust/status is revisable

## 6. Emerging E4

ძლიერი NEED ჩანს ორი დამოუკიდებელი ღერძის გამოსაყოფად:

    HISTORY_STATUS
    CURRENT_EPISTEMIC_STATUS

ეს ჯერ WORKING distinction-ია და არა frozen executor invariant.
