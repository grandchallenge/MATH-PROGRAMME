# EXT-015 REACH / UC-OP-004 — finite Gaussian heat graphs and collision-partition incidence

**Primary disposition: EXACT FINITE GRAPH/PARTITION RANK CLASSIFICATION within directional convolutional heat models.** For a finite graph of heat-diffusion directions on physical vertex coordinates, the ellipticity gate of protected UC-OP-001 on a collision partition is equivalent to full column rank of one integer matrix counting vertices in intersections of the graph's connected components with the partition blocks. This gives exact positive cases, legal failure witnesses and a finite test for every collision partition, without constructing a new original105 all-corner scalar stage or a general completed108 source Green operator.

## 1. Original source lock and restricted model

Use original105 scalar collision stages (Git blob a8ce66ff0edec33e2aff299550fca2089d671033), original108 complete mixed coefficient histories/partition inclusions (Git blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6), and original126 parameter-row contract (Git blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163). The specific conic first Green core A/D is protected in corrected [195](JOINT_DEFECT_SOURCE_AUDIT_195.md), Git blob fc0fddb678f0cc0c1b9764bb449ab6d9150b33d0, with critical196 blob 6c9607eb3db55153e999587e6546931244ef2150 and PR3371 merge 1d741353367997f51d0789ad7049ded1c0712c9e.

Protected [UC-OP-001](UNIFORM_CONIC_GREEN_OPERATOR_AUDIT_UC001.md), primary blob 437d40de4a1a5a723cb49bcf31f0190df1fda0b5, [critic UC002](AGENT_CRITICAL_REVIEW_UNIFORM_CONIC_UC002.md) blob 948bfc32d186ea63c3543e7a5d2bad17bfd3c5b4, and [ledger UC003](UNIFORM_CONIC_ACCEPTANCE_UC003.md) blob f78c82800d3850543591d8106d27911aa3b2bb34, native PR3376 merge ce828643ec7cf2e001ab068e578daf4befb91fbb, establish that an actual *directional convolutional* Gaussian has positive-interior conic smoothing exactly on cones avoiding its heat-normal kernel. The legal nonidentity partition counterexample shows one heat direction need not regularize every conormal. CP223 custody transition in PR3377 remains separate from the mathematical calculation here and must be verified before the next promotion.

Here we study only finite **convolutional** heat directions $e_i-e_j$ on independent real vertex variables $(x_i)_{i=1}^n$, with positive fixed weights $a_{ij}$. Nothing in the proof identifies a scalar **multiplication** edge of original105 with such a convolution, or automatically constructs a scalar105 all-corner heat source after a conic Fourier split.

## 2. Graph kernel and a collision-partition conormal

Let $G=(V,E)$ be a finite undirected graph, $V=\{1,\dots,n\}$, whose edge directions are $v_e=e_i-e_j$. Let $L:\mathbb R^n\to\mathbb R^E$ have rows $\sqrt{a_e}(e_i-e_j)^T$, where $a_e>0$. Its Gaussian heat multiplier has quadratic form

$$
E_G(\zeta)=\|L\zeta\|_2^2
=\sum_{(i,j)\in E}a_{ij}(\zeta_i-\zeta_j)^2.
\tag{UC4.1}
$$

Let $H_1,\dots,H_k$ be the connected components of $G$, including isolated vertices. Exactly

$$
\ker L
=\left\{\zeta:\ \zeta_i=c_h\ \text{for all }i\in H_h,
\quad h=1,\dots,k\right\}.
\tag{UC4.2}
$$

This follows from positivity of weights: $L\zeta=0$ precisely when $\zeta_i=\zeta_j$ for every graph edge, and hence when $\zeta$ is constant on each connected component. The resulting $k$ component-indicator vectors are linearly independent, so $\dim\ker L=k$.

Let $P=\{B_1,\dots,B_b\}$ be an arbitrary partition of the same vertex set, representing the collision diagonal

$$
\Delta_P=\{x:\ x_i=x_j\text{ whenever }i,j\in B_\alpha\}.
\tag{UC4.3}
$$

Its annihilator (the *normal covector space*) is

$$
C_P=N^*\Delta_P
=\left\{\zeta:\sum_{i\in B_\alpha}\zeta_i=0
\quad\text{for }\alpha=1,\dots,b\right\}.
\tag{UC4.4}
$$

The $b$ block-sum equations are linearly independent; therefore $\dim C_P=n-b$. The partition with $n$ singleton blocks has $C_P=\{0\}$ and is automatically elliptic on its vacuous conormal, regardless of graph topology.

## 3. Exact integer intersection-matrix theorem

Define the $b\times k$ **partition/heat-component incidence matrix**

$$
M_{P,G}=(m_{\alpha h}),\qquad
m_{\alpha h}=|B_\alpha\cap H_h|\in\mathbb N_0.
\tag{UC4.5}
$$

**Theorem UC4.1 (exact graph/partition heat-normal gate).** The following are equivalent:

1. The directional Gaussian energy $E_G$ is strictly positive on every nonzero conormal in $C_P$.
2. $\ker L\cap C_P=\{0\}$.
3. The integer matrix $M_{P,G}$ has full column rank $k$ over $\mathbb Q$ (equivalently $\mathbb R$).

If these conditions hold, then the restriction $E_G|_{C_P}$ has a uniform positive quadratic lower bound on the unit conormal sphere, with constant depending on the fixed graph weights and partition. If they fail, every nonzero rational $c\in\ker M_{P,G}$ gives an explicit nonzero real conormal witness $\zeta_i=c_h$ on $H_h$ with $E_G(\zeta)=0$.

**Proof.** By UC4.2, any $\zeta\in\ker L$ has unique component constants $(c_h)_{h=1}^k$. The block sum over $B_\alpha$ is

