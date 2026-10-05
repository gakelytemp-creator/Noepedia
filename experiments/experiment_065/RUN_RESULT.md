# Experiment 065 — RUN RESULT

Status: PASS

Focused verification run: 37254245461

Branch A accuracy: 50%
Branch B accuracy: 100%
Winner: META_POLICY_V1_B
Accuracy margin: 0.50
Status: BRANCH_WINNER_CANDIDATE

Both branches were replayed on the same frozen 8-case set and had graph_valid_rate = 1.0.

Close-control comparison used a 0.05 margin and correctly returned REMAIN_OPEN because the preregistered 0.10 margin gate was not met.

Parent policy remained preserved. Both branches retained BRANCHED_FROM_META_POLICY links. active_policy_mutated = false.

Architectural conclusion: historical meta-policy versions can now branch into alternative candidate policies, be compared on identical frozen evidence, and produce a winner candidate without automatically changing the active policy.
