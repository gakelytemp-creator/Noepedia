# GW06 — preregistration amendment A1

**Status:** PRE-TRANSLATION AMENDMENT. This amendment was made before any GW06 cold N or L translation existed. No translation output, execution result, or answer-book plaintext was available when the changes below were made. Therefore this is a pre-translation repair, not a post-hoc adaptation.

## Reason

The first frozen harness at commit `c33ac0f` / prereg commit `fc5f5b0` was not executable: the final output writer contained an upload-escaping syntax defect in which the intended `"\n"` string had become a literal line break inside the Python string. The previously recorded harness SHA-256 `6197781b649a0719eb709896b2a9872486d2e83b81cb599e6f7064016cbaf7b1` is therefore **superseded and invalid for GW06 execution**.

A second pre-translation defect was also repaired: direct task lookups for required law addresses now fail closed with `NEED / RULE_ABSENT` instead of raising when a cold translation omits or renames the expected `YL2` or `YL3` address. This guard does not infer an answer and does not repair the translation.

## New frozen harness

- Repair commit: `dfed810610aa646d3df5908102c128aa8ba4ec26`.
- `core/demon/run_c/gw06_runner.py` SHA-256: `61681cee2161c6b4f508d94528da0028a27070dbb3c8629be329d174b4c28194`.
- Original executor/workshop baseline remains `83ca690adf4e55f42edf085a23b27321fa8d1557`.
- V0.3 remains unchanged at SHA-256 `8f0e64c4450f698341fa0bdf6ca815c64f9c17bfea8452604cd414f4019f33e6`.

## Frozen cold-encoder prompts

The prompts were added before cold translation and explicitly require law-address identity `addr == YL1...YL6`.

- `current/experiments/GW06_ENCODER_PROMPT_N.md` SHA-256: `34e8d8274be5a4ab0e9935bb459da33eb315b2cac70c5f8934f30201ce36d88d`.
- `current/experiments/GW06_ENCODER_PROMPT_L.md` SHA-256: `3b389e69088d5099ae0bc1740c972528bb9522e7ff6ba155c058af0d5ac20b2e`.
- N receives the world text plus the frozen rule-record format.
- L receives the same inputs plus `dictionary_v0_3.json`, and is instructed to use V0.3 family shapes when they fit without information loss.

## Preflight gate

A reproducible repository-native preflight is frozen at `.github/workflows/gw06-preflight.yml`.

GitHub Actions run `39620717731` on commit `808ebfd949dc28b29e91d3d63ed17f23000c4117` completed with conclusion **success**. The gate performed:

1. `python -m py_compile core/demon/run_c/gw06_runner.py`;
2. six address-correct unknown-family laws, baseline mode, all 14 events completed;
3. the same six unknown-family laws, workshop mode, all 14 events completed;
4. a fixture with `YL2` and `YL3` absent/misaddressed, baseline mode, all 14 events completed and X1–X3 reported `NEED / RULE_ABSENT`;
5. the same absent-rule fixture, workshop mode, with the same non-crashing guard behavior.

The smoke tests assert completion and guard behavior only. They do not inspect semantic GW06 outcomes and therefore do not expose or tune against the sealed answer book.

## Freeze effect

For all subsequent GW06 protocol steps, the A1 harness hash and prompt hashes above supersede the original harness hash in `GW06_PREREG.md`. World-text, answer-book, ciphertext, V0.3, success criteria, run matrix, structural-neutrality caveats, and answer-book seals are otherwise unchanged.

Cold translation must not begin from the superseded harness. It may begin only from the repository state containing this amendment.
