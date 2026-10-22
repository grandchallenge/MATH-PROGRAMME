# Erdős #41 — Uniform future containers and forced occupied windows

**19 October 2026. Disposition:** rigorous, alignment-free **order $k\log R$ entropy loss** for all future B3 batches and a proved **forced populated-window extraction** under hypothetical persistent critical density. The results **do not** force a true maximum-cardinality deficit, exclude a critically populated batch, or settle Erdős #41. Mathematical originality and protected admission remain separate.

## 1. Old-pair-sum constraints apply to *any* future interval

Let P⊂[1,R] be a finite repeated-summand B3 set with n=|P|>=5, and let

$$
Q=\{a+b:a,b\in P,\ a\le b\},\quad q=\binom{n+1}{2}.
$$

Define the undirected difference graph G(P;J) on the integer positions of **any interval J containing exactly R integers**, with an edge {x,x'} whenever x−x'∈(Q−Q)\{0}. If X⊂J is disjoint from P and P∪X is B3, **X is independent in this graph**: otherwise q+x=q'+x' are equal sums of distinct unordered triples of type PPX. No reflected anchor is necessary.

We use the previously proved difference multiplicity property

$$
r_Q(d)=|\{(q,q')\in Q^2:q-q'=d\}|\le n\quad(d\ne0).
$$

For every subset U⊂J of m positions, counting overlaps among all translates Q+x, x∈U, in at most 3R integer positions gives

$$
\boxed{
e(G(P;J)[U])\ge
\frac1{2n}\left(\frac{m^2q^2}{3R}-mq\right).
}\tag{HEREDITARY-OVERLAP}
$$

This is translation-invariant in J. It is valid for *every* induced vertex subset U, including sets produced adversarially by deleting high-conflict sites and optimizing the remaining batch.

Assume 0<c<=1 and n>=cR^(1/3), and put

$$
\delta=\frac{c^3}{48},\qquad
s=\min\left(R,\left\lceil\frac{6R}{q}\right\rceil\right).
$$

For every induced U with |U|>s, the factor mq/(3R)>2, and the preceding inequality gives

$$
\boxed{e(G[U])\ge\delta|U|^2.}\tag{HEREDITARY-SUPERSATURATION}
$$

Every induced graph above size s therefore has a vertex of degree at least 2δ|U|. Note s<=12c^(−2)R^(1/3)+1: the critical scale now enters as the size at which the *hereditary* collision graph can stop being dense.

## 2. Exact deterministic greedy containers, not a random-graph analogy

**Theorem A (fingerprint/container lemma).** Let G be any graph with R vertices such that every induced subset of more than s vertices spans at least δ times the square of its cardinality in edges, with 0<δ<1/2 and s>=1. Let

$$
t=\left\lceil\frac{\log(R/s)_+}{-\log(1-2\delta)}\right\rceil,
\qquad \log(x)_+=\max(0,\log x).
$$

Then every independent set I of G has an injective description by:

1. a subset of at most t **iteration indices** from {1,...,R}, recording the selected vertices in a canonical greedy procedure, and
2. an arbitrary subset of a residual vertex set of size at most s, determined by those indices.

Consequently,

$$
\boxed{
i_k(G)\le\sum_{j=0}^{\min(k,t)}
\binom Rj\binom s{k-j},
\qquad
\sum_{k=0}^R i_k(G)
\le2^s\sum_{j=0}^t\binom Rj
\le2^s(t+1)R^t.
}\tag{ALL-INDEPENDENT-CONTAINERS}
$$

**Proof.** Maintain an available vertex set U, initially V(G), and a selected fingerprint. While |U|>s and fewer than t vertices have been selected, choose the **deterministically tie-broken maximum-degree vertex** v of G[U]. If v∈I, record the current iteration index and remove v together with all its neighbors; otherwise remove v alone. Because I is independent, no member of I is accidentally removed. When a vertex v∈I is selected, the hereditary supersaturation hypothesis implies deg_U(v)>=2δ|U|, so |U| is multiplied by at most 1−2δ. After t selections |U|<=s, so the process stops (possibly earlier). All previously unselected vertices of I remain in the final U.

Given the set of iteration indices corresponding to selected vertices, the entire deterministic procedure—including its stopping state, chosen vertices, and final U—is reproducible without knowing I. The residual I∩U is then a subset of at most s vertices. Thus the encoding is injective, and counting fingerprints and residual choices gives the formulas. This argument controls the number of **complete integral independent sets** of *every size*, not merely their random expected collisions. QED.

**Theorem B (order $k\log R$ future entropy penalty).** For any P⊂[1,R] satisfying the B3 and density hypotheses, and *any future interval J of exactly R integers disjoint from P*, let $\mathcal E_k(P,J)$ denote all k-subsets X⊂J for which P∪X remains B3. With q,s,t,δ above,

$$
\boxed{
|\mathcal E_k(P,J)|
\le\sum_{j=0}^{\min(k,t)}
\binom Rj\binom s{k-j},
\qquad
\sum_k|\mathcal E_k(P,J)|\le2^s(t+1)R^t.
}\tag{FUTURE-CONTAINERS}
$$

These bounds are uniform over all possible shape-changing choices for X and remain valid with additional disjoint earlier elements outside P (which can only remove extensions).

If n>=cR^(1/3), then s=O_c(R^(1/3)) and t=O_c(log R). Hence

$$
\boxed{
\log\sum_k|\mathcal E_k(P,J)|
=O_c(R^{1/3}+(\log R)^2)=O_c(R^{1/3}).
}\tag{STRONG-ENTROPY}
$$

For k in [ηR^(1/3),MR^(1/3)] with fixed η,M>0, log binom(R,k)=(2/3)k log R+O_(η,M)(k), while

$$
\boxed{
\log|\mathcal E_k(P,J)|\le O_c(k+(\log R)^2)=O_(c,η,M)(k).
}\tag{LOG-ENTROPY-GAP}
$$

Thus the deficit relative to all unrestricted k-subsets is **(2/3+o(1))k log R**, not merely the previous constant times k. This is the stronger integrality-dependent entropy loss sought. There is no contradiction: exp(O_c(k)) is still extremely large, so nonempty B3 extensions of critical cardinality are not excluded.

The associated deterministic alpha bound follows already from the translate counting: if X is independent, all q translates Q+x are disjoint inside 3R positions, so

$$
\boxed{|X|\le3R/q\le6R/n^2=O_c(R^{1/3}).}\tag{CRITICAL-ALPHA-CAP}
$$

This is **critical order**, not little-o of R^(1/3). An entropy theorem cannot alone improve that order.

## 3. Density actually forces some future windows — without any arithmetic alignment

The earlier staged counting argument had a genuine gap: it prescribed window locations that critical prefix density need not fill. The following extraction repairs *that portion* of the argument, without pretending that a count of extension possibilities forces impossibility.

**Theorem C (forced populated future window).** Assume hypothetically that an infinite B3 A obeys A(N)>=cN^(1/3) for every sufficiently large N, 0<c<=1. Put C0=18^(1/3) and select any fixed integer Λ>=2 satisfying

$$
c\Lambda^{1/3}\ge 2C_0.
$$

For every sufficiently large integer R, partition the annulus (R,ΛR] into the Λ−1 disjoint consecutive intervals of **exactly R integers**:

$$
J_i=(iR,(i+1)R]\cap\mathbb Z,\quad 1\le i<\Lambda.
$$

The prefix P=A∩[1,R] contains n>=cR^(1/3) elements, while cubic B3 packing gives |P|<=C0R^(1/3). Therefore

$$
|A\cap(R,\Lambda R]|
\ge(c\Lambda^{1/3}-C_0)R^{1/3}
\ge C_0R^{1/3}.
$$

Some future interval J_i contains at least

$$
\boxed{
k_i=|A\cap J_i|\ge\eta_cR^{1/3},
\qquad
\eta_c=\frac{C_0}{\Lambda-1}>0.
}\tag{FORCED-POPULATED-WINDOW}
$$

**Proof.** The difference of counting-function bounds gives the total annular mass, and the pigeonhole principle supplies one of the Λ−1 windows. No block alignment, middle anchor, residue class, short-gap smoothness, or fixed bin occupation is assumed. QED.

For this *actually occupied* J_i and actual old P, Theorem B gives the strong bound

$$
\boxed{
\#\{X\subseteq J_i:|X|=k_i,\ P\cup X\text{ is B3}\}
\le\exp(O_c(R^{1/3})),
}\tag{FORCED-WINDOW-COUNT}
$$

because the true k_i is at most C0R^(1/3) by local triple-sum packing and at least η_cR^(1/3). The unrestricted number of subsets of that size is exp((2/3+o(1))k_i log R).

This proves **both**: (i) a substantially larger entropy loss of order k log R, and (ii) its application to *a future interval guaranteed to be populated by every hypothetical c-persistent B3 set*. It does **not** prove a shortage of cardinality or any density valley; the count exp(O_c(R^(1/3))) leaves many possibilities.

## 4. Exact multiscale extension-tree corollary (forced locations but only conditional entropy)

For a geometrically increasing sequence of checkpoints R_j (e.g. R_j=Λ^j R_0), the preceding extraction supplies, **along each actual hypothetical persistent-density B3 chain**, an index i_j in {1,...,Λ−1} and a populated future batch X_j=A∩J_(j,i_j), with cardinality k_j>=η_cR_j^(1/3).

At a fixed checkpoint and conditional on the *entire actual previous chain*, the number of compatible possible choices for this populated batch is at most exp(O_c(R_j^(1/3))), by Theorem B. If the batch-selection windows are made disjoint by using R_(j+1)>=ΛR_j, then these are separately owned future selections and the **conditional logarithmic extension-choice budget is additive**:

$$
\boxed{
\log(\text{number of choices for the prescribed sequence }i_j,k_j
\text{ along a fixed compatible chain})
\le O_c\!\left(\sum_jR_j^{1/3}\right).
}\tag{MULTISCALE-FORCED-ENTROPY}
$$

More precisely, this is a uniform product bound on **the stagewise tree of compatible choices at the chosen windows**, with previous full prefixes fixed. No claim is made that these partial batches alone specify the entire underlying B3 set: elements in skipped locations may vary, and summing over them may increase the number of full histories. Indices and possible batch sizes add at most O_c(h log R_h) bits, but no global counting theorem about all B3 prefix histories follows without tracking these other elements.

**Limit of the new achievement:** the forced windows can be counted with an order $k\log R$ entropy discount, but positive entropy exp(O_c(k)) remains. The potential conjectural remedy is **cross-window incompatibility among the remaining fingerprints or reciprocal signed-code survivors**, not stronger first-moment packing.

## 5. Next precise gap

To solve Erdős #41 one would need to show that no sequence of the remaining containers can stay populated at every large scale, or that additional cross-window signed-sum constraints force the total compatible capacity below the required η_cR^(1/3). The proven container size s≈R^(1/3) is still at the critical threshold, so independent sets of the required size are not excluded by these arguments.

A sufficient next lemma would force, from the entire earlier history, a container of size **o_c(R^(1/3))** at one of the guaranteed occupied windows; that would contradict the forced lower occupancy. A weaker enough alternative is a bounded potential that cannot be replenished over all scale-owned windows. Neither statement is presently established, and Erdős #41 remains OPEN.

Mathematics is at research status pending independent specialist review. Primary GCL docket #2622; public problem status at https://www.erdosproblems.com/41.
