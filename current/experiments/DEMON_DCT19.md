# DEMON_DCT19 — convergent paths with distinct provenance

**Status: EXPERIMENTAL RECORD / CONVERGENCE-PROVENANCE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT18-ის საპირისპირო შემთხვევა: ორი განსხვავებული lawful path ერთსა და იმავე terminal outcome-მდე მიდის.

## 1. paths

    PATH_1: Q1 → R_SUBSCOPE → MATCH

    PATH_2: Q1 → R_HIERARCHY → R_CONTAINS → MATCH

ორივე finite, cycle-free და lawful არის.

    JP1 RESULT → MATCH
    JP2 RESULT → MATCH

## 2. one outcome, multiple justifications

Conflict არ არსებობს. იქმნება ერთი evaluation result:

    EV1 TYPE → EVALUATION_RESULT
    EV1 RESULT → MATCH
    EV1 REFERS_TO JP1 ; ROLE JUSTIFICATION
    EV1 REFERS_TO JP2 ; ROLE JUSTIFICATION

RESULT = GO.

## 3. provenance rule

> **same result ≠ same provenance**

Convergent paths არ უნდა შეიკუმშოს ერთ provenance chain-ად.

> **Convergent justifications accumulate provenance, not truth-value.**

ორი path თავისით არ ნიშნავს 'ორჯერ უფრო ჭეშმარიტს'.

## 4. OPEN

Path count თავისით support diversity-საც არ უდრის, რადგან paths შეიძლება ერთმანეთზე იყვნენ დამოკიდებული ან დიდად overlapდებოდნენ.

შემდეგი probe ამოწმებს რა ხდება, თუ convergent paths-იდან ერთი მოგვიანებით invalidated/challenged ხდება.
