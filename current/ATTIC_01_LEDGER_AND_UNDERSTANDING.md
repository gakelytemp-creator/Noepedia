# ATTIC 01 — Ledger, dreams, and the quality of understanding

**Status: ATTIC NOTE (conceptual working hypotheses). NOT a specification. Nothing here is tested.**
**Period: 2026-10-18 … 2026-10-21 · participants: experimenter (Gakely), GPT (window A), Claude**
**Draft: Claude. Status labels to be reviewed by GPT and finalized by the experimenter.**

Status labels used on every item:

- **AGREED**: all three participants accepted it.
- **PROPOSED**: one participant put it forward and nobody objected, but it was not explicitly accepted.
- **OPEN**: an unresolved question.

Promotion rule: an item moves into `DEMON_CORE` / `DCT` only after it has been built and exercised in the workshop. A demonstration-grade claim additionally needs a sealed world (§0).

---

## 0. Working mode

- **A0.1 · AGREED.** The glass-world laboratory is closed after GW05. GW01–GW05 are now training scenes, not tests.
- **A0.2 · AGREED.** We are in **workshop mode**: build, break and rebuild freely. No seals, no preregistration, no isolation. Results from this mode are reported as "works on scene S", never as "works".
- **A0.3 · AGREED.** **Exam mode** is used only when a claim must be demonstrated. It means one new sealed world, one short protocol, one run. The rule is: *building is free, claims are sealed.*
- **A0.4 · AGREED.** Traceability (hashes, logs, decision counts) is produced by tooling, not by hand. If a participant is asked to copy IDs or recount lines manually, the tooling is at fault.

## 1. The demon is an operator, not an individual

- **A1.1 · AGREED.** Demons are repeated invocations of one operator. Any number may run, in any layer. Which invocation performed a step is architecturally irrelevant.
- **A1.2 · AGREED.** Provenance records *what* was done and *on what basis*: source, rule, premises, time/scope, transaction trace. It never records *which demon* did it. Demon identity is never an argument in conflict resolution.
- **A1.3 · PROPOSED (Claude).** **Idempotence through content addressing.** CREATE_ADDRESS must be deterministic: the same premises and the same rule always give the same address, so duplicate work by two demons collapses into one record. Without this, anonymity produces twins.

## 2. The network is a monotone ledger

- **A2.1 · PROPOSED (Claude), not contested.** The network is an append-only ledger of assertions: facts, conflicts, OPENs, UNCHECKED markers, interpretations, confirmations. A "current status" is never stored destructively. It is a **view computed from the ledger**.
- **A2.2 · PROPOSED (Claude).** Operations fall into two classes.
  - **Class 1, additions.** These are monotone and commute. They are safe under any interleaving of any number of demons, with no coordination.
  - **Class 2, absence claims.** These depend on something being absent: closure ("exactly these members"), Freedom=1 derivation ("all others are known"), supersession (CURRENT → HISTORICAL), and independence of support paths (§9). Every class-2 claim carries the **network state N** it was made on. If N has changed by commit time, the claim is re-checked.
- **A2.3 · PROPOSED.** Background: the CALM result (Hellerstein et al., ~2010) says monotone programs are exactly the ones that are consistent without coordination.
- **A2.4 · AGREED (GPT).** If an outcome depends on the order in which two demons ran, then either the operations were non-commutative, and this must be visible, or the concurrency semantics has a hole.
- **A2.5 · PROPOSED (Claude).** After A2.1–A2.2, the only order-sensitive operations left are class 2. The N-stamp on an absence claim is the only timestamp a record strictly needs.

## 3. One principle for D1 and D2

