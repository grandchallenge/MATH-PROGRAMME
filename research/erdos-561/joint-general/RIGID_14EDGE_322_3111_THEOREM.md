# Erdős #561 — exact 15-edge joint residual, 322 versus 3111

**Date:** 2026-11-21. **Claim:** paper-level proof UNDER_REVIEW. This resolves one 3-by-4 strict-switching residual case for *all finite simple host graphs*. It does not prove the unrestricted joint-residual conjecture or Erdős #561. All star forests are vertex-disjoint unions of ordinary non-induced positive-edge stars.

For a list $a$ of positive integers write $F(a)$ for the disjoint union of stars with edge counts in $a$. The arrow $G\to(R,B)$ means every red/blue edge-colouring of $G$ has red $R$ or blue $B$.

## Theorem

Every finite simple graph satisfying BOTH

$$
G\to(F(2,2),F(3,1,1,1))
$$

and

$$
G\to(F(3,2,2),F(1,1,1))
$$

has at least 15 edges. Equality is achieved by $F(4,4,3,2,2)$.

Thus the minimum joint-residual host size for original star profiles $n=(3,2,2)$ and $m=(3,1,1,1)$ is **15**. Their antidiagonal tail is $(4,4,3,2,2)$; the two separate residual antidiagonals are $(4,4,2,2,2)$ and $(3,3,3,2,2)$ with sums 14 and 13.

## Lemma 1: universal two-vertex deletion

If $G\to(F(3,2,2),F(1,1,1))$, then for *every distinct* $x,y\in V(G)$, the graph $G-\{x,y\}$ contains $F(3,2,2)$, a forest with seven edges on ten nonisolated vertices.

**Proof.** Colour every edge incident with either $x$ or $y$ blue and all other edges red. The blue edges have the vertex cover $\{x,y\}$, so cannot contain a three-edge matching. Therefore the red remainder contains the stated forest. In particular $v_+(G)\ge12$ when $x,y$ are chosen nonisolated, and $e(G-\{x,y\})\ge7$. QED.

## Lemma 2: one-star deletion and a ten-edge threshold

If $G\to(F(2,2),F(3,1,1,1))$, then

$$
G-v\to(K_{1,2},F(3,1,1,1))
$$

for every vertex $v$. Indeed, from a violating colouring of $G-v$ colour all edges at $v$ red. A red $F(2,2)$ would need a two-edge red star entirely in $G-v$, which is forbidden, while no new blue edges have been added.

Every graph $H\to(K_{1,2},F(3,1,1,1))$ has at least ten edges: the all-blue colouring forces an $F(3,1,1,1)$ with six edges; select one edge from each of its four disjoint components and colour those four edges red, colouring all others blue. Red is a matching, so arrowing forces a further, edge-disjoint blue six-edge forest. Therefore $e(H)\ge4+6=10$. QED.

Consequently, for any hypothetical 14-edge joint host, every vertex has degree at most four.

## Lemma 3: a subcubic saturated-matching theorem

**Statement.** If a finite simple graph $H$ has maximum degree at most three and **at most seven degree-three vertices**, it admits a matching meeting every degree-three vertex. Equivalently its edges can be coloured red/blue with red degree at most one and blue degree at most two.

**External input and exact scope.** Apply the *ordinary* Lovász $(g,f)$ factor theorem, using

$$
g(v)=\max(0,d(v)-2),\qquad f(v)=\min(1,d(v)).
$$

A $(g,f)$ factor is precisely the required matching. The ordinary theorem states that a factor exists iff, for every disjoint vertex sets $S,T$,

$$
A=f(S)+\sum_{v\in T}\min(2,d(v))-e(S,T)\ \ge\ q(S,T),
$$

