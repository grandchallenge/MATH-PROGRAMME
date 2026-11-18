# Erdős #561 — replacing the degree-five density dependency

**Status:** self-contained combinatorial reduction to Vizing's adjacency lemma plus a small exact certificate, pending separate substantive mathematical review. The result is used only in the fixed `F(4,2,2)` versus `F(4,3,1)` case of Erdős #561.

## Lemma (the only critical-graph consequence required)

If `C` is a finite simple **5-edge-critical** graph, meaning `Δ(C)=5`, `χ′(C)=6`, and removing any edge makes it 5-edge-colourable, and `e(C)≤17`, then `|V(C)|=7` (ignoring isolates) and `e(C)≥16`.

### Step 1. Density bound using only Vizing's adjacency lemma

In a 5-edge-critical graph, a vertex of degree one is impossible: a 5-edge-colouring of `C-e` extends to a pendant edge because its other endpoint is incident to at most four edges in `C-e`. Thus all vertex degrees are 2, 3, 4, or 5. Let `n_j` be the number of vertices of degree `j`.

Vizing's adjacency lemma says that for every edge `uv` in a `Δ`-critical simple graph, if `d(v)=j`, then `u` has at least `Δ-j+1` **other** neighbours of degree `Δ`. In a 5-critical graph:

- Every degree-two vertex has two degree-five neighbours. A degree-five neighbour of a degree-two vertex has no other neighbour below degree five.
- Every degree-three vertex has at least two degree-five neighbours. In fact no neighbour can have degree two or three; if it has a degree-four neighbour, the adjacency lemma applied in the other direction forces both of its remaining neighbours to have degree five.
- A degree-five vertex adjacent to a degree-three vertex can have at most two neighbours below degree five, and it cannot also neighbour a degree-two vertex.

Give each degree-five vertex **one unit of capacity**. For each degree-two vertex, charge one unit to each of its two degree-five neighbours. For each degree-three vertex, charge half a unit to two chosen degree-five neighbours. No degree-five vertex is charged more than one unit: when incident to a degree-two vertex it receives only one charge of one; otherwise it has at most two neighbours of degree three, each sending one-half. Thus

`n_5 >= 2 n_2 + n_3`.

By the handshake lemma,

`2e(C) - 4|V(C)| = n_5 - 2n_2 - n_3 >= 0`, hence **`e(C) >= 2|V(C)|`.**

Therefore `e(C)≤17` implies `|V(C)|≤8`.

### Step 2. A finite exact seven/eight-vertex classification

Any graph with `Δ=5` on at most six vertices is a subgraph of the properly five-edge-colourable complete graph `K_6`. The remaining cases are seven and eight vertices.

The portable script `critical5_atlas_verify.py` reads **all** graph6 isomorphism classes from Brendan McKay's pinned original `graph7.g6` and `graph8.g6` datasets. It filters for connected simple graphs with `Δ=5` and at most fifteen edges (seven vertices), or at most seventeen edges (eight vertices). A complete backtracking algorithm tests whether a proper five-edge-colouring exists, choosing the uncoloured edge with the fewest available colours. Global colour names are interchangeable, so the search can safely use existing colours and introduce only the next new one.

| Number of vertices | Total graph classes | Connected candidate classes | Not five-edge-colourable |
|---|---:|---:|---|
| 7 | 1,044 | 337 | 0 with at most 15 edges |
| 8 | 12,346 | 4,362 | 10 with at most 17 edges; **all ten have a degree-one vertex** |

A degree-one vertex is forbidden in an edge-critical graph, so none of the ten eight-vertex exceptions is 5-critical. Thus a 5-critical graph with `e≤17` has **seven vertices**, and must have **at least sixteen edges**.

The graph datasets are copyright Brendan McKay, released under CC BY 4.0 (attribution retained in this directory). Hashes are checked fail-closed by the script. The finite census is exact relative to these complete graph-isomorphism catalogues; it is not an unchecked random search.

## Consequence for the original 24-edge proof

Let `Q` have 17 edges, maximum degree five, and satisfy the two residual Ramsey conditions from `EXACT_JOINT_422_431_PROOF.md`. The second condition implies `Q→(K_{1,4},K_{1,3})`, so `Q` cannot be properly five-edge-colourable. An edge-minimal six-edge-chromatic subgraph `C` of `Q` is 5-edge-critical. By the lemma, `C` has seven vertices and at least sixteen edges. As `Q` has at most one additional edge, it has at most nine nonisolated vertices; but the first residual condition forces an eleven-vertex blue copy of `F(4,3,1)`. Contradiction.

**This removes the need to rely on Kayathri's inaccessible 1994 full text for this fixed theorem.** The only external general result here is Vizing's adjacency lemma. It does **not** certify the fixed theorem automatically: the joint-residual finite classification, both colouring arguments, and manuscript still require review. General Erdős #561 remains open.

## Reproduction

Run `python3 critical5_atlas_verify.py` from the directory containing `fixtures/graph7.g6` and `fixtures/graph8.g6`. Python 3.10+ standard library only. Data references: https://users.cecs.anu.edu.au/~bdm/data/graphs.html . The source SHA-256 values appear in the script and in the repository's `SOURCE_LOCK.md`.
