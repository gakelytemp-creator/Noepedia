# DEMON_DCT12 — challenged then rehabilitated without history loss

**Status: EXPERIMENTAL RECORD / STATUS-SEPARATION PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT11-ის შემდეგ კითხვა იყო: შეუძლია თუ არა ერთსა და იმავე commit-ს დროთა განმავლობაში ნდობის სტატუსი რამდენჯერმე შეეცვალოს ისე, რომ არც committed history გადაიწეროს და არც ძველი audit-ები დაიკარგოს?

## 1. საწყისი ისტორია

    C1 HISTORY_STATUS = COMMITTED
    T3 derived from C1

პირველი audit:

    A1 TARGET → C1
    A1 CHECK_POLICY → R_CHECK_V1
    A1 RESULT → PASS

ამ მომენტში T3 epistemically supported/valid არის მოქმედი წესებით.

## 2. challenge

შემოდის R_CHECK_V2 და re-audit:

    A2 TARGET → C1
    A2 CHECK_POLICY → R_CHECK_V2
    A2 RESULT → FAIL

T3 current epistemic state ხდება CHALLENGED, მაგრამ C1 HISTORY_STATUS = COMMITTED უცვლელია.

## 3. rehabilitation

მოგვიანებით მოდის ახალი evidence E_NEW, რომელიც ავსებს იმ condition X-ს, რის გამოც A2 FAIL იყო.

    A3 TARGET → C1
    A3 CHECK_POLICY → R_CHECK_V2
    A3 REFERS_TO → E_NEW ; ROLE NEW_EVIDENCE
    A3 RESULT → PASS

თუ შესაბამისი network policy არსებობს, მიმდინარე epistemic state შეიძლება გადავიდეს:

    SUPPORTED → CHALLENGED → SUPPORTED_AGAIN

ყველა audit record რჩება addressable.

## 4. STOP როცა selection policy აკლია

    STOP_15
    WHERE: DCT12 / post-challenge re-audit PASS
    WANTED: update current epistemic status of T3
    AVAILABLE: C1 committed; A1 PASS; A2 FAIL; A3 PASS
    MISSING: policy for selecting current epistemic status from audit history
    STOP_CLASS: NEED

დემონი არ იგონებს წესს „უახლესი ყოველთვის იგებს“.

## 5. scope-dependent rehabilitation

თუ E_NEW და A3 მხოლოდ SCENE_2 scope-ში მოქმედებს, სრული global rehabilitation დაუშვებელია ავტომატურად.

    STOP_16
    WHERE: DCT12 / scope-dependent rehabilitation
    WANTED: determine whether T3 is globally rehabilitated
    AVAILABLE: A2 FAIL scope; A3 PASS scope; T3 use scope
    MISSING: scope-resolution policy
    STOP_CLASS: NEED

## 6. მთავარი შედეგი

> **HISTORY_STATUS ≠ EPISTEMIC_STATUS**

historical occurrence რჩება სტაბილური, ხოლო epistemic status შეიძლება time/scope/audit-dependent იყოს.

## 7. MARK semantics — WORKING

DCT12 აჩვენებს, რომ MARK destructive overwrite არ უნდა იყოს.

> **MARK ქმნის ახალ addressable status assertion-ს, ხდის მას მიმდინარე შესაბამის scope/time-ში და ინარჩუნებს წინა status assertions-ს ისტორიულ კვალად.**

ეს არის WORKING semantics და საჭიროებს multi-scope coexistence probe-ს — DCT13.
