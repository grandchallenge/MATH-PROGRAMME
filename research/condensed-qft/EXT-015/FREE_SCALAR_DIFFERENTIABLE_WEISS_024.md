# EXT-015D / 024 — actual smooth free-scalar comparison, higher cohomology and Weiss descent

**Mathematical scope:** A concrete one-dimensional **free real scalar** field theory, its actual differentiable polynomial observables, and its **formal free BV quantization** over $\mathbb R[[\hbar]]$. We construct the smooth classical comparison, verify the completed pro-cochain filtration, compute every classical cohomological degree on an interval, and prove completed Weiss descent for the classical and formal free quantum models. We **do not** claim a general comparison with liquid derived Hom in higher degrees, interacting renormalized theories, or a natural quantum extension of arbitrary distributional products.

**Status:** Research proof for GCL critical audit and protected admission. This note treats the higher-derived question for **the actual free-scalar observable complex**; it does not replace the independently different liquid Ext comparison from [019–020](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md).

**Primary reference:** Costello–Gwilliam, [*Factorization Algebras in Quantum Field Theory*, Vol. I](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), §4.2.1, especially **Lemma 4.2.1.1** (printed p. 62), §4.2.6 (pp. 68–69), §6.1, and Appendix **B.6.0.7–B.6.1.1** (printed pp. 469–471). The quoted categorical structure and elliptic smooth/distributional homotopy result are those of this source, not an identification invented between unrelated categories.

## 1. Actual free field and the two differentiable observable models

For each open subset $U\subseteq\mathbb R$, the free scalar action with kinetic operator $D=\partial_x^2$ is

$$
S(\phi)=\frac12\int_U \phi\,D\phi\,dx.
$$

Use compactly supported **smeared** observables, as in §4.2 of the source. The two-term differentiable cochain complex of linear observables is

$$
L_{\mathrm{sm}}(U):
\quad \mathcal D(U)[-1]\xrightarrow{D}\mathcal D(U)[0],
\tag{24.1}
$$

where $\mathcal D(U)=C_c^\infty(U)$. The corresponding complex of **all** compactly supported polynomial distributional linear observables is

$$
L_{\mathrm{dist}}(U):
\quad \mathcal E'_c(U)[-1]\xrightarrow{D}\mathcal E'_c(U)[0],
\tag{24.2}
$$

where $\mathcal E'_c(U)$ denotes distributions with compact support contained in $U$. To avoid accidental confusion, $\mathcal E'_c(U)$ here is **not** the space of smooth fields $C^\infty(U)$ and is not $\mathcal D(U)$.

The inclusion of smooth densities in compactly supported distributions is a natural continuous linear cochain morphism $j_U:L_{\mathrm{sm}}(U)\to L_{\mathrm{dist}}(U)$.

For each $n\ge0$, define **graded symmetric powers in convenient differentiable cochain complexes**,

$$
\mathcal O_{\mathrm{sm},n}(U)=
\mathrm{Sym}^{n}_{\mathrm{ConVS}}L_{\mathrm{sm}}(U),
\qquad
\mathcal P_{\mathrm{dist},n}(U)=
\mathrm{Sym}^{n}_{\mathrm{DVS}}L_{\mathrm{dist}}(U).
\tag{24.3}
$$

These use the actual convenient/differentiable smooth multilinear structure; they are not the real-liquid mapping objects of [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md). In the regular case the smooth kernel theorem yields a canonical description of each homogeneous summand as compactly supported **smooth graded tensor kernels on $U^n$**, modulo the graded symmetric-group action. The distributional model uses compactly supported distributional kernels on $U^n$.

Define the uncompleted polynomial observables

$$
\mathcal O_{\mathrm{sm}}^{\mathrm{cl}}(U)
=\bigoplus_{n\ge0}\mathcal O_{\mathrm{sm},n}(U),
\qquad
\mathcal P_{\mathrm{dist}}^{\mathrm{cl}}(U)
=\bigoplus_{n\ge0}\mathcal P_{\mathrm{dist},n}(U).
\tag{24.4}
$$

A plot from a finite-dimensional smooth manifold $M$ into the regular kernel of degree $n$ space means a **convenient-smooth family** of compactly supported smooth kernels. Explicitly, locally on $M$ the kernels have a common compact support in $U^n$, and their joint function on $M\times U^n$ is smooth. The distributional plots are the smooth families of distributions from Costello–Gwilliam's DVS structure. Products, smooth kernel extension by zero, symmetrization and multiplication are smooth multilinear maps in this structure.

