# QFT-COND-001 / TENSOR-KERNEL-001 — Restricted analytic-condensed comparison

**Status:** mathematically proved **restricted comparison**, contingent only on precisely attributed published source theorems. **Not novel**: the new content here is the explicit assembly and limitation audit, not a new nuclear tensor theorem or new result in QFT.  
**Source of record:** [QFT-COND-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2596).  
**Scope:** real scalar coefficients; ordinary condensed category, Scholze's quasiseparated $\mathcal M$ complete category, and finite free objects in a liquid (parameter $p$) derived category. No claim about arbitrary derived completed tensor products or interacting fields.

> **Successor result (QFT-COND-002):** [Derived Schwartz tensor comparison](DERIVED_SCHWARTZ_TENSOR_002.md) proves the previously open **infinite-dimensional** Schwartz comparison as an object-level equivalence in $D(\mathrm{Liq}_p(\mathbb R))$; see Clausen–Scholze, *Complex Geometry*, Theorem 4.11 and Remark 4.12. This does not transfer the statement to the earlier $\mathcal M$ -complete Banach category or establish a new QFT observable theorem. The material below remains the intentionally more restricted TK-1 to TK-4 predecessor.

## 0. Outcome at a glance

This note constructs **three precisely distinguished** realizations and establishes:

1. **Schwartz kernel comparison (all $a,b\ge1$, infinite-dimensional):** the scalar-valued maps *out of the ordinary condensed tensor* of the two Schwartz spaces are canonically the tempered distribution kernels on the product. This proves a Hom-level comparison; **it does not prove an object-level tensor equivalence**.
2. **Banach analytic tensor comparison (arbitrary real Banach spaces):** the tensor of the two associated $\mathcal M$ complete condensed real spaces is canonically the condensed realization of their completed projective Banach tensor. This is Scholze's Proposition 4.10; we transport the free massive scalar covariance through it.
3. **Infrared boundary:** at zero mass the same $L^2$ bounded covariance construction fails, with an explicit Fourier-annulus counterexample. 
4. **Derived tensor comparison (finite-dimensional only):** finite free liquid (parameter $p$) modules are tensor-flat as finite sums of the monoidal unit, so there are no higher Tor terms. This is not a statement about infinite-dimensional Schwartz spaces.
5. **No-go control:** derived ordinary $\mathbb Z$ solidification kills the condensed topological real line. It is therefore not a conservative coefficient realization for real free-field observables.

In particular, the status of the original **infinite-dimensional derived Schwartz tensor** question remains **OPEN**. None of the established isomorphisms below is passed off as that theorem.

## 1. Definitions and precise ambient categories

Fix a sufficiently large but controlled cardinal/site for condensed modules as in the source references; size changes are not asserted to be harmless without the standard accessibility setup.

For a metrizable real topological vector space $E$ write $\underline E$ for its associated condensed $\underline{\mathbb R}$ -module,

$$
\underline E(S)=\mathrm{Cont}(S,E)
$$

for profinite $S$ (with pointwise vector-space operations). The ordinary condensed tensor is the tensor in the Grothendieck abelian category

$$
\mathrm{CondMod}_{\underline{\mathbb R}}.
$$

The canonical condensed-realization functor on metrizable spaces is fully faithful as a functor of underlying spaces by Scholze, *Lectures on Analytic Geometry*, Proposition 1.2(2). Hence it is fully faithful on continuous real-linear maps and on jointly continuous real-bilinear maps when the product of source spaces remains metrizable.

**Analytic Banach realization.** Let $\mathcal A_{\mathcal M}$ denote Scholze's category of *quasiseparated $\mathcal M$ complete condensed real vector spaces*, as in *Lectures on Analytic Geometry*, Definition 4.1. It carries the projective tensor $\otimes_{\pi,\mathcal M}$ defined by Proposition 4.9, characterized by its universal property for bilinear maps into another $\mathcal M$ complete object. For a real Banach space $V$,

$$
j_{\mathcal M}(V)=\underline V\in\mathcal A_{\mathcal M}.
$$

For real Banach $V,W$, Scholze's Proposition 4.10 supplies a canonical natural isomorphism

$$
\boxed{\quad
j_{\mathcal M}(V)\otimes_{\pi,\mathcal M}j_{\mathcal M}(W)
\;\cong\;
j_{\mathcal M}(V\widehat\otimes_\pi W).
\quad}\tag{A}
$$

