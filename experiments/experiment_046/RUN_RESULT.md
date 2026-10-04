# Experiment 046 — RUN RESULT

Status: PASS

GitHub Actions run: 37233041620

Positive case: PROMOTE
- one new rule record created
- parent rule preserved
- OPEN preserved
- OPEN refinement created

Negative case: REJECT
- no new rule record created
- rejected candidate record created
- parent rule preserved
- OPEN preserved
- OPEN refinement created

Architectural result: PASS

All append-only history invariants passed. The test confirms that decision records can be materialized into versioned graph records without overwriting prior rule history.

Remaining limitation: candidate generation and domain-specific null selection are still external to the generic harness.
