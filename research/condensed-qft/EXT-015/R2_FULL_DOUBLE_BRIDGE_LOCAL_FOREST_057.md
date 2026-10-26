# EXT-015 REACH-R2 / 057 — complete recursive proper-subgraph forest for the double-bridge graph

**Status:** new bounded mathematical candidate; exact independent critical review and protected admission required. This completes the proper 1PI **subgraph** calculation left open by [R2/055](R2_DOUBLE_BRIDGE_INSERTION_DEFECT_055.md), not just a whole-graph correction. The eight-edge, six-vertex graph formed from two triangles and two crossing edges has **ten** proper 1PI subgraphs and **24** proper Zimmermann-compatible forests. Its entire source-local counterterm library can be constructed recursively from intrinsic Gaussian graph data. After insertion of *all* those proper counterterms, exactly two graph-local divergences remain, a scalar delta at order $\epsilon^{-3}$ and a second-derivative delta at order $\epsilon^{-1}$; subtracting them gives a strong distributional limit of zero.

**Not claimed:** a forest recursion for arbitrary graphs, arbitrary differentiated/Wick subgraph sources, a globally closed BV second-order operator or interacting QME, completed normal-topology B.6 Weiss descent, or the original liquid higher-Ext verdict.

**Source dependencies:** protected [R2/049](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md), [R2/051](R2_K4_NESTED_OVERLAP_FOREST_051.md), [R2/053](R2_BRANCHING_FOREST_FACTORISATION_053.md); source candidate [R2/055](R2_DOUBLE_BRIDGE_INSERTION_DEFECT_055.md) and its exact covariance computations. The latter's source PR [#2849](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2849) was not yet merged when this stacked candidate was started. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. Fixed graph and all proper forests

The vertex set is $V=\{0,1,2,3,4,5\}$ and the eight separately labeled edges are

$$
e_0=01,\ e_1=12,\ e_2=02,\quad
e_3=34,\ e_4=45,\ e_5=35,\quad
e_6=03,\ e_7=14.
\tag{57.1}
$$

Every edge uses the normalized unit Gaussian delta approximate identity $\kappa_\epsilon$. For a connected subgraph $\gamma$, let $h_\gamma=|E(\gamma)|-|V(\gamma)|+1$ be its cycle rank; $\tau(\gamma)$ its spanning-tree count (unit edge weights).

**Lemma 57.1 (complete 1PI and forest inventory).** The proper bridgeless connected cyclic subgraphs are exactly the following ten:

| Index | Edge labels | Vertices | Cycle rank | $\tau$ |
| --- | --- | --- | --- | --- |
| A | 0,1,2 | 3 | 1 | 3 |
| B | 3,4,5 | 3 | 1 | 3 |
| C | 0,3,6,7 | 4 | 1 | 4 |
| D | 0,4,5,6,7 | 5 | 1 | 5 |
| E | 1,2,3,6,7 | 5 | 1 | 5 |
| F | 0,1,2,3,6,7 | 5 | 2 | 11 |
| H | 0,3,4,5,6,7 | 5 | 2 | 11 |
| I | 1,2,4,5,6,7 | 6 | 1 | 6 |
| J | 0,1,2,4,5,6,7 | 6 | 2 | 14 |
| K | 1,2,3,4,5,6,7 | 6 | 2 | 14 |

The only vertex-disjoint pair is $\{A,B\}$. There are **12 nested pairs**, and no larger compatible proper forest. Hence there are

$$
1+10+12+1=\boxed{24}
\tag{57.2}
$$

admissible proper forests, where the terms count empty, singleton, nested-pair and disjoint-pair forests. There are **four crossing simple cycles** (lengths four, five, five, six), and four additional crossing 1PI sources with cycle rank two.

**Proof.** Enumerate the edge subsets of the eight-edge graph and retain those connected after deleting every chosen edge. The exhaustive finite characterization is directly reproducible in [fixture 057](fixtures/check_full_double_bridge_forest_057.py), with a finite case partition by edge count and cycle rank. The subsets in the table are exactly all the survivors. For forest compatibility, two sources must be nested by edge inclusion, or disjoint in vertices. Among the ten, the only vertex-disjoint pair is $A,B$; direct inclusion comparison yields twelve strict nested pairs, none participating in a longer chain. This proves the count. $\square$

