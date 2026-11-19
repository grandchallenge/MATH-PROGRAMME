# Erdős #561 — all subcubic obstructions through eighteen edges contain one motif

**Research date: 2026-11-19.** This is a general paper proof from the ordinary Lovász `(g,f)`-factor theorem, extending the unique sixteen-edge obstruction classification. The three-star Ramsey consequences depend on the existing unpromoted joint-residual reduction. The unrestricted conjecture remains OPEN.

## Structural theorem (16–18 edges)

Let `G` be a finite simple graph, with maximum degree at most three, and between **16 and 18 edges**. If the edges cannot be red/blue coloured so that red degrees are at most one and blue degrees at most two, then `G` **contains** the unique sixteen-edge obstruction as a spanning subgraph of its nontrivial degree-three core. All remaining `|E(G)|−16` edges lie outside its two five-vertex blocks (they may touch the central degree-two vertex of the motif). In particular, at most two extra edges remain, and neither can meet any vertex in a five-vertex block.

The motif consists of two disjoint five-vertex seven-edge graphs, each a `K5` with a two-edge path and a disjoint edge removed, with each block's unique degree-two vertex attached by one edge to the **same** central vertex `x`. This is exact at 16 edges; at 17 or 18 edges the extra edges may be present only outside the two blocks. The central vertex has degree two *inside the motif*, though it may acquire one additional edge in the larger graph.

### Proof

The previously proved 15-edge sharpness theorem shows that failure of degree caps `(1,2)` requires at least ten degree-three vertices. Since the graph has at most 18 edges, the handshake identity bounds the number of degree-three vertices by twelve.

Choose the standard ordinary Lovász `(g,f)`-factor obstruction for caps one and two. For a violated cut, write `A<q` where `A` is a nonnegative integer and `q` is the number of tight parity-odd components. Every such component consists entirely of degree-three vertices, and its edge counts to the cut sides `S,T` satisfy the congruence

$$
|C|+e(C,T)\equiv1\pmod 2.
$$

The degree-sum identity says `|C|≡e(C,S)+e(C,T) (mod 2)`, so `e(C,S)` is odd. For even component size, `e(C,T)` is odd as well. Consequently every counted component of even size has weighted boundary `e(C,S)+2e(C,T)≥3`, every odd component has boundary weight at least one, and every counted component of size at most three has weighted boundary at least three by the simple-graph degree bound.

The ordinary factor cut inequality gives

$$
3A\ge e(S,U)+2e(T,U),\qquad U=V(G)\setminus(S\cup T).
$$

Since `A≤q−1`, the total weighted boundary of all counted components is at most `3(q−1)`.

There must be a counted component of order at least four, by the connected high-degree-core argument. If it were the **only** such large component, all other counted components would contribute at least `3(q−1)`, forcing the large component's boundary to zero. Its counted parity would then require an isolated **odd-order cubic graph**, impossible by the handshake identity. Hence at least **two large counted components** exist.

The sizes of all counted components total at most twelve. For each size `c`, the constraints `0≤e(C)≤c(c−1)/2`, `3c=2e(C)+e(C,S)+e(C,T)` and `c+e(C,T)` odd provide exact lower bounds on weighted and unweighted boundary. The resulting small finite case analysis leaves only four types satisfying the weighted cut inequality:

- exactly two components of sizes `(5,5)`;
- three components of sizes `(1,5,5)`;
- four components of sizes `(1,1,5,5)`;
- two components of sizes `(5,7)`.

The final three cannot occur within an 18-edge graph. They require at least five, eight and two edges, respectively, leaving their counted components; but the total degree *outside* those counted components is at most `36−3·11=3`, `36−3·12=0`, and `36−3·12=0`. Therefore no vertices outside the components have enough available degree to receive the required boundary edges. These impossibilities hold a fortiori at 16 or 17 edges.

