# Erdős #561 — exact 15-edge joint residual minimum for (3,2,1) versus (4,1,1,1)

**Research date: 2026-11-20. Status: exact, source-locked research proof; mathematical source review pending.** This establishes one previously unresolved strict-switching instance of issue #3490 for **all finite simple graph hosts**. It does not prove the unrestricted joint-residual conjecture or unrestricted Erdős #561. The graph reduction below is self-contained; it does not assume the unpromoted three-star size-Ramsey reduction.

## Theorem

Let `F(a,b,...)` denote the vertex-disjoint union of stars with the indicated **positive edge counts**. If a finite simple graph `G` satisfies both

$$
G\to(F(2,1),F(4,1,1,1))
\quad\text{and}\quad
G\to(F(3,2,1),F(1,1,1)),
$$

then `|E(G)|≥15`. This is sharp: the host

$$
H=F(5,4,3,2,1)
$$

has exactly **15 edges** and arrows both target pairs. Hence the minimum number of edges required to satisfy these **two** Ramsey relations simultaneously is **15**.

The two individual canonical residual star-host edge counts are strictly less than 15; the joint antidiagonal sum for original sequences `n=(3,2,1)` and `m=(4,1,1,1)` is

$$
J=5+4+3+2+1=15.
$$

## Proof I. A hypothetical fourteen-edge counterexample is rigid

Write **A** for the first residual Ramsey condition and **B** for the second. We first prove directly that any host satisfying both has at least fourteen edges, then classify the equality case.

The all-blue colouring in A forces a copy of `F(4,1,1,1)`; in particular `G` has a vertex `v` of maximum degree `d≥4`.

**Two-centre lemma.** There is a vertex `u≠v` with degree at least four in the graph obtained by deleting `v`. Otherwise each `w≠v` with original degree at least four is a neighbour of `v` (its degree must drop on deleting `v`). Colour every edge `vw` for such a `w` red, and if necessary colour additional edges incident with `v` red until at least `d−3` edges at `v` are red. Colour everything else blue. The red graph is a **single star**, so cannot contain the two vertex-disjoint nontrivial red stars `F(2,1)`. Every blue degree is at most three: this holds at `v` by construction, at all other originally high-degree vertices because they lose an edge `vw`, and at originally lower-degree vertices automatically. Thus blue contains no four-edge star and therefore no `F(4,1,1,1)`, contradicting A. This proves the lemma.

Now colour blue all edges incident with the two vertices `v,u` and colour every remaining edge red. The blue graph has a vertex cover of size two. It cannot contain the three vertex-disjoint nontrivial blue edges of `F(1,1,1)`, each of which would need a distinct vertex of the cover. Therefore B forces a red `F(3,2,1)` in the graph after deleting `v,u`. Its six edges are disjoint from the edges at the two centres. Thus

$$
|E(G)|\ge d_G(v)+d_{G-v}(u)+6\ge4+4+6=14.
$$

Suppose `|E(G)|=14`. Every inequality must be equality. Consequently `d_G(v)=4`, `d_(G-v)(u)=4`, and `G−{v,u}` has **exactly six edges**, all used in one `F(3,2,1)`. Because `v` was chosen of maximum original degree four, `v` and `u` cannot be adjacent (else `d_G(u)≥5`). Both have degree exactly four, the whole graph has maximum degree four, and the six-edge remainder is a disjoint union of stars of edge sizes `(3,2,1)` plus isolated vertices.

Fix a labelled representative for its six nontrivial edges:

$$
B_0=\{01,02,03,45,46,78\}.
$$

Call the two new degree-four vertices `9` and `10`. Every other edge is incident with one of these vertices. Therefore each additional old-vertex attachment is an edge from vertex 9 or 10 to one of the nine vertices `0,...,8`, and every new vertex outside `B_0` can have edges only to vertex 9, vertex 10, or both. All other edges are forbidden by the exhausted fourteen-edge budget.

Let `A,B⊆{0,...,8}` be the old neighbours of 9 and 10, respectively. Necessarily `|A|,|B|≤4`. Vertex 0 has original degree three, so it cannot belong to both `A` and `B`; every other old vertex has room for both attachments under the maximum-degree-four constraint. Let `h` be the number of **new** common neighbours of 9 and 10. Then

$$
0\le h\le\min(4-|A|,\;4-|B|).
$$

The number of new private neighbours of 9 is exactly `4−|A|−h`, and similarly for 10. Because new private vertices are indistinguishable up to graph isomorphism, `A,B,h` describe **every** equality-case graph, possibly with harmless isomorphic duplicates. The finite parameter count is

$$
\sum_{\substack{A,B\subseteq\{0,\ldots,8\}\\|A|,|B|\le4\\0\notin A\cap B}}
\bigl(1+\min(4-|A|,4-|B|)\bigr)=\boxed{74,553}.
$$

This is a complete parameterization, not a search restricted to stars, trees, bipartite graphs, or a sampled graph database.

## Proof II. Every equality-case graph has an explicit avoiding colouring

