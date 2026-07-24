# PC-WP00 — Source, normalization, equivalence, and non-circularity audit

## Metadata

- Domain: Poincaré theorem and Hamilton–Perelman reconstruction
- Campaign: `PC-001`
- Work Package: `PC-WP00`
- Canonical tracker: `MATH-PROGRAMME#69`
- Primary type: solved-result status spine, source audit, equivalence map, and proof-route normalization
- Global theorem-spine node advanced: `PC-T017`
- Incoming dependencies: dimension-three category equivalence; Hamilton–Perelman Ricci-flow theory; prime decomposition; van Kampen theorem
- Claim status: classical theorem solved; WP00 proves only local logical bridges and source-normalization claims
- Certification target: human audit followed by selective theorem-prover and certificate formalization
- Foundational profile: present
- Promotion state: `WP00_PROMOTED_WP01_WP02_PERMITTED`

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | `SOLVED CLASSICAL THEOREM / WP00 PROMOTED` |
| Conditional on | Standard dimension-three category theorems and the cited Hamilton–Perelman proof chain |
| Strongest supported claim | The topological Poincaré statement, smooth Poincaré statement, and PL statement are equivalent in dimension three; the Hamilton–Perelman finite-extinction route proves the smooth statement; elliptization and geometrization are strict stronger routes |
| Not claimed | A new proof, independent re-verification of the full analytic core, or equivalence of Poincaré with elliptization/geometrization |
| Support-route class | `PRIMARY_SOURCE_AUDIT`, `LITERATURE_RECONSTRUCTION`, `CONTINUUM_PROOF_INTERFACE`, `FORMALIZATION_HANDOFF` |
| Foundational profile | Present below and in the master plan |
| Certification state | WP00 source/equivalence layer audited; analytic imports remain unformalized literature interfaces |
| First executable step | Run WP01 false-proof atlas and WP02 source-normalized theorem ledger in parallel |

## 2. Foundational profile

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
  regularity:
    - topological
    - PL
    - smooth
    - time_dependent_riemannian_metric_away_from_surgery_times
  axiom_profile:
    base: classical_ZFC_style_mathematics
    choice_usage: ordinary_manifold_and_analysis_usage
    excluded_middle: used
    large_cardinal_usage: none
    determinacy_usage: none
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
    notes: category changes, singular limits, surgery bookkeeping, discarded components, and compressed analytic arguments are the principal semantic risks
```

## 3. Lay executive companion

### The object

A closed `3`-manifold is a space that locally looks like ordinary three-dimensional space, has no boundary, and is compact. The theorem asks whether the absence of non-contractible loops forces the entire space to be the `3`-sphere.

### The obstruction

A metric can be smoothed by Ricci flow only until curvature concentrates. Singularities are not incidental defects; they encode the topological decomposition. The proof must show that singular regions have controlled standard forms, cut them without losing the topological ledger, continue the flow, and interpret eventual extinction.

### The reconstruction target

The programme target is not the slogan “Ricci flow rounds the manifold.” It is the exact chain:

```text
category bridge
  -> smooth metric
  -> controlled singularities
  -> surgery continuation
  -> finite extinction
  -> connected-sum classification
  -> simple-connectivity discharge.
