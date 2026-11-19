# A complete certified finite bridge for the first unresolved 3-versus-4 residual case

**Date: 2026-11-19. Scope: bounded exact original mathematical subtheorem, conditional on neither Erdős #561 nor an unproved 3×3 formula.** The only unbounded input is Theorem B of `JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md`, independently proved there by explicit avoiding colourings.

## Theorem

Set `n=(3,2,1)`, `m=(3,1,1,1)`. Every finite simple graph G satisfying both

$$
G\to(F(2,1),F(3,1,1,1))
\quad\text{and}\quad
G\to(F(3,2,1),F(1,1,1))
$$

has **at least 13 edges**. Conversely, the disjoint five-star residual host of antidiagonal edge sizes `(4,3,3,2,1)` has 13 edges and arrows both residual pairs. Therefore the joint residual minimum is **exactly 13**. The two separate residual antidiagonal sums are both 12, so this is a genuine strict switching-surplus-one theorem for **arbitrary simple graph hosts**.

## Proof: unbounded structural reduction

By the arbitrary-host peeling bound with s=3,t=4, every simultaneous-arrowing graph has at least `2*m1+sum(n)=2·3+6=12` edges. Suppose for contradiction that it has exactly 12.

The all-blue colouring in the first residual relation forces a blue `K_(1,3)`, hence G has a vertex `v` of degree at least three. The proof of Theorem B shows that if no vertex `u≠v` has at least three neighbours in `G−v`, there exists an explicit red star centred at `v` and blue graph with maximum degree two, avoiding the first residual pair. Consequently such a vertex `u` must exist.

Colour all edges incident with `{v,u}` blue and every other edge red. The blue graph has vertex cover of size two and therefore cannot contain the three disjoint blue edges required by `F(1,1,1)` in the second residual relation. Hence the remaining red graph `G−{v,u}` contains `F(3,2,1)` with **six edges**. At least three edges meet `v`, at least three further distinct edges meet `u` outside `v`, and at least six remain: their sum is the entire 12-edge budget. All inequalities are equalities: `deg_G(v)=3`, `deg_(G−v)(u)=3`, `v` and `u` are **not adjacent**, and `G−{v,u}` has exactly six edges, every one used in a copy of `F(3,2,1)`. In particular the whole nontrivial remainder is **precisely** three disjoint stars of respective edge counts `(3,2,1)` plus isolated vertices, and both `v,u` have degree three.

Write the fixed six-edge remainder with edge set

$$
B=\{01,02,03,45,46,78\},
$$

with the degree-three star centre at vertex 0 and the degree-two star centre at vertex 4. Add new vertices numbered 9,10 for the cubic hubs `v,u`, and their six incident edges. Neither hub can meet vertex 0 because it is already saturated in the original Δ≤3 graph (v has maximum degree three). Vertex 4 can meet at most one hub, other old vertices 1,2,3,5,6,7,8 can meet either hub, and any additional new leaf can be adjacent to hub 9 only, hub 10 only, or both. No edge is allowed between 9 and 10, and no edge outside these six original edges and six attachments can occur.

Thus, up to renaming newly introduced vertices, all possible graphs arise by selecting for each of the eight old vertices `(1,...,8)` one of four attachment patterns `{none,9,10,both}`, excluding `both` at vertex 4; requiring at most three old-neighbour attachments per hub; and allocating the remaining incident edges to `h` shared new neighbours and otherwise private new leaves, for every feasible `0≤h≤min(3−a9,3−a10)`. This is a **complete finite superset** of all possible 12-edge counterexamples; different descriptions may yield isomorphic graphs, which is harmless.

There are **9,194** attachment configurations. The second residual relation yields two further necessary conditions: colour all edges meeting `{9,0}` blue and the remaining edges red; likewise for `{10,0}`. Each blue graph has a two-vertex cover, so cannot contain a blue matching of three edges. The residual red graph must be `F(3,2,1)` and has exactly six edges, since both deleted vertices have degree three and are not adjacent. These two exact necessary component-shape tests reduce the 9,194 attachment configurations to **130**.

For each of those 130 graphs, the two independent checkers `search_rigid_12edge.py` and `verify_rigid12_independent.py` enumerate actual vertex-disjoint ordinary star-forest embeddings and apply exact all-colouring tests. **129 fail the second residual Ramsey property**; precisely **one** satisfies the second property, and that graph fails the first. The unique borderline graph is a **disjoint union of the fixed `F(3,2,1)` and two separate three-edge stars**, with exactly 12 edges (no edge identifications). The certificate `RIGID_12EDGE_CERTIFICATE.json` includes its exact graph-edge list and an explicit avoiding red/blue colouring for the first residual condition, so the last step is independently inspectable without trusting a status bit.

The two separate enumerations agree not only on the final answer but also on the intermediate exact counts `9,194`, `130`, `129` and `1`. Both use distinct graph-generation loops and different forest-embedding code. Thus no 12-edge graph satisfies both residual conditions; since the 13-edge canonical star host does, the minimum is 13. **QED.**

## Independent finite computation audit

The first verifier enumerates each of the four allowed old-vertex attachment patterns, constraints at the degree-two centre and both hubs, shared fresh neighbours, and private leaves, then tests component shapes and full Ramsey arrowing using its general ordinary forest-embedding oracle. The second starts from all eligible old-neighbour subsets for the two hubs, reconstructs shared and private leaves independently, and uses a different exact embedding generator and subset-saturation colouring dynamic program. The latter has no imports of the first graph enumeration or its graph-embedding helper.

Both verifiers enforce **full** two-colouring adversarial tests, not a sampled red/blue selection, graph-class inference or matching-degree approximation. An explicit candidate graph could have arbitrary cycles among its vertices if allowed by the edge budget; the proof of the structural reduction shows there is no budget for other edges once the forced six-edge residual forest and the two cubic hubs are specified. This is why the finite graph generation is complete for the hypothetical counterexample class.

**Outcome:** `JOINT_RESIDUAL_PROVED_FOR_THIS_SPECIFIC_3X4_CASE`, not `JOINT_RESIDUAL_PROVED` for the unrestricted `s,t≥3` hypothesis. General issue #3490 remains **PARTIAL**.
