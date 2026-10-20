# EXT-015D / D14 / 028 — restricted smooth duals, higher-Ext syzygies and regulated distributional BV

**Disposition:** Three independent mathematical outputs. (A) An explicit **parameter-plot enrichment** for continuous scalar duals of arbitrary real Fréchet spaces, extending the nuclear free-field *source class*, without asserting a universal functor on all liquid modules. (B) An exact **dimension-shifting reduction** of the original higher liquid Ext stage-comparison problem to first Ext for specified syzygies; the syzygy comparison itself remains OPEN. (C) A **positive-scale BV construction on every compactly supported distributional polynomial kernel**, a rigorous obstruction to preserving ordinary disjoint-open multiplication with any nonzero smooth regulator, and an explicit **Wick-corrected formal factorization algebra** obtained by conjugation with a smooth double antiderivative. The UV limit on the unrestricted distributional space is shown to fail on a specified diagonal class. These are free-field results, not an interacting renormalization theorem.

**Programme sources:** [D10 proof 026](VARIANCE_OBSTRUCTION_SCALAR_DUAL_BRIDGE_026.md), [GCL critical audit 027](AGENT_CRITICAL_REVIEW_D10_027.md), [smooth free field 024](FREE_SCALAR_DIFFERENTIABLE_WEISS_024.md). Primary analytic category: Peter Scholze, [*Lectures on Analytic Geometry*, Theorem 6.5, printed p. 35](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf). Primary regulator/factorization context: Costello–Gwilliam, [*Factorization Algebras in Quantum Field Theory*, Volume II, §7.2.3 (heat kernels) and §7.2.4 (parametrices)](https://people.math.umass.edu/~gwilliam/factorization2.pdf), and Volume I, Appendix B.2/B.6. The proofs below do not infer their conclusions solely from these references.

## 1. Beyond nuclearity: a representable differentiable dual for any Fréchet source

Let $E$ be **any** real Fréchet space, not necessarily nuclear. For every finite-dimensional smooth manifold $M$, define

$$
\mathcal P_E(M)
=\operatorname{Hom}_{\mathrm{Liq}_p(\mathbb R)}
\bigl(\underline E,\underline{C^\infty(M)}\bigr)
\cong L_{\mathrm{cts}}\bigl(E,C^\infty(M)\bigr).
\tag{28.1}
$$

The right-hand isomorphism is Fréchet full faithfulness, **not** an isomorphism of arbitrary liquid internal Hom objects. It makes $\mathcal P_E$ into a contravariant functor on parameter manifolds: a smooth map $f:M'\to M$ acts by postcomposing with $f^*:C^\infty(M)\to C^\infty(M')$.

**Theorem 28.1 (Fréchet-scalar differentiable enrichment).** Formula (28.1), with differentiation in the output parameter space, defines a differentiable vector-space plot structure on the continuous scalar dual $E'$ for **every** real Fréchet $E$. It is natural **contravariantly** under continuous linear source maps $E\to F$. For $E=C^\infty(V)$ it recovers *exactly* the compactly supported distributional smooth-plot rule of Costello–Gwilliam B.2.1.1.

**Proof.** At the point $M=*$, (28.1) is $L_{\mathrm{cts}}(E,\mathbb R)=E'$. Pullback of smooth functions preserves continuity and respects compositions and identities. If $M=\bigcup M_i$, the sheaf gluing theorem for $C^\infty$ and its initial Fréchet topology show that linear operators $E\to C^\infty(M_i)$ agreeing on overlaps glue uniquely to a continuous $E\to C^\infty(M)$: every seminorm on the latter tests derivatives on compact subsets of finitely many $M_i$. For coordinate derivatives $\partial_{x_j}$, postcomposition $E\to C^\infty(M)\xrightarrow{\partial_{x_j}}C^\infty(M)$ defines a flat connection; mixed partials commute. A continuous map $E\to F$ induces $F'\to E'$ by precomposition, and likewise on plots. When $E=C^\infty(V)$, the right side of (28.1) is literally the DVS plot formula for compact distributions in B.2.1.1. $\square$

