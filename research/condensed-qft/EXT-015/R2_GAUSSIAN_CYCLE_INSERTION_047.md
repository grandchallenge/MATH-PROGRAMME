# EXT-015 REACH-R2 / 047 — exact cycle-creating insertion, effective resistance and the finite-part obstruction

**Status: NEW BOUNDED MATHEMATICAL CANDIDATE; separate critical audit required.** This answers the first concrete cycle-creating insertion obligation after [R2/046](R2_BRIDGE_TREE_LAURENT_BV_046.md). For any connected Gaussian delta graph, adding another delta edge is an exact **rank-one update** of the reduced weighted Laplacian. The resulting graphwise Laurent coefficients and all of their local counterterms are determined by a finite-dimensional state $(Q,c,h)$; successive insertions commute regardless of order. A cycle-creating Wick edge also admits an exact Gaussian-moment finite-part expansion and preserves the edge-level regulated identity $P_\epsilon''=\kappa_\epsilon$ after coefficientwise renormalization. The candidate proves that keeping **only** finite parts cannot implement even one nontrivial linear cycle-insertion operation.

This is **not** a universal Bogoliubov/Zimmermann forest recursion on independently renormalized overlapping subgraphs, a completed BV coderivation on all distributions, an interacting QME, or a full Costello–Gwilliam B.6 differentiable Weiss theorem.