We classify all 74,553 complete attachment descriptions by exact integer operations. The classification uses **two separate implementations**: `verify_rigid14_exact.cpp`, with bitset subgraph embeddings and all 2^14 red/blue colourings where necessary, and `verify_rigid14_independent.py`, with a separately implemented graph generator, disjoint-star embeddings and constructive red matching search. Both return the same partition:

| Constructive certificate | Count |
| --- | ---: |
| A two-vertex deletion already violates B | **72,512** |
| A single red star defeats A | **1,914** |
| A red matching defeats A | **127** |
| Graphs satisfying both residual conditions | **0** |
| **Total configurations** | **74,553** |

The alternatives are **mathematically sufficient**, not merely empirical labels:

**Certificate 1: two-vertex deletion.** For B to arrow `(F(3,2,1),F(1,1,1))`, deleting **any two vertices** must leave a red copy of `F(3,2,1)`. Otherwise colour all edges incident with those two vertices blue, and every other edge red. Three blue vertex-disjoint single-edge stars cannot fit inside a graph whose edges are all covered by two vertices, and the red residual has no target forest. The checker explicitly enumerates every possible `F(3,2,1)` embedding, records its vertex mask and detects a pair of vertices intersecting **every** such embedding. This proves failure of B in 72,512 configurations.

**Certificate 2: a red star.** A red graph consisting of edges incident with **one** vertex has no two vertex-disjoint nontrivial components, so it avoids red `F(2,1)`. If every possible blue `F(4,1,1,1)` embedding includes the chosen vertex, colour all edges at that vertex red and the others blue; this destroys every blue target. The checker computes the intersection of the vertex sets of **all** ordinary blue target embeddings. This gives the explicit avoiding colouring in 1,914 additional configurations.

**Certificate 3: a red matching.** A red matching has maximum degree one, so it contains no two-edge red star, hence no red `F(2,1)`. If a red matching contains at least one edge of **every** possible full blue `F(4,1,1,1)` embedding, the complement blue graph contains no such target. In each of the final 127 configurations the independent Python checker constructs just such a matching; the complete list of these **127 edge-level matchings** is stored in `RIGID_14EDGE_CERTIFICATE.json` for direct review. The C++ checker independently exhausts the **entire 2^14 two-colouring space** in these remaining configurations and also finds that A fails every time.

The three certificate categories exhaust all 74,553 simple attachment descriptions. Thus no fourteen-edge graph satisfies both residual Ramsey properties. The reduction in Proof I excludes all lower edge counts. **QED for the 15-edge lower bound.**

## Proof III. A fifteen-edge host meets both conditions

The known disjoint-star host `H=F(5,4,3,2,1)` has exactly fifteen edges. For a pair of star-forest targets, a disjoint-star host arrows them if its sorted component-edge sizes coordinatewise dominate the target pair's antidiagonal maxima. This criterion has a simple independent greedy proof: at each host star, either reserve enough red edges for the next red target star or reserve enough blue edges for the next blue target star, proceeding through the list until one full target forest has been reserved on disjoint host components.

For the first residual pair, the necessary antidiagonal sizes are `(5,4,2,2,1)`; for the second, `(3,3,3,2,1)`. In each case `(5,4,3,2,1)` dominates them componentwise. Therefore H arrows both residual pairs and realizes the lower bound. **QED for the exact minimum of fifteen edges.**

## Scope, methods and reproducibility

Both verifiers generate all `A,B,h` triples allowed in Proof I, including graphs with cycles, intersecting high-degree neighbourhoods, shared new neighbours, and multiple possible graph symmetries. They deliberately **do not** assume the host is a star forest. All target embeddings are ordinary **non-induced** vertex-disjoint star forests; inducedness would be the wrong Ramsey problem. The C++ program uses bitsets for complete embedding and red/blue subset-DP tests. The Python program independently uses graph-adjacency combinations and explicit red matching witnesses. Both independently reproduce the exact counts above. The Python certificate includes the deterministic ordered-generation SHA-256 `9c378118e45d242aa64a1c8839fce57a43f239f092bb7f350f1f1e0d5e168b2f` and 127 directly inspectable matching colourings.

The mathematical reduction to the complete finite search class is a universal argument for **arbitrary finite simple graphs**, so this is a finite proof of a genuinely unrestricted-host single parameter case, not a restricted-host numerical experiment. Nevertheless, a computer-aided exact proof and a complete Lean kernel formalization are different standards; no full Lean formalization of this result is claimed.

**Claim boundary:** `JOINT_RESIDUAL_PROVED_FOR_N321_M4111`, `JOINT_RESIDUAL_GENERAL_S_T_GE_3` remains **OPEN/PARTIAL**. The broader three-star size-Ramsey reduction and unrestricted Erdős #561 are not proved by this case. The result should be source-admitted through GCL's existing protected policy as a substantive paper-plus-finite-certificate claim, retained `UNDER_REVIEW` pending mathematical source review and formal certification.
