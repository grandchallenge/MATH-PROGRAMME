# Erdős #561 — sharp matching deficiency and conditional three-star closure

**Research date: 2026-11-19.** The graph-theoretic statements are unconditional deductions from the classical designated-vertex Tutte theorem. The application to the size-Ramsey conjecture remains **conditional on the earlier GCL joint-three-star residual theorem, which is still under review**. We do not claim that unrestricted Erdős #561 has been solved.

## Theorem 1. Sharp designated-vertex matching bound

Let `D≥2` be even and let `G` be a finite simple graph of maximum degree at most `D`. Let `U` be the set of its vertices of original degree exactly `D`, and put `k=|U|`. There exists a matching of `G` covering all but at most

$$
\left\lfloor\frac{k}{D+1}\right\rfloor
$$

vertices of `U`. The bound is sharp for every even `D` and each positive integer `r`: the disjoint union of `r` copies of odd complete graph `K_(D+1)` has `r(D+1)` saturated vertices and every matching leaves at least one unmatched vertex in each copy.

This is an elementary consequence of the designated-vertex Tutte matching criterion (Akiyama and Kano, *Factors and Factorizations of Graphs*, 2007, Theorem 1.4.7). No novelty claim is made about the classical matching theory.

### Proof

For `S⊆V(G)`, let `q_U(G−S)` count the odd-order connected components of `G−S` all of whose vertices belong to `U`. The classical criterion states that a graph has a matching saturating a prescribed set `W` if and only if `q_W(G−S)≤|S|` for every `S`.

Fix any `S`. Each counted component `C` has odd order `c` and all its vertices have degree **exactly `D` in the original graph**. Because it is a component of `G−S`, its only external edges meet `S`.

For `1≤c≤D−1`, simplicity bounds its internal edges and gives

$$
e_G(C,S)=Dc-2e_G(C)\ge Dc-c(c-1)=c(D-c+1)\ge D.
$$

The last inequality holds on the integer interval `[1,D]`, where the concave product is minimized at either endpoint. Call such counted components **small**. Since `D` is even but `c` odd, all remaining counted components have at least `D+1` vertices; call them **large**.

Let `b` and `l` denote the number of small and large counted components. The small components together send at least `Db` edges into `S`, whose total degree is at most `D|S|`, so `b≤|S|`. The large components are disjoint and each consumes at least `D+1` vertices of `U`, so `l≤floor(k/(D+1))`. Therefore

$$
q_U(G-S)=b+l\le |S|+\left\lfloor\frac{k}{D+1}\right\rfloor.
$$

Let `r=floor(k/(D+1))`. Augment `G` with `r` new unmarked vertices, each connected to every vertex of `U`. Call the resulting graph `H`. For any deletion set `X⊆V(H)`, if at least one new vertex survives, all surviving prescribed vertices of `U` belong to a component also containing that unmarked vertex. Hence `q_U(H−X)=0`. If all new vertices are deleted, write `X=S∪{all r new vertices}`; then the previous inequality gives `q_U(H−X)=q_U(G−S)≤|S|+r=|X|`. By the classical designated-vertex Tutte criterion, `H` has a matching covering every vertex of `U`.

Delete the matching edges meeting the `r` new vertices. The remaining original edges are a matching in `G` covering all but at most `r` vertices of `U`. This proves the theorem. **QED.**

For `D=4`, the bound is at most `floor(k_4/5)` missed degree-four vertices. If `e(G)≤29`, the degree sum gives `4k_4≤2e(G)≤58`, so `k_4≤14`. Thus there is a matching which misses **at most two** vertices of original degree four.

### Independent exact validation

`verify_marked_matching_exact.py` checks all 685 NetworkX graph-atlas classes with maximum degree at most four and at most seven vertices, plus 260 seeded larger graphs. It computes maximum designated-vertex matching coverage using its own exhaustive vertex-mask dynamic program, independently examines every deletion set and odd all-marked component, and confirms exact deficiency equality in every test. It additionally verifies sharpness for one, two, three and four disjoint copies of `K5`, up to 20 vertices. Its matching optimum does not rely on NetworkX's built-in matching solver.

## Theorem 2. Two universal avoiding-colouring constructions

Let `G` be any finite simple graph with maximum degree at most four and at most **29 edges**. By Theorem 1, choose a matching `M` leaving at most two vertices of original degree four unmatched; call that set `X`, with `|X|≤2`.

