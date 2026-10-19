# EXT-015C / 019 — positive degree-one comparison for fixed test-function source

**Mathematical disposition:** A complete *candidate proof*, subject to the explicitly identified source-presentation and strict-LF realization hypotheses. The proof addresses the original \(\mathrm{Ext}^1\) target-stage comparison, not merely its phantom subgroup. The protected verification matrix must not mark it as admitted until its categorical relations argument and change-of-filtration steps have passed critical review.

**Question:** Can an extension carry genuinely global analytic information that no compact-support stage can capture?

## 1. Main statement

Fix $0<p\le1$ and work in the abelian category $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$. Take $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$ and $G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)}$, with $G=\varinjlim_b G_b$.

**Theorem 19.1 (positive EXT-015C).** The natural map

$$
\theta^1:\varinjlim_b
\mathrm{Ext}^1_{\mathcal A_p}(H,G_b)
\longrightarrow
\mathrm{Ext}^1_{\mathcal A_p}(H,G)
\tag{19.1}
$$

is an isomorphism, provided the established source-stage presentation and the two Valdivia–Vogt identifications cited below are interpreted as isomorphisms in the stated liquid category. The injection is the independently reviewed Theorem A-16.2. The new obligation is surjection, proved below.

This theorem does **not** assert degree-two derived comparison, a varying compact-support source, or the Costello–Gwilliam smooth-cochain comparison.

## 2. General relative Ext-continuity lemma from profinite relations

**Lemma 19.2.** Let $S$ be any profinite set, $\mathcal M(S)=\mathcal M_{<p}(S)$ its free real liquid module, and let

$$
E_1\hookrightarrow E_2\hookrightarrow\cdots,\qquad
E=\varinjlim_m E_m
$$

be liquid monomorphisms. Suppose that **for every profinite $K$** and every morphism $\mathcal M(K)\to E$, there exists $m$ through which it factors. Then

$$
\varinjlim_m\mathrm{Ext}^1(\mathcal M(S),E_m)
\xrightarrow{\sim}
\mathrm{Ext}^1(\mathcal M(S),E).
\tag{19.2}
$$

**Proof.** Choose a surjection of profinite sets $\pi:T\twoheadrightarrow S$ with $T$ extremally disconnected. Write $R=T\times_ST$, itself profinite, and $d=\mathcal M(p_1)-\mathcal M(p_2)$.

A surjection $T\to S$ is an effective epimorphism of condensed sets. The liquid free-module functor on condensed sets, being a left adjoint, preserves its coequalizer. Therefore the following is right exact in $\mathcal A_p$:

$$
\mathcal M(R)\xrightarrow{d}\mathcal M(T)
\xrightarrow{\varepsilon}\mathcal M(S)\longrightarrow0.
\tag{19.3}
$$

Set $L=\operatorname{im}(d)=\ker\varepsilon$. The source $\mathcal M(T)$ is projective by Scholze, *Lectures on Analytic Geometry*, Theorem 6.5, because $T$ is extremally disconnected. The image presentation gives an epimorphism $\mathcal M(R)\twoheadrightarrow L$. Hence the exact projective presentation

$$
0\longrightarrow L\longrightarrow\mathcal M(T)
\longrightarrow\mathcal M(S)\longrightarrow0
\tag{19.4}
$$

computes first Ext as the cokernel of

$$
\mathrm{Hom}(\mathcal M(T),E)\longrightarrow\mathrm{Hom}(L,E).
\tag{19.5}
$$

By hypothesis, **every** map $L\to E$ has finite output stage: precompose it with the epimorphism $\mathcal M(R)\twoheadrightarrow L$. The composite factors through some $E_m$, since $R$ is profinite. The equality of its image with the image of $L\to E$, together with the monomorphism $E_m\hookrightarrow E$, induces a unique factorization $L\to E_m$ in the abelian category. The same hypothesis applied to $T$ makes all maps $\mathcal M(T)\to E$ stage-bounded.

For **surjectivity** of (19.2), represent an arbitrary first-Ext class by a map $L\to E$ in (19.5), and choose its finite stage. For **injectivity**, suppose a finite-stage class becomes zero in $\mathrm{Ext}^1(\mathcal M(S),E)$. In (19.5) it is a boundary from a map $\mathcal M(T)\to E$, which factors at a finite stage; enlarge that stage to contain the original class. The class already vanishes there. This proves (19.2). $\square$

**Crucial technical point:** No claim that $\mathcal M(S)$ is projective for *arbitrary* profinite $S$ was used. Only the chosen extremally disconnected cover $T$ is projective. The relation module $L$ need not itself be projective, compact or Fréchet: it is the **epimorphic image of the free measure module on the profinite kernel pair $R$**, which is enough to control maps out of $L$.

