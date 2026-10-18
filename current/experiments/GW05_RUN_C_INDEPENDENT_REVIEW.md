# GW05 RUN C — independent decision review

**Status: REVIEW RECORD (step 6 of the RUN C gate sequence)**
**Date: 2026-10-18 · reviewer: Claude**
**Reviewer conflict, stated openly:** the reviewer authored the GW05 world and the sealed GW05 answer book. This review is written in generic terms and refers to no GW05 content. Any code change made after this review must be logged as a post-review decision (see §5).

## 0. Artifacts reviewed (hashes verified at repo HEAD `d269373`)

| artifact | sha256 |
|---|---|
| GW05_RUN_C_FAMILY_DICTIONARY.json | `2f926863…61f0cb87` ✓ |
| run_c/family_executor.py | `c95c959b…6683bbe` ✓ |
| GW05_RUN_C_DECISION_LOG.json | `efd98ab0…78c83ce` ✓ |

Tests: PASS (run with `PYTHONPATH=core/demon`; without it the test file fails to import `demon_core`, which is a minor reproducibility note). Static audit: GENERALITY_GATE PASS, 0 text hits, 0 AST hits — reproduced.

## 1. Counts

```
AUTHOR_DECISION_COUNT   = 14
REVIEWER_DECISION_COUNT = 26   (14 author decisions accepted + 12 additional loci below)
DECISION_UNDERCOUNT     = 12
```

All 14 author entries are accepted as genuine decisions. RC-D13 and RC-D14 are process/evaluation decisions rather than executable semantics; they are counted, but a reader may prefer to report 12 executable + 2 process.

## 2. Additional decision loci (not in the author log)

| ID | locus | underspecified point | choice made silently in code | semantics affected |
|---|---|---|---|---|
| RV-01 | `current_records` | what "current" means | a record is current iff its **last** status assertion is literally `CURRENT`; scope/time qualifiers (DCT13–15) are ignored | YES |
| RV-02 | `_eval_expression` | which values are numeric | only Python `int`; `bool` passes as int; floats/strings count as missing | YES |
| RV-03 | lookup expression | lookup with several current values | treated as *incomplete* (not as conflict), and `missing_subjects` is empty in that case | YES |
| RV-04 | aggregate expression | a member with **several** current values | treated as **missing**. Consequence: if that member is the unique "missing" one, DERIVE can propose a further value for a subject that already has conflicting values. Possible EXECUTOR_ERROR path | YES |
| RV-05 | `_equality_sides` | evaluation order of the two sides | right is computed against left subjects; left re-evaluated only if it has an `all` filter. Asymmetric, order-dependent | YES |
| RV-06 | filter / binding tokens | which literal schema tokens are accepted | code hard-codes `"scoped_node"`, `"other_links_than_left"` (alias of the dictionary's `other_members_than_other_side`), `"same_link"` | YES |
| RV-07 | `handle_balance` DERIVE | role of the closure record | closure is used only as a **gate** (a matching closure exists); the member set is still taken from current records, never compared with `exact_members`. A closed member lacking its membership record is invisible to the derivation | YES |
| RV-08 | exact cardinality VALIDATE_INCOMING | re-assertion of an already-current identical fact | counted as a non-distinct duplicate → BLOCK | YES |
| RV-09 | implication VALIDATE_INCOMING | which direction is validated on ingest | only incoming **antecedent** facts are checked; an incoming consequent-position value that breaks the implication for a subject already satisfying the antecedent is not checked at ingest | YES |
| RV-10 | implication CHECK | request without SUBJECT | `subject=None` matches every subject in `current_matches`; check silently becomes global | YES |
| RV-11 | schema mismatch handling | how a non-conforming record is reported | `SchemaError` exception (aborts) rather than a structured `SCHEMA_DRIFT` result | YES (for GW05-N/L classification) |
| RV-12 | dictionary completeness | which field paths the target schema requires | dictionary lists only top-level `required_fields` for the balance family; handlers additionally read `balance.excluded_nodes`, `balance.equality.{left,right}`, `derivation.conditions[].adjacent_link_set.closure_declared_by`, `lookup.subject`, and the tokens in RV-06. An encoder following the dictionary cannot know these paths | YES (dictionary is under-specified relative to its own handlers) |

## 3. Structural findings (more important than the count)

**F1 · The UNCHECKED mechanism is unreachable.**
`unchecked_marker()` is defined but never called anywhere in `core/demon`. `validation_dependencies()` only considers rules whose `RULE_TYPE` is in the dictionary. A rule that is an EXECUTOR_HOLE (unknown type) therefore has no dependency signature and can never be found as a dependency. A SCHEMA_DRIFT rule (known type, different shape) resolves its signature paths to nothing and also never matches. The two cases the marker was designed for both fall outside it. Tests do not exercise the marker.

**F2 · The dictionary does not fully define the compiler target** (RV-12 + RV-06). For GW05-L this matters directly: an encoder that complies perfectly with the dictionary as written may still be unreadable by the handlers. Without a fix, GW05-L cannot separate ENCODER_NONCOMPLIANCE from dictionary incompleteness. A practical criterion: *every field path and every literal token any handler reads must appear in the dictionary.* That is also a mechanical gate: string literals in handler code ⊆ dictionary vocabulary ∪ generic core vocabulary.

**F3 · Generality gate is correct for what it tests, but tests one thing.** It catches world identifiers (and after RC-D14, bare category tokens). It does not catch **schema-instance tokens** from one translation (`scoped_node`, `same_link`, `adjacent_link_set`, `other_links_than_left`). These carry no world content, but they bind the handlers to the GW04 encoder's wording; some contain domain-flavoured words ("link"). The F2 gate would cover this.

## 4. Things that are clearly good

- Open-world handling is consistent: undercount → OPEN (RC-D05), open-membership mismatch → OPEN (RC-D10), missing consequent → NEED (RC-D07), no automatic supersession (RC-D06).
- Derivation only for the uniquely determined numeric value (RC-D04) and request-subject/predicate guards prevent unasked derivations.
- Handlers return structured results, never event answers; no event or world identifiers present.

## 5. Recommendation on what may change before freeze

The design places this review *before* the final freeze, so changes are permitted. Because the reviewer knows the GW05 answer book, I recommend limiting post-review changes to items where the code fails **its own written design**, not to semantic preferences:

- **F1** (marker unreachable) — design promised it; fixing it is restoring the spec.
- **F2 / RV-12** (dictionary lists every path/token handlers read) — needed for GW05-L to mean what it claims.
- **RV-11** (structured SCHEMA_DRIFT instead of exception) — needed for the preregistered classification.

All other RV items (RV-01…RV-10) should be **logged, not changed**, as additional decisions with their current choices. Each change made must get its own post-review DECISION_ID, and the final count reported as author / reviewer / post-review.
