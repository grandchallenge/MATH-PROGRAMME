# EXT-015D / 026 — an exact D10 variance obstruction and corrected scalar-valued liquid kernel bridge

**Mathematical disposition:** **PROVED NO-GO** for a weight-preserving quasi-isomorphism between the originally proposed liquid derived mapping objects of [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md) and the actual free-scalar observables of [024](FREE_SCALAR_DIFFERENTIABLE_WEISS_024.md). **CONSTRUCTED AND PROVED** a correctly typed, natural identification of their *replacement* underived scalar-valued liquid dual **underlying cochain complexes** with compactly supported distributional polynomial kernels in **all cohomological degrees and finite polynomial weights**. This extends to the product completion as an isomorphism of underlying cochain complexes. **Further proved on connected intervals:** the corrected field-source complex has an explicit continuous contraction onto two affine modes; its finite symmetric powers are homotopy equivalent to finite-dimensional projective liquid objects, so their **underived scalar Hom computes genuine derived scalar RHom in every degree**. This is **not** a theorem identifying liquid plots with Costello–Gwilliam DVS smooth plots.

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

The **actual classical free-field polynomial observables** of 024 have the component of weight $w$

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

The product comparison is not being promoted to a morphism of complete differentiable **pro**-cochain complexes without an actual natural liquid-to-DVS plot functor. Nonetheless all ordinary cohomological degrees of this scalar-liquid complex are identified with those of the distributional classical polynomial observables. In particular, for a connected interval, [024](FREE_SCALAR_DIFFERENTIABLE_WEISS_024.md) implies zero cohomology outside degree zero, and the completed cohomology is the formal two-variable series space $\mathbb R[[a,b]]$ in degree zero.

This degreewise exact comparison is stronger than a hypothetical degree-zero numerical analogy, but fundamentally **different** from the degree-zero/degree-one target-support Ext continuity result in [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md).

## 5. All-degree derived scalar bridge on a connected interval

There is a stronger and **fully proved** conclusion for the actual one-dimensional free scalar. Its smooth **field** complex, unlike the originally proposed test-function source of [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md), has an explicit continuous contraction onto a finite-dimensional **projective liquid** object.

Fix a nonempty connected open interval $U$, and choose any base point $x_0\in U$. Define the continuous linear operators on the nuclear Fréchet space $C^\infty(U)$

