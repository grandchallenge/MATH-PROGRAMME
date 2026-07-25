# PC-WP00 — Source, normalization, equivalence, and non-circularity audit

## Metadata

- Domain: Poincaré theorem and Hamilton–Perelman reconstruction
- Campaign: `PC-001`
- Work Package: `PC-WP00`
- Tracker: `MATH-PROGRAMME#69`
- Result status: `SOLVED_CLASSICAL_THEOREM`
- Promotion state: `WP00_PROMOTED_WP01_WP02_PERMITTED`
- Global target advanced: `PC-T017`
- Claim posture: literature reconstruction and selective certification; no new-proof claim

## Result-status box

| Field | Value |
|---|---|
| Mathematical status | Solved classical theorem |
| Canonical target | Every closed connected simply connected topological `3`-manifold is homeomorphic to `S³` |
| Smooth target | Every closed connected simply connected smooth `3`-manifold is diffeomorphic to `S³` |
| Primary route | Ricci flow with surgery, finite extinction, and topology bookkeeping |
| Stronger routes | Elliptization and geometrization |
| Certification state | WP00 logic/source audit promoted; analytic imports unformalized |
| Next work | WP01 false-proof atlas and WP02 theorem ledger in parallel |

## Foundational profile

```yaml
foundational_profile:
  carrier_type: closed_connected_three_manifolds
  ambient_structure:
    - topological_manifold
    - piecewise_linear_manifold
    - smooth_manifold
    - riemannian_manifold
    - fundamental_group
    - ricci_flow_with_surgery
    - finite_surgery_history
  axiom_profile:
    base: classical_mathematics
    excluded_middle: used
    large_cardinal_usage: none
  witness_policy:
    existence_claim: literature_derived_complete_proof
    witness_location: Perelman_preprints_and_detailed_reconstructions
  certification_target:
    - human_source_audit
    - terminal_topology_formalization
    - surgery_history_certificate_validator
    - provenance_bearing_analytic_interfaces
  pathology_risk:
    level: high
    notes: category changes, singular limits, surgery bookkeeping, discarded components, and compressed analytic arguments
```

## The object

A closed `3`-manifold is compact, has no boundary, and locally looks like ordinary `3`-space. The theorem asks whether triviality of every loop up to contraction forces the entire manifold to be the `3`-sphere.

The canonical statement is

```math
\forall M,
\quad
\bigl(M\text{ closed connected topological }3\text{-manifold}
\land \pi_1(M)=1\bigr)
\Longrightarrow
M\cong_{\mathrm{Top}}S^3.
```

## The obstruction

The equation

```math
\partial_t g=-2\operatorname{Ric}(g)
```

smooths geometry only while the flow remains regular. General metrics develop curvature singularities. A valid proof therefore requires quantitative non-collapsing, blow-up compactness, singularity models, canonical neighbourhoods, controlled surgery, topology accounting, and finite extinction.

The programme target is not the slogan “Ricci flow rounds the manifold.” It is the exact chain

```text
category bridge
  -> smooth metric
  -> controlled singularities
  -> surgery continuation
  -> finite extinction
  -> connected-sum classification
  -> simple-connectivity discharge.
```

## Category audit

- `closed` means compact without boundary;
- connectedness is explicit rather than hidden in a convention for simple connectivity;
- simple connectivity implies orientability through the orientation double cover;
- Moise-type triangulation/Hauptvermutung and compatible smoothing results bridge the topological, PL, and smooth categories in dimension three;
- a smooth paracompact manifold admits a Riemannian metric.

The category bridge remains an imported theorem interface until exact source extraction is complete.

## Route hierarchy

### Full geometrization

```text
geometrization -> elliptization -> Poincare.
```

### Elliptization

```text
M = S^3/Gamma, pi_1(M)=Gamma, pi_1(M)=1 -> Gamma=1 -> M=S^3.
```

### Finite-extinction route

```text
Ricci flow with surgery
  + finite extinction
  + surgery topology ledger
  -> connected sum of spherical space forms and sphere bundles
  -> trivial free product of factor groups
  -> only S^3 factors remain
  -> M=S^3.
```

Poincaré does not imply elliptization or geometrization. Finite extinction does not imply the topological conclusion without the surgery ledger.

## Source hierarchy

### Primary sources

1. Perelman, *The entropy formula for the Ricci flow and its geometric applications*, arXiv:`math/0211159`.
2. Perelman, *Ricci flow with surgery on three-manifolds*, arXiv:`math/0303109`.
3. Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds*, arXiv:`math/0307245`.

