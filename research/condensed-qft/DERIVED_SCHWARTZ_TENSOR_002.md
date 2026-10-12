# QFT-COND-002 — Derived Schwartz tensor comparison in real liquid vector spaces

**Disposition:** **PROVED BY REDUCTION TO PUBLISHED THEOREMS**, not a novel theorem.  
**Precise object-level conclusion:** **YES**, in the stable derived category of real p-liquid modules, for Schwartz spaces on finite-dimensional Euclidean spaces.  
**Provenance:** [QFT-COND-002](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2599), following [QFT-COND-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2596).  
**Limits:** no claim for arbitrary Banach spaces, uncountably generated products, distributions with singular multiplication, free BV observables, or Weiss descent. No Lean certification is asserted.

## 1. The central result, correctly typed

Fix a real number $p$ with $0<p\le 1$. Let

$$
\mathcal L_p=\mathrm{Liq}_p(\mathbb R)
$$

be the abelian category of $p$ -liquid condensed real vector spaces, in the sense of Clausen–Scholze. The tensor product in this category is the **liquid** tensor product, here denoted by $\otimes_{\mathbb R,<p}^{\mathrm{liq}}$. Its derived symmetric monoidal category is

$$
\mathcal D_p=D(\mathcal L_p),
$$

with monoidal product $\otimes_{\mathbb R,<p}^{\mathbb L}$. These structures and the exact fully faithful embedding into derived condensed real vector spaces are established in Scholze's *Lectures on Analytic Geometry*, Theorem 6.5. The $p$ parameter is fixed, not varied in a hidden comparison.

Let $\mathrm{NFr}_{\mathbb R}$ denote the ordinary category of **real nuclear Fréchet spaces** and continuous real-linear maps. Define the realization

$$
\Phi_p(E)=\underline E[0]\in\mathcal D_p.
$$

This is well-typed: the condensed realization of a nuclear Fréchet space is $p$ -liquid for every $0<p\le1$, as described in Clausen–Scholze, *Condensed Mathematics and Complex Geometry*, Remark 4.12 (and Section 2, on inverse limits of Banach spaces). The association is functorial on continuous real-linear maps. This functor is defined only on the stated source category; it is not claimed to be exact on the entire nonabelian category of locally convex spaces.

For integers $a,b\ge1$ define $E_a=\mathcal S(\mathbb R^a,\mathbb R)$ and $E_b=\mathcal S(\mathbb R^b,\mathbb R)$ with their classical nuclear Fréchet topologies.

**Theorem DC-1 (derived Schwartz comparison, sourced).** There is a canonical equivalence in $\mathcal D_p$,

$$
\boxed{
\Phi_p(E_a)\otimes_{\mathbb R,<p}^{\mathbb L}\Phi_p(E_b)
\;\simeq\;
\Phi_p\!\left(\mathcal S(\mathbb R^{a+b},\mathbb R)\right).
}\tag{DC-1}
$$

The equivalence is induced by the jointly continuous bilinear external product

$$
E_a\times E_b\longrightarrow\mathcal S(\mathbb R^{a+b},\mathbb R),
\qquad (f,g)\longmapsto ((x,y)\mapsto f(x)g(y)).
$$

It is an **object-level** derived equivalence, not merely an equivalence after applying scalar-valued Hom.

### Proof

**Step A — membership and tensor flatness.** The spaces $E_a,E_b$ are nuclear Fréchet, hence their condensed realizations are $p$ -liquid. More strongly, Clausen–Scholze's *Condensed Mathematics and Complex Geometry*, Theorem 4.11 and Remark 4.12 (p. 46 in the cited PDF), establish that nuclear Fréchet spaces are **flat for the liquid tensor**. Therefore the exact degree-zero $p$ -liquid objects $\underline{E_a}$ and $\underline{E_b}$ compute their derived tensor in degree zero:

$$
\underline{E_a}[0]\otimes_{\mathbb R,<p}^{\mathbb L}
\underline{E_b}[0]
\simeq
\left(\underline{E_a}\otimes_{\mathbb R,<p}^{\mathrm{liq}}
\underline{E_b}\right)[0].
$$

