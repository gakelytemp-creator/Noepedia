# DEMON_DCT22 — multi-level invalidation wave

**Status: EXPERIMENTAL RECORD / DEPENDENCY-WAVE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT21-ის შემდეგ მოწმდება რა ხდება, როცა composition policy თვითონ დგას justification-ზე და ეს upstream justification იცვლება.

## 1. dependency chain

    PJ1
      ↓ supports
    CP1
      ↓ governs
    EV1
      ↓ supports
    T3

CP1 თავისთავად არაა უსაფუძვლო:

    CP1 REFERS_TO PJ1 ; ROLE JUSTIFICATION

## 2. upstream change

შემოდის:

    PJ1 → CHALLENGED

დემონი dependency path-ს ხედავს, მაგრამ downstream statuses-ს თვითონ არ იგონებს.

## 3. edge-local propagation

თითოეულ edge-ს შეიძლება თავისი consequence policy ჰქონდეს.

მაგალითად:

    PJ1 challenged → CP1 OPEN

შემდეგ სხვა policy შეიძლება განსაზღვრავდეს რას ნიშნავს CP1 OPEN EV1-ისთვის.

> **Propagation is edge-local.**

## 4. first missing edge policy

თუ PJ1→CP1 consequence policy არ არსებობს:

    STOP_28
    WHERE: DCT22 / policy support changed
    WANTED: determine consequence for CP1
    AVAILABLE: PJ1 challenged; CP1 depends on PJ1
    MISSING: dependency consequence policy
    STOP_CLASS: NEED

თუ პირველი ნაბიჯი გადაწყვეტილია, მაგრამ CP1→EV1 consequence policy არ არსებობს:

    STOP_29
    WHERE: DCT22 / downstream wave frontier
    WANTED: determine consequence for EV1
    AVAILABLE: CP1 changed; EV1 uses CP1 as composition policy
    MISSING: downstream consequence policy
    STOP_CLASS: NEED

## 5. wave may stop

თუ CP1-ს ორი justification აქვს და composition policy ამბობს ALTERNATIVE, მაშინ PJ1-ის challenge შეიძლება მეორე surviving justification-მა შეაკავოს.

ანუ:

    upstream change
    → local re-evaluation
    → surviving sufficient support
    → propagation stops

## 6. wave may continue

თუ local support აღარ არის საკმარისი:

    upstream change
    → local support lost
    → edge-local consequence
    → next node re-evaluation

## 7. შედეგი

> **A change propagates only through explicit dependency edges and their policies.**

> **Each downstream node is re-evaluated locally; a wave may stop when sufficient support survives.**

> **There is no default global invalidation cascade.**

> **The demon follows the dependency graph until support survives, a rule blocks, or a required propagation policy is missing.**
