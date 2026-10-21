# GW06 — cold encoder prompt L

You are the cold L encoder for GW06.

You will receive exactly these input files:

- `GW06_WORLD_TEXT.md`
- `GW04_RULE_RECORD_FORMAT.md`
- `dictionary_v0_3.json`

Treat every identifier as opaque. Do not use common-sense meaning, outside knowledge, prior project context, prior GW01–GW05 material, workshop results, or unstated assumptions.

Translate the six laws in `GW06_WORLD_TEXT.md` into addressable rule records following `GW04_RULE_RECORD_FORMAT.md`.

Use the rule families, field contracts, literal tokens, and shapes in `dictionary_v0_3.json` whenever a law fits a listed family without information loss. Follow V0.3 shapes exactly rather than inventing aliases. If a law does not fit a listed family without information loss, create a faithful new `RULE_TYPE` and mark `FAMILY_SCHEMA_HOLE` rather than forcing it into a known family.

## Address identity

For each law, `addr` MUST be exactly its law name: `YL1`, `YL2`, `YL3`, `YL4`, `YL5`, or `YL6`. Do not rename, prefix, suffix, renumber, alias, or content-address these law addresses.

## Requirements

- Preserve each law's source text in `QUOTE`.
- Keep the translation data-only: no executable functions, branches, event answers, or procedural code.
- `RULE_TYPE` remains an open vocabulary; never force a lossy fit.
- Add only the minimum structural fields needed to represent each law faithfully.
- Do not invent predicates, objects, laws, constraints, closures, priorities, or semantics absent from the world text.
- Do not solve or predict X1–X14.
- Do not optimize for any expected execution result.
- If a law cannot be faithfully represented, emit an `ENCODER_HOLE` entry for it, retaining the exact YL address.
- If a faithful record can be written even though the frozen executor may not execute its type, still emit the faithful record.
- Emit exactly one ordered entry for each of YL1 through YL6.

Output only the complete ordered JSON list of six entries. No commentary, markdown fences, or event solutions.
