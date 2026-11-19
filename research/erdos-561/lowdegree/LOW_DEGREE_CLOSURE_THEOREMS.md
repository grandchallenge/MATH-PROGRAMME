# Erdős #561 — sharp mixed-cap subcubic bound and complete degree-2 finite gate

**2026-11-19.** Research evidence. The finite-graph statements below are independent of the size-Ramsey conjecture. Applying them to a hypothetical size-Ramsey counterexample uses the earlier GCL paper-level joint three-star residual theorem, **which remains under mathematical review**. Do not promote the overall conjecture to solved.

## 1. The sharp sixteen-edge obstruction for degree caps (1,2)

**Theorem.** Every finite simple graph `G` with maximum degree at most three and at most **15 edges** can be edge-coloured red/blue so that red has maximum degree at most one and blue has maximum degree at most two. The bound on edges is sharp: an explicit 16-edge simple graph with maximum degree three admits no such colouring.

In fact, the preliminary maximum-degree result is stronger: any subcubic graph with at most **nine degree-three vertices** has a (1,2)-capped colouring.

### The maximum-degree count: why nine vertices suffice

Use the ordinary Lovász `(g,f)`-factor condition already source-locked in MATH-PROGRAMME. For `D=3`, `alpha=1`, `beta=2`, a failed partition produces disjoint vertex sets `S,T` and a positive number `q` of special connected components of `G−(S∪T)` for which `A(S,T)<q`. Here `A` is a nonnegative integer and its weighted edge-boundary inequality says

$$
3A\ge e(S,U)+2e(T,U),\qquad U=V(G)\setminus(S\cup T).
$$

Each counted component `C` consists entirely of degree-three vertices (isolated degree-zero vertices contribute zero parity). Its parity criterion is

$$
|C|+e(C,T)\equiv1\pmod 2.
$$

Since all its vertices have degree three, the graph handshake identity also gives

$$
3|C|\equiv e(C,S)+e(C,T)\pmod 2.
$$

Combining the two congruences shows that **`e(C,S)` is odd**, so it is at least one. If `|C|` is even, `e(C,T)` is also odd and therefore at least one. Consequently a counted component's weighted boundary `b(C)=e(C,S)+2e(C,T)` is at least **three for even-sized components**, and at least **one for odd-sized components**.

The earlier general core lemma shows that a violated cut has a counted component of at least four degree-three vertices. If there is just one such *large* component, all other counted components have at most three vertices and supply at least three units of weighted boundary each. Since `A≤q−1`, the large component must have zero boundary, so it is an isolated three-regular graph whose counted parity forces odd order. But a three-regular graph on an odd number of vertices is impossible by the handshake lemma.

Suppose there are at least two large counted components. With **at most nine degree-three vertices**, there can be exactly two, of orders (4,4) or (4,5), with possibly a third counted singleton only in the (4,4) case. The weighted boundary of a counted four-vertex component is at least three, and that of a counted five-vertex component is at least one:

- (4,4) with `q=2` has weighted boundary at least six, exceeding `3(q−1)=3`.
- (4,5) with `q=2` has weighted boundary at least four, again exceeding three.
- (4,4,1) with `q=3` has weighted boundary at least `3+3+3=9`, exceeding `3(q−1)=6`.

Each possibility contradicts the ordinary factor cut inequality `3A≥weighted boundary` and `3A≤3(q−1)`. Therefore every graph with at most nine degree-three vertices has a capped colouring. QED.

### Why fifteen edges suffice

Suppose an uncolourable graph has at most 15 edges. The preceding result forces **at least ten degree-three vertices**. Their combined degrees are at least 30, but the whole graph has degree sum at most 30. Equality is therefore forced: it has exactly 15 edges, exactly ten nonisolated vertices, and is three-regular on those ten vertices.

We now use **Tutte's perfect matching theorem**, and show directly that every simple cubic graph without a perfect matching must have at least 16 vertices. Suppose `S` is a Tutte obstruction in such a cubic graph, with `s=|S|` and `q` odd components of `G−S`. Since the number of vertices of a cubic graph is even, `q` and `s` have the same parity; Tutte's failure requires `q≥s+2`.

Every odd component `C` of `G−S` has an **odd positive** number of edges into `S`, by the handshake identity. If `|C|≤3`, the boundary has at least three edges, because a simple graph on at most three vertices has at most three internal edges. Let `h` count the odd components of order at least five, and let `q−h` be the smaller ones. The sum of all these boundary edges is at least

$$
3(q-h)+h=3q-2h,
$$

but it cannot exceed `3s`, the total degree capacity of vertices in `S`. Since `q≥s+2`, these two inequalities imply `h≥3`. Consequently the cubic graph has at least **three disjoint odd components of order five**, plus at least one vertex in `S`: at least `3·5+1=16` vertices. (The set `S` cannot be empty, because cubic connected components have even order.) This contradicts ten vertices.

Thus every ten-vertex cubic graph has a perfect matching. Colour its matching edges red and the remaining edges blue; all red degrees equal one and all blue degrees equal two. Contradiction. Hence **15 edges cannot obstruct the (1,2)-capped colouring**. QED.

### Sharpness at 16 edges

Take two disjoint five-vertex graphs each obtained from `K5` by deleting three edges: `(0,1)`, `(0,2)` and `(3,4)`. The designated vertex 0 has internal degree two, and the other four vertices have degree three. Add a new center vertex `x` connected to vertex 0 in each five-vertex block. The resulting simple graph has **11 vertices, 16 edges, ten degree-three vertices and one degree-two vertex**.