**Theorem 24.1 (actual differentiable polynomial comparison).** The maps

$$
j_{U,n}:\mathcal O_{\mathrm{sm},n}(U)
\longrightarrow\mathcal P_{\mathrm{dist},n}(U)
\tag{24.5}
$$

are smooth **cochain homotopy equivalences** of differentiable complexes for every $U$ and every $n\ge0$. They are natural for extension by zero along open inclusions and assemble into a morphism of classical prefactorization algebras.

**Proof and source check.** This is exactly the construction and mathematical conclusion of Costello–Gwilliam **Lemma 4.2.1.1**. Its proof invokes the elliptic smooth-distribution comparison of Appendix B.10 and says explicitly that it provides smooth cochain homotopies, not merely isomorphisms of underlying vector-space cohomology. In one dimension $D=\partial_x^2$ is elliptic. Naturality of the inclusion $j_U$ under extension by zero is immediate for test functions and distributions. For disjoint opens, the prefactorization multiplication is graded symmetric product after extension by zero, and $j$ commutes with it because it is induced on generators. This is the needed *actual smooth differentiable* comparison, without replacing the field space by a liquid Ext source.

## 2. The B.6 complete pro-cochain comparison

Define the arity-completed classical objects

$$
\widehat{\mathcal O}_{\mathrm{sm}}^{\mathrm{cl}}(U)
=\prod_{n\ge0}\mathcal O_{\mathrm{sm},n}(U),
\qquad
\widehat{\mathcal P}_{\mathrm{dist}}^{\mathrm{cl}}(U)
=\prod_{n\ge0}\mathcal P_{\mathrm{dist},n}(U),
\tag{24.6}
$$

with decreasing **arity-tail** filtration $F^N=\prod_{n\ge N}(-)_n$ and product differentiable plots. Each quotient is the finite direct sum of weights $n<N$ and the projections are smoothly split by inserting zeros. Therefore (i) $F^0$ is the full object, (ii) every tail inclusion is a **differentiable cofibration** with induced plots, and (iii) the objects are complete and separated. These verify **B.6.0.7**, not merely the ordinary algebraic filtration axioms.

The finite quotient towers have smoothly split fibrations. For each fixed $k$, the quotient of the tower element indexed by $N$ by $F^k$ becomes constant once $N\ge k$. Its successive kernel is the individual differentiable weight $N$ complex. The comparison on each kernel is $j_{U,N}$, a smooth homotopy equivalence by Theorem 24.1. Thus **all three** hypotheses of **B.6.0.11** hold.

**Theorem 24.2 (completed classical comparison, all cohomological degrees).**

$$
\widehat j_U:
\widehat{\mathcal O}_{\mathrm{sm}}^{\mathrm{cl}}(U)
\longrightarrow
\widehat{\mathcal P}_{\mathrm{dist}}^{\mathrm{cl}}(U)
\tag{24.7}
$$

is a weak equivalence of **differentiable pro-cochain complexes**, and in particular a quasi-isomorphism in **every cohomological degree**, not just degrees zero and one.

This is an immediate application of B.6.0.11 to the explicitly verified split towers. The proof works despite possible nonvanishing in individual higher degrees because the map on each kernel is a smooth chain homotopy equivalence. It says nothing about comparison with the *liquid* derived Hom complexes from 022 in those higher degrees.

**Arity completion warning:** The ordinary direct sum (24.4) and the completed product (24.6) are not isomorphic as objects. The distinction is substantive and agrees with [the actual noncommutation example 021](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md). The comparison uses completion *after* the finite quotient construction.

## 3. Every cohomological degree on a connected interval

Let $I\subseteq\mathbb R$ be a nonempty connected open interval. Define the moment map

$$
m:\mathcal D(I)\to\mathbb R^2,
\qquad m(f)=\left(\int_I f(x)\,dx,\ \int_I x f(x)\,dx\right).
\tag{24.8}
$$

**Lemma 24.3 (explicit smooth contraction).** The sequence

$$
0\longrightarrow\mathcal D(I)
\xrightarrow{\partial_x^2}\mathcal D(I)
\xrightarrow{m}\mathbb R^2
\longrightarrow0
\tag{24.9}
$$

