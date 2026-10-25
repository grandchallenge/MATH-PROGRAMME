# EXT-015 REACH-R2 / 053 — a multi-branch local forest theorem for Gaussian cyclic blocks joined by bridges

**Disposition:** bounded new mathematical candidate; source-locked hostile review required. This proves a *counterterm-level* factorization theorem for finite **trees of individually renormalized cyclic graph blocks**. Within each block, proper divergent 1PI cycles may overlap and nest as in [049](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md) and [051](R2_K4_NESTED_OVERLAP_FOREST_051.md). Between blocks, the entire forest poset is a Cartesian product, so disjoint counterterms compose without multiplying incompatible diagonal distributions. The result gives a nonzero two-theta finite distribution, an exact 64-forest count, a 4,096-forest two-K4 stress case, and a free Wick-to-delta bridge identity **after the actual local forest subtractions**.

**It does not prove** a universal forest recursion for graphs whose block quotient itself has cycles, global BV nilpotence or a QME, the normal-topology smooth Weiss comparison, or the original liquid degree-two Ext comparison.

**Protected source:** R2/042–052, particularly [049](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md), [K4/051](R2_K4_NESTED_OVERLAP_FOREST_051.md) and [K4 review/052](AGENT_CRITICAL_REVIEW_K4_FOREST_052.md). Initial protected main head: \`4cbb57b07eec56f094a06cd65965fcd238825e53\`. Parent issue [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. A class closed under adding new bridge branches

Let $T$ be any finite **tree** on $q$ block vertices. Label each block $i$ by a fixed connected Gaussian delta graph $G_i$ whose *source-local, already prepared* renormalization is mathematically admitted in the present programme: a triangle, a parallel-edge triangle, a five-edge theta, or K4 (including graph isomorphisms, fixed positive Gaussian weight choices where separately proved, and the original unit-weight schemes). Each edge of $T$ specifies one bridge connecting one vertex in a block to one vertex in another, with a chosen unit Gaussian **delta** or **Wick** propagator. The quotient of the composite graph $\widehat G$ by collapsing each block is precisely $T$; each bridge is a genuine graph-theoretic bridge.

For each block $G_i$ write

$$
A_{i,\epsilon}=\prod_{e\in E(G_i)}\kappa_\epsilon(x_{e^-}-x_{e^+}),\qquad
R_{i,\epsilon}=A_{i,\epsilon}-\sum_{\gamma\subsetneq G_i}^{\rm forest}\mathsf I_{\gamma,\epsilon}-\mathsf C_{i,\epsilon},
\tag{53.1}
$$

where the finite forest preparation and prepared overall counterterm are **exactly** those established in the corresponding earlier source papers. The sum is *shorthand for the actual finite source-local preparation*, with nested counterterms packaged into the already prepared parent counterterms; it is not the product of overlapping delta distributions. In particular, for a theta source,

$$
R_{\Theta,\epsilon}
=A_{\Theta,\epsilon}
-S_{A,\epsilon}-S_{B,\epsilon}-S_{C,\epsilon}
-\frac{g_\Theta}{\epsilon^2}\delta_\Theta,
\quad
R_{\Theta,\epsilon}\longrightarrow L_\Theta
\tag{53.2}
$$

strongly in distributions, with $g_\Theta$ and $L_\Theta$ fixed in R2/049. For K4 the analogous source $R_{K4,\epsilon}$ subtracts every proper nested/overlap preparation plus both the full-diagonal scalar and second-derivative overall terms of R2/051; it tends to zero, with an $O(\epsilon)$ test-seminorm remainder. For the triangle source, $R_{\triangle,\epsilon}=A_{\triangle,\epsilon}-(c_3/\epsilon)\delta_\triangle$ tends to zero.

Choose one internal root in each block and let $y_i$ be its independent internal relative coordinates. For each bridge $b$ use the *actual* endpoint separation $t_b$ as an independent external coordinate, and retain one free global root coordinate $s$. A tree of block roots plus internal differences is an integer unimodular linear coordinate transformation; its absolute Jacobian is one. Therefore the internal $y_i$ and the bridge differences $t_b$ are independent coordinates, regardless of which endpoints are used for the bridges.

For each bridge put

$$
B_{b,\epsilon}(t)=
\begin{cases}
\kappa_\epsilon(t),&\text{delta bridge},\\
P_\epsilon(t)=(|\cdot|/2)*\kappa_\epsilon(t),&\text{Wick bridge},
\end{cases}
\qquad
B_{b,\epsilon}\longrightarrow B_{b,0}
\in\{\delta_0,P_0\}
\tag{53.3}
$$

strongly in distributions. The limits also hold after each finite derivative in $t$.

## 2. Forest combinatorics beyond one nested branch

Write $\mathfrak F(G)$ for the collections of proper divergent **1PI** edge-subgraphs that are pairwise disjoint or nested, using the same subgraph definition and prepared-counterterm conventions as R2/049 and 051. If the connected graph $\widehat G$ has genuine bridge edges between its blocks, then **no connected 1PI subgraph may contain a bridge**: deleting that edge disconnects such a subgraph. Every proper 1PI subgraph of $\widehat G$ consequently lies completely inside a unique $G_i$, and this includes the *whole* block $G_i$, which is now proper in $\widehat G$.

**Lemma 53.1 (Cartesian forest decomposition).** The complete forest poset of the bridge-assembled graph satisfies the canonical isomorphism

$$
\mathfrak F(\widehat G)\cong
\prod_{i=1}^q \mathfrak F_{\le G_i}(G_i),
\tag{53.4}
$$

where the factor on the right allows the full block as a forest element, together with any nested proper forest below it. There are no additional 1PI subgraph terms spanning a bridge, and no additional compatibility constraints between different blocks.

**Proof.** A connected 1PI graph is bridgeless by definition. Every edge of the block quotient is a bridge of the assembled graph; if a connected subgraph contains such an edge, deleting it disconnects that subgraph. Thus the 1PI subgraphs are exactly those entirely inside individual blocks. Within one block their forest compatibility is exactly the original nesting/disjointness relation. Between different blocks the edge and vertex sets are disjoint; every pair is compatible. Partitioning a forest by block gives the proposed bijection, whose inverse is disjoint union. Inclusion and nesting order are preserved. $\square$

**Nontrivial counts.** A theta block has three mutually overlapping proper cycles, so it has four proper forest choices (empty or one cycle). Allowing its full theta as a new proper supergraph counterterm doubles the possibilities, yielding

$$
|\mathfrak F_{\le\Theta}(\Theta)|=2(1+3)=8.
\tag{53.5}
$$

Two theta blocks joined by a bridge thus have exactly **64 forests**, including nested forests within either block and forests selecting a divergent subgraph in *both* blocks. For K4, R2/051 proves 32 proper forest choices; adding the full K4 doubles this to 64. Two copies of K4 joined by one bridge therefore have exactly **4,096 forests**. These are not guesses based on the cyclomatic number; they are the direct products of the independently verified nested/overlap inventories.

The source counterterms for an entire theta or K4 block are **prepared** overall coefficients. Each such coefficient already incorporates its nested child-forest terms; do not multiply the parent's singular delta by a child's delta. For two theta blocks, the 64 abstract forest choices are compressed in the **25 well-defined terms** obtained by multiplying the five source-level terms of (53.2) for each block; unpacking the already prepared parent counterterm into its recursive forest origin recovers the remaining nested labels. The 25 products are across independent block coordinates only.

## 3. A distributionally convergent local forest recursion

For every such bridge tree, define its explicitly source-local *forest-renormalized regulated amplitude* by

$$
\mathcal R_{T,\epsilon}
=
\left(\mathop{\boxtimes}_{i=1}^q R_{i,\epsilon}(y_i)\right)
\boxtimes
\left(\mathop{\boxtimes}_{b\in E(T)}
B_{b,\epsilon}(t_b)\right),
\tag{53.6}
$$

transported through the unimodular coordinate change to the original vertex variables. This is not merely a prescription for the **final whole-graph** constant term: every source-local proper-cycle and prepared parent counterterm is inserted in its original block, and the Cartesian expansion implements each admissible disjoint forest contribution. Every product of singular distributions occurs only across independent coordinates. The complementary bridge edges remain *smooth at positive regulator*.

**Theorem 53.2 (branching local forest theorem).** For any finite fixed tree of the admitted block sources and any choice of delta/Wick bridges, (53.6) is an unambiguously defined distribution for every $\epsilon>0$, and

$$
\mathcal R_{T,\epsilon}
\longrightarrow
\mathcal L_T:=
\left(\mathop{\boxtimes}_{i=1}^q L_i\right)
\boxtimes
\left(\mathop{\boxtimes}_{b\in E(T)}B_{b,0}\right)
\tag{53.7}
$$

in the strong distribution topology, where $L_i=\lim R_{i,\epsilon}$ is the *previously proved* forest-renormalized block distribution. The limit and preparation are independent of the order in which bridge branches and disjoint counterterms are assembled, up to canonical coordinate and tensor permutations. Counterterms for any fixed source subgraph are **identical** in every containing bridge-tree supergraph; their embeddings differ only by multiplication with the remaining regulated independent-variable edge factors.

**Proof.** In the unimodular variables, source preparation is performed solely in $y_i$ for each block. All source R2/049/051 estimates give strong convergence of the finitely many $R_{i,\epsilon}$ and hence boundedness of their families in the strong dual on compact parameter intervals. Gaussian approximate identities satisfy $\kappa_\epsilon\to\delta_0$ strongly, while Gaussian convolution gives $P_\epsilon\to P_0$ strongly; the families of bridge derivatives similarly converge and are bounded. The exterior tensor product of distributions in independent variables is jointly sequentially continuous along these bounded convergent families (equivalently, expand against bounded compact test families with uniform seminorm bounds, using the finite nuclear tensor-product structure of smooth compact tests). This yields (53.7). Associativity and symmetry of the exterior tensor product, together with the tree's unimodular coordinate charts and Lemma 53.1, give independence of assembly order. Every source-local term is the same distribution in its $y_i$ variables regardless of the number or placement of bridges. $\square$

**Scope:** This theorem proves *source-independent forest compatibility under arbitrary branching bridge extensions*. It is stronger than R2/049's single cyclic core plus attached tree (which contained no second independently divergent cyclic block), but still does not cover a new edge connecting two already-connected blocks and thereby creating an additional cycle.

## 4. A nonzero two-theta witness; no premature finite-part projection

Fix two identical unit-weight five-edge theta blocks, connected by one unit delta bridge. In the tree coordinates $(u_i,v_i,w_i)$ of each theta block, let $\phi$ be a compact test that agrees near all collision diagonals with $u_1^2u_2^2$ times a normalized global-root cutoff, and is identically one in the bridge separation near $t=0$.

From R2/049 the *already forest-renormalized* theta finite distribution satisfies

$$
\langle L_\Theta,u^2\rangle
=A:=\frac1\pi
\left(\frac5{32\sqrt2}-\frac1{4\sqrt6}\right)\ne0.
\tag{53.8}
$$

**Corollary 53.3 (strictly nonzero 64-forest amplitude).** The complete bridge-renormalized two-theta graph has the exact nonzero finite test pairing

$$
\left\langle\mathcal L_{T},\phi\right\rangle
=A^2
=\frac{139-80\sqrt3}{6144\pi^2}
>0.
\tag{53.9}
$$

Its 64-forest counterterm preparation is not equivalent to dropping all Laurent poles *before* gluing: both theta blocks have nonzero prepared finite parts, but the source-local terms accounting for their proper overlapping cycles and parent counterterms must still be inserted to obtain them. The disjoint forest terms required by Lemma 53.1 are indispensable to the factorized source preparation.

**Proof.** By Theorem 53.2, the limiting distribution is $L_\Theta(y_1)\boxtimes L_\Theta(y_2)\boxtimes\delta(t)$, times the unrestricted root variable. The test factors, and the bridge delta evaluates its cutoff to one. Therefore the pairing is the square of (53.8). Squaring the two algebraic surds gives exactly (53.9). The strict inequality follows from $139^2>3\cdot80^2$, i.e. $19321>19200$. $\square$

For two K4 blocks the same 4,096-forest recursion is well-defined but its selected source scheme has $L_{K4}=0$, so the particular fully subtracted limit is zero. Its nontrivial contribution is the large nested/disjoint **forest consistency**, not an invented positive finite value.

## 5. BV bridge conversion *after* the proper forest subtractions

**Corollary 53.4 (free edge identity on forest-renormalized blocks).** If $b$ is any Wick bridge, then the derivative in its *independent bridge difference coordinate* satisfies

$$
\partial_{t_b}^2\mathcal R_{T,\epsilon}^{P_b}
=\mathcal R_{T,\epsilon}^{K_b},
\qquad
\partial_{t_b}^2\mathcal L_T^{P_b}
=\mathcal L_T^{K_b}.
\tag{53.10}
$$

This remains true when each endpoint block has overlapping and nested divergent 1PI subgraphs, including the two theta blocks above. It holds after finite bridge derivatives and any sequence of conversions on distinct bridge edges.

**Proof.** The source-local forest counterterms $R_{i,\epsilon}$ involve only internal $y_i$ and never bridge variables $t_b$. Consequently $\partial_{t_b}^2$ hits only $P_\epsilon(t_b)$, and $P_\epsilon''=\kappa_\epsilon$ exactly. Derivatives commute with the strong distributional limit, proving the second identity. Distinct bridge derivatives commute. $\square$

This is a bounded **free** BV edge relation on a domain closed under tree-bridge assembly and source-local subtraction; it is not the second-order BV operator identity on *all* cycle-creating insertions or interacting graphs.

## 6. Exact regression and next theorem

The exact standard-library fixture [053](fixtures/check_branching_forests_053.py) checks the 64 and 4,096 forest counts by enumeration/cartesian recursion; verifies the compressed five-term theta preparation and its 25 independent-variable products; verifies $A^2=(139-80\sqrt3)/(6144\pi^2)$ without floating point; and checks the formal Wick bridge derivative identity plus the two-K4 zero finite-part control.

**Achieved:** a *multi-branch* source-local forest recursion with simultaneous disjoint, nested and overlapping divergent subgraphs, genuine nonzero Gaussian finite-part witness, and a free Wick/BV bridge identity after renormalization.

**Unsolved:** the same forest recursion after inserting a **cycle-creating edge between bridge-separated blocks**, where formerly independent block variables are constrained by a new edge. This is the next decisive graph: two theta blocks joined by a bridge and then by a second cross edge. The graph has an additional global cycle, and its new proper 1PI subgraphs can span the old block boundary. Test whether the existing prepared block counterterms remain source-independent inside that supergraph or whether an exact insertion anomaly appears. A full BV second-order coderivation, QME, normal-topology Weiss, and liquid Ext remain open.