# Erdős #561 — a constructive unrestricted-host residual bound, and exact infinite families

**Research date: 2026-11-19. Disposition: `PARTIAL`, with unbounded proved subtheorems, not a resolution of the full joint-residual hypothesis.** All graphs in the theorems below are finite and simple. The stars have positive integer edge counts, subgraph containment is ordinary, and red/blue star-forest components must be vertex-disjoint. The two residual arrowing hypotheses are those of MATH-PROGRAMME issue #3490.

Let `n=(n1,...,ns)`, `m=(m1,...,mt)` be positive nonincreasing integer sequences, `s,t≥3`. Put `F(n)=⊔ K_(1,ni)`, `N=sum(ni)`, `M=sum(mj)`, and

$$
w_k(n,m)=\max_{i+j=k}(n_i+m_j-1),\qquad 2\le k\le s+t.
$$

The issue conjectures that if a finite simple `G` satisfies both

$$
G\to(F(n_2,\ldots,n_s),F(m))
\quad\text{and}\quad
G\to(F(n),F(m_2,\ldots,m_t)),
$$

then `e(G)≥J(n,m)`, where

$$
J(n,m)=\sum_{k=3}^{s+t} w_k(n,m).
$$

The standard antidiagonal star host has exactly `J` edges and satisfies both arrowing properties. The issue is whether **any arbitrary graph** with fewer edges might also satisfy both. We prove the exact star-host characterization and a **new lower bound for arbitrary simple graph hosts**, which is sharp for several nonuniform families with positive/unbounded switching surplus.

## Theorem A — exact simultaneous Ramsey characterization among star hosts

Let `H=⊔_{l=1}^r K_(1,h_l)` be a disjoint union of nontrivial edge-stars, with `h1≥h2≥...≥hr≥1`. For any two star-forest targets with lengths `p,q≥1`, write their antidiagonal edge weights `u_1,...,u_(p+q−1)` (so `u_l=max_{i+j=l+1}(a_i+b_j−1)`). Then

**`H→(F(a),F(b))` if and only if `r≥p+q−1` and `h_l≥u_l` for every `1≤l≤p+q−1`.**

**Necessity.** If `r<p+q−1`, colour the first `min(p−1,r)` entire stars red and the rest blue. Neither colour has enough different nontrivial connected components for its target. Otherwise suppose some `h_l<u_l`; choose indices `i,j` with `i+j=l+1` and `u_l=a_i+b_j−1`. Colour the first `i−1` host stars entirely red and the next `j−1` entirely blue. In every remaining host star, choose at most `a_i−1` red edges and at most `b_j−1` blue edges; this always partitions its edges since `h_k≤h_l≤a_i+b_j−2`. The red graph has fewer than `i` component-stars with at least `a_i` edges, so cannot contain `F(a)`. The blue graph similarly has fewer than `j` component-stars of at least `b_j` edges, so cannot contain `F(b)`. Thus arrowing fails.

**Sufficiency.** Given any edge two-colouring, start with target indices `i=j=1`. At host component `l=i+j−1`, its edge count is at least `a_i+b_j−1`. If it has at least `a_i` red edges, reserve that component as the next red star and increment `i`; otherwise it has at least `b_j` blue edges, so reserve it as the next blue star and increment `j`. This takes at most `p+q−1` steps before `i=p+1` or `j=q+1`. Reserved host components are vertex-disjoint, so the corresponding complete monochromatic forest appears. **QED.**

**Joint residual corollary.** The antidiagonal weights of the two residual pairs are `a_l`, `b_l` for `l=1,...,s+t−2`. Every pair of original indices with sum at least three has `i≥2` or `j≥2`, so

$$
\max(a_l,b_l)=w_{l+2}(n,m).
$$

