# QFT-COND-005 / LFO-010: Strict LF outputs and the infinite-jet obstruction

**Disposition:** A positive, underived description of smooth multilinear maps with *strict LF targets*, together with an exact non-splitting theorem for infinite jets. The results constrain but do **not** establish a full derived/smooth pro-cochain equivalence. Both rely on classical mathematics and carry no originality claim. [QFT-COND-004 tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2603).

## 1. Strict LF target comparison: source-dependent output support

Let $U_1,\ldots,U_n,V$ be Euclidean opens, $n\ge1$ finite. Fix cofinal compact exhaustions $K_{i,a}\Subset U_i$ and $L_b\Subset V$. Write $E_{i,a}=\mathcal D_{K_{i,a}}(U_i)$ and $G_b=\mathcal D_{L_b}(V)$, nuclear Fréchet spaces. Their strict LF limits are $\mathcal D(U_i)$ and $\mathcal D(V)$. Let $\mathrm{Mult}_b$ mean bornologically bounded multilinear operations, which Costello–Gwilliam Appendix C.1 identifies with smooth multilinear operations on complete bornological spaces.

**Theorem LFO-1 (strict LF-output formula).** There is a natural bijection

$$
\mathrm{Mult}_b(\mathcal D(U_1),\ldots,\mathcal D(U_n);\mathcal D(V))
\cong
\varprojlim_{\mathbf a}\varinjlim_b
\mathrm{Mult}_{\mathrm{cont}}(E_{1,a_1},\ldots,E_{n,a_n};G_b).
\tag{LFO1}
$$

**Proof.** A bounded multilinear operation restricts to a bounded and jointly continuous operation on each tuple of Fréchet support stages. Via the completed projective tensor universal property, it linearizes to a continuous linear map from the nuclear Fréchet space $H_{\mathbf a}=\widehat\bigotimes_{\pi,i}E_{i,a_i}$ to the complete strict LF space $\mathcal D(V)$. Grothendieck's Fréchet-to-LF factorization theorem, reproduced as Lemma 1 of Smirnov's *On kernel theorems for (LF)-spaces*, ensures that this map factors **continuously** through some Fréchet target stage $G_{b(\mathbf a)}$. Restrictions on overlapping source stages are compatible, establishing the forward map.

Conversely, compatible stagewise continuous multilinear maps assemble uniquely into an algebraic multilinear map on the unions. Any bounded subset of a strict LF test-function space lies and is bounded in one Fréchet support stage. Hence the image of any product of bounded input sets is bounded in a target support stage, showing that the map is bornologically bounded. Injectivity of the target stage embeddings guarantees uniqueness. By Costello–Gwilliam's bornological multicategory theorem, these are exactly the relevant smooth multilinear maps. $\square$

**Quantifier discipline:** the output stage $b(\mathbf a)$ may depend on the input stages. One cannot replace $\varprojlim_{\mathbf a}\varinjlim_b$ by $\varinjlim_b\varprojlim_{\mathbf a}$.

**Exact counterexample.** The identity operator $T=\mathrm{id}:\mathcal D(\mathbb R)\to\mathcal D(\mathbb R)$ is smooth, bounded and continuous. It maps every fixed input support stage into that same output stage, but cannot have its **entire** image inside any fixed compact support. Therefore the reversed-order limit-colimit expression misses $T$.

## 2. Precisely what transfers to p-liquid maps

With $A_p(U)=\varinjlim_K\underline{\mathcal D_K(U)}$ in real liquid modules with parameter $p$, the nuclear Fréchet tensor theorem and full faithfulness of the Fréchet realization identify each stagewise Hom term in (LFO1) with

$$
\mathrm{Hom}_{\mathrm{Liq}_p}
\left(\bigotimes_{i=1}^n\underline{E_{i,a_i}},\underline{G_b}\right).
\tag{LFO2}
$$

Thus **degree-zero smooth LF-output operations** are represented by the explicit mixed stagewise limit-colimit of liquid Hom sets in (LFO2). This is a positive analytic comparison of the actual stagewise operations.

**Not established:** an isomorphism from this mixed stagewise Hom set onto the unrestricted liquid Hom set $\mathrm{Hom}_{\mathrm{Liq}_p}(\bigotimes_i A_p(U_i),A_p(V))$. That stronger statement needs the relative target-stage compactness/factorization property

$$
\mathrm{Hom}_{\mathrm{Liq}_p}\left(\bigotimes_i\underline{E_{i,a_i}},\varinjlim_b\underline{G_b}\right)
\stackrel{?}{\cong}
\varinjlim_b\mathrm{Hom}_{\mathrm{Liq}_p}\left(\bigotimes_i\underline{E_{i,a_i}},\underline{G_b}\right).
\tag{LFO3}
$$

Nuclearity and tensor flatness do **not by themselves** prove (LFO3). The further comparison of higher derived Hom objects and differentiable pro-cochain mapping complexes therefore remains open.

## 3. A strict nuclear Fréchet extension that never splits linearly

Fix $K=[-1,1]$ and $E=\mathcal D_K(\mathbb R)$, nuclear Fréchet. The **Borel jet map**

