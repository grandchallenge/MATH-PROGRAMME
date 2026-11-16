# EXT-015 REACH / UC-OP-005 — source-locked critical review of graph-component collision-incidence rank

**Verdict: BOUNDED INTERNAL MATHEMATICAL ACCEPT, with exact graph/convolution source scope.** Verifier V-UC005 and Adversary A-UC005 are logically distinct checks under the same authenticated ChatGPT/GitHub identity. This is neither an independently authenticated nonauthor APPROVED review nor public mathematical certification.

## 1. Frozen source and executable evidence

Primary [HEAT_GRAPH_PARTITION_INCIDENCE_UC004.md](HEAT_GRAPH_PARTITION_INCIDENCE_UC004.md), exact Git blob d9d5698d3de3729fbc33dfd539ed9c9c22b9a1f3, on branch research/reach-heat-graph-incidence-uc004-20261115. The corresponding exact rational fixture [heat_graph_partition_rank_uc004.py](../../../fixtures/algebraic/heat_graph_partition_rank_uc004.py), Git blob 92339fe9cb730a19b334430cea2c34cf511dc91f, was fetched directly from its GitHub branch and run by authenticated CHAD OS-only Python. Exit 0, six test groups PASS; file SHA256 bee077be655508f7af8fd957d9602d62f5b9e1314e5d19962da4eeb91c4bddd3; execution receipt 61379a550a30401181463b8aacd04c85, independent_execution_attested=false. This fixture is an exact algebraic regression, not an independently verified proof of source-stage all-corner analytic claims.

Protected antecedents: original105 Git blob a8ce66ff0edec33e2aff299550fca2089d671033, mixed108 Git blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 and source-controlled parameter126 Git blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163. The bounded conic heat-normal operator [UC001](UNIFORM_CONIC_GREEN_OPERATOR_AUDIT_UC001.md) blob 437d40de4a1a5a723cb49bcf31f0190df1fda0b5 and [critic UC002](AGENT_CRITICAL_REVIEW_UNIFORM_CONIC_UC002.md) blob 948bfc32d186ea63c3543e7a5d2bad17bfd3c5b4 were native protected-merged in PR3376, merge ce828643ec7cf2e001ab068e578daf4befb91fbb. Nonterminal CP223 in PR3377 is separately pending, and is not treated as a mathematical theorem or protected here.

## 2. V-UC005 — graph kernel and collision conormal without sign errors

For edge heat directions $e_i-e_j$ with strictly positive fixed weights, the quadratic energy is the sum of positive terms $a_{ij}(\zeta_i-\zeta_j)^2$. Its kernel therefore requires equal coordinates at the endpoints of every edge, hence constants on each connected component $H_h$; isolated vertices add legitimate independent constants. Conversely every component-constant vector has zero energy. The component indicator vectors are linearly independent, proving precisely $k$ kernel dimensions.

For a collision partition with blocks $B_\alpha$, the physical diagonal is defined by equalities within each block. Its tangent vectors are constant within each block. A covector annihilates all tangent vectors precisely when its **sum in each block is zero**, independently for each block. Thus the displayed conormal condition UC4.4 is correct, and its dimension is $n-b$. This orientation is crucial: requiring covectors to be equal within each partition block would give the tangent space instead of its annihilator.

Intersecting the graph kernel with the conormal imposes the linear system $\sum_h|B_\alpha\cap H_h|c_h=0$. The map from constants $c$ to the covector $\zeta_i=c_h$ is injective; hence the intersection dimension is the nullity of the integer matrix $M_{P,G}$. Its vanishing is exactly column rank $k$. Integer coefficients ensure rational row-reduction produces a rational kernel witness if the rank is deficient; the associated real covector is an explicit nonzero characteristic conormal. The energy's continuous strictly positive quadratic form on the compact unit conormal sphere gives the fixed positive lower bound. The zero-conormal singleton partition is vacuous and has full column rank because each component indicator is nonzero and these columns are independent.

**V-UC005 PASS Theorem UC4.1 with positive fixed weights and exact conormal orientation.** Its conclusion is about a genuine directional *convolutional* heat model; it is not a statement about the original105 scalar multiplication edges.

