# PC-WP00 — Problem, source, equivalence, and non-circularity audit

**Audit date:** 2026-07-24  
**Campaign:** `PC-001`  
**Canonical tracker:** `MATH-PROGRAMME#69`

## 1. Audit determination

The Poincaré conjecture is a solved theorem. The canonical topological statement is established by the Hamilton–Perelman Ricci-flow programme, with Perelman's three 2002–2003 preprints as the primary proof sources and later detailed reconstructions supplying expanded arguments.

The GCL challenge is therefore normalized as a solved-result reconstruction and certification campaign. Any artifact that calls the theorem open, proposes numerical evidence for it, or treats the programme as a novelty race fails the status gate.

## 2. Canonical theorem registry

### PC-TOP — topological formulation

Let `M` be a closed, connected topological `3`-manifold. If `pi_1(M)=1`, then `M` is homeomorphic to `S³`.

### PC-PL — piecewise-linear formulation

Let `M` be a closed, connected PL `3`-manifold. If `pi_1(M)=1`, then `M` is PL-homeomorphic to `S³`.

### PC-DIFF — smooth formulation

Let `M` be a closed, connected smooth `3`-manifold. If `pi_1(M)=1`, then `M` is diffeomorphic to `S³`.

### ELL — elliptization / spherical space-form formulation

Every closed, connected `3`-manifold with finite fundamental group is diffeomorphic to a spherical space form `S³/Gamma`, for a finite group `Gamma` acting freely and isometrically on the round `3`-sphere.

### GEO — geometrization formulation

Every closed orientable `3`-manifold admits the canonical prime and torus decompositions into pieces carrying one of Thurston's eight model geometries, with the usual qualifications and uniqueness statements.

### RF-EXT — finite-extinction classification formulation

For the topological class covered by the finite-extinction theorem, a Ricci flow with surgery exists for all positive time, becomes extinct in finite time, and its surgery history reconstructs the initial manifold as a connected sum of spherical space forms and `S²`-bundles over `S¹` (including the orientability-dependent alternatives in the general statement).

## 3. Category and convention audit

### 3.1 Connectedness

Some definitions include path-connectedness in “simply connected.” The campaign states connectedness explicitly to avoid convention-dependent vacuity for disconnected manifolds.

### 3.2 Boundary

The theorem concerns manifolds without boundary. A compact simply connected `3`-manifold with boundary need not be `S³`; the `3`-ball is the immediate counterexample to any boundary-suppressed formulation.

### 3.3 Orientability

A connected non-orientable manifold has a nontrivial orientation double cover and an associated nontrivial homomorphism from its fundamental group to `Z/2`. Hence a simply connected manifold is orientable. This discharges orientability in the Poincaré case but not in the general surgery theorem.

### 3.4 Topological to PL

Moise's dimension-three triangulation theorem gives a compatible PL structure on every topological `3`-manifold, and the dimension-three Hauptvermutung gives uniqueness at the classification level. The exact theorem wording and noncompact qualifications remain a source-extraction debt, but the closed case needed here is standard.

### 3.5 PL to smooth

Compatible smoothing theory identifies PL and smooth `3`-manifold classification. Morgan–Tian explicitly work in the smooth category and note that topological and smooth classification in dimension three are equivalent.

### 3.6 Smooth metric

Every smooth paracompact manifold admits a smooth Riemannian metric by partition of unity. Compactness permits normalization by a global rescaling without changing topology.

## 4. Equivalence and implication matrix

Legend:

- `EQ`: equivalent after named classical bridge;
- `=>`: one-way implication;
- `NO`: converse not supplied and false as a logical equivalence of theorem strengths;
- `BRIDGE`: implication requires an external theorem explicitly named below.

| From / To | `PC-TOP` | `PC-PL` | `PC-DIFF` | `ELL` | `GEO` | `RF-EXT` |
|---|---:|---:|---:|---:|---:|---:|
| `PC-TOP` | identity | `EQ/BRIDGE` | `EQ/BRIDGE` | `NO` | `NO` | `NO` |
| `PC-PL` | `EQ/BRIDGE` | identity | `EQ/BRIDGE` | `NO` | `NO` | `NO` |
| `PC-DIFF` | `EQ/BRIDGE` | `EQ/BRIDGE` | identity | `NO` | `NO` | `NO` |
| `ELL` | `=>` | `=>/BRIDGE` | `=>` | identity | `NO` | `NO` |
| `GEO` | `=>` | `=>/BRIDGE` | `=>` | `=>` | identity | `NO` |
| `RF-EXT` | `=>` | `=>/BRIDGE` | `=>` | only with finite-group specialization | not by itself | identity |

