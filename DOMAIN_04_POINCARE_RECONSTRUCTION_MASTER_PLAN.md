# DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md

## Domain

**Domain 04: Poincaré theorem / Hamilton–Perelman proof reconstruction**

- Campaign identifier: `PC-001`
- Canonical tracker: `MATH-PROGRAMME#69`
- Result status: `SOLVED_CLASSICAL_THEOREM`
- Programme state: `WP00_PROMOTED_WP01_WP02_PERMITTED`
- Primary route: Ricci flow with surgery plus finite-time extinction
- Stronger routes: elliptization and Thurston geometrization
- Claim posture: reconstruction, dependency audit, pedagogy, and selective certification; no novelty claim

## Canonical theorem

Let `M` be a closed, connected topological `3`-manifold. Then

```math
\pi_1(M)=1
\quad\Longrightarrow\quad
M\cong_{\mathrm{Top}}S^3.
```

Here `closed` means compact without boundary. After the dimension-three category bridge, the corresponding smooth statement is equivalent in content:

> Every closed, connected, simply connected smooth `3`-manifold is diffeomorphic to `S³`.

## Programme posture

This is a solved-problem reconstruction campaign. It must:

1. preserve the official solved status;
2. distinguish topological, PL, smooth, elliptization, geometrization, and finite-extinction formulations;
3. mark equivalences separately from one-way stronger implications;
4. expose every imported theorem between topology, smooth geometry, Ricci flow, surgery, extinction, and terminal classification;
5. version and cross-check the Hamilton–Perelman source chain;
6. maintain a proof-dependency graph, claim ledger, and proof-debt register;
7. formalize only delimited slices whose imported boundaries remain visible.

## Category bridge

Ricci flow acts on smooth Riemannian manifolds, whereas the canonical theorem is topological. Dimension-three triangulation, Hauptvermutung, and smoothing results give the required bridge:

```text
closed topological 3-manifold
  -> compatible PL structure
  -> compatible smooth structure
  -> smooth Riemannian metric
  -> Hamilton–Perelman flow
  -> diffeomorphism conclusion
  -> homeomorphism conclusion.
```

The phrase “choose a metric” may not conceal these dependencies.

## Audited proof routes

### Route A — geometrization

```text
geometrization
  -> elliptization in the finite-fundamental-group case
  -> spherical space form S^3/Gamma
  -> Gamma = 1 when pi_1(M)=1
  -> M = S^3.
```

This route is valid but strictly stronger than Poincaré.

### Route B — elliptization

```text
finite pi_1
  -> M diffeomorphic to S^3/Gamma
  -> pi_1(M) is Gamma
  -> trivial pi_1 gives Gamma=1
  -> M diffeomorphic to S^3.
```

Elliptization implies Poincaré. Poincaré alone does not imply elliptization.

### Route C — finite extinction

```text
category bridge and initial metric
  -> Ricci flow with surgery
  -> finite-time extinction for the relevant topological class
  -> surgery-history connected-sum classification
  -> simple connectivity eliminates every nontrivial factor
  -> M diffeomorphic to S^3
  -> M homeomorphic to S^3.
```

This is the primary Poincaré-specific reconstruction route.

## Theorem spine

```text
PC-D000  Category, compactness, connectedness, and fundamental-group conventions
PC-L001  Dimension-three topological/PL/smooth category bridge
PC-L002  Simple connectivity implies orientability
PC-L003  Existence and normalization of a smooth Riemannian metric
PC-L004  Short-time Ricci flow interface
PC-L005  Entropy, reduced geometry, and no-local-collapsing interfaces
PC-L006  High-curvature limits and canonical-neighbourhood interface
PC-L007  Ricci flow with surgery existence and parameter hierarchy
PC-L008  Topological description of surgery and discarded components
PC-L009  Prime-decomposition/no-aspherical-factor hypothesis bridge
PC-L010  Finite-time extinction theorem
PC-L011  Extinction plus surgery history gives connected-sum classification
PC-L012  van Kampen/free-product elimination of nontrivial factors
PC-C013  Smooth Poincaré conclusion
PC-C014  Topological Poincaré conclusion
PC-B015  Elliptization implies Poincaré
PC-B016  Geometrization implies elliptization
PC-T017  Source-complete Hamilton–Perelman reconstruction target
```

## Dependency architecture

