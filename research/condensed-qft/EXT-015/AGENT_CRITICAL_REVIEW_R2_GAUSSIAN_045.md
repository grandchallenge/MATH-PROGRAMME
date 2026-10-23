# EXT-015 REACH-R2 / 045 — mathematical critical audit of Gaussian graph finite parts and mixed Wick/BV edge identities

**Role and exact source.** Separate GCL logical mathematical critic pass against [candidate R2/044](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md), exact source PR [#2827](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2827), head \`578c991f886ee956d83160391288fb0db782ec53\`. This role-scoped check uses the same authenticated programme identity; it does **not** create a fictional external referee or confer MATHCERT authority. The candidate was verified with the exact rational fixture at that head; accepted mathematical claims below remain *bounded* until protected admission.

## 1. Independent Gaussian normalization and locality audit

For any connected positive-weight graph, a reduced incidence matrix has full column rank. Thus $Q=B^{\mathsf T}WB$ is positive definite. The product of $m$ unit-mass Gaussian edge approximants is proportional to the normalized Gaussian of dimension $n-1$ Gaussian with precision $Q/\epsilon^2$. The proportionality factor is

$$
(2\pi)^{-(m-n+1)/2}\,
\epsilon^{-(m-n+1)}
\sqrt{\frac{\prod_e w_e}{\det Q}}.
\tag{45.1}
$$

This independently checks the cycle-rank exponent and coefficient in (44.4). $\det Q$ equals the sum of weighted spanning trees, and its positivity is not a regularization assumption. As $\epsilon\downarrow0$ the normalized Gaussian is an approximate identity on the full relative-coordinate space. Even moments give powers of $\epsilon^2$ with the covariance contraction operator $\mathcal L_Q$; no odd moments occur. Therefore the local singular terms in (44.5) use precisely the powers $2k-h<0$, and the finite term for even $h$ has the coefficient $c_G/(2^{h/2}(h/2)!)$.

**Hostile normalization:** For a tree, the weighted spanning-tree sum is the product of its edge weights, so $c_G=1$ regardless of the chosen positive weights. The output is the canonical product of tree-edge deltas, a necessary control. The candidate passes it. For a triangle, $\det Q=3$ at unit weights and $h=1$, so the finite term vanishes; this is a **scheme-dependent finite-part statement**, not a declaration that the triangle distribution itself is zero.

**Disposition:** ACCEPT Theorem 44.1 and Corollary 44.2 within the specified Gaussian scheme.

## 2. Jets, Hermite parity and missing generality

The derivative identity

$$
\kappa_{\epsilon,w}^{(r)}(z)
=
\left(-\frac{\sqrt w}{\epsilon}\right)^r
\mathrm{He}_r(\sqrt w z/\epsilon)
\kappa_{\epsilon,w}(z)
\tag{45.2}
$$

is exact. The polynomial factor has inversion parity $(-1)^r$. Thus on any graph with edge-derivative sum $R$, a moment of total test degree $k$ vanishes whenever $R+k$ is odd. Since the putative finite degree is $k=h+R$, **odd cycle rank** forces the finite coefficient to vanish for every differentiated delta graph. The negative-power counterterms are local because the Gaussian moment expansion acts only at the full vertex diagonal.

**Adversarial scope:** These are **whole-graph** counterterms. They do not automatically satisfy a local forest insertion law for every proper divergent connected subgraph of an arbitrary graph. Explicitly, graphwise finite-part projection is a linear operation; it is not an algebra homomorphism on Laurent families. The candidate's own disconnected-graph counterexample proves that promoting it to such a homomorphism would be false.

**Disposition:** ACCEPT Theorem 44.3 only as a finite graphwise Gaussian jet extension.

## 3. Schur overlap calculation with exact witness

Marginalizing a normalized Gaussian with positive precision $Q$ over a coordinate block produces the Gaussian with Schur complement $S=D-B^{\mathsf T}A^{-1}B$. This follows by completing the square, with the determinant identity $\det Q=\det A\det S$. Since finite Gaussian integrations commute by Fubini, the final Schur complement is uniquely determined by the **union** of eliminated variables, including when two specified elimination sets overlap.

For the theta graph with unit weights, the candidate's exact Laplacian

$$
Q=
\begin{pmatrix}2&-1&-1\\-1&3&-1\\-1&-1&3\end{pmatrix}
\tag{45.3}
$$

has determinant $8$ and inverse with diagonal $(1,5/8,5/8)$; elimination of coordinates 1 and 2 (indexed from one) leaves Schur complement $8/5$ and eliminated determinant factor $5$. All six orders of full elimination have pivot product $8$. Independent rational fixture checks cover these equalities and 17 additional positive weighted graph instances.

**Hostile distinction:** This result is a coherent Gaussian **variable marginalization**, not automatically coherent subtraction of **overlapping edge subgraph divergences**. It creates effective interactions after eliminating internal vertices. It also does not prove full smooth normal-cone multilinear operations, only ordinary distribution-valued Gaussian integrals and Laurent coefficient compatibility.

**Disposition:** ACCEPT Theorem 44.4 with its exact variable-elimination scope.

## 4. Mixed Wick/BV kernel and its nonzero example

Let the delta edges include a connected spanning subgraph. Their Gaussian product forces all relative positions to scale as $\epsilon$. Each additional Wick derivative of order $t$ of $P_{\epsilon,w}$ scales as $\epsilon^{1-t}$, while each Gaussian delta derivative of order $r$ scales as $\epsilon^{-1-r}$. Relative integration has $\epsilon^{n-1}$ volume factor. Hence the resulting pole degree is exactly

$$
\Omega=h_D+R_D+R_P-|E_P|.
\tag{45.4}
$$

The unscaled Wick kernel is smooth with at most linear growth, and the Gaussian backbone ensures every mixed moment exists. Therefore the same distributional Taylor argument gives local counterterms and a finite part. Crucially, the *regulated functions themselves* obey $P_{\epsilon,w}''=\kappa_{\epsilon,w}$, so the Laurent coefficient at degree zero is identical whether one takes two derivatives on a Wick edge or replaces that edge with a delta edge. No master-equation or graph algebra conclusion is needed for that identity.

**Independent nonzero instance.** For three delta edges in a unit triangle and a parallel Wick edge, the delta backbone covariance along the chosen edge is $2/3$. Convolution with a unit-variance Gaussian gives expectation $E|N(0,5/3)|/2=\sqrt{5/(6\pi)}$. Multiplication by the triangle coefficient $1/\sqrt{6\pi}$ yields the nonzero finite amplitude $\sqrt5/(6\pi)\delta_\triangle$. Two derivatives on that Wick edge yield a unit fourth delta edge; its precision becomes $\left(\begin{smallmatrix}3&-2\\-2&3\end{smallmatrix}\right)$ with determinant five, and its second-derivative local finite part is nonzero as specified in 044. The exact rational fixture now derives the first coefficient from covariance and checks the second precision and finite-jet squared coefficient; neither merely asserts a constant.

**Adversarial boundary:** Adding an arbitrary new Wick edge when the delta backbone does **not** already connect every vertex is outside the theorem. Gluing two separately renormalized parts need not preserve the spanning delta condition; hence this graphwise free identity cannot be treated as the commutator identity for a complete second-order BV operator. A broad interacting quantum master equation and completed Costello–Gwilliam B.6 are not established.

**Disposition:** ACCEPT Theorem 44.8 and Example 44.9 solely in the connected Gaussian-backbone sector.

## 5. Genuine failure of naive factorization and corrected rule

On each unit triangle, $h=1$, so its own finite part vanishes. On the tensor product of two such regulated triangles, the total pole is $\epsilon^{-2}$; the Gaussian second moments contribute a **nonzero** coefficient of $\epsilon^0$ proportional to the Laplacians acting on the two diagonal deltas. The explicit test $1+y_1^2+z_1^2$, with localized root factors, gives $2/(9\pi)$, not zero. This proves that the global finite part is not the exterior tensor product of finite parts.

Defining the renormalized value for a disconnected graph as the exterior tensor product of its **individually** renormalized connected components is a mathematically valid symmetric-monoidal extension, with canonical permutation and association laws. It is deliberately a **prescription**, not a theorem that unmodified global finite-part extraction mysteriously becomes multiplicative.

**Hostile limitation:** The componentwise prescription is consistent with disjoint union and continuous fixed vertex derivatives, but cross-component Wick gluing can create new connected graphs and need not commute with the componentwise finite-part operation. Do not promote Corollary 44.7 to a full prefactorization algebra without checking those cross contractions.

**Disposition:** ACCEPT Theorem 44.6 and Corollary 44.7 as bounded negative and constructive claims, respectively.

## 6. Mathematical acceptance boundary and next decisive tests

| Claim | Critical finding |
| --- | --- |
| All-order connected Gaussian delta/delta-jet local counterterms | ACCEPT, fixed Gaussian scheme |
| Poset-independent Gaussian marginalization for overlapping elimination sets | ACCEPT, **not** a forest theorem for edge subgraphs |
| Mixed P-to-delta edge identity on connected Gaussian backbone | ACCEPT, bounded free graphwise BV identity |
| Failure of naive global finite part for disconnected graphs | ACCEPT, exact nonzero hostile control |
| Componentwise symmetric-monoidal repair | ACCEPT for disjoint union; **not** arbitrary Wick gluing |
| Universal nested/overlapping 1PI subgraph recursion | OPEN |
| Full BV second-order operator and quantum master equation | OPEN |
| Full differentiable B.6 Weiss descent and liquid higher Ext | OPEN |

The next research action should compare the connected-component prescription with a **two-stage subgraph-local Bogoliubov recursion**, where one Gaussian-connected subdivergence appears inside two distinct supergraphs. Determine whether counterterm coefficients can be chosen independently of the supergraph while preserving differentiated Wick edge identities. An explicit failure would be a valid mathematical obstruction.

**Validation:** Source head \`578c991f886ee956d83160391288fb0db782ec53\`, exact Python fixture PASS on authenticated CHAD, mathematical Markdown gate PASS, 17 weighted graphs and all six theta elimination orders. The reviewer is a separate GCL role-scoped logical pass, not a second authenticated account or an external source of certification. Admission must use protected PR merge and exact readback. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains OPEN.