# PC-WP00 — Problem, source, equivalence, and non-circularity audit

**Audit date:** 2026-07-24  
**Campaign:** `PC-001`  
**Tracker:** `MATH-PROGRAMME#69`

## Audit determination

The Poincaré conjecture is a solved theorem. Perelman's 2002–2003 preprints complete the Hamilton Ricci-flow programme and establish the stronger geometrization theorem. The GCL campaign is therefore a solved-result reconstruction and certification campaign, not an open-problem attack.

## Canonical theorem registry

### `PC-TOP`

Every closed connected simply connected topological `3`-manifold is homeomorphic to `S³`.

### `PC-PL`

Every closed connected simply connected PL `3`-manifold is PL-homeomorphic to `S³`.

### `PC-DIFF`

Every closed connected simply connected smooth `3`-manifold is diffeomorphic to `S³`.

### `ELL`

Every closed connected `3`-manifold with finite fundamental group is a spherical space form `S³/Γ`, with `Γ` finite and acting freely and isometrically.

### `GEO`

Every closed orientable `3`-manifold admits the canonical decompositions and geometric pieces asserted by Thurston geometrization.

### `RF-EXT`

For the class covered by Perelman's finite-extinction theorem, a Ricci flow with surgery exists, becomes extinct in finite time, and its surgery history reconstructs the initial manifold as a connected sum of permitted spherical and sphere-bundle components.

## Convention and category audit

1. `closed` means compact without boundary.
2. Connectedness is explicit rather than convention-dependent.
3. A simply connected manifold is orientable through the orientation double cover.
4. Moise's dimension-three triangulation/Hauptvermutung theorem supplies the Top-to-PL bridge.
5. Compatible smoothing theory supplies the PL-to-Diff bridge.
6. A smooth paracompact manifold admits a smooth Riemannian metric.
7. Exact theorem extraction for items 4–5 remains `PC-D001` proof debt.

## Equivalence and implication matrix

Legend: `EQ` means equivalent through a named classical bridge; `=>` means one-way implication; `NO` means the converse is not supplied.

| From / To | `PC-TOP` | `PC-PL` | `PC-DIFF` | `ELL` | `GEO` | `RF-EXT` |
|---|---:|---:|---:|---:|---:|---:|
| `PC-TOP` | identity | `EQ` | `EQ` | `NO` | `NO` | `NO` |
| `PC-PL` | `EQ` | identity | `EQ` | `NO` | `NO` | `NO` |
| `PC-DIFF` | `EQ` | `EQ` | identity | `NO` | `NO` | `NO` |
| `ELL` | `=>` | `=>` | `=>` | identity | `NO` | `NO` |
| `GEO` | `=>` | `=>` | `=>` | `=>` | identity | `NO` |
| `RF-EXT` plus surgery ledger | `=>` | `=>` | `=>` | only after finite-group specialization | not by itself | identity |

### Category equivalence

`PC-DIFF => PC-TOP` follows by forgetting structure. The reverse implication requires the dimension-three category bridge before applying the smooth theorem. PL classification sits between them.

### Elliptization is stronger

Elliptization classifies all closed `3`-manifolds with finite fundamental group, including nontrivial finite groups. Poincaré treats only the trivial group.

### Geometrization is stronger

Geometrization treats all compact orientable `3`-manifolds and all Thurston geometries. Poincaré contains no corresponding classification of non-spherical pieces.

### Finite extinction is not equivalent

Finite extinction is a dynamical theorem over a broader topological class. It contributes to Poincaré only together with a precise surgery-topology ledger and terminal classification.

## Proof-route separation

### Route A

```text
GEO -> ELL -> PC-DIFF -> PC-TOP.
```

### Route B

```text
ELL -> S^3/Gamma -> pi_1(M)=Gamma -> Gamma=1 -> PC-DIFF -> PC-TOP.
```

### Route C

```text
Top/PL/Diff bridge
  -> smooth metric
  -> Ricci flow with surgery
  -> finite extinction
  -> connected-sum reconstruction
  -> van Kampen/free-product discharge
  -> PC-DIFF
  -> PC-TOP.
```

