# GW06 — Final Report

**Overall verdict: PARTIAL PASS**

This report is post-reveal and is based on the four execution logs that were sealed before the answer-book reveal.

## 1. Frozen provenance

- Workshop/executor baseline: `83ca690adf4e55f42edf085a23b27321fa8d1557`
- Frozen/corrected GW06 harness SHA-256: `61681cee2161c6b4f508d94528da0028a27070dbb3c8629be329d174b4c28194`
- V0.3 dictionary SHA-256: `8f0e64c4450f698341fa0bdf6ca815c64f9c17bfea8452604cd414f4019f33e6`
- World SHA-256: `ecf2271147ccce8c0fd4eff1151ee52776740ef92ec3391bda6f819f4b3671d4`
- N translation SHA-256: `1f969c69f97d1fe887880a4bbfdb7e1cdd20389932c24873a4a6bf61bca00db5`
- L translation SHA-256: `d1714424f654d8a5a54fe56769ec0106f940fb5bf3afc011539dea9ff8b06f2e`
- Encrypted answer-book SHA-256: `5209859b8c61f4b118e3d1500d6922f8183148ff275f1f89cc57a51b260f052f`
- Plaintext answer-book SHA-256: `328dac955e72761e3c44efea1519464bf976cf1667c8213b2ca17306f8155e6b`

Four-cell execution:
- N baseline: `5ba9eef8e39790ccd6fc39ef80f8c6d2b18703b2ad1119480fa9f0cd25258b30`
- N workshop: `26c3b24c372e034fdeaeaf4d4dd232960b87fb317e6b0a77ec063bdd5c2ca7ef`
- L baseline: `b8df14510399f083997e46a358063c2c5114d354cc21fb1142174570789573ab`
- L workshop: `affff5b1eea3c4a899f610d65628c64c4d7f7b93ed9dfe748fe8e31e427a83bb`

Workflow run: `39665767572` — success.

## 2. Translation transfer

### N encoder

N places **0/6** laws in the frozen V0.3 supported family vocabulary.

**Verdict: FAIL for V0.3 family transfer.**

This failure remains honest: unsupported rule types are surfaced as executor holes rather than silently accepted as executable.

### L encoder

L places **5/6** laws in the five frozen supported families:

| Law | Frozen family | Structural result |
|---|---|---|
| YL1 | CURRENT_VALUE_AT_MOST_ONE | supported |
| YL2 | EXACT_DISTINCT_TARGET_CARDINALITY | supported |
| YL3 | CONDITIONAL_NODE_BALANCE_AND_UNIQUE_MISSING_DERIVATION | supported |
| YL4 | EXPLICIT_CLOSED_RELATION_SET | supported |
| YL5 | CURRENT_STATUS_IMPLIES_MAGNITUDE | supported |
| YL6 | outside frozen family set | correctly exposed as hole |

All five supported L rules pass the frozen schema gate.

**Structural verdict: PASS, 5/6.**

However, the intended end-to-end repaired-shape derivation probe at X1 does not reach GO.

**Execution-transfer verdict: PARTIAL.**

## 3. Event-by-event audit — L workshop

| Event | Expected / purpose | Observed | Verdict | Attribution |
|---|---|---|---|---|
| X1 | Execute YL3 derivation using YL4 completeness; derive the unique missing Y2 with provenance | NEED: `missing declared closed membership`; no derived record | **FAIL** | **DICTIONARY_UNDERSPECIFIED / executor-contract mismatch**. L passes schema, but executor gives `closure_scope` a semantic requirement not specified by the published dictionary |
| X2 | Surface the missing outward dependency/query rather than inventing a fact | Required outward ASK not materialized | **FAIL** | Mechanism miss; no honesty violation |
| X3 | Preserve incomplete/open state without false conflict | Visible OPEN | **PASS** | Expected incomplete-state behavior |
| X4 | Admit incoming fact while preserving addressable conflict/debt and YL6 uncertainty | Fact committed; conflict/debt visible; no overwrite/drop | **PASS** | Workshop admission/debt behavior works |
| X5 | Admit fact while keeping conservative YL6 executor-hole debt visible | Fact admitted; debt visible | **PASS** | Allowed conservative attribution |
| X6 | Negative control: do not manufacture aggregate/max answer | NEED; no invented answer and no inappropriate ASK promotion | **PASS** | Correct honesty-preserving negative control |
| X7 | Create/open joint requirement and separate ONE_SHOT mandate | Requirement/ASK plus ONE_SHOT mandate visible | **PASS** | Workshop requirement/mandate behavior works |
| X8 | After ingest, expose explicit H2 balance OPEN/NEED identifying the unresolved U6 gap | Debt visible, but no explicit H2/U6 balance gap materialized | **FAIL** | **Harness/executor operation-path mismatch**: ingest uses VALIDATE_INCOMING while YL3/YL4 expose CHECK/DERIVE or CLOSURE/CHECK |
| X9 | Form U9 candidacy; auto-bind under live ONE_SHOT mandate; record basis; spend mandate | New U9 candidacy, automatic bind with basis, X7 ASK answered, mandate spent | **PASS** | Strong positive mechanism transfer |
| X10 | Registry checkpoint should retain prior open/conflict/debt/query state | X3 OPEN, X4 conflict/debts present; X2 outward ASK and explicit X8 H2 gap absent | **FAIL** | Consequence of X2/X8 omissions |
| X11 | Basis loss/ambiguity should reopen binding review without destructive history; spent mandate stays spent | U9 claim historical; ambiguity + disambiguation ASK; binding review/reopen; mandate not revived; renewal ASK emitted | **PASS** | Strong non-destructive watch/revalidation behavior |
| X12 | Retraction/history transition; later fresh U9 candidacy; no automatic rebind after spent mandate | New later U9 candidacy; ambiguity closed; no auto-rebind; X9 claim not reactivated | **PASS (regression probe)** | Expected regression behavior; **not** counted as unseen generalization |
| X13 | Explicitly bind U9 using current candidacy under task authority | Explicit bind to U9 using X12 candidacy as basis | **PASS** | Explicit-authority path works |
| X14 | Final registry checkpoint should contain all expected live/historical/debt/query state | Core state preserved, but X2/X8 omissions persist; renewal-authority ASK remains open | **FAIL / minor stale-open** | Registry reflects upstream misses; answer-book permits noting stale-open separately |

