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

## 3. LFO3 on actual compact-support stages

For Euclidean opens $U_i,V$, choose nested compact exhaustions and write $E_{i,a}=\mathcal D_{K_{i,a}}(U_i)$, $G_b=\mathcal D_{L_b}(V)$, and $H_{\mathbf a}=\widehat\otimes_{\pi,i}E_{i,a_i}$.

The open comparison is

$$
\Phi_{\mathbf a}:\varinjlim_b\operatorname{Hom}_{\mathcal A}(\underline{H_{\mathbf a}},\underline{G_b})
\longrightarrow
\operatorname{Hom}_{\mathcal A}(\underline{H_{\mathbf a}},\varinjlim_b\underline{G_b}).
\tag{LFO3}
$$

**Proposition LPR-2 (injectivity conditional on monomorphism preservation).** If $\underline{G_b}\to\underline{G_{b'}}$ are monomorphisms and their filtered colimit maps $\underline{G_b}\to\varinjlim_b\underline{G_b}$ remain monomorphisms, then $\Phi_{\mathbf a}$ is injective.

**Proof.** If two stagewise maps yield the same morphism into the colimit, move both to a common larger stage $G_c$. The difference $\underline H\to\underline{G_c}$ vanishes after composition with the monomorphism $\underline{G_c}\to\varinjlim_b\underline{G_b}$, hence already vanishes at stage $c$. $\square$

**Remaining surjectivity question:** Does every *liquid* morphism from each fixed nuclear Fréchet input stage into $A_p(V)=\varinjlim_b\underline{G_b}$ factor through a single output support stage? Grothendieck's classical Fréchet-to-strict-LF factorization theorem answers this for **continuous linear maps into the classical LF topology**, but it cannot be silently applied to a morphism into a colimit taken in $\mathcal A$. The missing bridge is an identification of $A_p(V)$ with the classical condensed/liquid realization of $\mathcal D(V)$ that reflects the relevant linear maps, or a direct liquid relative-stage factorization theorem.

This is a *relative compactness* question for the particular support diagram, not a claim that $\underline H$ is compact with respect to every filtered colimit.

## 4. Concrete tests for a final LFO3 adjudication

1. Compare $\varinjlim_b\underline{\mathcal D_{L_b}(V)}$ with $\underline{\mathcal D(V)}$ formed from the locally convex LF space, including maps from profinite test spaces.
2. Check whether the candidate comparison preserves global points, plots and bounded input sets. Underlying-point equality alone is insufficient for Hom comparison.
3. Attempt to construct a liquid morphism $\underline H\to A_p(V)$ whose support is not uniformly bounded on $H$, or establish a theorem forcing factorization through some $G_b$.
4. Test the same bridge for higher derived Hom and finite tensor products, separately from the underived case.

**Disposition:** LPR-1 is proved from explicit standard-category axioms; LPR-2 gives injectivity under verified stage monomorphisms. **LFO3 surjectivity remains open.** Neither result proves enriched B.6 equivalence, Weiss descent, or renormalized BV operations.

## References

- Peter Scholze, [Lectures on Analytic Geometry](https://arxiv.org/abs/2605.03655), liquid vector spaces and derived inverse limits.
- Clausen–Scholze, [Condensed Mathematics and Complex Geometry](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), Fréchet realization and liquid category.
- A. G. Smirnov, [On kernel theorems for (LF)-spaces](https://arxiv.org/abs/math/0612756), Grothendieck Fréchet-to-LF factorization.
