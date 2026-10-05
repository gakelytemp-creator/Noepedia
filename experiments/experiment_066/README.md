# Experiment 066 — Branch Merge / Evidence Merge

Purpose:
validate conservative merging of non-conflicting meta-policy branches.

Pass criteria:
- non-conflicting field changes merge into one candidate definition;
- merged candidate replays on the same frozen evidence;
- merge is accepted only if no worse than the best parent branch;
- conflicting field edits block merge creation;
- parent and branch history remain preserved;
- active policy is not mutated automatically.
