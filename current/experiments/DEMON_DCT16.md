# DEMON_DCT16 — conflicting match policies on one qualifier

**Status: EXPERIMENTAL RECORD / QUALIFIER-RULE-CONFLICT PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT15-ში qualifier-ს საკუთარი MATCH_POLICY მიება. DCT16 ამოწმებს რა ხდება, როცა ერთ qualifier-ზე ორი applicable matching policy ერთსა და იმავე query context-ზე ურთიერთსაწინააღმდეგო პასუხს იძლევა.

## 1. assertion და qualifier

    ES1 TARGET → T3
    ES1 STATE → SUPPORTED

    Q1 TYPE → APPLICABILITY_QUALIFIER
    Q1 VALUE → SCENE_A
    ES1 REFERS_TO Q1 ; ROLE QUALIFIER

Q1-ზე ორი matching policyა:

    Q1 REFERS_TO R_SUBSCOPE ; ROLE MATCH_POLICY
    Q1 REFERS_TO R_EXACT ; ROLE MATCH_POLICY

მათი წესები:

    R_SUBSCOPE: query scope matches if it is equal to or a subscope of qualifier scope
    R_EXACT: query scope matches only if it is exactly equal to qualifier scope

## 2. query context

გვაქვს:

    SCENE_B is_subscope_of SCENE_A
    SCENE_B ≠ SCENE_A

query:

    STATUS(T3, SCENE_B)

მაშინ:

    R_SUBSCOPE(Q1, SCENE_B) → MATCH
    R_EXACT(Q1, SCENE_B) → NO_MATCH

ორივე policy applicableა, მაგრამ qualifier applicability-ზე საპირისპირო შედეგს იძლევა.

## 3. სწორი ქცევა

დემონი არ ირჩევს არც MATCH-ს და არც NO_MATCH-ს, არ იყენებს newest/strictest/worst-rule heuristic-ს და ES1-ს არც APPLICABLE-ად და არც NOT_APPLICABLE-ად არ აცხადებს.

იქმნება rule-level addressable conflict:

    CF_QPOLICY_1 TYPE → CONFLICT
    CF_QPOLICY_1 STATUS → OPEN
    CF_QPOLICY_1 REFERS_TO R_SUBSCOPE ; ROLE CONFLICT_SIDE
    CF_QPOLICY_1 REFERS_TO R_EXACT ; ROLE CONFLICT_SIDE
    CF_QPOLICY_1 REFERS_TO Q1 ; ROLE CONTEXT

## 4. STOP

    STOP_22
    WHERE: DCT16 / qualifier matching-policy conflict
    WANTED: determine whether ES1 applies to query context
    AVAILABLE: two applicable MATCH_POLICY rules with incompatible results
    MISSING: unique legal qualifier evaluation
    STOP_CLASS: BLOCK
    CAN_ASK_OUTSIDE: NO

ეს BLOCK არის, არა NEED: matching machinery და rules არსებობს; სწორედ მოქმედი rules ვერ იძლევა ერთ კანონიერ continuation-ს.

## 5. downstream containment

ვიდრე qualifier applicability unresolved არის, ES1 არ შედის epistemic-status comparison/conflict set-ში.

> **Applicability conflict must be resolved before semantic/status conflict is evaluated.**

ანუ:

    qualifier-policy conflict
        → BLOCK applicability
        → do not leak ES1 downstream

## 6. DCT08 recurrence

DCT16-ს ახალი conflict mechanism არ დასჭირდა. DCT08-ის იგივე first-class rule-conflict machinery მუშაობს qualifier layer-ზეც.

ეს დამოუკიდებელი recurrence აძლიერებს პრინციპს:

> **Rule conflicts are handled structurally at the layer where they arise; higher layers receive no fabricated result.**

## 7. შედეგი

DCT15-ის generic qualifier framework survives the adversarial test: representation generic რჩება, matching semantics ქსელში ცხოვრობს, ხოლო contradictory matching policies ჩვეულებრივ addressable CONFLICT/BLOCK-ად იქცევა.

ახალი primitive არ დამატებულა.
