# ADR-0005 — Initialize Birch–Swinnerton-Dyer as a governed source-and-equivalence campaign

**Date:** 2026-07-24  
**Status:** Accepted; `BSD-WP00` promoted  
**Owner:** The Amanuensis with the Axiomatist, Cartographer, Steward, Archivist, and Referee

## Context

The Birch–Swinnerton-Dyer name is used for a rank equality, finiteness of the Tate–Shafarevich group, a strong leading-term formula, parity statements, `p`-adic conjectures, restricted converse theorems, family theorems, and finite computations. These statements are related but not interchangeable. Normalization drift in Euler factors, periods, exceptional-zero corrections, or Selmer local conditions can also turn a correct restricted theorem into an incorrect global claim.

## Decision

Initialize campaign `BSD-001` and Work Package `BSD-WP00`, subject to the following controls:

1. `BSD-RANK-Q`, `BSD-SHA-Q`, and `BSD-LEAD-Q` are separate universal obligations.
2. The campaign uses a complete finite Hasse–Weil `L`-function and records an explicit concordance with Wiles's initially incomplete official notation.
3. A `p^infinity`-Selmer corank is identified with Mordell–Weil rank only after the `Sha[p^infinity]` contribution is controlled.
4. Root numbers and parity theorems determine parity only, not exact rank.
5. Every converse or `p`-part theorem retains curve class, prime, reduction, residual-representation, direction, and normalization hypotheses.
6. The phrase `p`-adic BSD is split into ordinary, multiplicative exceptional-zero, supersingular signed, and multivariable profiles.
7. Individual-curve, finite-database, family, proportion, and universal quantifiers are never silently promoted.
8. Formalization begins with statement separation, corank algebra, finite Euler-factor conversions, parity logic, and ledger validation.
9. No mechanism, novelty, or progress claim is admitted at WP00.

## Alternatives considered

1. Treat the rank equality as the whole refined conjecture. Rejected because it omits finiteness and the leading coefficient.
2. Use `Selmer rank` as a synonym for Mordell–Weil rank. Rejected because the exact Kummer sequence contains a possible divisible `Sha` contribution.
3. Use a root-number sign as an exact-rank predictor. Rejected because the functional equation controls only parity.
4. Pool all `p`-adic results under one theorem node. Rejected because exceptional zeros, signed Selmer groups, variables, and interpolation factors materially change the statement.
5. Begin with large curve databases or twist searches. Rejected because bounded or family evidence cannot discharge the universal quantifier and would precede the semantic audit.

## Consequences

- `BSD-WP00` is promoted as a governed artifact after policy and independent Referee review.
- The complete normalization registry, statement lattice, implication ledger, dependency DAG, proof-debt register, claim ledger, and MATHCERT handoff are authoritative WP00 outputs.
- `BSD-WP01` and `BSD-WP02` may proceed in parallel.
- Restricted-target and mechanism selection remain behind later Council gates.
- Exact theorem concordance, the full `p`-adic taxonomy, and formalization reconnaissance remain nonblocking proof debt.

## Affected artifacts

- `DOMAIN_03_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`
- `campaigns/birch_swinnerton_dyer/WP00_FOUNDATION_STATUS/`
- `reviews/birch_swinnerton_dyer/BSD-WP00.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`
- `MATH-PROGRAMME#66`
- `MATH-PROGRAMME#67`

## Review provenance

- Governing instruction: execute the BSD source-and-equivalence audit, 2026-07-24.
- Canonical tracker: `https://github.com/grandchallenge/MATH-PROGRAMME/issues/66`.
- Pull request: `https://github.com/grandchallenge/MATH-PROGRAMME/pull/67`.
- Programme policy workflow: `30083374165`.
- Review record: `reviews/birch_swinnerton_dyer/BSD-WP00.agent_review.yaml`.

## Supersedes

No prior Birch–Swinnerton-Dyer campaign decision. `ADR-0004` is reserved by the Hodge-conjecture campaign and is not reused here.
