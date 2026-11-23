# Cross-repository handoff — Noepedia ↔ 3DGabro (2026-11-23)

**Owner's architectural intention:** Noepedia is the **central** knowledge / semiotic-navigation project. 3DGabro is the **geometry/CAD application and experimental polygon**, not a sibling competing as the primary ontology. Other repositories provide specialized instruments, datasets or application domains as appropriate. The organizational relationship is an architectural goal; networked runtime integration is **not yet implemented**.

## For Claude/GPT/new researcher: reading order

1. [Noepedia current architectural entry](../current/README.md) and [architecture](../current/ARCHITECTURE.md).
2. [2026-11-23 conceptual snapshot](../current/CONCEPTUAL_SNAPSHOT_2026-11-23_ANKETA_NAVIGATION.md) — exact current thesis and limitations.
3. [Detailed conversation atlas](ANKETA_DIALOGUE_ATLAS_2026-11-23.md) — arguments, corrections, examples, how we arrived here.
4. [3DGabro repository](https://github.com/gakelytemp-creator/3DGabro) and its experimental [GSE-001 issues #2](https://github.com/gakelytemp-creator/3DGabro/issues/2), [#3](https://github.com/gakelytemp-creator/3DGabro/issues/3), [Phase-0 PR #4](https://github.com/gakelytemp-creator/3DGabro/pull/4), [concept PR #5](https://github.com/gakelytemp-creator/3DGabro/pull/5).
5. [3DGabro bridge document](https://github.com/gakelytemp-creator/3DGabro/blob/research/noepedia-link-2026-11-23/research/NOEPEDIA_GEOMETRY_BRIDGE.md) — geometric specialization and present implementation state.

**Important provenance note:** PR #4 and #5 are **drafts** and not presumed merged into 3DGabro/main. Noepedia's `current/` documentation remains authoritative for Noepedia; new material is a **dated research snapshot/working hypothesis**, not a retroactive alteration of historical Noepedia tests. Avoid creating a new ontology layer or relabeling prior GW/DCT results as questionnaire confirmation.

## Proposed domain-neutral interface (concept only)

| Noepedia role | Domain polygon supplies |
|---|---|
| Stable object / relation / operation addresses | Domain objects such as point sets, features, CAD programs |
| Provenance, scope, unknowns, history | Measurements, seeds, tolerances, mesh/scan refs and transformation runs |
| Query/cut/partition, tentative candidate promotion | Geometry-specific comparisons and new-feature candidates |
| Reusable relation tests across domains | A geometric oracle that actually evaluates CAD/continuous geometry |
| Constructive task / returned result and failure | Reconstructive or generative geometric experiment and independently evaluated result |

**Not implied:** a central runner already serving all repos, cross-repo shared storage API, automatic model-to-model updates, or an autonomous agent already trained.

## Stable change management

- Do not rewrite historical experimental outcomes. Add date-stamped snapshots with provenance.
- Keep hypotheses distinct from measured facts and past claims.
- Distinguish exact relations from tolerance-qualified approximate relations; record contradictory cases rather than erasing them.
- Keep edits to Noepedia's `current/` as **proposed**, through PR review.
- Use GitHub PR/issue comments as durable communication for assistants with read-only access; GitHub itself is not a live agent bus.
- When implementing a new Noepedia core interface, make a separate approved decision after reviewing `current/ARCHITECTURE.md` and `current/EPISTEMIC_RULES.md`.

## Decisions still genuinely open

1. Is the first-cell event `(A, action, B)` the actual minimal core, or an expression inside Noepedia's addressable SPO field?
2. Does "drawer" mean reversible partition, canonical normalization, lossy projection or combinations? They need separate contracts.
3. Can the learner invent executable new cuts from comparisons and counting without privileged predicates, and how is transfer certified?
4. What independence/uncertainty/evidence boundary permits cheap propagation vs expensive geometric measurement?
5. How to measure newly discovered domain-independent operator structure rather than merely good in-domain labels?
6. Does questionnaire representation improve learning relative to strong neural, retrieval, fixed-questionnaire and nonlearned organizer controls? Phase gates are in GSE-001 #2/#3.

**Requested reviewer focus:** Challenge the cross-repository role and the proposed *minimal* interface; identify contradictions with Noepedia's `current/` layer before suggesting code. Small tests before expanding F/C/M governance lists.