**Boundary:** Nuclearity is unnecessary for this **dual plot functor**, but is crucial for identifying finite tensor powers with spaces of smooth kernels on Cartesian products. For a general Banach space $E$, we do **not** assert $E^{\widehat\otimes_\pi n}=C^\infty(V^n)$ or identify dual tensor powers with all compact distributional kernels. Likewise this theorem does not turn arbitrary non-Fréchet liquid objects into differentiable vector spaces or prove that $\mathcal P_E$ is exact on nonsplit short exact sequences. On split Fréchet direct sums its compatibility is immediate.

## 2. Original test-function-valued higher liquid Ext: an exact, honest syzygy gate

Return to the original liquid source $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$, compact-support output stages $G_b$ and their union $G$, and $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$. Scholze's Theorem 6.5 ensures enough projectives. Choose an actual projective epimorphism $P_0\twoheadrightarrow H$ with kernel $K_0$, and recursively projective epimorphisms $P_i\twoheadrightarrow K_{i-1}$ with kernels $K_i$.

**Theorem 28.2 (higher-degree support comparison is precisely a syzygy Ext¹ comparison).** For every $q\ge2$ there is a natural commutative diagram of canonical isomorphisms

$$
\begin{array}{ccc}
\varinjlim_b\mathrm{Ext}^q_{\mathcal A_p}(H,G_b)
&\longrightarrow&
\mathrm{Ext}^q_{\mathcal A_p}(H,G)\\
\big\downarrow\wr&&\big\downarrow\wr\\
\varinjlim_b\mathrm{Ext}^1_{\mathcal A_p}(K_{q-2},G_b)
&\longrightarrow&
\mathrm{Ext}^1_{\mathcal A_p}(K_{q-2},G).
\end{array}
\tag{28.2}
$$

**Proof.** From $0\to K_0\to P_0\to H\to0$, $\mathrm{Ext}^j(P_0,-)=0$ for all $j>0$, so the natural long exact Ext sequence gives $\mathrm{Ext}^q(H,T)\cong\mathrm{Ext}^{q-1}(K_0,T)$ for $q\ge2$ and every $T$. Repeat the same argument for $0\to K_1\to P_1\to K_0\to0$ until first Ext is reached. Every connecting map is natural in the coefficient $T$. Apply it to each $G_b$ and to $G$, then pass through the filtered colimit of ordinary abelian groups. The resulting square is (28.2). $\square$

This is a **complete reduction, not a solution of arbitrary higher liquid Ext**. In particular, at degree two the missing theorem is exactly the filtered-output Ext¹ comparison for $K_0$. There is no justification for applying the earlier fixed **Fréchet-source** theorem 019 to $K_0$ without proving it has the same analytic properties; a kernel of a projective liquid cover is not automatically a nuclear Fréchet realization. This is the exact work needed to advance the original higher-degree line.

## 3. Regularized BV contraction on every compact distributional kernel

Work on open intervals $U\subseteq\mathbb R$ and the genuine distributional two-term linear-observable complex

$$
L_{\mathrm{dist}}(U):
\quad\mathcal E'(U)^{-1}
\xrightarrow{D=\partial_x^2}
\mathcal E'(U)^0,
\tag{28.3}
$$

where $\mathcal E'(U)$ is the continuous dual of $C^\infty(U)$, hence compactly supported distributions. Let $A_{\mathrm{dist}}(U)$ denote the **completed-kernel polynomial graded symmetric algebra**: at every finite arity its terms are compactly supported graded distributional kernels on $U^n$ with the appropriate finite permutation invariants. This is **not** merely the algebraic symmetric tensor algebra of individually decomposable distributions; it includes distributions correlated along all diagonals. The differential $d$ applies $D$ to an odd generator and is extended as a graded derivation.

Choose an **even** $\kappa\in C_c^\infty(\mathbb R)$ with $\int\kappa=1$ and $\kappa(0)>0$. For $\epsilon>0$ put

$$
\kappa_\epsilon(t)=\epsilon^{-1}\kappa(t/\epsilon),
\qquad
K_\epsilon(x,y)=\kappa_\epsilon(x-y).
\tag{28.4}
$$