is exact and has a continuous linear right inverse to $m$. It yields a smooth chain contraction of $L_{\mathrm{sm}}(I)$ onto $\mathbb R^2$ concentrated in cohomological degree zero.

**Proof.** A compactly supported affine function vanishes, so $\partial_x^2$ is injective. Integration by parts gives both moments zero on the image. Conversely for $g$ with both moments zero, define

$$
(Kg)(x)=\int_{-\infty}^{x}(x-t)g(t)\,dt.
\tag{24.10}
$$

Then $(Kg)''=g$; before the support $Kg=0$, and after the support it equals $x\int g-\int t g=0$. Thus $Kg\in\mathcal D(I)$. Every support stage of the zero-moment subspace is mapped by $K$ continuously into the same compact interval's test-function space. Two distinct bumps in $I$ have linearly independent moment vectors, so they give a continuous linear section of $m$. Splitting with that section and $K$ gives continuous linear cochain homotopies; they are smooth in the convenient/DVS structure. $\square$

The characteristic-zero tensor/Künneth and finite symmetric-group averaging arguments preserve this smooth contraction in every finite homogeneous polynomial weight. Consequently

$$
H^q\bigl(\mathcal O_{\mathrm{sm}}^{\mathrm{cl}}(I)\bigr)=
\begin{cases}
\mathrm{Sym}(\mathbb R^2),&q=0,\\
0,&q\ne0,
\end{cases}
\tag{24.11}
$$

and for the **arity completion** of (24.6),

$$
H^0\bigl(\widehat{\mathcal O}_{\mathrm{sm}}^{\mathrm{cl}}(I)\bigr)
\cong\prod_{n\ge0}\mathrm{Sym}^n(\mathbb R^2)
\cong\mathbb R[[a,b]],
\qquad H^{q\ne0}=0.
\tag{24.12}
$$

The distributional polynomial model has the same cohomology in **every degree** by Theorem 24.2. This explicitly answers the higher-cohomological-degree question for this **free one-dimensional classical observable model**. It does **not** calculate higher real-liquid Ext of the fixed source against arbitrary coefficients.

## 4. Classical Weiss descent with actual smooth chain homotopies

Let $\mathfrak U=\{U_i\}$ be a Weiss cover of $U$: every finite subset of $U$ belongs to some $U_i$. For fixed $n\ge1$, the opens $\{U_i^n\}$ cover $U^n$ in the **ordinary** topology. Moreover finite intersections are $(\bigcap U_i)^n$.

The graded tensor-kernel description identifies the weight $n$ part of the augmented Weiss Čech complex for $\mathcal O_{\mathrm{sm}}^{\mathrm{cl}}$ with the augmented Čech complex of compactly supported smooth sections of a finite-rank graded bundle on $U^n$, followed by finite symmetric-group coinvariants. A locally finite partition of unity subordinate to the cover $\{U_i^n\}$ gives a contracting homotopy of the augmented Čech complex. Multiplication by each fixed partition function preserves compact support and is continuous linear (hence differentiable-smooth). On a compact kernel support only finitely many partition functions occur. The homotopy commutes with the internal complex with differential $\partial_x^2$ **only up to the total Čech differential**, but the double-complex spectral sequence suffices: each coefficient-degree Čech resolution is exact, and the cochain complexes are degreewise bounded at each fixed arity. Equivalently use the corresponding acyclic-assembly lemma. Averaging over the finite symmetric group preserves this property.

The weight-zero summand is the constant unit and its augmented Čech complex is exact for a nonempty Weiss cover with the usual unital conventions.

**Theorem 24.4 (classical smooth Weiss descent).** The augmented Weiss Čech map

$$
\check C_{\mathrm{Weiss}}
(\mathfrak U,\mathcal O_{\mathrm{sm}}^{\mathrm{cl}})
\longrightarrow\mathcal O_{\mathrm{sm}}^{\mathrm{cl}}(U)
\tag{24.13}
$$

is a weak equivalence in differentiable cochain complexes in **all cohomological degrees**. For the completed objects (24.6), use **B.6.0.8** to complete the Čech direct sums after arity truncation; then B.6.0.11 and the split-arity tower give a weak equivalence of complete differentiable pro-cochain complexes. The distributional model has the same descent result by the smooth homotopy equivalences (24.5) and two-out-of-three.

