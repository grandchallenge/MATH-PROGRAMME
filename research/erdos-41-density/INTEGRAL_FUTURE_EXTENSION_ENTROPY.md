# Erdős #41 — Integral future-batch entropy deficit

**18 October 2026. STATUS:** proved finite arithmetic and counting theorems, and a cumulative entropy deficit in a specified geometric B3 extension protocol. **NOT PROVED:** a decline in maximum future-batch cardinality, a general density dip, or Erdős #41. Source programme: issue #2622 and preceding forward-extension/shadow work.

## 1. A density-sensitive incompatibility graph on the full future position set

Let P be any repeated-summand B3 subset of [1,R], with n=|P|>=4. Write

$$
Q=\{a+b:a,b\in P,\ a\le b\},\quad q=|Q|=\binom{n+1}{2}.
$$

For d>0 let r_Q(d) be the number of pairs u,v∈Q with u−v=d.

**Lemma 1 (pair-sum difference multiplicity).**

$$
\boxed{r_Q(d)\le n\quad(d>0).}\tag{POINTWISE-CAP}
$$

**Proof.** If d=a_0−b_0 belongs to P−P, B3 uniqueness in u+b_0=v+a_0 forces u=a_0+t, v=b_0+t for a unique t∈P. Thus r_Q(d)=n. If d∉P−P, write u=a+b with a<=b and v=c+e. Suppose two different representations have the same chosen first element a. Then
a+b−c−e=a+b'−c'−e' gives b+c'+e'=b'+c+e. When b=b', B2 uniqueness makes both representations identical. Otherwise B3 equality of the triple multisets forces b∈{c,e} and b'∈{c',e'}. The remaining target elements agree, say t, and d=a−t∈P−P, a contradiction. Therefore at most one representation is assigned to each chosen a∈P, proving the cap. QED.

Partition the integer interval [2,2R] into four consecutive bins of lengths at most ceil(R/2). One bin contains at least q/4 of the q pair sums, and its positive differences are <=floor(R/2). Since q/4>=n²/8>=2, and binom(z,2)>=z²/4 for z>=2, the number of **distinct** short pair-sum differences is at least

$$
\boxed{
|\{1\le d\le\lfloor R/2\rfloor:d\in Q-Q\}|
\ge \binom{q/4}{2}/n\ge n^3/256.
}\tag{SHORT-DIFFERENCE-SUPPLY}
$$

The first displayed binomial expression at noninteger q/4 is shorthand for the valid real polynomial z(z−1)/2; the subsequent bound is what is used.

Let G_P(R) be the graph with vertices 1,...,R, where {t,u} is an edge whenever t−u∈Q−Q and t≠u. Each of the above short distances supplies at least R/2 distinct edges.

**Theorem 1 (arithmetic graph edge density):**

$$
\boxed{e(G_P(R))\ge n^3R/512.}\tag{GRAPH-DENSE}
$$

Consequently, if n>=cR^(1/3), the graph has at least epsilon_c R² edges, epsilon_c=c³/512. These bounds hold for **every** actual B3 prefix, with no alignment, mixing, or residue hypotheses.

### Why this graph controls the true future optimizer

Choose y>6R. Any actual k-element B3 extension X in the future interval J_y=[2y−R,2y−min(P)] has a reflected k-set T=2y−X⊂[min(P),R]. If P∪{y}∪X is B3, T **must be independent** in G_P(R). Otherwise distinct q,q'∈Q and t,u∈T satisfy q−q'=t−u≠0, giving equal three-sums of type PPX:
2y+q−t=2y+q'−u.
This uses actual **binary no-collision constraints**; no probability estimate substitutes for the B3 definition.

## 2. A universal integral entropy bound for every future batch shape

**Lemma 2 (dense-graph independent-set penalty).** Suppose a simple graph G on L vertices has e(G)>=epsilon L² with 0<epsilon<=1/4. For every integer 2<=k<=epsilon L,

$$
\boxed{
i_k(G)\le2e^{-\epsilon(k-1)/4}\binom{L}{k},
}\tag{INDEPENDENT-SET-ENTROPY}
$$

where i_k counts its k-element independent sets.

**Proof.** The total degree sum is at least 2epsilon L². Therefore at least epsilon L vertices have degree at least epsilon L. Call them high-degree. Uniformly sample an ordered k-tuple of distinct vertices and expose the first a=floor(k/2) elements. The probability that this half has no high-degree vertex is at most e^(−epsilon a). If there is such a vertex, at least epsilon L−a>=epsilon L/2 of its neighbors remain unexposed, since k<=epsilon L. The other b=k−a chosen vertices must avoid all of them for the full k-set to be independent. Conditional on the first half this occurs with probability at most e^(−epsilon b/2). Add the two cases and use a>= (k−1)/2 and b>=k/2 to obtain the displayed bound. QED.