```text
D000 -> L001 -> L003 -> L004 -> L005 -> L006 -> L007 -> L008 -> L011 -> L012 -> C013 -> C014
  |                                                    ^          ^
  +-> L002 --------------------------------------------+          |
  +-> L009 -> L010 -----------------------------------------------+

B016 -> B015 -> C014
```

`B015` and `B016` are implication routes, not equivalences with the Poincaré theorem.

## Source hierarchy

### Primary proof sources

1. Grisha Perelman, *The entropy formula for the Ricci flow and its geometric applications*, arXiv:`math/0211159`.
2. Grisha Perelman, *Ricci flow with surgery on three-manifolds*, arXiv:`math/0303109`.
3. Grisha Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds*, arXiv:`math/0307245`.

### Detailed reconstructions

4. John Morgan and Gang Tian, *Ricci Flow and the Poincaré Conjecture*, Clay Mathematics Monographs 3, 2007.
5. Bruce Kleiner and John Lott, *Notes on Perelman's Papers*, Geometry & Topology 12 (2008), arXiv:`math/0605667`.
6. Huai-Dong Cao and Xi-Ping Zhu, *A Complete Proof of the Poincaré and Geometrization Conjectures*, Asian Journal of Mathematics 10 (2006), used with attribution and version-history caution.

### Foundational topology and geometry

7. Edwin E. Moise, dimension-three triangulation and Hauptvermutung.
8. James Munkres, compatible smoothing results.
9. Richard Hamilton, positive-curvature, singularity-formation, and nonsingular-flow precursor results.
10. Kneser–Milnor prime decomposition and van Kampen connected-sum interfaces.
11. John Milnor and the Clay Mathematics Institute for the canonical statement and official status.

## Work Packages

### PC-WP00 — source, normalization, equivalence, and non-circularity audit

Status: promoted.

Delivered:

- solved-result status correction;
- category dictionary and bridge;
- implication/equivalence matrix;
- proof-route separation;
- source hierarchy;
- theorem DAG;
- claim and proof-debt ledgers;
- MATHCERT handoff;
- Agent Council review and next-stage gate.

### PC-WP01 — false-proof and semantic-failure atlas

Status: permitted.

Required failures include homology-sphere substitution, Whitehead-manifold substitution, boundary suppression, smooth flow through singularity, surgery treated as topology-preserving, extinction without bookkeeping, blow-up/original-space confusion, category suppression, route-strength collapse, circular prime-factor discharge, and formal-interface overclaim.

### PC-WP02 — source-normalized Hamilton–Perelman ledger

Status: permitted.

Extract exact theorem statements, hypotheses, constants, normalizations, parameter dependencies, corrections, and consumers for entropy, reduced geometry, non-collapsing, `kappa`-solutions, canonical neighbourhoods, surgery, topology changes, and finite extinction.

### PC-WP03 — surgery topology and extinction bookkeeping

Status: closed pending WP01/WP02 integration.

### PC-WP04 — certification substrate

Status: initial handoff open only for finite history and terminal algebraic/topological logic.

## Three-pillar split

### MATHFORGE

- source discovery and edition control;
- false-proof atlas;
- reconstruction comparison;
- theorem-location and citation audit.

### MATHSOLVE

- theorem spine and proof-debt ownership;
- analytic theorem ledger;
- surgery/extinction reconstruction;
- pedagogical compression only after dependency closure.

### MATHCERT

- finite surgery-history representation;
- connected-sum and group-expression terminal logic;
- provenance-bearing analytic interfaces;
- no full-proof badge unless the imported analytic chain is actually formalized.

## Foundational profile

- Carrier: closed connected topological, PL, smooth, and Riemannian `3`-manifolds.
- Ambient structures: algebraic topology, geometric topology, Riemannian geometry, nonlinear parabolic PDE, geometric measure theory, and finite surgery histories.
- Classical base: standard classical mathematics.
- Witness policy: literature-derived complete proof; formal certificates initially cover selected logical and combinatorial slices.
- Pathology risk: high at category changes, singular limits, surgery times, discarded components, and compressed theorem interfaces.

## Claim boundary

The campaign does not claim:

- a new proof;
- independent verification of every Hamilton–Perelman estimate;
- equivalence of Poincaré with elliptization or geometrization;
- that extinction alone determines topology;
- that formalized implication interfaces certify their analytic assumptions;
- novelty for any classical component.

## Current executable stage

Execute `PC-WP01` and `PC-WP02` in parallel. `PC-WP03` remains closed until adversarial review and cross-document integration establish a stable surgery-and-extinction interface.