### Concrete strict-LF target

Suppose each $E_m$ is a closed Fréchet output stage and $E$ is the liquid realization of their regular strict LF union. Every plot from a profinite compact $K$ into that LF space has compact, hence bounded, image, and therefore lands continuously in one closed Fréchet stage. The free-liquid universal property then verifies the hypothesis of Lemma 19.2 for *every* profinite $K$.

In particular, take $B_n=\underline s$ and

$$
E=\bigoplus_{n\ge1}B_n,\qquad
E_m=\bigoplus_{n\le m}B_n.
\tag{19.6}
$$

The usual locally convex direct sum of Fréchet spaces is a regular strict LF space with these closed stages; its liquid realization agrees with (19.6). Thus Lemma 19.2 applies.

## 3. Weight stages have finite-coordinate first Ext

Write $S_\infty=\mathbb N\cup\{\infty\}$, a profinite convergent sequence. The defining map

$$
\mathcal M(S_\infty)\longrightarrow\mathcal M(*)
\tag{19.7}
$$

induced by the collapse $S_\infty\to*$ has a section induced by the distinguished point $\infty$. Its kernel $\mathcal M(\mathbb N)$ is therefore a direct summand of $\mathcal M(S_\infty)$. Here $\mathcal M(\mathbb N)$ is the locally profinite measure object, **not** the free measure object on a noncompact profinite set.

Taroyan's explicit source construction recalled in [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) realizes each positive rapid weight stage

$$
T_r=r\cdot\mathcal M(\mathbb N)
\tag{19.8}
$$

as a liquid object isomorphic to that direct summand. In particular, Lemma 19.2 applies to $T_r$ as a retract: Ext¹ of a retract is a direct summand of Ext¹ of the containing object, compatibly with target maps.

With the target (19.6) we obtain **natural isomorphisms**

$$
\mathrm{Ext}^1_{\mathcal A_p}
(T_r,\bigoplus_{n\ge1}B_n)
\cong
\bigoplus_{n\ge1}
\mathrm{Ext}^1_{\mathcal A_p}(T_r,B_n).
\tag{19.9}
$$

Indeed Lemma 19.2 gives the colimit over finite prefixes, and finite direct sums in an abelian category commute with Ext¹ in the coefficient variable. The comparison is natural in the weight $r$, because it is induced by the canonical coefficient inclusions and projections. This is the **missing local Ext¹ statement** from 018: it is stronger than ordinary Hom factorization, and it is proved without claiming $\mathrm{Ext}^1(T_r,B_n)=0$.

## 4. Countable direction globalizes finite output support

As in [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md), the weight poset $\mathscr R$ is countably directed and

$$
H\cong\underline s\cong\varinjlim_{r\in\mathscr R}T_r.
\tag{19.10}
$$

Fix a genuine class $\xi\in\mathrm{Ext}^1(H,E)$ for $E=\bigoplus_nB_n$. For every $r$, its restriction $\xi_r\in\mathrm{Ext}^1(T_r,E)$ has only finitely many nonzero coordinates by (19.9).

**Uniform finite support of the local classes.** Suppose infinitely many indices $n$ occurred nontrivially in $\xi_r$ for some $r$ (with $r$ depending on $n$). Choose one witness weight $r_n$ for each of those indices. Countable direction provides a common upper bound $r_\star$. Since $\xi_{r_n}$ is the restriction of $\xi_{r_\star}$ along $T_{r_n}\to T_{r_\star}$, the corresponding coordinate at $r_\star$ must be nonzero for every such $n$. This contradicts (19.9) at $r_\star$. Thus one **finite** set $F$ contains the support of every local class $\xi_r$.

For each $n\in F$, let $\xi_n$ be the image of $\xi$ under the canonical coefficient projection $E\to B_n$. Define the global finite-coordinate class

$$
\zeta=\sum_{n\in F}
(\iota_n)_*\xi_n\in\mathrm{Ext}^1(H,E).
\tag{19.11}
$$

Naturality of (19.9) gives $(\xi-\zeta)|_{T_r}=0$ for **every** $r$. The low-degree derived mapping edge for (19.10) is exact:

$$
0\longrightarrow
\varprojlim\nolimits_r^{1}\mathrm{Hom}(T_r,E)
\longrightarrow
\mathrm{Ext}^1(H,E)
\longrightarrow
\varprojlim_r\mathrm{Ext}^1(T_r,E).
\tag{19.12}
$$

This exact fragment requires neither projectivity of $T_r$ nor vanishing of their first Ext groups. The nested source-stage Hom systems and countably directed inverse-limit lemma (18.3), proved in [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md), give