## 3. A-UC005 — hostile graph, partition and complete-span tests

The graph with edge $(1,2)$ and isolated vertex3 is disconnected but has component matrix for partition $\{\{1,3\},\{2\}\}$ equal to $\left(\begin{smallmatrix}1&1\\1&0\end{smallmatrix}\right)$, determinant $-1$. Thus blanket rejection of disconnected graphs for **every chosen** partition would be false. The same graph fails the full-collision one-block partition, whose incidence row is $(2,1)$ and has rank one instead of two. Both conclusions are reproduced by the exact fixture.

For the four-vertex graph with edges $(1,2),(3,4)$ and crossing partition $\{\{1,3\},\{2,4\}\}$, the incidence matrix has two identical rows $(1,1)$ and rank one. Component constants $(1,-1)$ produce covector $(1,1,-1,-1)$, which obeys both crossing block-sum equations and is killed by both heat edge directions. This explicitly shows why testing whether each heat edge is nonzero on one chosen conormal generator is not the same as full-rank testing of the entire conormal space.

The all-partitions corollary is tested by the **full collision partition**, which is present in the original collision arrangement. It has only one row and rank one, so any graph with at least two connected components necessarily fails. Conversely a connected graph has one nonzero incidence column for every partition, hence full column rank. This establishes the if-and-only-if without requiring graph completeness or positive lower bounds uniform in edge weights approaching zero.

**A-UC005 PASS Examples UC4.2–UC4.4 and Corollary UC4.5.** The witness is a characteristic direction for convolutional heat smoothing, not evidence that the original108 legal partition insertion is an illegal source or that a different scalar/Wick history cannot represent the same evaluated family.

## 4. Source-stage boundary and independent attack on overreach

| Inference | Review |
| --- | --- |
| Exact integer matrix rank decides heat-normal ellipticity for one fixed graph and partition | ACCEPT |
| Graph connectedness is equivalent to passing **all** collision partitions for directional convolutional heat | ACCEPT |
| A disconnected graph fails every individual partition | REJECT, actual passing counterexample |
| Positive heat weights can be arbitrarily varied without losing a uniform ellipticity constant | REJECT; rank is invariant for strictly positive weights but quantitative constant may degenerate |
| The heat edge directions in this graph are automatically original105 scalar multiplication factors | REJECT; different operators and no factorization was proved |
| Rank passing automatically constructs a fixed original105 PHG stage across all collision corners | REJECT; full fixed-index and remainder estimates are absent |
| Rank passing on the ambient conormal implies a full original108 Green source operator for tangent R1, all partition jets and126 parameter rows | REJECT; the source-level maps, density, index control and completion have not been supplied |
| Exact fixture run certifies analytical microlocal theorem externally | REJECT; OS-only arithmetic regression, same-system mathematical review |
| Universal150.L, residual W acyclicity, originalR3, full126.14, higher weights and M5/R4 | OPEN |

This review preserves the useful separation: a rank-passing incidence matrix is a **preflight necessary gate and sufficient conormal-ellipticity test for the stipulated directional convolution**, not a certificate of source membership or of a general homotopy/Green inverse. Passing it authorizes no scalar105 source enlargement or new completed108 operation.

## 5. Final bounded decision and next research

**BOUNDED ACCEPT of exact primary UC004 Git blob d9d5698d3de3729fbc33dfd539ed9c9c22b9a1f3 with zero mathematical author corrections.** The exact rational fixture has six groups PASS and an authenticated OS-only receipt; the printed tests do not replace the mathematical proof.

The next genuinely source-level obligation is to take an actual rank-passing original105/108 **factorized** Gaussian history and prove all-corner fixed scalar index/remainder estimates, legal R1/partition inclusion maps, physical density continuity through completion and source-controlled126 rows. If such a history cannot be made source-legal, identify the exact failed stage or conormal and produce a corrected theorem or counterexample. Original universal150.L, W and R3 remain OPEN. This review is not external certification, and protected admission/readback of UC004/005/006 remains a separate gate.
