# EXT-015 REACH-R3 / 031 — an explicit projective summand of the actual first liquid syzygy

**Disposition: NEW MATHEMATICAL CANDIDATE; critical review required.** This is a source-specific reduction in the real p-liquid category. It does **not** decide the degree-two target-stage Ext comparison. It exhibits a genuinely support-escaping map from the original syzygy that is a **projective boundary**, and then splits off an explicit countably generated projective summand so that this entire family of trivial representatives can be removed algebraically.

**Exact sources:** protected [review 016](AGENT_CRITICAL_REVIEW_AB_016.md), in particular its actual measure-generator cover (B-16.2)–(B-16.3); protected [result 019](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md), which proves first Ext for the fixed source but does not prove it for its syzygy; protected D14 [028](D14_REGULATED_BV_SYZYGY_028.md), Theorem 28.2. Source audit was against protected main 37384b473239aee26fb6cbefde1b020f06b375fc.

## 1. Actual liquid source and actual projective cover

Fix 0 < p <= 1. Put $E=\mathcal D_{[-1,1]}(\mathbb R)$, $H=\underline E$, and take exactly the projective cover of 016:

$$
P_0=\bigoplus_{(T,u)\in\mathscr S_H}\mathcal M_{<p}(T),
\qquad
\varepsilon:P_0\twoheadrightarrow H,
\qquad K_0=\ker\varepsilon.
\tag{31.1}
$$

Each $T$ is extremally disconnected and has the prescribed weight bound; the summand map is induced by $u:T\to E$. Since a singleton is extremally disconnected, for **each** $w\in E$ the indexing system includes a singleton summand $\mathcal M_{<p}(*)=\underline{\mathbb R}$. Let $e_w\in P_0(*)$ denote its canonical generator. Then $\varepsilon(e_w)=w$. These are morphisms and points of the **specified** liquid projective cover, not an informal free vector-space resolution.

Choose a nonzero $v\in E$. For every integer $n\geq1$ form the relation

$$
r_n=e_{2nv}+e_v-e_{(2n+1)v}\in K_0(*).
\tag{31.2}
$$

The inclusion in $K_0$ is justified because $\varepsilon(r_n)=2nv+v-(2n+1)v=0$. The singleton labels $2nv$, $(2n+1)v$ and $v$ have the intended distinctness; no two even and odd positive integer multiples coincide.

## 2. A genuine projective direct summand of K0

Put $Q=\bigoplus_{n\geq1}\underline{\mathbb R}$ in the category $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$. Define

$$
s:Q\longrightarrow K_0,\quad s(e_n)=r_n.
\tag{31.3}
$$

Because each factor is the projective singleton liquid module and $Q$ is a coproduct, the specified family of morphisms uniquely defines a liquid map $s$; its existence is not contingent on a topology on an infinite-dimensional vector-space model.

Define $\widetilde q:P_0\to Q$ **on every projective summand** by

- On the singleton summand indexed by $2nv$, send its generator to $e_n\in Q$;
- On every other singleton summand, and every non-singleton summand, send the summand to zero.

The universal property of the coproduct $P_0$ supplies a unique liquid morphism. Set $q=\widetilde q|_{K_0}$.

**Theorem 31.1 (explicit split projective relation summand).** The maps $s$ and $q$ satisfy $q s=\mathrm{id}_Q$. Hence

$$
K_0\simeq Q\oplus K_0^{\mathrm{red}},
\qquad
K_0^{\mathrm{red}}=\ker(q),
\tag{31.4}
$$

with explicit complementary idempotents $s q$ and $1-s q$. Moreover $Q$ is projective, because the singleton $\underline{\mathbb R}$ is projective by Scholze's Theorem 6.5 and a coproduct of projectives remains projective in this module category.

**Proof.** On each generator $e_n\in Q$,

$$
q\,s(e_n)=
\widetilde q(e_{2nv}+e_v-e_{(2n+1)v})=e_n.
$$