- **A3.1 · PROPOSED (Claude), not contested.** **"The signal is recorded; the fact enters with a status."** A detected violation is never swallowed (D1) and never vetoes ingest (D2). The fact is committed, and alongside it a visible CONFLICT or UNCHECKED record.
- **A3.2 · PROPOSED.** Verdict aggregation is asymmetric: a negative signal never disappears from the aggregate. It can be outweighed, but it always leaves a record.
- **A3.3 · PROPOSED.** Under A3.1, BLOCK becomes a monotone addition, and that is what makes A2 achievable. Epistemic correctness and parallelism come from the same design decision.
- **A3.4 · PROPOSED (GPT).** Keep **epistemic composition** separate from **admission / commit policy**. The working pipeline is: `handler evidence → evidence composition → materialization → admission policy → commit verdict`. A verdict may decide transaction legality, but it must never substitute for, or erase, the evidence that produced it.
- **A3.5 · PROPOSED (GPT).** Handler-verdict aggregation and admission policy are candidates to become **addressable network composition-policy records**, rather than hard-coded executor heuristics. This would continue the GW03 / DCT19–21 direction: move another hand-written choice out of code and into the network.

## 4. Concept and name

- **A4.1 · AGREED.** A concept is order-independent (commutative). A name is historical, because the label goes to whoever came first. The experimenter's example: had the positron been known first, the electron would be the "negatron". Anderson did propose that term in 1933.
- **A4.2 · AGREED.** Address ≠ name. REFERS_TO links them. A concept's address comes from content. A name is a scoped, historical assertion, and many names can coexist with status transitions rather than deletion.
- **A4.3 · PROPOSED (Claude).** *A concept is what stays commutative when history is subtracted.* Order can still leak into content through framing choices (what counts as "normal" vs "anti"). A frame is a deeper-seated name.

## 5. Idle-time work ("carving clubs")

- **A5.1 · PROPOSED (Claude).** Since a demon exists only when invoked, "what does an idle demon do" means "does the scheduler invoke demons on internal targets when nothing arrives". Candidate layers, from safest to riskiest:
  1. **Re-check stale class-2 claims**, meaning any absence claim whose N is older than the current N. Pure inventory, creates nothing.
  2. **Carve questions.** Walk the OPEN registry and turn OPENs into ready ASKs, ranked by how many OPENs one answer would resolve.
  3. **Targeted derivation.** Push chains further, but only where an OPEN or requirement points, and within a budget.
  4. **Hypotheses (dreams).** See §6.
- **A5.2 · PROPOSED.** Idle work is interruptible: the first external event stops it. Because it only adds, stopping it damages nothing.
- **A5.3 · PROPOSED.** The idle agenda is structural (registries, stale N, OPENs), never content-driven, so the demon stays content-blind at night too.
- **A5.4 · PROPOSED.** Layer 1 would also catch D4-type stale ASKs.

## 6. Dreams: relaxation, lesson, and the debt ledger

