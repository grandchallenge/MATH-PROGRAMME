# DOMAIN_03_POINCARE_RECONSTRUCTION_MASTER_PLAN.md

## Domain

**Domain 03: Poincaré theorem / Hamilton–Perelman proof reconstruction**

- Campaign identifier: `PC-001`
- Canonical tracker: `MATH-PROGRAMME#69`
- Result status: `SOLVED_CLASSICAL_THEOREM`
- Programme state: `WP00_PROMOTED_WP01_WP02_PERMITTED`
- Primary route: Ricci flow with surgery plus finite-time extinction
- Stronger ambient route: Thurston geometrization and elliptization
- Claim posture: reconstruction, dependency audit, pedagogy, and selective certification; no novelty claim

## Canonical theorem

Let `M` be a closed, connected topological `3`-manifold. If

```math
\pi_1(M)=1,
```

then

```math
M\cong S^3.
```

Here `closed` means compact without boundary. The symbol `≅` denotes homeomorphism in the canonical topological statement.

After the dimension-three category bridge, the corresponding smooth statement is stronger in wording but equivalent in content:

> Every closed, connected, simply connected smooth `3`-manifold is diffeomorphic to `S³`.

## Correct programme posture

This campaign does not attempt to rediscover an open solution. It reconstructs and certifies the logical architecture of a solved theorem.

The obligations are therefore different from an open-problem campaign:

1. identify the canonical theorem and result status;
2. separate topological, PL, smooth, elliptization, geometrization, and finite-extinction formulations;
3. state which formulations are equivalent and which are only one-way strengthenings;
4. expose every imported theorem in the passage from topology to Ricci flow and back;
5. audit the Hamilton–Perelman source chain without replacing compressed arguments by folklore;
6. construct a proof-dependency graph suitable for pedagogical reconstruction and selective formalization;
7. preserve the boundary between a source-complete reconstruction and an independent re-proof of the full analytic core.

## Why the category bridge matters

Ricci flow is defined on smooth Riemannian manifolds, while the canonical Poincaré statement is topological. In dimension three, the discrepancies among the topological, piecewise-linear, and smooth categories disappear through the Moise triangulation/Hauptvermutung theorem and compatible smoothing results.

The campaign must therefore make the bridge explicit:

```text
closed topological 3-manifold
  -> compatible PL structure
  -> compatible smooth structure
  -> smooth Riemannian metric
  -> Hamilton–Perelman flow
  -> diffeomorphism conclusion
  -> homeomorphism conclusion.
```

None of these arrows is to be hidden inside the phrase “choose a metric.”

## Audited proof routes

### Route A — full geometrization

```text
Thurston geometrization
  -> spherical geometry for the finite-fundamental-group case
  -> trivial deck group when pi_1(M)=1
  -> M is S^3.
```

This route is valid but stronger than necessary for the Poincaré conclusion.

### Route B — elliptization / spherical space-form theorem

```text
closed 3-manifold with finite pi_1
  -> spherical space form S^3/Gamma
  -> pi_1(M) is isomorphic to Gamma
  -> Gamma is trivial when pi_1(M)=1
  -> M is S^3.
```

Elliptization implies Poincaré. Poincaré alone does not imply elliptization.

### Route C — Poincaré-specific finite-extinction route

```text
topological-to-smooth bridge
  -> initial Riemannian metric
  -> Ricci flow with surgery for all positive time
  -> finite-time extinction for the relevant topological class
  -> surgery-history connected-sum classification
  -> simple connectivity eliminates every non-spherical factor
  -> M is diffeomorphic to S^3.
```

This is the primary reconstruction route.

## Theorem spine

```text
PC-D000  Category, compactness, connectedness, and fundamental-group conventions
PC-L001  Dimension-three topological/PL/smooth category bridge
PC-L002  Simple connectivity implies orientability
PC-L003  Existence and normalization of a smooth Riemannian metric
PC-L004  Short-time Ricci flow interface
PC-L005  Perelman entropy/reduced-volume and no-local-collapsing interfaces
PC-L006  High-curvature limits and canonical-neighbourhood interface
PC-L007  Ricci flow with surgery existence and parameter hierarchy
PC-L008  Topological description of surgery and discarded components
PC-L009  Prime-decomposition/no-aspherical-factor hypothesis bridge
PC-L010  Finite-time extinction theorem
PC-L011  Extinction plus surgery history gives connected-sum classification
PC-L012  van Kampen/free-product elimination of nontrivial factors
PC-C013  Smooth Poincaré conclusion M diffeomorphic to S^3
PC-C014  Topological Poincaré conclusion M homeomorphic to S^3
PC-B015  Elliptization implies Poincaré
PC-B016  Geometrization implies elliptization
PC-T017  Source-complete Hamilton–Perelman reconstruction target
```

## Dependency architecture

```text
D000 -> L001 -> L003 ------------------------------------------┐
  |        |                                                    |
  +-> L002 +----------------------------------------------------+
                                                               v
L004 -> L005 -> L006 -> L007 -> L008 -> L011 -> L012 -> C013 -> C014
                                   ^       ^
                                   |       |
                              L009 -> L010-+

B016 -> B015 -> C014

primary Perelman sources + detailed reconstructions -> L005 ... L010
Moise/Munkres category sources -> L001
Kneser–Milnor + van Kampen -> L009, L011, L012
```

The stronger `B015` and `B016` branches are implication routes, not equivalences with the Poincaré theorem.

## Source hierarchy

### Primary proof sources

1. Grisha Perelman, *The entropy formula for the Ricci flow and its geometric applications*, arXiv:`math/0211159`.
2. Grisha Perelman, *Ricci flow with surgery on three-manifolds*, arXiv:`math/0303109`.
3. Grisha Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds*, arXiv:`math/0307245`.

