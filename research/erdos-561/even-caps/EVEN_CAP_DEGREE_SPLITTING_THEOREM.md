# Erdős #561 — unconditional even-cap edge splitting

**2026-11-19. General graph-theoretic result, independent of the star-forest residual theorem.** The construction below is a classical consequence of regular graph factorization, presented here explicitly for verification. We do **not** claim that the underlying existence of 2-factorizations is newly discovered, nor that unrestricted Erdős #561 is solved.

## Theorem: both caps even are always attainable

Let `G` be any finite simple graph and let `alpha` and `beta` be positive **even** integers with `Delta(G)≤alpha+beta`. Then its edge set can be divided into red and blue edges so that

$$
\Delta(R)\le\alpha,\qquad\Delta(B)\le\beta.
$$

For the key remaining degree-four case, `alpha=beta=2`: **every graph of maximum degree at most four can be split into two subgraphs of maximum degree at most two.** No bound on graph order, number of edges, connectivity or number of saturated vertices is required.

### Constructive proof

Write `D=alpha+beta=2k`. At each vertex `v`, add `D−deg_G(v)` fictitious incident half-edges. The total number of fictitious half-edges equals `D|V|−2|E|`, which is even. Pair them arbitrarily to form additional edges; permit repeated edges and loops, counting each loop as degree two. This gives a **D-regular multigraph** `H` containing the original simple graph `G` as a specified edge subset.

Since `D` is even, every connected component of `H` has an Euler circuit. Orient its edges consistently along that circuit, obtaining in-degree `k` and out-degree `k` at every vertex. Make a bipartite multigraph `B` with an outgoing and an incoming copy of every vertex. For each oriented edge from `u` to `v`, place one edge joining the outgoing copy of `u` to the incoming copy of `v`. Every vertex of `B` has degree exactly `k`.

By the standard perfect-matching theorem for regular bipartite multigraphs (Hall's theorem, iterated after deleting each perfect matching), the edges of `B` decompose into `k` perfect matchings. Under the inverse correspondence, each matching selects **one incoming and one outgoing edge at every vertex of `H`**. Each selected factor therefore has undirected degree exactly two at every vertex, with loops contributing two incidences as usual.

Assign exactly `alpha/2` of these factors red and the remaining `beta/2` factors blue. Every vertex in `H` then has red degree exactly `alpha` and blue degree exactly `beta`. Finally delete all fictitious edges, keeping the original edges with their assigned colours. Deleting edges cannot increase any degree. The desired edge partition of `G` follows. **QED.**

### Direct degree-four implementation

When `alpha=beta=2`, the bipartite multigraph `B` is **2-regular**: every component is an even cycle (possibly two parallel edges). Colour its edges alternately, producing the two perfect matchings without any search or appeal to the general regular-bipartite matching theorem. This is an explicit linear-time construction once the Euler tours are known.

`verify_even_caps_constructive.py` implements exactly this degree-four construction: complete the graph with dummy edges/loops to degree four, orient Euler circuits, find one perfect matching of the resulting bipartite 2-regular multigraph, and pull both factors back to the original edges. It checks every relevant NetworkX graph-atlas graph of at most seven vertices (**685 graph isomorphism types with maximum degree ≤4**), plus 200 independently generated larger simple graphs, with no failure. These tests corroborate the proof but are not its basis.

## Consequence for the small three-star shortlist

In the exact preceding 25-case source certificate (`research/erdos-561/unique16/SIXTEEN_TO_EIGHTEEN_PARAMETER_CERTIFICATE.json`), there are precisely **three ordered cases** with both degree caps even:

- `(3,2,1)` versus `(3,3,3)` and its colour reversal;
- `(3,3,2)` versus `(3,3,2)`.

All three have `D=n₁+m₁−2=4` and caps `(2,2)`. The universal edge partition prevents any maximum-degree-four arrowing graph from avoiding the degree-capped colouring, so all three are eliminated **conditional on the existing paper-level three-star reduction that constrains a hypothetical minimum counterexample to maximum degree four**. The exact integer audit in `verify_even_cap_parameters.py` gives **22 ordered / 11 unordered** remaining method-survivors, all with caps `(1,3)` up to swapping colours.

This theorem is **unconditional as a statement about edge partitions of arbitrary finite graphs**. Its translation to exact original size-Ramsey numbers is still conditional on the previously admitted, unpromoted three-star residual reduction. No assertion about the unrestricted Erdős #561 conjecture is made.