### Detailed reconstructions

4. Morgan–Tian, *Ricci Flow and the Poincaré Conjecture*.
5. Kleiner–Lott, *Notes on Perelman's Papers*.
6. Cao–Zhu, used with attribution and version-history caution.

### Foundational imports

7. Moise and Munkres for the dimension-three category bridge.
8. Hamilton for precursor Ricci-flow theory.
9. Kneser–Milnor and van Kampen for terminal topology.
10. Milnor and Clay for the canonical statement and official status.

## Theorem-spine slice

| Node | Statement | WP00 status |
|---|---|---|
| `PC-D000` | category and connectivity conventions | closed |
| `PC-L001` | Top/PL/Diff bridge | audited import; extraction pending |
| `PC-L002` | simple connectivity implies orientability | closed |
| `PC-L003` | smooth metric exists | standard import |
| `PC-L004` | short-time Ricci flow | source normalization pending |
| `PC-L005` | entropy/reduced geometry/non-collapsing | source normalization pending |
| `PC-L006` | canonical neighbourhoods | source normalization pending |
| `PC-L007` | surgery flow exists | headline theorem audited |
| `PC-L008` | topology of surgery/discarded components | headline theorem audited |
| `PC-L009` | simply connected case lies in extinction class | audit expansion pending |
| `PC-L010` | finite-time extinction | headline theorem audited |
| `PC-L011` | extinct history yields connected-sum classification | interface audited |
| `PC-L012` | trivial group eliminates nontrivial factors | proved in package |
| `PC-C013` | smooth Poincaré conclusion | classical theorem |
| `PC-C014` | topological Poincaré conclusion | classical theorem |
| `PC-T017` | source-complete reconstruction | advanced; incomplete |

## Terminal connected-sum discharge

Assume the imported surgery/extinction theorem gives a connected-sum expression built from spherical space forms and `S²`-bundles over `S¹`. Van Kampen identifies the fundamental group as the free product of the factor groups. If the total group is trivial, every factor group is trivial. Hence no sphere-bundle factor occurs, every spherical deck group is trivial, every spherical factor is `S³`, and connected sum with `S³` is neutral. Therefore the manifold is `S³`.

This argument does not assume Poincaré for an unknown prime factor; it uses only the quotient definition of a spherical space form and the imported surgery classification.

## Trust quartet

### Proved in WP00

- implication/equivalence logic;
- orientability consequence;
- terminal factor elimination conditional on the connected-sum classification;
- explicit claim and formalization boundaries.

### Checked

- official solved status;
- canonical theorem statement;
- identities and roles of the three Perelman preprints;
- Morgan–Tian headline surgery/extinction/classification chain;
- existence of the classical category bridge.

### Remaining reconstruction debt

- theorem-level category source extraction;
- exact Perelman/Morgan–Tian/Kleiner–Lott crosswalk;
- parameter hierarchy for canonical neighbourhoods and surgery;
- topology of every surgery/discarded component;
- finite-extinction proof ledger.

### External verification boundary

The analytic Hamilton–Perelman core remains a provenance-bearing literature import until individually reconstructed or formalized.

## Failure analysis

The tempting route “run Ricci flow until the manifold becomes round” fails because curvature may blow up in finite time. Short-time existence and smoothing intuition do not cross singularities. The viable route requires Perelman's non-collapsing, singularity control, canonical neighbourhoods, surgery, and extinction machinery.

## Certification handoff

The first MATHCERT slice is finite and algebraic/combinatorial:

1. represent permitted terminal factors and a finite surgery history;
2. validate component ancestry, splits, removals, and extinction;
3. reconstruct the factor expression;
4. interpret connected sum as a free-product expression through an explicit imported interface;
5. prove that trivial total group eliminates all nontrivial factors.

No formal artifact may claim a full formal proof while Ricci-flow and surgery theorems remain imported.

## Claim boundary

WP00 does not claim:

- a new proof;
- independent verification of the major analytic estimates;
- equivalence of Poincaré with elliptization or geometrization;
- topology from extinction without surgery bookkeeping;
- formal certification of an imported theorem;
- novelty for any classical component.

## Exit gate

WP00 is promoted as the source/equivalence foundation. `PC-WP01` and `PC-WP02` may proceed in parallel. `PC-WP03` remains closed until their adversarial review and cross-document integration.