Here $\widehat\otimes_\pi$ on the right is the **classical completed projective Banach tensor**. The category $\mathcal A_{\mathcal M}$ is not asserted to be abelian or stable, and its underived tensor is **not** decorated with a derived symbol.

**Finite derived realization.** Fix $0<p\le1$ and use the (source-proved) analytic ring of liquid (parameter $p$) real vector spaces; write $\mathcal D_p=D(\mathrm{Liq}_p(\mathbb R))$ with its derived symmetric monoidal tensor $\otimes^{\mathbb L}_{\mathrm{Liq}_p}$. Its unit is the liquid (parameter $p$) real coefficient object $\underline{\mathbb R}$ in degree zero. On finite-dimensional spaces set

$$
j_p(\mathbb R^n)=\underline{\mathbb R}^{\oplus n}[0].
$$

This definition does **not** define $j_p$ on arbitrary Schwartz spaces. In particular, (A) and the finite derived calculation below take place in different ambient categories. The agreement on finite free coefficients is insufficient to identify all their tensors.

## 2. Restricted Schwartz kernel comparison

Let $E_a=\mathcal S(\mathbb R^a,\mathbb R)$ with the usual nuclear Fréchet topology, $a\ge1$. Define $\mathrm{Bil}_{c}(E_a,E_b;\mathbb R)$ to be the real vector space of **jointly continuous** real-bilinear functionals.

**Theorem TK-1 (Hom-level condensed Schwartz kernel comparison).** For all positive integers $a,b$ there is a canonical natural isomorphism of real vector spaces

$$
\boxed{\quad
\mathrm{Hom}_{\mathrm{CondMod}_{\underline{\mathbb R}}}
\bigl(\underline{E_a}\otimes_{\underline{\mathbb R}}
\underline{E_b},\underline{\mathbb R}\bigr)
\;\cong\;
\mathcal S'(\mathbb R^{a+b},\mathbb R).
\quad}\tag{TK-1}
$$

The map sends a condensed scalar-valued bilinear functional to its unique classical distribution kernel.

**Proof.** By the defining universal property of the tensor in condensed modules, the left side is the space of morphisms

$$
\underline{E_a}\times\underline{E_b}\longrightarrow\underline{\mathbb R}
$$

that are $\underline{\mathbb R}$ linear in each argument. Since $E_a$ and $E_b$ are Fréchet and metrizable, so is $E_a\times E_b$; moreover, $\underline{E_a\times E_b}\cong\underline{E_a}\times\underline{E_b}$. By full faithfulness of condensed realization on metrizable topological spaces (Scholze, Proposition 1.2(2)), those morphisms correspond **bijectively** to jointly continuous bilinear maps $E_a\times E_b\to\mathbb R$. Thus the left side equals $\mathrm{Bil}_{c}(E_a,E_b;\mathbb R)$.

By the universal property of the completed locally convex projective tensor product,

$$
\mathrm{Bil}_{c}(E_a,E_b;\mathbb R)
\cong
\bigl(E_a\widehat\otimes_\pi E_b\bigr)'_{\mathrm{cont}}.
$$

The classical nuclear Schwartz tensor-product theorem gives a topological isomorphism

$$
E_a\widehat\otimes_\pi E_b\cong
\mathcal S(\mathbb R^{a+b},\mathbb R),
\qquad f\otimes g\longmapsto ((x,y)\mapsto f(x)g(y)).
$$

Its continuous linear dual is the space of real tempered distributions on $\mathbb R^{a+b}$. The composite proves (TK-1). Naturality is with respect to continuous real-linear maps between the stated test spaces when the induced tensor/kernel pullbacks are defined. $\square$

**Critical boundary.** TK-1 is an isomorphism of vector spaces of **scalar-valued functionals**. We have **not** shown

$$
\underline{E_a}\otimes_{\underline{\mathbb R}}\underline{E_b}
\stackrel{?}{\cong}\underline{E_a\widehat\otimes_\pi E_b},
$$

nor a tensor equivalence in a stable analytic derived category. In general, knowing all maps to **one** target $\underline{\mathbb R}$ does not prove that two condensed modules are isomorphic: the purported comparison morphism must be constructed and checked against a detecting family, not just a scalar dual.

The theorem is **not a new Schwartz kernel theorem**. Its proof is a careful formal interface between two established results.

## 3. Analytic Banach tensor and the massive free-field covariance

Let $d\ge1$, $m>0$, and $H=L^2(\mathbb R^d,\mathbb R)$ with the usual real Hilbert-space topology. Under the Fourier convention

