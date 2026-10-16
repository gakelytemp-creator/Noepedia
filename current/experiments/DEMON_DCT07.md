# DEMON_DCT07 — dependency policy lives in the network

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT05–DCT06-ის შემდეგ კითხვა იყო: downstream consequence-ს მხოლოდ უნივერსალური propagation law აკლია, თუ dependency-edge-ის შესახებ ინფორმაციაა არასაკმარისი?

## 1. ერთი premise, ორი განსხვავებული სიცოცხლე

გვაქვს ერთი upstream record:

    T1 = (O1,P1,O2) CURRENT

და ორი descendant:

    RA = (A1, REFERS_TO, T1) ; RA ROLE PREMISE
    RB = (B1, REFERS_TO, T1) ; RB ROLE PREMISE

ორივე provenance-ის დონეზე ერთნაირად უკავშირდება T1-ს.

მაგრამ ორი construction rule განსხვავებულ semantics-ს ითხოვს:

    R_A: A1 არის snapshot derivation; T1-ის HISTORICAL გახდომა A1-ს არ აუქმებს თავის ისტორიულ scope-ში.
    R_B: B1 არის live construction; მისი გამოყენება დაშვებულია მხოლოდ მანამ, სანამ T1 CURRENT რჩება.

## 2. upstream transition

შემოდის:

    N1 = (O1,P1,O4) @ t2
    T1 → HISTORICAL
    N1 → CURRENT

იგივე transition და იგივე ROLE=PREMISE ორ სხვადასხვა downstream consequence-ს იძლევა.

აქედან:

> **ROLE = PREMISE არასაკმარისია propagation-ის განსასაზღვრად.**

## 3. policy როგორც ქსელის record

რადგან RA და RB თვითონ addressable relation-record-ებია, მათზე შეიძლება policy rule-ის მითითება:

    RA REFERS_TO R_A ; ROLE POLICY
    RB REFERS_TO R_B ; ROLE POLICY

დემონს აღარ სჭირდება hard-coded უნივერსალური propagation algorithm. იგი პოულობს შესაბამის dependency-edge-ს, მის policy rule-ს და ატარებს მას.

## 4. STOP როცა policy არ არის

თუ dependency-edge-ს policy არ ახლავს:

    STOP_10
    WHERE: DCT07 / premise status transition
    WANTED: determine downstream consequence
    AVAILABLE: dependency path, ROLE=PREMISE, upstream status transition
    MISSING: applicable dependency-policy rule
    STOP_CLASS: NEED
    CAN_ASK_OUTSIDE: NO

## 5. სამუშაო ჰიპოთეზა

> **Status propagation არ არის demon-core primitive. Upstream status transition-ის downstream შედეგი განისაზღვრება ქსელში მისამართიანი dependency-policy rule-ით. თუ policy rule არ არის — NEED.**

ეს რჩება WORKING HYPOTHESIS-ად და საჭიროებს rule-level conflict test-ს.
