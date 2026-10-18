# QFT-COND-004 / CF-001 — A descent-compatible complete filtered liquid realization

**Disposition:** **POSITIVE, restricted and source-backed**: the smooth-kernel free massive scalar's quantum-weight completion satisfies Weiss descent **in an explicitly defined complete filtered liquid target**, with the completed Čech coproduct and completed tensor. It is genuinely infinite (contains formal observables of unbounded weight). **Comparison outcome:** the quantum-weight truncations match *term by term* the filtration quotients in Costello–Gwilliam, Vol. 1, §15.1.3 and Appendix B.5–B.6. **NOT proved:** an analytic equivalence of the entire category of differentiable pro-cochain complexes with the liquid target, preservation of all smooth multilinear operations, or compatibility with interacting/renormalized theories. The argument is a restricted repackaging of published formal completed-factorization methods, not an independent novelty claim.

**Research issue:** [QFT-COND-004](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2603).  
**Inputs:** [polynomial BV and Weiss descent](COMPACT_SUPPORT_FACTORISATION_003.md); [quantum weight and ordinary inverse-limit no-go](QUANTUM_WEIGHT_PRO_COMPLETION_004.md); [pro-valued no-go](PRO_VALUED_WEISS_NO_GO_005.md).

> **FC-007 scope correction:** [Triangular filtered dg comparison](TRIANGULAR_FILTERED_COMPARISON_007.md) demonstrates that this split-weight category is **not full or essentially surjective** in the general Costello–Gwilliam complete filtered category. It constructs the exact finite-dimensional triangular alternative and proves Weiss descent propagation across finite filtrations, including filtration-raising differentials. The present restricted completed Weiss theorem remains valid **only in its specified split target**.

## 1. A genuinely completed analytic target

Fix $0<p\le1$ and set

$$
\mathcal C_p=D(\mathrm{Liq}_p(\mathbb R)).
$$

By Scholze's analytic-ring theory, this is a presentable stable symmetric monoidal category whose tensor preserves colimits in each variable. Our **split complete quantum-weight liquid category** is

$$
\mathcal{CF}^{\mathrm{spl}}_p
=
\mathrm{Fun}(\mathbb N_0^{\mathrm{disc}},\mathcal C_p).
\tag{CF1}
$$

An object is a sequence $X=(X_0,X_1,\ldots)$ of derived liquid modules; morphisms are **weight-preserving** maps. Its *formal completed realization*, which is **not** a colimit-preserving forgetful functor, is the underlying product with a specified tail filtration:

$$
\mathrm{Real}_{\Pi}(X)=\prod_{w\ge0}X_w,
\qquad
F^N\mathrm{Real}_{\Pi}(X)=\prod_{w\ge N}X_w.
\tag{CF2}
$$

The finite quotient is canonically

$$
Q_N(X)=\mathrm{Real}_{\Pi}(X)/F^N
\simeq\bigoplus_{w<N}X_w.
\tag{CF3}
$$

Thus $X$ defines a **complete and separated** filtered object with $\mathrm{Real}_{\Pi}(X)\simeq\mathrm{holim}_NQ_N(X)$ in the stable category. The tails and splitting are part of the structure, not ignored after forming the product. This is a restricted subcategory of complete filtered complexes: not every filtered complex splits, and general filtration-preserving maps may mix weights. We do not claim equivalence to the full differentiable pro-cochain category.

Define the **completed Cauchy tensor** by

$$
(X\widehat\otimes_{\mathrm{CF}}Y)_n
=
\bigoplus_{i+j=n}
(X_i\otimes_{\mathbb R,<p}^{\mathbb L}Y_j).
\tag{CF4}
$$

The sum for each fixed $n$ is **finite**. The unit is concentrated in weight zero. In the realized notation,

$$
\mathrm{Real}_{\Pi}(X\widehat\otimes_{\mathrm{CF}}Y)
\simeq
\mathrm{holim}_N\!
\bigoplus_{i+j<N}X_i\otimes_{\mathbb R,<p}^{\mathbb L}Y_j.
\tag{CF5}
$$

The Cauchy product makes $\mathcal{CF}^{\mathrm{spl}}_p$ symmetric monoidal: associativity, braiding and unitality are inherited from finite sums and the symmetric monoidal structure of $\mathcal C_p$. Its tensor preserves **all** colimits in each variable because the component formulas use only colimit-preserving tensor and finite coproducts.

