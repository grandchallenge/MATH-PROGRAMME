# EXT-015 REACH-R2 / 046 — bridge-tree Laurent-state renormalization and a genuine free BV gluing identity

**Status: bounded mathematical candidate requiring separate critical review.** This closes the first exact **bridge gluing** obligation left open by [R2/044](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md). It proves that a full distribution-valued Laurent jet, rather than an isolated finite part, provides associative gluing for any finite *tree of Gaussian delta-connected blocks*, including **Wick or BV bridge edges**. The exact free edge identity $P_\epsilon''=\kappa_\epsilon$ survives finite-part renormalization even when the Wick edge breaks global delta connectivity. It proves and repairs an explicit failure of gluing already-renormalized subgraphs. This is **not** a universal overlapping 1PI BPHZ/Zimmermann forest recursion, BV second-order coderivation on all configuration distributions, or a quantum master equation.

**Pinned evidence:** previously protected [R2/042](R2_OVERLAPPING_CYCLES_DELTA_JETS_042.md), [R2/043 audit](AGENT_CRITICAL_REVIEW_R2_THETA_043.md), [R2/044 Gaussian graph theory](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md) and [R2/045 audit](AGENT_CRITICAL_REVIEW_R2_GAUSSIAN_045.md). Protected main at branch creation \`c6c58ae442ae009f3bf8691fde17d8e2ea6c2a45\`. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. Precise category of bridge-assembled collision graphs

Let $G$ be a finite connected labeled multigraph obtained from disjoint connected **delta-only** graphs $G_1,\ldots,G_q$ by adding $q-1$ bridge edges whose quotient graph on the blocks is a tree. Each internal block contains only positive-weight Gaussian delta edges; a block consisting of an isolated vertex is allowed. The bridge edges may independently carry either a Gaussian delta propagator or a symmetric Wick propagator, or finite derivatives of those distributions. The *undifferentiated* case is proved first.

Give every edge a positive weight $w$. Define

$$
\kappa_{\epsilon,w}(t)
=\frac{\sqrt w}{\sqrt{2\pi}\epsilon}
e^{-wt^2/(2\epsilon^2)},
\qquad
P_{\epsilon,w}=P_0*\kappa_{\epsilon,w},
\qquad
P_0(t)=\frac{|t|}{2},
\qquad
P_{\epsilon,w}''=\kappa_{\epsilon,w}.
\tag{46.1}
$$

For each block $G_i$, choose an internal root vertex and coordinates $y_i$ consisting of all other vertex positions relative to that root. Its reduced weighted graph Laplacian $Q_i$ is positive definite if it has at least two vertices. Set

$$
h_i=|E(G_i)|-(|V(G_i)|-1),\quad
c_i=(2\pi)^{-h_i/2}
\sqrt{\frac{\prod_{e\in E(G_i)}w_e}{\det Q_i}},
\quad
\mathcal L_i
=\sum_{a,b}(Q_i^{-1})_{ab}
\partial_{y_{i,a}}\partial_{y_{i,b}}.
\tag{46.2}
$$

For an isolated vertex use $h_i=0,c_i=1$, and $\mathcal L_i=0$ with no internal variables.

For each bridge $e$ oriented from its endpoint in block $i$ to its endpoint in block $j$, take the **actual difference** of those vertex coordinates as an independent coordinate $t_e$. Retain one global root position $s$. Because the quotient of the blocks is a tree, all block-root positions can be reconstructed successively from $s$, the internal differences $y_i$, and the bridge differences $t_e$. This is an integer linear triangular coordinate transformation of determinant of absolute value one. Thus

$$
(s,\, (y_i)_{i=1}^q,\,(t_e)_{e\in E_{\mathrm{bridge}}})
\tag{46.3}
$$

is a global system of Lebesgue-Jacobian-one coordinates on the full vertex-position space. Every internal graph edge depends only on its own $y_i$; every bridge edge depends only on its own $t_e$. This **coordinate fact**, not an unjustified multiplication of collision deltas, is the crucial separation.

Let $\delta_i=\prod_a\delta(y_{i,a})$. For each bridge let $q_e=\delta_0(t_e)$ if it is BV/delta-type, and $q_e=P_0(t_e)$ if it is Wick-type. In these independent coordinates set

$$
S_G=\left(\mathop{\boxtimes}_{i=1}^q\delta_i\right)
\boxtimes\left(\mathop{\boxtimes}_{e\in E_{\mathrm{bridge}}}q_e\right),
\quad
H=\sum_{i=1}^q h_i,
\quad
C=\prod_i c_i,
\quad
\mathcal D_G=\sum_i\mathcal L_i+
\sum_{e\in E_{\mathrm{bridge}}}w_e^{-1}\partial_{t_e}^2.
\tag{46.4}
$$

The free global root coordinate $s$ is understood, without any imposed delta in that variable.

## 2. Exact heat representation and entire Laurent jet

Denote by $T_{G,\epsilon}$ the ordinary product of the positively regulated **internal delta edges** and all specified regulated bridge edges, as a smooth or polynomially growing function of all vertex positions.

**Theorem 46.1 (exact bridge-tree heat identity).** In tempered distributions on the vertex-position space, for every positive $\epsilon$,

$$
T_{G,\epsilon}
=
C\epsilon^{-H}\,
\exp\left(\frac{\epsilon^2}{2}\mathcal D_G\right)S_G.
\tag{46.5}
$$

Here the exponential is the actual Gaussian heat **semigroup** acting independently in each internal block and each bridge variable, not a claim that the formal series converges on arbitrary smooth tests.

For every nonnegative integer $N$, the equality yields a full strong-distribution Laurent asymptotic expansion

$$
T_{G,\epsilon}
=
C\sum_{k=0}^N
\frac{\epsilon^{2k-H}}{2^k k!}
\mathcal D_G^k S_G
+O_{\mathcal D'}(\epsilon^{2N+2-H}).
\tag{46.6}
$$

The error is uniform on bounded compactly supported test families. Every coefficient is a finite-order tempered distribution, local in the internal block collision coordinates and the delta bridge coordinates; Wick bridges may retain genuine $P_0$ dependence in their free relative variables.

**Proof.** On block $i$, the exact normalized Gaussian identity from R2/044 gives the distribution equality

$$
\prod_{e\in E(G_i)}\kappa_{\epsilon,w_e}(d_e)
=
c_i\epsilon^{-h_i}
\exp\left(\frac{\epsilon^2}{2}\mathcal L_i\right)\delta_i.
\tag{46.7}
$$

For a delta bridge, the one-dimensional Gaussian heat kernel satisfies $\kappa_{\epsilon,w}=\exp((\epsilon^2/2w)\partial_t^2)\delta_0$. For a Wick bridge, the convolution defining $P_{\epsilon,w}$ is the **same heat semigroup** applied to $P_0$. Exterior tensor products across the independent coordinates (46.3) commute with these separate semigroups, proving (46.5) *exactly*. The scalar exponent is $\sum_i h_i=H$; each bridge has its own normalized delta or Wick kernel and introduces no additional scalar power.

For the asymptotic claim, expand each heat kernel in its parameter $\epsilon^2$ against a compact smooth test. Repeated Taylor expansion, Gaussian moment bounds, and polynomial growth of $P_0$ control the remainder in the strong topology. Tensor products are well defined because all variables are independent. Collect the finitely many terms of total Taylor degree $k$ to obtain (46.6). A finite sum of constant-coefficient commuting second derivatives equals $\mathcal D_G$, so multinomial coefficients combine into $1/k!$. $\square$

**Corollary 46.2 (finite local/partial-diagonal renormalization).** Subtract precisely the terms of (46.6) with $2k<H$; the remaining family converges strongly to

$$
\mathrm{FP}(T_G)=
\begin{cases}
\displaystyle
\frac{C}{2^{H/2}(H/2)!}\mathcal D_G^{H/2}S_G,
& H\text{ even},\\
0,& H\text{ odd}.
\end{cases}
\tag{46.8}
$$

Every subtraction is a distribution on the collision strata already present in $S_G$. In particular for Wick bridges one must **not** falsely call it a full-vertex-diagonal local counterterm: $P_0(t_e)$ has nonzero support away from the bridge collision. The definition is local in each collapsed divergent subgraph, not necessarily in the unconstrained external separation. For all-delta bridge graphs the output is supported on the full vertex collision diagonal.

## 3. An actual associative gluing operation, with retained Laurent state

The **renormalization state** of a block is not its finite part but its full bounded-below Laurent germ

$$
\mathfrak L(G_i)=
c_i\sum_{k\ge0}
\frac{\epsilon^{2k-h_i}}{2^k k!}
\mathcal L_i^k\delta_i.
\tag{46.9}
$$

A bridge contributes the corresponding independent-variable Gaussian heat germ applied to $q_e$, beginning in order $\epsilon^0$. Glue by taking the exterior tensor product of the Laurent germs, adding the bridge germ, and applying the unimodular coordinate change. **Do not project to degree zero at an intermediate gluing stage.**

**Theorem 46.3 (associative bridge-tree Laurent gluing).** For any fixed labeled bridge tree as above, this retained-state gluing is associative and symmetric under reordering disjoint subassemblies, up to the canonical permutation and change-of-root coordinate isomorphisms. For any root and any parenthesization, it produces the same full Laurent coefficients as (46.6). A final projection $\mathrm{CT}$ to the $\epsilon^0$ coefficient therefore gives the same renormalized distribution under any order of gluing. Vertex differential operators with constant coefficients commute with this final projection.

**Proof.** A Laurent germ has a finite lower exponent and a well-defined coefficient at every exponent. Its exterior tensor product with independent-variable germs has a coefficientwise **finite** Cauchy product. The Cauchy product is associative; the exterior tensor product of distributions on disjoint variables is associative and symmetric. In a bridge tree, any gluing order introduces one previously unused bridge coordinate and the same final set of independent variables. Distinct root/parenthesis coordinate choices are related by unit-determinant linear diffeomorphisms, whose pullback commutes with the original regulated amplitude. Uniqueness of asymptotic coefficients implies the same transformed Laurent germ. Constant-coefficient differential operators commute with the distributional Laurent coefficient extraction. This gives the claim. $\square$

**Strict limitation:** This gluing is proved for **bridges**, i.e. edges joining subassemblies without forming an additional cycle in their quotient. Inserting an edge between vertices already connected creates a new loop and does **not** fall under this simple exterior-tensor-product theorem. Overlapping divergent subgraphs and arbitrary interacting diagrams remain the next obstruction.

## 4. Free BV edge conversion persists across a Wick bridge

**Theorem 46.4 (free BV identity despite disconnected delta backbone).** Suppose an edge $e$ is a **Wick bridge**. Replace its propagator by a **delta bridge** of the same weight and retain every other edge. The finite parts satisfy

$$
\partial_{t_e}^2\mathrm{FP}(T_G^{P_e})
=
\mathrm{FP}(T_G^{K_e}).
\tag{46.10}
$$

The identity holds coefficientwise for the entire Laurent germs and after any sequence of Wick-bridge-to-delta conversions or additional constant-coefficient vertex differentiations. It includes configurations with **no globally connected delta backbone before the conversion**, a case omitted from the bounded theorem R2/044.

**Proof.** The edge identity $\partial_t^2P_0=\delta_0$ is a Schwartz distribution identity. In (46.4), replacing $q_e=P_0$ by $\delta_0$ does not change $H,C$, or $\mathcal D_G$; the same $w_e^{-1}\partial_{t_e}^2$ heat term appears in both. The edge derivative $\partial_{t_e}^2$ commutes with all constant-coefficient operators in $\mathcal D_G$. Differentiate (46.6) term by term. The resulting coefficient for each Laurent power is exactly the coefficient of the delta-bridge family. Selecting $\epsilon^0$ proves (46.10). Conversions on distinct bridge variables commute. $\square$

**This is a genuine free graphwise BV compatibility result**, but **not yet** the nilpotence, second-order Leibniz property or interacting QME of an operator on a domain closed under all cyclic Wick gluing.

## 5. Exact two-triangle counterexample and its correction

Take two unit-weight triangle blocks $A$ and $B$ on vertices $(0,1,2)$ and $(3,4,5)$, joined by a bridge between vertices $2$ and $3$. Take $a=x_0-x_2$, $e=x_5-x_3$ and $t=x_2-x_3$ as three of the independent relative coordinates. Their Gaussian variances are

$$
\mathrm{Var}(a)=\frac23,\quad
\mathrm{Var}(e)=\frac23,\quad
\mathrm{Var}(t)=1,
\quad
c_A=c_B=\frac1{\sqrt{6\pi}},\quad H=2.
\tag{46.11}
$$

For a **delta bridge**, (46.8) yields

$$
\mathrm{FP}(T_{A-K-B})
=
\frac{1}{12\pi}
(\mathcal L_A+\mathcal L_B+\partial_t^2)
(\delta_A\boxtimes\delta_B\boxtimes\delta(t)).
\tag{46.12}
$$

Pair it with a compact test that equals $(x_0-x_5)^2=(a+t-e)^2$ near the full collision diagonal, with an independently normalized root-coordinate cutoff. The result is exactly

$$
\left\langle\mathrm{FP}(T_{A-K-B}),\phi\right\rangle
=
\frac{1}{6\pi}
\left(\frac23+1+\frac23\right)
=
\frac7{18\pi}.
\tag{46.13}
$$

Each triangle individually has odd cycle rank one and **zero finite part**. Naively gluing the *two finite parts* through $\delta(t)$ therefore gives zero, contradicting (46.13). The missing bridge-gluing correction comes from **three** Laurent coefficient convolutions: the positive-order quadratic moment in $A$ paired with the pole in $B$; the pole in $A$ paired with the quadratic moment in $B$; and the two poles paired with the positive-order bridge moment. All are mandatory.

For a **Wick bridge** at the same location, the full finite part is

$$
\mathrm{FP}(T_{A-P-B})=
\frac{1}{12\pi}\left[
(\mathcal L_A+\mathcal L_B)
(\delta_A\boxtimes\delta_B)\boxtimes P_0(t)
+
(\delta_A\boxtimes\delta_B)\boxtimes\delta(t)
\right].
\tag{46.14}
$$

This is nonzero and is **not** confined to the full six-point diagonal. It is a valid distribution-valued gluing operation for freely moving component positions. In particular, a test that is constant in the internal relative coordinates near their origin and has a Wick-separation factor $f(t)$ satisfying $f(0)=1$ gives $\langle\mathrm{FP}(T_{A-P-B}),\phi\rangle=1/(12\pi)$ after normalizing the root cutoff. Differentiating (46.14) twice in $t$ gives **exactly** (46.12), not merely equality of divergent leading coefficients.

**Second independent gluing witness:** Connect four unit triangles in a bridge chain with unit delta edges $t_1,t_2,t_3$. The total cycle rank is four, $C=(6\pi)^{-2}$. On a test that agrees near the total diagonal with $t_1^2t_2^2$, the finite-part pairing is

$$
\frac{1}{36\pi^2},
\tag{46.15}
$$

because the two independent bridge variances are one. Any procedure that replaces an individual triangle by its zero finite part before gluing instead gives zero. This confirms the defect is not specific to the two-block example.

## 6. Scope, tests and next theorem

**Established on the bounded graph class:** exact Gaussian heat normal form, all-orders local/partial-local distributional Laurent germ, explicit finite local counterterms, fully associative bridge-tree gluing retaining Laurent coefficients, free Wick-to-delta bridge conversion even without an existing global delta backbone, and exact positive hostile examples of missing gluing terms.

**Not established:** arbitrary new cyclic edges, overlapping 1PI subgraph recursion, Epstein–Glaser/BPHZ locality on the full graph Hopf algebra, a global second-order BV differential/quantum master equation, differentiable Weiss descent, or the original degree-two liquid Ext stage comparison.

The exact standard-library rational fixture [046](fixtures/check_bridge_laurent_046.py) checks Kirchhoff/bridge determinant factorization, the two-triangle effective resistance $7/3$, all three missing finite-part contributions, the four-triangle chain witness, Laurent convolution associativity, and the symbolic free Wick-to-delta coefficient map. It is not a substitute for the full distributional proof.

**Next decisive obligation:** extend the retained Laurent-state composition beyond bridges to **cycle-creating insertions**, with subgraph-local counterterms whose renormalization is independent of the supergraph. Determine whether the free BV edge conversion and differential identities survive such cycles, or exhibit an exact insertion anomaly. This is the next step required before claiming a complete renormalized BV algebra.