Therefore **a disjoint-star host satisfies both residual arrowing conditions iff its sorted edge counts coordinatewise dominate `w3,...,w_(s+t)`**, with at least `s+t−2` components. Its edge count is at least `J`, and equality forces precisely the canonical antidiagonal star list up to isomorphism and isolated vertices. This proves the issue's inequality among **all** disjoint-star hosts for arbitrary `s,t`, not for arbitrary graphs.

## Theorem B — iterative two-hub peeling bound for arbitrary graphs

Suppose `s≥3` and `t≥4`. Put `a=n1`, `b=m1`, `N=sum(ni)`. If **any finite simple graph** arrows both residual pairs, then

$$
\boxed{e(G)\ge 2b+N+(t-4)a.}
$$

Equivalently: if `e(G)<2b+N+(t−4)a`, we can explicitly construct a red/blue colouring avoiding one of the two required residual pairs.

### Proof

For any set `S` of at most `t−2` vertices, colour all edges incident with `S` blue and all other edges red. The blue graph has vertex cover `S` and therefore cannot contain the `t−1` **vertex-disjoint nontrivial stars** of `F(m2,...,mt)`: each would require a different vertex of `S`. Since the graph arrows the second residual pair, its remaining red edges must contain `F(n)`. In particular,

$$
e(G-S)\ge N\qquad\text{for every }|S|\le t-2.
$$

The red forest necessarily contains a star with `a` edges, so the maximum degree of the remaining graph is at least `a` for every such `S`.

Because the first residual property holds, the all-blue colouring contains `F(m)`. Therefore `G` has a vertex `v` of maximum degree `d≥b`.

Suppose that some other vertex `u` has **at least `b` neighbours outside `v`**, or equivalently `d_(G-v)(u)≥b`. Set `S={v,u}`. The edges incident with `v` account for at least `b` edges, and the edges at `u` not already counted account for at least another `b`.

Starting with this `S`, repeat exactly `t−4` times: by the preceding vertex-cover observation, the remaining graph still has a red copy of `F(n)` as long as `|S|≤t−3`. Choose the centre of its `a`-edge star and add that centre to `S`. This deletes **at least `a` further edges** each time, none counted in earlier steps. In the final graph `|S|=t−2`, which again must contain a red copy of `F(n)` and hence at least `N` remaining edges. Consequently

$$
e(G)\ge 2b+(t-4)a+N,
$$

as claimed.

Thus, if `e(G)` were smaller than the claimed bound, **no such `u` exists**. Every vertex other than `v` has degree at most `b−1` after deleting `v`. Simplicity now implies every vertex of original degree at least `b`, other than `v`, **is a neighbour of `v`** (otherwise deleting `v` would not lower its degree).

Colour red all edges joining `v` to other vertices of original degree at least `b`. Colour additional edges incident with `v` red, if needed, until at least `d−b+1` of its incident edges are red. Colour **all other edges blue**. The red graph is contained in a single star centred at `v` and hence cannot contain `F(n2,...,ns)`, which has at least **two vertex-disjoint nontrivial components**. Every vertex has blue degree at most `b−1`, so the blue graph contains no `K_(1,b)` and therefore no `F(m)`. This contradicts the first residual arrowing condition. **QED.**

**Symmetric consequence:** If `s≥4`, exchange the two colours and the two target forests to obtain

$$
e(G)\ge 2n_1+M+(s-4)m_1.
$$

For `s,t≥4`, both bounds hold simultaneously; take their maximum. No assumption about graph structure, connectedness, vertex count or parity is made.

## Theorem C — exact unbounded nonuniform families, including positive switching surplus

**Family C1: three red stars versus arbitrarily many blue stars.** Let `t≥4` and

$$
n=(a,1,1),\qquad m=(b,c,\underbrace{1,\ldots,1}_{t-2}),
$$

where `a≥c≥1` and `b≥a+c−1`. The original antidiagonal maxima are

$$
w_3=b,\quad w_4=b,\quad w_5=\cdots=w_{t+1}=a,\quad w_{t+2}=w_{t+3}=1.
$$