$$
J:E\longrightarrow\mathbb R^{\mathbb N_0},\qquad
J(f)=(f(0),f'(0),f''(0),\ldots)
\tag{JET1}
$$

is continuous and surjective, by Borel's theorem followed by multiplication with a fixed bump equal to one near $0$. The target has its Fréchet **product** topology. The kernel is closed, the map is open by the Fréchet open mapping theorem, and the sequence

$$
0\longrightarrow\ker J\longrightarrow E\xrightarrow{J}\mathbb R^{\mathbb N_0}\longrightarrow0
\tag{JET2}
$$

is a **strict short exact sequence of nuclear Fréchet spaces**.

Every finite jet map $J_N:E\to\mathbb R^N$ has a continuous linear section:

$$
s_N(a_0,\ldots,a_{N-1})(x)
=\chi(x)\sum_{j=0}^{N-1}\frac{a_jx^j}{j!},
\qquad J_Ns_N=\mathrm{id},
\tag{JET3}
$$

where $\chi$ is smooth, compactly supported in $(-1,1)$ and equals one near zero.

**Theorem LFO-2 (infinite-jet nonsplitting).** The full map $J$ has **no continuous linear right inverse**, despite all the finite sections (JET3).

**Proof.** Suppose $s:\mathbb R^{\mathbb N_0}\to E$ were a continuous linear section. The seminorm $q(f)=\sup_{|x|\le 1/2}|f(x)|$ is continuous on $E$. Because the source carries the **product topology**, continuity of the seminorm $q\circ s$ forces a bound $q(s(a))\le C\max_{0\le i<M}|a_i|$ for some finite $M$ and $C$. For each basis vector $e_j$ with $j\ge M$, $q(s(e_j))=0$. Thus $s(e_j)$ vanishes near zero and has zero infinite jet, contradicting $Js(e_j)=e_j$. $\square$

**Strict derived consequence.** The nonsplit strict exact sequence (JET2) defines a nonzero Yoneda extension

$$
[\epsilon_J]\ne0\quad\text{in}\quad
\mathrm{Ext}^1_{\mathrm{strNF}}(\mathbb R^{\mathbb N_0},\ker J).
\tag{JET4}
$$

This is an obstruction **in the exact category of nuclear Fréchet spaces**. Full faithfulness of the Fréchet-to-liquid realization also implies there is no degree-zero liquid linear section of $\underline J$. However, **a nonzero Ext class in derived liquid modules is not claimed** without separately checking the exactness and Ext behavior of that realization. The theorem says nothing negative about possibly existing **nonlinear** smooth or plotwise lifting maps.

**Why this matters for completion:** finite quotient splittings cannot automatically be assembled into a continuous linear section of an infinite completed pro-object. It is a concrete failure mode even among nuclear Fréchet spaces; invoking a flat nuclear tensor comparison alone does not address it.

## 4. The remaining derived/enriched proof obligations

A claimed smooth-enriched comparison with the Costello–Gwilliam B.6 differentiable pro-cochain category must establish (1) the relative liquid target-stage property (LFO3) or characterize its failure; (2) preservation and reflection of declared **strict** exact sequences and derived extension classes, including (JET2); (3) the correct mixed support-stage and quantum-weight completion order; and (4) compatible differentiable cofibrations and smooth multilinear mapping objects. Finite-stage Hom comparisons alone resolve none of these four automatically.

**Scope:** LFO-1 is an underived LF-output multilinear theorem. LFO-2 is a classical nonsplitting theorem furnishing a strict exact-category obstruction. Neither constructs a renormalized BV theory, proves an equivalence of complete smooth pro-cochains, or claims independent mathematical priority.

## 5. Sources and verification

- [A. G. Smirnov, *On kernel theorems for (LF)-spaces*](https://arxiv.org/abs/math/0612756), Lemma 1 and its attribution to Grothendieck's Théorème A.
- [Costello–Gwilliam, *Factorization Algebras in Quantum Field Theory*, Volume 1](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), Appendix B.6.0.7–B.6.1.1 and C.1.0.5–C.1.0.7.
- [Ralf Meyer, *Bornological versus topological analysis in metrizable spaces*](https://arxiv.org/abs/math/0310225) and [*Analytic cyclic cohomology*](https://arxiv.org/abs/math/9906205), bornological/Fréchet multilinear facts.
- [Borel map and nonsplitting](https://mathoverflow.net/questions/431793/is-the-borel-lemma-projection-a-smooth-principal-bundle), classical infinite-jet example.
- [Clausen–Scholze, *Condensed Mathematics and Complex Geometry*](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), nuclear Fréchet/liquid tensor and metrizable full faithfulness.

**Fixture:** `python3 qft_cond_004/strict_lf_output_derived_boundary.py`. It uses exact rational finite-jet matrices, a finite support-stage identity adversary and multilinear moment calculations. It cannot certify the infinite Grothendieck or Borel theorems; those are proved or sourced above.

**Governance:** FIL-008 and ENR-009 remain documented as local/unadmitted in the prior transaction. This LFO-010 file should not be represented as protected-merged until the repository's exact merged head verifies its presence.