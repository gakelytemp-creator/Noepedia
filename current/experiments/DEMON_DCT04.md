# DEMON_DCT04 — independent recurrence of relation-record roles

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT03-ში გაჩნდა NEED:

> **relation-record needs addressable role/qualification**

DCT04 ამოწმებს, განმეორდება თუ არა იგივე ხვრელი სრულიად სხვა კონტექსტში — knowledge credit-ში.

## 1. საწყისი სტრუქტურა

გვაქვს:

```text
KC1 TYPE KNOWLEDGE_CREDIT
MR1 = missing relation
SRC_A = authorization/provenance source
D1 = credit-dependent descendant
```

`REFERS_TO`-თი სამივე კავშირი ტექნიკურად შესაძლებელია:

```text
RF1 = (KC1, REFERS_TO, MR1)
RF2 = (KC1, REFERS_TO, SRC_A)
RF3 = (KC1, REFERS_TO, D1)
```

## 2. გაჭედვა

მხოლოდ `REFERS_TO` არ ამბობს, რომელი reference რა ფუნქციას ასრულებს:

```text
MR1   → debt
SRC_A → authorization/provenance
D1    → dependent descendant
```

ამიტომ:

```text
STOP_07

WHERE:
DCT04 / reconstruct knowledge-credit structure

WANTED:
distinguish semantic function of each REFERS_TO edge

AVAILABLE:
RF1, RF2, RF3
all reference edges addressable

MISSING:
role/qualification of relation-record

STOP_CLASS:
NEED

CAN_ASK_OUTSIDE:
NO
```

## 3. დამოუკიდებელი განმეორება

DCT03:

```text
reference edge → PREMISE / CONTEXT / RULE_USED
```

DCT04:

```text
reference edge → DEBT / AUTHORIZATION / DEPENDENT_DESCENDANT
```

ორი დამოუკიდებელი ფუნქცია ერთსა და იმავე representational need-ს აჩვენებს.

## 4. მინიმალური დამატება

შემოტანილ იქნა WORKING meta-relation:

```text
ROLE
```

მინიმალური მნიშვნელობა:

> **მისამართიან relation-record-ს ამ ადგილობრივ კონსტრუქციაში აქვს კონკრეტული ფუნქციური როლი.**

მაგალითად:

```text
RF1 ROLE DEBT
RF2 ROLE AUTHORIZATION
RF3 ROLE DEPENDENT_DESCENDANT
```

და DCT03-ში:

```text
RF1 ROLE PREMISE
RF2 ROLE PREMISE
RF3 ROLE CONTEXT
RF4 ROLE RULE_USED
```

## 5. საზღვარი

`ROLE` თავისით არ ნიშნავს:

```text
truth
causality
support
priority
ownership
type
```

იგი მხოლოდ local qualification-ია.

უფრო კონკრეტული semantics ქსელში რჩება და საჭიროების შემთხვევაში ცალკე NEED-ებიდან უნდა გაჩნდეს.

## 6. შედეგი

`ROLE`-ის დამატების შემდეგ DCT03 და DCT04 ორივე აღარ საჭიროებს
`PREMISE_OF`, `DEBT_OF`, `SOURCE_OF`, `CONFLICT_MEMBER` და მსგავს
fundamental predicate-ების წინასწარ შექმნას.

მიღებული სამუშაო ძვალი:

```text
addressable triplet
    ↓
REFERS_TO
    ↓
addressable reference-edge
    ↓
ROLE
```

## 7. სტატუსი

`ROLE` არის **WORKING meta-relation**, არა საბოლოო ontology primitive.

მისი შენარჩუნება დამოკიდებულია მომავალ integrated stress tests-ზე.