**Smooth multicategory verification.** For pairwise disjoint $U_1,\ldots,U_r\subset V$, the structure map is the product of extension-by-zero images in the graded symmetric algebra. At each finite output arity its component is a **finite sum of completed external tensor products** of smooth kernels, followed by graded symmetrization. It is a smooth cochain map multilinear in $r$ arguments. Total polynomial arity is additive; the completed product therefore preserves the B.6.1.1 filtration inequality exactly. These are the actual maps, not an unsupported claim that ordinary continuous algebraic maps are smooth.

## 5. A concrete formal free BV quantization and its Weiss descent

Set $A(U)=\mathcal O_{\mathrm{sm}}^{\mathrm{cl}}(U)$, **without arity completion** in each coefficient. On the algebra of compactly supported smooth polynomial observables, the pairing of an even generator $f$ and odd generator $\eta$ is

$$
\omega(f,\eta)=\int_U f(x)\eta(x)\,dx.
\tag{24.14}
$$

It extends uniquely to the odd second-order BV operator $\Delta_{\mathrm{BV}}$ on $A(U)$ by summing graded contractions of all even–odd generator pairs. Smoothness follows because integration of smooth compactly supported kernels is a continuous multilinear contraction at each finite polynomial weight. The graded algebraic identities are

$$
\Delta_{\mathrm{BV}}^2=0,\qquad
d_{\mathrm{cl}}\Delta_{\mathrm{BV}}
+\Delta_{\mathrm{BV}}d_{\mathrm{cl}}=0,
\tag{24.15}
$$

where $d_{\mathrm{cl}}$ is the graded derivation of $\partial_x^2:\mathcal D(U)[-1]\to\mathcal D(U)[0]$. The second identity follows from the formal self-adjointness of $\partial_x^2$ under the pairing, integration by parts, and the graded antisymmetry of the odd contractions.

Define the **actual formal smeared free BV** observable object

$$
\mathcal O_{\mathrm{free}}^{\mathrm q}(U)
=\left(A(U)[[\hbar]],\
d_{\mathrm{cl}}+\hbar\Delta_{\mathrm{BV}}\right),
\qquad
F^N=\hbar^N A(U)[[\hbar]].
\tag{24.16}
$$

This is a complete differentiable pro-cochain complex with smoothly split **graded** filtration quotients. Its finite quotients modulo powers of $\hbar$ are $\bigoplus_{k<N}\hbar^kA(U)$ as graded differentiable spaces; their projections are smoothly split surjective and the tails carry the induced smooth plots. Thus B.6.0.7 is satisfied. Equation (24.15) makes $d_q^2=0$ and makes every $F^N$ a subcomplex.

For disjoint opens, the BV pairing between images vanishes because the supports are disjoint. Therefore the *same graded symmetric multiplication* defines smooth filtration-preserving multilinear **cochain** maps

$$
\prod_{i=1}^{r}\mathcal O_{\mathrm{free}}^{\mathrm q}(U_i)
\longrightarrow
\mathcal O_{\mathrm{free}}^{\mathrm q}(V).
\tag{24.17}
$$

They are associative and permutation-equivariant by the symmetric product and extension-by-zero. In particular $\mathcal O_{\mathrm{free}}^{\mathrm q}$ is a genuine **B.6.1.1 differentiable prefactorization algebra** in this explicitly given formal free model. The canonical reduction

$$
\mathcal O_{\mathrm{free}}^{\mathrm q}(U)/\hbar
\xrightarrow{\ \cong\ }
\mathcal O_{\mathrm{sm}}^{\mathrm{cl}}(U)
\tag{24.18}
$$

is an **identity** of differentiable cochain complexes and prefactorization structure maps, not an asserted map on quantum distributional products. There is **no** canonical unrestricted $\Delta_{\mathrm{BV}}$ on arbitrary distributional diagonal kernels, so do not upgrade (24.5) to a quantum distributional chain map without renormalization.

**Theorem 24.5 (formal free quantum Weiss descent).** With the completion with respect to powers of $\hbar$ in (24.16), the augmented completed Weiss Čech morphism for $\mathcal O_{\mathrm{free}}^{\mathrm q}$ is a weak equivalence of differentiable pro-cochain complexes in **every cohomological degree**.

