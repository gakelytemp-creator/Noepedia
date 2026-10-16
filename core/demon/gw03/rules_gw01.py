#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rules_gw01.py — GW01-ის წესები, როგორც დეკლარაციული ჩანაწერები (GW03).

ეს ფაილი მხოლოდ მონაცემია: არც ერთი ფუნქცია, არც ერთი განშტოება.
ყოველ ჩანაწერს ახლავს QUOTE — ზუსტი ციტატა WORLD_INPUT.md-დან
(sha256 841ddd53…), რომლის მიმართაც აუდიტი ამოწმებს თარგმანს.

ტიპების ლექსიკონი (GW03_DESIGN §2-ის ჰიპოთეზა): CARDINALITY_POLICY,
DERIVATION, TEMPORAL_POLICY, INGEST_GUARD, CLOSURE_POLICY, INVARIANT.
ცვლადები იწყება "?"-ით. წესის საგანი პრედიკატი ინახება RULE_PREDICATE
ველში (და არა PREDICATE-ში), რათა წესის ჩანაწერი SPO-ფაქტად არ წაიკითხოს
— წესი ქსელის ბინადარია, მაგრამ არა სამყაროს ფაქტი.

ENCODER-ის შენიშვნები (პატიოსნად, თარგმანის ყოველ არჩევანზე):
  [EN-1] R4: ტექსტი არ ამბობს, რა ქნას დარაჯმა, როცა პირობის (Y,P3) წყვილი
         multiplicity-გაურკვევლობაშია. ჩანაწერი ამას არ წყვეტს — evaluator-ის
         ზოგად სემანტიკას რჩება (იხ. generic_evaluator guard_stops).
  [EN-2] წყაროს კლასი: "VIS* = vision" — კლასად ვთვლით პრეფიქსს ციფრების
         მოჭრით (VIS2→VIS). ტექსტის glob-აღნიშვნის ერთ-ერთი წაკითხვაა.
  [EN-3] R2/R3: "derive" ნებადართულია და არა სავალდებულო — saturation vs
         goal-directed არჩევანს ტექსტი არ აკეთებს (იხ. evaluator-ის შენიშვნა).
"""

RULES = [
    dict(addr="R1", RULE_TYPE="CARDINALITY_POLICY",
         RULE_PREDICATE="P1", POLICY="SINGLE_CURRENT_TARGET",
         QUOTE="R1  P1 is SINGLE_CURRENT_TARGET: an object has at most one "
               "current P1 target."),

    dict(addr="R2", RULE_TYPE="DERIVATION",
         PREMISES=[("?X", "P2", "?Y"), ("?Y", "P1", "?Z")],
         CONCLUSION=("?X", "P1", "?Z"),
         QUOTE="R2  (X P2 Y) and (Y P1 Z)  => derive (X P1 Z). Derivation "
               "authorized (CREATE_ADDRESS allowed), must REFERS_TO premises "
               "and rule."),

    dict(addr="R3", RULE_TYPE="DERIVATION",
         PREMISES=[("?X", "P1", "?Y"), ("?Y", "P1", "?Z")],
         CONCLUSION=("?X", "P1", "?Z"),
         QUOTE="R3  (X P1 Y) and (Y P1 Z)  => derive (X P1 Z). Same "
               "authorization as R2."),

    dict(addr="R4", RULE_TYPE="INGEST_GUARD", SOURCE_CLASS="VIS",
         CONDITION=("?Y", "P3", "S1"), FORBIDDEN=("?X", "P1", "?Y"),
         QUOTE="R4  If (Y P3 S1) then records of form (X P1 Y) are not "
               "observable by source class VIS."),

    dict(addr="R5", RULE_TYPE="TEMPORAL_POLICY",
         RULE_PREDICATE="P1", POLICY="LATER_TIME_SUPERSEDES",
         DEMOTE_TO="HISTORICAL",
         QUOTE="R5  For P1 under R1: a P1 assertion with later TIME supersedes "
               "an earlier one (earlier becomes HISTORICAL, not deleted)."),

    dict(addr="R6", RULE_TYPE="CLOSURE_POLICY",
         RULE_PREDICATES=["P4", "P5"], POLICY="NO_CLOSURE",
         QUOTE="R6  P4 and P5: no closure rule exists. Absence of a P4/P5 "
               "record says nothing."),

    dict(addr="C1", RULE_TYPE="INVARIANT",
         PATTERN=("O7", "P1", "O1"), REQUIRED_STATE="CURRENT",
         QUOTE="C1  Scene constraint: (O7 P1 O1) must remain current for the "
               "whole scene."),
]
