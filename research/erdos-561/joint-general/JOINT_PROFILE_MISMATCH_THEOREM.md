# Erdős #561 — residual-profile mismatch theorem and an exact 3×4 infinite family

**Research date: 2026-11-20.** This is a paper proof for arbitrary finite simple host graphs. It is an unconditional mathematical subtheorem, NOT a proof or refutation of the full multi-star residual conjecture (#3490), the upstream original 3×3 transfer, or unrestricted Erdős #561. Graph arrows mean that *every* red/blue edge-colouring contains one of the two specified ordinary, non-induced, vertex-disjoint star forests. All component sizes count positive edges.

Write `F(n)` for the disjoint union of stars whose edge counts are the nonincreasing sequence `n=(n1,...,ns)`. Let `n'=(n2,...,ns)` and `m'=(m2,...,mt)`.

## Theorem A — general residual-profile mismatch

Let `s≥3,t≥4`. Let `n=(n1,...,ns)` and `m=(b,m2,...,mt)` be positive, nonincreasing integer sequences with `b=m1`. Set `N=sum(n_i)`. Suppose

$$
\sum_{j=2}^t m_j=N
$$

but the two multiset profiles `n` and `m'` are **different** (equivalently their disjoint star forests are nonisomorphic after ignoring isolated vertices). Then **every** finite simple graph `G` satisfying both

$$
G\to(F(n'),F(m))
\quad\text{and}\quad
G\to(F(n),F(m'))
$$

has

$$
\boxed{e(G)\ge 2b+N+1.}
$$

The theorem holds regardless of host order, connectedness, cycles, overlapping star centres, or parity. It does **not** assume the conjectured joint-residual formula.

### Proof

**First: force two distinct large-degree centres.** Colour every edge of `G` blue. The first arrowing condition forces a blue `F(m)` and hence a vertex `v` of degree `d_G(v)=Δ(G)≥b`. If there were no vertex `u≠v` with `d_(G-v)(u)≥b`, proceed as follows. Colour red all edges joining `v` to vertices of original degree at least `b`. Every such neighbour exists by the assumed absence of a high-degree vertex in `G-v`: any original degree-`b` vertex not adjacent to `v` would remain degree at least `b` after deletion. Extend these red edges within the star at `v` until at least `d_G(v)-b+1` incident edges are red. Colour every other edge blue. The red graph is a single star and cannot contain `F(n')`, whose `s−1≥2` nontrivial components must be vertex-disjoint. All blue degrees are at most `b−1`, so blue cannot contain the `b`-edge star required by `F(m)`. This violates the first arrowing condition. Therefore such a vertex `u` necessarily exists.

**Second: count the remaining edges.** Colour all edges incident with `S={v,u}` blue, and all other edges red. The blue graph has a vertex cover of size at most two, so it cannot contain the `t−1≥3` vertex-disjoint nontrivial stars of `F(m')` (each must use a distinct vertex of any vertex cover). By the second arrowing condition, the red graph `G-S` must contain `F(n)` and thus at least `N` edges. The sets of edges at `v`, at `u` outside `v`, and outside both are disjoint, so

$$
e(G)=d_G(v)+d_{G-v}(u)+e(G-S)\ge b+b+N=2b+N.
$$

**Third: equality would force two incompatible residual forests.** Assume for contradiction that `e(G)=2b+N`. Every inequality above is then equality. Thus `d_G(v)=b=Δ(G)`, `d_(G-v)(u)=b`, and `G-S` has exactly `N` edges, all occupied by a copy of `F(n)`. Further, `v` and `u` are **not adjacent**: otherwise `d_G(u)≥b+1` would exceed `Δ(G)=b`. Both centres have original degree exactly `b`.

Now colour **every edge incident with `u` red** and every remaining edge blue. The red graph is a single star, so it avoids `F(n')`. Consequently the first arrowing condition forces `G-u` to contain a blue copy of `F(m)`. But

$$
e(G-u)=e(G)-d_G(u)=b+N=\sum_{j=1}^t m_j.
$$

The blue target forest uses **all** available edges. Thus, ignoring isolated vertices, `G-u` is *exactly* `F(m)`, not merely a graph with a loose subgraph of that shape. Vertex `v` still has degree exactly `b` in `G-u`. Because `b` is the largest star size in `m`, `v` is the centre of one of its `b`-edge star components (or an endpoint of such a component if `b=1`). Removing `v` therefore leaves, again ignoring isolated vertices, **exactly** `F(m')`.

However the second-arrowing equality already established that `G-{v,u}` is **exactly** `F(n)` on its nonisolated edges. The same graph cannot simultaneously be `F(n)` and the nonisomorphic `F(m')`. This contradicts the profile-mismatch assumption.

Hence equality at `2b+N` is impossible, giving the stated stronger integer lower bound. **QED.**

## Theorem B — a sharp two-parameter infinite family

Let integers `a≥3` and `b≥2a−2`, and set

$$
n=(a,1,1),\qquad m=(b,a-1,2,1).
$$

Then the exact minimum edge count of any finite simple graph simultaneously arrowing the two corresponding residual pairs is

$$
\boxed{J(n,m)=2b+a+3.}
$$

### Proof

The red full forest `F(n)` has `N=a+2` edges. The blue residual `F(m')=F(a-1,2,1)` also has `(a-1)+2+1=a+2=N` edges. The two forests are not isomorphic because their largest stars have sizes `a` and `a−1`, respectively. Theorem A therefore gives the **arbitrary-host** lower bound

$$
e(G)\ge2b+(a+2)+1=2b+a+3.
$$

For these parameters, the five antidiagonal weights of the original joint-residual star-host construction (excluding its first weight) are

$$
(w_3,w_4,w_5,w_6,w_7)=(b,b,a,2,1).
$$

Indeed `b≥2a−2` makes the first two maxima equal to `b`; the last three maxima are `a,2,1`. The disjoint-star graph

$$
H=F(b,b,a,2,1)
$$

has `2b+a+3` edges and arrows both residual pairs by the classical elementary greedy antidiagonal star-host criterion (proved separately in this repository without any hypothesis about arbitrary hosts). This upper bound matches Theorem A's unrestricted-host lower bound, so the stated value is exact. **QED.**

In particular, for `a=3`, **every** `b≥4` is proved:

$$
\boxed{J((3,1,1),(b,2,2,1))=2b+6.}
$$

The already independently resolved benchmark `b=5` therefore has exact value **16**, and the result also covers `b=4` at 14 edges, `b=6` at 18 edges, and arbitrarily large `b`.

## Relationship to prior protected research

The existing protected manuscript `RIGID_15EDGE_311_5221_THEOREM.md` and claim `ERDOS561-JOINT-RIGID-3X4-009` **already independently prove the single pair** `n=(3,1,1),m=(5,2,2,1)` at 16 edges, by an A-only rigidity lemma specialized to the red matching target `2K2`. That result is not reintroduced as a new claim here. The **new contribution** is Theorem A's unrestricted residual-profile mismatch for arbitrary `s≥3,t≥4`, including non-matching red residual forests and blue forests with repeated leading sizes, plus Theorem B's sharp two-parameter family. The finite case verification below is deliberately complementary: it checks a complete non-star attachment class under an explicit uniform avoiding colouring, rather than duplicating the already version-controlled proof's finite star-host arm-allocation test.

## Exact independent full-graph check of the first 16-edge benchmark

For `n=(3,1,1)`, `m=(5,2,2,1)`, suppose the simultaneous arrowing holds in a graph of exactly **15** edges. Theorem A's first two steps force two nonadjacent degree-five vertices `8,9` and an **exact** five-edge remainder `F(3,1,1)` after deleting both. Label its edges `01,02,03,45,67` on vertices `0,...,7`. Both new degree-five vertices can attach to any old vertices (the original three-star centre has degree three and can accept both new edges without exceeding five). All other new vertices can attach privately to one hub or be shared by both. Thus every possible 15-edge graph is represented, up to relabelling new leaves, by two old-neighbour sets `A,B⊆{0,...,7}` of size at most five and a number of new shared neighbours

$$
0\le h\le\min(5-|A|,5-|B|).
$$

This is a **complete superclass** of any hypothetical equality graph, not a restriction to disjoint stars or a random sample. It contains exactly **84,630** attachment descriptions. Two completely separate verification implementations reproduce the following *explicit avoiding-colouring certificate for each description*: colour every edge incident with hub 8 red; colour all other edges blue. Red is a single star, hence avoids the required red two-edge matching `F(1,1)`. Blue has exactly ten edges. Both checkers verify that its edge set is **never** a copy of `F(5,2,2,1)`, as already forced by the general proof. Consequently this colouring defeats the **first** residual relation in every one of the 84,630 generated graphs.

- `verify_profile_mismatch_15edge.py`: independent Python combinations-based generator, adjacency traversal and exact component star-shape classifier. Its exact partition: **84,108** blue graphs are not disjoint star forests, and **522** are star forests with the wrong component-size profile. Zero can contain the ten-edge blue target, since there are exactly ten blue edges.
- `verify_profile_mismatch_cpp.cpp`: separate C++ bitset generator and adjacency-component classifier independently reproduces **84,108 / 522 / 0**. It checks the full 84,630 candidate count and the fixed explicit red/blue colouring.
- `verify_profile_mismatch.py`: independent exact-integer source check covering 2,416 smaller general theorem parameter profiles with equal red-full and blue-tail edge totals but nonisomorphic forests (no contradictory canonical star-host upper bounds), plus 814 test points of the infinite family and 396 further cases of the `a=3` specialization. The complete proof is the graph argument above, **not** a finite sample extrapolation.

Machine-readable source records `RIGID_15EDGE_MISMATCH_CERTIFICATE.json` and `PROFILE_MISMATCH_PARAMETER_CERTIFICATE.json` preserve exact counts, conditions, and generation hash. The source-lock manifest and canonical research claim ledger distinguish mathematical paper proof (`UNDER_REVIEW`) from deterministic finite checks (`CHECKED`).

## General scope and next research case

Theorem A applies to *any* lengths `s≥3,t≥4` and all positive star edge sizes satisfying its equal-edge-count and profile-inequality conditions. Theorem B makes it sharp for the stated two-parameter family and solves the previous smallest 16-edge benchmark. These results do **not** close arbitrary unequal-sum or equal-profile cases, and do not validate the full original Erdős #561 conjecture.

A smaller unresolved strict-switch case, not covered by these theorems, is `n=(3,2,1)` against `m=(4,2,1,1)`: its proposed antidiagonal joint value is **15**, while the preceding established elementary/peeling bounds give **14**. This is the next direct falsification target; a 14-edge graph satisfying both residual properties would refute the general joint-residual hypothesis.
