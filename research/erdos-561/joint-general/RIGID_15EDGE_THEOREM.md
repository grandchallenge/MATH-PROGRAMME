# Erdős #561 — exact 3-versus-4 joint residual family with equal leading stars

**Research date: 2026-11-20. Scope: unconditional mathematical subtheorem for arbitrary finite simple graph hosts, not unrestricted Erdős #561 or all of issue #3490.** Star components are positive-edge stars; embedding is ordinary non-induced and distinct forest components must have vertex-disjoint supports.

## Theorem 1 (an infinite exact joint-residual family)

For every integer `a≥4`, set `n=(a,2,1)` and `m=(a,1,1,1)`. The smallest number of edges of a finite simple graph `G` simultaneously satisfying

`G → (F(2,1), F(a,1,1,1))` and `G → (F(a,2,1), F(1,1,1))`

is exactly

$$
\boxed{3a+4}.
$$

The canonical disjoint-star host `F(a+1,a,a,2,1)` has exactly `3a+4` edges and satisfies both arrowing relations. This establishes the joint residual inequality in an **infinite family of arbitrary graph hosts** with positive switching surplus one.

More generally, **Theorem 2:** for any integers `a≥4` and `2≤b<a`, every finite simple graph simultaneously arrowing `(F(b,1),F(a,1,1,1))` and `(F(a,b,1),F(1,1,1))` has at least `3a+b+2` edges. When `b=2`, this is sharp and Theorem 1 results. For larger b, the conjectured antidiagonal value is `3a+2b`, so Theorem 2 improves the general peeling bound by one edge but is **not** a complete proof of that larger value.

## Proof of the stronger lower bound (Theorem 2)

Fix `a≥4`, `2≤b<a`, and suppose `G` satisfies both residual arrowing conditions. Put `N=a+b+1`.

**1. Every pair of deleted vertices leaves a full red forest.** For *every* set `S⊆V(G)` with `|S|≤2`, colour all edges incident with S blue and the remaining edges red. A graph whose edges are covered by at most two vertices cannot contain the three disjoint nontrivial blue edges of `F(1,1,1)`. The second residual arrowing condition therefore forces

$$
G-S\supseteq F(a,b,1),\qquad e(G-S)\ge N.
$$

In particular, after deleting any two vertices, at least one remaining vertex has degree at least `a`.

**2. Two independent high-degree centres are necessary.** The all-blue colouring in the *first* residual condition forces a blue `F(a,1,1,1)`, hence a vertex v of maximum degree `d≥a`. If no other vertex has degree at least `a` after deleting v, explicitly colour red every edge `vw` whose other endpoint had original degree at least a. Colour extra edges at v red until at least `d-a+1` incident edges are red, then colour all other edges blue. The red graph is a single star and avoids `F(b,1)`, which has two vertex-disjoint positive-edge components. The blue graph has maximum degree at most `a−1`, so it avoids the `a`-edge blue star, contradicting the first residual condition. Thus there exists u different from v with `d_(G-v)(u)≥a`.

Consequently

$$
e(G)\ge d_G(v)+d_{G-v}(u)+e(G-\{u,v\})\ge a+a+N=3a+b+1.
$$

(The displayed edge decomposition counts each edge exactly once.)

**3. Equality would force three disjoint saturated stars.** Suppose `e(G)=3a+b+1`. The preceding inequalities imply that `d_G(v)=a` is the global maximum, `d_(G-v)(u)=a`, and `e(G−{u,v})=N`. Since the maximum degree is a, vertices u and v cannot be adjacent. By step 1, the entire nontrivial remainder `G−{u,v}` consists of precisely `F(a,b,1)`. Let w be the centre of its a-edge star, let L be the a leaves of that star, and let P be the disjoint two-component forest `F(b,1)`.

The centre w already has original degree a, so it is adjacent neither to u nor to v. Delete `{w,u}`. Both are nonadjacent degree-a vertices, leaving exactly `e(G)−2a=N` edges. Step 1 forces a full `F(a,b,1)` using **all remaining edges**. Vertex v still has degree a, and because `b<a`, it is necessarily the unique centre of the a-edge star in this remaining forest. Its star must be vertex-disjoint from P. Therefore **no edge from v meets any vertex of P**. Interchanging u and v gives the same conclusion for u.

The only original degree-a vertices are now w,u,v. Indeed, every leaf of the original w-star has degree at most three (its edge to w and at most one edge to each of u,v), which is strictly less than a; P has maximum degree b<a and no incident edges from either hub; and any other new vertex has degree at most two (one possible edge to each hub). All three centres w,u,v are pairwise nonadjacent.

