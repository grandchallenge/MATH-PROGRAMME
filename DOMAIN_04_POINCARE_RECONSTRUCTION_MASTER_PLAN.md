# DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md

## Domain

**Domain 04: Poincaré theorem / Hamilton–Perelman proof reconstruction**

- Campaign identifier: `PC-001`
- Canonical tracker: `MATH-PROGRAMME#69`
- Result status: `SOLVED_CLASSICAL_THEOREM`
- Programme state: `WP05_REFEREE_PROMOTED_QUALIFIED_ARCHIVE_READY`
- Primary route: Ricci flow with surgery plus finite-time extinction
- Stronger routes: elliptization and Thurston geometrization
- Claim posture: source-normalized reconstruction, adversarial audit, conditional topology certification, bounded kernel checking, and qualified archival publication; no novelty claim

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
6. maintain theorem, false-proof, event, claim, proof-debt, certificate, trust, and archive ledgers;
7. formalize only delimited slices whose imported boundaries remain visible;
8. publish only under the bounded archival description fixed by `ARCHIVE-PC-001`.

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
  -> spherical space form S3/Gamma
  -> Gamma = 1 when pi1(M)=1
  -> M = S3.
```

This route is valid but strictly stronger than Poincaré.

### Route B — elliptization

```text
finite pi1
  -> M diffeomorphic to S3/Gamma
  -> pi1(M) is Gamma
  -> trivial pi1 gives Gamma=1
  -> M diffeomorphic to S3.
```

Elliptization implies Poincaré. Poincaré alone does not imply elliptization.

### Route C — finite extinction

```text
category bridge and initial metric
  -> smooth Ricci-flow segments
  -> high-curvature canonical neighbourhoods
  -> controlled surgery and restart
  -> all-time Ricci flow with surgery
  -> finite-time extinction
  -> finite source-bound surgery history
  -> backward connected-sum reconstruction
  -> simple connectivity eliminates every nontrivial factor
  -> M diffeomorphic to S3
  -> M homeomorphic to S3.
```

This is the primary Poincaré-specific reconstruction route.

## Theorem spine

```text
PC-D000  Category, compactness, connectedness, and fundamental-group conventions
PC-L001  Dimension-three topological/PL/smooth category bridge
PC-L002  Simple connectivity implies orientability
PC-L003  Existence and normalization of a smooth Riemannian metric
PC-L004  Short-time Ricci flow interface
PC-L005  Entropy, reduced geometry, pseudolocality, and no-local-collapsing
PC-L006  Ancient limits and canonical-neighbourhood interface
PC-L007  Standard caps, surgery, noncollapse, and all-time surgery flow
PC-L008  Topological description of surgery and discarded components
PC-L009  Prime-decomposition/no-aspherical-factor hypothesis bridge
PC-L010  Finite-time extinction theorem
PC-L011  Finite surgery history and backward connected-sum reconstruction
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

## Certification architecture

```text
WP02 imported topology/extinction interfaces
  -> WP03 source-bound finite event contract
  -> WP03 executable history validation
  -> WP04 Lean event and history carriers
  -> WP04 finite backward evaluator
  -> WP04 active-set and evaluator correctness theorems
  -> WP04 provenance-preserving bounded certificate
  -> WP05 claim-level trust and archival closure.
```

The formal boundary is `ImportedEventRelation`. It connects a source-certified event to its finite reconstruction equation. It does not assert event existence or any Ricci-flow analytic theorem.

## Adversarial guard architecture

`PC-WP01` protects the proof spine from:

```text
D000 -> homology/open/boundary substitutions
L001 -> category suppression
L004/L007 -> smooth-flow-through-singularity
L006 -> pointed-limit/global-manifold confusion and deleted hypotheses
L007/L008 -> surgery topology, orientation, finiteness, and source drift
L010/L011 -> extinction without topology
L009/L012 -> circular prime-factor discharge
B015/B016 -> stronger-route equivalence collapse
T017 -> formal-interface overclaim.
```

`PC-WP03` adds executable event-history guards for source omission, component loss, ancestry collision, malformed cuts, impermissible discards, orientation drift, discreteness/finiteness confusion, nonempty terminal slices, and terminal group-profile failure.

`PC-WP04` adds certificate-policy guards for source removal, declaration drift, proof placeholders, and opaque local axioms.

`PC-WP05` adds archival-policy guards against removed disclosures, false closure of source-concordance debt, false analytic-formalization claims, trust-matrix deletion, and reopening of the new-proof gate.