$$
\varprojlim\nolimits_r^{1}\mathrm{Hom}(T_r,E)
\cong\bigoplus_n
\varprojlim\nolimits_r^{1}\mathrm{Hom}(T_r,B_n).
\tag{19.13}
$$

Thus the residual class $\xi-\zeta$, which belongs to the image of the first arrow in (19.12), comes from **finitely many** $B_n$ coefficient summands. Since $\zeta$ is already finite-coordinate, so is $\xi$.

It follows that

$$
\varinjlim_m\mathrm{Ext}^1
(H,\bigoplus_{n\le m}B_n)
\xrightarrow{\sim}
\mathrm{Ext}^1(H,\bigoplus_{n\ge1}B_n).
\tag{19.14}
$$

Injectivity also follows from the finite-prefix coordinate retractions, independently of the proof just given. Everything in this step is in ZFC: no Continuum Hypothesis or other additional set theory is used.

## 5. Transfer back to compactly supported test functions

By the Valdivia–Vogt representation recorded and source cited in [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md), one has a noncanonical LF topological isomorphism

$$
\mathcal D(\mathbb R)
\cong\bigoplus_{n\ge1}^{\mathrm{LF}}s.
\tag{19.15}
$$

The liquid realization of the left side is $G$ by [LFO-013](../LFO3_SURJECTIVITY_THEOREM_013.md). The right side is $E$ in (19.6). Under this isomorphism, the **finite-summand filtration** is cofinal with the **compact-support filtration in its effect on first Ext**: each finite sum of Fréchet spaces maps continuously into $\mathcal D(\mathbb R)$ and lands in a common compact-support stage by fixed-Fréchet-to-strict-LF factorization (LFO-013). Conversely each compact-support Fréchet stage maps continuously into the LF direct sum and lands in a finite direct sum. All these stage factorizations are morphisms of liquid modules by full faithfulness on Fréchet realizations and the closed-stage comparison.

Consequently the images of the two filtered-colimit Ext¹ maps agree, and (19.14) gives **surjectivity** of (19.1). The already reviewed EXT-015A injection supplies **injectivity**. This completes the proof of Theorem 19.1. $\square$

## 6. Independent hostile review and exact claim boundary

1. **Nonprojective free source.** $\mathcal M(S_\infty)$ was never assumed projective. Its *extremally disconnected cover* is projective, and its relation kernel is generated by the free measure object on the profinite kernel pair. The distinction is essential.
2. **No unjustified derived compactness.** Lemma 19.2 proves a target-specific relative first-Ext factorization from an explicit *two-term projective presentation*, not from ordinary Hom compactness or a false general interchange of Ext with filtered colimits.
3. **Noncompact relation space prohibited.** $R=T\times_ST$ is compact profinite. It is this fact that makes a map from the relation generator uniformly output-stage bounded. Replacing $R$ with a noncompact locally profinite relation space would invalidate the argument.
4. **Known nonzero scalar Ext.** A nonzero $\mathrm{Ext}^1(\underline s,\underline{\mathbb R})$ under CH is compatible with the theorem: its target is already one coordinate. This result asserts finite support of **every realized liquid class with direct-sum output**, not scalar Ext vanishing.
5. **Ghost plots.** The nonzero pointwise-invisible quotient section from [018](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) is compatible with our proof: sections of a cokernel on a profinite set require descent, not singleton tests. Lemma 19.2 uses **free-module cokernel preservation**, not pointwise equality.
6. **Original auxiliary counterexample.** The nonsplit extension from [017](SCALAR_PHANTOM_ESCAPE_017.md) has non-Fréchet source $\mathsf Q$, not a countably directed colimit of the specified weight stages with their Hom properties, and is no contradiction.
7. **What is not concluded.** No theorem for a varying source support stage, arbitrary nonregular LF output, higher Ext groups, quantum completed limits, or differentiable factorization-algebra comparison follows automatically.

**Source theorem checks required at protected admission:** (i) Effective-epimorphism/coequalizer of $T\to S$ in condensed sets; (ii) free p-liquid module universal property on arbitrary profinite sets and projectivity on extremally disconnected sets (Scholze, *Lectures on Analytic Geometry*, Theorem 6.5); (iii) Taroyan's real-liquid weight-stage colimit representation and its countable direction; (iv) Valdivia–Vogt test-function LF representation and LFO-013 finite-support factorization. Each is used with its stated scope.

**Mathematical consequence:** For the fixed nuclear Fréchet test-function source and the ordinary compact-support strict LF output, an Ext¹ class does **not** carry irreducible global output-support information. The proof is a targeted degree-one statement, not a claim about all derived or smooth observables.