### 4.1 Why `PC-TOP`, `PC-PL`, and `PC-DIFF` are equivalent

- `PC-DIFF => PC-TOP` is immediate by forgetting smooth structure.
- `PC-TOP => PC-DIFF` requires the dimension-three category bridge: smooth the input, apply the smooth theorem, and use the category equivalence to interpret the result.
- The PL statements sit between them through compatible triangulation and smoothing.

### 4.2 Why elliptization is stronger

Elliptization classifies every closed `3`-manifold with finite fundamental group, not merely those with trivial group. Setting `Gamma=1` gives Poincaré. The Poincaré theorem contains no classification of nontrivial finite fundamental groups and therefore does not imply elliptization.

### 4.3 Why geometrization is stronger

Geometrization classifies all compact orientable `3`-manifolds after canonical decompositions. Its spherical finite-group case yields elliptization, hence Poincaré. Poincaré alone says nothing about hyperbolic, Seifert, Sol, or the other geometric pieces.

### 4.4 Why finite extinction is not equivalent to Poincaré

Finite extinction is a dynamical statement about a surgery flow and a broader topological class. Poincaré does not construct such a flow or imply its extinction. Conversely, extinction contributes to Poincaré only after the surgery-topology ledger is imported.

## 5. Proof-route separation

### Route A: `GEO => ELL => PC-DIFF => PC-TOP`

Required bridges:

1. geometrization identifies a finite-fundamental-group prime manifold as spherical;
2. a spherical manifold is `S³/Gamma`;
3. `pi_1(M)` identifies with the deck group `Gamma`;
4. trivial fundamental group gives `Gamma=1`;
5. category bridge gives the topological statement.

Status: valid, stronger than needed, and not the primary pedagogical route.

### Route B: `ELL => PC-DIFF => PC-TOP`

Required bridges:

1. elliptization theorem;
2. universal-cover/deck-group description of spherical space forms;
3. category bridge.

Status: valid and concise, but hides the proof mechanisms delivered by Ricci flow.

### Route C: `RF-EXT + surgery ledger => PC-DIFF => PC-TOP`

Required bridges:

1. smooth structure and initial Riemannian metric;
2. Ricci flow with surgery existence;
3. finite extinction for the simply connected case;
4. topological description of every surgery and discarded component;
5. induction reconstructing the initial connected sum;
6. van Kampen/free-product terminal discharge;
7. category bridge.

Status: canonical Poincaré-specific reconstruction route.

## 6. Source hierarchy and exact use

### S0 — official status and statement

- Clay Mathematics Institute, Poincaré Conjecture page: official solved status and overview.
- John Milnor, *The Poincaré Conjecture*: canonical problem description, historical false starts, category comparison, elliptization relation, and Hamilton overview.

### S1 — primary Hamilton–Perelman sources

- `PER-1`: arXiv:`math/0211159`, entropy/reduced-geometry/non-collapsing and geometric applications.
- `PER-2`: arXiv:`math/0303109`, construction of Ricci flow with surgery and corrections to claims from `PER-1`.
- `PER-3`: arXiv:`math/0307245`, finite extinction for closed oriented `3`-manifolds whose prime decomposition has no aspherical factors.

These sources are primary. Their compressed presentation does not permit WP00 to label every downstream lemma independently rechecked.

### S2 — detailed complete reconstruction

- Morgan–Tian, *Ricci Flow and the Poincaré Conjecture*.

Audited headline statements:

- Theorem 0.1: classification for fundamental group a free product of finite groups and infinite cyclic groups.
- Corollary 0.2: closed simply connected `3`-manifold is diffeomorphic to `S³`.
- Theorem 0.3: existence of Ricci flow with surgery and topological description of surgery changes under the stated `RP²` condition.
- Theorem 0.4: finite extinction under the stated group hypothesis.
- Theorem 18.1: detailed finite-extinction theorem and terminal deduction.

### S3 — independent reconstruction/cross-check

- Kleiner–Lott, *Notes on Perelman's Papers*.
- Cao–Zhu, Hamilton–Perelman proof exposition, used only with attribution and version-history caution.

### S4 — category and topology sources