For arbitrary compactly supported distributional tensors, contraction in one even and one odd variable using the smooth function $K_\epsilon$ is an unambiguous push-forward after multiplication by a smooth function. Summing over all even–odd pairs (with Koszul signs) defines the odd second-order operator $\Delta_\epsilon$ on $A_{\mathrm{dist}}(U)$. All operations preserve compact support of the remaining variables. If a family of compact distributions is smooth in the DVS sense, contracting with a smooth fixed kernel produces a smooth family: the map on plots is postcomposition of a continuous operator $C^\infty(U^{n-2})\to C^\infty(U^n)$ given by multiplication by the kernel and insertion of the unaffected variables.

The relation $\partial_x^2 K_\epsilon=\partial_y^2 K_\epsilon$ implies the standard free BV relations

$$
[d,\Delta_\epsilon]=0,\qquad
\Delta_\epsilon^2=0.
\tag{28.5}
$$

These may also be verified by the **exact conjugation** below, which derives rather than assumes them. Hence $(A_{\mathrm{dist}}(U)[[\hbar]],d+\hbar\Delta_\epsilon)$ is a well-defined formal complete differentiated cochain complex at **every positive** scale.

## 4. Locality no-go for the uncorrected multiplication

**Theorem 28.3 (no nonzero strictly local smooth BV regulator under ordinary multiplication).** Let $K\in C^\infty(U\times U)$ be a smoothing kernel defining an odd contraction between even and odd compact distributions. If the **ordinary graded symmetric multiplication of extension-by-zero observables** is a cochain map for **every** pair of disjoint subintervals $U_1,U_2\subset U$ with differential $d+\hbar\Delta_K$, then $K=0$.

**Proof.** For distinct $x\ne y$ choose disjoint neighborhoods $U_1\ni x$ and $U_2\ni y$. Let $a=\delta_x$ be an even linear distributional generator and $b=\delta_y$ an odd linear generator. The second-order BV operator kills each single generator, but

$$
\Delta_K(ab)
-\Delta_K(a)b-a\Delta_K(b)
=K(x,y).
\tag{28.6}
$$

If their ordinary multiplication were a cochain map for the quantum differentials, its cross term would vanish, so $K(x,y)=0$ for every $x\ne y$. Thus $K$ vanishes on the dense open complement of the diagonal. Continuity forces it to vanish also on the diagonal. $\square$

For the specific compactly supported regulator (28.4), the uncorrected multiplication **does** give a chain map for pairs of observables whose compact supports are separated by a distance greater than $\epsilon$ times the support radius of $\kappa$. But there is no **uniform** positive scale that works for every pair of observables on arbitrary disjoint opens with touching boundaries. This is a precise local-to-global limitation, not a refutation of positive-scale BV complexes themselves.

## 5. The constructive remedy: a smooth Wick primitive and corrected factorization

Define the **even symmetric smooth propagator kernel**

$$
P_\epsilon(x,y)
=\frac12\int_{\mathbb R}|x-y-t|\,\kappa_\epsilon(t)\,dt
=\bigl(\tfrac12|\cdot|*\kappa_\epsilon\bigr)(x-y).
\tag{28.7}
$$

As a convolution of a distribution with a compact smooth function, $P_\epsilon$ is $C^\infty$, even and symmetric in $x,y$, with

$$
\partial_x^2P_\epsilon(x,y)=
\partial_y^2P_\epsilon(x,y)=K_\epsilon(x,y).
\tag{28.8}
$$

The kernel has at most linear growth at infinity; pairing it with **compactly supported distributions** is always defined. Let $B_\epsilon$ be the **even degree-zero second-order operator** on $A_{\mathrm{dist}}(U)$ that contracts pairs of **even** generators using $P_\epsilon$; normalize so that $B_\epsilon(ab)=\langle a\boxtimes b,P_\epsilon\rangle$ for any two even linear generators $a,b$. For arbitrary compact distributional tensor kernels its action is again smooth multiplication and push-forward, so it is defined on **all** polynomial kernels.

**Lemma 28.4 (exact BV commutator).**

$$
[B_\epsilon,d]=\Delta_\epsilon,\qquad
[B_\epsilon,\Delta_\epsilon]=0.
\tag{28.9}
$$

