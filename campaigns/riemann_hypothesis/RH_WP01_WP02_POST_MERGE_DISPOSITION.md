# RH-WP01 / RH-WP02 — Post-merge disposition

**Campaign:** `RH-001`  
**Decision date:** 2026-07-26  
**Repository state:** implemented, merged through PR #90, and programme-policy CI passed  
**Formal promotion state:** `NOT_PROMOTED / RETAINED_REVIEW_BLOCKERS`  
**Mathematical status:** `OPEN CONJECTURE`

## Repository evidence

- Pull request: `grandchallenge/MATH-PROGRAMME#90`
- Merge commit: `895ce47cbf47fc6715e365d7c31a010fcda425cc`
- Programme policy workflow: `30156255759`
- Workflow conclusion: `success`
- Integrated package: `RH-WP01-WP02-post-WP00-integration.md`

## Disposition

`RH-WP01` and `RH-WP02` are present on `main`, their deterministic replay and cross-ledger validation passed, and their repository integration gate is discharged.

They are **not formally promoted**. The governing legacy review records remain:

- `reviews/riemann_hypothesis/RH-WP01.agent_review.yaml`
- `reviews/riemann_hypothesis/RH-WP02.agent_review.yaml`

Both records retain `promotion_recommended: false` and a blocking Referee finding. The remaining controlled obligations are:

1. independent source-locator and source-concordance review for moving theorem-frontier entries;
2. explicit migration to the schema-bound Agent Council review contract, or a superseding reviewed disposition that preserves the same claim boundary;
3. a separate promotion decision after those obligations are discharged.

## Current supported description

- `RH-WP01` is an implemented, merged, CI-passed eliminative false-proof atlas.
- `RH-WP02` is an implemented, merged, CI-passed source-normalized theorem, criterion, computation, evidence, and barrier ledger.
- Neither artifact proves or disproves RH, establishes a new theorem, certifies a new zero range, constructs a Hilbert–Pólya operator, selects a proof mechanism, or supports a novelty claim.

## Interpretation rule

Repository merge and successful CI establish integration and replay facts. They do not silently convert a blocking review record into promotion. Public pages must state both facts: the artifacts exist and passed CI; formal promotion remains withheld.