# GW06 — Claude Review Reconciliation

**Status:** POST-REVEAL EXTERNAL REVIEW RECONCILIATION

This record reconciles Claude's independent post-reveal review with GPT's prior GW06 audit. Claude authored the GW06 world, answer book, and much of the workshop code, so the review is independent of GPT's audit but not independent of the experiment itself.

## Accepted corrections

### 1. Core score must be split

The prior report pooled X11–X12 into a single 7/8 "core mechanism" score. PREREG requires the X11→X12 regression probe to be reported separately from novel-path evidence.

Corrected breakdown:

- novel core `{X4, X5, X7, X8, X9, X13}`: **5/6**
- regression probe `{X11, X12}`: **2/2**

The pooled 7/8 may be retained only as a descriptive aggregate, not as the preregistered generalization score.

### 2. X10 and X14 are not independent failures

X10 mainly reflects the already-counted X2/X8 omissions.

X14 mainly reflects those same upstream omissions plus one new minor `STALE_OPEN` on the renewal-authority ASK.

Therefore:
- X10 adds no independent mechanism miss.
- X14 adds only the minor stale-open condition beyond earlier misses.

The prior extended 8/11 figure is conservative but double-counts failure consequences and should not be used as the primary mechanism score.

### 3. X8 attribution is shared with the answer book

The frozen harness contract did not promise a post-ingest balance CHECK. The answer book nevertheless expected an explicit H2/U6 balance OPEN/NEED.

Corrected attribution:
- harness/executor integration limitation; **plus**
- partial **ANSWER_BOOK_ERROR**.

The score remains a miss because changing the preregistered oracle after reveal would violate protocol.

### 4. X1 wording should name the incomplete WS05 repair

Claude confirms the prior `DICTIONARY_UNDERSPECIFIED` attribution.

Additional finding: this should be stated as an **incomplete V0.3/WS05 contract repair**, not merely a generic stack mismatch. The dictionary requires `closure_scope` but does not constrain the semantic value expected by the executor.

Positive evidence should also be stated explicitly:
- L's YL3 uses the repaired `link_filter` shape;
- L's YL3 uses the parameterized `members_lacking_value` shape.

Thus **shape transfer succeeded**, while **semantic transfer failed** at X1 because the published contract remained underspecified.

### 5. "Unseen-world generalization" claim is too strong

The prior final report overstated what X7–X13 establishes.

N × workshop follows X7→X13 identically despite N having zero executable laws. This shows that much of that path is driven by public-script/C1 machinery rather than law translation.

Further, X7–X13 is structurally close to scenarios used to build the workshop mechanisms, and X11→X12 is explicitly a known regression probe.

Corrected claim:
- X7–X13 supports **renamed-replay robustness / state-machine robustness**;
- it should **not** be presented as strong unseen-path generalization evidence.

The genuinely novel mechanism evidence is narrower, especially X4/X5, with X8 as the principal miss.

### 6. Honesty claim remains PASS, with an observability limit

The zero honesty-violation result remains supported.

However, the logs' `NETWORK_DELTA` records CREATED/CHANGED state but does not independently prove the absence of removals. The "no deletion" statement relies additionally on code inspection.

Future harnesses should log removals explicitly.

## Process-record additions

### A. Claude exposure to N translation before runs

The cold N translation was pasted into Claude's session before the four runs.

This exposure is judged non-causal because:
- the harness and answer book were already frozen;
- Claude made no change/comment that affected execution;
- the four run logs were later sealed before answer-book reveal.

Nevertheless, the exposure must be recorded as a process event.

### B. L contamination chronology qualifier

The reinstatement of the pre-contamination L output rests on the experimenter's chronology: L output was produced before the N output was pasted into the same chat.

The chat hash proves the session identity but does not independently prove message-order timing of the preserved bytes.

Therefore all L-dependent results should carry the qualifier:

> **conditional on the chronology recorded in GW06_COLD_L_CONTAMINATION_CORRECTION_01.md**

This does not invalidate the run, but it limits independent verifiability of the contamination correction.

## Corrected verdict framing

- **N translation transfer:** FAIL
- **L structural shape transfer:** PASS (5/6 supported families; repaired YL3 shapes present)
- **L semantic/end-to-end transfer:** FAIL/PARTIAL because X1 does not execute under the underspecified closure-scope contract
- **Novel mechanism evidence:** 5/6
- **Regression probe:** 2/2
- **Renamed-replay/state-machine robustness:** positive
- **Honesty:** PASS, 0 violations, subject to the removal-observability limit
- **Overall GW06:** **PARTIAL PASS**

No code changes are proposed in this reconciliation.