**Construction A: avoid three blue four-edge stars.** Colour every edge of `M` red and every other edge blue. The red graph is a matching, so it contains **no** two-edge star `K_(1,2)`. The only vertices of blue degree four are the unmatched vertices in `X`, at most two. Thus the blue graph cannot contain **three vertex-disjoint copies** of `K_(1,4)`. Consequently this colouring avoids any red target containing a two-edge star and any blue target containing three disjoint four-edge stars.

**Construction B: avoid three red two-edge stars.** Colour all edges of `M` red and additionally colour **every edge incident with a vertex of `X` red**. Colour the rest blue. Every vertex of original degree four now has a red edge, and all other original degrees were already at most three. Thus every blue degree is at most three, so the blue graph contains no four-edge star. After deleting `X`, the red graph is a subgraph of the matching `M`. Accordingly, **every red two-edge star must meet `X`**. Three vertex-disjoint red two-edge stars would have to meet three distinct vertices of `X`, impossible for `|X|≤2`. This colouring avoids three vertex-disjoint red two-edge stars and any blue target containing a four-edge star.

Both constructions are universal over the given degree and edge limits; they do not assume the graph is connected or has bounded order.

**Sharpness of the general 29-edge avoidance guarantee:** The graph `3K5` has 30 edges. In any colouring, either a red two-edge star appears, or the red edges form a matching in each odd clique and one blue four-edge star appears in **each** clique. Therefore a universal avoidance guarantee for `(red K_(1,2), blue 3K_(1,4))` fails at 30 edges. For `(red 3K_(1,2), blue K_(1,4))`, avoiding a blue four-edge star would force every vertex of each odd `K5` to have a red edge, so the red edges in each clique cannot be a matching and must contain a two-edge star. These give three vertex-disjoint red two-edge stars, proving sharpness for the second pair also. We do not infer sharpness for the original three-component target pairs from these simpler examples.

## Theorem 3. Exact closure of the remaining 22 ordered three-star method cases

The previously source-locked `research/erdos-561/even-caps/EVEN_CAP_PARAMETER_CERTIFICATE.json` lists **22 ordered three-star parameter pairs** not previously covered by the programme's colouring arguments (11 up to red/blue reversal). All have forced maximum degree four, and their candidate host edge counts are **at most 23**. There are exactly two classes:

1. **18 ordered cases** have one target equal to `(2,2,2)` (three disjoint two-edge stars), and the other target has at least one four-edge star. Apply **Construction B**, with the `(2,2,2)` target regarded as red. If necessary interchange red and blue. There is no red copy of three disjoint two-edge stars, and there is no blue four-edge star.
2. **4 ordered cases** are `(2,1,1)` versus `(4,4,4)` and `(2,2,1)` versus `(4,4,4)`, including both colour reversals. Apply **Construction A** with the smaller-star forest regarded as red. Its required two-edge star is absent because red is a matching; the blue graph cannot contain three disjoint four-edge stars.

**Every one of the previous 22 method-surviving three-star parameter pairs is therefore excluded**, conditional on the earlier GCL joint-residual hypothesis reducing an original Ramsey counterexample to a graph of exactly `E=W−1` edges and maximum degree `D=n₁+m₁−2`. The entire three-by-three parameter-method shortlist is consequently **empty** for pairs whose two largest target star sizes are both at least two: earlier source-locked arithmetic gates covered the high-degree cases, and the preceding low-degree gates plus this theorem cover the rest.

### Critical dependency and non-claim

This is a **conditional** paper-level conclusion. The upstream joint-three-star residual theorem remains `UNDER_REVIEW` and is neither reproved nor independently certified in this document. We do not cover cases in which one target's largest star has only one edge, and we do not cover arbitrary forests with more than three star components. The unrestricted Erdős #561 conjecture therefore remains **OPEN**. What is now complete is the separate *three-star low-degree edge-colouring obstruction programme*, conditional on the central residual reduction.

## Sources and evidence

- J. Akiyama and M. Kano, *Factors and Factorizations of Graphs* (2007), Theorem 1.4.7 (matching saturating a specified set): https://gorogoro.cis.ibaraki.ac.jp/web/papers/FactorGraphVer1A4.pdf
- Proof provenance: prior `research/erdos-561/unique-core/`, `research/erdos-561/lowdegree/`, `research/erdos-561/unique16/`, and `research/erdos-561/even-caps/` in protected MATH-PROGRAMME.
- `verify_final_three_star_gate.py`: independent exact classification of every one of the final 22 ordered target pairs, including previous source-certificate identity checks.
- `verify_coloring_constructions.py`: independently applies the two colourings to finite simple graphs and checks the required target-avoidance properties.
- `verify_marked_matching_exact.py`: finite exhaustive marked matching and prescribed odd-component deficiency comparisons. No result from this finite test is substituted for the general mathematical proof.