## 2. Graph-intrinsic scalar counterterms by increasing loop number

For any connected unit-weight Gaussian graph $\gamma$, its regulated amplitude has the exact form

$$
T_{\gamma,\epsilon}
=(2\pi)^{-h_\gamma/2}
\tau(\gamma)^{-1/2}\epsilon^{-h_\gamma}
\rho_{\gamma,\epsilon},
\tag{57.3}
$$

where $\rho_{\gamma,\epsilon}$ is the appropriately normalized relative Gaussian approximate identity. The scalar coefficient $\tau(\gamma)^{-1/2}$ depends only on the source graph.

For every proper 1PI source $\gamma$ in Lemma 57.1 define its recursively **prepared overall subtraction**

$$
C_{\gamma,\epsilon}
=(2\pi)^{-h_\gamma/2}
a_\gamma\,\epsilon^{-h_\gamma}\delta_\gamma,
\tag{57.4}
$$

where $\delta_\gamma$ is the independent product of Dirac deltas on a spanning tree of the source. The coefficients $a_\gamma$ are defined in strictly increasing edge count by the source-only recursion

$$
a_\gamma=
\frac1{\sqrt{\tau(\gamma)}}
-
\sum_{\substack{\beta\subsetneq\gamma\\
\beta\text{ proper 1PI}}}
\frac{a_\beta}{\sqrt{\tau(\gamma/\beta)}}.
\tag{57.5}
$$

Contract every vertex of $\beta$ to one vertex to construct $\gamma/\beta$, retain all other edges with multiplicity, and allow self-loop edges, which contribute a Gaussian $\kappa_\epsilon(0)$ but do not change the tree determinant. **No proper source $\gamma$ in the table contains two vertex-disjoint divergent 1PI children**; this is why (57.5) has no disconnected-child product term. For the full graph, the pair $\{A,B\}$ must be included and will be explicitly included in Section 3.

**Lemma 57.2 (entire prepared-source table).** For the six one-loop sources $A,B,C,D,E,I$ the coefficients are respectively $1/\sqrt3,1/\sqrt3,1/2,1/\sqrt5,1/\sqrt5,1/\sqrt6$. The four two-loop sources have

$$
\begin{aligned}
a_F=a_H&=
\frac1{\sqrt{11}}
-\frac13-\frac1{\sqrt8}-\frac1{\sqrt5},\\
a_J=a_K&=
\frac1{\sqrt{14}}
-\frac1{\sqrt6}-\frac1{\sqrt{10}}-\frac1{2\sqrt3}.
\end{aligned}
\tag{57.6}
$$

These are *intrinsic proper-source constants*, fixed without reference to the containing six-vertex graph. The complete recursion is a valid distributional source preparation: every source has cycle rank one or two, so its only negative Laurent term after subgraph subtraction is the scalar $\epsilon^{-h_\gamma}\delta_\gamma$; there are no divergent derivative-delta terms for a proper source.

**Proof.** One-loop sources contain no proper 1PI cyclic subgraph, and their coefficient is their isolated-cycle tree normalization. A two-loop proper source has exactly three proper one-loop 1PI children, all pairwise overlapping, so only singleton proper forests contribute to its preparation. Source-level contraction gives quotient spanning-tree counts $(3,2,1)$ for the respective triangle, square and five-cycle children of each $\tau=11$ source, and $(4,2,1)$ for the respective triangle, five-cycle and six-cycle children of each $\tau=14$ source. Multiplying the reciprocal square roots of these quotient counts by the intrinsic child coefficients gives exactly the terms displayed in (57.6). Formula (57.5) gives the two explicit expressions. The source regulated amplitudes and each collapsed child insertion have Gaussian expansions with even moments and common overall degree $\epsilon^{-2}$; their next term is order $\epsilon^0$, hence no derivative counterterm is required on these proper sources. $\square$

