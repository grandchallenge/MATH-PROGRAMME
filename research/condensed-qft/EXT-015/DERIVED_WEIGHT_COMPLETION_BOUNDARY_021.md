# EXT-015D / 021 — support, weight completion and a derived-limit boundary

**Disposition:** PROVED, in complexes of real vector spaces, two explicit independent obstructions to promoting the admitted fixed-source first-Ext comparison to a completed differentiable pro-cochain comparison. PROVED a sufficient inverse-limit comparison lemma for the underlying complexes. **NOT PROVED:** an equivalence in Costello–Gwilliam's differentiable multicategory, a higher liquid Ext theorem, or Weiss descent. Neither counterexample asserts failure of the actual quantum-observables comparison.

**Inputs:** [positive liquid first-Ext comparison 019](FIXED_SOURCE_EXT1_ISOMORPHISM_019.md) and [critical audit 020](AGENT_CRITICAL_REVIEW_019_020.md). Primary smooth/filtered definitions: Costello–Gwilliam, *Factorization Algebras in Quantum Field Theory*, Volume I, Appendix B.6, **Definition B.6.0.7**, **Definition B.6.0.8**, **Lemma B.6.0.11** and **Definition B.6.1.1**, printed pp. 469–471, [source PDF](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf#page=479). The source defines completion before taking the relevant filtered coproduct and requires smooth, filtration-compatible multilinear maps. The present arguments intentionally examine only the underlying complexes.

## 1. Two distinct limit operations

Let $k=\mathbb R$. For support index $b\in\mathbb N$ and weight $w\in\mathbb N$, let $V_{b,w}^{\bullet}$ be cochain complexes with **injective** transition maps in $b$. Assume the differentials preserve weights. Form the weight-complete cochain complex

$$
C_b=\prod_{w\ge0}V_{b,w}^{\bullet},
\qquad
F^NC_b=\prod_{w\ge N}V_{b,w}^{\bullet}.
\tag{21.1}
$$

These are complete and separated: $C_b=\varprojlim_N C_b/F^NC_b$, with finite truncation $C_b/F^NC_b=\bigoplus_{w<N}V_{b,w}^{\bullet}$. There are **two different constructions**:

$$
C_{\mathrm{naive}}=\varinjlim_b C_b,
\qquad
C_{\mathrm{completed}}
=\varprojlim_N\varinjlim_b (C_b/F^NC_b).
\tag{21.2}
$$

The second is the filtered-completed support colimit of the underlying complexes. It is the operation demanded by the completed direct-sum convention in B.6.0.8; that convention is not the ordinary uncompleted colimit.

**Theorem 21.1 (exact order-of-operations criterion).** There is a natural isomorphism of cochain complexes

$$
C_{\mathrm{completed}}
\cong
\prod_{w\ge0}\left(\varinjlim_bV_{b,w}^{\bullet}\right).
\tag{21.3}
$$

The canonical map $C_{\mathrm{naive}}\to C_{\mathrm{completed}}$ is injective. Its image consists exactly of families $(x_w)_w$ for which **one common support stage $b$** contains every $x_w$ (and a cochain representative of each of its finitely many nonzero cohomological-degree components). It induces an isomorphism modulo $F^N$ for **every** finite $N$, so its image is dense in the filtration topology. It is surjective exactly when all families admit a common support stage.

**Proof.** Filtered colimits commute with finite direct sums of complexes of real vector spaces. Thus for each finite $N$,

$$
\varinjlim_b(C_b/F^NC_b)
=\bigoplus_{w<N}\varinjlim_bV_{b,w}^{\bullet}.
$$

The inverse limit over finite prefixes is the countable product, giving (21.3). Injectivity follows because stages embed coordinatewise and an element that is zero in every output coordinate must already be zero at its original stage. A family in the image is exactly one represented by an element of one $C_b$; conversely a common stage collects all coordinates into the product $C_b$. Every finite prefix of a family has a common support stage by taking the maximum of finitely many indices, which proves the finite-quotient assertion. The completion is separated, so the finite-quotient assertion also proves density. $\square$

If the differential has **filtration-raising terms** rather than preserving weight exactly, the same underlying vector-space argument applies provided it is compatible with all finite weight quotients. The result is then an identification of the corresponding complete complexes with their induced continuous differential; an unbounded differential not preserving filtration is outside the claim.

## 2. An explicit failure with zero differential

For $b,w\ge0$, set

$$
V_{b,w}=\begin{cases}
\mathbb R,&w\le b,\\
0,&w>b,
\end{cases}
\qquad d=0.
\tag{21.4}
$$

All support transitions are split injections, all finite-dimensional stages are smooth in the usual sense, and every weight truncation stabilizes once $b\ge N$.

**Theorem 21.2 (completion does not commute with ordinary support colimit).**

$$
C_{\mathrm{naive}}
=\mathbb R^{(\mathbb N)},
\qquad
C_{\mathrm{completed}}
=\mathbb R^{\mathbb N},
\qquad
\mathrm{coker}(C_{\mathrm{naive}}\to C_{\mathrm{completed}})
=\mathbb R^{\mathbb N}/\mathbb R^{(\mathbb N)}
\ne0.
\tag{21.5}
$$

**Proof.** $C_b$ consists of the first $b+1$ coordinates, so the union has finite coordinate support. The finite $N$ truncation at sufficiently large $b$ is $\mathbb R^N$, and inverse limit over $N$ is the full product. The constant sequence $(1,1,\ldots)$ is a concrete element of the product not belonging to any $C_b$. With zero differential the failure occurs already in $H^0$. $\square$

**Scope:** This is **not** a counterexample to the completed-colimit construction of Costello–Gwilliam; it demonstrates precisely why their Definition B.6.0.8 completes it. It is not a refutation of EXT-015C's finite-support first-Ext theorem, which concerns each *individual* extension class without a simultaneous unbounded weight family.

## 3. A separate higher-derived limit obstruction

Let $E=\mathbb R^{(\mathbb N)}$ be the vector space of finitely supported scalar sequences, and $A_N=\bigoplus_{j\ge N}\mathbb Re_j\subset E$. Consider the cochain complex, concentrated in degrees $0,1$,

$$
K_N:\quad E\ \xrightarrow{\;\pi_N\;}\ E/A_N\cong\mathbb R^N.
\tag{21.6}
$$

Bonding maps $K_{N+1}\twoheadrightarrow K_N$ are the identity in degree zero and the finite-coordinate projection in degree one. They are **surjective in every cochain degree**, and each $K_N$ has

$$
H^0(K_N)=A_N,\qquad H^1(K_N)=0.
\tag{21.7}
$$

**Theorem 21.3 (first cohomology appears at the complete limit).** The inverse limit is

$$
\varprojlim_NK_N:\quad
\mathbb R^{(\mathbb N)}
\hookrightarrow\mathbb R^{\mathbb N},
$$

and therefore

$$
H^1(\varprojlim_NK_N)
\cong\mathbb R^{\mathbb N}/\mathbb R^{(\mathbb N)}
\ne0
\quad\text{although}\quad H^1(K_N)=0\ \forall N.
\tag{21.8}
$$

Moreover the Milnor correction is **exactly** this quotient:

$$
\varprojlim\nolimits_N^1 H^0(K_N)
\cong\mathbb R^{\mathbb N}/\mathbb R^{(\mathbb N)}.
\tag{21.9}
$$

**Proof.** The inverse limit in degree zero is $E$ because all bonding maps are the identity; in degree one the limit of the finite-coordinate spaces is $\mathbb R^{\mathbb N}$. Their differential is the canonical injection, so (21.8) follows.

For (21.9), take the towerwise short exact sequence $0\to A_N\to E\to E/A_N\to0$. The inverse system of $E$ is constant, so its first derived inverse limit vanishes. The direct limit along the decreasing $A_N$ is irrelevant; its ordinary inverse limit is $\bigcap_N A_N=0$. The long exact inverse-limit sequence yields

$$
\varprojlim\nolimits_N^1 A_N
\cong
\mathrm{coker}\!\left[
E\longrightarrow\varprojlim_N(E/A_N)
\right]
=\mathbb R^{\mathbb N}/\mathbb R^{(\mathbb N)}.
$$

A direct Roos witness is the sequence $(e_N)_{N\ge0}$ in $\prod_NA_N$. If it were a coboundary, finitely supported $a_N\in A_N$ would satisfy $a_N-a_{N+1}=e_N$. Repeated substitution forces the fixed finitely supported $a_0$ to contain every basis coefficient $e_N$, which is impossible. Thus the derived-limit class is genuinely nonzero. $\square$

**Why this matters:** Surjectivity of transition maps on *cochain degrees* makes the ordinary inverse limit model the homotopy inverse limit. It does **not** make the inverse limit commute with cohomology. In this example $H^0(K_N)=A_N$ has a non-Mittag–Leffler decreasing-image tower, so its first derived limit survives in $H^1$.

This is a deliberately elementary **vector-space** obstruction, not yet a constructed nonzero liquid $\mathrm{Ext}^2$ class or quantum observable. It shows which hypothesis a proposed higher-derived lifting theorem has to prove.

## 4. A positive finite-quotient comparison criterion

**Proposition 21.4 (safe algebraic passage to completion).** Let $f_N:X_N^\bullet\to Y_N^\bullet$ be a morphism between sequential inverse systems of cochain complexes of real vector spaces. Assume the transition maps in both systems are surjective in each cochain degree. If **every** $f_N$ is a quasi-isomorphism, then

$$
\varprojlim_N f_N:
\varprojlim_NX_N^\bullet
\longrightarrow
\varprojlim_NY_N^\bullet
\tag{21.10}
$$

is a quasi-isomorphism.

**Proof.** For degreewise surjective towers, ordinary inverse limits compute the derived inverse limits of complexes; equivalently the Roos product-difference map is degreewise surjective. The homotopy inverse limit of a diagram of quasi-isomorphisms is a quasi-isomorphism. Concretely, the Milnor short exact sequences

$$
0\to\varprojlim\nolimits_N^1H^{q-1}(X_N)
\to H^q(\varprojlim_NX_N)
\to\varprojlim_NH^q(X_N)\to0
$$

and the corresponding sequence for $Y_N$ have isomorphic left and right terms, by naturality and levelwise quasi-isomorphism. The middle terms are therefore isomorphic. $\square$

If only the finite quotients have a quasi-isomorphism in degrees at most $1$, the analogous low-degree conclusion **requires checking the degree-zero Milnor corrections as well**; the existence of a first-Ext stage theorem alone is insufficient.

**Differentiable caution.** Proposition 21.4 is about underlying complexes. The B.6.0.11 criterion additionally requires the specified *differentiable fibrations*, eventual stabilization of filtration quotients and quasi-isomorphisms of the relevant fibers. An algebraically surjective map need not have the differentiable fibration property, and an algebraic quasi-isomorphism need not respect smooth plots. The B.6.1.1 smooth multilinear operations impose further obligations.

## 5. Concrete EXT-015D mathematical boundary and next test

For each compact output-support cutoff $b$, each quantum weight $N$, and every required arity $k$, the programme must provide **actual** complexes and smooth multilinear maps. The following requirements are **independent**:

| Gate | Mathematical contract | Status |
| --- | --- | --- |
| D-WT | Define completed weight quotient $C_b/F^{N}C_b$ and verify support-stage maps | ABSTRACT MODEL VERIFIED; ACTUAL QFT MODEL OPEN |
| D-ORD | Use completed support colimit, not $\varinjlim_b$ of complete stages without completing again | NECESSARY; explicit noncommutation 21.2 |
| D-ROOS | Check $\varprojlim^1_NH^{q-1}(C_b/F^NC_b)$, or use true levelwise quasi-isomorphisms with degreewise surjective towers | ABSTRACT COUNTEREXAMPLE 21.3; QFT CHECK OPEN |
| D-DIFF | Verify smooth plots, differentiable cofibrations/fibrations, and filtration-compatible multilinear maps of B.6.0.7–B.6.1.1 | OPEN |
| D-WEISS | Verify factorization multiplication and Cech/Weiss descent **after** the appropriate completed coproduct | OPEN |
| D-HIGH | Verify positive degree $q\ge2$ of the actual liquid target-stage derived comparison | OPEN |

A **specific positive next experiment** is to build the first nontrivial quantum-weight quotients of the actual linear field-observable model on nested intervals and verify both (i) completion order at each fixed weight, and (ii) the Milnor correction of the weight tower in degrees zero and one. The model must be genuine differentiable B.6 data before any upgrade from underlying-chain results.

**Verdict:** The existing fixed-source Ext¹ theorem is preserved. Further mathematical work is now reduced to independently checkable quantum-weight completion, higher-derived-limit and smooth Weiss gates. No Human Steward routine approval is needed to work on them.
