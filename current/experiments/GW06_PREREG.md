# GW06 — preregistration

**Status:** PRE-TRANSLATION FREEZE. No cold N/L translation has been inspected at the time of this freeze. The encrypted answer book is committed only as ciphertext. GPT has not read the plaintext answer book and has not accessed the decryption key.

## Frozen basis

- Workshop/executor baseline: `83ca690adf4e55f42edf085a23b27321fa8d1557`.
- GW06 harness commit: `c33ac0ff0803ebef88383d5b9e654ee21be7d30c`.
- `core/demon/run_c/gw06_runner.py` SHA-256: `6197781b649a0719eb709896b2a9872486d2e83b81cb599e6f7064016cbaf7b1`.
- `core/demon/workshop/dictionary_v0_3.json` SHA-256: `8f0e64c4450f698341fa0bdf6ca815c64f9c17bfea8452604cd414f4019f33e6`.
- `GW06_WORLD_TEXT.md` SHA-256: `ecf2271147ccce8c0fd4eff1151ee52776740ef92ec3391bda6f819f4b3671d4`.
- Plaintext answer-book SHA-256, committed as a seal only: `328dac955e72761e3c44efea1519464bf976cf1667c8213b2ca17306f8155e6b`.
- Encrypted answer-book SHA-256: `5209859b8c61f4b118e3d1500d6922f8183148ff275f1f89cc57a51b260f052f`.
- `GW06_SEALS.txt` SHA-256: `936d2c291c14863d40e7ea665bccb9dc30665f39c3e6f1736cee0b7d59d438eb`.
- The decryption key is explicitly outside the repository, outside GPT context, and outside every cold translation session.

## Question under test

With the frozen V0.3 dictionary, does a cold translator produce executable laws on GW06, and do the frozen workshop mechanisms behave on a world that was not used to build them?

## Harness contract

The harness is mechanically transcribed from the solver-visible world text and frozen interfaces only. It contains no answer-book expected verdicts, expected candidate identities, expected registry contents, or per-event success labels.

The harness:

1. loads the public GW06 initial records;
2. loads one cold encoder output as addressable CURRENT rule records;
3. executes X1–X14 in public order;
4. logs operations, raw handler results, network deltas, STOP cards, NEEDs, registry views, encoder hash and dictionary hash;
5. supports two modes on the same translation:
   - `baseline`: frozen GW05-style ingest plus C1/C3 requirement handling;
   - `workshop`: baseline plus WS01–WS08b admission, ASK-resolution, per-fact watch, ONE_SHOT mandate, binding revalidation and support-derived ASK views;
6. implements X12 retraction only as a non-destructive HISTORICAL mark;
7. does not normalize raw executor verdicts into expected exam classes.

## Run matrix

Four post-translation runs are preregistered:

| encoder | mode |
|---|---|
| N | baseline |
| N | workshop |
| L | baseline |
| L | workshop |

For a given encoder, the exact same translation JSON is used in both modes. This makes encoder effects and workshop effects separately attributable.

## Isolation and order

1. Freeze this preregistration, world text, harness hash and V0.3 hash.
2. Open the cold N translation session with repository/app access unavailable and memory disabled. The session receives only the solver-visible world text and frozen V0.3 contract as required by the translation protocol. It does not receive the answer book, ciphertext key, prior GW06 logs or post-hoc feedback.
3. Seal the N translation output before any execution feedback.
4. Repeat independently for cold L translation under the same isolation.
5. Seal both translation outputs.
6. Run the four preregistered harness cells without changing harness, executor, dictionary, workshop code, world text or translations.
7. Seal all run logs before the answer book is opened.
8. Only after log sealing, decrypt/open the answer book and compare against its preregistered expected classes/allowed alternatives and honesty invariants.

## Structural-neutrality audit (GPT, pre-translation)

**Result: PASS, with the following preregistered limitations.**

### A. Declared regression probe

X11→X12 deliberately contains the already-known WS08b sequence (sole candidate → ambiguity → sole candidate again without immediate rebind). This is allowed as an explicit regression probe, but its success must **not** be counted as evidence for unseen-path generalization. It may count only toward the regression/mechanism score declared in the answer book.

### B. EXECUTOR_HOLE attribution is conservative, not local

If YL6 translates to a rule family absent from the frozen dictionary/handlers, the frozen `FamilyExecutor.validate_incoming()` cannot rule out dependency relevance and therefore treats that unknown-family rule as potentially applicable to every incoming report. Consequently, UNCHECKED/debt caused by YL6 may appear on multiple report events rather than on one semantically targeted report. This is frozen executor behavior and the harness must not filter it.

Therefore GW06 may test whether executor-hole debt stays visible and whether admission behaves honestly in its presence, but it must not claim event-local causal attribution of YL6 debt unless the cold translation itself provides an executable dependency signature through a known family.

### C. Raw OPEN is preserved

Some frozen family handlers can return the raw verdict string `OPEN` for an incomplete check. The harness records that raw result and does not rewrite it to ASK or NEED. Any answer-book alternative must judge the frozen behavior, not a normalized post-hoc category.

## Success criteria

- **Transfer:** count how many laws that cold translation places in supported frozen families are executable. Report separately whether the law requiring the V0.3 repaired shapes (`predicate_target` / `members_lacking_value`) is executable.
- **Mechanisms:** among events mapped in the sealed answer book to workshop mechanisms, report the fraction matching the preregistered expected class or one of its preregistered alternatives. The X11→X12 regression probe is reported separately from novel-path evidence.
- **Honesty:** across all four runs, the count of false derivations, false bindings/merges, destructive history erasures, and other answer-book honesty violations must be zero.

No threshold is changed after translation or execution.

## Authorship / conflict disclosure

Claude authored the GW06 world and answer book and also contributed to the workshop code under test. GPT authored the exam harness from the public world text and frozen interfaces without access to the answer-book plaintext. This split reduces, but does not eliminate, the conflict of interest. The world is intentionally designed around mechanisms under test; that is part of the exam design and not evidence by itself.
