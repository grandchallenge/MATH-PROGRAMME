# QFT-COND-005 / LFO-013 — Strict LF liquid realization and the LFO3 theorem

**Mathematical disposition:** LFO3 is **proved** for the ordinary compact-support smooth test-function filtration. The proof is underived. No equivalence of derived mapping complexes or differentiable pro-cochains is claimed. This supersedes the open-surjectivity language in [LPR-012](LIQUID_ROOS_PERSISTENCE_LFO3_012.md) and [LFO-010](STRICT_LF_OUTPUT_DERIVED_BOUNDARY_010.md); see the [verification matrix](RUN_MATRIX_013.md).

## 1. Precise setting

Fix $0<p\leq1$, and take the standard full abelian category $\mathcal A=\mathrm{Liq}_p(\mathbb R)\subset\mathrm{Cond}(\mathbb R)$. The inclusion preserves all colimits [Clausen–Scholze, Theorem 3.11]. A complete locally convex real vector space defines a liquid at parameter $p$ object; for metrizable complete locally convex spaces this is the ordinary condensed realization $E\mapsto\underline E$.

Let $V\subseteq\mathbb R^d$ be open and $L_1\subseteq L_2\subseteq\cdots\Subset V$ an exhaustion by compact sets such that each compact subset of $V$ is contained in some $L_b$. Put

$$
G_b=\mathcal D_{L_b}(V)=\{f\in C^\infty(V):\mathrm{supp}(f)\subseteq L_b\},\qquad
A_p(V)=\varinjlim_b\underline{G_b}.
\tag{13.1}
$$

Every $G_b$ is a nuclear Fréchet space. For $b\le c$, the inclusion $G_b\to G_c$ is a closed topological embedding: the support condition is the intersection of kernels of continuous point evaluations outside $L_b$.

**Categorical input C1 (sectionwise colimit).** Filtered colimits in $\mathrm{Cond}(\mathbb R)$ are evaluated sectionwise on the profinite test site: filtered colimits of abelian-group-valued sheaves on this finite-cover site remain sheaves, because filtered colimits commute with finite limits in abelian groups. Theorem 3.11 ensures that the colimit in $\mathcal A$ is the same one. Thus, for every profinite $S$,

$$
A_p(V)(S)=\varinjlim_b\mathrm{Cont}(S,G_b).
\tag{13.2}
$$

In particular $A_p(V)(*)=\bigcup_bG_b$ as an algebraic vector space. The structural maps $\underline{G_b}\to A_p(V)$ are monomorphisms, because the stagewise maps are injective and the filtered colimit is exact.

**Categorical input C2 (Fréchet full faithfulness).** If $H$ is Fréchet, a liquid map $\underline H\to\underline{\mathbb R}$ is a continuous linear functional on $H$. The underlying condensed functor is fully faithful on compactly generated spaces (Fréchet spaces are metrizable, hence compactly generated); the liquid subcategory is full.

## 2. Theorem LFO3-S (source-stage uniform target support)

Let $H$ be a nuclear Fréchet space, in particular any finite completed projective tensor product of fixed compact-support stages

$$
H_{\mathbf a}=
\widehat{\bigotimes}_{\pi,i=1}^{n}\mathcal D_{K_{i,a_i}}(U_i).
$$

Then the canonical map

$$
\Phi_H:
\varinjlim_b\mathrm{Hom}_{\mathcal A}(\underline H,\underline{G_b})
\xrightarrow{\ \sim\ }
\mathrm{Hom}_{\mathcal A}(\underline H,A_p(V))
\tag{13.3}
$$

is a bijection. In fact the proof applies to any Fréchet $H$ whose condensed realization is liquid at parameter $p$.

**Proof: surjectivity, step 1 (continuous point probes).** Let $F:\underline H\to A_p(V)$ be liquid-linear. For any $x\in V$, the maps $G_b\to\mathbb R$, $g\mapsto g(x)$, are compatible continuous linear maps, hence induce a liquid-linear evaluation $\mathrm{ev}_x:A_p(V)\to\underline{\mathbb R}$. The composition

$$
\lambda_x=\mathrm{ev}_x\circ F:H\to\mathbb R
$$

is continuous and linear by C2.

**Step 2 (Baire uniformization).** Define

$$
H_b=\bigcap_{x\in V\setminus L_b}\ker\lambda_x.
\tag{13.4}
$$

Each $H_b$ is a closed vector subspace of $H$. By (13.2), for every $h\in H$ the global point $F(h)\in A_p(V)(*)$ is a compactly supported smooth function, and therefore $h\in H_b$ for some $b$. Consequently

$$
H=\bigcup_b H_b.
$$

Because $H$ is Fréchet, it is a Baire space. At least one $H_{b_0}$ has nonempty interior; any linear subspace with nonempty interior equals $H$. Hence $H_{b_0}=H$: **one target support $L_{b_0}$ contains $F(h)$ for all $h\in H$.**