Suppose two of these saturated centres share a neighbour x. Delete x together with the **third** saturated centre. The first two centres lose one edge each; the third is removed; and all other original vertices had degree less than a. The remaining graph has maximum degree at most `a−1`, contradicting step 1, which forces an a-edge star after **every** deletion of up to two vertices. Thus the three saturated centres have pairwise disjoint neighbour sets.

It follows that G's nontrivial components are **exactly** three disjoint a-edge stars together with the untouched F(b,1):

$$
G \cong F(a,a,a,b,1)\quad\text{plus isolated vertices}.
$$

**4. Equality fails the first residual Ramsey relation.** In this disjoint-star graph, colour one edge in each of the three a-edge stars red and all remaining edges blue. The red graph is a matching and therefore has no b-edge star because `b≥2`; hence red avoids `F(b,1)`. Every blue degree is at most `a−1` (the unmodified b-edge component satisfies b<a), so blue avoids `F(a,1,1,1)`. This is an explicit colouring contradicting the first residual arrowing condition.

Hence equality at `3a+b+1` is impossible. Together with step 2, we conclude

$$
\boxed{e(G)\ge3a+b+2}.\qquad\text{QED (Theorem 2).}
$$

## Proof of sharpness for b=2 (Theorem 1)

For `n=(a,2,1)`, `m=(a,1,1,1)`, the corresponding antidiagonal weights excluding the first are

$$
(w_3,w_4,w_5,w_6,w_7)=(a+1,a,a,2,1).
$$

The canonical host `F(a+1,a,a,2,1)` therefore has `3a+4` edges and simultaneously arrows both residual forest pairs, by the standard elementary greedy characterization for disjoint-star hosts. For b=2, Theorem 2 gives the **identical** lower bound `3a+4`; hence the minimum is exact. **QED (Theorem 1).**

## Exact finite independent corroboration: a=4,b=2

For `(a,b)=(4,2)` a hypothetical 15-edge graph is forced to be a seven-plus-eight-edge construction: a fixed `F(4,2,1)` of seven edges plus two nonadjacent degree-four hubs. Its old vertices are labelled `0,...,9`, with original star edges `01,02,03,04,56,57,89`, and hubs `10,11`. The old centre 0 is saturated and cannot be a hub neighbour. Each hub may attach to at most four of old vertices `1,...,9`, and its remaining edges meet fresh private or shared new neighbours. Thus every possible equality graph is represented by two subsets A,B of `{1,...,9}` of size at most four, and `0≤h≤min(4−|A|,4−|B|)` new shared neighbours. This is a complete structural class of **84,653** descriptions, including non-star and cyclic graphs.

The source-controlled, independently implemented tests are:

- `verify_rigid15_exact.cpp`: independently enumerates every graph in this class; constructs ordinary vertex-disjoint star-forest embeddings; checks the necessary all-two-vertex-deletion condition for the second residual relation; and uses complete red/blue colouring checks in any surviving case. It reports **84,652 failures of the necessary second-residual deletion test** and exactly one survivor, which does not arrow the first residual relation.
- `verify_rigid15_structural.py`: independently enumerates all 84,653 configurations by Python combinations, using the **explicit mathematical reasons** of the proof rather than the C++ embedding code. Of the configurations, 84,025 violate the second residual by connecting a hub to the smaller F(2,1) remainder, 623 by connecting a hub to a leaf of the original four-star, and four by sharing a fresh new neighbour between hubs. Exactly one remains: the disjoint union F(4,2,1)+2K_(1,4), with the directly described A-avoiding colouring.

These two independent checks agree on the key conclusion: **the only graph that survives all necessary two-vertex deletion constraints does not satisfy both residual conditions**. The finite verification is supplementary: steps 1–4 already prove the infinite theorem for all a≥4, so no inference from finite data to unbounded graph hosts is being made.

## Claim boundary and next obstruction

The new theorem resolves `(4,2,1)` versus `(4,1,1,1)` at exactly **16 edges**, and infinitely many larger analogous pairs. The full joint-residual hypothesis for all s,t≥3 remains **OPEN/PARTIAL**, and neither the unrestricted size-Ramsey conjecture nor the paper-level original three-star residual transfer is certified here.

The next modest unresolved positive-switching example by conjectured edge count is `(3,1,1)` versus `(5,2,2,1)`, with proposed joint minimum **16** and current general lower bound **15**; this family has a different lower-component structure and is not covered by the three-saturated-centre proof. More ambitious examples with b>2 in Theorem 2 retain a gap `b−2` between the improved bound and proposed general joint count.