Therefore

$$
J(n,m)=2b+(t-3)a+2.
$$

Theorem B gives the **same** lower bound because `N=a+2`:

$$
2b+N+(t-4)a=2b+(t-3)a+2.
$$

The canonical disjoint-star host of exactly this edge count gives equality. Hence **the conjectured joint-residual minimum is proved without restriction on the graph host**, for all positive integers and every `t≥4` in this family.

This includes `n=(2,1,1),m=(4,1,1,1,1)` at the **exact minimum 14 edges**: the unrestricted-host bound is not just a finite computer experiment.

**Unbounded switching surplus within C1.** The two *separate* residual canonical antidiagonal sums are

$$
L=2b+c+t-2,\qquad R=(t-1)a+c+1.
$$

Define the purely algebraic switching surplus `σ=J−max(L,R)`. Thus

$$
\sigma=\min\{(t-3)(a-1)-(c-1),\ 2(b-a)-c+1\}.
$$

For `t=4`, take a free positive integer `r` and set `a=2r`, `b=3r`, `c=r`. Then

$$
J=8r+2,\qquad L=7r+2,\qquad R=7r+1,\qquad\sigma=r.
$$

Thus we prove a family with **arbitrarily large switching surplus**, for arbitrary simple graph hosts. This is a genuine positive part of issue #3490 and not a consequence of taking the larger of the two separate antidiagonal sums. We are **not** assuming either residual's proposed formula is already certified in order to compute the algebraic surplus.

**Family C2: equal leading stars with all other components single edges.** Let `s,t≥3`, let `a≥1`, and set

$$
n=(a,1,\ldots,1)\quad(s\text{ components}),\qquad
m=(a,1,\ldots,1)\quad(t\text{ components}).
$$

The canonical weights give

$$
J(n,m)=(\max(s,t)-1)a+(\min(s,t)-1).
$$

If `t≥4` and `t≥s`, Theorem B gives equality:

$$
2a+(a+s-1)+(t-4)a=(t-1)a+(s-1)=J.
$$

If `s≥4` and `s≥t`, use the symmetric bound instead. The remaining case `s=t=3` follows from the elementary centre-deletion bound in Theorem D below, also giving `J=2a+2`. Hence C2 is proved for **all `s,t≥3`**. These families can be nonuniform when `a>1`.

## Theorem D — elementary complementary lower bounds for all s,t≥3

Regardless of whether Theorem B applies, any graph satisfying the two joint residual arrowing conditions obeys

$$
e(G)\ge N+\sum_{j=1}^{t-2}m_j,\qquad
e(G)\ge M+\sum_{i=1}^{s-2}n_i.
$$

**Proof of the first inequality.** From the first residual arrowing condition, colour all edges blue. The host contains a blue copy of the full `t`-component forest `F(m)`. Let `S` consist of the distinct centres of its **largest `t−2` component stars**. These stars use at least `Σ_(j=1)^(t−2)m_j` different edges incident with `S`. Now use the *second* residual arrowing condition: colouring every edge incident with `S` blue and every other edge red produces a blue graph with vertex cover `S` of size `t−2`, too small to contain `F(m2,...,mt)` with `t−1` disjoint nontrivial stars. Hence the red remainder `G−S` contains `F(n)`, using at least `N` further, disjoint edges. Add the two contributions. The second inequality is symmetric, starting with an all-red copy of `F(n)` forced by the second residual condition, then using the first residual condition. **QED.**

In particular, if both targets are matchings (`n=1^s`, `m=1^t`), either bound is `s+t−2`, precisely `J`. This independently proves the entire **matching-versus-matching** residual family for all `s,t≥3`.

## Theorem E — exact first nontrivial switching case beyond the infinite families

The separate proofs `RIGID_12EDGE_FINITE_THEOREM.md` and `RIGID_13EDGE_FINITE_THEOREM.md` establish, without any restriction on the host graph topology,

