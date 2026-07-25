# ADR-0003: Initialize Navier–Stokes critical-integrability as a governed campaign

**Date:** 2026-07-23  
**Status:** Accepted for draft initialization  
**Owner:** The Amanuensis with the Axiomatist, Cartographer, Steward, and Referee

## Context

The proposed challenge asks whether every three-dimensional incompressible Navier–Stokes Leray–Hopf solution arising from smooth compactly supported divergence-free data satisfies

```math
∫₀ᵀ ‖u(t)‖_{L⁶(ℝ³)}⁴dt<∞
```

on every finite interval. The estimate is scaling-critical and would place the solution in a classical conditional regularity class. The question is therefore close enough to the central global-regularity problem that loose wording, source drift, or a hidden solution-class mismatch would be materially misleading.

## Decision

Initialize the problem as campaign `NS-CI-001` and Work Package `NS-CI-WP00`, subject to the following controls:

1. `ℝ³` is the primary domain; `𝕋³` is a separate hypothesis profile.
2. The campaign distinguishes the available `L²_tL⁶_x` estimate from the open `L⁴_tL⁶_x` estimate.
3. The energy-space non-embedding witness is used only to rule out generic interpolation shortcuts; it is not a Navier–Stokes counterexample.
4. Imported regularity, local-theory, and weak–strong uniqueness statements remain unpromoted until their exact hypotheses are source-audited.
5. The word `equivalent` remains conditional on a bidirectional correspondence audit with the official positive global-regularity formulation.
6. Formalization begins with mixed-norm scaling and implication interfaces, not with an axiom disguised as the open estimate.
7. Numerical work, when opened, is classified as mechanism exploration and cannot promote a continuum regularity claim.
8. No novelty, near-solution, or progress claim is permitted at initialization.

## Alternatives considered

1. Treat the integral as a routine corollary of the energy inequality. Rejected because the energy estimate gives only square-integrability in time and the reverse finite-measure inclusion is false.
2. Open a broad Navier–Stokes campaign without a single norm target. Rejected because it would lack a falsifiable theorem spine and would encourage unfocused mechanism generation.
3. State immediate equivalence with the Millennium problem without qualification. Rejected until domain, data, solution-class, and weak–strong uniqueness bridges are written explicitly.
4. Begin with large numerical campaigns. Rejected because bounded truncations cannot certify the continuum universal estimate and would precede the source audit.
5. Attempt full PDE formalization first. Rejected because current theorem-prover infrastructure is better used initially on the exact scaling and logical substrate.

## Consequences

- `NS-CI-WP00` is registered as a draft governed artifact.
- Promotion is blocked by source, correspondence, Archivist, and Referee obligations.
- Cross-pillar issues must be opened in MATHFORGE, MATHSOLVE, and MATHCERT.
- WP01 may catalogue invalid routes but cannot be promoted before WP00's source/equivalence audit.
- Restricted target selection is deferred to `NS-CI-R012` after the imported theorem chain is stable.

## Unresolved obligations

- Exact Leray–Hopf and energy-inequality source audit.
- Exact Ladyzhenskaya–Prodi–Serrin theorem audit at `(4,6)`.
- Weak–strong uniqueness and local continuation audit.
- Bidirectional correspondence with the official positive global-regularity branch.
- Dated current-status and claimed-proof audit.
- Theorem-prover library reconnaissance.

## Affected artifacts

- `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`
- `campaigns/navier_stokes_critical_integrability/WP00_FOUNDATION_STATUS/`
- `reviews/navier_stokes/NS-CI-WP00.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `MATH-PROGRAMME#55`

## Review provenance

- Governing instruction: initiate the properly posed MATH-PROGRAMME challenge, 2026-07-23.
- Canonical tracker: `https://github.com/grandchallenge/MATH-PROGRAMME/issues/55`.
- Review record: `reviews/navier_stokes/NS-CI-WP00.agent_review.yaml`.

## Supersedes

No prior Navier–Stokes campaign decision. `ADR-0002` governs the accepted Union-Closed Agent Council pilot and is not reused here.