$$
\widehat f(p)=\int_{\mathbb R^d}e^{-ip\cdot x}f(x)\,dx,
\qquad
\|f\|_2^2=(2\pi)^{-d}\int|\widehat f(p)|^2\,dp,
$$

define

$$
B_m(f,g)
=\frac1{(2\pi)^d}\int_{\mathbb R^d}
\frac{\overline{\widehat f(p)}\,\widehat g(p)}
{|p|^2+m^2}\,dp.
$$

For real $f,g$, this is a real-valued bilinear form (although its Fourier presentation uses complex-valued transforms).

**Theorem TK-2 (infinite-dimensional analytic-condensed free covariance).** The following assertions hold.

1. $B_m$ is real-bilinear, symmetric, positive and bounded with sharp bilinear operator norm $\|B_m\|=m^{-2}$.
2. It determines a unique morphism in the explicitly chosen $\mathcal M$ complete category,

   $$
   \boxed{\quad
   \beta_m:
   j_{\mathcal M}(H)\otimes_{\pi,\mathcal M}j_{\mathcal M}(H)
   \longrightarrow
   j_{\mathcal M}(\mathbb R).
   \quad}\tag{TK-2}
   $$

3. Under (A) this is exactly the classical continuous linear functional

   $$
   \widetilde B_m:H\widehat\otimes_\pi H\longrightarrow\mathbb R.
   $$

4. Restricting the bilinear form along $\mathcal S(\mathbb R^d,\mathbb R)\hookrightarrow H$ yields the unique tempered Schwartz kernel $K_m\in\mathcal S'(\mathbb R^{2d},\mathbb R)$ with

   $$
   \langle K_m,f\otimes g\rangle=B_m(f,g).
   $$

   In distribution notation $K_m(x,y)=k_m(x-y)$ where

   $$
   \widehat{k_m}(p)=\frac1{|p|^2+m^2}.
   $$

**Proof.** Plancherel and Cauchy–Schwarz, using $0<(p^2+m^2)^{-1}\le m^{-2}$, show

$$
|B_m(f,g)|\le m^{-2}\|f\|_2\|g\|_2.
$$

Positivity and symmetry follow from the real Fourier multiplier; equivalently, $B_m(f,g)=\langle f,G_m g\rangle_{L^2}$ where $G_m=\mathcal F^{-1}M_{(|p|^2+m^2)^{-1}}\mathcal F$ is a bounded positive self-adjoint operator. Its norm is the essential supremum of its multiplier, $m^{-2}$: any nonzero Fourier-space $L^2$ function supported in a sufficiently small ball around $0$ approaches this bound. Therefore the bilinear norm is exactly $m^{-2}$.

By the universal property of the projective Banach tensor, $B_m$ corresponds uniquely to $\widetilde B_m\in(H\widehat\otimes_\pi H)'$. Applying $j_{\mathcal M}$ and the canonical isomorphism (A), proved in the cited Scholze source, gives exactly one $\mathcal A_{\mathcal M}$ morphism $\beta_m$. Thus this step is not a conjectural application of an unnamed "condensed completion."

The continuous injection $\mathcal S(\mathbb R^d)\hookrightarrow L^2(\mathbb R^d)$ makes the restricted $B_m$ jointly Schwartz-continuous. Apply TK-1, or equivalently the classical Schwartz kernel theorem, to obtain the unique $K_m$. The Fourier multiplier formula identifies its translation-invariant distribution kernel; it is well-defined and tempered because $(|p|^2+m^2)^{-1}$ is bounded and of at most polynomial growth. $\square$

**What is genuinely infinite-dimensional here?** $H$ is an infinite-dimensional Banach/Hilbert space. Hence TK-2 is an actual object-level analytic-condensed completed-tensor comparison, not just the trivial case of finite free modules. Its proof, however, imports rather than improves Scholze's general Banach theorem, so no new QFT theorem is claimed.

**Distribution caution.** For some $d$, $k_m$ is singular at the origin; the kernel need not be an ordinary function on the diagonal. This does not define Wick square or renormalized coincident-point products.

### TK-2b: an exact failure in the massless Banach construction

**Proposition TK-2b (infrared counterexample).** If $m=0$, the Fourier multiplier $|p|^{-2}$ does **not** define a bounded bilinear form $B_0$ on $H=L^2(\mathbb R^d,\mathbb R)$ for any $d\ge1$. Thus the particular Banach-level analytic-condensed morphism of TK-2 does not exist for the massless covariance, without changing its domain or codomain.