**Proof.** Fix a Weiss cover. At truncation order $\hbar^N$, form the completed Čech complex as prescribed by B.6.0.8. The transition to the $(N-1)$st quotient is a smooth split surjection on graded spaces, hence a differentiable fibration, with kernel $\hbar^{N-1}$ times the **classical** Čech complex. The corresponding target kernel is $\hbar^{N-1}A(U)$ with differential $d_{\mathrm{cl}}$, because the $\hbar\Delta_{\mathrm{BV}}$ part vanishes on the associated graded. The kernel augmentation is a differentiable quasi-isomorphism by Theorem 24.4. For each fixed $k$, the tower modulo $\hbar^k$ is constant for $N\ge k$. These are exactly the three requirements of B.6.0.11. Therefore the inverse-limit augmented Čech map is a weak equivalence of differentiable pro-cochain complexes. No unjustified assertion that cohomology commutes with inverse limits has been used: the proof uses *kernelwise equivalences and fibrations*, the properties missing from the hostile Roos tower in [021](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md). $\square$

There is also a direct induction on $N$ using the short exact sequences of the quotients in powers of $\hbar$. The B.6 argument is stronger because it certifies the **actual differentiable filtration**, not only an algebraic quasi-isomorphism.

## 6. Checkable additional higher-degree information on intervals

On a connected interval the classical complex has cohomology entirely in degree zero by (24.11). Each finite $\hbar$ quotient of (24.16) is built by successive extensions with associated graded copies of the classical complex. Induction on the quantum weight yields

$$
H^q(\mathcal O_{\mathrm{free}}^{\mathrm q}(I)/\hbar^N)=0
\quad(q\ne0).
\tag{24.19}
$$

The maps on degree-zero cohomology in the finite tower indexed by powers of $\hbar$ are surjective by the long exact sequences, because the classical $H^1$ vanishes. Therefore the degree-zero cohomology tower is Mittag–Leffler and its derived first inverse limit vanishes. Passing to the complete limit with respect to powers of $\hbar$ gives

$$
H^q(\mathcal O_{\mathrm{free}}^{\mathrm q}(I))=0
\quad(q\ne0).
\tag{24.20}
$$

Its degree-zero cohomology is a complete filtered deformation of the **polynomial** space $\mathrm{Sym}(\mathbb R^2)$, with associated graded $\mathrm{Sym}(\mathbb R^2)[\hbar]$ for the filtration by powers of $\hbar$. As a module it is a formal deformation in $\hbar$; we do not identify its same-open multiplication with the classical commutative polynomial product, because the BV differential is second-order and the quantum factorization multiplication is defined on disjoint opens.

**Important:** This is an all-cohomological-degrees result for the free BV observable complex itself, not a proof that arbitrary *higher liquid Ext* groups of test-function sources commute with support colimits.

## 7. Honest comparison ledger

| Obligation | Verdict |
| --- | --- |
| Actual free-scalar two-term observable complex and differentiable plots | CONSTRUCTED; source-backed |
| Smooth regular versus distributional polynomial cochain comparison | PROVED ALL COHOMOLOGICAL DEGREES, classical (24.1) |
| Complete arity filtration and B.6.0.7/B.6.0.11 | PROVED (24.2) |
| Exact higher-cohomology of classical polynomial observables on an interval | PROVED (24.3), zero outside degree zero |
| Classical Weiss descent, including completed polynomial arity | PROVED (24.4) |
| Formal smeared free BV quantum cochains, smooth factorization maps, $\hbar$ completion | CONSTRUCTED; identities (24.15–24.18) |
| Formal free quantum Weiss descent in all cohomological degrees | PROVED (24.5) via B.6.0.11 |
| Quantum cohomology off degree zero on a connected interval | PROVED ZERO (24.19–24.20) |
| A canonical map identifying earlier real-liquid RHom complexes 022 with these differentiable polynomial observables | **NOT CONSTRUCTED; OPEN** (different variance and source) |
| General higher real-liquid Ext support comparison and completed interacting BV/renormalized theories | **OPEN** |
| Natural quantization of *all* distributional polynomial kernels | **NOT CLAIMED**; diagonal products obstruct it |

**Mathematical conclusion:** For the explicitly defined *one-dimensional free scalar* model, the smooth classical comparison and Weiss descent are verified at the actual differentiable-pro-cochain level. The formal smeared free BV quantization satisfies smooth B.6 compatibility for completion in $\hbar$ and Weiss descent in all cohomological degrees. The true remaining programme gap is a **typed and naturally defined bridge from this B.6 theory to the earlier liquid derived mapping objects**, followed by higher real-liquid Ext support comparison and any genuinely interacting/renormalized extension. Nothing in 024 silently provides that bridge.