Here the absence of higher Tor comes from liquid tensor flatness, *not* the unrelated fact that the ordinary algebraic tensor of real vector spaces is exact.

**Step B — liquid tensor comparison.** The same Remark 4.12 states that on nuclear Fréchet spaces the liquid tensor product agrees with their **usual completed topological tensor product**:

$$
\underline{E_a}\otimes_{\mathbb R,<p}^{\mathrm{liq}}
\underline{E_b}
\cong
\underline{E_a\widehat\otimes_\pi E_b}.
$$

This is an isomorphism of **p-liquid condensed modules**, not merely a bijection at the one-point profinite test object. The role of trace-class inverse-limit presentations is critical in the source proof.

**Step C — classical Schwartz tensor theorem.** Classical nuclear-space theory gives the topological isomorphism

$$
E_a\widehat\otimes_\pi E_b
\cong
\mathcal S(\mathbb R^{a+b},\mathbb R)
$$

under the external product. Applying condensed realization and combining with Steps A and B proves (DC-1). Its naturality follows from the universal properties of the source comparison and the continuous bilinear external product. $\square$

**Derived consequence.** The comparison morphism, defined by the external product followed by the universal property of the liquid tensor, has zero cone:

$$
\mathrm{Cone}(\mathrm{comparison}_{a,b})\simeq0,
\qquad
\mathrm{Tor}^{\mathrm{liq}}_i(\underline E_a,\underline E_b)=0
\quad(i>0).
$$

The degree-zero cohomology is canonically $\underline{\mathcal S(\mathbb R^{a+b})}$, and all other cohomology groups vanish.

**Source status:** This argument is a **direct application** of already published Clausen–Scholze results and the classical Schwartz tensor theorem. GCL may claim a carefully typed **application and proof audit**, not mathematical priority.

## 2. Explicit infinite-dimensional model: Hermite coefficients

The Schwartz comparison is **not** a disguised finite-dimensional approximation. A concrete description makes that testable.

For $d\ge1$, let $I_d=\mathbb N_0^d$ and $|\nu|=\nu_1+\cdots+\nu_d$. Expanding in tensor products of one-dimensional Hermite functions gives a topological isomorphism

$$
\mathcal S(\mathbb R^d,\mathbb R)
\cong
s(I_d):=
\left\{
(c_\nu)_\nu:\ \sup_{\nu\in I_d}(1+|\nu|)^k|c_\nu|<\infty
\text{ for every integer }k\ge0
\right\}.
$$

This is the standard Hermite characterization of Schwartz functions; it is not an innovation of condensed mathematics. Hermite coefficients are real for real-valued test functions.

An especially transparent source-compatible $p$ -liquid inverse system is obtained by taking

$$
q=p/2,\qquad L_d\in\mathbb N,\qquad L_dq>d,
\qquad \lambda_\nu=(1+|\nu|)^{-L_d}.
$$

With $I=I_d$ countable, all $\lambda_\nu$ are nonzero. The multiplier is $q$ -summable because the number of multiindices with $|\nu|=n$ equals $\binom{n+d-1}{d-1}$, and

$$
\binom{n+d-1}{d-1}
=\prod_{j=1}^{d-1}\frac{n+j}{j}
\le(n+1)^{d-1}.
$$

It follows that

$$
\sum_{\nu\in I_d}|\lambda_\nu|^q
=
\sum_{n=0}^\infty
\binom{n+d-1}{d-1}(n+1)^{-L_dq}
\le
\sum_{n=0}^\infty(n+1)^{d-1-L_dq}
<\infty.
$$

For an explicit rational-exponent certificate, take $p=1$, $q=1/2$ and $L_d=2(d+1)$; then the last bound becomes

$$
\sum_{\nu\in I_d}|\lambda_\nu|^{1/2}
\le\sum_{n=0}^{\infty}(n+1)^{-2}
\le2.
$$

Define the tower $T_d$ with terms $\mathcal M_{<p}(I_d)$ and transition maps given by multiplication by $\lambda$:

