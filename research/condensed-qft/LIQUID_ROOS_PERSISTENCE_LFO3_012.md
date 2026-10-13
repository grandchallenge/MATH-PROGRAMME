# QFT-COND-005 / LPR-012 — Persistence of the Roos obstruction in real p-liquid modules and LFO3 reduction

**Status:** conditional-on-standard-category-axioms categorical proof with explicit axioms; no claim of a full Costello–Gwilliam B.6 equivalence. Related: [DLI-011](DERIVED_LIMIT_OBSTRUCTION_011.md), [LFO-010](STRICT_LF_OUTPUT_DERIVED_BOUNDARY_010.md).

## 1. Ambient category and exactness gate

Fix $0<p\le1$ and let $\mathcal A=\mathrm{Liq}_p(\mathbb R)$, with $D(\mathcal A)$ its unbounded derived category. Use the standard fully faithful realization $E\mapsto\underline E$ of nuclear Fréchet spaces.

The precise structural inputs used below are:

- **P1** $\mathcal A$ is an abelian category with exact products (AB4*), so countable inverse towers have their derived limit modeled by the two-term Roos complex.
- **P2** The free liquid module on the one-point profinite set is a projective object $P_*$, and $\operatorname{Hom}_{\mathcal A}(P_*,-)$ is ordinary evaluation at a point and preserves countable products.
- **P3** $\operatorname{Hom}_{\mathcal A}(P_*,\underline E)=E$ as an underlying real vector space, naturally in continuous linear maps.

In a category with enough compact projective generators, P1 follows from the exactness of products and P2 is the special generator of a singleton; these statements must be understood for the **chosen liquid category**, not imported from condensed abelian groups without verification.

## 2. Theorem LPR-1 (nonzero derived liquid limit)

Let $s$ be rapidly decreasing real sequences with its standard nuclear Fréchet topology and $S:s\to s$ the right shift. Regard each $s$ as $\underline s\in\mathcal A$ and form the inverse tower $\cdots\to\underline s\xrightarrow{S}\underline s$. Under P1–P3,

$$
H^1\left(R\varprojlim_n\underline s\right)\neq0.
$$

**Proof.** The Roos differential $\Delta:\prod_n\underline s\to\prod_n\underline s$ is the morphism $\Delta((y_n))=(y_n-Sy_{n+1})$. Consider $x=(e_0)_n$ as a global element of the target product, or equivalently a map $P_*\to\prod_n\underline s$. If $\Delta$ were epimorphic, projectivity of $P_*$ would lift $x$ to a global element of the source product. By P2–P3 this would provide a tuple $(y_n)\in\prod_n s$ satisfying $y_n=e_0+Sy_{n+1}$. The first coordinate of each $y_n$ is one, and induction makes every coordinate of $y_0$ equal to one. This contradicts $y_0\in s$. Hence $\Delta$ is not epic. By P1, its cokernel is exactly $H^1(R\varprojlim\underline s)$, which is nonzero. $\square$

**Boundary:** The argument proves nonzero higher derived inverse-limit cohomology in $D(\mathrm{Liq}_p(\mathbb R))$ under P1–P3. It does not assert that its underlying-point evaluation fully characterizes the cohomology object, nor that a BV quantum-weight tower contains this particular shift subsystem. It requires no comparison of Fréchet $\operatorname{Ext}^1$ with liquid $\operatorname{Ext}^1$.

## 3. LFO3 on actual compact-support stages — CLOSED BY LFO-013

The earlier open surjectivity question has now been resolved **for the specified compact-support test-function targets**. See [LFO3-S theorem and full proof](LFO3_SURJECTIVITY_THEOREM_013.md).

For fixed nuclear Fréchet $H_{\mathbf a}$, the comparison

$$
\varinjlim_b\operatorname{Hom}_{\mathcal A}(\underline{H_{\mathbf a}},\underline{G_b})
\xrightarrow{\sim}
\operatorname{Hom}_{\mathcal A}(\underline{H_{\mathbf a}},A_p(V))
$$

is a bijection. The proof uses point evaluations $A_p(V)\to\mathbb R$ to produce continuous scalar functionals on $H_{\mathbf a}$; Baire's theorem forces a common compact target support; filtered colimits computed on profinite plots and closed embeddings $G_b\hookrightarrow G_c$ then upgrade pointwise support control to an actual liquid factorization. Injectivity uses monomorphisms of support stages.

Moreover, strict LF bounded-set regularity gives a natural identification

$$
A_p(V)=\varinjlim_b\underline{\mathcal D_{L_b}(V)}
\cong\underline{\mathcal D(V)}
$$

as liquid modules, by checking maps from arbitrary profinite sets. This identification is specific to the regular strict LF test-function system.

**Non-consequence:** the output support stage still depends on the source support stage. The global interchange $\varprojlim_{\mathbf a}\varinjlim_b\not\cong\varinjlim_b\varprojlim_{\mathbf a}$ remains false in general; the identity on $\mathcal D(\mathbb R)$ supplies the counterexample.

## 4. Remaining derived and enriched tests

1. Establish higher derived $\operatorname{RHom}$ mapping-object behavior for the same fixed compact-support stages, with exactness hypotheses recorded.
2. Compare countable source-stage inverse limits and quantum-weight pro-completions in the specified stable category; DLI-011 remains a nontrivial warning.
3. Define the differentiable pro-cochain enrichment of Costello–Gwilliam Appendix B.6 and test multiplicative/cofibration compatibility.
4. Verify Weiss descent and the completion order for the actual free BV observables.

**Disposition:** LPR-1 persists under standard liquid-category axioms; **underived LFO3 is proved**, not merely injective. This does not prove enriched B.6 equivalence, Weiss descent, or interacting BV operations.

## References

- Peter Scholze, [Lectures on Analytic Geometry](https://arxiv.org/abs/2605.03655), liquid vector spaces and derived inverse limits.
- Clausen–Scholze, [Condensed Mathematics and Complex Geometry](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), Fréchet realization and liquid category.
- A. G. Smirnov, [On kernel theorems for (LF)-spaces](https://arxiv.org/abs/math/0612756), Grothendieck Fréchet-to-LF factorization.
