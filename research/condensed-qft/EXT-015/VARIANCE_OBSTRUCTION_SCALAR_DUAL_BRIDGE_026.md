# EXT-015D / 026 — an exact D10 variance obstruction and corrected scalar-valued liquid kernel bridge

**Mathematical disposition:** **PROVED NO-GO** for a weight-preserving quasi-isomorphism between the originally proposed liquid derived mapping objects of [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md) and the actual free-scalar observables of [024](FREE_SCALAR_DIFFERENTIABLE_WEISS_024.md). **CONSTRUCTED AND PROVED** a correctly typed, natural identification of their *replacement* underived scalar-valued liquid dual **underlying cochain complexes** with compactly supported distributional polynomial kernels in **all cohomological degrees and finite polynomial weights**. This extends to the product completion as an isomorphism of underlying cochain complexes. It is **not** a derived liquid equivalence or a theorem identifying liquid plots with Costello–Gwilliam DVS smooth plots.

**GCL inputs:** [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md), [024](FREE_SCALAR_DIFFERENTIABLE_WEISS_024.md), [025](AGENT_CRITICAL_REVIEW_FREE_SCALAR_025.md). Source anchors: Costello–Gwilliam, *Factorization Algebras in Quantum Field Theory*, Volume I, §4.2.1, especially **Lemma 4.2.1.1** (printed page 62), and Appendix B.6 (printed pages 469–471), [primary PDF](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf). The topological input is the classical nuclear Schwartz kernel theorem for $C^\infty(U)$, with strong continuous dual $\mathcal E'(U)$.

## 1. Fatal object-level obstruction to the previously proposed bridge

Fix a nonempty open interval $U\subseteq\mathbb R$. Write $G(U)=\underline{\mathcal D(U)}$ and let $H=\mathcal D_{[-1,1]}(\mathbb R)$, as in [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md). Its polynomial input of weight $w$ is

$$
E_w=\mathrm{Sym}^{w}_{\pi}(H),\qquad E_0=\mathbb R,
$$

and the liquid mapping complex in 022 is

$$
B_w(U)=R\mathrm{Hom}_{\mathrm{Liq}_p(\mathbb R)}
(\underline{E_w},G(U)).
\tag{26.1}
$$

The **actual classical free-field polynomial observables** of 024 have weight-$w$ part

$$
P_w(U)=\mathrm{Sym}^{w}_{\mathrm{DVS}}
\left[
\mathcal E'(U)^{-1}\xrightarrow{\partial_x^2}
\mathcal E'(U)^0
\right],
\qquad P_0(U)=\mathbb R[0].
\tag{26.2}
$$

**Theorem 26.1 (no weight-preserving quasi-isomorphism).** No natural or unnatural family of weightwise quasi-isomorphisms $B_w(U)\simeq P_w(U)$ exists for every $w\ge0$. Consequently the **obvious weight-preserving** direct-product completion $\prod_wB_w(U)$ cannot be identified with $\prod_wP_w(U)$ by a filtered quasi-isomorphism inducing an equivalence on every associated graded arity.

**Proof.** A singleton is extremally disconnected, so Scholze's compact projective free real-liquid generator gives $\underline{\mathbb R}=\mathcal M_{<p}(*)$ **projective**. Hence

$$
B_0(U)=R\mathrm{Hom}(\underline{\mathbb R},G(U))
\simeq \mathrm{Hom}(\underline{\mathbb R},G(U))[0]
\cong\mathcal D(U)[0].
\tag{26.3}
$$

On the observable side $P_0(U)=\mathbb R[0]$. The vector space $\mathcal D(U)$ is infinite-dimensional, while $\mathbb R$ is one-dimensional. These complexes cannot be quasi-isomorphic; thus their arity-zero associated graded pieces cannot be equivalent. No higher cohomology or topology is needed for the contradiction. $\square$

This is **not** a contradiction of the valid Ext-continuity theorem in [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md). It identifies a wrong **choice of source and output functors** for the intended field-observable comparison. A first-degree target-support continuity theorem is not an identification of observables.

## 2. Correct the variance: smooth fields in, real scalars out

The smooth field space on $U$ is

$$
F(U)=C^\infty(U)
$$

with its standard nuclear Fréchet topology. Its continuous linear dual is precisely the compactly supported distributions:

$$
F(U)'=\mathcal E'(U),\qquad
\lambda_T(\phi)=\langle T,\phi\rangle.
\tag{26.4}
$$

For every $w\ge0$, nuclearity and the completed projective tensor kernel theorem give

$$
F(U)^{\widehat\otimes_\pi w}\cong
C^\infty(U^w),
\qquad
\left(F(U)^{\widehat\otimes_\pi w}\right)'
=\mathcal E'(U^w).
\tag{26.5}
$$