```

### What this package achieved

- corrected the campaign status from conjectural to solved;
- fixed the topological and smooth theorem statements;
- separated equivalences from stronger implications;
- identified the direct finite-extinction proof route;
- recorded the source hierarchy and source debts;
- exposed the terminal topology argument;
- opened the next two controlled work packages.

### What this package did not achieve

- it did not reproduce every analytic proof;
- it did not independently certify Perelman's preprints;
- it did not formalize Ricci flow with surgery;
- it did not compress the proof into an informal “rounding” argument.

## 4. Formal problem statement

### Definitions and notation

- `M` is a Hausdorff, second-countable `3`-manifold.
- `closed` means compact and boundaryless.
- `simply connected` means path-connected with trivial fundamental group.
- `S³={x in R⁴ : ||x||=1}`.
- `M ≅_Top N`, `M ≅_PL N`, and `M ≅_Diff N` denote homeomorphism, PL homeomorphism, and diffeomorphism.

### Exact target statement

```math
\forall M,
\quad
\bigl(M\text{ closed connected topological }3\text{-manifold}
\land \pi_1(M)=1\bigr)
\Longrightarrow
M\cong_{\mathrm{Top}}S^3.
```

### Smooth formulation

```math
\forall M,
\quad
\bigl(M\text{ closed connected smooth }3\text{-manifold}
\land \pi_1(M)=1\bigr)
\Longrightarrow
M\cong_{\mathrm{Diff}}S^3.
```

### Category correspondence

In dimension three, Moise's triangulation/Hauptvermutung theorem and compatible smoothing theory identify the topological, PL, and smooth classification problems. This is an imported classical bridge and must remain visible in the theorem DAG.

## 5. Object and obstruction

The smallest conceptual obstruction is the existence of singularities under Ricci flow.

For a smooth metric `g(t)`, Ricci flow obeys

```math
\partial_t g(t)=-2\operatorname{Ric}(g(t)).
```

If the flow stayed smooth and converged after rescaling to a constant-positive-curvature metric, the conclusion would be comparatively direct. General metrics can instead develop unbounded curvature. The proof therefore needs all of the following, not merely the differential equation:

1. a non-collapsing theorem at curvature scales;
2. compactness of blow-up sequences;
3. classification/control of ancient singularity models;
4. canonical neighbourhoods at high curvature;
5. surgery parameters and persistence estimates;
6. topological accounting for every cut, cap, and discarded component;
7. a finite-extinction theorem in the relevant topological class.

## 6. Known terrain and source audit

| Source or result | Claim used here | Audit state | Spine dependency |
|---|---|---|---|
| Clay status page | Poincaré is solved; Perelman proved geometrization | audited 2026-07-24 | result status |
| Milnor official problem description | canonical topological statement and category warning | audited | `PC-D000`, `PC-L001` |
| Moise 1952 | triangulation and dimension-three Hauptvermutung | source identified; theorem extraction pending WP02-topology lane | `PC-L001` |
| Munkres 1960 / Moise 1977 | smoothing/category compatibility | source identified; exact formulation pending | `PC-L001` |
| Hamilton 1982 | positive-Ricci-curvature Ricci-flow model case | metadata audited | historical dependency |
| Perelman `math/0211159` | entropy, reduced geometry, non-collapsing, singularity control | primary source identified; theorem ledger pending | `PC-L005`, `PC-L006` |
| Perelman `math/0303109` | Ricci flow with surgery | primary source identified; theorem ledger pending | `PC-L007`, `PC-L008` |
| Perelman `math/0307245` | finite extinction for no-aspherical-factor class | abstract and hypothesis audited; full theorem ledger pending | `PC-L009`, `PC-L010` |
| Morgan–Tian 2007 | detailed complete Poincaré proof and terminal classification | theorem statements audited | `PC-L007`–`PC-C014` |
| Kleiner–Lott 2008 | independent detailed reconstruction/comparison | source identified; crosswalk pending | analytic ledger |
| Kneser–Milnor decomposition | prime decomposition and connected-sum framework | standard import; exact source normalization pending | `PC-L009`, `PC-L011` |
| van Kampen theorem | fundamental group of connected sum is free product | standard import | `PC-L012` |

## 7. Claim ledger summary and trust quartet

### Claim ledger summary

| Claim ID | Statement | Status | Evidence | Certification state |
|---|---|---|---|---|
| `PC-WP00-C001` | The Poincaré conjecture is a solved theorem | audited | Clay status and proof literature | external status audited |
| `PC-WP00-C002` | Topological, PL, and smooth formulations are equivalent in dimension three | audited with source-extraction debt | Moise/Munkres/Morgan–Tian | unformalized import |
| `PC-WP00-C003` | Geometrization implies elliptization, which implies Poincaré | checked implication | standard route and Milnor description | human-audited logic |
| `PC-WP00-C004` | The converse implications are not supplied by Poincaré | checked semantic boundary | quantifier/strength comparison | human-audited logic |
| `PC-WP00-C005` | Surgery existence + topology ledger + finite extinction imply the Poincaré conclusion | audited theorem interface | Morgan–Tian Theorems 0.1, 0.3, 0.4, 18.1 | analytic imports unformalized |
| `PC-WP00-C006` | The terminal free-product argument eliminates all nontrivial factors under simple connectivity | proved in package at theorem-interface level | van Kampen plus space-form definitions | formalization candidate |
| `PC-WP00-C007` | WP00 proves no new Poincaré theorem | audited | package claim boundary | enforced |

### What is proved?

Within WP00, the logical implication matrix and the terminal factor-elimination argument are proved at ordinary mathematical exposition level, conditional on named classical and analytic imports.

### What is checked?

The official solved status, canonical theorem statement, Perelman paper identities and abstracts, Morgan–Tian headline theorem chain, and the route distinctions are checked against primary or canonical sources.

### What remains open?

No mathematical part of the Poincaré theorem remains open. Programme reconstruction debts remain: exact theorem extraction, parameter dependencies, source crosswalks, surgery bookkeeping, and formalization.

### What requires external verification?

Every imported analytic theorem, the precise category-equivalence formulation, and the detailed Kneser–Milnor hypothesis bridge remain external until reconstructed or formalized.

## 8. Theorem-spine slice and dependency DAG

| Node ID | Role | Statement | Status | Dependencies | Discharge criterion |
|---|---|---|---|---|---|
| `PC-D000` | definition | category and connectivity conventions | closed | none | canonical definitions committed |
| `PC-L001` | category bridge | Top/PL/Diff classification equivalence in dimension three | imported/audited | Moise, Munkres | exact theorem statements cross-referenced |
| `PC-L002` | topology lemma | simply connected closed manifold is orientable | closed | orientation cover | elementary proof or formalization |
| `PC-L003` | geometry bridge | compatible smooth manifold admits a Riemannian metric | closed import | partition of unity | standard formal source |
| `PC-L005` | analytic interface | Perelman non-collapsing/reduced-geometry control | imported | Ricci flow | source-normalized theorem ledger |
| `PC-L006` | singularity interface | high-curvature regions have canonical neighbourhoods | imported | `PC-L005` | source-normalized theorem ledger |
| `PC-L007` | surgery interface | flow with surgery exists with controlled parameters | imported | `PC-L006` | exact source and parameter hierarchy |
| `PC-L008` | topology interface | surgery changes topology by recorded connected sums/removals | imported/audited | `PC-L007` | explicit surgery ledger |
| `PC-L009` | hypothesis bridge | simply connected case lies in finite-extinction class | audited with topology debt | prime decomposition | exact proof and sources |
| `PC-L010` | extinction interface | surgical flow becomes extinct in finite time | imported/audited | `PC-L007`, `PC-L009` | source-normalized proof ledger |
| `PC-L011` | classification bridge | extinction history yields connected sum of spherical space forms and sphere bundles | imported/audited | `PC-L008`, `PC-L010` | explicit induction ledger |
| `PC-L012` | terminal topology | trivial fundamental group eliminates every nontrivial factor | closed | van Kampen | formal proof candidate |
| `PC-C013` | smooth conclusion | `M ≅_Diff S³` | classical theorem | `PC-L001`–`PC-L012` | full reconstruction |
| `PC-C014` | topological conclusion | `M ≅_Top S³` | classical theorem | `PC-C013`, `PC-L001` | full reconstruction |

This package advances `PC-T017` by fixing the global proof graph and preventing stronger theorem routes from being mislabeled as equivalences.

## 9. Proofs and classified computations

### Support route: terminal connected-sum discharge

- pedagogical class: `CONTINUUM_PROOF` at elementary topology level;
- input: a connected-sum decomposition into spherical space forms and `S²`-bundles over `S¹`;
- operation: apply van Kampen to obtain a free product of factor fundamental groups;
- conclusion: if the total fundamental group is trivial, every factor group is trivial; no `S²`-bundle factor occurs; every spherical space-form factor has trivial deck group and is `S³`; a connected sum of copies of `S³` is `S³`;
- claim supported: `PC-WP00-C006`;
- limitation: the decomposition itself is imported from the surgery/extinction theorem chain.

No numerical computation is relevant to WP00.

## 10. Failure and negative-result analysis

### Attempted route

“Run Ricci flow until the manifold becomes round.”

### Why it was plausible

Ricci flow smooths curvature in favorable cases, and Hamilton proved convergence for positive Ricci curvature.

### Smallest exact obstruction

For a general initial metric, curvature can become unbounded in finite time. The smooth flow then ceases to exist in its original form, so convergence cannot be asserted without singularity analysis and surgery.

### What the obstruction rules out

It rules out every proof that uses only short-time existence, curvature diffusion intuition, or the positive-curvature model case.

### What remains viable

Perelman's quantitative singularity analysis, canonical neighbourhood theorem, controlled surgery, and finite-extinction argument.

## 11. Proof-debt register

See `09_PROOF_DEBT.json`. The blocking debts for WP02 are:

- exact dimension-three category theorem extraction;
- exact Perelman-to-Morgan–Tian theorem crosswalk;
- surgery parameter hierarchy;
- topology of discarded components;
- no-aspherical-factor/group-hypothesis equivalence;
- finite-extinction mechanism ledger.

None of these debts changes the solved status of the theorem. They determine whether the GCL reconstruction is source-complete.

## 12. Certification boundary and MATHCERT handoff

### Pencil-and-paper claims

- category and route implication logic;
- orientability consequence;
- terminal free-product factor elimination;
- finite surgery-history induction once the surgery theorem interface is assumed.

### Machine-checked or replayed claims

None in WP00.

### Exact certificate candidates

- finite rooted forest encoding surgery-time component ancestry;
- local rewrite rules for connected-sum decomposition and component removal;
- validator proving that an extinct history with permitted terminal component types reconstructs the initial connected-sum class;
- terminal fundamental-group discharge.

### Formalization blockers

- mature formal libraries for topological and smooth manifolds in dimension three;
- connected sum and fundamental groups;
- diffeomorphism-level category bridge;
- geometric analysis and Ricci flow infrastructure.

### First item for MATHCERT

Formalize a finite algebraic surrogate of the terminal topology argument: a list/tree of factors labeled by finite groups or `Z`, together with a proof that trivial free product forces every label trivial. Keep the geometric realization theorem as an explicit imported interface.

## 13. First executable step

- Input: WP00 source hierarchy, equivalence matrix, theorem DAG, and proof debt.
- Operation: execute WP01 and WP02 in parallel.
- Output artifact: exact false-proof fixtures and a source-normalized Hamilton–Perelman theorem ledger.
- Completion test: a specialist can identify every hidden assumption in a compressed Poincaré proof and locate the source/interface for every analytic step.
- Spine node advanced: `PC-T017`; debts discharged: `PC-D001` through `PC-D006` as assigned.

## 14. Escalation gate

- [x] The theorem-spine slice has been audited.
- [x] All dependency families are named.
- [x] The proof-debt register is current.
- [x] The trust quartet is complete.
- [x] The foundational profile is present.
- [x] The first executable step is explicit.
- [x] The next packages name the nodes they advance.
- [x] The solved/open status distinction is explicit.
- [x] Stronger routes are not mislabeled as equivalences.

WP00 is promoted as a source-and-equivalence foundation. This promotion certifies the campaign architecture, not the full analytic proof.