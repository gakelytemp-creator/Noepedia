# DEMON_DCT08 — conflicting policies on one dependency edge

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT07-ის შემდეგ dependency consequence ქსელში მცხოვრებ policy rule-ს მიება.

DCT08 ამოწმებს ყველაზე სახიფათო შემთხვევას:

> **რა ხდება, როცა ერთ dependency-edge-ზე ორი applicable policy ერთმანეთთან შეუთავსებელ შედეგს ითხოვს?**

## 1. საწყისი სტრუქტურა

    RA = (A1, REFERS_TO, T1)
    RA ROLE PREMISE

RA-ზე ორი policy rule არის მიბმული:

    RA REFERS_TO R_KEEP ; ROLE POLICY
    RA REFERS_TO R_OPEN ; ROLE POLICY

მათი ეფექტები:

    R_KEEP: upstream CURRENT→HISTORICAL ⇒ descendant keeps validity in historical scope
    R_OPEN: upstream CURRENT→HISTORICAL ⇒ descendant becomes OPEN

ორივე rule კანონიერად არსებობს და ორივე applicableა.

## 2. transition

შემოდის:

    T1: CURRENT → HISTORICAL

დემონი პოულობს RA-ს და ორივე policy-ს.

ორივე ცალ-ცალკე ქმნის კანონიერ candidate action-ს, მაგრამ candidate-ები ერთმანეთს ეწინააღმდეგებიან.

## 3. rule-level conflict

დემონი არც ერთ policy-ს თვითნებურად არ ირჩევს.

იქმნება addressable conflict:

    CF_POLICY_1 TYPE CONFLICT
    CF_POLICY_1 STATUS OPEN
    CF_POLICY_1 REFERS_TO R_KEEP ; ROLE CONFLICT_SIDE
    CF_POLICY_1 REFERS_TO R_OPEN ; ROLE CONFLICT_SIDE
    CF_POLICY_1 REFERS_TO RA ; ROLE CONTEXT

## 4. STOP

    STOP_11
    WHERE: DCT08 / conflicting dependency policies
    WANTED: apply downstream status consequence to A1
    AVAILABLE: RA dependency edge; R_KEEP applicable; R_OPEN applicable; proposed effects conflict
    MISSING: unique legal continuation
    STOP_CLASS: BLOCK
    CAN_ASK_OUTSIDE: NO

აქ BLOCK გამოიყენება იმიტომ, რომ სტრუქტურა არ აკლია; არსებული მოქმედი წესები ერთობლივად ვერ იძლევა ერთ კანონიერ გაგრძელებას.

## 5. NETWORK DELTA

კანონიერი delta მხოლოდ conflict-ის რეგისტრაციაა. A1-ის status transition არ commit-დება.

## 6. ჰომოიკონური შედეგი

Rules თვითონ first-class addressable records არიან, ამიტომ იგივე READ / MATCH / REFERS_TO / ROLE / CONFLICT / OPEN ინფრასტრუქტურა rule-level conflict-საც ხედავს.

ახალი meta-meta demon არ გახდა საჭირო.

## 7. ახალი OPEN საზღვარი

თუ rule-ებიც მთლიანად ქსელშია, შეიძლება თვით audit-preservation rule-საც დაუპირისპირდეს სხვა rule, მაგალითად conflict-ის დამალვის ან newest-rule wins ქცევა.

ამიტომ DCT08 აჩენს ახალ რეალურ OPEN-ს:

> **რომელი მინიმალური invariants უნდა დარჩეს executor boundary-ში, რათა ქსელმა საკუთარი audit machinery ვერ გააუქმოს?**

ეს არის NETWORK-RULES vs EXECUTOR-INVARIANTS საზღვარი.

## 8. სტატუსი

DCT08 ამყარებს rule-level conflict handling-ს, მაგრამ bootstrapping boundary ჯერ OPEN რჩება.