where $q$ counts connected components $C$ of $H-(S\cup T)$ on which $g=f$ everywhere and $f(C)+e(C,T)$ is odd. The clause is **$e(C,T)$**; do not substitute another factor theorem. The source-locked classical input is documented in \`research/erdos-561/formal-graph/LOVASZ_CAP_PARTITION_BRIDGE.md\`.

**Proof.** Suppose some $S,T$ violate the inequality, so the integer $A<q$. Set $U=V(H)\setminus(S\cup T)$. Using $3f(v)\ge d(v)$ and $3\min(2,d(v))\ge2d(v)$ for degrees at most three, expand the degree sums and cancel the $S$–$T$ edge contributions:

$$
3A\ge 2e(S)+4e(T)+e(S,U)+2e(T,U)\ge0.
$$

Thus $q\ge1$ and $0\le A\le q-1$. Every counted component with positive degree consists entirely of degree-three vertices; degree-zero components contribute even parity and are not counted. A counted component $C$ of size $r\le3$ has at least $3r-r(r-1)=r(4-r)\ge3$ edges to $S\cup T$, by simplicity and the fact that it is a component of $H[U]$. Call these components *small*.

If all $q$ counted components are small, the weighted boundary $e(S,U)+2e(T,U)$ is at least $3q$, contradicting $3A\le3(q-1)$. Hence there is a large counted component containing at least four cubic vertices. With at most seven cubic vertices in the whole graph, it is the **only** large counted component, and the other $q-1$ small ones contribute at least $3(q-1)$ to the weighted boundary. The displayed inequality and $3A\le3(q-1)$ now force the large component to have **zero** boundary to $S\cup T$. As a component of $H[U]$ it is consequently an isolated connected 3-regular component of the full graph. By the handshake lemma its order is even. Its parity test $f(C)+e(C,T)=|C|+0$ is therefore even, contradicting that it was counted by $q$. The ordinary factor theorem yields the matching. QED.

This is an ordinary analytic deduction from the published factor theorem, **not** a Lean formalization of that external result.

## Proof of the 15-edge lower bound

Suppose a joint host has at most fourteen edges. Adding disjoint isolated edges preserves both arrowing relations, so assume $e(G)=14$. Lemma 2 shows $\Delta(G)\le4$; the all-blue colouring in the first relation forces a degree-three vertex, so $\Delta(G)\in\{3,4\}$.

**Case $\Delta(G)=4$.** Choose a degree-four vertex $v$ and let $H=G-v$. Then $e(H)=10$ and by Lemma 2 the graph $H$ arrows $(K_{1,2},F(3,1,1,1))$. The all-blue colouring of this relation shows $v_+(H)\ge10$. For every $w\in H$, Lemma 1 applied to $v,w$ gives $e(H-w)\ge7$, hence $d_H(w)\le3$. If $k$ is the number of degree-three vertices of $H$, the handshake lemma gives

$$
20=2e(H)\ge3k+(v_+(H)-k)\ge10+2k.
$$

So $k\le5$. Lemma 3 supplies a red matching and a blue maximum-degree-two remainder in $H$; this colouring has neither red $K_{1,2}$ nor blue $F(3,1,1,1)$, a contradiction.

**Case $\Delta(G)=3$.** An edge partition with red maximum degree one and blue maximum degree two would avoid the *first* joint residual relation, since red $F(2,2)$ needs degree two and blue $F(3,1,1,1)$ needs degree three. Thus by Lemma 3, $G$ has at least eight cubic vertices. By Lemma 1, $v_+(G)\ge12$, so

$$
28=2e(G)\ge3\cdot8+(12-8)=28.
$$

Equality throughout forces exactly eight cubic vertices, exactly twelve nonisolated vertices, and the other four nonisolated vertices all of degree one. Choose a leaf $\ell$, its neighbour $x$, and some nonisolated $y\notin\{\ell,x\}$. Removing $x,y$ leaves at most ten of the original nonisolated vertices and makes $\ell$ isolated, leaving at most **nine** nonisolated vertices. This contradicts Lemma 1, which requires the ten-vertex forest $F(3,2,2)$ after deleting ANY two vertices.

Both cases contradict the joint hypothesis; $e(G)\ge15$. QED.

## Matching upper bound and reproducibility

The canonical disjoint-star host $F(4,4,3,2,2)$ has 15 edges. Its sorted star sizes dominate both residual antidiagonal lists coordinatewise, and the elementary star-host greedy Ramsey criterion in \`JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md\` proves that it arrows both conditions. Separately, \`verify_rigid14_322_3111.py\` enumerates **every one of 900 red-arm allocations** across its five star components and verifies both joint conditions in each allocation. The independent arithmetic section reproduces both antidiagonal index conventions. The finite upper check is not offered as an arbitrary-host proof.

## Boundaries

Claim: exact single 322/3111 joint residual value, paper-level UNDER_REVIEW. The source can be admitted under normal GCL protected policy without certifying the mathematics. No independent referee disposition or MATHCERT certificate follows automatically. The unrestricted s,t>=3 joint residual issue #3490 and the unrestricted original Erdős #561 conjecture remain OPEN/PARTIAL. The actual next unresolved mathematics is a universal coupled arbitrary-host lower bound recovering every antidiagonal switching surplus, or a certified counterexample to that proposed reduction.
