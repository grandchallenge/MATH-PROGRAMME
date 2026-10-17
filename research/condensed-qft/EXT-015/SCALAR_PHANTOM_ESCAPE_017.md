# QFT-COND-005 / EXT-015C — scalar-phantom obstruction and exact escaping example 017

**GCL mathematical status:** PROVED auxiliary liquid counterexample, plus an exact two-channel obstruction for the specified fixed Fréchet source. **The principal fixed-test-function-source Ext¹ surjectivity problem remains OPEN.** This is a research deduction by the GCL mathematics function, not a worker RESULT/1 or mathematical certification from an external body.

**Guiding question:** Can an extension carry genuinely global analytic information that no compact-support stage can capture?

**Mathematical baseline:** [agent critical review 016](AGENT_CRITICAL_REVIEW_AB_016.md), admitted in [PR #2740](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2740); earlier fixed-Fréchet Hom theorem [LFO-013](../LFO3_SURJECTIVITY_THEOREM_013.md). The source-specific goal is still the degree-one comparison in [SPEC](SPEC.md). No claims about smooth Costello–Gwilliam B.6 mappings are made here.

## 1. Concrete scalar objects in the real liquid category

Fix $0<p\le 1$ and let $\mathcal A=\mathrm{Liq}_p(\mathbb R)$. Set

$$
\mathsf S=\bigoplus_{n\ge 1}\underline{\mathbb R},
\qquad
\mathsf P=\prod_{n\ge 1}\underline{\mathbb R},
\qquad
\mathsf Q=\mathsf P/\mathsf S.
\tag{17.1}
$$

All products, sums and the cokernel are computed in the liquid abelian category. Scholze's *Lectures on Analytic Geometry*, Theorem 6.5, printed page 35, identifies $\underline{\mathbb R}=\mathcal M_{<p}(*)$ as compact projective, and says that the inclusion of liquid real modules into condensed real modules preserves kernels, cokernels and all relevant colimits. The product is the condensed realization of the Fréchet product $\mathbb R^{\mathbb N}$.

The natural map $j:\mathsf S\to\mathsf P$ is a monomorphism. Indeed every section of $\mathsf S$ on a profinite test object comes from some finite direct sum, and finite direct sums embed coordinatewise in $\mathsf P$. Thus

$$
0\longrightarrow\mathsf S
\xrightarrow{j}\mathsf P
\xrightarrow{q}\mathsf Q
\longrightarrow0
\tag{17.2}
$$

is a genuine short exact sequence in $\mathcal A$.

**Lemma 17.1 (nonzero, scalar-invisible quotient).** The liquid object $\mathsf Q$ is nonzero, but

$$
\mathrm{Hom}_{\mathcal A}(\mathsf Q,\underline{\mathbb R})=0,
\qquad
\mathrm{Hom}_{\mathcal A}(\mathsf Q,\mathsf P)=0.
\tag{17.3}
$$

**Proof.** Since $\underline{\mathbb R}$ is projective, evaluation at the singleton is exact in $\mathcal A$. Thus

$$
\mathsf Q(*)\cong
\mathbb R^{\mathbb N}/\mathbb R^{(\mathbb N)}
\ne0.
\tag{17.4}
$$

For any liquid-linear $f:\mathsf Q\to\underline{\mathbb R}$, its composition with $q$ is a map $\mathsf P\to\underline{\mathbb R}$ annihilating $\mathsf S$. The Fréchet realization is fully faithful, so this composite is a continuous linear functional on the product Fréchet space $\mathbb R^{\mathbb N}$. Every such functional depends on only finitely many coordinates. Vanishing on all finitely supported vectors forces the functional to be zero. As $q$ is epic, $f=0$. Finally, $\mathrm{Hom}(\mathsf Q,\mathsf P)=\prod_n\mathrm{Hom}(\mathsf Q,\underline{\mathbb R})=0$ by the product universal property. This establishes (17.3). $\square$

In particular, $\mathsf Q$ is **not** the realization of any nonzero Hausdorff Fréchet space: such a space has a nonzero continuous linear functional by Hahn–Banach. The ordinary separated locally convex quotient of the product by its dense finite-sequence subspace is zero, whereas the liquid categorical quotient is nonzero. This is precisely why a scalar-probe/Baire argument on the quotient $\mathsf Q$ is invalid.

## 2. A genuine escaping liquid extension, with a non-Fréchet source

**Theorem 17.2 (auxiliary counterexample).** The class of (17.2),

$$
\eta\in\mathrm{Ext}^1_{\mathcal A}(\mathsf Q,\mathsf S),
\tag{17.5}
$$

is nonzero and does not lie in the image of any finite-stage group

$$
\mathrm{Ext}^1_{\mathcal A}
\left(\mathsf Q,\bigoplus_{n\le b}\underline{\mathbb R}\right)
\longrightarrow
\mathrm{Ext}^1_{\mathcal A}(\mathsf Q,\mathsf S).
\tag{17.6}
$$

Moreover its image in $\mathrm{Ext}^1(\mathsf Q,\mathsf S/\mathsf S_{\le b})$ is nonzero for every $b$.

**Proof.** If (17.2) split, it would have a right inverse $\mathsf Q\to\mathsf P$, contradicting (17.3) and $\mathsf Q\ne0$. Therefore $\eta\ne0$. Pushing (17.2) along $j:\mathsf S\to\mathsf P$ kills its class: its own middle term provides the required boundary in the long exact Hom–Ext sequence, so $j_*\eta=0$ in $\mathrm{Ext}^1(\mathsf Q,\mathsf P)$.

For each finite prefix $\mathsf S_{\le b}$, its inclusion into $\mathsf P$ admits a coordinate projection retraction $\mathsf P\to\mathsf S_{\le b}$. Therefore the induced map $\mathrm{Ext}^1(\mathsf Q,\mathsf S_{\le b})\to\mathrm{Ext}^1(\mathsf Q,\mathsf P)$ is injective. If $\eta$ came from a finite prefix, its zero push-forward to $\mathsf P$ would force that prefix class to vanish, hence $\eta=0$, a contradiction. The long exact sequence for $0\to\mathsf S_{\le b}\to\mathsf S\to\mathsf S/\mathsf S_{\le b}\to0$ then says the image of $\eta$ in the last target's Ext¹ is nonzero. $\square$

This is a fully genuine liquid-category escaping extension. **It does not solve EXT-015C for $H=\underline{\mathcal D_K(U)}$: its source is $\mathsf Q$, which is not Fréchet.**

## 3. Embed the obstruction into the actual test-function output on the line

Take the strict compact-support liquid test-function object

$$
G=\varinjlim_{b\ge1}\underline{\mathcal D_{[-b,b]}(\mathbb R)}
\cong\underline{\mathcal D(\mathbb R)}.
\tag{17.7}
$$

Choose $x_n=3n$ and smooth compact-support bumps $\phi_n$ supported in $(3n-1,3n+1)$ with $\phi_n(x_n)=1$. Define liquid-linear morphisms

$$
\iota:\mathsf S\longrightarrow G,
\qquad
r:G\longrightarrow\mathsf S
\tag{17.8}
$$

as follows: $\iota$ sends the $n$th scalar summand to its multiple of $\phi_n$; $r$ sends each test function $f$ to the finite sequence $(f(x_n))_n$. Every compact-support stage $G_b$ maps under $r$ into a **finite** scalar prefix, since only finitely many $x_n$ lie in $[-b,b]$. Its finite-stage maps are continuous linear maps of Fréchet spaces, hence liquid. The colimit property constructs $r$, and $r\iota=\mathrm{id}_{\mathsf S}$.

Let $C=\ker r$; then $G\cong\mathsf S\oplus C$. Push forward (17.2) along $\iota$. The resulting exact liquid sequence is explicitly isomorphic to

$$
0\longrightarrow G
\longrightarrow \mathsf P\oplus C
\longrightarrow\mathsf Q
\longrightarrow0
\tag{17.9}
$$

where $G=\mathsf S\oplus C$ embeds by $(s,c)\mapsto(j(s),c)$ and the quotient map is $(u,c)\mapsto q(u)$. It is nonsplit by composing any putative section with the projection to $\mathsf P$ and using (17.3).

**Theorem 17.3 (escaping actual test-function output).** The class

$$
\xi=\iota_*\eta\in\mathrm{Ext}^1_{\mathcal A}(\mathsf Q,G)
\tag{17.10}
$$

does not originate from $\mathrm{Ext}^1(\mathsf Q,G_b)$ for any $b$. Consequently its image in $\mathrm{Ext}^1(\mathsf Q,G/G_b)$ is nonzero for every $b$.

**Proof.** By construction, $r_*\xi=\eta$. If $\xi$ came from stage $G_b$, applying $r_*$ would express $\eta$ as the image of an Ext¹ class from the **finite scalar prefix** containing $r(G_b)$. This contradicts Theorem 17.2. The long exact sequence for $0\to G_b\to G\to G/G_b\to0$ gives persistence in every quotient. $\square$

Thus the **output** in this counterexample is exactly the original programme's test-function output on $\mathbb R$, not an auxiliary ring or an invented coefficient system. The only deliberately weakened hypothesis is the **source**, which is non-Fréchet. A proof of C-positive for fixed nuclear Fréchet $H$ must use that completeness/Baire hypothesis essentially.

## 4. Exact decomposition of the scalar support-escape obstruction for any fixed source

Now let $H$ be **any** liquid source, particularly the genuine fixed test-function Fréchet source of EXT-015. Use the exact sequence (17.2). Put

$$
E_n=\mathrm{Ext}^1_{\mathcal A}(H,\underline{\mathbb R}),
\quad
E=\mathrm{Ext}^1_{\mathcal A}(H,\mathsf S),
\quad
P_H=\prod_{n\ge1}E_n.
\tag{17.11}
$$

The notation $P_H$ in (17.11) is **only a product of Ext groups**, not the projective cover $P_H$ from review 016; below write $\mathscr E(H)=\prod_nE_n$ to avoid that collision.

Define the coordinate map

$$
\rho:E\longrightarrow\mathscr E(H)=\prod_n E_n
\tag{17.12}
$$

using the projections $\mathsf S\to\underline{\mathbb R}$. The first-Ext functor in the **second** variable commutes with products here: take any actual projective presentation of $H$ (Theorem 6.5 provides enough projectives), apply Hom to the product, and use exactness of products of real vector spaces to commute the first-cokernel with products. Thus $\mathrm{Ext}^1(H,\mathsf P)\cong\mathscr E(H)$.

Let

$$
F(H)=\bigoplus_n E_n\ \subseteq E,
\qquad
K(H)=
\frac{\mathrm{Hom}_{\mathcal A}(H,\mathsf Q)}
{\mathrm{im}\bigl(\mathrm{Hom}_{\mathcal A}(H,\mathsf P)
\to\mathrm{Hom}_{\mathcal A}(H,\mathsf Q)\bigr)}.
\tag{17.13}
$$

Here $F(H)\hookrightarrow E$ is the direct sum of the finite-prefix extension groups; its injection is guaranteed by finite-coordinate retractions. The connecting homomorphism for (17.2) identifies $K(H)\cong\ker\rho$.

**Theorem 17.4 (two independent escape channels).** There is a canonical short exact sequence

$$
0\longrightarrow K(H)\longrightarrow
\frac{\mathrm{Ext}^1_{\mathcal A}(H,\mathsf S)}
{\bigoplus_n\mathrm{Ext}^1_{\mathcal A}(H,\underline{\mathbb R})}
\longrightarrow
\frac{\mathrm{im}(\rho)}
{\bigoplus_n\mathrm{Ext}^1_{\mathcal A}(H,\underline{\mathbb R})}
\longrightarrow0.
\tag{17.14}
$$

**Proof.** The long exact sequence of (17.2) identifies $\ker\rho$ with $K(H)$, by exactness at Ext¹ and at Hom into $\mathsf Q$. The image of every finite-prefix Ext group under $\rho$ is the corresponding finitely supported coordinate tuple, and every such tuple is attained; consequently $F(H)\cap\ker\rho=0$ and $\rho(F(H))=\bigoplus_nE_n$. Quotienting the exact sequence $0\to\ker\rho\to E\to\mathrm{im}\rho\to0$ by the finite-prefix subgroup gives (17.14). $\square$

The left channel $K(H)$ consists of **phantom escaping classes**, invisible to all scalar coordinate push-forwards; it is nonzero precisely when some liquid map $H\to\mathsf Q$ does **not** lift to $\mathsf P$. The right channel consists of extension classes with **genuinely infinitely many nonzero scalar component classes**. These are distinct mechanisms; a search only for coordinate-visible classes is not exhaustive.

### Actual fixed compact-support source reduction

Take $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$. The retraction $r:G\to\mathsf S$ from Section 3 induces an injection

$$
\frac{\mathrm{Ext}^1(H,\mathsf S)}
{\bigoplus_n\mathrm{Ext}^1(H,\underline{\mathbb R})}
\ \hookrightarrow\
\mathrm{coker}\left[
\varinjlim_b\mathrm{Ext}^1(H,G_b)
\to\mathrm{Ext}^1(H,G)\right].
\tag{17.15}
$$

Indeed, if a scalar-sum extension becomes finite-stage after $\iota_*$, applying $r_*$ makes it finite-prefix because $r(G_b)$ lies in a finite scalar prefix. Therefore **either nonzero channel in (17.14) is sufficient to refute EXT-015C-positive for the actual connected-line test-function target**.

**What is still unproved:** neither $K(H)\ne0$ nor the existence of an infinite-coordinate class in $\mathrm{im}\rho$ has been established for this fixed Fréchet $H$. Vanishing of both scalar channels would still not settle positive surjectivity for every other component of $G$.

## 5. No-go result for naive infinite-jet/diagonal candidates

Suppose one starts with any countable collection of continuous linear functionals $\lambda_n:H\to\mathbb R$ and builds the product map $\lambda=(\lambda_n):H\to\mathsf P$. Its composition with $q:\mathsf P\to\mathsf Q$ **already has an explicit lift**, namely $\lambda$. Hence its boundary in $\mathrm{Ext}^1(H,\mathsf S)$ is **zero**:

$$
\delta(q\lambda)=0.
\tag{17.16}
$$

This rules out a common but misleading candidate: pointwise unbounded collections of scalar or Borel-jet observables do **not** by themselves produce an escaping liquid extension. One must either construct a genuinely nonliftable morphism $H\to\mathsf Q$ or produce an extension with infinitely many nonzero scalar-coordinate Ext¹ images, accounting for all liquid boundaries.

## 6. Exact verdict and next agent-owned boundary

| Claim | Verdict |
| --- | --- |
| $\mathsf Q$ nonzero and scalar-invisible | PROVED |
| $\mathsf Q\to\mathsf P$ section nonexistent; exact liquid extension (17.2) nonsplit | PROVED |
| Genuine extension (17.9) into $G=\underline{\mathcal D(\mathbb R)}$ escapes all target compact stages for source $\mathsf Q$ | PROVED, NON-FRÉCHET SOURCE |
| Fixed-source scalar escape decomposition (17.14) and sufficient injection (17.15) | PROVED |
| Any diagonal sequence of continuous linear functionals generates nonzero phantom boundary | REFUTED by (17.16) |
| $K(\underline{\mathcal D_{[-1,1]}})\ne0$ or infinitely supported coordinate Ext classes exist | OPEN |
| Fixed-test-function-source C-positive or C-negative | OPEN |

**Next mathematical attack:** For the fixed nuclear Fréchet test-function source $H$, determine whether all maps $H\to\mathsf Q$ lift to the Fréchet product $\mathsf P$, and separately whether $\mathrm{Ext}^1(H,\mathsf S)$ has infinitely coordinate-visible classes. Treat the former as a direct quotient-lifting problem and the latter as a genuine liquid degree-one product/coproduct comparison. These are **GCL mathematical specialist obligations**, not manual Human Steward tasks.

**Reproducibility:** The arguments are categorical diagram chases using the verified compact projective scalar, product-topology continuous dual, finite-stage splitting, and the established strict LF liquid realization. No finite numerical experiment is a substitute for their proofs. Citation: Peter Scholze, *Lectures on Analytic Geometry*, Theorem 6.5 (printed p. 35), and previously admitted [LFO-013](../LFO3_SURJECTIVITY_THEOREM_013.md).
