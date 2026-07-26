# Domain 08 · Riemann Hypothesis

**Campaign ID:** `RH-001`  
**Mathematical status:** open conjecture  
**Programme state:** WP00 promoted; WP01 and WP02 implemented, merged, and CI-passed but not formally promoted  
**Governance:** `ADR-0009`; `ADR-0010`

## Canonical challenge

Every nontrivial zero of the meromorphically continued Riemann zeta function should have real part `1/2`, with zeros counted using the campaign's fixed multiplicity and range conventions.

The target is the classical Riemann Hypothesis. Generalized variants, simplicity, Lindelöf, density-one results, pair correlation, random-matrix evidence, finite verification, and incomplete spectral proposals are separate statements.

## Programme posture

`RH-WP00` fixes the `zeta`, completed-function, `xi`, `Xi`, and Hardy `Z` normalizations; pole and zero taxonomy; symmetry and multiplicity conventions; exact core equivalences; source-bound arithmetic criteria; spectral obligations; false-proof seeds; theorem spine; proof debt; and certification boundary.

PR #90 implemented and merged the two authorized successor packages:

- `RH-WP01` — an executable eliminative false-proof atlas;
- `RH-WP02` — a source-normalized theorem, criterion, computation, evidence, and barrier ledger.

Their deterministic replay and integrated programme-policy workflow passed. They are not formally promoted: the governing legacy review records retain `promotion_recommended: false` and blocking Referee findings pending independent source-locator review and a schema-bound or explicitly superseding promotion decision.

Mechanism generation, claimed-proof promotion, unrestricted numerical search, novelty claims, and any new zero-range certification remain closed.

## Canonical artifacts

- [WP00 integrated audit](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/RH-WP00-source-normalization-equivalence-audit.md)
- [WP01/WP02 integration dossier](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/RH-WP01-WP02-post-WP00-integration.md)
- [WP01 false-proof atlas](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/riemann_hypothesis/WP01_FALSE_PROOF_ATLAS)
- [WP02 theorem ledger](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/riemann_hypothesis/WP02_THEOREM_LEDGER)
- [Post-merge retained-blocker disposition](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/riemann_hypothesis/RH_WP01_WP02_POST_MERGE_DISPOSITION.md)
- [Merge record PR #90](https://github.com/grandchallenge/MATH-PROGRAMME/pull/90)
- [Catalogue-integration decision ADR-0009](../decisions/ADR-0009_POST_MERGE_DOMAIN_COVERAGE.md)
- [Continuity and documentary authority decision ADR-0010](../decisions/ADR-0010_DOCUMENTARY_LIBRARY_AUTHORITY.md)

## Claim boundary

The programme has not proved or disproved RH, established a new zero-free region, critical-line proportion, prime-counting error estimate, equivalent criterion, Hilbert–Pólya operator, newly certified zero computation, or novelty result. Implementation, repository merge, replay, CI success, public documentation, and documentary publication are not theorem support.