**Theorem 2 (true B3 future-batch entropy deficit).** Let P⊂[1,R] be B3 with n>=max(4,cR^(1/3)); let y>6R; and put epsilon_c=c³/512. For every integer 2<=k<=epsilon_c R, the number N_k(P,y) of **complete and genuinely B3-compatible** future batches X⊂J_y of size k obeys

$$
\boxed{
N_k(P,y)\le
2e^{-\epsilon_c(k-1)/4}\binom Rk.
}\tag{COMPLETE-BATCH-COUNT}
$$

**Proof.** Reflect every actual X to an independent T in G_P(R) and apply Lemma 2. Any additional reciprocal signed-code restrictions further reduce N_k. The estimate holds for **all** optimally rearranged integral batches, not just random completions or a fixed future shape. QED.

Thus the logarithm of the number of permissible future choices is at least epsilon_c(k−1)/4−log 2 below the unrestricted binomial log capacity whenever that quantity is positive. For each fixed c,eta>0 and k>=eta R^(1/3), the bound becomes exponentially small as a fraction of all size-k candidates for sufficiently large R.

## 3. A rigorous cumulative deficit in an adaptive geometric extension protocol

Fix a B3 P_0⊂[1,R_0] with at least four elements. Put R_j=16^j R_0 and y_j=8R_j. At stage j choose an arbitrary future batch

$$
X_j\subseteq J_j=[15R_j,16R_j-\min(P_j)],\qquad |X_j|=k_j,
$$

and set P_(j+1)=P_j∪{y_j}∪X_j. Count only histories that remain B3, whose actual prefixes satisfy |P_j|>=cR_j^(1/3), and whose sizes obey 2<=k_j<=epsilon_c R_j. Each P_j lies in [1,R_j]; each X_j is disjoint from earlier stages and can **adapt to the entire preceding history**.

**Theorem 3 (multiscale integral entropy deficit).** For a fixed starting P_0 and sizes k_0,...,k_(h−1), the number of valid stage-h histories is at most

$$
\boxed{
\prod_{j=0}^{h-1}\binom{R_j}{k_j}
\exp\left(
-\frac{\epsilon_c}{4}\sum_{j=0}^{h-1}(k_j-1)+h\log2
\right).
}\tag{STAGED-CUMULATIVE-DEFICIT}
$$

**Proof.** Conditional on **each** admissible previous history, the old B3 prefix satisfies the hypotheses of Theorem 2. Hence it has at most 2exp(−epsilon_c(k_j−1)/4) binom(R_j,k_j) legal shape-changing future k_j-batches. Iterate the uniform branching bound along the tree. No probabilistic independence of histories is claimed. Each loss belongs to its own disjoint future selection stage, so this is a true additive loss of **logarithmic extension counts**, not repeated counting of the same representation. QED.

When k_j>=eta R_j^(1/3), the negative contribution to the log counting bound is Omega_(c,eta)(sum_j R_j^(1/3)), overcoming the h log 2 factor for large scales.

**EXACT LIMITATION:** The stated extension protocol is not forced by the density hypothesis in Erdős #41; an actual infinite B3 set may avoid these prescribed future windows. More fundamentally, log binom(R,k)=Theta(k log R) at critical k, while this theorem deducts only Theta_c(k). Thus exponentially **rare** batches can remain exponentially **numerous**, and the theorem says nothing about a universal decrease in the **maximum admissible batch size** C(P,J). It does not establish the critical-density valley.

## 4. The genuinely unresolved quantitative bridge

The previous first-moment fractional profile p_n=(1/4)n^(−2/3) is compatible with exact expected pair/triple packing at every resolution but is not an integral B3 set. Theorems 1–3 provide a genuine, *binary* penalty on complete extensions, uniform over old prefixes and future-batch rearrangements.

To complete #41 one still needs to upgrade the counting deficit to a **cardinality-capacity** obstruction, or derive a much stronger loss on actual future batches (for example Theta(k log R) rather than Theta(k) under a sequence of genuinely forced intervals), or prove a scale-owned potential exhausted by every persistent-density extension chain, regardless of its location. No such theorem is proved here. In particular the fact that a random critical batch almost surely contains collisions does not imply that an adversarially constructed critical B3 batch cannot exist.

Research docket #2622. The proof is submitted for independent GCL specialist review; this note does not certify originality or resolve Erdős #41. Public statement: https://www.erdosproblems.com/41.