The finite permutation group acts with the usual Koszul signs when field variables have cochain parity. Its invariants describe graded symmetric compactly supported distributional kernels. Importantly, (26.5) is a statement about **continuous duals of completed tensor products**; it does **not** say that an algebraic tensor product of compact distributions exhausts the distributions on $U^w$.

Write $\mathcal F(U)$ for the genuine two-term Fréchet field complex

$$
\mathcal F(U):
\quad C^\infty(U)^0
\xrightarrow{D}
C^\infty(U)^1,
\qquad D=\partial_x^2.
\tag{26.6}
$$

The cochain-complex continuous dual $\mathcal F(U)^\vee$, with the transpose differential and dual cohomological grading, is

$$
\mathcal F(U)^\vee:
\quad\mathcal E'(U)^{-1}
\xrightarrow{D^{\,t}}
\mathcal E'(U)^0;
\tag{26.7}
$$

$D^{\,t}=D$ on distributions, as follows by integration by parts on smooth compactly supported test functions. The sign in the cochain dual differential is fixed by the usual graded Hom rule and can be removed by an explicit change of sign in one two-term component.

For each **finite** $w$, form the completed projective graded Fréchet tensor complex

$$
\mathcal T_w(U)=
\mathcal F(U)^{\widehat\otimes_\pi w}.
\tag{26.8}
$$

Its individual cochain degrees are finite direct sums of the nuclear Fréchet spaces $C^\infty(U^w)$. The graded permutation action on $\mathcal T_w$ commutes with its tensor differential.

## 3. A genuine liquid-versus-distributional comparison on underlying complexes

Because each term of $\mathcal T_w(U)$ is Fréchet, its real-liquid realization is defined, and the canonical comparison of liquid real-linear morphisms with continuous linear maps is **fully faithful in degree zero**. Define the following cochain complex of real vector spaces using **ordinary liquid Hom, not derived Hom**:

$$
\mathscr B_w^q(U)=
\mathrm{Hom}_{\mathrm{Liq}_p(\mathbb R)}
\left(
\underline{\mathcal T_w(U)^{-q}},
\underline{\mathbb R}
\right)^{\mathfrak S_w},
\tag{26.9}
$$

with the transposed tensor differential. For $w=0$ interpret $\mathcal T_0=\mathbb R[0]$.

**Theorem 26.2 (correctly typed scalar-liquid kernel bridge).** For every $0<p\le1$, every open interval $U$, and every finite polynomial arity $w$, there is a **natural isomorphism of underlying real cochain complexes**

$$
\boxed{\quad
\mathscr B_w^\bullet(U)
\cong
P_w^\bullet(U),
\quad}
\tag{26.10}
$$

where $P_w$ denotes the compactly supported distributional homogeneous **classical polynomial observable cochain complex** in (26.2), understood through the **completed** tensor-kernel convention in Costello–Gwilliam §4.2.1.

**Proof.** Each cochain term of $\mathcal T_w$ is a finite direct sum of $C^\infty(U^w)$. Full faithfulness for Fréchet scalar-valued maps identifies each corresponding Hom in (26.9) with the **continuous dual**, namely a finite direct sum of compactly supported distributions $\mathcal E'(U^w)$ by (26.5). This exactly matches the degreewise distributional kernel model for $P_w$. The finite-group projector is a finite continuous idempotent, and invariants commute with finite duality in characteristic zero. The transposed differential is the same sum of distributional differential operators, with the standard Koszul signs, as the polynomial observable differential; hence the degreewise identifications commute with all differentials. They are natural in $U$, since restriction of smooth field configurations for an open embedding $V\hookrightarrow U$ transposes to **extension by zero** of compactly supported distributions $V^w\hookrightarrow U^w$. $\square$

**Prefactorization compatibility on underlying complexes.** For pairwise disjoint $U_1,\ldots,U_r\subset V$, distributional kernel extension by zero followed by exterior tensor product and finite symmetrization defines the graded multilinear structure maps. These agree on both sides of (26.10), because pairing with a completed field tensor separates distributions. Thus the comparison intertwines the **underlying real-linear prefactorization operations**.

**Crucial boundary:** Neither (26.9) nor liquid full faithfulness equips the set of morphisms with the complete **Costello–Gwilliam differentiable plot structure**. The DVS plots are an additional analytic structure, and merely transporting them along (26.10) does not establish that this structure arises functorially from the liquid category. Similarly, a term-by-term ordinary Hom complex is not automatically a model for $R\mathrm{Hom}_{\mathrm{Liq}_p}$; its cochain terms need not be projective or K-projective in the source variable.

