# GW06 — preregistration amendment A2

**Status:** PRE-TRANSLATION HASH CORRECTION. This amendment is made before any GW06 cold L translation begins. No cold L translation output, harness execution log, or answer-book plaintext has been inspected.

## Correction

`GW06_PREREG_AMENDMENT_A1.md` recorded the wrong SHA-256 for the frozen L encoder prompt.

A1 recorded:

`3b389e69088d5099ae0bc1740c972528bb9522e7ff6ba155c058af0d5ac20b2e`

That value does **not** correspond to the file committed at `d857bc4251e188729f55f05e95dc46eb37684273`.

The repository file:

`current/experiments/GW06_ENCODER_PROMPT_L.md`

has SHA-256:

`9a4a5239746fe07deb1457c670a3e6e3a3710ca72341519eb6038c81fb648a79`

and Git blob SHA:

`10fe9c3d211fcf920b3ad44833302d7dd5d1d046`.

The prompt content itself is unchanged and remains the intended frozen L prompt. It requires:

- inputs `GW06_WORLD_TEXT.md`, `GW04_RULE_RECORD_FORMAT.md`, and `dictionary_v0_3.json`;
- exact law-address identity `addr == YL1...YL6`;
- V0.3 family/field/literal shapes when they fit without information loss;
- a faithful new `RULE_TYPE` plus `FAMILY_SCHEMA_HOLE` when no listed family fits without information loss;
- no solving or prediction of X1–X14 and no optimization for expected execution results.

## Freeze effect

For the GW06 cold L translation protocol, the only valid frozen L prompt hash is:

`9a4a5239746fe07deb1457c670a3e6e3a3710ca72341519eb6038c81fb648a79`

The A1 value `3b389e69088d5099ae0bc1740c972528bb9522e7ff6ba155c058af0d5ac20b2e` is superseded as a preregistration transcription error.

No prompt bytes, world text, harness, V0.3 dictionary, answer-book seal, success criterion, run matrix, or structural-neutrality caveat are changed by A2.
