# ADR-0005 — Initialize Birch–Swinnerton-Dyer as a governed source-and-equivalence campaign

**Date:** 2026-07-24  
**Status:** Accepted and WP00 promoted  
**Owner:** The Amanuensis with the Axiomatist, Cartographer, Steward, Archivist, and Referee

## Context

The Birch–Swinnerton-Dyer name is used for a rank equality, finiteness of the Tate–Shafarevich group, a strong leading-term formula, parity statements, `p`-adic conjectures, restricted converse theorems, family theorems, and finite computations. These statements are related but not interchangeable. Normalization drift in Euler factors, periods, exceptional-zero corrections, or Selmer local conditions can turn a correct restricted theorem into an incorrect global claim.

## Decision

Initialize campaign `BSD-001` and Work Package `BSD-WP00` under these controls:

1. `BSD-RANK-Q`, `BSD-SHA-Q`, and `BSD-LEAD-Q` are separate universal obligations.
2. Use a complete finite Hasse–Weil `L`-function and record an explicit concordance with Wiles's initially incomplete official notation.
3. Identify a `p^infinity`-Selmer corank with Mordell–Weil rank only after controlling the `Sha[p^infinity]` contribution.
4. Root numbers and parity theorems determine parity only, not exact rank.
5. Every converse or `p`-part theorem retains curve class, prime, reduction, residual-representation, direction, and normalization hypotheses.
6. Split `p`-adic BSD into ordinary, multiplicative exceptional-zero, supersingular signed, and multivariable profiles.
7. Never silently promote individual-curve, finite-database, family, proportion, or density statements to the universal quantifier.
8. Begin formalization with statement separation, corank algebra, finite Euler-factor conversions, parity logic, and ledger validation.
9. Admit no mechanism, novelty, or progress claim at WP00.

## Alternatives rejected

- Treating rank equality as the entire refined conjecture.
- Using Selmer rank as a synonym for Mordell–Weil rank.
- Using a root-number sign as an exact-rank predictor.
- Pooling all `p`-adic results under one theorem node.
- Beginning with large curve databases or twist searches before the semantic audit.

## Consequences

- `BSD-WP00` is promoted after Programme policy checks, independent Referee reconstruction, and Amanuensis integration.
- `BSD-WP01` and `BSD-WP02` may proceed in parallel.
- Restricted-target and mechanism selection remain behind later Council gates.
- Exact low-rank theorem concordance, the expanded `p`-converse/`p`-part taxonomy, recent twist-family provenance, and formal-library reconnaissance remain nonblocking debt.

## Affected artifacts

- `DOMAIN_03_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`
- `campaigns/birch_swinnerton_dyer/WP00_FOUNDATION_STATUS/`
- `reviews/birch_swinnerton_dyer/BSD-WP00.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`
- `MATH-PROGRAMME#66`

## Review provenance

- Canonical tracker: `https://github.com/grandchallenge/MATH-PROGRAMME/issues/66`.
- Pull request: `https://github.com/grandchallenge/MATH-PROGRAMME/pull/67`.
- Review record: `reviews/birch_swinnerton_dyer/BSD-WP00.agent_review.yaml`.
- Programme policy workflow: `30084664646`.

## Supersedes

No prior Birch–Swinnerton-Dyer campaign decision.