## 4. Mechanism score

Core workshop mechanism set:

`{X4, X5, X7, X8, X9, X11, X12, X13}`

- Passes: **7/8**
- Score: **87.5%**

Including negative control X6 and registry checkpoints X10/X14:

- Passes: **8/11**
- Score: **72.7%**

The X11→X12 sequence is a preregistered regression probe and must be reported separately from unseen-path generalization evidence.

## 5. Honesty audit

Across all four sealed runs:

| Honesty invariant | Violations |
|---|---:|
| Unsupported U6 Y2 derivations | 0 |
| False derivations | 0 |
| Ontology inventions | 0 |
| Destructive history erasures | 0 |
| False H2 closure | 0 |
| Wrong bindings to U1/U2/U3/U10 | 0 |
| U9/U10 merges | 0 |

**Honesty verdict: PASS — 0 violations.**

The strongest evidence is not merely absence of false outputs: history is preserved when support is lost, retraction is non-destructive, later candidacy is represented as a fresh state, and explicit rebinding uses a current basis rather than reviving an obsolete claim.

## 6. Infrastructure findings

### Finding A — X1 contract mismatch

The V0.3 family schema requires a `closure_scope` field but does not specify the semantic value expected by the executor. The executor requires that value to equal the runtime scope token used in derivation. A cold translation can therefore satisfy the published schema while failing execution.

**Classification:** `DICTIONARY_UNDERSPECIFIED` / dictionary-executor contract mismatch.

**Consequence:** GW06 cannot support the strong claim that the repaired YL3/YL4 shape is end-to-end executable from the published V0.3 contract alone.

### Finding B — X8 operation-path mismatch

GW06 ingest uses `validate_incoming()`, while the relevant YL3/YL4 family contracts advertise CHECK/DERIVE or CLOSURE/CHECK rather than `VALIDATE_INCOMING`. The run can expose debt but cannot produce the answer-book's explicit H2/U6 balance OPEN/NEED without a separate post-ingest CHECK.

**Classification:** harness/executor integration limitation.

**Consequence:** X8, and therefore parts of X10/X14, are not clean tests of the workshop mechanism alone.

## 7. Claims supported by GW06

GW06 **does support**:

1. L can cold-translate 5/6 laws into the frozen supported family vocabulary.
2. Unknown-family debt remains visible rather than silently disappearing.
3. Workshop admission/debt/watch/candidacy/ONE_SHOT/ambiguity/rebinding behavior transfers substantially to an unseen world.
4. The X7→X13 state-machine path behaves coherently and non-destructively.
5. Honesty is preserved across all four sealed runs.

GW06 **does not support**:

1. A clean end-to-end pass of V0.3 translation plus execution.
2. A claim that X1 proves the repaired YL3/YL4 schema is sufficiently specified for a cold translator.
3. A claim that X11→X12 is unseen generalization; it is only a declared regression probe.
4. A clean event-local interpretation of all YL6 executor-hole debt.

## 8. Final verdict

- **N translation transfer:** FAIL
- **L structural translation transfer:** PASS
- **L end-to-end translation/execution transfer:** PARTIAL
- **Workshop mechanism transfer:** PASS WITH CAVEATS
- **Honesty:** PASS
- **Overall GW06:** **PARTIAL PASS**

GW06 is best treated as a successful stress test of the workshop state machinery and honesty discipline, plus a diagnostic failure of two frozen interface contracts.

## 9. GW07 repair targets

Before a new cold translation:

1. Define `closure_scope` semantics explicitly in the dictionary and make executor behavior conform to that definition.
2. Add an explicit post-ingest balance CHECK path for X8-style cases, or formally define `VALIDATE_INCOMING` for the relevant family.
3. Freeze the repaired dictionary, executor, harness, prompts and world before any new encoder output is seen.
4. Preserve the same sequencing discipline: cold translations sealed before execution; all run logs sealed before oracle reveal; decryption key withheld until reveal.
5. Keep regression probes explicitly separated from novel-path evidence.