**Counterterm sign convention:** $C_{\gamma,\epsilon}$ is the signed kernel **subtracted** from the source amplitude. The prepared two-loop coefficients in (57.6) are negative, as in the earlier theta example; this is permissible. The formula must not multiply a nested child's singular delta directly with its parent's singular delta. The parent coefficient in (57.6) already incorporates its three nested child contributions.

## 3. The full 24-forest preparation

For the full graph $G$, define the prepared amplitude

$$
\begin{aligned}
\overline R_{G,\epsilon}
={}&T_{G,\epsilon}
-\sum_{\gamma\in\{A,B,C,D,E,F,H,I,J,K\}}
C_{\gamma,\epsilon}
\,T_{G\setminus\gamma,\epsilon}\\
&+C_{A,\epsilon}C_{B,\epsilon}
\,T_{G\setminus(A\cup B),\epsilon}.
\end{aligned}
\tag{57.7}
$$

Each product is interpreted by identifying the subgraph coincidence deltas, multiplying only the *remaining positive-regulator smooth edge kernels*, and using independent coordinates for the disjoint $A,B$ product. Formula (57.7) is a **compressed forest sum**: the 12 nested forests are already included inside the four recursively prepared two-loop parent coefficients, and the one disjoint pair appears explicitly as the final positive term.

For a collection $F$ of contracted, disjoint source subgraphs, let $Q_{G/F}$ be the reduced weighted Laplacian of the quotient, and let $M_{G/F}$ be its inverse covariance embedded into the fixed original relative coordinates

$$
y=(x_0-x_3,x_1-x_3,x_2-x_3,x_4-x_3,x_5-x_3)
\tag{57.8}
$$

by the natural equality map on contracted vertex coordinates. If all vertices collapse, take $M_{G/F}=0$.

## 4. Exact scalar and derivative poles of the full forest preparation

Let $\delta_G$ be the full diagonal delta distribution in the five relative coordinates. Define

$$
\begin{aligned}
\mathfrak a_G &=
\frac1{\sqrt{\tau(G)}}
-\sum_{\gamma\subsetneq G\atop \gamma\text{ 1PI}}
\frac{a_\gamma}{\sqrt{\tau(G/\gamma)}}
+\frac{a_Aa_B}{\sqrt{\tau(G/(A\cup B))}},
\\
\mathfrak B_G&=
\frac12\left[
\frac{M_G}{\sqrt{\tau(G)}}-
\sum_{\gamma\subsetneq G\atop\gamma\text{ 1PI}}
\frac{a_\gamma M_{G/\gamma}}{\sqrt{\tau(G/\gamma)}}
+\frac{a_Aa_BM_{G/(A\cup B)}}{\sqrt{\tau(G/(A\cup B))}}
\right].
\end{aligned}
\tag{57.9}
$$

Here $\tau(G)=30$, the ten source quotient tree counts, in the exact order of Lemma 57.1, are

$$
(8,8,4,2,2,2,2,1,1,1),
\quad
\tau(G/(A\cup B))=2.
\tag{57.10}
$$

**Theorem 57.3 (complete double-bridge local forest recursion and strong limit).** The prepared amplitude has exactly the two negative Laurent orders

