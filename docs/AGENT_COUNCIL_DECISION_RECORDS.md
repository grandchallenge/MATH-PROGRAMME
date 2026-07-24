# Agent Council Decision Records

## Status

Active programme register.

**Owner:** The Amanuensis.

Decision records preserve governance choices that affect how an artifact must be interpreted, reviewed, integrated, or superseded. They record why a choice was made and which alternatives were rejected. They do not replace mathematical proofs, claim ledgers, or source provenance.

## Record contract

Each decision record contains:

- a stable decision ID;
- date and decision status;
- context and governing problem;
- the adopted decision;
- material alternatives considered;
- consequences and unresolved obligations;
- affected artifact references;
- review-provenance references;
- supersession relationships, when applicable.

## ADR-0001: Establish the Amanuensis continuity office

**Date:** 2026-07-09  
**Status:** Accepted  
**Owner:** The Amanuensis

### Context

The Agent Council assigned specialist responsibilities for foundations, discovery, verification, exposition, implementation, provenance, and external review. No office was responsible for preserving the programme's internal reasoning across revisions or for integrating specialist reviews into one authoritative artifact.

### Decision

Establish the Amanuensis as the council office responsible for:

- the artifact ledger;
- decision records;
- the terminology registry;
- review provenance;
- cross-document consistency;
- final editorial integration.

Every governed artifact carries an `amanuensis_control` record. Promotion is blocked when the artifact-ledger identity is absent, review provenance is incomplete, cross-document consistency is not reviewed, final integration is not reviewed, or no authoritative integrated artifact is identified.

### Alternatives considered

1. Assign these duties to the Archivist. Rejected because external literature provenance and internal editorial continuity are distinct responsibilities.
2. Leave continuity implicit in pull-request history. Rejected because commit history does not express semantic decisions, unresolved obligations, or the authoritative integrated version.
3. Treat final integration as a Composer duty. Rejected because composition governs artifact structure, not continuity across versions and review states.

### Consequences

- The Exposition Kernel expands from four writing offices to an Exposition and Continuity Kernel of five offices.
- Agent-review schemas require the Amanuensis and an `amanuensis_control` record.
- Work Package promotion now includes continuity and integration gates.
- The repository maintains canonical artifact, decision, and terminology registers.

### Affected artifacts

- `docs/MATH_PROGRAMME_AGENT_COUNCIL.md`
- `docs/AGENT_COUNCIL_GOVERNANCE.md`
- `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`
- `templates/agent_review.yaml`
- `schemas/agent_review.schema.json`
- `schemas/agent_review.schema.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`

### Review provenance

- Governing instruction: Grand Challenge MATH-PROGRAMME council deliberation, 2026-07-09.
- Repository integration: pull request 50, branch `agent-council-governance`.

### Supersedes

No prior decision record.

## ADR-0003: Initialize Navier–Stokes critical-integrability as a governed campaign

**Date:** 2026-07-23  
**Status:** Accepted for draft initialization  
**Owner:** The Amanuensis with the Axiomatist, Cartographer, Steward, and Referee

### Context

The proposed challenge asks whether every three-dimensional incompressible Navier–Stokes Leray–Hopf solution arising from smooth compactly supported divergence-free data satisfies

```math
∫₀ᵀ ‖u(t)‖_{L⁶(ℝ³)}⁴dt<∞
```

on every finite interval. The estimate is scaling-critical and would place the solution in a classical conditional regularity class. The question is therefore close enough to the central global-regularity problem that loose wording, source drift, or a hidden solution-class mismatch would be materially misleading.

### Decision

Initialize the problem as campaign `NS-CI-001` and Work Package `NS-CI-WP00`, subject to the following controls:

