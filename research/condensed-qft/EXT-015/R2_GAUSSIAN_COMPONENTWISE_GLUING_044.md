# EXT-015 REACH-R2 / 044 — Gaussian collision graphs, coherent coarse-graining and the finite-part factorization defect

**Status: BOUNDED MATHEMATICAL CANDIDATE; separately audit before mathematical promotion.** On the full finite graph class of Gaussian-regulated delta kernels and their derivatives, this note supplies an exact all-orders local expansion, an associative Schur-complement marginalization procedure for overlapping elimination sets, and a *symmetric-monoidal componentwise finite-part prescription*. It also proves that taking the finite part **after** multiplying disconnected divergent graphs violates factorization. It does **not** prove a universal subgraph-local BPHZ forest formula or a complete BV/QME theory.

**Source lock:** current protected [R2/042](R2_OVERLAPPING_CYCLES_DELTA_JETS_042.md) and [R2/043](AGENT_CRITICAL_REVIEW_R2_THETA_043.md), protected main at authoring c6b0ce36de521e29a7b60b2bc9104a3c4e81879c. These are already protected-admitted. Earlier R2/041 was not PR-admitted and remains subject to the original [CONTROL #44](https://github.com/grandchallenge/CONTROL/issues/44) host-denial incident; no claim here depends on having published 041.

## 1. Exact connected graph Gaussian identity

Let $G=(V,E)$ be a finite **connected**, undirected multigraph with $n\ge2$ vertices, $m$ edge occurrences and positive edge weights $w_e$. Self-loops may be omitted or handled as constant Gaussian factors; for transparency assume each edge joins two distinct vertices. Fix a vertex $r$ as root and write $y_i=x_i-x_r$ for the remaining $n-1$ relative coordinates, with root coordinate $s=x_r$. The change of variables has absolute determinant one. Choose arbitrary orientations of edges and the reduced incidence matrix $B\in\mathbb R^{m\times(n-1)}$. Define

$$
Q_G=B^{\mathsf T}\mathrm{diag}(w_e)B,\qquad
\tau_w(G)=\det Q_G>0,\qquad
h=m-n+1.
\tag{44.1}
$$

Here $h$ is the cycle rank; $\tau_w(G)$ is the weighted spanning-tree sum by the matrix-tree theorem. The exact source-normalized Gaussian delta regulator is

$$
\kappa_{\epsilon,w}(z)
=
\frac{\sqrt w}{\sqrt{2\pi}\epsilon}
\exp\left(-\frac{wz^2}{2\epsilon^2}\right).
\tag{44.2}
$$

Let $T_{G,\epsilon}(x)=\prod_{e=(i,j)}\kappa_{\epsilon,w_e}(x_i-x_j)$. Put

$$
c_G=(2\pi)^{-h/2}
\sqrt{\frac{\prod_e w_e}{\tau_w(G)}},
\qquad
\rho_{\epsilon,Q}(y)
=
\frac{\sqrt{\det Q}}{(2\pi\epsilon^2)^{(n-1)/2}}
\exp\left(-\frac{y^{\mathsf T}Qy}{2\epsilon^2}\right).
\tag{44.3}
$$

**Theorem 44.1 (exact Gaussian graph normal form).** For every such graph and every positive $\epsilon$,

$$
T_{G,\epsilon}(s,y)=c_G\epsilon^{-h}\rho_{\epsilon,Q_G}(y).
\tag{44.4}
$$

Consequently, in the space of distributions over all vertex positions and for any integer $N\ge0$,

$$
T_{G,\epsilon}
=
c_G\sum_{k=0}^{N}
\frac{\epsilon^{2k-h}}{2^k k!}
\mathcal L_G^k\delta_G
+O_{\mathcal D'}(\epsilon^{2N+2-h}),
\quad
\mathcal L_G=
\sum_{i,j}(Q_G^{-1})_{ij}\partial_{y_i}\partial_{y_j},
\tag{44.5}
$$

where $\delta_G=\prod_{i\ne r}\delta(y_i)$ has the standard Jacobian-one normalization. The estimate is uniform on each bounded family of compactly supported smooth tests and on compact positive-weight sets.

**Proof.** The product of $m$ Gaussian normalizations contributes $(2\pi\epsilon^2)^{-m/2}\prod_e\sqrt{w_e}$, and its exponent is the quadratic form $y^{\mathsf T}Q_G y$. Divide this product by the normalized Gaussian density $\rho_{\epsilon,Q_G}$ and obtain exactly $c_G\epsilon^{-h}$. Since $G$ is connected, $B$ has full column rank and $Q_G$ is positive definite. If $Z$ is centered Gaussian with covariance $Q_G^{-1}$, pair (44.4) with a test $\phi(s,y)$: the result is $c_G\epsilon^{-h}\int ds\,\mathbb E[\phi(s,\epsilon Z)]$. The Gaussian identity $\mathbb E\phi(\epsilon Z)=(\exp((\epsilon^2/2)\mathcal L_G)\phi)(0)$, understood by its finite Taylor remainder, gives (44.5). Every Gaussian moment is finite uniformly on compact positive-weight sets, so Taylor's theorem bounds the remainder by the stated power. Evenness kills odd moments. Distributional derivatives of $\delta_G$ have positive sign at even derivative orders. $\square$

**Corollary 44.2 (complete local Gaussian counterterms and finite part).** Subtract the terms of (44.5) for which $2k<h$; these are local derivatives of the **full collision diagonal**. The result converges to the finite-part distribution

$$
\mathrm{FP}(T_G)=
\begin{cases}
\displaystyle
\frac{c_G}{2^{h/2}(h/2)!}
\mathcal L_G^{h/2}\delta_G,&h\text{ even},\\[2mm]
0,&h\text{ odd}.
\end{cases}
\tag{44.6}
$$

For a tree, $h=0$ and $c_G=1$, so (44.6) recovers exactly the canonical product of the edge deltas. For a triangle, $h=1$, the symmetric Gaussian finite part is zero. For the four-vertex five-edge theta graph, $h=2$, the finite part is a nonzero quadratic derivative-delta operator and is consistent with the local second-derivative structure of R2/042, but belongs to a different regulator scheme.

## 2. Arbitrary differentiated delta edges

Let $r_e\ge0$ be the derivative order of each edge kernel and put $R=\sum_e r_e$. Use probabilists' Hermite polynomials $\mathrm{He}_k$, defined by

$$
(-1)^k\frac{d^k}{dz^k}e^{-z^2/2}
=\mathrm{He}_k(z)e^{-z^2/2}.
\tag{44.7}
$$

The product of differentiated edges has the exact representation

$$
T^{\mathbf r}_{G,\epsilon}
=
c_G\epsilon^{-(h+R)}
H_{\mathbf r}(y/\epsilon)\rho_{\epsilon,Q_G}(y),
\quad
H_{\mathbf r}(z)=
\prod_{e\in E}(-\sqrt{w_e})^{r_e}
\mathrm{He}_{r_e}(\sqrt{w_e}(Bz)_e).
\tag{44.8}
$$

**Theorem 44.3 (all-order jet finite part and parity).** Put $d=h+R$, $\mu_\alpha=\mathbb E_{Z\sim N(0,Q_G^{-1})}[H_{\mathbf r}(Z)Z^\alpha]$. Then, coefficientwise as distributions,

$$
T^{\mathbf r}_{G,\epsilon}
\sim
c_G\sum_{k\ge0}\epsilon^{k-d}
\sum_{|\alpha|=k}
\frac{(-1)^{|\alpha|}\mu_\alpha}{\alpha!}
\partial_y^\alpha\delta_G.
\tag{44.9}
$$

Subtracting all terms $k<d$ yields the finite local term at $k=d$. In particular the finite part **vanishes for every odd cycle rank $h$**, regardless of edge-jet orders; for even $h$, it is a local derivative-delta distribution of total order at most $h+R$ with explicit Gaussian polynomial moments.

**Proof.** The $r$th derivative of (44.2) is $(-\sqrt w/\epsilon)^r\mathrm{He}_r(\sqrt w z/\epsilon)\kappa_{\epsilon,w}(z)$. Multiplication gives (44.8). Taylor-expand $\phi(s,\epsilon Z)$ by total multi-index degree and integrate the compact test against the Gaussian polynomial weight; the moments of $H_{\mathbf r}$ bound every remainder. The delta derivative pairing introduces the sign in (44.9). Since $H_{\mathbf r}(-z)=(-1)^R H_{\mathbf r}(z)$ and $Z^\alpha$ has parity $|\alpha|$, $\mu_\alpha=0$ if $R+|\alpha|$ is odd. At finite-part degree $|\alpha|=h+R$, the parity becomes $h+2R$, odd exactly when $h$ is odd. $\square$

Unlike arbitrary formal point values on singular diagonals, these are distributions in all **moving vertex-position variables**. Independent smooth translations of the positions act smoothly into the ordinary strong distribution topology, as does the dependence on positive edge weights. These statements do not assert the stronger normal-cone multilinear topology or a BV master equation.

## 3. Coherent elimination for nested and overlapping variable sets

Split relative coordinates as $(u,v)$ and the positive definite graph precision matrix as

$$
Q=
\begin{pmatrix}
A&B\\ B^{\mathsf T}&D
\end{pmatrix},
\quad
S=D-B^{\mathsf T}A^{-1}B.
\tag{44.10}
$$

**Theorem 44.4 (Schur marginal and order-independent coarse graining).** Integrating the normalized Gaussian $\rho_{\epsilon,Q}$ over the coordinates $u$ produces exactly $\rho_{\epsilon,S}(v)$, with $\det Q=\det A\det S$. For any two elimination sets $I,J$ (including overlapping ones), eliminating their union by either permitted sequence of disjoint remaining pieces produces the **same** final Schur complement and normalization. Thus the Gaussian graph amplitudes, their Gaussian moment expansions, and **the coefficients of their finite-part local counterterms when tested on retained coordinates** are independent of elimination order.

**Proof.** Complete the square in $u$ in the Gaussian exponent:

$$
u^{\mathsf T}Au+2u^{\mathsf T}Bv+v^{\mathsf T}Dv
=
(u+A^{-1}Bv)^{\mathsf T}A(u+A^{-1}Bv)
+v^{\mathsf T}Sv.
$$

Integration in $u$ gives the determinant factor and marginal precision $S$. All integrals have Gaussian decay and are absolutely convergent. Fubini's theorem makes iterated integrations independent of order. When $I$ and $J$ overlap, integrate their intersection once and then the two disjoint differences; this is an ordinary lawful decomposition, not multiplication of overlapping singular delta counterterms. Gaussian moments and the Taylor/finite-part coefficient functionals are uniquely determined by these marginals, proving the coefficientwise statement. $\square$

**Example 44.5 (exact theta witness).** With unit edge weights and root vertex 4, the theta-graph reduced Laplacian and inverse are

$$
Q=
\begin{pmatrix}
2&-1&-1\\
-1&3&-1\\
-1&-1&3
\end{pmatrix},
\quad
Q^{-1}=
\begin{pmatrix}
1&1/2&1/2\\
1/2&5/8&3/8\\
1/2&3/8&5/8
\end{pmatrix},
\quad \det Q=8.
\tag{44.11}
$$

Eliminating the first two coordinates in either order has determinant prefactor $5$ and leaves scalar Schur complement $8/5$. Eliminating all three coordinates in *any* of the six orders has product of pivots $8$. The normalized finite part on a test equal near the diagonal to $1+y_1^2+2y_2^2+3y_3^2$ is $(33/8)c_G$ times the integral over the root coordinate.

This **does not** establish the full renormalized subgraph forest formula: Schur elimination of graph **variables** generates effective interactions between remaining vertices, and is not the same as assigning universal counterterms to edge subgraphs. It is an exact, reusable compatibility lemma for a Gaussian sector of that larger programme.

## 4. A real factorization obstruction and its exact correction

Let $G_1$ and $G_2$ be **two disjoint triangles**, with identical unit weights. For each connected triangle $h=1$, so $\mathrm{FP}(T_{G_i})=0$ by (44.6). But the regularized tensor product has expansion

$$
T_{G_1,\epsilon}\boxtimes T_{G_2,\epsilon}
=
c_1c_2\epsilon^{-2}
\left[
\delta_1\boxtimes\delta_2+
\frac{\epsilon^2}{2}
\left(
\mathcal L_1\delta_1\boxtimes\delta_2+
\delta_1\boxtimes\mathcal L_2\delta_2
\right)
+O(\epsilon^4)
\right].
\tag{44.12}
$$

**Theorem 44.6 (global finite part fails the disjoint-union axiom).** The coefficient of $\epsilon^0$ in (44.12) is nonzero although both component finite parts vanish. In fact for tests equal to $1+y_1^2+z_1^2$ near the two collision diagonals, and with compact root-coordinate factors normalized to integral one, this global finite-part pairing is exactly

$$
\frac{2}{9\pi}\ne0,
\tag{44.13}
$$

while the product of component finite parts is zero. Therefore **extracting one global Laurent finite part after multiplying disconnected regulated amplitudes is not a symmetric-monoidal renormalization**.

**Proof.** For each triangle $\tau=3$, $h=1$, $c_i=1/\sqrt{6\pi}$, and the diagonal entries of its inverse reduced Laplacian equal $2/3$. The $\epsilon^0$ coefficient in the product is $(c_1c_2/2)(\mathcal L_1\delta_1\boxtimes\delta_2+\delta_1\boxtimes\mathcal L_2\delta_2)$. Acting on the displayed test gives $(c_1c_2/2)(4/3+4/3)=2/(9\pi)$. Each one-component finite part is zero because only odd powers $\epsilon^{2k-1}$ appear. $\square$

**Corollary 44.7 (a symmetric-monoidal corrected prescription).** For an arbitrary finite graph with connected components $G_1,\ldots,G_q$, define

$$
\mathcal R_\mathrm{comp}(G)
=
\mathop{\boxtimes}_{a=1}^{q}\mathrm{FP}(T_{G_a})
\tag{44.14}
$$

and analogously for differentiated delta edges, with each component renormalized using (44.9) *before* taking the exterior tensor product. Then $\mathcal R_\mathrm{comp}$ is symmetric-monoidal for disjoint unions, permutation-invariant, supported on each connected component's collision diagonal, and compatible with vertex differentiation **within the connected graph sector** and Gaussian coordinate marginalization of local coefficient functionals.

**Proof.** Disjoint-union factorization is exactly how (44.14) is defined; the canonical associativity/symmetry isomorphisms for exterior tensor products give its coherence. For a connected graph, extracting the $\epsilon^0$ coefficient of a distribution-valued Laurent asymptotic commutes with every fixed continuous linear differential operation; the Gaussian integrals of Section 3 establish the analogous property for admissible relative-coordinate marginalizations. The connected output is supported on the full diagonal by (44.6)/(44.9). No statement about interacting products or arbitrary graph insertion is inferred. $\square$

**Critical qualification:** Equation (44.14) fixes only the **disjoint-union factorization defect**. It is not yet proved stable under arbitrary Wick insertion of cross-component propagator edges or BV gluing of previously renormalized subgraphs. That stronger extension must satisfy new identities; the theorem does not rename a missing proof as complete.

## 5. Exact arithmetic regression and next obligation

The standard-library exact fixture [044](fixtures/check_gaussian_graph_044.py) verifies the reduced Laplacians, weighted matrix-tree equality, all six theta elimination orders, overlapping Schur reductions, additional weighted graph cases, the nonzero disjoint-triangle obstruction and a theta second-derivative coefficient without floats or external algebra libraries.

**Achieved:** explicit all-orders Gaussian graph counterterms with edge derivatives; genuine distribution-valued collision outputs; order-independent Gaussian marginalization even for overlapping eliminated sets; an exact obstruction to naive global finite-part factorization; a corrected connected-component monoidal prescription.

**Not achieved:** universal subgraph-local counterterm recursion for arbitrary overlapping 1PI insertions; a domain-closed BV second-order operation that respects the connected-component prescription under all Wick contractions; master-equation anomaly/cocycle; normal-topology completed B.6 Weiss descent; original liquid Ext degree-two verdict.

**Next exact mathematics:** combine the Gaussian conditional-moment calculus with a properly **subgraph-local** Bogoliubov/Zimmermann recursion on a bounded family of graphs, and prove commutation with the free BV differential or exhibit an explicit insertion anomaly. Any claim of a general forest formula must distinguish overlapping **edge subgraphs** from overlapping **elimination-variable sets**.

**Source context:** The matrix-tree theorem and Gaussian marginalization are standard; the specific GCL construction and its factorization counterexample here are derived directly, not claimed as novel universal mathematical machinery. See [Scholarpedia BPHZ framework](https://www.scholarpedia.org/article/BPHZ_framework) for the distinct forest-formula requirements. Parent research issue: [EXT-015 REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).