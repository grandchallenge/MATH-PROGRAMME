# EXT-015 REACH-R2 / 051 — a nested-overlap proper-subgraph renormalization of the Gaussian complete graph K4

**Disposition: NEW BOUNDED MATHEMATICAL CANDIDATE, separate critical audit required.** This advances beyond the two-supergraph result [049](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md). It extends the **same intrinsic** triangle, square and prepared theta counterterms into the six-edge complete graph on four vertices, enumerates all 13 proper one-particle-irreducible (1PI) cyclic subgraphs and all 18 nested proper forest pairs, and derives **both** the full-diagonal scalar pole and the first nontrivial derivative-delta overall pole. The prepared graph converges after subtracting these two local terms. No redefinition of a proper subgraph counterterm is needed to fit its new supergraph.

**Not claimed:** universal BPHZ renormalization on every graph, compatibility with arbitrary mixed Wick/delta-jet subgraph gluing, a globally defined BV operator or QME, completed Costello–Gwilliam B.6, or liquid higher Ext.

**Protected source dependencies:** reviewed [R2/042–043](R2_OVERLAPPING_CYCLES_DELTA_JETS_042.md), [R2/044–045](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md), [R2/046](R2_BRIDGE_TREE_LAURENT_BV_046.md), [R2/047–048](R2_GAUSSIAN_CYCLE_INSERTION_047.md), and [R2/049–050](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md). Initial source main \`e5c85975427781e078b2b6159c38d11288598b6c\`. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. Proper forest inventory: 13 source-local objects and 18 nested pairs

Let $G=K_4$ have the six unit Gaussian delta edges of the complete graph on vertices $1,2,3,4$. Each edge carries $\kappa_\epsilon(x_i-x_j)$ with the even normalized Gaussian

$$
\kappa(z)=\frac{e^{-z^2/2}}{\sqrt{2\pi}},
\qquad
\kappa_\epsilon(z)=\frac1\epsilon\kappa(z/\epsilon).
\tag{51.1}
$$

**Lemma 51.1 (complete proper 1PI inventory).** The proper connected bridgeless cyclic edge subgraphs of $K_4$ consist of exactly

- four labeled triangles with three edges;
- three labeled simple squares with four edges;
- six labeled five-edge theta graphs ($K_4$ with one edge omitted).

There are no others. Every pair of proper 1PI cycles overlaps in vertices and at least one edge; hence no two distinct proper 1PI subgraphs are disjoint. Nested pairs occur only when a triangle or square lies inside a five-edge theta. Each triangle is contained in exactly three theta graphs, and each square in exactly two. Thus there are precisely $4\cdot3+3\cdot2=18$ nested two-subgraph forests. Including 13 singleton forests and the empty forest, the complete set has **32 proper forests**.

**Proof.** Connected bridgeless cyclic edge subgraphs require at least three edges. Three edges yield exactly a triangle; four edges yield exactly a four-cycle because a triangle with a fourth pendant edge has a bridge; five edges yield exactly $K_4$ minus one edge, which is bridgeless and isomorphic to theta. All six edges give the full graph and are not proper. For each omitted edge of a theta, a triangle is included exactly when the omitted edge is one of the three edges not in the triangle (three choices). A square is included when the omitted edge is one of its two complementary diagonals (two choices). Two distinct triangles in $K_4$ share an edge; each square contains four edges, and each theta contains five. Thus every pair overlaps, and the only strict containments are the counted triangle/square-in-theta pairs. $\square$

The only admissible direct proper-subgraph insertions in a preparation step are therefore **single** connected 1PI subgraphs. Nested forest contributions are already represented in the *prepared theta counterterm* inherited from [049](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md); multiplying overlapping delta counterterms or treating a theta as a primitive one-loop source would be incorrect.

## 2. An unchanged source counterterm library

The Gaussian moments, independent of the containing graph, are

$$
\begin{aligned}
c_3&=\frac1{\sqrt{6\pi}},&
c_4&=\frac1{\sqrt{8\pi}},&
\kappa(0)&=\frac1{\sqrt{2\pi}},\\
b_3&=\int_{\mathbb R}\kappa(t)^3\,dt
=\frac1{2\pi\sqrt3},&
b_{3,2}&=\int_{\mathbb R}t^2\kappa(t)^3\,dt
=\frac1{6\pi\sqrt3}.
\end{aligned}
\tag{51.2}
$$

For a proper triangle $\gamma$, subtract the intrinsic kernel $(c_3/\epsilon)\delta_\gamma$, multiplied only by the smooth regulated edges of $K_4$ not in $\gamma$. For a proper square, use $(c_4/\epsilon)\delta_\gamma$ identically. For a proper theta graph, use the *prepared* source-local overall counterterm already calculated in 049:

$$
\mathsf S_{\Theta,\epsilon}
=\frac{g_\Theta}{\epsilon^2}\delta_\Theta,
\qquad
g_\Theta=
\frac1\pi\left(
\frac1{4\sqrt2}
-\frac1{\sqrt6}
-\frac14
\right).
\tag{51.3}
$$

**Source-local sign convention:** $\mathsf S$ is the distribution **subtracted** from the amplitude. The theta coefficient $g_\Theta$ is negative; subtracting it **adds** its absolute value. This is allowed and is not a regulator positivity claim. Its coefficient is **not recalibrated in K4**. It was computed by preparing a five-edge theta graph against its three proper cycle counterterms; those three nested contributions are already included in $g_\Theta$. Thus the six theta embeddings represent the 18 nested forest pairs of Lemma 51.1 without attempting ill-defined simultaneous delta products.

## 3. Precise K4 Gaussian scaling

Take vertex 4 as root, and relative coordinates

$$
y_1=x_1-x_4,\qquad
y_2=x_2-x_4,\qquad
y_3=x_3-x_4.
\tag{51.4}
$$

Let $\delta_G=\delta(y_1)\delta(y_2)\delta(y_3)$. The exact precision and inverse covariance are

$$
Q_G=
\begin{pmatrix}3&-1&-1\\-1&3&-1\\-1&-1&3\end{pmatrix},
\qquad
Q_G^{-1}
=\frac14\begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix},
\quad
\det Q_G=16.
\tag{51.5}
$$

Set $\mathcal L_G=\sum_{i,j=1}^3(Q_G^{-1})_{ij}\partial_{y_i}\partial_{y_j}$. As the graph has six edges and three independent relative coordinates, its cycle rank is $h=3$, and its raw exact Gaussian normalization is

$$
T_{G,\epsilon}
=c_G\epsilon^{-3}\rho_{\epsilon,Q_G},
\qquad c_G=\frac1{8\sqrt2\,\pi^{3/2}}.
\tag{51.6}
$$

Its first two singular Laurent coefficients are

$$
T_{G,\epsilon}
=
\frac{c_G}{\epsilon^3}\delta_G+
\frac{c_G}{2\epsilon}\mathcal L_G\delta_G
+O_{\mathcal D'}(\epsilon).
\tag{51.7}
$$

## 4. Intrinsic proper-subgraph insertions in K4

Collapsing any triangle $\gamma$ identifies its three vertices. The three remaining edges all connect the common collapsed triangle vertex to the fourth, omitted vertex. Let $t_\gamma$ denote that one remaining quotient-edge coordinate. The intrinsic subgraph insertion becomes

$$
\mathsf I_{\gamma,\epsilon}
=\frac{c_3}{\epsilon}\delta_\gamma
\kappa_\epsilon(t_\gamma)^3.
\tag{51.8}
$$

Because the two source moments $b_3,b_{3,2}$ are finite and odd moments vanish,

$$
\mathsf I_{\gamma,\epsilon}
=
\frac{c_3b_3}{\epsilon^3}\delta_G+
\frac{c_3b_{3,2}}{2\epsilon}
\partial_{t_\gamma}^2\delta_G
+O_{\mathcal D'}(\epsilon).
\tag{51.9}
$$

Here $\partial_{t_\gamma}$ is the normal derivative in the **quotient coordinate** of the collapsed triangle, holding its two internal differences fixed. It is not an arbitrary global vertex derivative.

Each four-edge square collapses **all four vertices** and leaves its two missing diagonal chords. Hence its source-local insertion is **exactly**

$$
\mathsf I_{\square,\epsilon}
=\frac{c_4\kappa(0)^2}{\epsilon^3}\delta_G,
\tag{51.10}
$$

with no derivative coefficient. Each five-edge theta also collapses all four vertices, and the remaining missing chord evaluates at zero:

$$
\mathsf I_{\Theta,\epsilon}
=\frac{g_\Theta\kappa(0)}{\epsilon^3}\delta_G.
\tag{51.11}
$$

The coefficients $c_3,c_4,g_\Theta$ do not depend on the containing complete graph. The *smooth complement factors* are the only data that depend on the embedding.

**Lemma 51.2 (sum of the four triangle quotient normal derivatives).** In the coordinates (51.4),

$$
\sum_{\gamma\ \mathrm{triangle}}
\partial_{t_\gamma}^2
=
\left(\partial_{y_1}+\partial_{y_2}+\partial_{y_3}\right)^2
+\sum_{i=1}^3\partial_{y_i}^2
=4\mathcal L_G.
\tag{51.12}
$$

**Proof.** For the triangle consisting of vertices $1,2,3$, the omitted vertex is the root 4, so moving the common collapsed-triangle coordinate changes all $y_i$ together and gives the first derivative direction. For each of the three triangles including vertex 4, the omitted vertex is one of $1,2,3$, giving a derivative along its individual $y_i$. Expand the square and compare with the explicit inverse matrix (51.5). $\square$

## 5. A complete three-loop prepared-overlap subtraction

Form the proper-subgraph preparation

$$
\overline R_{G,\epsilon}
=
T_{G,\epsilon}
-\sum_{\gamma\in \mathrm{Tri}(G)}\mathsf I_{\gamma,\epsilon}
-\sum_{\gamma\in \mathrm{Sq}(G)}\mathsf I_{\gamma,\epsilon}
-\sum_{\gamma\in \mathrm{Theta}(G)}\mathsf I_{\gamma,\epsilon}.
\tag{51.13}
$$

There are respectively 4, 3 and 6 terms. No product of two overlapping singular subgraph counterterms occurs.

Define two local overall coefficients:

$$
\begin{aligned}
a_{-3}
&=c_G-4c_3b_3-3c_4\kappa(0)^2-6g_\Theta\kappa(0)\\
&=\frac1{\pi^{3/2}}\left(
\sqrt3-\frac34+\frac5{24\sqrt2}
\right),\\[2mm]
a_{-1}
&=\frac{c_G}{2}-2c_3b_{3,2}
=-\frac7{144\sqrt2\,\pi^{3/2}}.
\end{aligned}
\tag{51.14}
$$

**Theorem 51.3 (K4 local forest recursion and complete negative-power cancellation).** With the exact, unchanged proper-subgraph counterterms of (51.3), the *prepared* amplitude obeys

$$
\overline R_{G,\epsilon}
=
\frac{a_{-3}}{\epsilon^3}\delta_G
+\frac{a_{-1}}{\epsilon}\mathcal L_G\delta_G
+O_{\mathcal D'}(\epsilon).
\tag{51.15}
$$

Consequently the overall-renormalized family

$$
R_{G,\epsilon}
=
\overline R_{G,\epsilon}
-\frac{a_{-3}}{\epsilon^3}\delta_G
-\frac{a_{-1}}{\epsilon}\mathcal L_G\delta_G
\longrightarrow0
\quad\text{strongly in distributions}.
\tag{51.16}
$$

The $O(\epsilon)$ convergence holds uniformly on bounded compact test-function families of sufficiently many derivatives.

**Proof.** Expand the exact bare Gaussian as in (51.7). Use the 4 triangle expansions (51.9), the 3 square equalities (51.10), and the 6 theta equalities (51.11). The resulting $\epsilon^{-3}$ coefficient is exactly the first line of (51.14). The only $\epsilon^{-1}$ sources are the bare Gaussian and the four triangle second moments. Lemma 51.2 converts the latter to $2c_3b_{3,2}\mathcal L_G\delta_G$, yielding the second line of (51.14). Gaussian symmetry rules out even Laurent exponents for this odd-cycle-rank graph; the next permitted order after $\epsilon^{-1}$ is $\epsilon^{+1}$. Gaussian moment bounds prove the remainder estimate. Both overall counterterms are supported on the full collision diagonal, and every proper-subgraph insertion multiplies its delta only by positive-regulator smooth kernels. Thus no Hörmander-forbidden product of overlapping deltas is formed. $\square$

**Nontrivial point:** The overall graph requires a **derivative-of-delta counterterm at order $\epsilon^{-1}$** in addition to the scalar $\epsilon^{-3}$ term. Subtracting only the leading scalar pole is insufficient. The coefficient $a_{-1}$ is nonzero, negative and determined exactly by the *same* intrinsic triangle source coefficient used earlier. This is a genuine new higher-overlap check of source-locality.

## 6. Exact adversarial controls and acceptance boundary

On a test function equal to one near the full diagonal with normalized root cutoff, the prepared amplitude has leading coefficient $a_{-3}/\epsilon^3$, and the derivative counterterm vanishes on that test. On a test equal to $y_1^2$ near the diagonal, the prepared amplitude has leading coefficient $(a_{-1}/\epsilon)\,\mathcal L_G y_1^2=(-7/(144\sqrt2\pi^{3/2}))\epsilon^{-1}$, because $\mathcal L_G y_1^2=1$. Both are exact, separately testable poles. After both subtractions they tend to zero.

The standard-library exact fixture [051](fixtures/check_k4_nested_forest_051.py) verifies all 13 proper 1PI subgraphs, the 18 nested forest pairs and 32 total forests; both determinant and covariance identities; Gaussian shape moments; the fixed theta-source coefficient; the scalar and derivative-delta overall coefficients; and a parameterized symbolic cancellation test on two independent compact quadratic probes. It does not substitute for the analytic distributional proof.

**Achieved:** a source-independent **nested-overlap 1PI subgraph recursion** on K4 using previously fixed proper cycle counterterms from lower-complexity graphs, and a complete strong-distribution finite result after two explicit local overall subtractions. This is strictly stronger than the theta/parallel two-supergraph examples of 049.

**Open:** extending this recursion to arbitrary graphs with disjoint divergent components and arbitrary overlapping/nested 1PI subgraphs; arbitrary differentiated delta kernels; edge-factor-to-global BV coderivation, square-zero identity and interacting QME; proper smooth normal-topology enriched factorization and B.6; original higher liquid Ext comparison.

**Next exact theorem:** prove a finite-graph recursive counterterm *functor* on a nontrivial graph class closed under all edge insertions and disjoint union, or find an exact obstruction when nested subgraph counterterms are inserted into graphs with shared vertices but no simple quotient-tree structure. REACH-R2 [#2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains OPEN; separate mathematical critical audit required before protected admission.