$$
\cdots
\xrightarrow{\lambda}
\mathcal M_{<p}(I_d)
\xrightarrow{\lambda}
\mathcal M_{<p}(I_d).
$$

**Tower identification (specialized source construction).** The resulting inverse limit, as a condensed real vector space, is the realization of the rapidly decreasing sequence space $s(I_d)$. At the one-point test object this is immediate from the characterization

$$
(c_\nu)\in s(I_d)
\iff
\forall k\ge0:\ ((1+|\nu|)^{kL_d}c_\nu)_\nu
\in\mathcal M_{<p}(I_d)(*).
$$

For the nontrivial condensed/sheaf-valued upgrade, one uses the trace-class/sequence-space replacement and inverse-limit arguments in Lemma 4.7, the remarks preceding Theorem 4.11, and Remark 4.12. This is **not** inferred solely from the displayed pointwise equality. In particular, the source proves the necessary vanishing of the derived $\varprojlim^1$ through its dense-image Mittag–Leffler lemma (Lemma 4.8).

**What the tower computes.** Applying Theorem 4.11 to $T_a$ and $T_b$ gives a liquid tensor inverse limit indexed by $I_a\times I_b$, whose transition weights are $\lambda_\nu\lambda'_\mu$. Since

$$
1+|\nu|+|\mu|
\le
(1+|\nu|)(1+|\mu|)
\le
(1+|\nu|+|\mu|)^2,
$$

the rapidly decreasing topology on $I_a\times I_b$ agrees with that on $\mathbb N_0^{a+b}$, up to cofinal polynomial seminorms (if $L_a\ne L_b$, compare exponents using their maximum and minimum). This recovers the right side of (DC-1).

**Care:** the explicit index/tower presentation is noncanonical (it chooses Hermite coordinates and weights); the resulting equivalence from the external product is canonical. Source Theorem 4.11/Remark 4.12, not a finite truncation experiment, is the authority for flatness and the p-liquid tensor computation.

## 3. Precise distinction from the earlier pilot

The previous [TK-1](ANALYTIC_TENSOR_KERNEL_001.md) established only

$$
\mathrm{Hom}_{\mathrm{CondMod}_{\underline{\mathbb R}}}
(\underline E_a\otimes_{\underline{\mathbb R}}\underline E_b,\underline{\mathbb R})
\cong\mathcal S'(\mathbb R^{a+b}).
$$

It did **not** identify objects or establish any higher-Tor vanishing. DC-1 improves that **logical scope** by using the **different, p-liquid monoidal category**, the actual analytic tensor, and flatness. It does not establish a stronger result than the original Clausen–Scholze source.

The previous TK-2 used Scholze's $\mathcal M$ -complete category and Banach projective tensor. That underived tensor cannot simply be substituted into $\mathcal D_p$. DC-1's flatness and derived equivalence come from the liquid source theorems; the categories are not being conflated.

The previous massless covariance counterexample TK-2b was a failure of boundedness on $L^2$, **not** a counterexample to DC-1. The Schwartz-space derived tensor equivalence persists at $m=0$ because the test-space comparison does not depend on a mass parameter. Infrared behavior of a covariance, especially existence of a massless inverse on given function/distribution spaces, is a separate analytical question.

## 4. Exact source audit and novelty boundary

