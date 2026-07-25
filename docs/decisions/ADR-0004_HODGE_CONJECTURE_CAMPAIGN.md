# ADR-0004: Initialize the Hodge conjecture as a governed rational cycle-class campaign

**Date:** 2026-07-24  
**Status:** Accepted for draft WP00 audit  
**Owner:** The Amanuensis with the Axiomatist, Cartographer, Archivist, Formalist, and Referee

## Context

The phrase “Hodge conjecture” is frequently used for several non-equivalent statements. The classical Millennium problem concerns rational Hodge classes on smooth projective complex varieties. Nearby integral and compact-Kähler formulations are false in general, while generalized, variational, absolute, motivated, standard-conjecture, Hodge-locus, and Tate statements have different objects and conclusions.

A campaign that begins from the slogan “classes of type `(p,p)` are algebraic” risks losing rationality, projectivity, cycle equivalence, codimension, or universal quantifiers before any mathematical mechanism is tested.

## Decision

Initialize campaign `HC-001` and `HC-WP00` with the canonical target

```math
CH^p(X)\otimes_Z Q
\twoheadrightarrow
H^{2p}(X,Q)\cap H^{p,p}(X)
```

for every smooth projective `X/C` and every `p`, subject to these controls:

1. Rational, integral, and complex coefficient profiles remain separate.
2. Smooth projective and compact-Kähler profiles remain separate.
3. `CH^p`, rational equivalence, and cohomological equality remain explicit.
4. The allowed output is a rational linear combination of algebraic subvarieties; effectivity is not added.
5. The generalized and variational Hodge conjectures are neighboring statements, not alternate labels.
6. Hodge-locus algebraicity, absolute Hodge, motivated cycles, standard conjectures, and Tate classes do not discharge algebraic-cycle construction without an explicit bridge.
7. Algebraicity of Künneth projectors or inverse Lefschetz correspondences may not be assumed in an argument that depends on their conjectural algebraicity.
8. Numerical period recognition is exploratory unless exact arithmetic and a geometric cycle construction close the claim.
9. Formalization begins with claim schemas, statement relations, and conditional boundary logic; unavailable Hodge/Chow foundations remain visible.
10. No restricted target, mechanism, computation, claimed proof, or novelty claim opens before WP00 promotion.

## Alternatives considered

1. State the integral conjecture. Rejected because it is false in general and changes the coefficient ring.
2. Work on arbitrary compact Kähler manifolds. Rejected because the unrestricted analogue is false and projectivity is material.
3. Begin from Hodge loci or period computations. Rejected because recognition and parameter algebraicity do not construct cycles.
4. Treat absolute or motivated classes as sufficient substitutes. Rejected because the missing bridge to algebraic cycles is precisely relevant.
5. Reduce immediately to Tate via good reduction. Rejected because comparison, specialization, field-of-definition, and lifting obligations are separate.
6. Attempt full Lean formalization first. Rejected because the integrated complex-projective/Hodge/Chow stack is not presently available in the bounded library audit.

## Consequences

- `HC-WP00` is registered as a draft governed artifact.
- MATHFORGE, MATHSOLVE, and MATHCERT companion lanes are required.
- The elementary boundary `p=0,1,n-1,n` and the dimension-at-most-three consequence are reconstructed before special-case generation.
- WP01 and WP02 remain closed until Amanuensis, Referee, and CI gates pass.
- `HC-R021` remains unselected until false-proof, known-case, construction, and prior-art ledgers are integrated.

## Unresolved obligations

- Complete exact historical source concordance for Hodge 1950.
- Locate and extract the exact Zucker compact-Kähler appendix cited by Deligne.
- Normalize Grothendieck's corrected generalized-Hodge and Tate's arithmetic formulations.
- Build a comprehensive higher-dimensional known-case ledger.
- Implement claim-schema mutation fixtures.
- Complete cross-pillar PR validation and final review.

## Affected artifacts

- `DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md`
- `campaigns/hodge_conjecture/WP00_FOUNDATION_STATUS/`
- `reviews/hodge_conjecture/HC-WP00.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `MATH-PROGRAMME#65`
- `MATHFORGE#21`
- `MATHSOLVE#62`
- `MATHCERT#23`

## Review provenance

- Governing instruction: execute `HC-WP00`, 2026-07-24.
- Canonical tracker: `https://github.com/grandchallenge/MATH-PROGRAMME/issues/65`.
- Review record: `reviews/hodge_conjecture/HC-WP00.agent_review.yaml`.

## Supersedes

No prior Hodge campaign decision. `ADR-0002` governs the accepted Union-Closed Agent Council pilot and is not reused here.