1. `ℝ³` is the primary domain; `𝕋³` is a separate hypothesis profile.
2. The campaign distinguishes the available `L²_tL⁶_x` estimate from the open `L⁴_tL⁶_x` estimate.
3. The energy-space non-embedding witness is used only to rule out generic interpolation shortcuts; it is not a Navier–Stokes counterexample.
4. Imported regularity, local-theory, and weak–strong uniqueness statements remain unpromoted until their exact hypotheses are source-audited.
5. The word `equivalent` remains conditional on a bidirectional correspondence audit with the official positive global-regularity formulation.
6. Formalization begins with mixed-norm scaling and implication interfaces, not with an axiom disguised as the open estimate.
7. Numerical work, when opened, is classified as mechanism exploration and cannot promote a continuum regularity claim.
8. No novelty, near-solution, or progress claim is permitted at initialization.

### Alternatives considered

1. Treat the integral as a routine corollary of the energy inequality. Rejected because the energy estimate gives only square-integrability in time and the reverse finite-measure inclusion is false.
2. Open a broad Navier–Stokes campaign without a single norm target. Rejected because it would lack a falsifiable theorem spine and would encourage unfocused mechanism generation.
3. State immediate equivalence with the Millennium problem without qualification. Rejected until domain, data, solution-class, and weak–strong uniqueness bridges are written explicitly.
4. Begin with large numerical campaigns. Rejected because bounded truncations cannot certify the continuum universal estimate and would precede the source audit.
5. Attempt full PDE formalization first. Rejected because current theorem-prover infrastructure is better used initially on the exact scaling and logical substrate.

### Consequences

- `NS-CI-WP00` is registered as a draft governed artifact.
- Promotion is blocked by source, correspondence, Archivist, and Referee obligations.
- Cross-pillar issues must be opened in MATHFORGE, MATHSOLVE, and MATHCERT.
- WP01 may catalogue invalid routes but cannot be promoted before WP00's source/equivalence audit.
- Restricted target selection is deferred to `NS-CI-R012` after the imported theorem chain is stable.

### Unresolved obligations

- Exact Leray–Hopf and energy-inequality source audit.
- Exact Ladyzhenskaya–Prodi–Serrin theorem audit at `(4,6)`.
- Weak–strong uniqueness and local continuation audit.
- Bidirectional correspondence with the official positive global-regularity branch.
- Dated current-status and claimed-proof audit.
- Theorem-prover library reconnaissance.

### Affected artifacts

- `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`
- `campaigns/navier_stokes_critical_integrability/WP00_FOUNDATION_STATUS/`
- `reviews/navier_stokes/NS-CI-WP00.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `MATH-PROGRAMME#55`

### Review provenance

- Governing instruction: initiate the properly posed MATH-PROGRAMME challenge, 2026-07-23.
- Canonical tracker: `https://github.com/grandchallenge/MATH-PROGRAMME/issues/55`.
- Review record: `reviews/navier_stokes/NS-CI-WP00.agent_review.yaml`.

### Supersedes

No prior Navier–Stokes campaign decision. `ADR-0002` remains reserved by the open Union-Closed Agent Council pilot and is not reused here.

## ADR-0004: Initialize the Hodge conjecture as a governed rational cycle-class campaign

**Date:** 2026-07-24  
**Status:** Accepted for draft WP00 audit  
**Owner:** The Amanuensis with the Axiomatist, Cartographer, Archivist, Formalist, and Referee

### Context

The phrase “Hodge conjecture” is frequently used for several non-equivalent statements. The classical Millennium problem concerns rational Hodge classes on smooth projective complex varieties. Nearby integral and compact-Kahler formulations are false in general, while generalized, variational, absolute, motivated, standard-conjecture, Hodge-locus, and Tate statements have different objects and conclusions.

A campaign that begins from the slogan “classes of type `(p,p)` are algebraic” risks losing rationality, projectivity, cycle equivalence, codimension, or universal quantifiers before any mathematical mechanism is tested.

### Decision

Initialize campaign `HC-001` and `HC-WP00` with the canonical target

```math
CH^p(X)\otimes_Z Q
\twoheadrightarrow
H^{2p}(X,Q)\cap H^{p,p}(X)
```

for every smooth projective `X/C` and every `p`, subject to these controls:

1. Rational, integral, and complex coefficient profiles remain separate.
2. Smooth projective and compact-Kahler profiles remain separate.
3. `CH^p`, rational equivalence, and cohomological equality remain explicit.
4. The allowed output is a rational linear combination of algebraic subvarieties; effectivity is not added.
5. The generalized and variational Hodge conjectures are neighboring statements, not alternate labels.
6. Hodge-locus algebraicity, absolute Hodge, motivated cycles, standard conjectures, and Tate classes do not discharge algebraic-cycle construction without an explicit bridge.
7. Algebraicity of Kunneth projectors or inverse Lefschetz correspondences may not be assumed in an argument that depends on their conjectural algebraicity.
8. Numerical period recognition is exploratory unless exact arithmetic and a geometric cycle construction close the claim.
9. Formalization begins with claim schemas, statement relations, and conditional boundary logic; unavailable Hodge/Chow foundations remain visible.
10. No restricted target, mechanism, computation, claimed proof, or novelty claim opens before WP00 promotion.

### Alternatives considered

1. State the integral conjecture. Rejected because it is false in general and changes the coefficient ring.
2. Work on arbitrary compact Kahler manifolds. Rejected because the unrestricted analogue is false and projectivity is material.
3. Begin from Hodge loci or period computations. Rejected because recognition and parameter algebraicity do not construct cycles.
4. Treat absolute or motivated classes as sufficient substitutes. Rejected because the missing bridge to algebraic cycles is precisely relevant.
5. Reduce immediately to Tate via good reduction. Rejected because comparison, specialization, field-of-definition, and lifting obligations are separate.
6. Attempt full Lean formalization first. Rejected because the integrated complex-projective/Hodge/Chow stack is not presently available in the bounded library audit.

### Consequences

- `HC-WP00` is registered as a draft governed artifact.
- MATHFORGE, MATHSOLVE, and MATHCERT companion lanes are required.
- The elementary boundary `p=0,1,n-1,n` and the dimension-at-most-three consequence are reconstructed before special-case generation.
- WP01 and WP02 remain closed until Amanuensis, Referee, and CI gates pass.
- `HC-R021` remains unselected until false-proof, known-case, construction, and prior-art ledgers are integrated.

### Unresolved obligations

- Complete exact historical source concordance for Hodge 1950.
- Locate and extract the exact Zucker compact-Kahler appendix cited by Deligne.
- Normalize Grothendieck's corrected generalized-Hodge and Tate's arithmetic formulations.
- Build a comprehensive higher-dimensional known-case ledger.
- Implement claim-schema mutation fixtures.
- Complete cross-pillar PR validation and final review.

### Affected artifacts

- `DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md`
- `campaigns/hodge_conjecture/WP00_FOUNDATION_STATUS/`
- `reviews/hodge_conjecture/HC-WP00.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `MATH-PROGRAMME#65`
- `MATHFORGE#21`
- `MATHSOLVE#62`
- `MATHCERT#23`

### Review provenance

- Governing instruction: execute `HC-WP00`, 2026-07-24.
- Canonical tracker: `https://github.com/grandchallenge/MATH-PROGRAMME/issues/65`.
- Review record: `reviews/hodge_conjecture/HC-WP00.agent_review.yaml`.

### Supersedes

No prior Hodge campaign decision. `ADR-0002` remains reserved and is not reused.

## ADR-0005: Initialize Poincaré as a solved-problem reconstruction campaign

**Date:** 2026-07-24  
**Status:** Accepted and promoted through WP00  
**Owner:** The Amanuensis with the Axiomatist, Archivist, Cartographer, Formalist, Steward, and Referee

### Context

The proposed challenge names the Poincaré Conjecture, but the mathematical problem was solved by Perelman through the Hamilton Ricci-flow programme. Treating it as an open conjecture would corrupt the result-status ledger and invite inappropriate novelty, mechanism-generation, or numerical-evidence workflows.

