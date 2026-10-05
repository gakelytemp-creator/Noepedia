# Current Architecture — Canonical Boundary

> Status: CURRENT / CANONICAL
> Date: 2026-10-05
>
> When older conceptual documents conflict with this file, this file and DIRECTION.md govern the current architecture. Historical experiment records remain unchanged.

## 1. Minimal architecture

~~~text
SEMANTIC WORLD
        ↕
LLM ADAPTER
        ↕
SOCRATIC DAIMONION
        ↕
NOEPEDIA FIELD

repeated stable Daimonion operations
        ↓
DETERMINISTIC ALGORITHMS
~~~

### Noepedia Field

The field is the persistent semiotic substrate. It stores addressable objects, triplet relation tables, predicates, network handles, provenance/source tokens, status, scope, time/context, versions, OPEN, and other explicit structures.

Its responsibility is database-like: store well, return well, address cheaply, traverse cheaply, preserve history where required.

The field is structure. It does not reason by itself.

### LLM Adapter

The LLM works at the language boundary. It translates semantic human material into candidate semiotic structure and translates structured retrieval results back into human language.

The LLM is not the Daimonion and its fluency is not persistent epistemic authority.

### Socratic Daimonion

The Daimonion is a learned semiotic operator over the field. It does not need to speak.

It learns decomposition, placement, identity handling, provenance/source-token handling, OPEN preservation, retrieval, query construction, task-specific mega-graph assembly, reconstruction, stopping, and view/attention selection.

### Deterministic algorithms

When a Daimonion operation repeats reliably enough that its conditions and outputs can be made explicit, it should be extracted and tested as a cheaper deterministic procedure.

Algorithms are crystallized Daimonion habits.

The revision subsystem is one such organ. It is not the whole Noepedia core.

## 2. Ingestion and retrieval

~~~text
INGESTION
semantic material
→ LLM candidate decomposition
→ Daimonion placement/testing
→ field storage + provenance + status + OPEN

RETRIEVAL
human question
→ LLM structural intent
→ Daimonion query / mega-graph
→ field result
→ Daimonion sufficiency check
→ LLM verbalization
~~~

## 3. Mega-graph

The mega-graph is not a permanent super-graph. It is a temporary task-specific assembly of only the field cuts required now: the pocketed garment.

Preferred control loop:

~~~text
ATTEND
→ retrieve minimal cut
→ reconstruct
→ sufficient? use/return
→ insufficient? preserve OPEN or missing view
→ widen locally
→ reconstruct again
~~~

Expensive intelligence should be concentrated at unresolved edges rather than used to render the whole field.

## 4. Evidence tokens and objectivization

A claim is not only a sentence. It can accumulate source/evidence tokens whose own relations record origin, independence, copying, measurement, conflict, time, and context.

Repeated wording is not automatically repeated evidence.

A high-confidence claim remains revisable. A strong mismatch can downgrade it rapidly, reopen scope, or reveal a missing context rather than simply deleting the claim.

Current condition and next justified action are more useful than a permanent rank.

## 5. Daimonion training

The first Daimonion should be trained on a synthetic polygon where hidden ground truth is known.

Training cases should include:

- one object under many names;
- one name for several objects;
- missing predicates and missing objects;
- duplicated evidence copied from one origin;
- genuinely independent evidence;
- contradictory sources;
- time/context dependent relations;
- incomplete hierarchies;
- retrieval requiring several networks;
- narrow single-path solutions;
- many-path solutions;
- underdetermined cases;
- inconsistent formulations;
- cases where OPEN is correct;
- cases where no solution exists in the current formulation.

The fitness target is not eloquence. It is correct semiotic operation.

## 6. Reconstruction as fitness

New knowledge often begins in a fragile or partially wrong state. Repeated decomposition, reconstruction, comparison, failure localization, alternate-view retrieval, and reconstruction again can move it toward functional assimilation.

A useful knowledge structure should increasingly support regeneration after partial loss, transfer into new contexts, and recognition of when no justified completion exists.

## 7. Status of the revision line

Experiments 042 onward produced a substantial, auditable revision subsystem. This work remains valid as one deterministic organ.

Experiments in blind automatic pair mining later showed why that organ must not be mistaken for the whole Daimonion or for a universal discovery engine.

The next central research direction is controlled learning of semiotic storage/retrieval behavior and neural-to-algorithmic compilation, not unrestricted correlation mining.

## 8. Supersession rule

Older conceptual documents remain valuable as research history, but passages that imply any of the following are superseded:

1. the revision subsystem is the whole Noepedia core;
2. the Daimonion is primarily a conversational LLM;
3. the persistent field itself should absorb flexible reasoning behavior;
4. a permanent mega-graph should contain all active knowledge;
5. fluent semantic completion is equivalent to semiotic grounding;
6. every request must end in an answer rather than OPEN / stop / underdetermined status.

Canonical current references:

- CURRENT_ARCHITECTURE.md
- SOCRATIC_DAIMONION.md
- DIRECTION.md
- core/revision/README.md for the bounded revision organ

Historical experiments remain historical and should not be rewritten to imitate the current view.
