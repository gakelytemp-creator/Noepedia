# Experiment 044 — Promotion Gates

Primary document:
`PROMOTION_GATES.md`

Status:
`PROMOTION_GATES_SPECIFICATION_COMPLETE`

Decision outputs:
- PROMOTE
- REJECT
- REMAIN_OPEN

Promotion requires:
`COMPLETE_PATH + FROZEN_TEST + UNTOUCHED_CONFIRMATION + REQUIRED_NULLS_PASS + HISTORY_PRESERVED + OPEN_REFINED`

Key distinction:
- REJECT = candidate was fairly tested and failed a scientific gate
- REMAIN_OPEN = no justified decision is available yet

Next step:
`Experiment 045 — Automated Revision Harness`