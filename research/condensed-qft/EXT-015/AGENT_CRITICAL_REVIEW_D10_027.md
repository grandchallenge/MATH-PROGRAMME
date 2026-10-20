# EXT-015D / 027 — critical mathematical audit of corrected all-degree scalar-liquid / DVS bridge

**Scope and disposition:** Independently re-check the *logical argument* of [D10 research 026](VARIANCE_OBSTRUCTION_SCALAR_DUAL_BRIDGE_026.md), preserving separately the originally false bridge of [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md). **ACCEPT as a bounded mathematical theorem**, pending protected review admission: the wrong-variance no-go; the corrected underived liquid scalar kernel dual; its derived enhancement by an explicit smooth-field contraction on **connected intervals**; and its **actual Costello–Gwilliam DVS plot enrichment** using manifold-valued liquid Hom. Do **not** claim general liquid-category smooth enrichment, BV contraction on arbitrary distributions, or interacting quantum equivalence. This critical argument uses one authenticated GCL identity and does not invent a second external referee.

**Protected mathematical source:** [Result 026 / PR #2782](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2782) merged at exact protected `main` commit `42cf8f3a221adeed6fbc7791a224536864cac258`. This review checks that source's theorem statements and proofs, not an unpublished draft.

**Primary references verified:** Costello–Gwilliam, [*Factorization Algebras in Quantum Field Theory*, Volume I](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), especially **Lemma 4.2.1.1** (printed p. 62), **Definition B.2.1.1** (printed p. 462, PDF page 469), **Definition B.2.1.2** (printed p. 463), and Appendix B.6 (printed pp. 469–471). Scholze, [*Lectures on Analytic Geometry*](https://arxiv.org/abs/2605.03655), Theorem 6.5, gives the projective singleton real-liquid object and the real-liquid exact category. The nuclear Schwartz kernel theorem gives the completed tensor identity for nuclear Fréchet smooth functions.

## I. Inspect the fatal wrong-variance and unit-arity mismatch

The original 022 degree-zero weight is $R\mathrm{Hom}_{\mathrm{Liq}_p}(\underline{\mathbb R},\underline{\mathcal D(U)})$. The singleton real-liquid module $\underline{\mathbb R}$ is projective, so this is $\mathcal D(U)$ concentrated in degree zero. The genuine observable polynomial unit of arity zero is instead $\mathbb R[0]$. For any nonempty $U$, $\mathcal D(U)$ is infinite-dimensional. Hence the originally contemplated comparison cannot be a weight-preserving graded quasi-isomorphism, even before considering smoothness. **ACCEPT NO-GO 26.1**. This does not refute 022's separate, correctly typed first-Ext support-continuity theorem.

## II. Reconstruct actual polynomial distributions from corrected liquid scalar inputs

The genuine field space is $F(U)=C^\infty(U)$, not the compactly supported test function source of 022. It is nuclear Fréchet, and

$$
C^\infty(U)^{\widehat\otimes_\pi w}
\cong C^\infty(U^w),
\qquad
C^\infty(U^w)'=\mathcal E'(U^w).
$$

The corrected two-term field cochain complex is $[C^\infty(U)^0\xrightarrow{\partial_x^2}C^\infty(U)^1]$. Each completed finite tensor term is a finite sum of the same Fréchet spaces on $U^w$. Their scalar-valued liquid Hom groups coincide with their continuous scalar duals by Fréchet full faithfulness; the transposed differential is exactly the distributional polynomial observable differential, including the Koszul tensor signs. Graded symmetric coinvariants are finite-group direct summands, and their duals are the invariant kernel spaces. This identifies **every term and differential**, naturally for interval inclusions, with the genuine distributional polynomial complexes described in CG §4.2.1. **ACCEPT 26.2**. No invalid identification of algebraic pure tensors with all distribution kernels has been used.

## III. Verify *derived* scalar Hom through an explicit continuous contraction

Choose $x_0\in U$ for a connected open interval and set

$$
(Tg)(x)=\int_{x_0}^{x}(x-t)g(t)\,dt.
$$

Then $(Tg)''=g$, while $T(f'')=f-f(x_0)-(x-x_0)f'(x_0)$. These are **continuous linear equalities in the Fréchet topology**, as controlled by compact seminorms. The field complex therefore deformation-retracts, by genuine liquid-linear maps and homotopies, onto affine solutions $\mathbb R^2[0]$.

Finite completed projective tensor powers preserve an explicit chain homotopy equivalence between nuclear Fréchet complexes; finite graded symmetrization preserves it by averaging. Thus every corrected graded symmetric **field-source** tensor complex is chain-homotopy equivalent to $\underline{\mathrm{Sym}^w(\mathbb R^2)}[0]$, a finite sum of copies of the **projective** singleton module. This makes the source K-projective *as a complex*; it does not imply individual $C^\infty$ Fréchet modules are projective. The ordinary scalar liquid Hom complex therefore computes the genuine derived scalar Hom in every cohomological degree. Its cohomology is the symmetric power of $\mathbb R^2$ in degree zero and vanishes in all other degrees. **ACCEPT 26.3–26.4**.

**Objectwise guard:** The base point for the contraction is not chosen naturally over all interval inclusions. K-projectivity and the canonical scalar Hom-to-derived comparison are nevertheless intrinsic, and the natural underived kernel identification still commutes with restriction/extension by zero.

## IV. Verify the exact DVS smooth-plot definition, not merely topological analogy

This is the decisive category-enrichment step. In **Definition B.2.1.1**, CG explicitly defines a smooth family of **compactly supported distributions** on a manifold $V$, parametrized by a smooth manifold $M$, to be a **continuous linear map**

$$
C^\infty(V)\longrightarrow C^\infty(M).
$$

The corrected GCL construction takes precisely

$$
\mathrm{Hom}_{\mathrm{Liq}_p}
\bigl(\underline{C^\infty(V)},\underline{C^\infty(M)}\bigr).
$$

Both source and target are Fréchet, so real-liquid full faithfulness yields an exact identification with the CG-defined plot set, **for each finite-dimensional parameter manifold**. Pullback along a map of parameter manifolds is exactly pullback of target smooth functions; the flat parameter-space connection in **Definition B.2.1.2** is the same differentiation on the target. The field differential acts on the *source* smooth coordinates and commutes with this flat parameter connection. The same argument applies termwise to graded symmetric finite tensors. This verifies **the plots and connection**, not just the underlying distributional vector space. **ACCEPT 26.5**.

The construction is **restricted**: its DVS plot functor uses an explicit family of liquid target modules $\underline{C^\infty(M)}$. It does not assert that the unadorned ordinary liquid internal Hom in every liquid module has a canonical Costello–Gwilliam smooth DVS realization.

## V. Completed classical and Weiss implications

The DVS comparison at each finite polynomial arity is a **literal differentiable cochain isomorphism**, natural under extension by zero. External tensor products, compact distributional support and finite symmetrization give the same smooth disjoint-open prefactorization maps on both sides. Product completion by arity with its tail filtration has smoothly split finite quotient projections; the termwise DVS isomorphism extends to an isomorphism of **complete differentiable pro-cochain complexes**. Its classical Weiss Čech maps are identified with the CG distributional polynomial ones; [024–025](AGENT_CRITICAL_REVIEW_FREE_SCALAR_025.md) already proved smooth/complete classical Weiss descent for the free scalar model. **ACCEPT 26.6**, within those hypotheses.

**Quantum boundary:** Compact distributional kernels need not admit diagonal BV contraction; CG themselves explicitly warn of the undefined product of distributions on the diagonal in their introductory treatment. The formal **smeared** free BV model of 024 remains valid, but no unrestricted quantum distributional extension follows from the classical DVS bridge.

## VI. Verdict and next obligation

| Claim | GCL mathematical verdict |
| --- | --- |
| Original 022 test-function-valued liquid RHom identifies weightwise with observables | **REFUTED**, wrong variance and arity-zero coefficient |
| Corrected scalar-valued liquid Hom of smooth field tensor terms identifies with distributional polynomial kernels | **PROVED**, natural all finite arities and underlying degrees |
| Corrected scalar-derived liquid RHom on connected intervals | **PROVED ALL DEGREES**, explicit contraction to finite projectives |
| Corrected scalar liquid Hom via manifold-valued targets reconstructs actual CG DVS plots | **PROVED**, literal B.2.1.1 and B.2.1.2 |
| Arity-completed classical DVS pro-cochains and classical Weiss descent | **PROVED**, under source-backed free-field comparison |
| Universal liquid-to-DVS enrichment; general old-source higher liquid Ext; arbitrary distributional quantum BV | **OPEN** |

**Next mathematical step:** Extend this restricted enriched construction to a precisely chosen broader class of liquid analytic spaces, or prove an obstruction. For quantum observables, identify the **regularized subspace** of distributional kernels on which BV contractions remain well-defined and compatible with smooth parameter plots and Weiss descent. Do not mark interactions solved. This audit is GCL agent mathematical work, not a new Human Steward obligation.
