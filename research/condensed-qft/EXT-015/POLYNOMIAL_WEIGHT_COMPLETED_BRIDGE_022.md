# EXT-015D / 022 — a completed polynomial-sector bridge through cohomological degree one

**Disposition:** PROVED, for real-liquid linear derived mapping complexes with sources given by *classical completed projective symmetric tensor powers* of the fixed nuclear Fréchet test-function space, that the **completed weight-by-weight support comparison** induces isomorphisms on $H^0$ and $H^1$. This supplies a bounded **positive** complement to the completion and Milnor hostile controls in [021](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md). **NOT PROVED:** equivalence of Costello–Gwilliam B.6 smooth multilinear cochain objects, higher liquid Ext, or Weiss descent.

**Inherited mathematical inputs:** [LFO-013 degree-zero factorization](../LFO3_SURJECTIVITY_THEOREM_013.md), [positive degree-one Ext comparison 019](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md), and [critical audit 020](AGENT_CRITICAL_REVIEW_019_020.md). Nuclear sequence-space tensor reference: Dietmar Vogt, [*The Tensor Algebra of the Space s*](https://popups.ulg.ac.be/0037-9565/index.php?id=2298), *Bull. Soc. R. Sci. Liège* 70 (2001), 435–440; Zinaida Lykova, [*Cyclic cohomology of certain nuclear Fréchet and DF algebras*](https://arxiv.org/abs/0704.1019), Example 6.7, records the completed tensor square of $s$ as the rapid-decay matrix space.

## 1. The actual homogeneous Fréchet sources

Fix $K=[-1,1]$, $H=\mathcal D_K(\mathbb R)$ and $0<p\le1$. For each **integer polynomial weight** $w\ge0$, define a Fréchet space

$$
E_w=
\begin{cases}
\mathbb R,&w=0,\\
\mathrm{Sym}^w_\pi(H),&w\ge1,
\end{cases}
\tag{22.1}
$$

where $\mathrm{Sym}^w_\pi(H)$ denotes the **classical** completed projective symmetric tensor power, obtained as the image of the finite-group symmetrizing idempotent on $H^{\widehat\otimes_\pi w}$. Write $\underline{E_w}$ for its real-liquid realization. We do **not** assume without comparison that this object is the categorical symmetric power under an arbitrary liquid monoidal structure.

**Lemma 22.1 (homogeneous sources are retracts of the fixed test-function source).** For every $w\ge1$, $\underline{E_w}$ is a retract in the real-liquid category of an object isomorphic to the original $\underline H$.

**Proof.** By the source-checked Valdivia–Vogt Fréchet isomorphism already used in [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md), $H\cong s$, where $s$ is the Fréchet space of rapidly decreasing sequences. The standard nuclear Köthe tensor-product theorem, recorded in the references above, gives

$$
s\widehat\otimes_\pi s
\cong s(\mathbb N^2),
\tag{22.2}
$$

the rapidly decreasing matrix space. A polynomially bounded Cantor pairing bijection $\mathbb N^2\cong\mathbb N$ identifies the matrix seminorms with the one-index rapid-decay seminorms: the index and its inverse have polynomial coordinate-growth bounds. Hence $s(\mathbb N^2)\cong s$ topologically. Iteration gives $H^{\widehat\otimes_\pi w}\cong s\cong H$ for each **fixed finite** $w\ge1$.

The symmetrizer

$$
e_w=\frac1{w!}\sum_{\sigma\in\mathfrak S_w}U_\sigma
$$

is a continuous linear idempotent on the completed projective tensor power. Its image $E_w$ is a continuous complemented Fréchet subspace, with explicit inclusion and projection. Real-liquid realization preserves this splitting, so $\underline{E_w}$ is a direct summand of the realization of the tensor power, which is isomorphic to $\underline H$. $\square$

The lemma is about each fixed finite weight. It does **not** produce a single uniform topological isomorphism simultaneously in all weights.

## 2. Transfer the admitted liquid result to each polynomial weight

**Theorem 22.2 (homogeneous first-Ext support comparison).** For every $w\ge0$ and $q=0,1$, with $G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)}$ and $G=\varinjlim_bG_b$, the canonical map

$$
\varinjlim_b
\mathrm{Ext}^q_{\mathcal A_p}(\underline{E_w},G_b)
\longrightarrow
\mathrm{Ext}^q_{\mathcal A_p}(\underline{E_w},G)
\tag{22.3}
$$

is an isomorphism, where $\mathrm{Ext}^0=\mathrm{Hom}$.

**Proof.** At weight zero the source is $\underline{\mathbb R}$, a projective compact liquid generator. Its first Ext vanishes, and degree-zero Hom is evaluation on the singleton; finite-support exhaustion gives the desired Hom comparison.

For $w\ge1$, Lemma 22.1 gives $\underline H\cong\underline{E_w}\oplus Z_w$ for some real liquid summand $Z_w$. For any target $T$, the natural first-Ext and Hom functors split as finite direct products

$$
\mathrm{Ext}^q(\underline H,T)
\cong
\mathrm{Ext}^q(\underline{E_w},T)
\oplus
\mathrm{Ext}^q(Z_w,T).
$$

The colimit comparisons are compatible with inclusion and retraction. Their direct sum is an isomorphism by [LFO-013](../LFO3_SURJECTIVITY_THEOREM_013.md) for $q=0$ and [019–020](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md) for $q=1$. A retract of an isomorphism is an isomorphism; thus the comparison for $\underline{E_w}$ is an isomorphism. $\square$

This is an **actual real-liquid** statement; the tensor sources themselves are classical nuclear Fréchet realizations. No scalar Ext-vanishing hypothesis or Continuum Hypothesis is used.