**The critical colimit rule.** Colimits in (CF1) are computed weightwise. For a family $\{X^\alpha\}$, the completed coproduct has realized object

$$
\mathrm{Real}_{\Pi}\!\left(
\bigoplus_{\alpha}^{\mathcal{CF}}X^\alpha
\right)
\simeq
\prod_{w\ge0}
\left(\bigoplus_\alpha X^\alpha_w\right)
\simeq
\mathrm{holim}_N
\bigoplus_\alpha Q_N(X^\alpha).
\tag{CF6}
$$

**Do not substitute** $\bigoplus_\alpha\prod_w X_w^\alpha$ for (CF6). The two can differ on precisely the escaping-support configuration in the previous no-go results.

This is a concrete, computable category, with finite-weight quotients, completed tensor and completed Čech coproduct. It does not simply rename $\mathrm{Pro}(\mathcal C_p)$: morphisms and colimits are different.

## 2. The completed quantum observable assignment

On Euclidean opens $U$ take the compact-support liquid BV complex $E_p(U)$ of QFT-COND-003 for the real massive free scalar $P=-\Delta+m^2$ and smooth test kernels. Define

$$
\widehat{\mathrm{Obs}}_{p,\mathrm{CF}}^{\,q}(U)_w
=
W_w(U)
=
\bigoplus_{\substack{r,k\ge0\\r+2k=w}}
\hbar^k\mathrm{Sym}^r_{\mathcal C_p}(E_p(U)).
\tag{CF7}
$$

The differential $D=d+\hbar\Delta_{\mathrm{BV}}$ **preserves the weight** $w=r+2k$; thus each component of (CF7) is a derived liquid cochain complex. The full formal observable has completed realization

$$
\prod_{w\ge0}W_w(U)
$$

and contains nonpolynomial infinite-weight series. Its quotient $Q_N$ is exactly the bounded-weight complex $T_N(U)$ from QW-001. This is a **real completion**: there is a compatible family of all truncations, and no requirement that an observable have only finitely many nonzero weights.

The disjoint-open external product from QFT-COND-003 adds weights, so the structure maps are morphisms in the symmetric monoidal category (CF1), using (CF4). Because mixed BV contractions between **disjoint supports** vanish, the full differential commutes with these maps. All associativity, symmetry, covariance under extension by zero and the unit are inherited strictly/coherently from the finite polynomial construction.

The unscaled odd BV bracket *alone* drops weight by two; the composite $\hbar\{-,-\}$ has the expected weight compatibility. We assert a coherent **completed free quantum factorization object**, not a full analytic BD equivalence with every renormalized construction.

## 3. Positive completed Weiss descent theorem

**Theorem CF-1 (completed quantum Weiss descent).** For every Weiss cover $\mathfrak U$ of a Euclidean open $U$ for which the predecessor's compact-support smooth-kernel construction applies, the **completed Čech comparison** is an equivalence in $\mathcal{CF}^{\mathrm{spl}}_p$:

$$
\boxed{
\mathrm{hocolim}_{\check C(\mathfrak U)}^{\mathcal{CF}}
\,\widehat{\mathrm{Obs}}_{p,\mathrm{CF}}^{\,q}
\;\xrightarrow{\;\sim\;}
\widehat{\mathrm{Obs}}_{p,\mathrm{CF}}^{\,q}(U).
}
\tag{CF8}
$$

Consequently this is a Weiss factorization algebra valued in the completed symmetric monoidal category (CF1).

**Proof.** Colimits in (CF1) are computed at each weight separately, hence applying the weight- $w$ evaluation to (CF8) gives

$$
\mathrm{hocolim}_{\check C(\mathfrak U)}
W_w(U_{i_0}\cap\cdots\cap U_{i_q})
\longrightarrow W_w(U).
$$

The finite-weight quantum theorem QW-001 proves this map is an equivalence: it filters $W_w$ by finitely many $\hbar$ powers, whose associated grades are the fixed-degree compact-support classical symmetric BV observables. Weiss covers of $U$ cover all finite configuration spaces $U^r$, and the smooth compact-support Čech contraction applies, after finite signed coinvariants. A finite extension argument proves descent with the full $d+\hbar\Delta$ differential.

