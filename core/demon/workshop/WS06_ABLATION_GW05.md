# WS06 — functional anatomy by ablation, scene GW05

**Status: WORKSHOP EXPERIMENT. Scope = GW05's task class only (ATTIC 01 A12.13). A zero contribution here means "zero on this scene", not "zero in general".**

`ablation_gw05.py` runs `gw05_scene.execute()` over every combination of the workshop switches and writes `ablation_gw05.json`, 48 runs in total:

- encoder N / L;
- `c13` (C1 joint support + C3 status registry);
- `admission` (WS01–WS02);
- `resolve_asks` (WS03);
- `debt_shape` fact / rule (WS04; only meaningful with admission on);
- dictionary V0.2 / V0.3 (WS05).

Metrics, all read from the final network:
- facts committed (of 7);
- F11 binding;
- registry size;
- open signal records in the network;
- conflicts and debt visible in the registry;
- unanswered ASKs;
- NEED stops;
- the F1–F12 verdict string.

## Summary table (dictionary V0.2; V0.3 is identical, see finding 1)

| enc | c13 | adm | res | debt | facts | bound | registry | signals in net | conflict in reg | debt in reg | ASK open | NEED |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N | 0 | 0 | · | · | 0/7 | — | 0 | 0 | 0 | 0 | 0 | 12 |
| N | 0 | 1 | · | fact | 7/7 | — | 0 | 35 | 0 | 0 | 0 | 5 |
| N | 1 | 0 | · | · | 0/7 | — | 2 | 0 | 0 | 0 | 1 | 10 |
| N | 1 | 1 | 0 | fact | 7/7 | I8 | 36 | 35 | 0 | 35 | 1 | 3 |
| N | 1 | 1 | 1 | rule | 7/7 | I8 | 5 | 5 | 0 | 5 | 0 | 3 |
| L | 0 | · | · | · | 7/7 | — | 1 | 0–4 | 0 | 0 | 0 | 5 |
| L | 1 | 0 | 0 | · | 7/7 | I8 | 2 | 0 | 0 | 0 | 1 | 3 |
| L | 1 | 0 | 1 | · | 7/7 | I8 | 1 | 0 | 0 | 0 | 0 | 3 |
| L | 1 | 1 | 1 | rule | 7/7 | I8 | 4 | 3 | 1 | 2 | 0 | 3 |

`·` means the switch has no effect in that row group. The full rows are in the JSON.

## Findings

1. **Dictionary V0.2 → V0.3: zero effect on all metrics in all 24 pairs.** This is expected, and it is the honest result of WS05: the old translations were compiled against the old contract.
2. **N: admission × c13 is a dependency pair (epistasis).**
   - Admission alone unfreezes the world (0/7 → 7/7) but binds nothing, because C1 is off.
   - c13 alone produces the joint ASK but cannot bind, because I8 never enters.
   - **Only both together bind RQ_F6 → I8.**
3. **resolve_asks is a pure downstream dependency.** It changes something only where a bind exists:
   - in N, only with c13 × admission (a three-way dependency);
   - in L, with c13 alone, because L's facts already enter without admission.
   - Elsewhere its contribution is zero *on this scene*.
4. **Masking: admission's signals are invisible without C3.** With c13 off, admission writes 35 (N) or 3–4 (L) open signal records into the network, yet the registry shows none of them. The base registry counts only `TYPE=OPEN`, which is the old GW04 type-vs-status defect. The signals exist; the reader cannot see them. In ATTIC terms: the record is correct, but the *view* masks it.
5. **debt_shape changes readability, not semantics.**
   - N: registry 36 → 6, or 35 → 5 with resolve_asks.
   - L: 6 → 5, or 5 → 4.
   - Facts, bindings, ASKs and verdicts are unchanged.
6. **In L, c13 alone decides binding.** Admission adds visibility only: the F4 conflict and the M2/M3 debts.

## What this anatomy does not say

- Nothing about whether these methods matter on other task classes.
- Nothing about whether a fresh translator would trigger them (exam mode).
- Verdict strings stay the same across rows where only visibility differs. Visibility versus decision is exactly the A3.4 split, and the matrix shows it holds on this scene.