Any (1,2)-capped colouring would require a red matching covering all ten degree-three vertices. Each five-vertex block is odd and must use its one external edge to be completely covered; but the two external edges meet at `x`, so the matching cannot use both. This is impossible. `verify_cubic_sharpness.py` checks all 65,536 edge subsets for a matching that covers all saturated vertices, verifies degree counts and the explicit Lovász cut witness `A=1<q=2`. Thus the 16-edge bound is sharp.

## 2. All degree-two original three-star candidates: finite exhaustive gate

Every simple graph of maximum degree at most two, ignoring isolated vertices, is a disjoint union of paths with one or more edges and cycles with at least three edges. For any fixed number `E` of edges, this gives **a complete enumeration of graph isomorphism types** by multisets of path and cycle lengths summing to `E`.

For target star forests with three components and largest size two, their component-edge triples are among `(2,1,1)`, `(2,2,1)` and `(2,2,2)`. The standalone C++17 checker `verify_degree2_exhaustive.cpp` enumerates all graphs of maximum degree at most two with exactly `W−1` edges for each distinct unordered target pair. For every graph, it tests all red/blue assignments **exactly**, using a component-union test to recognize the three disjoint target stars and a downward-subset dynamic program to detect each monochromatic target. It reports at least one avoiding colouring for every graph type.

| Target triples | Edges `W−1` | Graph types exhaustively checked | Arrowing counterexamples |
| --- | ---: | ---: | ---: |
| 211 vs 211 | 8 | 46 | 0 |
| 211 vs 221 | 10 | 106 | 0 |
| 211 vs 222 | 12 | 232 | 0 |
| 221 vs 221 | 11 | 156 | 0 |
| 221 vs 222 | 13 | 334 | 0 |
| 222 vs 222 | 14 | 482 | 0 |
| **Total** | — | **1,356** | **0** |

Reversing red and blue covers the remaining three ordered cases. Every hypothetical graph with **fewer** than `W−1` edges can be padded to `W−1` edges by isolated single-edge components, without increasing maximum degree above two or destroying arrowing. Consequently these six cases cover **all nine ordered pairs** in the degree-two shortlist, provided the earlier joint-residual deduction forcing maximum degree two for a minimal hypothetical counterexample is valid.

## 3. Source-corrected literature audit

An external source check on **2026-11-19** found an important time/version hazard. Fu, Luo and Ni's arXiv record `2606.04439` initially bore the title *Size Ramsey number for star forests* (June 3, 2026), with an abstract claiming to settle the whole conjecture. **That is not the current paper.** The July 4, 2026 revision **v3** is titled *Size Ramsey minimal graphs for uniform star forests* and its stated new theorem characterizes minimal graphs for **uniform** star forests in several colours. It does **not** assert a proof of the unrestricted nonuniform Burr–Erdős–Faudree–Rousseau–Schelp conjecture. Version-sensitive literature should refer to the v3 source, not the stale v1/v2 abstract. Exact source: https://arxiv.org/abs/2606.04439 (current v3); version history https://arxiv.org/abs/2606.04439v3 . The Erdős #561 problem page still lists the general conjecture as open: https://www.erdosproblems.com/561 .

The published 2025 paper by Davoodi, Javadi, Kamranian and Raeisi, *On a conjecture of Erdős on size Ramsey number of star forests*, **Ars Mathematica Contemporanea** 25 #P2.09 (DOI https://doi.org/10.26493/1855-3974.3081.d6c) proves three particularly relevant exact cases: both target forests uniform (earlier Burr et al. 1978); all component sizes on both sides odd (Theorem 2.5); and one side consists of equal odd stars against another forest whose largest size is odd and **whose smallest component has size at least two** (Theorem 2.6). The last positivity condition is material and must not be silently dropped. Accessible text: https://www.researchgate.net/publication/383374379_On_a_conjecture_of_Erdos_on_size_Ramsey_number_of_star_forests .

`verify_lowdegree_ledger.py` applies only these **explicitly grounded hypotheses** to the exact 75 ordered cases from the previous source-locked research certificate. Twelve ordered pairs are covered by these earlier publications. Among them one also falls within the new degree-two exhaustive gate; thus **11** published cases add genuinely new coverage after our low-degree gates.

## 4. Exact partition of the prior 75 research candidates

| Category | Ordered pairs |
| --- | ---: |
| Prior method-survivors | 75 |
| New exhaustive degree-two gate | 9 |
| New sharp subcubic sixteen-edge gate | 16 |
| Already covered by published special theorems | 12 |
| Overlap between new and published cases | 1 |
| **Remaining not settled by these specified arguments** | **39** |

The 39 entries consist of **14 forced-degree-three** and **25 forced-degree-four** ordered parameter pairs; up to reversing the two colours, they comprise **20** cases. The machine-readable `LOWDEGREE_75_CASE_LEDGER.json` gives the complete pair list, proposed source coverage and the exact reason each entry is retained or excluded. These 39 are **not automatically 39 mathematically open problems**; other known results or new colourings may cover further cases.

**Boundaries.** The general graph-theoretic subcubic theorem is proved on paper using the already audited ordinary Lovász factor criterion and classical Tutte matching theorem. It is not machine formalized end-to-end in Lean. The degree-two part is a complete finite combinatorial enumeration using an independently inspectable deterministic C++ program. The mathematical Ramsey corollaries continue to depend on the earlier three-star joint residual theorem, which remains a source-locked **paper-level** claim. The unrestricted Erdős #561 conjecture is not solved by this package.