$$
J((3,2,1),(3,1,1,1))=13,\qquad
J((3,1,1),(4,3,1,1))=14.
$$

The two separate residual canonical sums are each 12 in the first case and each 13 in the second, hence the switching surplus is one in both cases. The universal bound of Theorem B excludes every graph with fewer than twelve edges. A hypothetical twelve-edge joint host is forced by equality to consist of `F(3,2,1)` plus two nonadjacent cubic attachment vertices. Two independently coded **complete** finite enumerators cover all 9,194 allowed attachment configurations, reduce to 130 via necessary extra vertex-deletion constraints, and check every two-edge-colouring of those 130 graphs: no counterexample exists. The unique borderline graph is explicitly listed with a residual-avoiding colouring. The canonical 13-edge star host attains the lower bound. The first proof is detailed in its standalone theorem and two independent executable certificates. For the second, the same two-hub equality reasoning forces the full five-edge forest `F(3,1,1)` plus two nonadjacent degree-four hubs; **31,667** attachment descriptions remain. An exact full-colouring-compatible structural test eliminates all but one of the **9,225** configurations with enough vertices for the full blue target. The last graph fails the other residual property. Two independent enumerators agree on every count. Neither result relies on the unproved unrestricted joint-residual hypothesis.

## Theorem F — exact 15-edge strict-switch case beyond the first two

The standalone proof `RIGID_14EDGE_FINITE_THEOREM.md` establishes, for **arbitrary finite simple graph hosts**,

$$
J((3,2,1),(4,1,1,1))=15.
$$

The larger separate residual star-host threshold is only 14. Every hypothetical fourteen-edge joint host necessarily has two nonadjacent degree-four vertices and a six-edge `F(3,2,1)` remainder: this follows **directly** from the two Ramsey conditions, without assuming the general issue. Two independent exhaustive graph generators enumerate all **74,553** permitted old/neighbour attachment descriptions. Each is defeated by one of three exact avoiding-colouring certificates: a two-vertex deletion (72,512), a single red star (1,914), or a red matching (127). The Python certificate includes the exact edges of all 127 red matchings; the independently written C++ implementation additionally tests the complete 2^14 colour space in its residual cases. No fourteen-edge joint host exists; the canonical fifteen-edge star host attains the minimum. This is a valid parameter-specific result, **not a proof of the full joint-residual hypothesis**.

## What remains genuinely unproved

The original proposed inequality for **arbitrary simple graph hosts and arbitrary positive star-size sequences** remains unresolved. Theorem B and D are necessary bounds; when their maximum is strictly **less** than `J`, they do not yet recover all antidiagonal switching surplus. Three positive-switching 3-versus-4 cases are now settled by complete, independently implemented finite equality-case classifications: `(3,2,1)` vs `(3,1,1,1)` at J=13, `(3,1,1)` vs `(4,3,1,1)` at J=14, and `(3,2,1)` vs `(4,1,1,1)` at J=15. The next small unresolved candidate is `(4,2,1)` vs `(4,1,1,1)`, with proposed J=16 and proven general lower bound 15. More general positive-switching patterns beyond these subtheorems still require proof or refutation. Our success in C1/C2 and the three finite exact cases must **not** be promoted to a proof for all `s,t≥3`.

The finite tests below try to falsify the conjecture, but their negative results cover only stated graph classes. The currently outstanding mathematical step is to control **overlapping star centres in arbitrary hosts** sufficiently to recover the missing difference between `J` and the proved universal bounds, not the previously resolved three-by-three low-degree case classification.

The issue disposition is **`PARTIAL`**, with an unconditional exact theorem for star hosts, unconditional iterative-peeling lower bounds for all graph hosts, and unconditional exact infinite families. Neither an unrestricted proof nor an explicit arbitrary-host counterexample was obtained.