## 4. Extend the bridge over all polynomial weights without changing the claim

Define the completed underlying cochain complexes

$$
\widehat{\mathscr B}(U)=\prod_{w\ge0}\mathscr B_w(U),
\qquad
\widehat P(U)=\prod_{w\ge0}P_w(U).
\tag{26.11}
$$

The comparison from Theorem 26.2 is an isomorphism at every weight, natural in $U$, hence their product is an **isomorphism of underlying completed real cochain complexes**, compatible with the decreasing arity-tail filtration. It respects the underlying prefactorization maps at each fixed output arity.

The product comparison is not being promoted to a morphism of complete differentiable **pro**-cochain complexes without an actual natural liquid-to-DVS plot functor. Nonetheless all ordinary cohomological degrees of this **underived** scalar-liquid complex are identified with those of the distributional classical polynomial observables. In particular, for a connected interval, [024](FREE_SCALAR_DIFFERENTIABLE_WEISS_024.md) implies zero cohomology outside degree zero, and the completed cohomology is the formal two-variable series space $\mathbb R[[a,b]]$ in degree zero.

This degreewise exact comparison is stronger than a hypothetical degree-zero numerical analogy, but fundamentally **different** from the degree-zero/degree-one target-support Ext continuity result in [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md).

## 5. Where the next genuine higher-derived obstruction lives

The next desired comparison would be

$$
\mathrm{Hom}_{\mathrm{Liq}_p}
\left(\underline{\mathcal T_w(U)},\underline{\mathbb R}\right)
\longrightarrow
R\mathrm{Hom}_{\mathrm{Liq}_p}
\left(\underline{\mathcal T_w(U)},\underline{\mathbb R}\right)
\tag{26.12}
$$

as a comparison of cochain complexes, with the left side interpreted as the termwise Hom complex (26.9), followed by graded invariants. This is **not** automatically a quasi-isomorphism: it requires suitable projectivity/K-projectivity or an acyclicity theorem for the **Fréchet smooth field-source complex** $\mathcal T_w$. Establishing the higher-liquid-$\mathrm{Ext}$ obstructions, with the exact coefficient $\underline{\mathbb R}$, is a meaningful independent next mathematical question.

Even if (26.12) were a quasi-isomorphism, a genuine **enriched** comparison to Costello–Gwilliam would still require:

1. A natural construction of smooth plots on liquid-derived scalar mapping complexes (or a restricted differentiable realization functor), proving its compatibility with the convenient/DVS kernel plots.
2. Fibration, cofibration, and inverse-tower conditions at every finite arity and quantum-weight quotient.
3. Preservation of the precise disjoint-support multilinear operations, BV contractions and Weiss Čech diagrams. The unrestricted distributional BV contraction remains undefined in general, as noted in [024–025](AGENT_CRITICAL_REVIEW_FREE_SCALAR_025.md).

The **proved no-go** from Theorem 26.1 and the **corrected underived kernel bridge** from Theorem 26.2 are therefore complementary: the original D10 formulation is refuted, and the mathematically appropriate scalar-valued replacement has been constructed with exact remaining obligations.

## 6. Verification ledger

| Question | Verdict |
| --- | --- |
| Original 022 polynomial-source, test-function-target $R\mathrm{Hom}$ is equivalent weightwise to free-scalar observables | **REFUTED** by arity-zero dimension mismatch (26.3) |
| Correct scalar liquid Hom on completed smooth **field** tensors equals distributional polynomial kernels | **PROVED AS UNDERLYING COMPLEXES**, all finite weights and cochain degrees (26.10) |
| Natural extension-by-zero, signed permutations and underlying disjoint-open polynomial multiplication | PROVED COMPATIBLE on underlying complexes |
| Arity-complete products of these underlying cochain complexes | PROVED IDENTICAL by product of the isomorphisms (26.11) |
| Canonical identification of their Costello–Gwilliam DVS plots with liquid internal Hom plots | **OPEN; NOT IMPLIED** |
| Comparison of termwise liquid Hom with derived liquid RHom in all degrees (26.12) | **OPEN; REQUIRES ACYCLICITY/PROJECTIVITY** |
| Genuine quantum distributional BV comparison and higher derived Weiss bridge | **OPEN** |

**Next GCL research obligation:** Apply a critical categorical and analytical review to the nuclear Fréchet dual-kernel step. Then attack (26.12) directly using the exact projective generator model of real liquid modules; separately build a plot-preserving restricted enrichment for test kernels, rather than renaming ordinary liquid Hom as a differentiable mapping object. No Human Steward routine approval or extra GitHub account is needed.