- Moise 1952 and 1977 for dimension-three triangulation/Hauptvermutung.
- Munkres 1960 for smoothing compatibility.
- Kneser–Milnor for prime decomposition.
- van Kampen for connected-sum fundamental groups.

### S5 — Hamilton precursor sources

- Hamilton 1982 for positive Ricci curvature and convergence.
- Hamilton 1995 for singularity formation.
- Hamilton 1999 for nonsingular long-time solutions and geometrization programme context.

## 7. Perelman source corrections that must remain visible

Perelman's surgery paper explicitly states that it continues the entropy paper and notes two exceptions to assertions sketched earlier: one collapsing theorem was deferred, and one lower-volume/smoothness claim was unjustified and unnecessary for the remaining conclusions.

Therefore:

1. the campaign must use versioned paper identities;
2. claims from the first preprint cannot be copied without checking whether the second modifies them;
3. no proof ledger may infer full geometrization from an abandoned intermediate assertion;
4. the Poincaré-specific finite-extinction route should avoid unnecessary dependence on long-time collapsing analysis.

## 8. Non-circularity audit

### 8.1 Category bridge

Moise/Munkres predate Perelman and do not assume Poincaré. Safe import.

### 8.2 Orientability

The orientation-cover argument is elementary and independent of Poincaré. Safe.

### 8.3 Prime decomposition

Kneser–Milnor decomposition predates Perelman. The exact form used must be checked to ensure no step identifies a simply connected prime factor with `S³` before the Ricci-flow conclusion. Existence of the decomposition and free-product behavior are safe; classification of simply connected prime factors would be circular.

### 8.4 No-aspherical-factor hypothesis

For a simply connected closed `3`-manifold, an aspherical prime factor is excluded by the free-product decomposition and the fact that a closed aspherical manifold has nontrivial fundamental group. This argument must not use Poincaré.

### 8.5 Surgery topology

The surgery theorem may classify discarded components as spherical space forms or sphere bundles. A spherical space form with trivial group is `S³` by its quotient definition, not by invoking Poincaré. Safe if stated this way.

### 8.6 Terminal connected-sum argument

Use van Kampen and the deck groups of spherical space forms. Do not insert “each simply connected summand is `S³`” as an independent premise; that would be the target theorem.

### 8.7 Geometrization route

When the full geometrization theorem is imported as Perelman's result, Poincaré follows as a corollary. This is not circular. However, using Poincaré to establish the spherical prime case inside a purported proof of geometrization and then deriving Poincaré is circular.

## 9. Poincaré-specific hypothesis discharge

Let `M` be closed, connected, and simply connected.

1. `M` is orientable by the orientation-cover argument.
2. Smooth `M` contains no embedded locally separating `RP²` of the type excluded in the surgery-existence theorem, because orientability supplies the required condition in the cited reconstruction.
3. `pi_1(M)=1` is a free product of zero nontrivial finite or infinite cyclic factors, so it satisfies Morgan–Tian's group hypothesis.
4. Equivalently, its prime decomposition has no aspherical factors; this bridge is recorded for exact topology-source audit.
5. The surgical flow therefore exists and becomes extinct.
6. The surgery history yields a connected sum of spherical space forms and sphere bundles.
7. Van Kampen gives a free product of factor groups.
8. Triviality of the total group excludes every `Z` factor and every nontrivial finite deck group.
9. Remaining spherical factors are `S³`; connected sum with `S³` is neutral.
10. Hence `M` is diffeomorphic to `S³`, and therefore homeomorphic to `S³`.

Steps 2–6 are imported theorem interfaces. Steps 1 and 7–10 are elementary topology candidates for formalization.

## 10. Claim boundary

Supported:

- solved status;
- exact theorem formulations;
- category equivalence with named imports;
- implication hierarchy;
- direct finite-extinction proof spine;
- terminal topology argument conditional on the surgery classification.

Not supported by WP00 alone:

- line-by-line verification of Perelman's analytic estimates;
- independent proof of canonical neighbourhoods;
- independent construction of surgery;
- independent proof of finite extinction;
- full formalization of any of those analytic components;
- novelty or priority claims.

## 11. Audit disposition

`PC-WP00` passes the source-and-equivalence gate with explicit downstream proof debt.

Permitted next work:

- `PC-WP01`: false-proof and semantic-failure atlas;
- `PC-WP02`: source-normalized Hamilton–Perelman theorem ledger.

Closed until integration:

- proof compression;
- formal surgery-history certification beyond the terminal algebraic surrogate;
- any claim that the analytic core has been independently recertified.