Equality on each coproduct summand gives equality of morphisms. The idempotent decomposition is an ordinary splitting in the abelian liquid category. Each projective Hom functor is exact in the coefficient variable, and products of surjections of abelian groups are surjective, so the coproduct $Q$ is projective. $\square$

For every liquid coefficient module $T$ and $j\geq1$ this gives the **natural** isomorphism

$$
\mathrm{Ext}^j_{\mathcal A_p}(K_0,T)
\simeq
\mathrm{Ext}^j_{\mathcal A_p}(K_0^{\mathrm{red}},T).
\tag{31.5}
$$

In particular, the original degree-two filtered-output comparison reduces to the same degree-one comparison for $K_0^{\mathrm{red}}$. This is a real reduction of the actual syzygy, not its solution.

## 3. A concrete escaping support map which represents zero Ext

Take smooth $g_n$ on the target real line with nonzero compact support contained in $(n+2,n+3)$. Regard their images as points of the liquid strict-LF union $G$ of 016–019. They have no common compact-support output stage $G_b$.

Define $j:Q\to G$ by $j(e_n)=g_n$, using the coproduct universal property. Put $\psi=j\widetilde q:P_0\to G$, and let $\phi=\psi|_{K_0}=j q$.

**Theorem 31.2 (support escape does not imply a nonzero liquid extension).** The actual liquid map $\phi:K_0\to G$ cannot factor through any compact-output stage $G_b$, because $\phi(r_n)=g_n$. Nevertheless $\phi$ represents **zero** in $\mathrm{Ext}^1(H,G)$: by construction $\phi=\psi i$ is a projective boundary for the genuine presentation (31.1).

**Proof.** If $\phi$ factored through $G_b$, each $\phi(r_n)$ would have support in $[-b,b]$, contradicted by $\mathrm{supp}(g_n)\subset(n+2,n+3)$ for sufficiently large $n$. The factorization through the projective map $\psi$ proves its Ext class vanishes by the cokernel description (B-16.4) in review 016. $\square$

This is an **adversarial example within the actual source syzygy**. Any search claiming a nonzero higher Ext obstruction from a support-escaping syzygy map, without quotienting projective boundaries, is invalid.

## 4. Canonical normalization of syzygy cocycles on the summand

**Corollary 31.3 (split-summand boundary subtraction).** Every map $\varphi:K_0\to G$ is cohomologous, in the projective presentation of $H$, to a map that vanishes identically on $s(Q)$.

**Proof.** Put $\varphi_{\mathrm{red}}=\varphi-\varphi s q$. Since $q=\widetilde q i$, we have

$$
\varphi-\varphi_{\mathrm{red}}
=(\varphi s\widetilde q)i;
\tag{31.6}
$$

thus the difference is an explicit projective boundary. Also $\varphi_{\mathrm{red}}s=\varphi s-\varphi s q s=0$. The corrected map factors through the complementary summand $K_0^{\mathrm{red}}$ in (31.4). $\square$

Equation (31.6) is natural in the target coefficient; at each target support stage, any $\varphi$ already valued in $G_b$ has its subtraction still valued in $G_b$. Thus the reduction is compatible with the filtered stage comparison.

## 5. Exactly what remains

This result **does not** prove that $K_0^{\mathrm{red}}$ is Fréchet, countably presented, compact, projective or suitably localized. It does not prove or disprove surjectivity or injectivity of the target-stage comparison for $\mathrm{Ext}^1(K_0^{\mathrm{red}},-)$. It supplies a concrete splitting and a sharp hostile control to prevent an invalid negative claim.

The next obligation is to analyze the **remaining relation object** $K_0^{\mathrm{red}}$ using actual profinite kernel pairs, attempt a projective cover and exact relation presentation, and test whether the relative Ext-continuity lemma of 019 extends after boundary normalization. The positive line must bound cocycles modulo all boundaries; the negative line must survive them.

**Acceptance status:** Candidate proof of Theorems 31.1–31.2 and Corollary 31.3, pending a separately recorded mathematical adversarial audit. Correct parent: [REACH-R3 #2798](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2798). Preserve the open degree-two comparison in EXT-015D.