## 3. Completed polynomial-weight comparison

For each $w$, choose a projective resolution $P_{w,\bullet}\to\underline{E_w}$ in $\mathcal A_p$ and define the complex of real vector spaces

$$
C_{b,w}^{\bullet}=\mathrm{Hom}_{\mathcal A_p}(P_{w,\bullet},G_b),
\qquad
C_w^\bullet=\mathrm{Hom}_{\mathcal A_p}(P_{w,\bullet},G).
\tag{22.4}
$$

Its cohomology computes genuine liquid Ext, not a Fréchet-only extension theory. Define the **weight-completed support-colimit comparison**

$$
\Phi:
\varprojlim_N\varinjlim_b
\left(\bigoplus_{w<N}C_{b,w}^{\bullet}\right)
\longrightarrow
\prod_{w\ge0}C_w^\bullet.
\tag{22.5}
$$

**Theorem 22.3 (bounded positive bridge).** The map $\Phi$ induces an isomorphism on $H^0$ and $H^1$:

$$
H^q(\Phi):
\varprojlim_N\varinjlim_b
\left(\bigoplus_{w<N}
\mathrm{Ext}^q_{\mathcal A_p}(\underline{E_w},G_b)\right)
\xrightarrow{\ \sim\ }
\prod_{w\ge0}
\mathrm{Ext}^q_{\mathcal A_p}(\underline{E_w},G),
\qquad q=0,1.
\tag{22.6}
$$

In the source of (22.6), the displayed inverse limit of Ext groups is canonically the cohomology of the inverse-limit complex in (22.5); this relies on the finite-prefix maps being **split surjective**.

**Proof.** For every finite $N$, a filtered colimit of finite direct sums of complexes equals the finite sum of the filtered colimits:

$$
\varinjlim_b\bigoplus_{w<N}C_{b,w}^{\bullet}
\cong
\bigoplus_{w<N}\varinjlim_bC_{b,w}^{\bullet}.
$$

Taking the inverse limit over the split finite-prefix projections gives the product complex

$$
\varprojlim_N\varinjlim_b
\bigoplus_{w<N}C_{b,w}^{\bullet}
\cong
\prod_w\varinjlim_bC_{b,w}^{\bullet}.
\tag{22.7}
$$

Products of real vector spaces are exact; hence the cohomology of a product of cochain complexes is the product of their cohomologies. Filtered colimits of real vector spaces are also exact. Therefore the map on cohomology is the product of the individual comparisons (22.3), all isomorphisms for $q=0,1$ by Theorem 22.2. This proves (22.6). The inverse-limit tower in (22.7) has **split projections**, so the Roos $\varprojlim^1$ term of its cohomology tower is zero; compare the counterexample in [021](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md), where the maps on $H^0$ were not Mittag–Leffler. $\square$

**Important order-of-operations guard:** Do not replace the left side of (22.5) with the *uncompleted* $\varinjlim_b\prod_wC_{b,w}^\bullet$. The [actual fixed-source liquid example in 021](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md) shows that this generally loses weight families with no uniform output-support cutoff even in cohomological degree zero.

## 4. What this does, and does not, give Costello–Gwilliam

The sources $E_w$ encode continuous **symmetric multilinear maps of degree** $w$ on $H$ through the completed projective tensor universal property. That makes (22.6) a rigorous algebraic bridge for a natural **linearized homogeneous polynomial sector**. The target cochains in (22.4) are *real-liquid derived Hom complexes*. They have not been identified with the complete, smoothly enriched cochains in Costello–Gwilliam Appendix B.6.

In particular, the following are **not** consequences of Theorem 22.3:

- A comparison of projective versus liquid completed tensor products as monoidal objects in *all* derived degrees.
- Smoothness of the B.6.1.1 nonlinear plots or multilinear operations merely because a linear map is continuous.
- Differentiable cofibration or fibration conditions from B.6.0.7, or the quasi-isomorphism-on-fibers conditions of B.6.0.11.
- A quasi-isomorphism in cohomological degrees $q\ge2$ for arbitrary $E_w$.
- Quantum BV interactions, renormalization, Weiss descent or a complete factorization-algebra equivalence.

The distinction matters: Theorem 22.3 handles the **correct weight completion** and genuine liquid cohomological degrees zero and one; the remaining B.6 comparison must preserve the differentiable structure and verify the higher-derived/Weiss gates independently.

## 5. Reviewable boundary and research continuation

| Question | Status |
| --- | --- |
| Tensor stability of $s$ and continuous symmetric projector | PROVED (22.1) |
| Each fixed polynomial weight, real-liquid Ext degrees zero and one, support comparison | PROVED (22.3) |
| Weight-completed polynomial cochain comparison in cohomological degrees zero and one | PROVED (22.6), algebraic cochain-model level |
| Uncompleted support colimit comparison | FALSE in general; [actual liquid counterexample 021](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md) |
| Actual B.6 smooth multilinear pro-cochain equivalence | OPEN |
| Higher liquid Ext for these symmetric tensor sources | OPEN |
| Completed quantum observables and Weiss descent | OPEN |

**Next agent-owned mathematical obligation:** Fix the concrete *free linear field theory* observables on nested intervals with their differentiable plot structure. Compare their finite quantum-weight quotients with the source-side complexes above, giving an exact map of smooth multilinear cochains; verify B.6.0.7 cofibrations/fibrations, B.6.1.1 plotwise smoothness and the finite-filtration fibers. A cochain-level identification is needed before applying B.6.0.11 or extending the result to Weiss descent. No Human Steward review assignment is required.