### Canonical detailed reconstruction

4. John Morgan and Gang Tian, *Ricci Flow and the Poincaré Conjecture*, Clay Mathematics Monographs 3, 2007.

### Independent detailed reconstruction and comparison sources

5. Bruce Kleiner and John Lott, *Notes on Perelman's Papers*, Geometry & Topology 12 (2008), arXiv:`math/0605667`.
6. Huai-Dong Cao and Xi-Ping Zhu, *A Complete Proof of the Poincaré and Geometrization Conjectures — Application of the Hamilton–Perelman Theory of the Ricci Flow*, Asian Journal of Mathematics 10 (2006), with historical attribution interpreted cautiously.

### Foundational topology and geometry sources

7. Edwin E. Moise, *Affine Structures in 3-Manifolds: V. The Triangulation Theorem and Hauptvermutung*, Annals of Mathematics 56 (1952), 96–114.
8. James Munkres, *Obstructions to the Smoothing of Piecewise-Differentiable Homeomorphisms*, Annals of Mathematics 72 (1960), 521–554.
9. Richard Hamilton, *Three-manifolds with positive Ricci curvature*, Journal of Differential Geometry 17 (1982), 255–306.
10. Richard Hamilton, *The formation of singularities in the Ricci flow*, Surveys in Differential Geometry II (1995), 7–136.
11. Richard Hamilton, *Non-singular solutions of the Ricci flow on three-manifolds*, Communications in Analysis and Geometry 7 (1999), 695–729.
12. Kneser–Milnor prime-decomposition and standard van Kampen interfaces, to be source-normalized in the topology ledger.

### Official status and statement sources

13. John Milnor, *The Poincaré Conjecture*, official Clay problem description.
14. Clay Mathematics Institute, Poincaré Conjecture status page, audited as `Solved` on 2026-07-24.

## Work Package sequence

### WP00 — source, normalization, equivalence, and non-circularity audit

Status: promoted.

Delivered:

- canonical theorem and result-status correction;
- category dictionary and topological-to-smooth bridge;
- exact implication/equivalence matrix;
- three proof-route separation;
- source hierarchy;
- theorem spine and dependency DAG;
- proof-debt and claim ledgers;
- MATHCERT handoff;
- Agent Council review and next-stage gate.

### WP01 — false-proof and semantic-failure atlas

Status: permitted.

Required fixtures include:

- homology sphere confused with simply connected sphere;
- contractible open `3`-manifold confused with `R³`;
- smooth Ricci flow assumed to exist through singularities;
- finite extinction treated as topology-free;
- surgery described as topology-preserving;
- pointed blow-up limits confused with the original manifold;
- canonical neighbourhoods asserted without quantitative hypotheses;
- orientability or `RP²` conditions suppressed;
- geometrization, elliptization, and Poincaré treated as equivalent;
- the Poincaré theorem imported circularly in the terminal topology step;
- formalized implication interfaces advertised as a new proof of the analytic core.

### WP02 — source-normalized Hamilton–Perelman theorem ledger

Status: permitted.

Goal: extract exact theorem interfaces, hypotheses, constants, parameter dependencies, and downstream consumers for entropy, reduced distance, no-local-collapsing, `kappa`-solutions, canonical neighbourhoods, surgery, and finite extinction.

### WP03 — surgery topology and extinction bookkeeping

Status: closed pending WP01/WP02 integration.

Goal: reconstruct the complete topological ledger of cuts, caps, discarded components, connected sums, and extinction.

### WP04 — certification substrate

Status: initial MATHCERT handoff open.

Goal: formalize the category-independent terminal logic and finite combinatorial surgery-history certificates while keeping analytic Ricci-flow theorems as provenance-bearing imports.

## Three-pillar split

### MATHFORGE

- source discovery and edition control;
- historical false-proof atlas;
- alternative reconstruction comparison;
- theorem-location and citation audit;
- no claimed-proof or novelty lane is needed for the established theorem itself.

### MATHSOLVE

- theorem spine and proof-debt ownership;
- proof-route separation;
- source-normalized analytic ledger;
- surgery and extinction reconstruction;
- pedagogical compression after dependency closure.

### MATHCERT

- category and terminal topology lemmas;
- connected-sum/fundamental-group logic;
- finite surgery-history data model and validator;
- explicit imported-theorem interfaces for the analytic core;
- no theorem-prover badge may imply that the full Hamilton–Perelman analysis has been independently formalized unless it has.

## Foundational profile

- Carrier: closed connected topological, PL, smooth, and Riemannian `3`-manifolds.
- Ambient structures: algebraic topology, geometric topology, Riemannian geometry, nonlinear parabolic PDE, geometric measure theory, and finite surgery histories.
- Classical base: standard classical mathematics with ordinary choice as used in manifold theory and analysis.
- Witness policy: the proof is literature-derived; formal certificates initially cover only selected logical and combinatorial slices.
- Pathology risk: high at category changes, singular limits, surgery times, discarded components, and compressed source interfaces.

## Claim boundary

This campaign does not claim:

- a new proof of the Poincaré theorem;
- independent verification of every estimate in Perelman's preprints or their reconstructions;
- that Poincaré, elliptization, and geometrization are equivalent;
- that finite extinction alone determines the initial manifold without surgery bookkeeping;
- that a theorem-interface formalization certifies its imported analytic hypotheses;
- novelty for any classical component of the proof.

## Current executable stage

Execute WP01 and WP02 in parallel.

WP01 builds the false-proof and semantic-failure atlas. WP02 builds the source-normalized Hamilton–Perelman theorem ledger. WP03 remains closed until their integration establishes a stable surgery-and-extinction interface.