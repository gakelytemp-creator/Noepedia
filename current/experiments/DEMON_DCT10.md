# DEMON_DCT10 — history erasure vs trace continuity

**Status: EXPERIMENTAL RECORD / EXECUTOR-BOUNDARY PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT09-ის transaction membrane-ის შემდეგ DCT10 ამოწმებს შეუძლია თუ არა ქსელს კანონიერად committed წარსულის სრულად წაშლა.

## 1. საწყისი ისტორია

    STATE_0: T1 CURRENT
    DELTA_1: T1 → HISTORICAL ; N1 → CURRENT
    CHECK → PASS
    COMMIT → C1
    STATE_1

C1 ინახავს T1/N1/DELTA_1-ზე მისამართიან კვალს.

## 2. სრული purge

ქსელში ჩნდება housekeeping rule R_PURGE და DELTA_2 ითხოვს:

    DELETE T1
    DELETE provenance(T1)
    DELETE C1 references to T1

ამის შემდეგ committed transition გაუკვალავი ხდება და შესაძლოა descendants dangling reference-ებით დარჩეს.

    STOP_13
    WHERE: DCT10 / historical purge
    WANTED: erase committed history
    MISSING: none
    STOP_CLASS: BLOCK
    REASON: committed transition would become untraceable

## 3. compacting is different

დაშვებულია payload-ის შეკუმშვა/არქივირება, თუ identity და provenance trace რჩება მისამართიანი:

    T1 STATUS → HISTORICAL_ARCHIVED
    identity preserved
    provenance/reference preserved
    payload compacted or unavailable

ამიტომ:

> **forget payload ≠ erase history**

## 4. E3 — TRACE CONTINUITY

> **A committed transition may be compacted, archived, superseded or corrected, but may not be made historically unaddressable or provenance-untraceable.**

## 5. correction without rewriting

თუ ძველი provenance SRC_A მოგვიანებით SRC_B-ით სწორდება, SRC_A-ის კვალი არ იშლება; იქმნება ახალი correction/supersession record.

> **შეცდომის გასწორება დაშვებულია; წარსულის გადაწერა — არა.**
