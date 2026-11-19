# Erdős #561 — sharp obstruction to universal apex–forest rigidity

**Date:** 2026-11-18. **Programme:** GCL MATH-PROGRAMME, #3490.
**Research status:** Complete mathematical counterexample to the proposed *universal structural hypothesis* (not a counterexample to Erdős #561); paper-level constructive replacement theorem; exact bounded verifier. No novelty or public certification claim.

## 1. The claim that fails

The assertion that *every optimal graph arrowing two star forests must become a forest when enough of its maximum-degree vertices are removed* is false. Even allowing **all** maximum-degree vertices to be deleted does not rescue it. Restricting to arbitrary deletion sets of **bounded cardinality independent of the target number of components** also fails.

### Exact infinite family: triangles mixed with stars

Let `P3=K_{1,2}`. For any integers `s,t≥1`, put `N=s+t−1`. For `0≤c≤N`, define

`G(s,t,c)=c K3 ⊔ (N−c) K_{1,3}`.

**Theorem 1 (classical, with independent direct arrowing proof).**

1. `G(s,t,c) -> (s P3, t P3)` and `e(G)=3N`.
2. Burr–Erdős–Faudree–Rousseau–Schelp, *Ramsey-minimal graphs for multiple copies* (1978), Theorem 1, proves `rhat(s P3,t P3)=3(s+t−1)` and classifies the optimal uniform-star hosts as exactly these star/triangle mixtures (up to isolated vertices). Thus **every** `G(s,t,c)` is globally edge-count optimal, not merely a constructed upper bound.
3. Every edge is Ramsey-essential: deleting any single edge permits a colouring with no red `sP3` and no blue `tP3`.
4. The feedback vertex number `τ(G)`—minimum number of vertices whose deletion makes `G` a forest—is **exactly** `c`. Its `c` vertex-disjoint triangles each need an independent deletion, and deleting one vertex from each suffices.
5. For `1≤c≤N−1`, `Δ(G)=3`, and the degree-three vertices are precisely the centres of the `(N−c)` stars. They meet no triangle. Therefore **no subset whatsoever of the maximum-degree vertices makes the remainder a forest**.
6. For `c=N`, `Δ(G)=2` and the minimum number of maximum-degree vertices needed to leave a forest is `N`, unbounded as `s+t` grows.

**Direct proof of (1).** In any 2-colouring of the three edges of `K3` or `K_{1,3}`, two of them have the same colour and share a vertex. Thus each connected component provides a monochromatic `P3`. With `s+t−1` components, either at least `s` provide red paths or at least `t` provide blue paths. Components are vertex-disjoint, hence so are the selected paths. All components have exactly three edges.

**Direct proof of (3).** After deleting any edge, the affected three-edge component becomes a two-edge path or two-edge star. Colour one of its edges red and the other blue; it supplies no monochromatic `P3`. Colour `s−1` of the other `N−1` components all red and the remaining `t−1` all blue. Neither required forest occurs.

**Smallest explicit mixed example:** `G=K3 ⊔ 2 K_{1,3}` has nine edges, arrows `(2P3,2P3)`, and is globally size-optimal by the original 1978 theorem. Its maximum-degree centres are disjoint from its triangle.

**Source lock:** Original 1978 article, `https://users.renyi.hu/~p_erdos/1978-38.pdf`, fetched with HTTP 200 via CHAD on 2026-11-18, byte count **797,122**, SHA256 **`b7af965c7eefa6ad427043cebe1c17d6a30a6c72e53ec3862814459df7ed9229`**, CHAD capture `ba5c91deb1cf428b8d97fd4c0e4c509d`. Independent historical restatement: `https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/SizeRamseyStars.html`.

### Exact mechanism: two different ways to force the pigeonhole count

- The `K_{1,3}` atom has maximum degree **3**, which is one more than the sum of the red and blue degree caps `1+1=2`. It forces a monochromatic `P3` by **degree overflow**.
- The `K3` atom has maximum degree **2**, exactly equal to the combined caps, but is **Class II**: its edges cannot be properly coloured with two colours because the cycle is odd. It forces a monochromatic `P3` by **parity**.
- Arbitrary mixtures of these two different obstruction mechanisms remain globally optimal. Hence a forest-only normal form discards genuine extremizers.

This is the **precise failure** of the proposed universal apex–forest hypothesis. It does **not** show that a hypothetical graph with fewer than the conjectured edge count exists or that a still stronger subcritical-only structure theorem is false. If Erdős #561 holds, no subcritical arrowing graph exists at all.

## 2. A replacement theorem with no forest assumption

Write `χ'_ℓ(H)` for the *list chromatic index*: the least q for which every assignment of at least q allowed colours to each edge of H admits a proper edge-colouring from the assigned lists.

**Theorem 2 (apex-to-list-colouring, elementary).** Let G be a finite simple graph with `Δ(G)=D`, and let `U⊆V(G)` be an **independent** set of k vertices. Put `H=G−U`. If

`χ'_ℓ(H) ≤ D−2k`,  **then** `χ'(G)=D`.

**Proof.** The graph B consisting of edges incident with U is bipartite, with `Δ(B)≤D`. By König's line-colouring theorem, colour B properly with D colours. For each edge `xy∈H`, disallow colours already incident with x or y in B. Each endpoint is incident with at most k edges of B, so at least `D−2k` colours remain. The definition of `χ'_ℓ(H)` supplies a compatible proper colouring of H. Combined with B this properly colours G with D colours. Since Δ(G)=D, equality holds. ∎

Thus **low list-edge-colouring complexity**, not necessarily acyclicity, is the usable structural condition. Several convenient elementary corollaries follow.

**Corollary 2a (forest, previously established):** If H is a forest with maximum degree r, then `χ'_ℓ(H)=r` for nonempty H, by leaf-edge induction. So `D≥2k+r` suffices.

**Corollary 2b (new pseudoforest formulation):** If H is a *pseudoforest* (each connected component contains at most one cycle), with maximum degree r≥2, then `χ'_ℓ(H)≤max(3,r)`. Consequently,

`D ≥ 2k + max(3,r)  ⇒  χ'(G)=D`.

**Proof.** Repeatedly peel leaves from H. The remaining core is a disjoint union of cycles. On each cycle, colour edges in cyclic order from their lists of at least three colours: every edge but the last has at most one coloured cycle neighbour, while the last has at most two. Then restore the peeled leaf edges in reverse order. When restoring an edge, only its nonleaf endpoint can have previously coloured H edges, at most `r−1`, so any list of at least r colours suffices. The lists also avoid the precoloured edges of B. ∎

For r≥3 this is **the same numerical threshold as the forest case**. The cost of admitting an odd cycle is concentrated at residual degree two: an odd cycle has list chromatic index exactly **3**, versus maximum degree **2**. That is the same tight parity obstruction exhibited by the 1978 extremizers.

**Corollary 2c (unrestricted residual graph):** If Δ(H)≤r and `D≥2k+2r−1`, then `χ'(G)=D`, without assuming any restriction on cycles. Indeed, each edge of H is adjacent to at most `2r−2` other H edges, and greedy list-edge colouring works from lists of size `2r−1`.

The thresholds are *sufficient*, not necessary, and may be conservative. No historical novelty is claimed for these elementary edge-colouring consequences.

## 3. What a genuine subcritical counterexample would have to satisfy

Let target forests `F(n_1,...,n_s)`, `F(m_1,...,m_t)` have `s,t≥2`. Let `W=Σ_{j=2}^{s+t} w_j` be Erdős's conjectured value and `w_2=n_1+m_1−1`. Define `J` as the minimum edges of a graph satisfying **both** vertex-deleted residual Ramsey relations (the joint-residual target in #3490).

**Proposition 3 (conditional degree/class-II pinning).** Assume the still-open general joint inequality `J≥W−w_2`. If a graph G arrows the original pair with `e(G)≤W−1`, then necessarily

- `e(G)=W−1`,
- `Δ(G)=w_2−1=n_1+m_1−2`,
- `J=W−w_2`, and **every maximum-degree vertex deletion** gives a joint-residual extremizer, and
- `χ'(G)=Δ(G)+1`: G is **Class II**.

**Proof.** Arrowing the two forests implies arrowing `(K_{1,n_1},K_{1,m_1})`. If `Δ(G)≤n_1+m_1−3`, Vizing's theorem properly colours edges with at most `(n_1−1)+(m_1−1)` colours. Assign the first `n_1−1` matching colours red and the rest blue; this avoids both large stars and hence both forests. Therefore `Δ(G)≥w_2−1`. Choose a maximum-degree vertex v. Vertex deletion gives both residual arrowing relations, hence `e(G)−Δ(G)≥J≥W−w_2`. Combining with `e(G)≤W−1` yields `Δ(G)≤w_2−1`. All inequalities are equalities, proving the first three assertions. If G were properly edge-colourable with Δ(G) colours, partition the `Δ=n_1+m_1−2` colour classes in the same way to defeat the Ramsey property. Thus `χ'(G)>Δ(G)`, and Vizing bounds it by `Δ(G)+1`. ∎

If `J>W−w_2`, the same argument proves **no** subcritical G exists; that parameter instance is settled without classification. If `J=W−w_2`, the correct next structural target is a **Class-II critical core**, not necessarily a forest after deleting maximum-degree vertices. The fixed `(4,2,2)` vs `(4,3,1)` proof followed this pattern.

## 4. Decision and experiments

1. **Reject** the universal maximum-degree-apex-to-forest conjecture: it is disproved by the 1978 globally optimal uniform family.
2. **Retain** the stronger subcritical-only programme as genuinely open, not falsely refuted by optimal hosts.
3. Replace a compulsory forest condition by list-edge-colouring certificates: sufficient tests `D−2k≥χ'_ℓ(H)`, forest `r`, pseudoforest `max(3,r)`, general graph `2r−1`.
4. Prioritize #3490's joint-residual inequality. Its equality regime forces exactly a **Class-II** potential counterexample. Extract and rule out critical Class-II subgraphs using degree/edge budgets and residual arrowing information, including parity corrections.
5. Continue source-locked, adversarial proof review; no protected theorem certification or full-conjecture closure is justified.

## Reproducibility

- `verify_parity_obstruction.py`: 20 small mixed-family cases, all red/blue colourings, explicit Ramsey-avoiding witnesses after every edge deletion; checks max-degree and feedback count claims.
- `pseudoforest_apex_colouring.py`: constructive König/Kempe precolouring plus cycle-first and leaf-restoration list-colouring; tests the theorem at the exact threshold and one extra colour for k=1..4 and r=2..5.
- `results.json`: exact outputs, controlled seed, SHA256 checksums in `SHA256SUMS.txt`.

**Claims ledger:** The 1978 optimality/classification is `LITERATURE_DERIVED`; the explicit non-apex counterexample, Class-II pinning proposition and list-colouring lemma are `PROVED_IN_PACKAGE` (ordinary paper proofs), and their computational trials are `COMPUTED_EXACTLY` for bounded domains. General #561 and general #3490 joint inequality remain **OPEN**.