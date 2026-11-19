# Erdős #561 — uniqueness of the sixteen-edge mixed-degree-cap obstruction

**Research date: 2026-11-19.** This is an unbounded paper proof using the ordinary Lovász `(g,f)`-factor theorem. It strengthens the sharp 16-edge result in source PR #3567, and excludes four further ordered three-star cases **conditionally on the existing paper-level three-star joint-residual theorem**. It does not solve unrestricted Erdős #561 and is not itself a full Lean kernel proof.

## Exact theorem

Let `G` be a finite simple graph of maximum degree at most three with exactly sixteen edges. Suppose its edges cannot be partitioned into red and blue such that every vertex has red degree at most one and blue degree at most two.

**Theorem.** Up to isolated vertices and graph isomorphism, `G` is uniquely determined. Take two disjoint copies of `K5` with the three edges `(0,1)`, `(0,2)`, `(3,4)` deleted in each copy. Their designated vertex 0 has degree two internally and all their other vertices have degree three. Add a new vertex `x`, and connect it to the designated vertex in each copy. The resulting graph has eleven nonisolated vertices and sixteen edges. No other graph with sixteen edges and maximum degree at most three violates the `(1,2)` edge-degree caps.

Equivalently, the unique obstruction is a pair of five-vertex, seven-edge blocks attached to one common degree-two cut vertex by one edge each.

## Proof

The earlier source-locked mixed-cap theorem establishes that any graph lacking a `(1,2)` capped partition has **at least ten degree-three vertices**. Each contributes three incidences, while `2|E(G)|=32`. Thus the number of degree-three vertices must equal ten (eleven would require at least 33 incidences). These ten vertices account for 30 of the 32 total incidences. The remaining nonisolated vertices are therefore either **one vertex of degree two** or **two vertices of degree one**.

Use the **ordinary** Lovász `(g,f)` factor criterion with `g(v)=max(0,d(v)−2)` and `f(v)=min(1,d(v))`. The cap partition fails, so there exist disjoint sets `S,T` for which the integer cut value `A(S,T)` satisfies `0≤A<q`. Here `q` counts components `C` of `G−(S∪T)` that are tight at every vertex (`g=f`) and satisfy the exact oddness condition `f(C)+e(C,T)` odd. A contributing component contains only degree-three vertices, since degree-zero isolated components never have odd parity. Let `U=V(G)−(S∪T)`.

The scaled cut bound from the ordinary factor theorem is

$$
3A\ge e(S,U)+2e(T,U).
$$

For any counted component `C`, put `s_C=e(C,S)`, `t_C=e(C,T)`, and `c=|C|`. Its parity condition says `c+t_C` odd. Since every vertex of `C` has degree three, the degree-sum parity identity also says `c≡s_C+t_C (mod 2)`. Subtracting yields **`s_C` odd**. Thus `s_C≥1`. For **even** `c`, `t_C` must be odd and at least one, so the *weighted boundary* `w_C=s_C+2t_C≥3`. For **odd** `c`, `w_C≥1`.

If `c≤3`, the simplicity/degree bound gives `s_C+t_C≥c(4−c)≥3`, hence `w_C≥3` regardless of parity. We call these components *small*; counted components of order at least four are *large*.

The earlier connected degree-core argument guarantees at least one large counted component. It also proves **exactly one large component is impossible** here: every other counted component pays at least three weighted boundary units, whereas `A≤q−1`, forcing the large component's own boundary to be zero. This would make it an isolated **odd-order three-regular graph**, impossible by the handshake identity. Therefore the violated cut must have **at least two** large counted components.

There are exactly ten degree-three vertices in total. Two large components must have sizes from the following possibilities (allowing further small counted components only if the total size stays ≤10): `(4,4)`, `(4,5)`, `(4,6)`, `(5,5)`, together with possible small counted components in `(4,4)` or `(4,5)` cases. Every even large component contributes at least three weighted boundary units, every odd large component at least one, and every small component at least three. Since `A≤q−1`, the total weighted boundary cannot exceed `3(q−1)`. The **only** size profile satisfying that inequality is **exactly two large components of sizes `(5,5)` and no other counted components**. The independent integer enumeration in `verify_cut_profiles.py` checks this over all 72 possible relevant size partitions with at most ten saturated vertices.

Both five-vertex components are odd, so each has **odd** weighted boundary `w_C=s_C+2t_C`. The two weights are positive, and their sum is at most `3(q−1)=3`. Thus both equal one. Consequently **each five-vertex component has precisely one edge into `S`, none into `T`**. They have no edges into each other, since they are distinct components of `G[U]`.

