# EXT-015 REACH-R2 / 049 — an actual two-supergraph local forest subtraction with overlapping and nested cycles

**Status: NEW BOUNDED MATHEMATICAL CANDIDATE; separately critically review.** Unlike earlier whole-graph Gaussian Laurent assignments, this construction gives **the same proper-subgraph counterterm in two different supergraphs**, subtracts every proper 1PI cyclic subgraph without multiplying overlapping singular counterterms, and obtains a finite distributional limit after one overall subtraction. A bridge-tree extension supplies a genuine nested case. The construction is an explicitly bounded, source-independent subgraph subtraction; it is not a universal Zimmermann/BPHZ recursion on all graphs, nor a complete BV or quantum-master-equation theorem.

**Source basis:** protected [R2/042](R2_OVERLAPPING_CYCLES_DELTA_JETS_042.md) and [audit 043](AGENT_CRITICAL_REVIEW_R2_THETA_043.md), [Gaussian graph 044](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md), [review 045](AGENT_CRITICAL_REVIEW_R2_GAUSSIAN_045.md), [bridge Laurent 046](R2_BRIDGE_TREE_LAURENT_BV_046.md), [Gaussian cycle insertion 047](R2_GAUSSIAN_CYCLE_INSERTION_047.md), and [critical review 048](AGENT_CRITICAL_REVIEW_CYCLE_INSERTION_048.md). Protected main at branch creation: \`814df762ac046a528a28bc222ecceea0439b0f22\`. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. A single proper-subgraph counterterm library

Fix the standard even unit Gaussian

$$
\kappa(z)=(2\pi)^{-1/2}e^{-z^2/2},
\qquad
\kappa_\epsilon(z)=\epsilon^{-1}\kappa(z/\epsilon).
\tag{49.1}
$$

All amplitudes are distributions in moving vertex-position variables, not evaluations of singular products at the diagonal. Define the following intrinsic, regulator-shape constants:

$$
\begin{aligned}
b_2&=\int_{\mathbb R}\kappa(z)^2\,dz
=\frac{1}{2\sqrt\pi},&
b_{2,2}&=\int_{\mathbb R}z^2\kappa(z)^2\,dz
=\frac{1}{4\sqrt\pi},\\
c_3&=\int_{\mathbb R^2}
\kappa(a)\kappa(b)\kappa(a+b)\,da\,db
=\frac{1}{\sqrt{6\pi}},&
c_4&=\int_{\mathbb R^3}
\kappa(a)\kappa(b)\kappa(c)\kappa(a+b+c)\,da\,db\,dc
=\frac{1}{\sqrt{8\pi}},\\
\kappa(0)&=\frac{1}{\sqrt{2\pi}}.
\end{aligned}
\tag{49.2}
$$

The values of $c_3,c_4$ follow either from Gaussian convolution at zero or from the matrix-tree theorem: a unit simple cycle of length $m$ has cycle rank one and spanning-tree sum $m$.

For each labeled proper **one-particle-irreducible (1PI) simple cycle** $\gamma$ of length $m\in\{2,3,4\}$, define its positive singular subtraction kernel by

$$
\mathsf S_{\gamma,\epsilon}
=\frac{c_m}{\epsilon}\,\delta_\gamma,
\quad
c_2=b_2,\qquad
\delta_\gamma=\text{product of independent spanning-tree edge deltas in }\gamma.
\tag{49.3}
$$

A counterterm is inserted into a supergraph by multiplying this source-local distribution by the **uncontracted smooth regulated edge factors** of that supergraph, then subtracting the resulting distribution. This prescription does not inspect the supergraph when computing $c_m$ or $\delta_\gamma$; the embedding determines only which edges remain.

**Important quantifier:** A cycle of length two is a pair of *distinct labeled parallel edges*. A four-edge cycle spanning all vertices is still a proper edge subgraph when its omitted chord remains. Graphs may also contain cyclic edge subsets with pendant bridges; those are not additional 1PI subgraphs. The construction never multiplies counterterms of two overlapping 1PI cycles in the same forest.

## 2. Theta graph: three overlapping proper cycles

Let $\Theta$ have vertices $1,2,3,4$, edge set $\{12,23,13,24,34\}$ and tree difference coordinates

$$
u=x_1-x_2,\qquad v=x_2-x_3,\qquad w=x_3-x_4,
\tag{49.4}
$$

with one free root coordinate. Its regulated amplitude is

$$
T_{\Theta,\epsilon}
=\kappa_\epsilon(u)\kappa_\epsilon(v)
\kappa_\epsilon(u+v)\kappa_\epsilon(v+w)\kappa_\epsilon(w).
\tag{49.5}
$$

The complete proper 1PI cycle inventory consists of triangles $A=(12,23,13)$ and $B=(23,24,34)$ and the spanning square $C=(12,24,34,13)$. Every pair overlaps; thus the only admissible proper forests are the empty forest and the **three singleton forests**. Write $\delta_\Theta=\delta(u)\delta(v)\delta(w)$.

The three independently assigned subgraph insertions are

$$
\begin{aligned}
S_{A,\epsilon}
&=\frac{c_3}{\epsilon}\delta(u)\delta(v)\kappa_\epsilon(w)^2,\\
S_{B,\epsilon}
&=\frac{c_3}{\epsilon}\delta(v)\delta(w)\kappa_\epsilon(u)^2,\\
S_{C,\epsilon}
&=\frac{c_4}{\epsilon}\delta_\Theta\kappa_\epsilon(v)
=\frac{c_4\kappa(0)}{\epsilon^2}\delta_\Theta.
\end{aligned}
\tag{49.6}
$$

The theta precision matrix and inverse in $(u,v,w)$ are

$$
Q_\Theta=
\begin{pmatrix}2&1&0\\1&3&1\\0&1&2\end{pmatrix},
\qquad
Q_\Theta^{-1}=
\begin{pmatrix}5/8&-1/4&1/8\\-1/4&1/2&-1/4\\1/8&-1/4&5/8\end{pmatrix},
\quad
\det Q_\Theta=8.
\tag{49.7}
$$

Its raw Gaussian coefficient is $c_\Theta=1/(4\sqrt2\pi)$, with cycle rank two.

## 3. Parallel-edge triangle: the same triangle counterterm in another supergraph

Let $\Pi$ have vertices $1,2,3$ with **two distinct parallel labeled** edges $a,b$ joining $1$ and $2$, plus edges $23,13$. Put

$$
u=x_1-x_2,\qquad v=x_2-x_3.
\tag{49.8}
$$

Then

$$
T_{\Pi,\epsilon}=\kappa_\epsilon(u)^2
\kappa_\epsilon(v)\kappa_\epsilon(u+v).
\tag{49.9}
$$

There are again precisely three proper 1PI simple cycles: triangle $A=(a,23,13)$, triangle $B=(b,23,13)$, and two-edge bubble $D=(a,b)$. They overlap pairwise. Their **source-local** subtractions, with the very same $c_3$ as in the theta graph, are

$$
\begin{aligned}
S_{A,\epsilon}=S_{B,\epsilon}
&=\frac{c_3\kappa(0)}{\epsilon^2}\delta_\Pi,\\
S_{D,\epsilon}
&=\frac{b_2}{\epsilon}\delta(u)\kappa_\epsilon(v)^2,
\qquad \delta_\Pi=\delta(u)\delta(v).
\end{aligned}
\tag{49.10}
$$

In this coordinate system

$$
Q_\Pi=\begin{pmatrix}3&1\\1&2\end{pmatrix},
\qquad
Q_\Pi^{-1}
=\begin{pmatrix}2/5&-1/5\\-1/5&3/5\end{pmatrix},
\qquad
\det Q_\Pi=5,\quad
c_\Pi=\frac{1}{2\pi\sqrt5}.
\tag{49.11}
$$

This is the decisive **different-supergraph check**: the triangle subtraction in both graphs is exactly $(c_3/\epsilon)\delta_\triangle$. What changes is the *remaining edge product* evaluated after collapse, not the counterterm intrinsic to the triangle.

## 4. Exact forest-preparation and overall-subtraction theorem

For either $G\in\{\Theta,\Pi\}$ define the **prepared distribution**

$$
\overline R_{G,\epsilon}=
T_{G,\epsilon}-\sum_{\gamma\in\mathcal C_G}S_{\gamma,\epsilon},
\tag{49.12}
$$

where $\mathcal C_G$ is exactly its three proper 1PI simple cycles; no pair is compatible as a disjoint or nested proper forest. Define the overall coefficient

$$
\begin{aligned}
g_\Theta&=c_\Theta-2c_3b_2-c_4\kappa(0)
=\frac{1}{\pi}\left(\frac{1}{4\sqrt2}-\frac{1}{\sqrt6}-\frac14\right),\\
g_\Pi&=c_\Pi-2c_3\kappa(0)-b_2^2
=\frac{1}{\pi}\left(\frac{1}{2\sqrt5}-\frac{1}{\sqrt3}-\frac14\right).
\end{aligned}
\tag{49.13}
$$

**Theorem 49.1 (two supergraphs, intrinsic overlapping subgraph counterterms).** The fully subtracted families

$$
R_{G,\epsilon}
=\overline R_{G,\epsilon}
-\frac{g_G}{\epsilon^2}\delta_G
\tag{49.14}
$$

converge strongly in distributions on the complete moving-vertex configuration space as $\epsilon\downarrow0$. Their limits are the following **finite local second-derivative distributions**:

$$
\begin{aligned}
L_\Theta
&=
\frac{c_\Theta}{2}
\sum_{i,j\in\{u,v,w\}}(Q_\Theta^{-1})_{ij}
\partial_i\partial_j\delta_\Theta
-\frac{c_3b_{2,2}}{2}
(\partial_u^2+\partial_w^2)\delta_\Theta,\\
L_\Pi
&=
\frac{c_\Pi}{2}
\sum_{i,j\in\{u,v\}}(Q_\Pi^{-1})_{ij}
\partial_i\partial_j\delta_\Pi
-\frac{b_2b_{2,2}}{2}
\partial_v^2\delta_\Pi.
\end{aligned}
\tag{49.15}
$$

For compactly supported test families, the remainders after subtraction are $O(\epsilon^2)$ in appropriate bounded-test seminorms. These are genuine **overlapping 1PI forest preparations**, with proper counterterms independent of the containing graph and a final graph-specific local subtraction. They demonstrate source independence across two distinct containing supergraphs, not universality across all supergraphs.

**Proof.** Each bare amplitude has cycle rank two and is exactly its constant $c_G\epsilon^{-2}$ times a normalized Gaussian in the independent relative coordinates, with covariance $\epsilon^2Q_G^{-1}$. The standard centered-Gaussian Taylor expansion gives

$$
T_{G,\epsilon}
=\frac{c_G}{\epsilon^2}\delta_G+
\frac{c_G}{2}\sum_{ij}(Q_G^{-1})_{ij}
\partial_i\partial_j\delta_G
+O_{\mathcal D'}(\epsilon^2).
\tag{49.16}
$$

For the theta triangles, the remaining two regulated factors become $\kappa_\epsilon(w)^2$ or $\kappa_\epsilon(u)^2$. Since $\kappa^2$ is even and has mass $b_2$ and second moment $b_{2,2}$,

$$
\frac{c_3}{\epsilon}\delta(u)\delta(v)\kappa_\epsilon(w)^2
=
\frac{c_3b_2}{\epsilon^2}\delta_\Theta
+\frac{c_3b_{2,2}}{2}\partial_w^2\delta_\Theta
+O_{\mathcal D'}(\epsilon^2),
\tag{49.17}
$$

and similarly for triangle $B$. The square term has exactly the leading pole in (49.6) and **no finite derivative part**.

For the parallel-edge triangle, each triangle collapse forces the other parallel edge to be evaluated at zero, giving $c_3\kappa(0)\epsilon^{-2}\delta_\Pi$ exactly. The bubble collapse leaves $\kappa_\epsilon(v)^2$, whose expansion is

$$
S_{D,\epsilon}
=\frac{b_2^2}{\epsilon^2}\delta_\Pi
+\frac{b_2b_{2,2}}2\partial_v^2\delta_\Pi
+O_{\mathcal D'}(\epsilon^2).
\tag{49.18}
$$

The differences of leading coefficients are (49.13), and subtracting them cancels the only negative Laurent power remaining in (49.12). The finite residues are (49.15). Gaussian rapid decay and vanishing odd moments give the strong $O(\epsilon^2)$ remainder on bounded compact test families. All products in (49.6) and (49.10) are well-defined because delta counterterms multiply only *uncontracted positive-regulator smooth factors*. No undefined product of overlapping deltas is taken. $\square$

**Locality:** The intrinsic cycle counterterms are supported only on the collision diagonal of that proper subgraph; the final $g_G\epsilon^{-2}\delta_G$ is supported on the total graph collision. No finite off-diagonal counterterm was inserted. The **overall** constants $g_G$ depend on the supergraph as permitted by local renormalization; this dependence must not be confused with proper-subgraph counterterm failure.

## 5. Exact hostile quadratic tests

Let each compact test be a smooth cutoff times the indicated quadratic polynomial, with the cutoff identically one on a fixed neighborhood independent of the regulator of the full collision and a separately normalized compact root-coordinate factor.

For the theta graph choose $\phi_\Theta=u^2$. The finite pairing is

$$
\langle L_\Theta,\phi_\Theta\rangle
=
\frac1\pi\left(\frac5{32\sqrt2}
-\frac1{4\sqrt6}\right).
\tag{49.19}
$$

For the parallel-edge graph choose $\phi_\Pi=v^2$. The finite pairing is

$$
\langle L_\Pi,\phi_\Pi\rangle
=
\frac1\pi\left(\frac3{10\sqrt5}-\frac18\right).
\tag{49.20}
$$

Both coefficients are **not** guessed by fitting a regulator limit: they follow from the exact Gaussian covariance and the intrinsic cycle-counterterm moments. The rational/surd coefficient fixture checks the source values, three-cycle inventories, subgraph pole cancellation, finite covariance residues, and the supergraph-invariant $c_3$ with exact algebraic identities.

## 6. A nested forest extension by an attached tree

Let $T$ be any finite tree of new vertices and unit Gaussian delta bridge edges attached to one vertex of $G\in\{\Theta,\Pi\}$, with no additional cycle. Use its independent oriented edge-difference coordinates $t_1,\dots,t_r$, and put $K_{\epsilon,T}=\prod_{j=1}^r\kappa_\epsilon(t_j)$.

**Proposition 49.2 (same proper counterterms work in bridge supergraphs).** With the counterterms of Theorem 49.1 inserted first into the cyclic core and the core's overall subtraction included, the bridge-extended family

$$
R_{G,\epsilon}\boxtimes K_{\epsilon,T}
\longrightarrow
L_G\boxtimes\left(\mathop{\boxtimes}_{j=1}^r\delta(t_j)\right)
\quad\text{strongly in distributions}.
\tag{49.21}
$$

No additional negative-power overall term is required for the bridge extension. The construction has a **nested** sequence of genuine subgraph operations: proper cycle counterterms inside $G$, then the *prepared* whole-core counterterm $g_G\epsilon^{-2}\delta_G$, then attachment of the tree. It respects the full bridge-tree Laurent calculus of [046](R2_BRIDGE_TREE_LAURENT_BV_046.md).

**Proof.** The quotient of the cyclic core and attached tree is a tree, so the bridge differences are independent of the core's relative coordinates with a unimodular change of variables. Theorem 49.1 gives strong convergence $R_{G,\epsilon}\to L_G$; the tensor product of the normalized Gaussian bridge kernels tends strongly to the product of one-dimensional deltas and stays bounded in the distribution topology. The exterior tensor product is hypocontinuous on bounded sets, hence the product family converges strongly to the displayed tensor product. Equivalently, use the explicit uniform Taylor remainders from Theorem 49.1 and Gaussian bridge moment bounds to obtain the convergence with an $O(\epsilon^2)$ remainder. $\square$

## 7. The boundary this resolves, and the one it does not

**Proved for a new nontrivial class:**
1. Intrinsic counterterms for triangle, square and parallel-bubble subgraphs, independent of the two containing supergraphs.
2. Exact three-cycle overlapping 1PI forest preparations for both the theta and parallel-edge triangle supergraphs.
3. Finite, explicitly calculated graphwise local derivatives after overall subtraction; all wavefront products avoided at finite positive regulator.
4. Nested use of those same local counterterms inside arbitrary finite **bridge-tree** extensions, including consistent strong limits.

**Still open:** applying the same counterterm library under **new cycle-forming supergraph insertions** that contain nested and overlapping 1PI subdivergences beyond this family; full BPHZ/Hopf-algebra character and forest insertion coherence; derivative-delta subgraph extensions and factor-local versus total-derivative BV identities; a domain-closed global BV operator and interacting QME; completed B.6 Weiss; liquid higher Ext.

**Next mathematical test:** insert a sixth edge into the theta graph (e.g. chord $14$), enumerate all proper 1PI subgraphs and all compatible nested/disjoint forests, and test whether the fixed counterterms computed here remain adequate when **two different divergent proper supergraphs overlap**. A signed counterexample to counterterm naturality would be as valuable as a positive closure theorem. Keep REACH-R2 #2797 OPEN.

**Test artifact:** [exact source regression](fixtures/check_two_supergraph_forest_049.py); standard-library rational/surd algebra, source policy gate, and a distinct exact-head role-scoped mathematical critical review are required before protected admission.