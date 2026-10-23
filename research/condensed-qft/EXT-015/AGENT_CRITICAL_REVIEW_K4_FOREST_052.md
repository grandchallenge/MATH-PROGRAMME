# EXT-015 REACH / 052 — adversarial mathematical review of the K4 nested-overlap subtraction

**Source-locked role-scoped GCL mathematical critic.** Reviewed research [R2/051](R2_K4_NESTED_OVERLAP_FOREST_051.md), exact source [PR #2837](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2837) head \`e677a0b1ab89cba1457a9951b59068ce30c67032\`, and [exact fixture 051](fixtures/check_k4_nested_forest_051.py). This is a logically separate mathematical pass under one authenticated GCL identity, not a fictitious external reviewer or complete certification. The parent [R2 issue #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains open.

## 1. Independent enumeration and strict forest bookkeeping

For the complete graph on four vertices with six distinct edges, a connected bridgeless proper subgraph containing a cycle can have three, four, or five edges. The possibilities are four three-edge triangles, three four-edge squares, and six five-edge graphs obtained by omitting exactly one edge, each isomorphic to theta. A three-edge cycle is contained in three five-edge theta graphs (the omitted edge is one of the three edges outside that triangle); a square is contained in two (the omitted edge is one of the two diagonals). Thus the nested pair count is $4\cdot3+3\cdot2=18$. Every pair of distinct proper 1PI graphs shares an edge; no two distinct proper 1PI subgraphs are disjoint. The forest poset has one empty forest, 13 singleton forests, and 18 nested two-subgraph forests: exactly 32.

**Potential error actively excluded:** a five-edge theta is not primitive. It has its *own* two triangles and square. Counting the theta's subtraction as merely the unprepared Gaussian leading constant would omit the nested forest contributions. The correct source counterterm is the already prepared value $g_\Theta/\epsilon^2$ from R2/049. Thus the 18 nested terms are incorporated *once*, through each theta counterterm. They must not be added a second time as independent products of singular diagonal distributions. This review accepts the use of the **prepared** theta coefficient and rejects a naive theta-leading-coefficient insertion.

**Disposition:** ACCEPT the 13/18/32 combinatorial inventory and nested-counterterm rule for this specific graph.

## 2. Recalculate all Gaussian normalization factors

With relative vertex coordinates $y_j=x_j-x_4$ for $j=1,2,3$, the K4 reduced precision is $Q=4I-J$, where $J$ is the all-ones matrix of size three. Its eigenvalues are $1,4,4$, so $\det Q=16$ and

$$
Q^{-1}=\frac14(I+J)
=\begin{pmatrix}1/2&1/4&1/4\\1/4&1/2&1/4\\1/4&1/4&1/2\end{pmatrix}.
\tag{52.1}
$$

The cycle rank is $6-3=3$. Thus the bare Gaussian density has coefficient $c_G=(2\pi)^{-3/2}/4=1/(8\sqrt2\pi^{3/2})$ times $\epsilon^{-3}$. Its next term is $(c_G/(2\epsilon))\mathcal L_G\delta_G$, not a scalar. Higher terms begin at positive powers of epsilon.

The independently evaluated intrinsic source constants, after factoring out $\pi^{-3/2}$, are:

| Contribution | Coefficient multiplying $\epsilon^{-3}\delta_G$ |
| --- | --- |
| Bare six-edge K4 | $+\sqrt2/16$ |
| Four triangles together, subtracted | $-\sqrt2/3$ |
| Three squares together, subtracted | $-3\sqrt2/8$ |
| Six prepared theta terms, subtracted | $-3/4+\sqrt3+3\sqrt2/4$ |

Their sum is exactly

$$
a_{-3}=\frac1{\pi^{3/2}}
\left(\sqrt3-\frac34+\frac{5\sqrt2}{48}\right).
\tag{52.2}
$$

A negative theta counterterm $g_\Theta$ creates a positive contribution when subtracted: this sign is **not optional**. The exact fixture uses rational coefficient triples for $1,\sqrt2,\sqrt3$ and asserts the identity without numerical approximation.

**Disposition:** ACCEPT the scalar pole coefficient; source and signs are consistent.

## 3. The derivative pole: independent normal-space witness

The triangle with vertices $1,2,3$ leaves vertex 4 outside; when the triangle's collapsed position changes, the quotient normal vector in the coordinates $(y_1,y_2,y_3)$ is $(1,1,1)$. The other three triangles contain the root and omit one of vertices $1,2,3$, so their quotient normals are the three standard basis vectors. Hence, writing $D_v=v\cdot\nabla_y$,

$$
\sum_{\mathrm{four\ triangles}}D_v^2
=\left(\partial_1+\partial_2+\partial_3\right)^2
+\partial_1^2+\partial_2^2+\partial_3^2
=4\mathcal L_G.
\tag{52.3}
$$

For an even normalized Gaussian $\kappa$, the density $\kappa^3$ has second moment $b_{3,2}=b_3/3=1/(6\pi\sqrt3)$. Every triangle produces finite-in-quotient expansion at order $\epsilon^{-1}$ proportional to $(c_3b_{3,2}/2)D_v^2\delta_G$. The four together contribute

$$
-\frac{c_3b_{3,2}}{2\epsilon}
\sum_v D_v^2\delta_G
=-\frac{2c_3b_{3,2}}{\epsilon}\mathcal L_G\delta_G
\tag{52.4}
$$

to the prepared amplitude. Squares and the prepared theta counterterms collapse all four vertices and therefore have **no** quotient-variable Taylor second moment at that order. The bare derivative term is $(c_G/2)\mathcal L_G\delta_G/\epsilon$. Their difference is

$$
a_{-1}=\frac{c_G}{2}-2c_3b_{3,2}
=-\frac{7\sqrt2}{288\pi^{3/2}}
=-\frac{7}{144\sqrt2\pi^{3/2}}.
\tag{52.5}
$$

**Hostile independent test:** On a smooth compactly supported test agreeing with $y_1^2$ near the full collision diagonal, $\mathcal L_G(y_1^2)=2(Q^{-1})_{11}=1$. The prepared amplitude then has exactly the nonzero pole $a_{-1}/\epsilon$. A proposed subtraction consisting only of $a_{-3}\epsilon^{-3}\delta_G$ would fail. The second local *derivative-of-delta counterterm* is necessary.

**Disposition:** ACCEPT the derivative-pole coefficient and necessity of both local overall counterterms.

## 4. Distributional meaning and finite remainder

Every proper source subgraph counterterm is a finite product of independent collision deltas on the subgraph multiplied only by **uncontracted, smooth positive-regulator** edge functions from K4. No two overlapping singular counterterms are multiplied. The bare Gaussian and the one-dimensional quotient products of $\kappa^3$ have inversion symmetry, so Taylor expansions contain only the powers $\epsilon^{-3}$, $\epsilon^{-1}$, $\epsilon^{1}$, and so on. The two displayed counterterms eliminate the entire negative part. Gaussian tails provide all required moments; Taylor remainders are $O(\epsilon)$ on bounded compact test sets.

**Hostile scope:** The strong limit of **this particular** K4 family is zero under the chosen minimal whole-graph subtraction prescription. This does not assert that all physical renormalization schemes have zero finite K4 amplitudes, nor that the coefficient assignments form a unique, functorial all-graph BPHZ scheme. Local finite renormalizations remain possible.

**Disposition:** ACCEPT Theorem 51.3 as a bounded analytic Gaussian distribution theorem.

## 5. Deliberate limits and next mathematical gate

1. Nested forest terms for K4 are accounted for through the prepared lower-theta source. This is a **finite three-loop example**, not a proof of a universal forest/Hopf-algebra character for arbitrary graphs, especially those with disjoint divergent 1PI components or multiple independently branching nests.
2. The counterterms are for undifferentiated *Gaussian delta edges*. Extending a source counterterm under arbitrary differentiated delta/Wick insertions and showing equivalence of edge-local and total BV differentials is unsolved.
3. This theorem does not supply a globally defined second-order BV coderivation, its nilpotence, or an interacting quantum master equation.
4. Ordinary strong distributional convergence does not establish normal-wavefront-cone smooth multilinear factorization or completed Costello–Gwilliam B.6 Weiss descent.
5. The original liquid source's higher-Ext comparison remains a separate research obligation.

The exact fixture verified all 13 1PI subgraphs, 18 nested pairs, 32 proper forests, K4 determinant 16, the four quotient normal directions and both poles with rational/surd arithmetic. Mathematical Markdown rendering was independently corrected and passed on the author's head. This review is a distinct logical mathematical pass; it is not independently authenticated specialist evidence.

**Next target:** a bounded class closed under **multiple simultaneous branches** of the nested-subgraph forest poset and disjoint cyclic components. Construct source-local counterterms by induction on the graph and prove that the forest recursion produces a genuine character under disjoint unions. Then check compatibility of differentiated delta/Wick insertions with the same counterterm assignment, or produce a precise anomaly.

**Verdict:** Theorems/Lemmas of R2/051 ACCEPT **within the exact K4 graph and its Gaussian scheme**, pending protected source/adversarial review admission. Keep R2 #2797 OPEN after admitting the bounded milestone.
