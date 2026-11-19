# A second exact 3-versus-4 joint residual case with positive switching surplus

**Date 2026-11-19.** Fully specified finite proof certificate after an unbounded structural reduction. Not a proof of the unrestricted Erdős #561 conjecture or all of joint residual issue #3490.

## Theorem

For red star forest `n=(3,1,1)` and blue star forest `m=(4,3,1,1)`, every finite simple graph simultaneously arrowing

$$
(F(1,1),F(4,3,1,1))\quad\text{and}\quad(F(3,1,1),F(3,1,1))
$$

has at least **14 edges**. This is attained by the disjoint antidiagonal star host of edge counts `(5,4,3,1,1)` and therefore is the exact joint minimum. The independent antidiagonal sums of the two separate residual pairs each equal **13**; the positive switching surplus is one.

## Unbounded reduction of a hypothetical smaller host

The general two-hub peeling theorem gives the unconditional lower bound

$$
e(G)\ge2m_1+\sum n_i=2\cdot4+5=13.
$$

Suppose both joint residual properties hold for a graph of exactly 13 edges. The first condition applied to the all-blue colouring forces a vertex `v` with degree at least 4. The constructive proof of the two-hub theorem then forces another vertex `u≠v` with degree at least 4 in `G−v`; otherwise colouring an appropriate substar at `v` red makes the blue maximum degree at most 3 and the red graph contain only one star, defeating the first condition.

Colour all edges incident with `S={v,u}` blue, everything else red. The blue graph has a two-vertex cover and therefore avoids the three vertex-disjoint nontrivial stars of the blue-deleted target `F(m₂,m₃,m₄)=F(3,1,1)`: each of its three separate stars must meet a different vertex of any edge-covering vertex set. Hence the remaining red edges must contain the full forest `F(3,1,1)` with five edges.

The 13-edge total is exhausted by the at least four edges incident to `v`, the at least four further edges incident to `u` in `G−v`, and the five red edges outside both centres. Equality forces `deg_G(v)=4`, `deg_(G−v)(u)=4`, the vertices `v,u` nonadjacent, maximum degree four, and the entire five-edge remainder equal to `F(3,1,1)` plus isolated vertices. We may fix this remainder as

$$
B=\{01,02,03,45,67\}.
$$

Add two hubs 8,9 of original degree exactly four. Every remaining edge joins one of these hubs to an old vertex or a new vertex; no extra edges occur. Among the eight old vertices, star centre 0 has internal degree three and can receive at most one extra hub edge. All others have internal degree one and may receive both. Every new vertex can attach to hub 8 only, hub 9 only, or both. Thus a complete finite superset is obtained by choosing two old-neighbour subsets `A,B⊆{0,...,7}` of size at most four with `0∉A∩B`, then a number `h` of fresh shared neighbours from `0` through `min(4−|A|,4−|B|)`, and making the other fresh neighbours private leaves. Every hypothetical 13-edge graph is isomorphic, up to isolated vertices, to one of these configurations.

The enumeration contains **31,667** simple attachment configurations (labelled, including possible isomorphic duplicates). A first-residual arrowing graph must contain a blue copy of `F(4,3,1,1)` in the all-blue colouring, requiring **13 nonisolated vertices**. The generated graph has `18−|A|−|B|−h` nonisolated vertices, so configurations with `|A|+|B|+h>5` are impossible. This removes **22,442**, leaving **9,225** candidates.

A red graph avoids the target `F(1,1)` precisely when its edges have **no two disjoint members**. In a simple graph, every set of edges with that property is either a subset of one star or a triangle. Thus the first residual arrowing relation can be tested exactly and finitely by considering all subsets of each star and the complete three-edge triangles as potential red edge sets, giving blue the complement. A candidate arrows `(F(1,1),F(4,3,1,1))` **iff** every such red set leaves a blue copy of `F(4,3,1,1)`.

Of the 9,225 configurations, **9,224 fail the first residual property** by an explicit red star/triangle colouring (including failures of the all-blue containment test). The **unique** first-residual-positive graph is the disjoint union of the fixed five-edge forest `F(3,1,1)` and two new copies of `K_(1,4)`, with no attachments to old vertices and no shared fresh leaves. It fails the **second** residual property `(F(3,1,1),F(3,1,1))` by an explicitly enumerated avoiding colouring included in `RIGID_13EDGE_CERTIFICATE.json`.

The deterministic exhaustive verifier `search_rigid_13edge.py` independently enumerates the 31,667 configurations and all red star/triangle choices; its full two-colouring oracle verifies the sole first-residual-positive case fails the second property. The separately implemented `verify_rigid13_independent.py` regenerates all attachments with a different loop order and independently constructs all ordinary vertex-disjoint star-forest embeddings, producing **exactly the same intermediate and final counts**:

| Exact category | Configurations |
| --- | ---: |
| All simple generated 13-edge configurations | 31,667 |
| Insufficient nonisolated vertices | 22,442 |
| Satisfying necessary vertex-count condition | 9,225 |
| Failing first residual arrowing | 9,224 |
| Satisfying first residual arrowing | 1 |
| Satisfying both residual arrowing conditions | **0** |

Consequently there is **no** joint-arrowing graph of 13 edges, and the canonical antidiagonal 14-edge star host is sharp. **QED.**

## Scope of numerical proof

The reduction to two degree-four hubs is a universal graph-theoretic argument for **all** finite simple graphs, not a restriction to a convenient host class. The finite enumeration is complete for the forced 13-edge equality class: every remaining edge is an attachment to one of the two hubs, and fresh neighbours can always be relabelled into shared and private types. Each subgraph test uses **ordinary (non-induced)** forest containment with disjoint vertex sets, and the target values are exact edge counts. No sampled colouring, heuristic theorem prover, assumed 3×3 residual theorem or SAT solver is involved.

This is an exact **single 3-versus-4 family member**, not the unrestricted `s,t≥3` candidate. Full issue #3490 remains **PARTIAL**.