In a functor category a map is an equivalence **if and only if** every component is an equivalence. Hence (CF8) holds. The previously constructed disjoint-open multiplication is defined by the completed Cauchy tensor (CF4), so the completed prefactorization structure and Weiss descent hold in the *same* target category. $\square$

**Computed realized Čech comparison.** Applying $\mathrm{Real}_{\Pi}$ *after forming the completed Čech colimit* yields

$$
\prod_{w\ge0}
\mathrm{hocolim}_{\check C(\mathfrak U)}W_w
\xrightarrow{\;\sim\;}
\prod_{w\ge0}W_w(U).
\tag{CF9}
$$

This is *not* the false map

$$
\mathrm{hocolim}_{\check C(\mathfrak U)}
\prod_{w\ge0}W_w
\longrightarrow
\prod_{w\ge0}W_w(U).
\tag{CF10}
$$

The earlier counterexamples tested (CF10) in ordinary derived liquid modules, and a different pro-valued Čech colimit. No contradiction arises: (CF8) is an equivalence under the completed coproduct rule, not a claim that an ordinary product preserves homotopy colimits.

## 4. The escaping-support example is repaired explicitly

Recall the genuine directed Weiss cover

$$
U=\coprod_{j\ge1}(3j,3j+1),\qquad
U_k=\coprod_{j\le k}(3j,3j+1).
$$

For the massive scalar, QW-001 constructed a quantum BV cohomology class $z_j\in W_j(U)^0$ supported in the $j$ th component, with a moment functional $\lambda_j(z_j)=1$ and $\lambda_j(Pg)=0$. The diagonal completed class

$$
z=(z_1,z_2,\ldots)
\in \prod_{w\ge0}W_w(U)
$$

cannot arise from any **single fixed** $U_k$ under the ordinary colimit of completed products. But under (CF6), its weight-quotient $Q_N(z)$ consists of only finitely many terms $z_1,\ldots,z_{N-1}$ and hence *does* come from the open $U_{N-1}$.

The stage $k(N)=N-1$ depends on $N$. The compatible family of these finite-stage representations defines a completed Čech class in

$$
\mathrm{holim}_N\mathrm{hocolim}_k T_N(U_k),
$$

which maps to $z$. **No uniform cover stage is required**, precisely because colimit is computed before the weight-limit. This removes the exact cohomological obstruction found in QW-001 and PRO-001. It does not make the forbidden ordinary/pro-valued comparison into an equivalence.

This is a concrete infinite-dimensional example where completed locality is restored by correctly specifying the target and its homotopy-colimit operation.

## 5. A mathematical comparison with Costello–Gwilliam

The match to published free-field quantum observables is **not merely terminological**. Costello–Gwilliam, *Factorization Algebras in Quantum Field Theory*, Volume 1, **§15.1.3, Proposition 15.1.3.1**, define the free quantum observable object as completed chains of a Heisenberg algebra, in differentiable pro-cochain complexes over $\mathbb R[[\hbar]]$. The displayed filtration in their text is

$$
F^N\mathrm{Obs}_{\mathrm{CG}}^q(U)
=
\prod_{k\ge0}
\hbar^k\mathrm{Sym}^{\ge N-2k}E_c^!(U).
\tag{CG1}
$$

Under the **common free smooth-kernel generator convention**, the quotient is the **finite** set of pairs $(r,k)$ obeying

$$
r+2k<N,
$$

so its graded and differential indexing is precisely

$$
\mathrm{Obs}_{\mathrm{CG}}^q(U)/F^N
\cong_{\text{formal finite-stage}}
\bigoplus_{r+2k<N}\hbar^k\mathrm{Sym}^r E_c^!(U).
\tag{CG2}
$$

Compare (CG2) with $Q_N\widehat{\mathrm{Obs}}_{p,\mathrm{CF}}^q(U)=T_N(U)$. The **quantum weight, cochain differential, finite cutoff, and completed-coproduct formula agree termwise**. This proves an exact **filtration-combinatorics/underlying algebraic smooth-kernel comparison**, and identifies the p-liquid coefficient replacement needed for a stronger analytic comparison.

