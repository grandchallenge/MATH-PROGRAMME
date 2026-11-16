# EXT-015 REACH / UC-OP-004 — exact heat-graph and partition incidence

**Primary disposition: BOUNDED FINITE CONORMAL CLASSIFICATION.** For an actual finite product of constant-direction Gaussian convolutions along graph differences, the heat-normal gate of UC001 reduces to the column rank of an integer matrix of component/block intersection sizes. The gate passes for every collision partition exactly when the ungrounded heat graph is connected. A failed gate has an actual compact smooth-block partition source whose heat output stays nonsmooth at every positive regulator. These are statements about this typed heat family; no original105 all-corner scalar theorem, completed108 universal operator, original126 family lift, universal150.L, residual W acyclicity or original R3 follows.

## 1. Frozen sources and operation type

| Contract | Source identity |
| --- | --- |
| [UC001 heat-normal gate](UNIFORM_CONIC_GREEN_OPERATOR_AUDIT_UC001.md) | Git blob 437d40de4a1a5a723cb49bcf31f0190df1fda0b5 |
| [UC002 distinct logical criticism](AGENT_CRITICAL_REVIEW_UNIFORM_CONIC_UC002.md) | Git blob 948bfc32d186ea63c3543e7a5d2bad17bfd3c5b4 |
| [UC003 bounded ledger](UNIFORM_CONIC_ACCEPTANCE_UC003.md) | Git blob f78c82800d3850543591d8106d27911aa3b2bb34; prior accepted scope and open original-source obligations; no terminal claim imported |
| [Original scalar105](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | Git blob a8ce66ff0edec33e2aff299550fca2089d671033; fixed complete corner indices and auxiliary remainder weights |
| [Original mixed108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | Git blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6; entire finite histories108.7 and completed coefficient stages108.6 |
| [Original parameter126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | Git blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163; whole-source rows, with full126.14 still open |

Work on $X=\mathbb R^n$ with $n\ge1$, one real coordinate per physical vertex. The zero-vertex unit has no conormal gate and is outside the graph assertion. Fix a finite undirected graph $G$ on these vertices, including isolated vertices. Orient its edges arbitrarily and let $D$ have columns $e_i-e_j$. Give each listed edge a strictly positive variance $w_e$, and set

$$
W=\mathrm{diag}(w_e),\qquad L=DWD^{\mathsf T},\qquad
E(\zeta)=\zeta^{\mathsf T}L\zeta
=\sum_{e=ij}w_e(\zeta_i-\zeta_j)^2.
\tag{UC4.1}
$$

Here $L$ is the covariance/Laplacian matrix, whereas UC001 used its letter $L$ for the directional analysis map. Their kernels agree after taking the Gram matrix. At regulator $\epsilon>0$ the actual heat operator is

$$
H_\epsilon T=\mu_\epsilon*T,\qquad
\mu_\epsilon=D_*\gamma_{\epsilon^2W},\qquad
\widehat\mu_\epsilon(\zeta)=e^{-\epsilon^2E(\zeta)/2},
\tag{UC4.2}
$$

where $\gamma_{\epsilon^2W}$ is the normalized Gaussian probability measure on edge variables. For no edges, $\mu_\epsilon=\delta_0$ and $L=0$. Repeated edges are allowed in the theorem, with positive variances summed; orientation has no effect. The fixture enumerates simple graphs because these already exhaust possible kernels.

Formula UC4.2 is a finite factorized **convolution** operator on a specified ambient distribution. Multiplication by a scalar Gaussian edge in105 is a different operation. No reordering of mixed108 multiplication, restriction, inclusion or vertex-forgetting is assumed to produce UC4.2. The standard Laplacian energy/component facts below are proved directly; no novelty or external certification is claimed for them.

## 2. Component/block intersection theorem

Let $\pi$ be a partition of the vertices into nonempty blocks $B$. Write $D_\pi\subset X$ for its physical diagonal, with coordinates constant within each block, and

$$
N_\pi=D_\pi^\perp
=\{\zeta:\ \sum_{i\in B}\zeta_i=0\text{ for every }B\in\pi\}.
\tag{UC4.3}
$$

Let $C_1,\ldots,C_c$ be the connected components of the heat graph, and form the integer matrix with rows indexed by partition blocks and columns by heat components:

$$
M_\pi(B,a)=|B\cap C_a|.
\tag{UC4.4}
$$

**Theorem UC4.1.** Component constants identify $\ker M_\pi$ with $\ker L\cap N_\pi$. In particular,

$$
\dim(\ker L\cap N_\pi)=c-\mathrm{rank}(M_\pi),
\qquad
E|_{N_\pi}\text{ is positive definite}
\ \Longleftrightarrow\ \mathrm{rank}(M_\pi)=c.
\tag{UC4.5}
$$

Positive definiteness on the zero space is vacuous, as required for the discrete partition.

**Proof.** Positivity of every $w_e$ makes $E(\zeta)=0$ equivalent to equality of the two entries on every edge. Thus $\ker L$ consists exactly of vectors $\zeta_i=u_a$ on $C_a$. The map from $u\in\mathbb R^c$ to this component-constant vector is injective. Its block sum on $B$ is $\sum_a|B\cap C_a|u_a$, so its membership in $N_\pi$ is precisely $M_\pi u=0$. A nonnegative quadratic form is positive definite on a subspace exactly when that subspace misses its kernel except at zero. This proves all assertions. $\square$

For direct computation choose a basis matrix $Q_\pi$ of $N_\pi$: within each block choose a root $r_B$ and take columns $e_i-e_{r_B}$ for the other vertices of that block. It has $d=n-|\pi|$ columns. The independent restricted-Gram check is

$$
K_\pi=Q_\pi^{\mathsf T}LQ_\pi,\qquad
d-\mathrm{rank}(K_\pi)=c-\mathrm{rank}(M_\pi).
\tag{UC4.6}
$$

This follows because $Q_\pi$ is injective onto $N_\pi$ and $K_\pi$ is positive semidefinite. It is the full matrix rank, not positivity on each basis vector, that controls all combinations. The criterion depends only on graph components and partition intersections; positive edge weights affect bounds, not the nullity.

**Corollary UC4.2 (all partitions).** For an ungrounded graph with $n\ge1$, the gate passes for every partition if and only if $G$ is connected.

**Proof.** If $G$ is connected its kernel consists of the single constant vector. Every $N_\pi$ has total frequency sum zero, so it contains no nonzero constant vector. Conversely use the full collision partition with one block: its matrix is the single row $(|C_1|,\ldots,|C_c|)$, of rank one. This has full column rank exactly when $c=1$. If $c\ge2$ an explicit obstructing kernel vector is obtained by $u_1=|C_2|$, $u_2=-|C_1|$ and all remaining $u_a=0$. $\square$

A disconnected graph can pass a particular partition. For example the partition into the heat components gives a diagonal matrix of positive component sizes. Thus the all-partitions conclusion must not replace the per-history test UC4.5.

The original six-vertex eleven-edge host has the six $K_4$ edges $01,02,03,12,13,23$ and edges $04,14,05,15,45$. It is connected. **Conditionally**, if these eleven edges are the directional convolutions UC4.2, its heat-normal gate passes all203 partitions of six vertices. The original Gaussian/Wick multiplication-host graph is not automatically this convolution graph. This calculation proves neither actual host factorization nor original source closure; it is a labelled algebraic control tied to the existing model.

## 3. A hostile crossing partition and an actual nonsmoothing source

Take four vertices, edges $01$ and $23$ with unit variances, and partition blocks $\{0,2\}$ and $\{1,3\}$. Then

$$
M_\pi=\begin{pmatrix}1&1\\1&1\end{pmatrix},\quad
q_1=e_0-e_2,\quad q_2=e_1-e_3,\quad
K_\pi=\begin{pmatrix}2&-2\\-2&2\end{pmatrix}.
\tag{UC4.7}
$$

Each displayed generator has positive energy two, but their sum $(1,1,-1,-1)$ lies in the heat kernel and the partition conormal. This is a rank failure on an entire legal nonidentity partition, invisible to a basis-vector-only energy check.

More generally suppose $M_\pi$ is column deficient. Choose a nonzero $u\in\ker M_\pi$ and its component-constant covector $\zeta$. Let $i_\pi:\mathbb R^{|\pi|}\to X$ be the block-coordinate inclusion, with its fixed actual coordinate density. Choose nonnegative, nonzero $f\in C_c^\infty(\mathbb R^{|\pi|})$ supported inside a small allowed physical interval patch, and put

$$
T=(i_\pi)_*(f(y)\,dy),\qquad
V=D_\pi+\mathrm{range}(D).
\tag{UC4.8}
$$

This is an actual legal order-zero partition-inclusion source of108.7, with smooth block coefficient and compact support, rather than an illegal singular original R1 coefficient on independent vertices. It uses the identity scalar coefficient locally (with a fixed cutoff if needed); no product of singular delta kernels is introduced. Its actual heat output is the positive finite measure

$$
H_\epsilon T
=A_*\bigl(f(y)\,dy\otimes\gamma_{\epsilon^2W}(z)\bigr),
\qquad A(y,z)=i_\pi y+Dz.
\tag{UC4.9}
$$

The annihilator of $V$ is $N_\pi\cap\ker D^{\mathsf T}$, which contains $\zeta\ne0$. Thus $V$ is a proper linear subspace. UC4.9 is supported in $V$ and has positive mass $\int f$, at every $\epsilon>0$. A smooth function supported in a proper linear subspace must be zero, since its complement is dense. Hence this nonzero distribution cannot be smooth. This is an actual nonsmoothing output, stronger than just an untested zero-energy covector. Heat tails can leave a compact physical patch; a final smooth cutoff near a support point preserves a nonzero singular output, and does not claim a globally compact heat kernel.

For completeness the converse for these **smooth block inputs** is also concrete. If UC4.5 passes, $V=X$ and $A$ is surjective. The input density in UC4.9 is Schwartz, because $f$ is compact smooth and the edge Gaussian is Schwartz. Pushforward of a Schwartz density under a surjective linear map is Schwartz: choose linear coordinates splitting kernel and image, integrate the kernel coordinates, and differentiate under this rapidly decaying integral. Thus $H_\epsilon T$ is smooth for every positive regulator. This converse does not apply to an arbitrary nonsmooth tangential block coefficient.

## 4. Positive conic estimates and their exact scope

If UC4.5 passes and $N_\pi\ne0$, compactness of its unit sphere supplies a constant $a_\pi>0$ such that $E(\zeta)\ge a_\pi|\zeta|^2$ on $N_\pi$. Continuity gives the same inequality with a smaller constant on a sufficiently small closed conic neighborhood of that subspace. For a fixed finite set of passing partitions, take the minimum of their positive constants and choose their neighborhoods accordingly. An empty conormal requires no frequency neighborhood or smoothing assertion.

The same conclusion is uniform for variances in a fixed compact subset of the strictly positive orthant: if $w_e\ge w_*>0$, compare UC4.1 with $w_*\sum_e(\zeta_i-\zeta_j)^2$. No estimate uniform through a vanishing edge variance is asserted. For fixed smooth bounded symbols supported in these elliptic cones, UC001 Theorem UC1.2 therefore applies with its original finite Sobolev seminorms and all fixed regulator derivatives. Smooth parameter-dependent variances also require bounded parameter derivatives on the compact parameter patch; differentiating their Gaussian factors produces finite polynomial factors, absorbed by a weaker Gaussian. This is only the ambient, conic-restricted operator estimate.

In particular conormal rank does not assert smoothing of arbitrary nonsmooth tangential coefficients on $D_\pi$, or global ellipticity on $X^*$. A connected ungrounded graph always leaves the common-coordinate heat kernel. Smooth-block inputs in section3 and fixed conic components as in UC001 are the precise positive assertions here. Neither proves a new original105 scalar stage with compatible all-corner power/logarithmic indices and recursive remainders.

## 5. Separately typed extension: coordinate heat represented by a ground node

This section permits additional **convolutional** heat directions $e_i$ with strictly positive variances. Represent such a direction as the edge from vertex $i$ to an auxiliary bookkeeping node $*$, whose covector value is fixed at zero. Ordinary edges remain $e_i-e_j$. This ground is an algebraic way of encoding coordinate heat, not a physical vertex, delta insertion, boundary condition or extra108 operation.

In the enlarged graph call a component free if it does not contain $*$. Components connected to $*$ contribute no heat-kernel variable: edge equalities force their covector values to zero. If there are $c_f$ free components, retain only their columns in UC4.4 and call the resulting matrix $M_\pi^f$. The same proof gives

$$
\ker L\cap N_\pi\cong\ker M_\pi^f,\qquad
E|_{N_\pi}>0\ \Longleftrightarrow\ \mathrm{rank}(M_\pi^f)=c_f.
\tag{UC4.10}
$$

The empty-column matrix has rank zero. The gate passes for every physical partition exactly when $c_f\le1$. If $c_f=0$, the heat form is positive definite on all of $X^*$. If $c_f=1$, a nonzero component constant has total frequency sum $|C_1|u_1\ne0$, so it cannot belong to any $N_\pi$. If $c_f\ge2$, the full physical collision gives the same two-component witness as Corollary UC4.2. In particular this differs from requiring the enlarged graph to be connected. The nonsmoothing measure proof also applies with coordinate columns included in $D$. No ground condition is imported into the ungrounded theorem.

## 6. Exact fixture and scientific boundary

The stdlib-only fixture [heat_graph_partition_incidence_uc004.py](../../../fixtures/algebraic/heat_graph_partition_incidence_uc004.py) independently constructs graph components/intersection matrices and the actual rational covariance restricted to within-block difference bases. It compares their nullities on every simple ungrounded graph and every partition for $1\le n\le5$, and every grounded graph and physical partition for $1\le n\le4$. Positive rational edge variances are used throughout. Every deficient matrix also supplies an exact rational component-constant witness checked against the partition sums and the actual covariance. Explicit controls cover the crossing partition UC4.7, particular-partition success for a disconnected graph, a grounded graph with exactly one free component, zero free components and a vanishing-variance invalidation of an incorrectly retained edge. The all-partitions equivalences are checked for every enumerated graph.

The labelled eleven-edge host additionally has all203 partitions checked against its actual rational covariance, under the conditional convolution interpretation above. No enumeration of all six-vertex graphs is needed for that control.

This finite arithmetic regression checks the incidence identities and hostile examples; it does not prove the analytic pushforward or Fourier estimates. Execution is CHAD-local on Windows using an isolated CPython environment, with external owner caches. The worktree has no admitted Python lockfile, so that environment is **not pinned**; a stdlib run is not a reproducible immutable deployment or independent execution attestation.

The result is a rejection/selection test for a proposed finite factorized heat family and partition history. It does not identify arbitrary scalar105 multiplication histories with that family. The remaining source obligations include actual factorization, complete105 scalar indices at every corner, fixed lower auxiliary weights, R1 restrictions, finite jets, proper density maps, continuity through108.6 completion and whole-source126 rows. The original uniform rapid relation is unchanged. Universal150.L, residual W acyclicity, original R3, full126.14, higher weights and M5/R4 remain open. No inverse, contracting homotopy, protected admission or external mathematical certification is asserted. Distinct logical criticism and a bounded ledger belong to subsequent artifacts, not this primary.