Passing these guards is necessary but is not an analytic proof certificate.

## Source hierarchy

### Primary proof sources

1. Grisha Perelman, *The entropy formula for the Ricci flow and its geometric applications*, arXiv:`math/0211159`.
2. Grisha Perelman, *Ricci flow with surgery on three-manifolds*, arXiv:`math/0303109`.
3. Grisha Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds*, arXiv:`math/0307245`.

### Detailed reconstructions

4. John Morgan and Gang Tian, *Ricci Flow and the Poincaré Conjecture*, Clay Mathematics Monographs 3, 2007.
5. Bruce Kleiner and John Lott, *Notes on Perelman's Papers*, Geometry & Topology 12 (2008), arXiv:`math/0605667`, version 5 used for concordance.
6. Huai-Dong Cao and Xi-Ping Zhu, *A Complete Proof of the Poincaré and Geometrization Conjectures*, Asian Journal of Mathematics 10 (2006), used with attribution and version-history caution.

### Foundational topology and geometry

7. Edwin E. Moise, dimension-three triangulation and Hauptvermutung.
8. James Munkres, compatible smoothing results.
9. Richard Hamilton, short-time, curvature, singularity, and nonsingular-flow precursor results.
10. Kneser–Milnor prime decomposition and van Kampen connected-sum interfaces.
11. John Milnor and the Clay Mathematics Institute for the canonical statement and official status.

## Source-concordance disposition

The campaign-critical theorem roles and logical directions are concordant across Perelman I/II/III, Morgan–Tian, and Kleiner–Lott:

- Perelman I governs entropy, reduced geometry, noncollapsing, and singularity-model preparation;
- Perelman II governs controlled surgery and all-time continuation;
- Perelman III governs finite extinction;
- Kleiner–Lott provides the detailed reconstruction cross-check for Perelman I and II and the finite-extinction handoff;
- Morgan–Tian is the governing complete detailed Poincaré reconstruction, including topology mutation and terminal reconstruction.

The graph-manifold assertion deferred in Perelman II and the maximal-horn/eventual-smoothness assertion identified there as unjustified are excluded from the selected finite-extinction route.

Line-by-line proof concordance, exact parameter translation, and independent analytic verification remain explicit debt. They block stronger claims but not the qualified archive.

## Work Packages

### PC-WP00 — source, normalization, equivalence, and non-circularity audit

Status: `PROMOTED`.

Delivered canonical status, category bridge, route hierarchy, source tiers, theorem DAG, proof debt, claim ledger, certification handoff, and Agent Council governance.

### PC-WP01 — false-proof and semantic-failure atlas

Status: `REFEREE_PROMOTED`.

Delivered fifteen exact semantic and proof-route fixtures.

Canonical artifact:

- `campaigns/poincare_reconstruction/WP01_FALSE_PROOF_ATLAS/00_README.md`

### PC-WP02 — source-normalized Hamilton–Perelman ledger

Status: `REFEREE_PROMOTED_AT_THEOREM_INTERFACE_LEVEL`.

Delivered the source ledger, correction crosswalk, parameter hierarchy, nineteen theorem interfaces, finite-extinction mechanism ledger, proof debt, claims, and MATHCERT handoff.

Canonical artifact:

- `campaigns/poincare_reconstruction/WP02_HAMILTON_PERELMAN_LEDGER/00_README.md`

The promotion does not assert independent analytic verification or full formalization.

### PC-WP03 — surgery topology and extinction bookkeeping

Status: `REFEREE_PROMOTED_CONDITIONAL_TOPOLOGY_CERTIFICATE`.

Delivered:

- exact finite event JSON Schema;
- separating and nonseparating transition catalogue;
- `D3` cap and discarded-component semantics;
- complete active-set and component-ancestry contract;
- finite-history derivation from bounded-interval finiteness plus extinction;
- backward connected-sum reconstruction theorem;
- `RP3#RP3` and bundle-factor normalization;
- non-circular simply connected terminal discharge;
- two positive and twelve malformed executable histories.

Canonical artifact:

- `campaigns/poincare_reconstruction/WP03_SURGERY_TOPOLOGY/00_README.md`

The certificate is conditional on the imported surgery and finite-extinction theorem interfaces.

### PC-WP04 — bounded certification substrate

Status: `KERNEL_CHECKED_BOUNDED_EVALUATOR_CERTIFICATE`.

Delivered:

