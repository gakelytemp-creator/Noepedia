# Experiment 065 — Policy Branching and Counterfactual Replay

Purpose: validate branching from one historical meta-policy into multiple candidate branches and compare them on the same frozen replay set without mutating the active policy.

Pass criteria:
- two branches derive from the same parent;
- both run on the same frozen cases;
- better branch wins by preregistered margin;
- parent policy remains preserved;
- winner remains a candidate, not automatically active;
- close/noisy branches remain open when margin is too small.