**Proof.** On an even generator and an odd generator their product has $d(a b)=a(D b)$, so $B_\epsilon d(ab)=\langle a\boxtimes D b,P_\epsilon\rangle=\langle a\boxtimes b,\partial_y^2P_\epsilon\rangle=\langle a\boxtimes b,K_\epsilon\rangle$, whereas $dB_\epsilon(ab)=0$. On a product of arbitrary even and odd kernels, expand by the second-order contraction rule: contractions of two even factors cancel between $B_\epsilon d$ and $dB_\epsilon$, leaving precisely the mixed even–odd contractions using $D P_\epsilon=K_\epsilon$. The sign for each contraction is the graded Koszul sign from moving the odd factor. As $B_\epsilon$ and $\Delta_\epsilon$ are constant-kernel contraction differential operators, their graded commutator vanishes (they involve commuting even contractions and at most one odd derivative). The same reasoning gives $\Delta_\epsilon^2=0$. These formulas hold directly on arbitrary distributional kernels because both sides are compositions of the **same continuous smooth-kernel pullback and push-forward operators**; no density of decomposable distributional tensors is assumed. $\square$

Let

$$
W_\epsilon=\exp(\hbar B_\epsilon).
\tag{28.10}
$$

This is **well-defined on $A_{\mathrm{dist}}(U)[[\hbar]]$**: every polynomial arity has only finitely many nonzero powers of the arity-lowering operator $B_\epsilon$ and each fixed power of $\hbar$ receives finitely many contributions. Its inverse is $\exp(-\hbar B_\epsilon)$.

**Theorem 28.5 (a genuine positive-scale distributional Wick prefactorization algebra).** On every open interval, the quantum differential

$$
d_\epsilon=d+\hbar\Delta_\epsilon
\tag{28.11}
$$

is conjugate to the classical differential:

$$
d_\epsilon=W_\epsilon\,d\,W_\epsilon^{-1}.
\tag{28.12}
$$

For pairwise disjoint opens $U_1,\ldots,U_r\subset V$, define the **corrected**, scale-dependent factorization structure map

$$
\mu^{(\epsilon)}_{U_1,\ldots,U_r\subset V}
=
W_{\epsilon,V}
\circ
\mu^{\mathrm{cl}}_{U_1,\ldots,U_r\subset V}
\circ
\bigotimes_{i=1}^r W_{\epsilon,U_i}^{-1}.
\tag{28.13}
$$

Then the collection $(A_{\mathrm{dist}}(U)[[\hbar]],d_\epsilon,\mu^{(\epsilon)})$ is a genuine **smooth formal $\hbar$-adically complete differentiable prefactorization algebra** at every fixed $\epsilon>0$. Its structure maps are chain maps, associative and equivariant under permutations, compatible with open inclusions and smoothly multilinear on the DVS parameter plots. Reduction modulo $\hbar$ is the original classical distributional prefactorization algebra.

**Proof.** The Baker–Campbell–Hausdorff series truncates after the first commutator because of (28.9):

$$
W_\epsilon dW_\epsilon^{-1}
=d+\hbar[B_\epsilon,d]
=d+\hbar\Delta_\epsilon.
$$

The reference classical multiplication $\mu^{\mathrm{cl}}$ is a smooth cochain map for $d$; conjugating its inputs and output by chain isomorphisms gives a cochain map for $d_\epsilon$. All prefactorization associativity/unit/permutation diagrams commute after this conjugation, since the middle $W_\epsilon^{-1}W_\epsilon$ factors cancel in each compositional diagram. Extension by zero commutes with $B_\epsilon$ because its smooth kernel is the restriction of the **same global translation-invariant kernel** to every open. Thus unary inclusions retain their canonical extension-by-zero form, and the construction is compatible across opens. Smoothness follows from the plotwise fixed smooth-kernel operations noted above. Each quantum coefficient is finite in the formal $\hbar$ filtration, and its quotient projections are smoothly split as **graded** DVS objects. $\square$

The key difference from the false construction ruled out in Theorem 28.3 is that $\mu^{(\epsilon)}$ is generally **not ordinary multiplication**: it contains cross-propagator Wick contractions. This is how smooth regularization and genuine factorization coexist.

## 6. Exact scale transport, and the UV limit that still fails

For any two scales $\epsilon,\eta>0$, define

$$
\mathcal R_{\epsilon\to\eta}
=W_\eta W_\epsilon^{-1}
=\exp\!\left(\hbar B_{P_\eta-P_\epsilon}\right).
\tag{28.14}
$$