**Protected basis:** [R2/042](R2_OVERLAPPING_CYCLES_DELTA_JETS_042.md), [R2/043 critical review](AGENT_CRITICAL_REVIEW_R2_THETA_043.md), [R2/044](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md), [R2/045 critical review](AGENT_CRITICAL_REVIEW_R2_GAUSSIAN_045.md), and [R2/046 bridge-tree Laurent gluing](R2_BRIDGE_TREE_LAURENT_BV_046.md). Protected main at initial branch creation: \`b35b255dc61932459a2932fcab14a5764f46cf1b\`. Mathematical tracker [#2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797). The earlier R2/041 PR safety denial is a separate unresolved transaction, [CONTROL #44](https://github.com/grandchallenge/CONTROL/issues/44).

## 1. Connected Gaussian delta graph as a complete finite-dimensional state

Let $G$ be a finite connected multigraph on $n\ge2$ labeled vertices with $m$ edge occurrences and strictly positive edge weights. Choose a root and $d=n-1$ relative coordinates $y\in\mathbb R^d$ with volume Jacobian one, reduced incidence matrix $B\in\mathbb R^{m\times d}$, and positive definite reduced Laplacian

$$
Q=B^{\mathsf T}\mathrm{diag}(w_e)B,\qquad
h=m-d,\qquad
c=(2\pi)^{-h/2}
\sqrt{\frac{\prod_{e\in E(G)}w_e}{\det Q}}.
\tag{47.1}
$$

Put $\mathcal L_Q=\sum_{ij}(Q^{-1})_{ij}\partial_i\partial_j$ and $\delta=\prod_{j=1}^{d}\delta(y_j)$. The source-normalized regulated amplitude and its full distributional Laurent germ are exactly

$$
T_{G,\epsilon}
=c\,\epsilon^{-h}\rho_{\epsilon,Q}(y)
=c\,\epsilon^{-h}
\exp\left(\frac{\epsilon^2}{2}\mathcal L_Q\right)\delta,
\quad
\rho_{\epsilon,Q}(y)=
\frac{\sqrt{\det Q}}{(2\pi\epsilon^2)^{d/2}}
\exp\left(-\frac{y^{\mathsf T}Qy}{2\epsilon^2}\right).
\tag{47.2}
$$

The heat exponential in the middle expression is the **actual Gaussian heat semigroup**; as a displayed Laurent series it is interpreted coefficientwise, not as a convergent derivative series on arbitrary tests.

The state $\mathfrak S(G)=(Q,c,h)$ therefore completely determines every Laurent coefficient, finite part and whole-graph counterterm of the regulated delta amplitude in this Gaussian scheme.

## 2. An exact cycle-creation map using effective resistance

Add a new positive-weight delta edge $e$ between two **already connected** vertices. Let $v\in\mathbb Z^d$ be the reduced incidence row for that edge, with sign immaterial, and let $w>0$ be its weight. Its relative displacement is $\ell(y)=v^{\mathsf T}y$. Define the effective-resistance scalar

$$
R=v^{\mathsf T}Q^{-1}v>0.
\tag{47.3}
$$

The following is an actual exact operator on the finite-dimensional graph state, not merely a divergent pointwise product of limiting delta distributions.

**Theorem 47.1 (rank-one Gaussian cycle insertion).** With $G^+=G\cup\{e\}$ and with the same vertex coordinates, the exact state update is

$$
\begin{aligned}
Q^+&=Q+wvv^{\mathsf T},\qquad h^+=h+1,\\
(Q^+)^{-1}&=Q^{-1}-
\frac{w\,Q^{-1}vv^{\mathsf T}Q^{-1}}{1+wR},\\
\det Q^+&=(\det Q)(1+wR),\\
c^+&=c\,
\frac{\sqrt w}{\sqrt{2\pi}\sqrt{1+wR}}.
\end{aligned}
\tag{47.4}
$$

Moreover, for **every** positive regulator scale,

$$
\kappa_{\epsilon,w}(v^{\mathsf T}y)\,
T_{G,\epsilon}(y)
=
c^+\,\epsilon^{-(h+1)}\rho_{\epsilon,Q^+}(y).
\tag{47.5}
$$

Consequently every singular counterterm and finite local distribution for $G^+$ is calculated without an ill-defined product of collision deltas:

$$
\begin{aligned}
\operatorname{Sing}(G^+)
&=
c^+\sum_{2k<h+1}
\frac{\epsilon^{2k-h-1}}{2^k k!}
\mathcal L_{Q^+}^{\,k}\delta,\\
\operatorname{FP}(G^+)
&=
\begin{cases}
\displaystyle
\frac{c^+}{2^{(h+1)/2}((h+1)/2)!}
\mathcal L_{Q^+}^{(h+1)/2}\delta,
&h+1\text{ even},\\
0,&h+1\text{ odd}.
\end{cases}
\end{aligned}
\tag{47.6}
$$

**Proof.** Multiplying the regulated amplitude by the *positive-scale* Gaussian edge multiplies its scalar normalization by $\sqrt w/(\sqrt{2\pi}\epsilon)$ and adds $w(v^{\mathsf T}y)^2/(2\epsilon^2)$ to its exponent. The combined precision is $Q^+=Q+wvv^{\mathsf T}$ and its extra cycle rank is one. The matrix determinant lemma gives $\det Q^+=\det Q(1+wR)$, and Sherman–Morrison gives the inverse in (47.4). Dividing by the correctly normalized Gaussian $\rho_{\epsilon,Q^+}$ produces the stated coefficient $c^+$ and proves (47.5) exactly. The Gaussian moment expansion of (47.2) with the new state gives (47.6), with local counterterms supported on the full coincidence diagonal. $\square$

**Corollary 47.2 (arbitrary insertion order is coherent).** For finitely many new edges $(v_j,w_j)$ added on the same connected vertex set, in any order, the final graph state is

$$
Q_{\mathrm{fin}}=Q+\sum_jw_jv_jv_j^{\mathsf T},\quad
h_{\mathrm{fin}}=h+r,\quad
c_{\mathrm{fin}}=
c\,(2\pi)^{-r/2}
\sqrt{\frac{\prod_jw_j\,\det Q}{\det Q_{\mathrm{fin}}}}.
\tag{47.7}
$$

Therefore all graphwise Gaussian Laurent coefficients and **whole-graph** counterterms are independent of insertion order. The same result includes parallel edges and formerly bridge-assembled connected delta graphs.

**Proof.** Apply (47.4) successively. Determinants telescope and all rank-one precision increments add; the result is symmetric under every permutation of the new edges. Every normalized positive-regulator product is likewise commutative. There is no multiplication of singular delta distributions, since all products are taken at $\epsilon>0$ before coefficientwise distributional expansion. $\square$

**Important restriction:** This proves order-independent **whole-graph** renormalization after cycle insertion, not automatically a universal subgraph-local counterterm that is independent of its containing supergraph. For overlapping 1PI subgraphs, further compatibility requirements remain.

## 3. The cycle-creating Wick edge

Instead insert a Wick propagator of the **same** weight, $\displaystyle P_{\epsilon,w}(t)=P_0*\kappa_{\epsilon,w}(t)$ with $P_0(t)=|t|/2$ and $P_{\epsilon,w}''=\kappa_{\epsilon,w}$. Scaling gives $P_{\epsilon,w}(t)=\epsilon p_w(t/\epsilon)$, where

$$
p_w(z)=\frac12\mathbb E|z+N(0,w^{-1})|.
\tag{47.8}
$$

**Theorem 47.3 (Wick cycle insertion, explicit finite part and edge-level BV relation).** Let $Z$ be centered Gaussian with covariance $Q^{-1}$ and define, for any multi-index $\alpha$,

$$
\mu_\alpha^{P}
=\mathbb E\left[Z^\alpha p_w(v^{\mathsf T}Z)\right].
\tag{47.9}
$$

Then the new Wick-edge amplitude has a full distributional Laurent expansion

$$
T^{P_e}_{G,\epsilon}
=c\sum_{k\ge0}\epsilon^{k+1-h}
\sum_{|\alpha|=k}
\frac{(-1)^k\mu_\alpha^P}{\alpha!}
\partial_y^\alpha\delta.
\tag{47.10}
$$

The moments vanish when $|\alpha|$ is odd. After subtracting all negative Laurent powers, its finite part is zero when $h$ is even. For **odd** $h$, the finite part is given by the coefficient at $k=h-1$, a local derivative of the full-vertex collision delta. In particular when $h=1$,

$$
\operatorname{FP}(G+P_e)
=c\sqrt{\frac{R+w^{-1}}{2\pi}}\,\delta,
\tag{47.11}
$$

which is strictly nonzero.

For each positive $\epsilon$, applying two **factor-local** derivatives to the selected Wick edge, while keeping every other graph edge factor unchanged, produces exactly the delta-edge graph. Taking coefficients of the two identical regulated products gives the edge-conversion identity

$$
\operatorname{CT}_{\epsilon^0}
\left[T_{G,\epsilon}\,
P_{\epsilon,w}''(v^{\mathsf T}y)\right]
=
\operatorname{CT}_{\epsilon^0}
\left[T_{G,\epsilon}\,
\kappa_{\epsilon,w}(v^{\mathsf T}y)\right]
=
\operatorname{FP}(G^+).
\tag{47.12}
$$

**Proof.** Pair the product with a test $\phi(y)$ and integrate against the Gaussian density in (47.2). Writing $y=\epsilon Z$ gives a prefactor $c\epsilon^{1-h}$ and integrand $p_w(v^{\mathsf T}Z)\phi(\epsilon Z)$. All Gaussian polynomial moments exist because $p_w$ has at most linear growth. Taylor's theorem and Gaussian tail bounds give a strong distributional expansion; the signs in (47.10) arise from derivatives of delta. Since $p_w$ is even, odd moments vanish. The zero-power coefficient requires $k=h-1$, and (47.11) follows because $v^{\mathsf T}Z+N(0,w^{-1})$ is centered normal of variance $R+w^{-1}$, whose absolute first moment is $\sqrt{2(R+w^{-1})/\pi}$. Finally $P_{\epsilon,w}''=\kappa_{\epsilon,w}$ is an exact smooth function identity at every positive regulator, so the two *edge-factor* products and all their Laurent coefficients agree. $\square$

**Differential-type warning:** The factor-local two derivatives in (47.12) are **not** the total vertex-coordinate derivative of the already assembled amplitude. When the inserted edge closes a cycle, its displacement $v^{\mathsf T}y$ is not an independent coordinate from the original graph's Gaussian factors. A total vertex derivative also differentiates those original factors. The proof therefore makes an **edge-labeled identity**, not a false statement that applying $\partial_{v^{\mathsf T}y}^2$ directly to the scalar finite part produces the delta-insertion finite part. The stronger global BV operator identity remains open.

## 4. Exact examples and a negative theorem for premature finite-part projection

**Example 47.4 (triangle and a parallel new edge).** A unit-weight triangle rooted at vertex 3 has

$$
Q=\begin{pmatrix}2&-1\\-1&2\end{pmatrix},
\qquad Q^{-1}=\begin{pmatrix}2/3&1/3\\1/3&2/3\end{pmatrix},
\quad
h=1,\quad c=\frac1{\sqrt{6\pi}}.
\tag{47.13}
$$

Add a unit edge along displacement $y_1-y_2$ (so $v=(1,-1)^{\mathsf T}$). Then $R=2/3$ and

$$
Q^+=\begin{pmatrix}3&-2\\-2&3\end{pmatrix},\qquad
(Q^+)^{-1}=
\begin{pmatrix}3/5&2/5\\2/5&3/5\end{pmatrix},
\qquad \det Q^+=5.
\tag{47.14}
$$

The graph has two cycles. Its nonzero renormalized finite part is

$$
\operatorname{FP}(G^+)=
\frac{1}{4\pi\sqrt5}\mathcal L_{Q^+}\delta.
\tag{47.15}
$$

On a compact test agreeing with $y_1^2$ near the collision diagonal, with an independently normalized root-coordinate cutoff, the finite-part pairing is $3/(10\pi\sqrt5)$.

The **Wick** edge along the same displacement instead gives the nonzero finite part

$$
\operatorname{FP}(G+P_e)
=\frac{\sqrt5}{6\pi}\,\delta.
\tag{47.16}
$$

These are two concrete, different outputs of the same cycle-creating edge operation, satisfying the regulated edge-conversion identity (47.12) **before** final projection.

**Theorem 47.5 (no cycle insertion linearized on finite parts alone).** There is no linear map on the vector space of finite-part distributions that implements cycle creation for all connected Gaussian delta graphs by acting **only** on $\operatorname{FP}(G)$ and discarding the other Laurent coefficients. In fact, for the triangle in Example 47.4, the source finite part is zero (since $h=1$), while the target of a unit parallel delta-edge insertion is the nonzero distribution (47.15). Every linear map sends zero to zero, a contradiction.

The theorem excludes this **premature projection** rule only. A graph-dependent reconstruction that retains $Q,c,h$, or a richer graph-indexed state, is perfectly valid; (47.4) gives such a construction. It does not refute the existence of a true subgraph-local BPHZ forest formula.

## 5. Scientific boundary and reproducibility

The standard-library exact regression fixture [047](fixtures/check_gaussian_cycle_insertion_047.py) checks the rank-one inverse and determinant identities for connected weighted graph inputs, arbitrary two-edge insertion orders, weighted Kirchhoff sums, both explicit triangle examples, and the squared normalizations of their nonzero finite parts. All matrix arithmetic is rational. Irrational constants involving $\pi$ and Gaussian absolute moments are checked by exact rational identities **after** factoring their prescribed symbolic powers; no floating-point tolerance is used.

**Established in this bounded Gaussian programme:** exact finite-state cycle insertion, all-order local Laurent counterterms, order-independent insertions including parallel edges, explicit Wick-cycle finite parts, a factor-local free BV edge substitution identity across newly created cycles, and an exact counterexample to linear cycle insertion on finite parts alone.

**Still open:** universal counterterm assignment for proper overlapping/nested edge subgraphs *independent of supergraph*; full BV differential/bracket identities on a domain closed under graph insertion and collision; interacting quantum master equation; normal-topology multimorphism and completed B.6 Weiss comparison; original liquid syzygy higher-Ext comparison. Neither this positive Gaussian result nor the negative finite-part obstruction authorizes claiming any of those.

**Next exact target:** build an insertion-compatible subgraph renormalization map on a family containing *two overlapping cycle insertions*, compute the full counterterm composition (rather than only the final rank-one-updated precision), and compare the induced factor-local Wick/BV edge conversion with a globally defined second-order BV operator. Source-specific positive proof or exact anomaly are both valid outcomes.