Thus `q=2`, and the only counted components are **two five-vertex components**. Each has an **odd positive** weighted boundary; their weights sum to at most `3(q−1)=3`, so both weights must equal one. Consequently each component has exactly **one edge into `S` and no edges into `T`**, and exactly seven internal edges. Its five internal degrees are `(2,3,3,3,3)`, which uniquely determines the seven-edge block. These two blocks plus their external attachment edges already account for **16 edges**.

There are at most two additional edges, and no further edge can meet either block, because all ten block vertices already have degree three. Every vertex of `T` consequently has degree at most two: it has no attachment to either block and may be incident to only those two additional edges. Hence `min(2,d(t))=d(t)` for all `t∈T`. In the Lovász cut formula,

$$
A=\sum_{s\in S}\min(1,d(s))+\sum_{t\in T}d(t)-e(S,T),
$$

the final two terms have nonnegative sum (the total degree of `T` is at least its edges to `S`). Therefore `A≥` the number of nonisolated vertices in `S`. As `A<q=2`, exactly **one** nonisolated vertex lies in `S`. The two attachment edges must consequently meet the **same** vertex `x`.

We have exhibited the exact canonical sixteen-edge obstruction as a subgraph. All remaining edges avoid both five-vertex blocks by degree saturation and may involve only `x` or vertices outside the motif. **QED.**

### Independent finite audit

`verify_16to18_cut_profiles.py` computes every integer partition of at most twelve counted degree-three vertices with at least two components of order at least four: **34 profiles** at each edge budget 16, 17 and 18. It independently applies both the weighted factor-cut bound and the total-degree-outside-the-components bound. Only `(5,5)` remains, exactly as claimed. This checks the finite combinatorial portion, without replacing Lovász's published theorem.

## Three-star forest consequence: the entire degree-three shortlist

Let the red and blue targets each consist of **three positive-size stars** and have leading star size at least two. Every such forest needs at least seven vertices. In the two-block motif, colour the first block and its attachment edge red and the second block and its attachment blue. Each colour touches only six vertices. Give all `r=|E(G)|−16≤2` remaining exterior edges to whichever target colour has enough vertex demand. The receiving colour touches at most **`6+2r`** vertices, because an edge can introduce at most two new vertices; the other colour still touches six vertices. Thus the colouring avoids both targets whenever one target requires more than `6+2r` vertices and the other requires more than six.

In the previous exact 39-case ledger, exactly **six** ordered cases have forced degree three and exactly `E=17` edges, and exactly **four** have forced degree three and `E=18` edges. Each meets the preceding inequality in at least one colour orientation. The exact pairs and assignments are listed in `SIXTEEN_TO_EIGHTEEN_PARAMETER_CERTIFICATE.json`. Moreover, `verify_16to18_colorings.py` exhaustively constructs **all** possible outside-edge placements, up to relabelling, using the central vertex and four fresh vertices: ten one-edge placements and 39 permitted two-edge placements per target pair, for **216 graph/target combinations**. It checks each graph is simple and remains subcubic, and verifies both colour classes have too few available vertices for their corresponding target forest.

The original sixteen-edge result already excludes four ordered pairs. The new seventeen/eighteen-edge theorem excludes **ten more**, for **fourteen total** exclusions from the earlier 39 low-degree method-survivors. Therefore the current exact shortlist is:

| Class | Ordered method-survivors | Up to swapping red and blue |
| --- | ---: | ---: |
| Forced maximum degree 3 | **0** | **0** |
| Forced maximum degree 4 | **25** | **13** |
| **Total** | **25** | **13** |

These conditional Ramsey conclusions rely on the previously admitted (but mathematically unpromoted) joint-three-star residual theorem to reduce a hypothetical original arrowing counterexample to `E=W−1` edges and exact maximum degree. The **graph-structural theorem itself** does not require that Ramsey premise. The unrestricted Erdős #561 conjecture, arbitrary larger star-forest component counts, and the remaining degree-four three-star cases are **not resolved by this work**.
