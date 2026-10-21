# EXT-015 REACH-R3 / 037 — split off every singleton-linear relation from the actual liquid projective presentation

**Disposition: NEW COVER-REDUCTION MATHEMATICAL CANDIDATE; critical review needed.** A direct strengthening of [031](R3_SYZYGY_SPLIT_SUMMAND_031.md): it removes **all algebraic linear redundancies in the singleton summands** of the actual measure-module projective cover, not merely one countable family. No claim of degree-two liquid Ext continuity or of minimality among non-singleton profinite generators is made.

**Source:** the genuine projective real p-liquid cover from [GCL mathematical review 016, equations B-16.2/3](AGENT_CRITICAL_REVIEW_AB_016.md); the admitted [R3 first split 031](R3_SYZYGY_SPLIT_SUMMAND_031.md) and [critical review 034](AGENT_CRITICAL_REVIEW_REACH_R2_R3_034.md). Exact source head 1b6e1897a24ea7d4d898a2f0b90b22ee2e435399. Parent [REACH-R3 #2798](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2798).

## 1. Actual projective cover and singleton component

Fix 0 < p <= 1 and put

$$
E=\mathcal D_{[-1,1]}(\mathbb R),\quad
H=\underline E,\quad
P_0=\bigoplus_{(T,u)\in\mathscr S_H}\mathcal M_{<p}(T),
\quad
\varepsilon:P_0\twoheadrightarrow H,
\quad
K_0=\ker\varepsilon.
\tag{37.1}
$$

As in 016, the indexing set contains exactly one representative of each singleton plot $(\{*\},w)$ for $w\in E$. Partition its index set into singleton plots and all the remaining extremally disconnected profinite plots. Hence the projective cover itself decomposes as

$$
P_0=P_{\mathrm{pt}}\oplus P_{\mathrm{prof}},
\qquad
P_{\mathrm{pt}}=\bigoplus_{w\in E}\underline{\mathbb R}.
\tag{37.2}
$$

Each $\underline{\mathbb R}$ is the genuine projective liquid measure module $\mathcal M_{<p}(*)$; its generator $e_w$ maps to $w\in H(*)$. The direct sum in (37.2) is taken in the liquid category. No assertion that the map from $P_{\mathrm{pt}}$ alone is epic onto all condensed plots is needed.

Choose a Hamel basis $\mathcal B\subset E$ of the underlying **real vector space**. For each $w\in E\setminus\mathcal B$, there are unique finitely many scalars $c_{w,b}$ such that

$$
w=\sum_{b\in\mathcal B}c_{w,b}b,\qquad
r_w=e_w-\sum_{b\in\mathcal B}c_{w,b}e_b\in K_0(*).
\tag{37.3}
$$

Every displayed sum is finite **for each w**. No continuous Hamel-coordinate functional on $E$ is asserted or used.

## 2. Global projective splitting

Define

$$
Q_{\mathrm{pt}}=
\bigoplus_{w\in E\setminus\mathcal B}
\underline{\mathbb R},\qquad
P_{\mathrm{red}}=
\biggl(\bigoplus_{b\in\mathcal B}\underline{\mathbb R}\biggr)
\oplus P_{\mathrm{prof}}.
\tag{37.4}
$$

Thus $P_{\mathrm{red}}$ is literally the projective direct sum of basis-singleton modules and every original non-singleton profinite generator. Let $s:Q_{\mathrm{pt}}\to K_0$ be determined on each coproduct summand by $s(f_w)=r_w$. Let $\widetilde q:P_0\to Q_{\mathrm{pt}}$ be the liquid map determined by sending the singleton generator $e_w$ to $f_w$ for $w\notin\mathcal B$, and all basis singleton and non-singleton projective summands to zero. Let $q$ be its restriction to $K_0$.

**Theorem 37.1 (maximal singleton-linear split in the original cover).** The maps satisfy $q\,s=\mathrm{id}_{Q_{\mathrm{pt}}}$. The endomorphism

$$
\Pi=1-s\widetilde q:P_0\longrightarrow P_0
\tag{37.5}
$$

is an idempotent with image precisely $P_{\mathrm{red}}$ as explicitly embedded in the original cover, and $\varepsilon\Pi=\varepsilon$. In particular, the restriction

$$
\varepsilon_{\mathrm{red}}:
P_{\mathrm{red}}\twoheadrightarrow H
\tag{37.6}
$$

remains a **genuine epimorphism of real liquid modules**. Moreover

$$
K_0\simeq Q_{\mathrm{pt}}\oplus K_{\mathrm{red}},
\qquad
K_{\mathrm{red}}=\ker(\varepsilon_{\mathrm{red}}),
\tag{37.7}
$$

with explicitly defined retraction and inclusion. Both $Q_{\mathrm{pt}}$ and $P_{\mathrm{red}}$ are projective liquid modules.

**Proof.** The coproduct universal property defines every displayed map: a map from an individual singleton summand is determined by the chosen target point, and the map from each non-singleton summand in $\widetilde q$ is identically zero. The finite Hamel expression in (37.3) is used separately for each singleton summand, so no infinite product or discontinuous Hamel-coordinate map out of the completed Fréchet space occurs.

For a generator $f_w$ of $Q_{\mathrm{pt}}$,

$$
q\,s(f_w)
=\widetilde q(e_w-\sum_b c_{w,b}e_b)=f_w.
$$

Thus $s$ splits. The endomorphism $\Pi$ sends $e_w$ for nonbasis $w$ to $\sum_b c_{w,b}e_b$, fixes every basis generator $e_b$, and fixes every non-singleton projective summand. It is a projection onto $P_{\mathrm{red}}$, so $\Pi^2=\Pi$. Since $\varepsilon(s(Q_{\mathrm{pt}}))=0$, $\varepsilon\Pi=\varepsilon$. As $\varepsilon$ is epic by 016 and factors through its restriction to $P_{\mathrm{red}}$, $\varepsilon_{\mathrm{red}}$ is epic. Applying the projection to the kernel shows $\Pi K_0=K_0\cap P_{\mathrm{red}}=K_{\mathrm{red}}$ and proves (37.7).

The projectivity statement is a direct use of the projectivity of $\underline{\mathbb R}=\mathcal M_{<p}(*)$, of every original $\mathcal M_{<p}(T)$, and of the fact that set-indexed coproducts of projectives are projective in this abelian module category. $\square$

## 3. Higher derived comparison reduces to a smaller true liquid syzygy

**Corollary 37.2.** For each liquid coefficient $T$ and each $j\ge1$,

$$
\mathrm{Ext}^j_{\mathrm{Liq}_p}(K_0,T)
\simeq
\mathrm{Ext}^j_{\mathrm{Liq}_p}(K_{\mathrm{red}},T)
\tag{37.8}
$$

naturally in $T$. In particular the **degree-two filtered-output comparison** for the original test-function source reduces without loss to

$$
\varinjlim_b \mathrm{Ext}^1(K_{\mathrm{red}},G_b)
\longrightarrow
\mathrm{Ext}^1(K_{\mathrm{red}},G).
\tag{37.9}
$$

Every syzygy cocycle $\varphi:K_0\to G$ is cohomologous (in the original cover's cokernel) to a cocycle vanishing on **all** singleton Hamel-linear relations $r_w$: subtract the projective boundary

$$
\bigl((\varphi s)\widetilde q\bigr)|_{K_0}.
\tag{37.10}
$$

**Proof.** For (37.8) use additivity of derived Hom in its first finite direct-sum argument, the decomposition (37.7), and $\mathrm{Ext}^j(Q_{\mathrm{pt}},T)=0$ for $j\ge1$ by projectivity. The isomorphisms commute with every target-stage inclusion $G_b\hookrightarrow G$ because the source splitting is independent of $T$. For (37.10), $\varphi-\varphi s q$ annihilates the image of $s$, and the difference extends to $P_0$ through $\varphi s\widetilde q$. It is therefore a boundary in the actual presentation of $H$, not merely in a vector-space shadow. $\square$

## 4. What has been removed and what has not

**Removed exactly:** all relations from expressing an arbitrary **singleton generator** $e_w$ linearly in singleton generators indexed by the Hamel basis. The construction is stronger than and subsumes the special redundant relations used in 031. Dependence on an arbitrary Hamel basis is harmless for the **abstract Ext isomorphism**, but no natural preferred Hamel basis or continuous Hamel-coordinate map is claimed.

**Still present:** the non-singleton projective generators indexed by genuinely nonconstant profinite plots into $E$, and their relations with the basis-singleton component. The reduced first syzygy $K_{\mathrm{red}}$ is not shown to be Fréchet, countably generated, compact, relative-Ext-continuous or projective.

**Next decisive mathematics:** obtain an exact **kernel-pair/projective relation cover of $K_{\mathrm{red}}$** involving only the remaining nonconstant profinite plots. Test relative support-localization *modulo every actual projective boundary*. A positive global stage theorem or a genuine liquid cocycle persisting through all target quotients remains the degree-two verdict; the present result does not decide either.

## 5. Adversarial verification

The exact finite-rank fixture [037](fixtures/check_all_singleton_relations_037.py) evaluates the idempotent $\Pi$, $q s=1$, and $\varepsilon\Pi=\varepsilon$ for rational finite-dimensional models with redundant singleton generators. This is a **finite algebra check only**. The real-liquid proof depends on the categorical coproduct/projectivity arguments above, not a numerical assertion.

**Status:** Theorems 37.1 and Corollary 37.2 are new candidate mathematics; a source-locked distinct role-scoped mathematical audit is mandatory before mathematical admission. REACH-R3 remains OPEN pending the actual reduced-syzygy Ext stage comparison.