$$
\sum_{i\in B_\alpha}\zeta_i
=\sum_{h=1}^k|B_\alpha\cap H_h|c_h
=(M_{P,G}c)_\alpha.
\tag{UC4.6}
$$

Thus $\ker L\cap C_P$ is linearly isomorphic to $\ker M_{P,G}$. It is zero exactly when this matrix has full column rank. Rational and real rank agree for an integer matrix; rank failure yields a rational nonzero kernel vector by rational row reduction. The energy vanishes exactly on $\ker L$ and, on the compact unit sphere of $C_P$, has a positive minimum precisely when their intersection is zero. This proves all statements, including the explicit witness and the vacuous $C_P=\{0\}$ case. $\square$

There is no numerical conditioning assumption in the rank test: any positive $a_e$ leave $\ker L$ unchanged, though the **quantitative** elliptic constant can become small when a positive weight approaches zero. A parameter family with weights degenerating to zero would require its own uniform constant and source-stage analysis.

## 4. Exact controls and the global all-partition consequence

**Example UC4.2 (connected graph).** If $G$ is connected then $k=1$. The single column of $M_{P,G}$ contains positive block sizes $|B_\alpha|$, so it has rank one for *every* partition. Hence connected directional heat graph smoothing is conormal-elliptic on **every** collision partition of the same vertex set, as an ambient heat convolution, with a uniform ellipticity constant across the finitely many partitions. The graph may be a tree: connectivity, not all-to-all edges, is sufficient for this rank property.

**Example UC4.3 (disconnected graph that still passes a chosen partition).** Let $G$ have one edge $(1,2)$ and vertex $3$ isolated: components $H_1=\{1,2\}$ and $H_2=\{3\}$. For $P=\{\{1,3\},\{2\}\}$,

$$
M_{P,G}=\begin{pmatrix}1&1\\1&0\end{pmatrix},
\qquad\det M_{P,G}=-1.
\tag{UC4.7}
$$

Thus this **particular** conormal passes the heat-normal gate despite disconnected heat graph topology. Connectivity is not necessary for a selected partition. A universal rule that rejects every disconnected graph for every partition would discard legal positive cases.

**Example UC4.4 (two disconnected heat components and a crossing collision).** Let $H_1=\{1,2\}$, $H_2=\{3,4\}$ and heat edges $(1,2),(3,4)$. For crossing partition $P=\{\{1,3\},\{2,4\}\}$,

$$
M_{P,G}=\begin{pmatrix}1&1\\1&1\end{pmatrix},
\qquad c=(1,-1)^T,\qquad
\zeta=(1,1,-1,-1).
\tag{UC4.8}
$$

This $\zeta$ is simultaneously conormal to the crossing partition and killed by both heat directions. Positive Gaussian smoothing along these two edges therefore fails to smooth this conormal at every positive regulator. It is an exact structural characteristic witness, not a claim that the corresponding original108 partition inclusion is illegal.

**Corollary UC4.5 (ellipticity on all collision partitions).** The finite heat graph is heat-normal elliptic on every collision-partition conormal **if and only if the graph is connected**.

**Proof.** The connected implication is Example UC4.2. Conversely take the full collision partition $P=\{V\}$. Its incidence matrix is one row $(|H_1|,\dots,|H_k|)$, of rank one. If $k>1$ it cannot have column rank $k$. Theorem UC4.1 gives a nonzero conormal with zero heat energy. $\square$

The exact formula also shows that testing only one generator of a multi-dimensional partition conormal is insufficient. Row rank must be computed on the entire integer matrix, as required by protected UC001.

## 5. Actual finite regression, source-stage and governance boundary

The exact rational control [heat_graph_partition_rank_uc004.py](../../../fixtures/algebraic/heat_graph_partition_rank_uc004.py) takes graph edges and arbitrary set partitions, constructs connected components and the integer matrix UC4.5, computes rational matrix rank and an optional rational null witness, and tests connected/singleton, disconnected passing, full collision obstruction, crossing collision obstruction and positive graph-weight independence. These are finite arithmetic tests, not empirical evidence of new scalar105 corner estimates.

A partition/graph incidence matrix is a compact **preflight filter** for a proposed directional convolutional heat factorization. It is not a substitute for the main remaining original-source obligations: actual factorization of Gaussian/Wick scalar **multiplication** histories, noncharacteristic R1 coefficient insertion/restriction for all partition jets, fixed scalar105 all-face index families and recursive weighted remainder estimates, proper physical pushforward densities, completed108.6 source tensor bounds, and original126.6 parameter rows. In particular, a connected heat graph guarantees a positive-interior smoothing direction on every collision conormal, but does **not** by itself construct a universal original108 Green source operator or a contractible residual $W$.

| Question | Bounded verdict |
| --- | --- |
| Exact heat-graph incidence/rank characterization for a chosen partition conormal | PROVED as finite rational theorem UC4.1 |
| Connected graph covers all partition conormals for directional Gaussian convolution | PROVED as an ambient rank property |
| Disconnected graph fails every partition | FALSE, explicit passing UC4.3 |
| Disconnected graph can miss a crossing or full-collision conormal | PROVED, explicit witnesses UC4.4–UC4.5 |
| Same assertions for arbitrary scalar Gaussian **multiplication** source histories | OPEN; no factorization supplied |
| Complete scalar105 PHG source map or universal original108 Green inverse | OPEN |
| Universal150.L, residual W acyclicity, originalR3, full126.14, higher weights and M5/R4 | OPEN |

This is one primary UC004 candidate, requiring exact source-locked adversarial critic UC005, bounded ledger UC006, fresh CI and native protected admission. Its result is exact on the stated graph/convolution model only; it does not assert an independent external mathematical certification or terminal REACH closure.
