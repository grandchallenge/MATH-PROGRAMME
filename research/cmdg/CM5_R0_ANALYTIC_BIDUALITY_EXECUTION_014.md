# CMDG CM5 E3 — analytic doubling and derived biduality execution ledger 014

**Status:** ANALYTIC_CONTRACTION_LEAN_VERIFIED; CATEGORICAL_EXT_TRANSFER_AND_CANONICAL_CONNECTING_REPLAY_PENDING; GENUINE_DERIVED_BIDUALITY_OPEN. This ledger distinguishes a verified analytic reduction from instantiation on the genuine condensed real/circle objects. It is not a public MATHCERT assertion.

## Exact authority and source

- Protected predecessors: PR #3586 (actual Cech-derived augmentation equivalence) and PR #3589 (actual unit-induced shifted-comparison iff solid-source higher-Ext acyclicity), both protected merged before this work.
- Scholze, *Lectures on Condensed Mathematics*, stable May 2026 edition, [source PDF](https://people.mpim-bonn.mpg.de/scholze/Condensed.pdf), Theorem 4.3 and its proof on printed pages 25–27; Proposition 5.7 on printed page 35. Existing source-lock entry: [CM5 biduality source 004](CM5_R0_NEGATIVE_SHIFT_BIDUALITY_SOURCE_004.md).
- Coefficient category is the existing integer-lifted genuine *Ambient = CondensedMod*; the actual solid objects are the protected *G_T*, canonically products of the existing discrete-integer coefficient object.

## E3A: independently proved Banach contraction

Let $E,F,G$ be real normed spaces, with $F,G$ Banach, and let $d:E\to F$, $\delta:F\to G$, $h:F\to E$, $k:G\to F$ and $T:F\to F$, $U:G\to G$ be bounded linear maps. Assume that $\delta T=U\delta$, both operator norms are strictly less than one, and the genuine cochain homotopy identity holds:

$$
d h+k\delta=1-T.
$$

Then every $f\in F$ with $\delta f=0$ has a primitive $g\in E$ with $dg=f$.

**Proof:** Completeness and the Neumann-series theorem make $1-T$ and $1-U$ invertible in the Banach operator algebras. Set $x=(1-T)^{-1}f$. Applying $\delta$ to $(1-T)x=f$ gives $(1-U)\delta x=0$. Injectivity of $1-U$ yields $\delta x=0$. Substituting into the homotopy identity gives $d(hx)=(1-T)x=f$. Hence $g=hx$ is an actual primitive. This is a convergent analytic argument, not a formal manipulation of an infinite series.

The actual pinned Lean declaration is *banach_closed_exact_of_contracting_doubling* in *CMDGCondensedCM4P3DerivedCM5R0UniformAnalyticDoublingContractingHomotopy.lean*. Exact-head CI for its original source commit 416d69aba6893c810a41cb5cfad428c1f9bbf812 (formal-validation run 44898051050, job 136827885646) passed; axiom readback was only propext, Classical.choice and Quot.sound. That receipt applies to the original source head, not automatically to later changes.

**Source instantiation still required:** For the genuine cochains computed from a functorial free-group resolution of the compact torus $A=(\mathbb R/\mathbb Z)^I$, the operator $B=[2]^*$ has norm at most one in each Banach degree. The chain homotopy between the map induced by doubling and multiplication by two gives $d h+h d=2-B$. Setting $T=B/2$ and rescaling the homotopy satisfies the proved theorem, provided all those *actual* degreewise identifications, homotopies, and bounds are constructed. The pinned GCL repository has not yet supplied those interfaces.

## E3B: genuine categorical real/circle Ext transfer

For any short exact sequence $0\to K\to R\to C\to0$ in the actual integer-condensed module category, the contravariant long-exact Ext sequence gives

$$
\mathrm{Ext}^{q+1}(R,Z)=0
\quad\text{and}\quad
\mathrm{Ext}^{q+2}(C,Z)=0
\quad\Longrightarrow\quad
\mathrm{Ext}^{q+1}(K,Z)=0.
$$

The new Lean module *CMDGCondensedCM4P3DerivedCM5R0UniformRealCircleExtTransfer.lean* constructs this using the actual extension class and exactness theorem of the existing pinned derived-category implementation. The new source is awaiting final exact-head CI. It does not assume a real/circle exact sequence is already available.

The companion module *CMDGCondensedCM4P3DerivedCM5R0UniformRealCircleCanonicalConnecting.lean* defines the canonical connecting additive homomorphism from $\\mathrm{Ext}^0(K,Z)$ to $\\mathrm{Ext}^1(C,Z)$ using the **actual extension class** of the short exact sequence. It proves that this very map is bijective whenever both $\\mathrm{Ext}^0(R,Z)$ and $\\mathrm{Ext}^1(R,Z)$ vanish. This pins the map, not just its source and target groups. The new source requires exact-head Lean replay and does **not** assume the real vanishing inputs.

**Independent underived real/circle exactness argument (not Lean-certified):** For an extremally disconnected compact test space $S$, any continuous map $S\\to\\mathbb R/\\mathbb Z$ lifts locally to $\\mathbb R$ along the standard covering map. Compactness gives finitely many local trivializations; a disjoint clopen refinement permits the lifts to glue continuously. Apply this independently to each coordinate of a map $S\\to(\\mathbb R/\\mathbb Z)^I$, then use continuity of maps into products to obtain a lift $S\\to\\mathbb R^I$. The kernel of coordinatewise reduction consists of continuous integer-valued functions in each coordinate. This gives the intended sheaf-level exactness by testing on Stonean covers. It does not construct the requisite condensed-module objects or a machine-checkable sheaf-exactness theorem.

## E3C: exact bridge to genuine derived biduality

The published argument requires the following *not yet independently Lean-certified* objects and theorems:

1. **Realization and exactness:** Construct actual condensed integer-modules representing the topological groups $\mathbb R$ and $\mathbb R/\mathbb Z$, their arbitrary products and a degreewise exact sequence $0\to\prod_I\mathbb Z\to\prod_I\mathbb R\to\prod_I(\mathbb R/\mathbb Z)\to0$.
2. **Breen–Deligne analytic cochains:** Construct a functorial free-group resolution of the genuine compact torus, verify the actual derived-Hom cochain comparison for real coefficients, the bounded doubling homotopy, the norm bounds and exactness in every degree. A lemma about abstract Banach cochains does **not** automatically supply this.
3. **Infinite coordinates:** Prove finite-subset directed-colimit comparison for derived-Hom from arbitrary products of circles, including the site/Sheaf-Cech cohomology bridge.
4. **Circle-to-integer derived Hom:** Construct the canonical connecting morphism induced by the genuine real/circle short exact sequence, and prove the resulting equivalence of the shifted direct sum of discrete integers with the actual derived-Hom object.
5. **Biduality with the correct arrow:** Prove that the resulting isomorphism $\bigoplus_I\mathbb Z\simeq\mathbf R\mathrm{Hom}(\prod_I\mathbb Z,\mathbb Z)$ is the *evaluation/biduality map*, not an abstract isomorphism.
**Protected underived canonical-map evidence:** The existing theorem *weightedFiniteBooleanMeasureLimitLift_measureSolidification_evaluationWeight_allTrue* (in the protected CM4 P3 PointFunctional fixture) identifies the finite-Boolean evaluation-weight map with the actual measure-solidification image of a point probe. This is a verified ingredient for checking the required unit/evaluation diagram after derived duality is constructed. It is not itself a derived diagram.

6. **Genuine unit and product-target transport:** Identify the already established canonical $G_T$ product isomorphism with the correct double-dual evaluation of $F_T$, and prove the required derived-Hom-to-product comparison for the genuine coefficient target $G_S$.

The current pinned Mathlib supplies a topological-space-to-condensed-*set* functor, but a ready-made fully typed real/circle *condensed abelian group* with derived realization was not located in the source audit. This is a concrete missing interface, not a claim of mathematical nonexistence.

**Boundary:** CM5_E3_GENUINE_REAL_CIRCLE_RESOLUTION_AND_CANONICAL_DERIVED_BIDUALITY_OPEN. No solid-source higher-Ext vanishing, all-shifts derived-solidification equivalence, or public MATHCERT certification follows until E3C is discharged with fresh exact-source proof and replay.