**Proof.** Fix $0<\varepsilon<1$. Choose any nonzero real Schwartz function $f_\varepsilon$ whose Fourier transform is supported inside the annulus $\varepsilon<|p|<2\varepsilon$; by symmetric choice of Fourier profile the inverse transform can be real. Normalize $\|f_\varepsilon\|_{L^2}=1$. On this support, $|p|^{-2}\ge(2\varepsilon)^{-2}$, hence

$$
B_0(f_\varepsilon,f_\varepsilon)
=\frac1{(2\pi)^d}\int
\frac{|\widehat f_\varepsilon(p)|^2}{|p|^2}\,dp
\ge \frac1{4\varepsilon^2}.
$$

The lower bound diverges as $\varepsilon\downarrow0$, proving unboundedness. A bounded functional on $H\widehat\otimes_\pi H$ would give a bounded bilinear form on $H\times H$, a contradiction. $\square$

**Scope:** this rules out the unmodified $L^2$ Banach projective-tensor realization of this covariance, not every massless distributional propagator or every possible infrared-regularized analytic realization. For $d\ge3$, $|p|^{-2}$ is locally integrable near $p=0$, and the corresponding tempered distribution can be treated separately. For low dimensions, extensions/zero-mode treatment require additional care. It is **a known analytic infrared phenomenon**, not a new quantum-field result.

