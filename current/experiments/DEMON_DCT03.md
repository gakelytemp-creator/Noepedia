# DEMON_DCT03 — reference-role ambiguity

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT02-ის შემდეგ `REFERS_TO` შევიდა როგორც WORKING generic record-to-record meta-relation.

DCT03 ამოწმებს მეორე მხარეს:

> **არის თუ არა REFERS_TO იმდენად ღარიბი, რომ ზუსტი provenance-ის აღდგენა ვეღარ მოხდეს?**

## 1. საწყისი სტრუქტურა

გვაქვს derived record `T3`, რომელიც ოთხ record-ზე მიუთითებს:

```text
RF1 = (T3, REFERS_TO, T1)
RF2 = (T3, REFERS_TO, T2)
RF3 = (T3, REFERS_TO, T0)
RF4 = (T3, REFERS_TO, R1)
```

სადაც:

```text
T1 = premise
T2 = premise
T0 = contextual record
R1 = applied rule
```

ყველა REFERS_TO edge თვითონაც addressable triplet-record-ია.

## 2. გაჭედვა

დემონს შეუძლია ნახოს ყველა reference, მაგრამ მხოლოდ `REFERS_TO`-დან ვერ არჩევს,
რომელი reference რა ფუნქციას ასრულებს.

```text
STOP_06

WHERE:
DCT03 / exact provenance reconstruction

WANTED:
distinguish premise-reference from contextual/rule reference

AVAILABLE:
RF1, RF2, RF3, RF4
all addressable

MISSING:
role/qualification of each relation-record

STOP_CLASS:
NEED

CAN_ASK_OUTSIDE:
NO
```

## 3. რატომ არ შეიქმნა ბევრი ახალი predicate

პირველი შესაძლო რეაქცია იქნებოდა:

```text
PREMISE_OF
CONTEXT_OF
RULE_USED
SOURCE_OF
```

მაგრამ ეს იქნებოდა ontology-ის სწრაფი გასქელება.

Addressable-triplet invariant გვაძლევს სხვა შესაძლებლობას:

> თვითონ reference-edge არის record და შეიძლება მასზე დაიწეროს დამატებითი relation.

კანდიდატი:

```text
RF1 ROLE PREMISE
RF2 ROLE PREMISE
RF3 ROLE CONTEXT
RF4 ROLE RULE_USED
```

## 4. შედეგი

DCT03-ის ბოლოს `ROLE` ჯერ არ გაყინულა.

მიღებული NEED:

> **relation-record needs addressable role/qualification**

მეთოდოლოგიური გადაწყვეტილება: ერთი სცენა საკმარისი არ არის ახალი fundamental meta-relation-ისთვის.

ამიტომ DCT03 დასრულდა OPEN/NEED-ით და გადავიდა დამოუკიდებელ recurrence test-ზე — DCT04.