| Duty | Primary source / evidence | Status |
| --- | --- | --- |
| $p$ -liquid abelian and derived symmetric monoidal categories | Scholze, *Lectures on Analytic Geometry* (2026), Theorem 6.5 | Established, imported |
| $p$ -liquidity of complete locally convex inverse-limit spaces | Clausen–Scholze, *Condensed Mathematics and Complex Geometry* (2026), Lecture II; Scholze, *Analytic*, Lectures II–VI | Established, imported |
| Flatness and tensor of prescribed countable diagonal inverse limits | Clausen–Scholze, *Complex Geometry*, Theorem 4.11, p. 46 | Established, imported |
| General nuclear Fréchet p-liquid flatness and completed tensor | Clausen–Scholze, *Complex Geometry*, Remark 4.12, p. 46 | Established, imported |
| Vanishing $\mathbf R^1\varprojlim$ in the relevant dense-image towers | Clausen–Scholze, *Complex Geometry*, Lemma 4.8, pp. 43–44 | Established, imported |
| Hermite expansion identifies Schwartz with rapidly decreasing multi-sequences | Classical Hermite/Schwartz spectral theory | Established, imported |
| Schwartz completed projective tensor theorem | Classical Schwartz/Grothendieck kernel and nuclear-space theory | Established, imported |
| Exact shell-counting bound for chosen tower weights | The elementary inequalities in §2, reproducible exact arithmetic fixture | Proven directly |
| DC-1 application to Schwartz spaces in $D(\mathrm{Liq}_p(\mathbb R))$ | Composition of the preceding source theorems | Proven here as a sourced corollary; **not novel** |
| General BV factorization or locality/descent transfer | Neither source theorem supplies this | **OPEN** |
| Interacting renormalized fields / gauge/BV local-to-global | Neither source theorem supplies this | **OPEN** |

**Primary source URLs:**

- https://arxiv.org/abs/2605.11731 — Clausen and Scholze, *Condensed Mathematics and Complex Geometry* (2026 stable edition), especially Theorem 4.11, Remark 4.12, and Lecture IV Exercise 5.
- https://people.mpim-bonn.mpg.de/scholze/Complex.pdf — source PDF; printed page 46 has Theorem 4.11 and Remark 4.12.
- https://arxiv.org/abs/2605.03655 — Scholze, *Lectures on Analytic Geometry* (2026 stable edition), Theorem 6.5.
- https://mathoverflow.net/questions/500784 — Peter Scholze's September 2025 answer explicitly states the tensor comparison for nuclear Fréchet spaces and test-function/distribution examples.
- https://www.mdpi.com/2227-7390/3/2/527 — background for Hermite/Schwartz spaces.
- https://academic.oup.com/qjmath/article/76/4/1189/8252976 — published erratum warning that completed tensor is not generally exact in all locally convex spaces: do not generalize flatness outside the source hypotheses.

## 5. Replay, adversarial boundaries, and interpretation

**Fixture:** Run \`python3 research/condensed-qft/fixtures/hermite_liquid_tower.py\`. It checks the exact multiindex shell counts, the finite-level summability domination, and product weights (with an deliberately invalid exponent). It does not simulate condensed objects or certify the full theorem. Infinite-dimensional correctness is mathematical, established by the sources and argument above.

**Known negative boundary (not counterexample to DC-1):** Clausen–Scholze, Lecture IV, Exercise 6, notes a failure of the natural liquid tensor comparison for products $\prod_I\mathbb R$ and $\prod_J\mathbb R$ when $I$ is uncountable and $J$ infinite. Thus the **countable/nuclear Fréchet** hypotheses are substantive. We do not promote an exercise statement into an independently certified new proof without separately discharging it.

**Physical interpretation:** for Gaussian field theory, multi-variable Schwartz test functions and their distribution kernels can now be transported through a *derived* symmetric monoidal analytic category without creating artificial higher Tor from tensoring the test spaces. This is **a rigorous consistency check of the analytic substrate**, not a proof that interacting quantum observables, coincidence limits, renormalized products or Weiss descent are preserved.

**Next genuine discovery gate:** construct the free BV/prefactorization observable assignment $U\mapsto\mathrm{Obs}(U)$ over suitable opens, with compactly supported test complexes, continuous differentials and completed symmetric powers. Test whether $\Phi_p$ preserves the **actual** required homotopy-colimit/descent and Wick/propagator operations, not only individual two-factor nuclear tensors. A nonzero obstruction would be meaningful; a positive theorem exceeding the literature would require source audit and independent certification.

## 6. Acceptance and publication policy

- Claim level: **source-backed mathematical corollary** (not novel independent discovery).
- Verification: exact-source theorem-number and hypotheses audit; explicit weight proof; deterministic exact fixture; Markdown math parser gate.
- No axiom/Lean certificate, external specialist mathematical signoff or new physics prediction is asserted.
- Exact protected head, review/admission and deployed MkDocs mathematical painting must be checked separately.
