# DEMON_DCT17 — recursive policy qualification and cycle detection

**Status: EXPERIMENTAL RECORD / RECURSIVE-EVALUATION PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT16-ის შემდეგ მოწმდება რა ხდება, როცა MATCH_POLICY თვითონ qualifier-ით არის შეზღუდული და applicability evaluation recursive ხდება.

## 1. finite recursive chain

    ES1 → Q1 → R_SCOPE_MATCH → PQ1 → R_LAYER_MATCH

თუ chain committed graph-ში finite და acyclic არის, recursive qualification დასაშვებია და evaluation მთავრდება.

## 2. cycle

ცუდი სცენა:

    R_SCOPE_MATCH
      → PQ1
      → R_LAYER_MATCH
      → PQ2
      → R_SCOPE_MATCH

evaluation path-ზე იგივე address მეორედ გვხვდება intermediate state-ის ცვლილების გარეშე.

დემონი არ აძლევს არც MATCH და არც NO_MATCH შედეგს.

იქმნება addressable cycle/problem record:

    CY1 TYPE → EVALUATION_CYCLE
    CY1 STATUS → OPEN
    CY1 REFERS_TO cycle members ; ROLE CYCLE_MEMBER

## 3. STOP

    STOP_23
    WHERE: DCT17 / recursive applicability evaluation
    WANTED: determine qualifier applicability
    AVAILABLE: addressable recursive policy/qualifier chain
    MISSING: terminating legal evaluation path
    STOP_CLASS: BLOCK

## 4. self-growing justification chain

Applicability evaluation არ უნდა ქმნიდეს ახალ structure-ს მხოლოდ იმავე მიმდინარე evaluation-ის გასამართლებლად. წინააღმდეგ შემთხვევაში regress შეიძლება თვითგენერირებადი გახდეს.

ეს ჯერ WORKING executor-hygiene hypothesis-ია და არა frozen invariant.

## 5. შედეგი

> **Recursive qualification is allowed when the committed justification graph is finite and acyclic. A cycle produces BLOCK, not a fabricated result.**

Emerging principle: every evaluation needs a finite, inspectable justification graph.