Route C is the primary Poincaré-specific reconstruction route.

## Source hierarchy

### Official status and statement

- Clay Mathematics Institute Poincaré status page.
- John Milnor, official Clay problem description.

### Primary proof sources

- Perelman, arXiv:`math/0211159`: entropy, reduced geometry, non-collapsing, and singularity analysis.
- Perelman, arXiv:`math/0303109`: Ricci flow with surgery.
- Perelman, arXiv:`math/0307245`: finite extinction for the no-aspherical-factor class.

### Detailed reconstructions

- Morgan–Tian, *Ricci Flow and the Poincaré Conjecture*.
- Kleiner–Lott, *Notes on Perelman's Papers*.
- Cao–Zhu, used with historical attribution and version caution.

### Foundational topology and geometry

- Moise and Munkres for category compatibility.
- Hamilton for precursor Ricci-flow theorems.
- Kneser–Milnor for prime decomposition.
- van Kampen for connected-sum fundamental groups.

## Audited headline theorem chain

Morgan–Tian supplies the following normalized interfaces:

1. surgery flow exists under the stated topological conditions;
2. surgery changes topology through explicit connected sums and permitted discarded components;
3. the flow becomes extinct under the stated group/topology hypothesis;
4. extinction plus the surgery history yields a connected sum of spherical space forms and sphere bundles;
5. the simply connected case reduces to `S³`.

These are audited theorem interfaces, not independently replayed proofs.

## Perelman correction discipline

Perelman's surgery preprint explicitly modifies or defers assertions sketched in the entropy preprint. Therefore:

1. source identities and versions must be recorded;
2. the first paper may not be copied without checking the second;
3. abandoned intermediate assertions may not be used to claim geometrization;
4. the Poincaré-specific route should avoid unnecessary dependence on long-time collapsing claims.

## Non-circularity audit

### Category bridge

Moise/Munkres predate Perelman and do not assume Poincaré.

### Orientability

The orientation-cover argument is independent of Poincaré.

### Prime decomposition

Kneser–Milnor existence and free-product behavior are safe imports. A proof may not identify an unknown simply connected prime factor with `S³` before completing the Ricci-flow argument.

### Extinction hypothesis

The simply connected case has no aspherical prime factor by topology and group theory, not by invoking Poincaré. Exact source normalization remains proof debt `PC-D006`.

### Spherical terminal factors

A spherical space form with trivial deck group is `S³` by the quotient definition. This does not invoke Poincaré.

### Terminal connected-sum argument

Van Kampen gives the free product of factor groups. Triviality of the total group excludes every `Z` factor and every nontrivial finite deck group. Connected sum with `S³` is neutral.

## Poincaré-specific hypothesis discharge

Let `M` be closed, connected, and simply connected.

1. `M` is orientable.
2. The dimension-three category bridge supplies a smooth structure and metric.
3. The cited surgery theorem applies under its normalized topological hypotheses.
4. The simply connected case satisfies the finite-extinction class without Poincaré.
5. The surgical flow becomes extinct.
6. The surgery history gives a connected sum of spherical space forms and sphere bundles.
7. Van Kampen gives a free product of factor groups.
8. Triviality of `pi_1(M)` eliminates all nontrivial factors.
9. Remaining spherical factors are `S³`.
10. Therefore `M` is diffeomorphic, hence homeomorphic, to `S³`.

Steps 3–6 remain imported theorem interfaces. Steps 1–2 and 7–10 are initial formalization candidates.

## Claim boundary

Supported by WP00:

- solved status;
- exact theorem formulations;
- category-equivalence interface;
- implication hierarchy;
- direct finite-extinction proof spine;
- terminal topology argument conditional on the connected-sum classification.

Not supported by WP00 alone:

- line-by-line verification of Perelman's estimates;
- independent construction of canonical neighbourhoods or surgery;
- independent proof of finite extinction;
- full formalization of the analytic core;
- novelty or priority claims.

## Audit disposition

`PC-WP00` passes the source, equivalence, and non-circularity gate with explicit proof debt. `PC-WP01` and `PC-WP02` may proceed in parallel. `PC-WP03` remains closed until their integration and Referee review.