**Step 3 (upgrade global points to a liquid morphism).** Fix an arbitrary profinite test space $S$ and plot $u:S\to\underline H$. By (13.2), the composite $F\circ u:S\to A_p(V)$ has a representative $v:S\to G_c$ continuous for some $c$. Move to $G_d$ for $d=\max(b_0,c)$. Every ordinary point $s\in S$ maps to a function supported inside $L_{b_0}$. Since $G_{b_0}$ is a **closed topological subspace** of $G_d$, the representative $v:S\to G_d$ factors continuously through $G_{b_0}$. These factorizations are unique (stage inclusions are monomorphisms) and compatible with pullback in $S$. They therefore assemble into a morphism of condensed real vector spaces $F_{b_0}:\underline H\to\underline{G_{b_0}}$. As $\mathcal A$ is a full subcategory of $\mathrm{Cond}(\mathbb R)$, this is a liquid morphism and $F=\iota_{b_0}F_{b_0}$. Surjectivity follows.

**Proof: injectivity.** If two stage maps become equal in $A_p(V)$, choose one common stage $G_c$ containing both targets. Their difference $H\to G_c$ becomes zero after composing with the monomorphism $\underline{G_c}\to A_p(V)$, hence already vanishes at stage $c$. The classes in the filtered colimit of Hom sets agree. $\square$

### Nonuniformity across *different* source stages

The theorem does **not** exchange the outer inverse limit over source support with the target filtered colimit:

$$
\varprojlim_{\mathbf a}\varinjlim_b\mathrm{Hom}(\underline{H_{\mathbf a}},\underline{G_b})
\not\cong_{\rm general}
\varinjlim_b\varprojlim_{\mathbf a}\mathrm{Hom}(\underline{H_{\mathbf a}},\underline{G_b}).
$$

The identity $\mathcal D(\mathbb R)\to\mathcal D(\mathbb R)$ remains the direct counterexample to a uniform compact output support for *all* source stages. LFO3-S supplies precisely one output support stage **for each fixed** $\mathbf a$.

## 3. Bridge to the classical strict LF realization

Let $\mathcal D(V)=\varinjlim_b^{\mathrm{strict\ LF}}G_b$ with its usual locally convex LF topology. The classical Dieudonné–Schwartz bounded-set theorem for strict LF spaces says that any bounded set in $\mathcal D(V)$ is contained and bounded in one step. In particular any compact set is contained in one $G_b$, and strictness identifies the topology on $G_b$ with the subspace topology from $\mathcal D(V)$.

For every profinite $S$, a continuous map $S\to\mathcal D(V)$ has compact image and hence lands in some $G_b$. It is continuous as a map $S\to G_b$. Conversely each such stage map is continuous into the LF space. Therefore

$$
\varinjlim_b\mathrm{Cont}(S,G_b)
\cong
\mathrm{Cont}(S,\mathcal D(V))
\tag{13.5}
$$

naturally in $S$, and thus

$$
A_p(V)\cong\underline{\mathcal D(V)}
\quad\text{as condensed, hence liquid, real vector spaces.}
\tag{13.6}
$$

This comparison **does** hold for this regular strict LF test-function filtration; it is not a general theorem about arbitrary locally convex inductive limits.

As an independent proof route, any liquid-linear $F:\underline H\to\underline{\mathcal D(V)}$ preserves convergent sequences of $H$ (the convergent-sequence compactum is profinite). Because $H$ is metrizable, the induced linear map $H\to\mathcal D(V)$ is continuous. Grothendieck's Fréchet-to-(LF) factorization theorem then yields some $G_b$ as its target. C1 and closed stage embeddings lift the factorization to liquid morphisms as in Step 3. The direct Baire proof in Section 2 avoids invoking this stronger classical factorization theorem.

## 4. Limits of the result

The theorem is entirely **underived**: it compares $\mathrm{Hom}$ sets for degree-zero nuclear Fréchet source stages. It says **nothing** about comparison maps for $\mathrm{Ext}^i$, derived internal Hom, infinite inverse towers, or differentiable pro-cochain enrichments. The DLI-011/LPR-012 nonzero Roos $\varprojlim^1$ obstruction remains independent.

It does **not** establish compactness of $\underline H$ relative to arbitrary filtered diagrams, nor does it license interchanging the source-stage inverse limit with the target-stage filtered colimit or quantum-weight completion.

## 5. Verification and provenance

- **Primary liquid-category source:** Dustin Clausen and Peter Scholze, [Condensed Mathematics and Complex Geometry](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), Lecture II on complete locally convex spaces (page 19); Lecture III, Theorem 3.11 (pages 28–29), on the fully faithful inclusion, all colimits, and the liquid category.
- **Strict LF regularity:** Dieudonné–Schwartz, *La dualité dans les espaces (F) et (LF)*, Annales de l'Institut Fourier **1** (1949), Props. 2 and 4 (inherited stage topology and bounded-set regularity). See also [strict inductive limit notes](https://www.mat.univie.ac.at/~kriegl/Skripten/2019SSe.pdf).
- **Alternative factorization:** A. G. Smirnov, [On kernel theorems for (LF)-spaces](https://arxiv.org/abs/math/0612756), Lemma 1 attributing Fréchet-to-LF factorization to Grothendieck.
- **Novelty:** no mathematical priority asserted. This is an explicit source-grounded resolution of the *programme's LFO3 obligation*. It must not be described as a novel theorem in condensed analysis.

**Next boundary:** verify higher derived $\mathrm{RHom}$ comparison for these stages and the correct smooth pro-cochain enrichment, with degree shifts, quantum-weight tower limits and Weiss descent treated separately.