The degree-three vertices in each component have total degree fifteen; with one external edge, the induced five-vertex graph has exactly `(15−1)/2=7` edges, with internal degrees `(2,3,3,3,3)`. Such a graph is uniquely isomorphic to `K5` after deleting three edges forming a length-two path plus a disjoint edge: the complement-degree sequence is `(2,1,1,1,1)` and the complement must contain a path on three vertices and an edge on the other two. The two components therefore use fourteen internal edges and their two boundary edges use the remaining two edges of `G`. `verify_five_vertex_block.py` independently checks all 1,024 labelled five-vertex simple graphs: exactly 30 have the required seven-edge internal degree profile, and all 30 are isomorphic to this unique block.

Because all ten degree-three vertices are inside these two components, the vertices in `S∪T` have total degree exactly two. The two boundary edges both end in `S`; also `e(S,T)=0` and `T` contains no positive-degree vertex. Thus `A(S,T)` equals the number of nonisolated vertices in `S`. Since `0≤A<q=2`, while `S` contains an endpoint of each boundary edge, **`A=1`**. Both boundary edges therefore end at **the same vertex `x`**, whose degree is two. No further nonisolated vertices or edges exist.

This proves the claimed unique graph structure. Its failure of the capped colouring is immediate: the red edges would have to form a matching covering the ten degree-three vertices; each odd five-vertex block must use its unique external edge, but those two edges share `x`, a contradiction. **QED.**

## Consequence for the last low-degree three-star parameters

The unique obstruction graph admits a different two-colouring that **avoids any two three-star targets whose largest star has at least two edges**, even though this colouring is *not* capped at degrees (1,2). Colour the first seven-edge block and its attachment to `x` red. Colour the second block and its attachment blue. Each colour has exactly eight edges but, crucially, touches only **six vertices**: the five vertices of its block and the common cut vertex `x`. Every three-star forest with three positive star components and one star of size at least two needs at least

$$
(2+1+1)+3=7
$$

vertices. Therefore neither colour can contain the relevant target forest.

Within the previous **39 ordered low-degree method-survivors** there are exactly four cases with forced degree three and exactly `E=W−1=16` edges:

- Red triple `(2,2,1)` versus blue triple `(3,3,2)`;
- Red `(2,2,2)` versus blue `(3,2,1)`;
- Their two colour-reversed counterparts.

By the uniqueness theorem, a graph in any of these four scenarios that fails the degree-capped partition must be the unique sixteen-edge obstruction. The explicit six-vertex-support colouring above avoids both target forests, so it cannot arrow either pair. Thus these **four ordered cases are excluded**, conditional only on the previously admitted (but not yet independently certified) joint-three-star Ramsey reduction that forces `E=W−1` edges and maximum degree three in a hypothetical original counterexample.

The resulting method-survivor list has **35 ordered cases, or 18 up to reversing red and blue**. Of these, **10** have forced maximum degree three and **25** have forced maximum degree four. They are remaining cases for this specific programme of arguments, **not** a claim of 35 intrinsically open theorems.

## Exact supporting verification

The self-contained `verify_cut_profiles.py` independently enumerates all 72 relevant positive component-size partitions of at most ten degree-three vertices, including every partition with a component of size at least four. Using the proved parity and simple-graph boundary constraints, it finds the **only** size profile consistent with a violated factor cut is `(5,5)` with both components having weighted boundary one. This verifies the finite case classification used in the general paper argument; it does not replace the underlying ordinary Lovász theorem.

The independent `verify_motif_colorings.py` reconstructs the canonical sixteen-edge graph from first principles, checks all graph-degree counts and edge uniqueness, verifies the two six-vertex-support colour classes, reads the exact source-locked prior 39-case list, and derives precisely the four named additional ordered exclusions. The source SHA-256 certificate and replay matrix record the computations.

**Certification boundary:** The general uniqueness theorem is a complete paper deduction from the published ordinary Lovász `(g,f)`-factor theorem, not a fully Lean-verified formalization. The Ramsey corollary depends on the separate three-star joint-residual theorem, still stored as a paper-level `UNDER_REVIEW` claim. Neither provides a resolution of the unrestricted Erdős #561 conjecture. A GCL specialist may adjudicate the substantive claim within the existing internal review policy without creating repetitive preliminary approval gates.

**Later strengthening in the same research package:** `SIXTEEN_TO_EIGHTEEN_CORE_THEOREM.md` extends this motif containment to 17 and 18 edges and excludes ten further ordered three-star cases; the **current** method-survivor list is **25 ordered / 13 unordered**, all of forced maximum degree four. The 35/18 count above is the **intermediate** 16-edge-only result.