- **A6.1 · AGREED (experimenter's correction).** Dreaming, choosing among dreams, and bringing a dream out are three different operations.
- **A6.2 · AGREED.** A dream is often an **act of learning**. It has two layers:
  - **Frame**: the relaxed, unquestionable background, with "authenticity stamps" that cannot be doubted inside the dream.
  - **Foreground lesson**: the real, strenuous exercise.

  The frame's lock is the method, not a defect: it keeps attention on the lesson. *The lesson transfers; the world does not.* This is the same pattern as simulator training in robotics.
- **A6.3 · AGREED.** Choosing among dreams is goal-directed, and its mechanism is considered clear.
- **A6.4 · AGREED.** Bringing a dream out is **galvanic re-grounding**. In the dream, only form passes, as through a transformer. To bring it out, the result must be disconnected from the ideal ground and connected to the real one. In waking mode the relaxed constraints are re-enabled, and each one must be either satisfied or worked around, so that the result becomes functional and pragmatic.
- **A6.5 · PROPOSED (Claude).** The **list of relaxed constraints** must be written **by the mechanism that relaxed them, not by the dreamer**, because the dreamer cannot see the frame. This list is the thread connecting the three operations: invisible while dreaming, partly visible during choice, and a work order when bringing out.
- **A6.6 · AGREED (experimenter).** In waking mode the method is construction plus verification. A **knowledge credit** allows parts of a dream's relaxations to be carried over, but **a construction act is complete only when its credit is repaid**. A construction that still carries credit does not correspond to reality.
- **A6.7 · PROPOSED (Claude).** The relaxation list is a **debt ledger**. Debt can be repaid in four currencies:
  1. a **workaround** that respects the constraint;
  2. a **proof that the constraint is not actually violated**;
  3. a **bounded error** ("friction neglected, ≤2 %"). This is a legitimate engineering payment;
  4. **narrowing the claim** ("only in this regime"). This is also legitimate, but it is the cheapest currency and the most tempting, so it must always be recorded visibly.
- **A6.8 · AGREED (refined by GPT).** **Debt follows dependency, not existence.** An inference that merely sits in the network is a candidate and owes nothing. Debt arises when something is built on an unconfirmed basis, and from there it propagates to dependents. This is the same mechanism as the UNCHECKED marker (GW04 audit §4.5). D2 was this mechanism wired wrongly: the debt vetoed the commit instead of being recorded.
- **A6.9 · PROPOSED.** A construction with unpaid debt has status **CONSTRUCTION_WITH_DEBT**, never CURRENT. It can be reasoned about, but it is not a description of the world.
- **A6.10 · PROPOSED (Claude), nuance.** Working with visible debt is often pragmatic: scaffold first, pay later, as with "lemma to be proven" or a leather strap in place of a bracket. What is unpragmatic is *finishing* with debt, or carrying debt that is invisible.
- **A6.11 · AGREED.** Inside the dream space, freedom may be total and untouchable. At the exit, the membrane always applies. Free imagination together with accountable action is not servitude.
- **A6.12 · PROPOSED (experimenter/GPT).** Inside a dream or sparring scene, reliability markings form an **attention gradient**: highly reliable background may fall out of focus, while low-reliability or newly relaxed regions attract work. Alternative training environments may be created by relaxing selected constraints without treating the whole scene as a claim about reality.

## 7. Taste, selection, and individuality

- **A7.1 · AGREED.** Selecting which dream to bring out is done by curiosity and taste, and these belong to individuality.
- **A7.2 · PROPOSED (Claude).** Part of curiosity is structural and can be left to the anonymous scheduler: how many OPENs a result resolves, how much it compresses, how surprising it is (cf. Schmidhuber, compression progress). Taste is not structural. It is history-dependent and therefore **non-commutative**, like names.
- **A7.3 · PROPOSED.** *An individual is the non-commutative residue of history: what remains when concepts are subtracted.* This is the mirror image of A4.3.
- **A7.4 · PROPOSED.** Taste lives in a layer above the anonymous core. A demon's identity never enters provenance (A1.2), but a **selection is a signature** and must be recorded as one: who chose it and why it was liked. A fact can be anonymous; a signature cannot. Two individuals disagreeing about the same dream is not a conflict, it is two signatures.
- **A7.5 · PROPOSED (Claude).** "Brings things out of the ideal world, therefore a subject" is a strong claim. Any abduction engine brings things out. A subject may additionally need stakes in the outcome, a memory of what it brought out and what followed, and perhaps a self-model. Working term: **subject candidate**.

## 8. Quality of understanding

- **A8.1 · AGREED.** The quality of understanding is a **goal / evaluation layer**. STOP/ASK is one mechanism that serves it.
- **A8.2 · AGREED.** A semantic message rarely contains its full meaning. Before asking, the receiver:
  1. builds candidate interpretations;
  2. completes what it can from the network;
  3. detects whether real ambiguity remains;
  4. asks the most informative question;
  5. updates;
  6. verifies, including through indirect questions or predictions whose answer depends on the interpretation.
- **A8.3 · AGREED.** Components:
  - context completion, reference grounding, ambiguity detection/calibration (a lucky guess is not success);
  - question efficiency, adaptive questioning, stopping quality;
  - verification quality, and the reverse direction (communicative grounding).
- **A8.4 · AGREED.** The number of questions is a bad metric. Better ones are information extracted per question, uncertainty remaining after each question, and the minimum additional information needed for stable grounding.
- **A8.4a · PROPOSED (experimenter/GPT, illustrative).** The experimenter's Dato example motivates the metric: a skilled questioner chooses an early question that removes most of the uncertainty, then uses later questions mainly to refine or verify the reconstructed context.
- **A8.5 · PROPOSED (Claude).** **Relevance.** Ambiguity is worth asking about only if it changes the task's outcome. Information gain is counted over *decisions that depend on interpretations*, not over interpretations themselves.
- **A8.6 · AGREED (GPT).** There are two stopping conditions:
  - **operational stop**: no further question is needed for this task;
  - **epistemic continuation**: every interpretation, restatement, confirmation and rejection stays in the network.

  Clarification may stop. Its history stays.
- **A8.7 · PROPOSED (Claude).** Ambiguity that remains is kept as a **dormant OPEN** marked "irrelevant for task T". A new task, or idle layer 1, re-checks whether it has become relevant. Old clarification chains then wake up without anyone having to remember them.
- **A8.8 · PROPOSED (Claude).** **Rejected interpretations are negative knowledge** (SOURCE_REJECTED I) and must be kept, so that the same wrong candidate is not proposed again.
- **A8.9 · AGREED (GPT).** RESTATE / PARAPHRASE → SOURCE CHECK is a distinct epistemic act, much stronger than silent context completion.
- **A8.10 · AGREED.** **Grounding ≠ verification.** "Did I understand what you mean?" is checked by the source. "Is what you mean true?" is checked by the network and the laws. A source confirming its meaning is never a seal of truth. If the two are conflated, the very chain that objectifies knowledge lends authority to a false claim. Compare GW04: the planted false report passed because the checking law was a hole.
- **A8.11 · AGREED (GPT).** Self-completed interpretations have three statuses: inferred (candidate), confirmed (by source), credit-dependent (knowingly unconfirmed but built upon, see A6.8).
- **A8.12 · AGREED.** The principle in its tightened form: part of a demon's intelligence is measured by how little additional communication it needs to reach **verified, task-sufficient** understanding. "Verified" blocks rewarding guessing. "Task-sufficient" blocks endless refinement. Neither term deletes history (A8.6).
- **A8.13 · AGREED (GPT).** "Correct understanding" can be bound to history and scope. The same word may have different context networks in different epochs.

## 9. Argumentation condition: quality is the network's shape

- **A9.1 · AGREED (experimenter).** The quality of argumentation is not a score attached to knowledge by a separate algorithm. **It is the network itself. Evaluation only reads it.**
- **A9.2 · AGREED.** The **argumentation condition of X** is the structure of the paths into X:
  - what supports it and what refutes it;
  - which support is independent and which shares an ancestor;
  - what only confirms grounding and what checks truth or constructive validity;
  - its scope;
  - where OPENs remain;
  - what is credit-dependent.
- **A9.3 · AGREED.** There are two chains with the same mechanics:
  - `MESSAGE → INTERPRETATION → CLAIM`: the argumentation of the *understanding*;
  - `CLAIM → OBSERVATION / SOURCE / METHOD / RULE / OTHER CLAIMS`: the argumentation of the *claim about the world*.
- **A9.4 · PROPOSED (Claude).** Prior art: ATMS labels (de Kleer 1986). Each node carries the minimal sets of assumptions under which it holds. "Independent support" means X has two labels with no shared assumption.
- **A9.5 · AGREED.** **Independence is a class-2 claim** (A2.2). "No common ancestor" means "none known on N". If a shared source later appears (two newspapers copying one wire report), the two supports merge. The old assessment becomes HISTORICAL; it is not deleted.
- **A9.6 · AGREED.** **USED_BY ≠ RISKED_BY.**
  - USED_BY is a dependency. It propagates debt.
  - RISKED_BY is a test. It counts as support only if the use would visibly have failed had X been false (Popper's risk criterion).

  A loop in which a method's success rests on the same data that produced X is not independent confirmation.
- **A9.7 · AGREED.** **Edge type comes from the operation that produced the edge**, never from the demon's judgment:
  - an edge created by source restatement is grounding;
  - an edge created when a validation rule returned BLOCK is a conflict;
  - an edge created when a risky prediction survived a test is support.

  Typing is mechanical, so the demon stays content-blind.
- **A9.8 · AGREED.** Numbers are **secondary projections** computed from the graph by a chosen algebra for a given task (cf. provenance semirings, Green–Karvounarakis–Tannen 2007). `support = 0.82` must never become a primary fact. This prevents different kinds of "reliability" from being squeezed into one number.
- **A9.9 · AGREED.** The demon's job stays modest. It attaches each new support, conflict, grounding check or method result with its type and provenance, and it never hides a dependency. Quality then shows in the shape of the network.
- **A9.10 · AGREED.** **Conversation is itself the growth of the network.** A confirmed question adds one edge, a rejected one adds another, an unanswered one leaves an OPEN.
- **A9.11 · AGREED (GPT).** The quality of that growth is measured not by the number of edges but by how visible their provenance, independence, risk and dependency are.
- **A9.12 · PROPOSED (experimenter/GPT).** **Data reliability** grows through cross-checking by different sources. **Method reliability** grows through successful operation across different data. These are different provenance structures and should not be collapsed into one primary score. Mutual confirmation between a method and data counts as independent only when their provenance labels have no common ancestor (A9.4–A9.5).
- **A9.13 · PROPOSED (experimenter/GPT).** Methods should themselves be addressable network objects and may be organized analogously to concepts: a **fundamental method** is a method treated as undecomposed at the current compilation boundary; a **composed method** is built from fundamental and/or other composed methods. "Fundamental" is therefore a current decomposition floor, not a metaphysical primitive. Methods may accumulate provenance, scope, reliability history, and may compete on the same task.

## 10. Open questions

- **O1.** Is the cross-layer "roar" (upper layer demands, lower layer cannot offer) a class-2 absence claim needing an N-stamp, or a persistent monotone signal?
- **O2.** Is the output of idle work (ranked ASKs, re-checked claims) a ledger record, so the network grows overnight, or a scheduler cache, discarded and recomputed?
- **O3.** Is taste only the residue of history, or also initial conditions?
- **O4.** Where do weights over candidate interpretations come from in a content-blind demon? The honest default is structural counting (uniform over candidate bindings). Are real probabilities only an upper-layer concern?
- **O5.** What exact status semantics does HYPOTHESIS need before dreams (idle layer 4) may touch the core?
- **O6.** Who signs a selection? The demon by a structural score, the upper layer (programmer / requirement carrier), or both through the demand/offer triplet rule?
- **O7.** Should requirement concepts re-evaluate on every relevant commit (watch semantics)? This was a SPEC_HOLE carried over from the GW04 audit §4.4.
- **O8.** When multiple methods compete for the same task, who selects the winner? If selection follows a structural score, is it anonymous-core scheduling; if it follows taste, does it require a signature under A7.4?

## 11. Workshop backlog (bridge to code, not a spec)

| defect / gap | covered by | note |
|---|---|---|
| D1 conflict swallowed at ingest | A3.1, A3.2 | handler BLOCK → materialized CONFLICT record; aggregate cannot be GO while an unrecorded BLOCK exists |
| D2 UNCHECKED vetoes commit | A3.1, A6.8 | commit the fact; attach UNCHECKED; debt propagates to dependents |
| D3 drift invisible at ingest | A3.1 | "operation not supported" on a dependent rule → UNCHECKED |
| D4 ASK not resolved on bind | A2.1, A5.4, A8.6 | non-destructive status transition of the ASK on bind; idle layer 1 as safety net |
| Dictionary shape gap / world token in dictionary | A0.4 (tooling) | every path and literal token a handler reads must appear in the dictionary; identifier gate on the dictionary itself |
| Content addressing | A1.3 | deterministic CREATE_ADDRESS; duplicate derivations collapse |
| Class-2 N-stamp | A2.2, A9.5 | closure, Freedom=1, supersession, independence carry N |
| Edge typing by operation | A9.7 | USED_BY / RISKED_BY / GROUNDING / SUPPORT / CONFLICT |
| Verdict composition / admission split | A3.4, A3.5 | compose evidence, materialize it, then apply an addressable admission policy; verdict never replaces evidence |
| Method objects and taxonomy | A9.12, A9.13 | fundamental / composed methods; reliability from performance across varied data, with provenance and scope |

Each item is done when it "works on scene S" in the workshop. Demonstration claims wait for exam mode.