$$
\overline R_{G,\epsilon}
=
(2\pi)^{-3/2}\left[
\frac{\mathfrak a_G}{\epsilon^3}\delta_G
+\frac1\epsilon\sum_{i,j=0}^{4}
(\mathfrak B_G)_{ij}\,
\partial_{y_i}\partial_{y_j}\delta_G
\right]
+O_{\mathcal D'}(\epsilon).
\tag{57.11}
$$

Every term is local on the full collision diagonal. The scalar coefficient is the exact nonzero algebraic number

$$
\boxed{
\mathfrak a_G=
\frac14+\frac{\sqrt2}{2}+\frac{\sqrt3}{3}
+\frac{\sqrt{10}}5+\frac{\sqrt{30}}{30}
-\frac{\sqrt{14}}7-\frac{\sqrt{22}}{11}.
}
\tag{57.12}
$$

The second-derivative matrix in (57.9) is also nonzero. For example, its first diagonal entry is

$$
(\mathfrak B_G)_{00}
=-\frac{5\sqrt6}{96}
+\frac{\sqrt2}{24}
+\frac{7\sqrt{30}}{600}\ne0.
\tag{57.13}
$$

Therefore two explicit **overall local counterterms**, obtained from exactly the same intrinsic proper-source data, produce a strong distributional finite limit:

$$
\overline R_{G,\epsilon}
-
(2\pi)^{-3/2}\left[
\frac{\mathfrak a_G}{\epsilon^3}\delta_G
+\frac1\epsilon\sum_{i,j}(\mathfrak B_G)_{ij}
\partial_{y_i}\partial_{y_j}\delta_G
\right]
\longrightarrow 0.
\tag{57.14}
$$

**Proof.** Each source $C_{\gamma,\epsilon}$ is a finite sum of distributions supported on its own collision diagonal, here consisting of exactly one scalar delta with an explicitly computed coefficient. Embedding a source into $G$ leaves a connected quotient Gaussian in the independent remaining positions. The same holds for the only disjoint forest $\{A,B\}$. A source with cycle rank $h_\gamma$ contributes an $\epsilon^{-h_\gamma}$ scalar; the quotient has cycle rank $3-h_\gamma$. Thus **every** forest term in (57.7) has overall order $\epsilon^{-3}$ and a relative normalized Gaussian. Expand each of these Gaussians through its covariance moment:

$$
(2\pi)^{-3/2}\epsilon^{-3}
\frac{\prod_{\gamma\in F}a_\gamma}
{\sqrt{\tau(G/F)}}
\left[\delta_G+
\frac{\epsilon^2}{2}
\sum_{i,j}(M_{G/F})_{ij}\partial_i\partial_j\delta_G
+O_{\mathcal D'}(\epsilon^4)\right].
\tag{57.15}
$$

(The product is empty for the bare graph.) The signs in (57.7) give (57.9). No odd Gaussian moments appear. The remainder after retaining order $\epsilon^{-1}$ is therefore $O(\epsilon)$ strongly on bounded compact test families. The recursive source coefficients (57.6) give (57.12) by exact radical arithmetic and (57.13) by rational quotient-covariance embedding; all graph contractions and radical expressions are reproduced by [fixture 057](fixtures/check_full_double_bridge_forest_057.py). Subtract the two negative orders to obtain (57.14). No undefined product of overlapping singular collision deltas is formed. $\square$

**A demanding hostile control:** Formula (57.9) must contain the $A,B$ disjoint forest term with a **plus** sign. Omitting it recovers neither the 24-forest enumeration nor the exact scalar coefficient. Conversely, adding the 12 nested forests *again* after using the prepared two-loop source constants in (57.6) double-counts them. The theorem's form includes disjoint contributions exactly once and nested contributions exactly once.

## 5. What was repaired and what remains

The older [R2/055](R2_DOUBLE_BRIDGE_INSERTION_DEFECT_055.md) proved the *naive* independent triangle preparation left two local poles. Here we have constructed the **complete proper 1PI forest** of the same graph, including all four new higher-loop crossing sources. The graph-local overall subtraction in (57.14) is therefore a **genuine finite forest recursion on this eight-edge graph**, with every proper-source coefficient computed independently of its containment in $G$.

It would nevertheless be inaccurate to call this an all-graph BPHZ character or prove global BV closure. The counterterms have been checked under the specific embeddings and Gaussian derivative-free graph class; this theorem does not establish universal compatibility under arbitrary further insertions, arbitrary graph edge weights, derivatives of delta on proper subgraphs, a mixed Wick graph domain closed under repeated BV compositions, or interacting QME.

**Next mathematical gate:** extend the same inductive proper-source counterterm assignment to a finite graph family closed under (i) disjoint union, (ii) one new cyclic edge insertion, and (iii) a nontrivial overlapping 1PI subgraph family not isomorphic to the current double-bridge case; then verify that the resulting renormalization map intertwines factor-local Wick-to-delta conversion with a globally defined second-order BV differential, or exhibit a nonzero anomaly. REACH-R2 #2797 remains OPEN.