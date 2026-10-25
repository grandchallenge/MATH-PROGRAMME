# EXT-015 REACH-R2 / 055 — exact cycle-creating gluing defect for two independently renormalized triangles

**Disposition: NEW BOUNDED MATHEMATICAL CANDIDATE; separate critical audit required.** The bridge-tree theorem [053](R2_BRANCHING_FOREST_FACTORISATION_053.md) is valid for independent bridge variables. This note computes the **first failure** when a second edge joins two formerly bridge-connected cyclic blocks. It produces an exact strictly positive $\epsilon^{-3}$ divergence and a second $\epsilon^{-1}$ local derivative-delta divergence after applying **all old block counterterms**. Both may be subtracted by explicit full-diagonal local counterterms, but this is not yet a universal source-independent forest recursion for the newly created cross-block 1PI subgraphs.

**Grounded sources:** protected Gaussian graph theorems [044](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md), [046](R2_BRIDGE_TREE_LAURENT_BV_046.md), [047](R2_GAUSSIAN_CYCLE_INSERTION_047.md), overlapping forest [049](R2_TWO_SUPERGRAPH_LOCAL_FOREST_049.md), K4 [051](R2_K4_NESTED_OVERLAP_FOREST_051.md), and source-admitted bridge-tree [053](R2_BRANCHING_FOREST_FACTORISATION_053.md). The separate review of 053 was not protected-admitted when this candidate began; no audit admission is inferred from a source merge. Initial protected main \`3ed45cb2bb550dd1bc58ebd8563890fefa0c21a6\`. Research issue [#2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. An exact minimal two-block graph

Take six labeled vertices $0,1,2,3,4,5$. The original two unit-Gaussian triangles are

$$
A=\{01,12,02\},\qquad B=\{34,45,35\}.
\tag{55.1}
$$

Join them by **two** distinct unit Gaussian delta edges $03$ and $14$. The first edge alone is a graph-theoretic bridge; adding the second creates a new cross-block cycle. The full eight-edge connected graph $G$ has $n=6$, $m=8$, and cycle rank $h=8-(6-1)=3$. The original $A$ and $B$ are no longer independent renormalization components.

Let $\kappa_\epsilon(t)=\epsilon^{-1}(2\pi)^{-1/2}e^{-t^2/(2\epsilon^2)}$, let $T_{A,\epsilon}$ and $T_{B,\epsilon}$ be their three-edge Gaussian products, and put

$$
c_3=(2\pi)^{-1/2}3^{-1/2}
=\frac1{\sqrt{6\pi}}.
\tag{55.2}
$$

The previously *proven and source-local* triangle preparations are

$$
R_{A,\epsilon}=T_{A,\epsilon}-\frac{c_3}{\epsilon}\delta_A,\qquad
R_{B,\epsilon}=T_{B,\epsilon}-\frac{c_3}{\epsilon}\delta_B.
\tag{55.3}
$$

Each prepared triangle tends strongly to zero in distributions. If the second cross edge had not been added, multiplying (55.3) and one independent bridge Gaussian would still converge by R2/053. The naive extension to two cross edges is the perfectly well-defined **positive-regulator** distribution

$$
F_\epsilon=
R_{A,\epsilon}R_{B,\epsilon}
\,\kappa_\epsilon(x_0-x_3)
\,\kappa_\epsilon(x_1-x_4).
\tag{55.4}
$$

The products involving the singular $\delta_A,\delta_B$ are legitimate at fixed $\epsilon$: they are supported on independent triangle collision coordinates and multiply only the **smooth positive-scale cross-edge factors**.

## 2. The exact four Gaussian covariance states

Choose root $x_3$ and absolute-Jacobian-one relative coordinates

$$
y=(x_0-x_3,x_1-x_3,x_2-x_3,x_4-x_3,x_5-x_3)
\in\mathbb R^5,\qquad
\delta_G=\prod_{j=1}^5\delta(y_j).
\tag{55.5}
$$

Write $L_M=\sum_{i,j=1}^5 M_{ij}\partial_{y_i}\partial_{y_j}$ for any symmetric positive semidefinite covariance matrix $M$. There are **four** distinct Gaussian normalization states in the expansion of (55.4):

1. Bare full graph, with reduced precision $Q_G$ and covariance $M_G=Q_G^{-1}$, weighted spanning-tree sum $\tau(G)=30$, and cycle rank three.
2. Triangle $A$ collapsed, with one factor $(c_3/\epsilon)\delta_A$ times the remaining five-edge quotient graph $G/A$; its quotient spanning-tree sum is $\tau(G/A)=8$, cycle rank two. Let $Q_A$ be its reduced precision, and $M_A$ its covariance embedded back into the original $y$ coordinates.
3. Triangle $B$ collapsed; the symmetric quotient has $\tau(G/B)=8$, cycle rank two, with embedded covariance $M_B$.
4. Both triangles collapsed; the two cross edges become a parallel-edge bubble with spanning-tree sum $\tau(G/(A,B))=2$, cycle rank one, and embedded covariance $M_{AB}$.

The explicit reduced matrices, all over $\mathbb Q$, are

$$
Q_G=
\begin{pmatrix}
3&-1&-1&0&0\\
-1&3&-1&-1&0\\
-1&-1&2&0&0\\
0&-1&0&3&-1\\
0&0&0&-1&2
\end{pmatrix},
\quad
Q_A=
\begin{pmatrix}2&-1&0\\-1&3&-1\\0&-1&2\end{pmatrix},
\quad
Q_B=
\begin{pmatrix}3&-1&-1\\-1&3&-1\\-1&-1&2\end{pmatrix}.
\tag{55.6}
$$

For $Q_A$ use quotient coordinates $z_A=(a,x_4-x_3,x_5-x_3)$ with $x_0=x_1=x_2=a+x_3$, embedded by

$$
J_A=
\begin{pmatrix}1&0&0\\1&0&0\\1&0&0\\0&1&0\\0&0&1\end{pmatrix}.
\tag{55.7}
$$

For $Q_B$ the quotient positions are $z_B=(x_0-x_3,x_1-x_3,x_2-x_3)$, with $x_3=x_4=x_5$, embedded by $J_B=(I_3;0_{2\times3})$. The bubble variable has covariance $1/2$ and is embedded along $v=(1,1,1,0,0)^{\mathsf T}$. Thus

$$
M_A=J_AQ_A^{-1}J_A^{\mathsf T},\qquad
M_B=J_BQ_B^{-1}J_B^{\mathsf T},\qquad
M_{AB}=\tfrac12vv^{\mathsf T}.
\tag{55.8}
$$

These definitions fix the quotient-relative delta normalizations without appealing to formal products of singular distributions.

## 3. A strictly positive insertion obstruction and its exact removal

Introduce the exact positive graph constants

$$
C_G=\frac{(2\pi)^{-3/2}}{\sqrt{30}},\quad
C_Q=\frac{(2\pi)^{-3/2}}{\sqrt{24}},\quad
C_{AB}=\frac{(2\pi)^{-3/2}}{3\sqrt2},
\qquad
D=C_G-2C_Q+C_{AB}.
\tag{55.9}
$$

Here $C_Q=c_3c_{G/A}=c_3c_{G/B}$, while $C_{AB}=c_3^2c_2$ uses the bubble constant $c_2=(2\pi)^{-1/2}/\sqrt2$. Define the local second-order differential operator

$$
\mathscr E=
\frac12\left(
C_GL_{M_G}
-C_Q L_{M_A}
-C_Q L_{M_B}
+C_{AB}L_{M_{AB}}
\right).
\tag{55.10}
$$

**Theorem 55.1 (failure and exact local repair of premature blockwise forest subtraction).** The fully old-source-prepared family (55.4) has the strong distributional Laurent expansion

$$
F_\epsilon
=
\frac D{\epsilon^3}\delta_G
+\frac1\epsilon\mathscr E\delta_G
+O_{\mathcal D'}(\epsilon),
\tag{55.11}
$$

with **strictly positive** scalar coefficient

$$
D=(2\pi)^{-3/2}
\left(
\frac1{\sqrt{30}}-\frac1{\sqrt6}+\frac1{3\sqrt2}
\right)>0.
\tag{55.12}
$$

Therefore **renormalizing the two triangle blocks and then inserting a cycle-creating second cross edge does not converge**. Subtracting the two explicit *new*, full-diagonal local terms gives the strong finite result

$$
F_\epsilon-
\frac D{\epsilon^3}\delta_G
-\frac1\epsilon\mathscr E\delta_G
\longrightarrow0.
\tag{55.13}
$$

The remainder is $O(\epsilon)$ uniformly on bounded compact test families with sufficiently many derivatives.

**Proof.** Expand the two parentheses in (55.4):

$$
F_\epsilon=
T_AT_B\kappa_\epsilon\kappa_\epsilon
-\frac{c_3}{\epsilon}\delta_AT_B\kappa_\epsilon\kappa_\epsilon
-\frac{c_3}{\epsilon}T_A\delta_B\kappa_\epsilon\kappa_\epsilon
+\frac{c_3^2}{\epsilon^2}\delta_A\delta_B
\kappa_\epsilon\kappa_\epsilon.
\tag{55.14}
$$

Every term is an exact Gaussian distribution on a quotient of the full vertex configuration. The first uses the full six-vertex graph with reduced precision $Q_G$ and cycle rank three. The next two use the respective four-vertex quotient graphs with cycle rank two, multiplied by a triangle counterterm of scale $\epsilon^{-1}$. The last uses the two-vertex parallel-edge quotient with cycle rank one multiplied by *two* triangle counterterms, giving again net scale $\epsilon^{-3}$. Consequently, after embedding each normalized Gaussian and its covariance back into the fixed $y$ coordinates, the four terms have expansions with scalar coefficients $C_G$, $-C_Q$, $-C_Q$, $+C_{AB}$ and second-derivative coefficients $C_GL_{M_G}/2$, $-C_QL_{M_A}/2$, $-C_QL_{M_B}/2$, $+C_{AB}L_{M_{AB}}/2$. This proves (55.11).

Evenness removes every odd centered moment, so after the $\epsilon^{-1}$ derivative coefficient the next term is $O(\epsilon)$, with strong bounds from the exact Gaussian moment estimates. To prove strict positivity of (55.12), multiply its dimensionless parenthesis by $\sqrt{30}$. The inequality becomes

$$
1+\frac{\sqrt{15}}3>\sqrt5.
\tag{55.15}
$$

Both sides are positive; squaring reduces it to $2\sqrt{15}>7$, which follows by squaring again since $60>49$. The scalar divergence therefore cannot cancel. Removing both displayed local coefficients proves (55.13). $\square$

**Additional quadratic hostile probe.** On a compact test agreeing with $y_1^2$ near the full collision diagonal, with normalized free-root cutoff, the remaining $\epsilon^{-1}$ coefficient after scalar subtraction is

$$
(2\pi)^{-3/2}
\left(
\frac7{10\sqrt{30}}-\frac5{4\sqrt{24}}
+\frac1{6\sqrt2}
\right),
\tag{55.16}
$$

which is nonzero (strictly negative). This verifies that the derivative counterterm in (55.13) is not an unnecessary formal decoration.

## 4. New cross-block proper 1PI sources

The eight-edge double-bridge graph has **ten proper bridgeless connected 1PI cyclic subgraphs**. Two are the original triangles, and **eight** cross both blocks. In particular there are four cross-block simple cycles: one of length four, two of length five, and one of length six, obtained by choosing either the direct or the two-edge alternate path between the cross-edge endpoints inside each triangle. The remaining four cross-block proper 1PI subgraphs contain more than one independent cycle.

For an isolated simple source cycle of length $m$, the Gaussian subgraph counterterm remains the **intrinsic** source-local

$$
\mathsf C_{m,\epsilon}=\frac1{\epsilon\sqrt{2\pi m}}\delta_{\mathrm{cycle}}
\qquad (m=4,5,6),
\tag{55.17}
$$

as in the earlier cycle library; it cannot be generated solely by selecting triangle counterterms inside $A$ and $B$. These new subgraph classes demonstrate combinatorially why the bridge-tree forest product no longer applies.

**Precise limitation:** Theorem 55.1 explicitly subtracts the *whole-graph* leftover poles of the **old-source-prepared** family. It does **not yet** show that inserting the complete new cross-block 1PI counterterm library (including overlapping higher-loop subgraphs) gives a supergraph-independent, nested-forest recursion. The new cross-cycle sources in (55.17) are identified but are *not* surreptitiously claimed to have been included in (55.14). Such a stronger recursion is the next mathematical obligation.

## 5. Free Wick-to-delta edge identity remains factor-local

If one of the two cross edges is replaced by the smoothed cusp propagator $P_\epsilon$ and the other remains a delta Gaussian, the original source preparations (55.3) are unchanged. For every positive $\epsilon$, differentiation **of that selected edge factor alone** gives $P_\epsilon''=\kappa_\epsilon$; multiplying by the other factors preserves the identity. Coefficientwise local Taylor renormalization therefore preserves this *edge-labelled* free relation. It is **not** a total derivative in the original vertex coordinates, since the selected edge is no longer an independent bridge coordinate and total derivatives hit the triangle propagators.

This demonstrates that the failure in Theorem 55.1 is an **insertion/local-counterterm compatibility defect**, not a failure of the elementary free propagator identity.

## 6. Exact tests and open mathematics

The deterministic standard-library fixture [055](fixtures/check_double_bridge_anomaly_055.py) checks the complete proper 1PI source inventory, the four cross-block simple cycles, graph and quotient Kirchhoff tree sums $30,8,8,2$, all four exact rational covariance embeddings, the two Laurent operator coefficients, the positivity of the scalar anomaly by exact integer inequalities, and the nonzero quadratic probe. This is a finite algebra/combinatorics regression; the distributional theorem is established by the Gaussian expansion above.

**Achieved:** an exact obstruction to premature forest factorization after adding a cycle-forming edge, including a strictly positive local scalar pole, a nonzero derivative pole, and a well-defined whole-diagonal correction that restores strong convergence.

**Open:** construction of the full 10-source **proper-subgraph** forest preparation on this graph, with supergraph-independent insertion coefficients and exact overlap/nesting consistency; a global second-order BV coderivation, QME, full normal-topology B.6 and liquid higher Ext.

**Next precise proof:** write the full forest poset for the double-bridge graph and perform the source-intrinsic Bogoliubov subtraction including all cross-block cycle and higher-loop sources, rather than fixing only the overall residual. Theorem 55.1 provides an exact rejection test for any proposed recursion that neglects the cross-block sources.