$$
p(f)=\bigl(f(x_0),f'(x_0)\bigr),
\quad
i(a,b)(x)=a+b(x-x_0),
\quad
(Tg)(x)=\int_{x_0}^{x}(x-t)g(t)\,dt.
\tag{26.12}
$$

All three maps are continuous: the first two are evaluations/finite-dimensional inclusion, and for every compact $K\subset U$ the derivatives and suprema of $Tg$ on $K$ are controlled by a finite set of seminorms of $g$ on the compact interval joining $K$ to $x_0$. They are morphisms of real liquid modules by Fréchet realization.

**Lemma 26.3 (explicit liquid homotopy contraction).** For the cochain complex $\mathcal F(U)=[C^\infty(U)^0\xrightarrow{D}C^\infty(U)^1]$, $D=\partial_x^2$, the operators above satisfy

$$
p\,i=\mathrm{id}_{\mathbb R^2},
\qquad
D T=\mathrm{id}_{C^\infty(U)},
\qquad
T D=\mathrm{id}_{C^\infty(U)}-i p.
\tag{26.13}
$$

Thus $T:\mathcal F^1\to\mathcal F^0$ is a continuous linear cochain homotopy between $\mathrm{id}_{\mathcal F}$ and the projection $i p$, and

$$
\underline{\mathcal F(U)}
\simeq_{\mathrm{chain\ homotopy}}
\underline{\mathbb R^2}[0].
\tag{26.14}
$$

**Proof.** The fundamental theorem of calculus gives $(Tg)''=g$. For any $f$, $f-Tf''$ is affine with the value and first derivative of $f$ at $x_0$, hence equals $i p(f)$. All operators are continuous and liquid-linear as noted. Therefore the identities hold as maps in $\mathrm{Liq}_p(\mathbb R)$, not merely at global points. $\square$

**Theorem 26.4 (corrected scalar liquid derived Hom is computed by the underived cochain dual).** For each finite polynomial arity $w\ge0$, form the graded symmetric **field-source** complex

$$
\mathcal S_w(U)=
\left(\underline{\mathcal F(U)}^{\widehat\otimes_{\pi}w}\right)_{\mathfrak S_w},
\tag{26.15}
$$

where the tensor product is first taken **classically on nuclear Fréchet cochain terms** and then realized in liquid modules; the finite graded symmetric-group coinvariant is the image of its averaging projector. Then $\mathcal S_w(U)$ is liquid-chain-homotopy equivalent to $\underline{\mathrm{Sym}^w(\mathbb R^2)}[0]$, a finite-dimensional projective object. It is therefore **K-projective** as a complex of liquid modules, although its individual Fréchet field terms need not be projective.

Consequently, for every $0<p\le1$, the natural underived-to-derived scalar comparison

$$
\boxed{\quad
\mathrm{Hom}^{\bullet}_{\mathrm{Liq}_p}
\left(\mathcal S_w(U),\underline{\mathbb R}\right)
\xrightarrow{\ \simeq\ }
R\mathrm{Hom}_{\mathrm{Liq}_p}
\left(\mathcal S_w(U),\underline{\mathbb R}\right)
\quad}
\tag{26.16}
$$

is a quasi-isomorphism in **all cohomological degrees**.

**Proof.** The continuous cochain maps and homotopies of Lemma 26.3 can be tensor-multiplied finitely using completed projective tensors. On nuclear Fréchet spaces, the tensor extensions of these continuous maps exist, and the standard tensor homotopy identity yields an explicit homotopy equivalence of the finite tensor power of $\mathcal F$ with $(\mathbb R^2)^{\otimes w}[0]$. Averaging this homotopy equivalence and its homotopies over the finite group $\mathfrak S_w$ gives the same conclusion for graded symmetric coinvariants and $\mathrm{Sym}^w(\mathbb R^2)[0]$.

A singleton free real-liquid measure object $\underline{\mathbb R}$ is projective; its finite direct sums, including $\underline{\mathrm{Sym}^w(\mathbb R^2)}$, are projective. A complex chain-homotopy equivalent to a bounded projective complex is K-projective: applying $\mathrm{Hom}$ to any acyclic target complex yields a contractible/acyclic result, since it does for the finite projective representative. Hence the naive Hom complex already computes the right-derived Hom of $\mathcal S_w(U)$, proving (26.16). $\square$

Combining (26.10) and (26.16), the **correctly typed** liquid derived scalar Hom has the same underlying cochain-level observable model and, objectwise on connected intervals, the same cohomology in every degree as the distributional free-scalar polynomial observables:

$$
H^qR\mathrm{Hom}_{\mathrm{Liq}_p}
\left(\mathcal S_w(U),\underline{\mathbb R}\right)
\cong
\begin{cases}
\mathrm{Sym}^w(\mathbb R^2),&q=0,\\
0,&q\ne0.
\end{cases}
\tag{26.17}
$$

The arity-completed product of these complexes has cohomology $\mathbb R[[a,b]]$ in degree zero and zero otherwise, because products of real vector spaces are exact. This result does **not** require asserting that Fréchet spaces $C^\infty(U)$ are projective individually. It uses the much stronger **explicit homotopy equivalence** to a finite projective object.

**Naturality caveat:** The auxiliary homotopy $T$ and projector $p$ depend on the chosen $x_0$. The canonical **identification of liquid Hom with compact distributional kernels** is natural for interval inclusions, and the statement of K-projectivity is objectwise independent of any chosen contraction; no naturally chosen base point across all interval inclusions is being claimed.

## 6. The remaining genuine enrichment and quantization boundary

Theorems 26.2 and 26.4 eliminate the ambiguity concerning higher scalar liquid $\mathrm{Ext}$ **for these corrected field-source symmetric powers on connected intervals**. They do **not** give a universal higher Ext target-support theorem for the originally different source and coefficient objects of [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md).

The next specific missing comparison is **enriched**: (26.9) gives the *set/vector-space* of liquid scalar morphisms, but the Costello–Gwilliam DVS polynomial kernels carry a specified **smooth plot structure**. Merely transporting this structure along the vector-space isomorphism is not a proof that it is canonically recovered from a liquid internal Hom construction.

Additional separate obligations are:

1. Define a natural liquid-to-DVS scalar mapping-object enrichment and verify that its plots agree with smooth families of compactly supported distributional kernels, including locally uniform compact supports.
2. Verify B.6 differentiable cofibrations/fibrations and filtration-compatible disjoint-support operations in that enriched comparison, not just on underlying real complexes.
3. Treat interacting/renormalized BV contractions and general higher liquid Ext with their actual, and different, source/coefficient objects. Arbitrary distributional diagonal contractions are still not defined by the classical comparison.

The no-go in Theorem 26.1 and the corrected all-degree scalar-derived result in Theorem 26.4 are compatible: **different, correctly typed objects** support different conclusions.

## 7. Verification ledger

| Question | Verdict |
| --- | --- |
| Original 022 polynomial-source, test-function-target $R\mathrm{Hom}$ is equivalent weightwise to free-scalar observables | **REFUTED** by arity-zero dimension mismatch (26.3) |
| Correct scalar liquid Hom on completed smooth **field** tensors equals distributional polynomial kernels | **PROVED AS UNDERLYING COMPLEXES**, all finite weights and cochain degrees (26.10) |
| Natural extension-by-zero, signed permutations and underlying disjoint-open polynomial multiplication | PROVED COMPATIBLE on underlying complexes |
| Arity-complete products of these underlying cochain complexes | PROVED IDENTICAL by product of the isomorphisms (26.11) |
| Smooth field complex and finite graded symmetric tensors contract to finite projective liquid objects on connected intervals | PROVED by exact integration homotopy (26.12–26.15) |
| Canonical identification of their Costello–Gwilliam DVS plots with liquid internal Hom plots | **OPEN; NOT IMPLIED** |
| Correct field-source scalar liquid Hom versus derived scalar RHom on connected intervals | **PROVED ALL DEGREES** by continuous two-term contraction to finite-dimensional projectives (26.16) |
| Genuinely enriched scalar liquid-to-DVS comparison respecting smooth plots and Weiss operations | **OPEN** |
| General old-source higher liquid Ext and quantum distributional BV comparison | **OPEN** |

**Next GCL research obligation:** Critically audit the explicit continuous homotopy contraction (26.12–26.16) and its finite symmetric tensor powers. Then construct a **natural plot-preserving enriched liquid scalar mapping functor**, checking DVS smoothness and filtered/Weiss compatibility rather than renaming ordinary liquid Hom as a differentiable mapping object. General old-source Ext and interacting/renormalized quantum observables remain independent open problems. No Human Steward routine approval or extra GitHub account is needed.
