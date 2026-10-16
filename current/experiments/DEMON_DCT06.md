# DEMON_DCT06 — historical premise propagation recurrence

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT05-ის NEED დამოუკიდებლად მოწმდება გარემოში, სადაც არც knowledge credit არის და არც conflict.

## 1. საწყისი ქსელი

    T1 = (O1,P1,O2) @ t1 CURRENT
    T2 = (O2,P2,O3) @ t1 CURRENT
    R1: (T1 + T2) → T3
    T3 = (O1,P3,O3) CURRENT

    RF1 = (T3, REFERS_TO, T1) ; RF1 ROLE PREMISE
    RF2 = (T3, REFERS_TO, T2) ; RF2 ROLE PREMISE
    RF3 = (T3, REFERS_TO, R1) ; RF3 ROLE RULE_USED

აქ GO.

## 2. upstream state transition

შემოდის N1 = (O1,P1,O4) @ t2. გვაქვს P1 SINGLE_CURRENT_TARGET და t2 > t1.

    T1 → HISTORICAL
    N1 → CURRENT

ესეც GO.

## 3. dependency discovery

    MATCH (? REFERS_TO T1) → RF1
    RF1 ROLE PREMISE → T3 depends on T1 as premise

## 4. STOP

ქსელი არ ამბობს, რა მოუვიდეს T3-ს. დემონს არ აქვს უფლება თვითონ აირჩიოს HISTORICAL, OPEN, CURRENT ან recompute.

    STOP_09
    WHERE: DCT06 / upstream state changed after derivation
    WANTED: determine consequence for descendant T3
    AVAILABLE: T1 HISTORICAL; T3→T1 ROLE PREMISE; T2 CURRENT; R1 known
    MISSING: rule governing downstream consequence of premise status change
    STOP_CLASS: NEED
    CAN_ASK_OUTSIDE: NO

## 5. დამოუკიდებელი recurrence

    DCT05: upstream premise → CONFLICTED ; downstream consequence unknown
    DCT06: upstream premise → HISTORICAL ; downstream consequence unknown

სტატუსები განსხვავებულია, მაგრამ ხვრელი ერთია:

> **known dependency + upstream status transition + missing downstream consequence law**

## 6. მეთოდოლოგიური გადაწყვეტილება

ჯერ არ ემატება უნივერსალური propagation rule, რადგან CONFLICTED ≠ HISTORICAL და შეიძლება მათი downstream semantics განსხვავდებოდეს.

შემდეგი კითხვა:

> **აკლია უბრალოდ propagation rule, თუ თვით dependency-edge-ზე არ არის საკმარისი ინფორმაცია, რომ consequence განისაზღვროს?**