- pinned Lean 4 and mathlib project;
- finite factor, reconstruction, event, event-contract, and history types;
- total backward evaluator;
- active-set coverage and exact-support theorems;
- explicit no-component-loss contract extraction;
- event- and history-level evaluator correctness conditional on `ImportedEventRelation`;
- chronological source-binding preservation;
- bounded terminal factor-profile elimination;
- repository replay of fourteen WP03 histories and adversarial certificate-policy mutations;
- rejection of `sorry` and local axioms.

Canonical artifacts:

- `campaigns/poincare_reconstruction/WP04_BOUNDED_CERTIFICATION/00_README.md`
- `fixtures/formal/PC-WP04/README.md`
- `fixtures/formal/PC-WP04/certificate_manifest.json`

The formalization is expression-level. It does not formalize manifold connected sums, van Kampen, Ricci-flow analysis, surgery existence, or finite extinction.

### PC-WP05 — integrated closure and source-concordance audit

Status: `REFEREE_PROMOTED_QUALIFIED_SOLVED_PROBLEM_ARCHIVE`.

Delivered:

- one dependency-complete WP00–WP04 dossier;
- Perelman/Morgan–Tian/Kleiner–Lott source-concordance audit;
- explicit Perelman II correction discipline;
- claim-level trust matrix;
- final category, orientation, boundary, and non-circularity audits;
- machine-readable dependency-closure and proof-debt registers;
- adversarial archival policy;
- bounded public archive note and publication manifest;
- Agent Council review and Referee closure decision.

Canonical artifacts:

- `campaigns/poincare_reconstruction/WP05_INTEGRATED_CLOSURE/00_README.md`
- `campaigns/poincare_reconstruction/WP05_INTEGRATED_CLOSURE/09_ARCHIVAL_MANIFEST.json`
- `docs/POINCARE_RECONSTRUCTION_ARCHIVE.md`

Publication disposition:

```text
READY_FOR_QUALIFIED_SOLVED_PROBLEM_ARCHIVAL_PUBLICATION
```

No theorem-strengthening stage is opened by this promotion.

## Three-pillar split

### MATHFORGE

- source discovery and edition control;
- false-proof and history-mutation atlases;
- reconstruction comparison;
- theorem-location and citation audit.

### MATHSOLVE

- theorem spine and proof-debt ownership;
- analytic theorem ledger;
- surgery and extinction reconstruction;
- pedagogical compression only after dependency closure.

### MATHCERT

- finite surgery-history representation;
- finite backward expression evaluation;
- provenance-bearing imported interfaces;
- bounded kernel-checked logic;
- no full-proof badge unless the analytic and manifold-level chains are actually formalized.

## Foundational profile

- Carrier: closed connected topological, PL, smooth, and Riemannian `3`-manifolds plus finite surgery histories and finite factor expressions.
- Ambient structures: algebraic topology, geometric topology, Riemannian geometry, nonlinear parabolic PDE, finite directed forests, connected sums, group free products, and proof-assistant datatypes.
- Classical base: standard classical mathematics.
- Witness policy: literature-derived complete proof; executable and kernel-checked certificates cover selected logical and combinatorial slices.
- Pathology risk: high at category changes, singular limits, surgery times, discarded components, source versions, event conservation, parser boundaries, and formalization claims.

## Claim boundary

The campaign does not claim:

- a new proof;
- independent verification of every Hamilton–Perelman estimate;
- equivalence of Poincaré with elliptization or geometrization;
- that extinction alone determines topology;
- that a schema-valid history proves the history exists;
- that the Lean evaluator proves the imported event relation;
- that the bounded Boolean factor profile formalizes van Kampen;
- that formalized implication interfaces certify their analytic assumptions;
- quotation-level or line-by-line source completeness where proof debt remains;
- a machine-checked proof of the Poincaré theorem;
- novelty or priority for any classical component.

## Archival state

`PC-001` enters archival maintenance after integration of `PC-WP05`.

Permitted maintenance includes citation repair, documentation preservation, CI upkeep, correction of overclaims, and bounded pedagogy that does not alter the claim surface.

A separate admission contract is required for:

- line-by-line source concordance;
- independent analytic verification;
- Top/PL/Diff formalization;
- manifold connected-sum and van Kampen formalization;
- verified JSON-to-Lean translation;
- Ricci-flow, surgery, or finite-extinction formalization;
- any full machine-checked Poincaré theorem claim.

No automatic theorem-strengthening stage remains authorized.