**Theorem 28.6 (strict scale cocycle).** The $\mathcal R_{\epsilon\to\eta}$ are isomorphisms of the differentiable prefactorization algebras from Theorem 28.5, with

$$
\mathcal R_{\eta\to\zeta}\,
\mathcal R_{\epsilon\to\eta}
=\mathcal R_{\epsilon\to\zeta},
\qquad
\mathcal R_{\epsilon\to\epsilon}=\mathrm{id}.
\tag{28.15}
$$

**Proof.** By (28.12), $W_\eta W_\epsilon^{-1}$ intertwines the two differentials; by (28.13), it intertwines all their factorization structure maps. All operators $B_P$ commute because they are even constant-kernel contractions, so their exponentials add. The identities follow exactly. $\square$

Because $\kappa$ is even, normalized, and compactly supported, $P_\epsilon(t)=|t|/2$ whenever $|t|$ exceeds the support radius of $\kappa_\epsilon$. Thus **the scale-change propagator** $P_\eta-P_\epsilon$ is itself smooth and **compactly supported** in the relative coordinate $x-y$, even though each $P_\epsilon$ has a noncompact linear tail. This is an exact bounded-range property of the **change of scale**, not strict locality of the individual positive-scale BV contraction.

**Theorem 28.7 (unrestricted distributional ultraviolet no-go).** Neither $\Delta_\epsilon$ nor $B_\epsilon$ has a finite coefficientwise limit as $\epsilon\downarrow0$ on **all** compactly supported distributional polynomial kernels.

**Proof.** At any $x_0\in U$, take the product of an even and an odd delta distribution, both supported at $x_0$. Then

$$
\Delta_\epsilon\bigl(\delta_{x_0}^{\mathrm{even}}
\delta_{x_0}^{\mathrm{odd}}\bigr)
=K_\epsilon(x_0,x_0)
=\frac{\kappa(0)}{\epsilon}
\longrightarrow+\infty.
\tag{28.16}
$$

For $B_\epsilon$, use the two-even distributional kernel $\delta_{x_0}''\boxtimes\delta_{x_0}$. Its contraction yields $\partial_x^2P_\epsilon(x_0,x_0)=\kappa(0)/\epsilon$. Both coefficients diverge. Thus there is no operatorwise UV limit on the unrestricted distributional model. The formal Wick factorization family is **well-defined for every positive scale** and canonically comparable between positive scales, but **renormalized zero-scale extension requires a smaller domain or counterterms**. $\square$

This result does **not** claim that UV renormalization is impossible. It proves that the **uncorrected** $\epsilon\downarrow0$ operator limit on all compactly supported distributions is impossible.

## 7. Mathematical contract and remaining programme boundary

| Obligation | Exact result |
| --- | --- |
| D14-E: extend natural scalar-dual DVS plots beyond nuclear smooth fields | PROVED for arbitrary real Fréchet source, *only* its scalar continuous dual |
| D14-H: higher original target-valued liquid Ext stage comparison | REDUCED EXACTLY to syzygy first-Ext stage comparison in each degree; NOT SOLVED for syzygies |
| D14-BV: positive-scale BV on arbitrary compact distributional polynomial kernels | CONSTRUCTED and PROVED for every $\epsilon>0$ |
| D14-LOC: ordinary disjoint-open multiplication is a quantum cochain map for every smoothing kernel | **REFUTED** for every nonzero smooth kernel |
| D14-WICK: corrected smooth $\hbar$-complete distributional prefactorization and scale-change isomorphisms | CONSTRUCTED and PROVED, including exact cocycle |
| D14-UV: unrestricted zero-scale limit exists | **REFUTED**, explicit diagonal divergence |
| D14-Q: interacting renormalized quantum theory; zero-scale extension with counterterms; higher Ext for original syzygies | OPEN |

**Next GCL mathematical task:** Classify the microlocally admissible and/or renormalized distributional subspaces for the $\epsilon\to0$ limit; prove compatibility with the exact Wick scale cocycle and the B.6 differentiable filtration. Independently attack the **explicit liquid first-Ext comparison for the first projective syzygy $K_0$** identified in (28.2). The general dual plot functor (28.1) does not, by itself, imply a monoidal/liquid-derived equivalence beyond the nuclear class. No routine Human Steward mathematical approval is required.