**Replay:** \`python3 research/condensed-qft/fixtures/massive_spectral_bounds.py\` checks positive-mass finite spectral multipliers and the exact $\varepsilon^{-2}$ lower-bound scaling with rational arithmetic. The continuum conclusion is established by the preceding proof, *not* by finite samples.

## 4. Finite free derived comparison — and no further

**Proposition TK-3.** In the fixed source-proven liquid (parameter $p$) derived category $\mathcal D_p$, for all finite $n,k\ge0$,

$$
\boxed{\quad
j_p(\mathbb R^n)\otimes^{\mathbb L}_{\mathrm{Liq}_p}
j_p(\mathbb R^k)
\simeq j_p(\mathbb R^{nk})
\quad}\tag{TK-3}
$$

canonically, and the object is concentrated in degree zero.

**Proof.** By definition the two inputs are finite direct sums of $n$ and $k$ copies of the symmetric monoidal unit $\underline{\mathbb R}[0]$. The tensor functor in any stable symmetric monoidal category is bi-exact and preserves finite direct sums, while $\mathbf1\otimes\mathbf1\simeq\mathbf1$. Thus the tensor of two finite free units is a sum of $nk$ units, concentrated in degree zero. Identifying $\mathbb R^n\widehat\otimes_\pi\mathbb R^k\simeq\mathbb R^{nk}$ recovers the classical finite-dimensional completed tensor. $\square$

The proof applies to **finite free objects only**. It supplies **no** assertion that $\Phi(\mathcal S(\mathbb R^a))$ is liquid (parameter $p$), has an exact/monoidal realization, or has zero derived Tor with another Schwartz object. In particular, do not use (TK-3) as a derived proof of (TK-1) or (TK-2).

## 5. Obstruction to the wrong category: ordinary solidification

Let $L(-)^{\square}:D(\mathrm{Cond}(\mathrm{Ab}))\to D(\mathrm{Solid})$ denote **derived ordinary $\mathbb Z$ solidification**, not the analytic $\mathcal M$ completion of Sections 1–3.

**Proposition TK-4 (no-go, imported from Scholze).** The condensed additive group of the real line satisfies

$$
L(\underline{\mathbb R})^{\square}\simeq0.
$$

Consequently $L(\underline{\mathbb R}^{\oplus n})^\square\simeq0$ for every finite $n$. In particular, ordinary derived $\mathbb Z$ solidification cannot be a faithful realization of the real scalar coefficient object, even on finite-dimensional real Gaussian degrees of freedom.

**Proof.** The displayed vanishing is *Lectures on Condensed Mathematics*, Corollary 6.1(iii), and is not proved anew here. The derived solidification is a left adjoint and preserves finite direct sums; apply it to each summand. The source coefficient $\underline{\mathbb R}$ is nonzero because its value at the one-point profinite set is $\mathbb R\ne0$. Thus the proposed realization is not conservative even on the scalar coefficient. $\square$

**Important qualification:** the fact that an individual source object is killed does **not** produce a counterexample to a particular comparison morphism if *both* sides are mapped to zero. It is a counterexample to **faithful scalar realization**, the physically essential property. Do not claim more.

## 6. Source ledger and authority of each statement

| Claim | Status | Dependency |
| --- | --- | --- |
| TK-1: condensed scalar Hom $\leftrightarrow$ tempered kernels | **Proved conditional on published theorems** | Full faithfulness [Scholze, *Analytic*, Prop. 1.2(2)] + ordinary tensor universal property + classical Schwartz tensor/kernel theorem |
| TK-2: analytic Banach tensor and free covariance | **Proved conditional on published theorems** | [Scholze, *Analytic*, Def. 4.1, Props. 4.9–4.10] + Fourier/Plancherel/Cauchy–Schwarz |
| TK-2b: massless unboundedness on $L^2$ | **Proved directly (classical infrared phenomenon)** | Fourier annulus localization and Plancherel | 
| TK-3: finite free derived liquid tensor | **Proved conditional on analytic-ring monoidality** | [Scholze, *Analytic*, Thm. 6.5 and analytic-ring formalism] + monoidal unit/finite-sum identities |
| TK-4: ordinary solidification kills reals | **Imported established theorem** | [Scholze, *Condensed*, Cor. 6.1(iii)] |
| Infinite-dimensional derived Schwartz tensor equivalence | **OPEN** | Requires definition of $\Phi$ in a stable analytic category and comparison at the object level |
| Factorization observables/descent transport | **OPEN** | Requires free BV observable complexes, coherence and Weiss descent |
| New QFT invariant, obstruction class, or prediction | **NOT ESTABLISHED** | No new physics result may be inferred from this note |

### Primary sources (stable 2026 editions)

1. P. Scholze, *Lectures on Analytic Geometry*, May 2026, Sections 1, 4, 6: https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf. **Exact imported boundaries:** Proposition 1.2(2) (fully faithful metrizable condensed realization); Definition 4.1, Propositions 4.9–4.10 ($\mathcal M$ complete projective tensor and Banach comparison); Theorem 6.5 and Appendix to Lecture VI (liquid analytic-ring category).
2. P. Scholze, *Lectures on Condensed Mathematics*, arXiv:2605.03658v1 (2026), Corollary 6.1(iii): https://arxiv.org/abs/2605.03658. **Exact imported boundary:** derived ordinary solidification of the topological real line vanishes.
3. Classical Schwartz kernel/nuclear tensor theorem, for example Richard Melrose's *Schwartz' kernel theorem* notes or standard distribution theory references. **Exact imported boundary:** $\mathcal S(\mathbb R^a)\widehat\otimes_\pi\mathcal S(\mathbb R^b)\cong\mathcal S(\mathbb R^{a+b})$ and continuous bilinear maps correspond to unique tempered distribution kernels.

Do **not** treat the 2026 editions of sources as novel results dated 2026; both are stable presentations of older Clausen–Scholze material.

## 7. New work that remains genuinely capable of producing a theorem

**Next attempt (TK-5, unproved):** specify a stable analytic category (for example, a fixed liquid (parameter $p$) theory), and construct a functor on a narrowly defined class of nuclear Fréchet test spaces into that category. **Before** claiming a tensor isomorphism:

1. Exhibit the actual image of $\mathcal S(\mathbb R^d)$ and establish whether it is liquid and how to compute it.
2. Construct a well-typed canonical map

   $$
   \Phi(E_a)\otimes^{\mathbb L}_{\mathcal D_p}\Phi(E_b)
   \longrightarrow \Phi(E_a\widehat\otimes_\pi E_b).
   $$

3. Determine whether its cone vanishes on a specified test family. Check both higher homology and degree-zero completeness. Compare against a detecting collection, not only scalar maps.
4. Independently seek a counterexample involving non-nuclear Banach spaces or failure of projective tensor exactness, while keeping the classical and derived hypotheses distinct.
5. Only then analyze disjoint-region structure maps and Weiss descent in the corresponding free BV observable construction.

**Success criterion:** a true restricted derived comparison with exact hypotheses, or an explicit nonzero cone/counterexample. A restatement of TK-1 or Scholze's Proposition 4.10 **does not** satisfy the novelty gate.

**Prior-art/new-claim verdict:** TK-1 through TK-4 are well-supported restricted benchmarks, but **no novel theorem** has yet been certified. This note completes the initial construction/comparison obligation **only in its explicitly restricted (underived and finite-derived) forms**.