The canonical theorem is topological, while the proof uses smooth Riemannian geometry and nonlinear PDE. In addition, several related statements—smooth Poincaré, elliptization, geometrization, Ricci flow with surgery, and finite extinction—are often compressed into one narrative despite having different logical strengths and dependencies.

### Decision

Initialize campaign `PC-001` and Work Package `PC-WP00` as a **solved-problem reconstruction campaign**, subject to the following controls:

1. The canonical target is the topological theorem: every closed connected simply connected topological `3`-manifold is homeomorphic to `S³`.
2. The topological, PL, and smooth formulations are treated as equivalent only through named dimension-three category theorems.
3. Geometrization implies elliptization, and elliptization implies Poincaré; no converse implication is claimed.
4. The primary pedagogical route is Ricci flow with surgery plus finite extinction and explicit surgery-topology bookkeeping.
5. Finite extinction is never used as a topology-free conclusion.
6. Perelman's three preprints remain the primary proof sources; detailed reconstructions are secondary sources and cross-checks.
7. Versioned source corrections, including modifications recorded in Perelman's surgery paper, must remain visible.
8. Formalization begins with finite surgery-history and terminal factor/fundamental-group logic, not with an axiom packaging the analytic core.
9. Numerical experimentation is not an evidentiary route for this solved theorem.
10. No new-proof, independent-recertification, novelty, or priority claim is permitted at WP00.

### Alternatives considered

1. Treat the challenge as an open Millennium problem. Rejected because the official status is solved.
2. Present only the implication “geometrization implies Poincaré.” Rejected because it hides the Poincaré-specific finite-extinction route and its mechanisms.
3. Begin directly in the smooth category. Rejected because the canonical theorem is topological and the category bridge is a substantive imported dependency.
4. State that Poincaré, elliptization, and geometrization are equivalent. Rejected because the latter statements are strictly stronger in scope.
5. Formalize a terminal implication theorem and label it a formal proof of Poincaré. Rejected because the geometric and analytic imports would remain unformalized.
6. Compress the proof to “Ricci flow rounds the manifold.” Rejected because general flows develop singularities and require non-collapsing, canonical neighbourhoods, surgery, and extinction analysis.

### Consequences

- `PC-WP00` is registered as a promoted governed artifact.
- The terms `solved-problem reconstruction campaign` and `finite-extinction route` are entered in the terminology registry.
- WP01 and WP02 may proceed in parallel.
- WP01 must build a false-proof and semantic-failure atlas.
- WP02 must produce a source-normalized Hamilton–Perelman theorem ledger and source crosswalk.
- PC-WP03 remains closed until WP01/WP02 integration and Referee review.
- MATHCERT work is limited initially to delimited finite-history and terminal algebraic/topological slices.

### Unresolved obligations

- Exact Moise/Munkres category-theorem extraction.
- Versioned Perelman/Morgan–Tian/Kleiner–Lott theorem crosswalk.
- Canonical-neighbourhood and surgery-parameter dependency ledger.
- Exact topology of surgeries and discarded components.
- Non-circular bridge to the finite-extinction hypothesis class.
- Finite-extinction proof ledger.
- Formal finite surgery-history and terminal factor-discharge substrate.

### Affected artifacts

- `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`
- `campaigns/poincare_reconstruction/WP00_SOURCE_EQUIVALENCE/`
- `reviews/poincare/PC-WP00.agent_review.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`
- `MATH-PROGRAMME#69`

### Review provenance

- Governing instruction: initiate and proceed with the Poincaré MATH-PROGRAMME challenge, 2026-07-24.
- Canonical tracker: `https://github.com/grandchallenge/MATH-PROGRAMME/issues/69`.
- Review record: `reviews/poincare/PC-WP00.agent_review.yaml`.
- Primary-source registry: `campaigns/poincare_reconstruction/WP00_SOURCE_EQUIVALENCE/04_PROBLEM_SOURCE_EQUIVALENCE_AUDIT.md`.

### Supersedes

No prior Poincaré campaign decision. The decision reserves the term “conjecture” for historical naming and uses “Poincaré theorem” for current mathematical status.