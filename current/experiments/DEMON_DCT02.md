# DEMON_DCT02 — independent recurrence of generic record reference

**Status: EXPERIMENTAL RECORD / ARCHITECTURE PROBE**  
**Date: 2026-10-16**

## 0. მიზანი

DCT01-ის rerun-ის შემდეგ ერთი STOP დარჩა:

> **generic record-to-record structural reference**

DCT02 სპეციალურად შეიქმნა ისე, რომ CONFLICT საერთოდ არ ყოფილიყო.

კითხვა იყო:

> იგივე NEED დამოუკიდებელ ფუნქციაშიც გამოჩნდება თუ არა?

თუ არა — conflict-ის ადგილობრივი patch იქნებოდა.  
თუ კი — უკვე გვექნებოდა განმეორებადი ინფრასტრუქტურული მოთხოვნა.

## 1. საწყისი ქსელი

    T1 = (O1, P1, O2) CURRENT
    T2 = (O2, P2, O3) CURRENT

    R1:
    if (X,P1,Y) and (Y,P2,Z)
    then may construct (X,P3,Z)

ყველა triplet/rule უკვე addressable record-ია DCT01-ის შემდეგ მიღებული WORKING invariant-ის მიხედვით.

## 2. დემონის გავლა

    READ T1
    READ T2
    READ R1

    MATCH
    X = O1
    Y = O2
    Z = O3

    PROPOSE
    T3 = (O1,P3,O3)

T3-ის თვითონ აგება შესაძლებელი იყო.

გაჭედვა გაჩნდა COMMIT gate-ში, რადგან provenance უნდა ყოფილიყო ზუსტად მისამართიანი:

    T3 derived using:
    T1
    T2
    R1

მაგრამ ჯერ არ არსებობდა ზოგადი კანონიერად გაყინული meta-relation, რომლითაც T3
ამ სამ record-ზე მიუთითებდა.

## 3. STOP card

    STOP_05

    WHERE:
    DCT02 / commit derived T3

    WANTED:
    preserve exact derivation provenance

    AVAILABLE:
    T3, T1, T2, R1
    all addressable

    MISSING:
    generic record-to-record structural reference

    STOP_CLASS:
    NEED

    CAN_ASK_OUTSIDE:
    NO

## 4. დამოუკიდებელი განმეორება

DCT01-ში იგივე NEED იყო:

    CONFLICT object
    → conflicting triplet-records

DCT02-ში:

    DERIVED record
    → premise-records / rule-record

ანუ ერთსა და იმავე ხვრელს უკვე ორი დამოუკიდებელი ფუნქცია შეეხო.

ეს არის მიზეზი, რის გამოც generic record-reference აღარ ითვლება ad-hoc conflict patch-ად.

## 5. მინიმალური დამატება

შემოტანილ იქნა WORKING meta-predicate:

    REFERS_TO

მისი მინიმალური მნიშვნელობა:

> **A-ს აქვს მისამართიანი სტრუქტურული მითითება B-ზე.**

იგი თავისით არ ნიშნავს:

    PART_OF
    CAUSE
    EVIDENCE
    SUPPORT
    TRUTH
    AGREEMENT
    SEMANTIC_DEPENDENCY

თუ მომავალში რომელიმე ასეთი როლი რეალურად დასჭირდება ქსელს, ის ცალკე NEED-იდან უნდა დაიბადოს.

## 6. rerun

DCT02:

    T3 REFERS_TO T1
    T3 REFERS_TO T2
    T3 REFERS_TO R1

    CHECK provenance
    → PASS

    COMMIT

STOP_05 ქრება.

ამავე დამატებით DCT01-ის დარჩენილი STOP_01-იც იხსნება:

    CF1 REFERS_TO T1
    CF1 REFERS_TO N1

## 7. Occam result

მიმდინარე ზრდის კვალი:

    addressable triplet/pattern
    → removed 3 STOPs in DCT01

    REFERS_TO
    → removes remaining DCT01 STOP
    → removes independent DCT02 STOP

ამრიგად REFERS_TO აკმაყოფილებს სამუშაო Occam კრიტერიუმს უკეთ, ვიდრე
conflict-specific ახალი predicate.

## 8. მეთოდოლოგიური მნიშვნელობა

DCT02 აძლიერებს მიმდინარე წესს:

> **ახალი ინფრასტრუქტურული ელემენტი არ უნდა დაიბადოს ერთი STOP-ის გამო, თუ შეგვიძლია
> დამოუკიდებელ სცენაში დაველოდოთ იგივე NEED-ის განმეორებას.**

ეს ქმნის არქიტექტურულ ზრდას failure/STOP-ის განმეორებიდან და არა წინასწარი ontology design-იდან.

## 9. საზღვარი

DCT02 არ ამტკიცებს, რომ REFERS_TO საბოლოო და უნივერსალური meta-relation-ია.

ამ ეტაპზე იგი არის:

**WORKING fundamental meta-relation**

და მისი მომავალი ბედი კვლავ ექვემდებარება:
- ახალ STOP-ებს;
- ზედმეტი ambiguity-ის ტესტებს;
- შესაძლო დაშლას უფრო ზუსტ primitive-ებად;
- ან უარყოფას, თუ მოგვიანებით უფრო მცირე მექანიზმი გამოჩნდება.