Furthermore, Costello–Gwilliam's **Appendix B.5, Definitions B.5.0.3–B.5.0.6** specify completed coproducts and completed tensors by taking the inverse limit of finite-quotient ordinary coproducts/tensors. Their **Appendix B.6, Definition B.6.0.8** gives the corresponding completed coproduct of differentiable pro-cochain complexes. Our formulas (CF5)–(CF6) are precisely the **p-liquid, split-weight analogue** of those formulas. The published **Proposition 15.1.3.1** proves completed free quantum factorization in its differentiable pro-cochain setting. The present result uses a separately specified liquid category and the previously established nuclear flatness to reconstruct that free smooth-kernel substrate.

**Limits of comparison — not established:** A fully faithful, exact, symmetric monoidal analytic functor from **all** Costello–Gwilliam differentiable pro-cochain complexes into (CF1) has **not** been built. Its objects need not have canonical weight splittings, and smooth multilinear maps can be filtration-preserving without preserving weight. A natural equivalence of the two full completed quantum observable theories, including bornological smoothness, BD bracket, and all distributional observables, is **not** claimed. At each nuclear Fréchet compact-support stage, the known liquid tensor/projective tensor comparison is available; extending it to all topological and differentiable LF/pro limits remains a separate proof obligation.

**Sources for this exact comparison:**

- K. Costello and O. Gwilliam, *Factorization Algebras in Quantum Field Theory*, Vol. 1, §15.1.3, Proposition 15.1.3.1 (completed free quantum observables), and Appendix B.5 (complete filtered coproduct and tensor), B.6 (differentiable pro-cochain complexes): https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf.
- P. Scholze, *Lectures on Analytic Geometry*, Theorem 6.5 (derived p-liquid symmetric monoidal category): https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf.
- D. Clausen and P. Scholze, *Condensed Mathematics and Complex Geometry*, Theorem 4.11 and Remark 4.12 (nuclear Fréchet liquid flatness/tensor): https://people.mpim-bonn.mpg.de/scholze/Complex.pdf.
- O. Gwilliam and K. Rejzner, *Relating Nets and Factorization Algebras of Observables: Free Field Theories*: https://link.springer.com/article/10.1007/s00220-019-03652-9.

## 6. Exact computational acceptance and limitations

**Fixture:** \`python3 research/condensed-qft/fixtures/completed_filtered_weiss.py\`. The tests are exact integer/rational calculations of:

1. The quotient identity $F^N=\prod_k\hbar^k\mathrm{Sym}^{\ge N-2k}$ with $r+2k<N$.
2. Preservation of quantum weight by both pieces of the free differential and consistency of finite truncation projections.
3. The finite Cauchy-product formula and its compatibility with truncations.
4. The escaping-support diagonal has a **different cover stage for each cutoff**; completed colimit accepts it and any fixed-stage ordinary colimit of completed products rejects it.
5. The proper degreewise completed coproduct and the incorrect ordinary coproduct differ already in an adversarial finite model.

These checks validate exact combinatorics, not the infinite derived liquid tensor, pro-homotopy colimits, nor published source theorems.

**Claim taxonomy:**

| Claim | Status |
| --- | --- |
| Complete separated split-weight analytic liquid category, completed Cauchy tensor | Defined and proved by direct category theory |
| CF-1 Weiss descent, coherent factorization | Proven **for the bounded-smooth free scalar model**, assuming previous QFT-COND-003 finite-degree tensor/Weiss theorem |
| Explicit repair of the escaping-support class using cutoff-dependent supports | Proven from the completed-coproduct formula |
| Exact match of quantum-weight indices, finite truncations, differential, and completed coproduct to CG | Source-backed formal/combinatorial comparison |
| Full smooth/differentiable/bornological equivalence with CG | **OPEN** |
| Coherent filtered BD bracket, renormalized local products, interactions, gauge theory | **NOT CLAIMED** |
| Genuinely new theorem in QFT or independent mathematical priority | **NOT ESTABLISHED** |

**Research decision:** The completion/locality problem has a **positive restricted answer** once one specifies the correct split complete filtered target. The prior three no-go results remain valid as negative controls for *wrong colimit categories*. The remaining mathematical novelty gate is a nontrivial analytic **comparison functor** with full differentiable pro-cochains (or a demonstrably stronger completion/descent criterion), not yet another weightwise Čech proof.
