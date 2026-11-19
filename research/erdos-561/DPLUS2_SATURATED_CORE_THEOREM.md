# Erdős #561 — sharp D+2 maximum-degree core theorem and 3×3 consequences

**GCL mathematical research dossier, 2026-11-19.** All graphs finite and simple. This theorem is an ordinary mathematical derivation; it has not received independently authenticated specialist review or kernel-level proof certification. The three-star Ramsey corollary additionally assumes the current internally reviewed (but uncertified) joint 3×3 residual theorem. No claim concerning the unrestricted Erdős #561 conjecture is made.

## 1. Main theorem: only an isolated parity clique can obstruct

Let `α,β≥1`, put `D=α+β≥2`, and let `G` have maximum degree at most `D`. Let `k_D` be the number of vertices with degree exactly `D`.

**Theorem.** If `k_D≤D+2`, then there exists an edge partition `E(G)=R⊔B` satisfying `Δ(R)≤α` and `Δ(B)≤β` **if and only if** at least one of these three conditions holds:

1. `D` is odd;
2. `α` and `β` are both even;
3. `G` has **no isolated component isomorphic to K_(D+1)**.

Equivalently, under `k_D≤D+2`, a capped partition fails **exactly** when `G` has an isolated `K_(D+1)` component, `D` is even, and `α,β` are odd.

### Lovász specialization

A capped red subgraph must have vertex degrees between

`g(v)=max(0,d_G(v)−β)` and `f(v)=min(α,d_G(v))`.

These satisfy `0≤g(v)≤f(v)≤d_G(v)`, so we may use the standard form of Lovász's `(g,f)`-factor theorem without any relaxed or extended hypothesis. For disjoint vertex sets `S,T`, let `Y=V(G)\(S∪T)`, and define

`A(S,T)=Σ_{s∈S} min(d_G(s),α) + Σ_{t∈T}min(d_G(t),β) − e_G(S,T)`.

Lovász's theorem says the capped partition exists if and only if `A(S,T)≥q(S,T)` for every such `S,T`, where `q` counts components `C` of `G[Y]` whose vertices all satisfy `g=f` and `α|C|+e_G(C,T)` is odd. The equality `g=f` occurs only at vertices with degree `D`, **or isolated vertices**; isolated components are parity-even and never counted. Thus every counted component consists entirely of degree-`D` vertices.

Since `D min(d,α)≥αd` and `D min(d,β)≥βd` for all `d≤D`, summing vertex degrees on S and T gives the key inequality

`D A(S,T) ≥ α e_G(S,Y)+β e_G(T,Y)+2α e_G(S)+2β e_G(T)`.

In particular, `A≥0`, and for the boundary `b(C)=e_G(C,S∪T)` of any counted component,

`D A ≥ min(α,β) Σ_{counted C} b(C)`.

If a counted component has `c≤D` vertices, its vertices all have total degree D, and since the graph is simple,

`b(C)=Dc−2e_G(C) ≥ Dc−c(c−1)=c(D−c+1)≥D`.

### Exhaustion of the obstruction

Suppose the capped partition fails, so for some `S,T` we have `A<q`. Both values are integers; `A≥0`, so `q≥1` and `A≤q−1`.

If every counted component has size at most D, each contributes at least D boundary edges. Hence `DA≥qD`, so `A≥q`, a contradiction. **At least one counted component has at least D+1 vertices.** Since `k_D≤D+2`, this is the only such component.

**If `q=1`:** then `A=0`. Its counted component `C` has no boundary to S or T. Because C is a component of `G[Y]`, it has no edges to any vertex outside C, hence it is isolated and D-regular.

- If `|C|=D+1`, it must be the complete graph `K_(D+1)`. Its oddness condition is `α(D+1)` odd, requiring D even and α odd (and therefore β odd).
- If `|C|=D+2`, no such counted component can exist: for D odd, a D-regular graph on D+2 (odd) vertices violates the handshake lemma; for D even, D+2 is even and `α(D+2)` is even, so it cannot be counted.

**If `q≥2`:** the total count of degree-D vertices forces `q=2`, with one counted component `C` of size D+1 and the other a singleton. The singleton has exactly D boundary edges. Since `A≤1`, we have `DA≤D`. If `C` were not complete, it would have at least one missing internal edge and hence at least two boundary edges; then `DA≥min(α,β)(D+2)>D`, impossible. Thus C is complete and its boundary is zero, making C an isolated `K_(D+1)`; the oddness criterion again forces D even and α,β odd.

This proves **necessity** of the isolated parity clique. Conversely, if G contains an isolated `K_(D+1)` and D is even with α,β odd, each clique vertex in any capped partition has exactly α red incident edges. The red degree sum in the clique would be `(D+1)α`, which is odd, contradicting the handshake lemma. This proves **sufficiency**. □

### Sharpness

The threshold `D+2` cannot be increased. For any even D≥2, take `G_D=K_(D+3)−C_(D+3)`, obtained by deleting the edges of a Hamilton cycle. It is connected, D-regular, and has exactly `D+3` maximum-degree vertices but no isolated `K_(D+1)` component. The `(α,β)=(1,D−1)` capped partition is impossible: every vertex would require exactly one red edge, giving an odd red degree sum on the odd number D+3 of vertices. The case D=2 is simply the five-cycle C5.

This shows precisely why the two-low-slack proof strategy cannot be extended indefinitely just by counting maximum-degree vertices: the next degree-core size supports genuinely new odd-order factor obstructions.

## 2. Three-star Ramsey consequence

Write `F(n)=K_{1,n₁}⊔K_{1,n₂}⊔K_{1,n₃}` for ordered triples `n₁≥n₂≥n₃≥1`, likewise m, with leading sizes n₁,m₁≥2. Let `W(n,m)` be the Burr–Erdős–Faudree–Rousseau–Schelp antidiagonal upper bound. Assume the previously reviewed paper-level joint three-star residual theorem `J(n,m)=W(n,m)−(n₁+m₁−1)`; it is **not yet independently certified**.

Define

`D=n₁+m₁−2`, `E=W−1`, `T=D(D+1)/2`, `R=max(Σn_i+3,Σm_j+3)`, `B=2E−D²+1`, `s=B−R`, `t=E−T`, and `α=n₁−1`, `β=m₁−1`.

**Corollary (D+2-core Ramsey gate).** The conjectured original answer `rhat(F(n),F(m))=W(n,m)` follows if

`0≤s≤2D−3`, **and at least one** of

1. `D` is odd, or one of α,β is even;
2. `t>s`.

**Proof.** Assume contrary that an arrowing graph G has fewer than W edges. The joint residual deletion theorem and Vizing imply `e(G)=E`, `Δ(G)=D`, and the `(α,β)` capped partition fails (it would avoid both target forests). By the earlier degree-core theorem, G contains at least D+1 degree-D vertices. If G had at least D+3 such vertices, then

`2E−v_+(G)=Σ_{d_G(v)>0}(d_G(v)−1)≥(D−1)(D+3)=D²+2D−3`.

Since `v_+(G)≥R`, this would force `s=B−R≥2D−2`, contradicting `s≤2D−3`. Thus G has at most D+2 maximum-degree vertices. Apply the theorem above.

If D is odd or one cap is even, the capped partition exists, contradiction.

Otherwise the only possible obstruction is an isolated `K_(D+1)` component. Let H denote the remaining graph; it has exactly `t=E−T` edges. Choose the target forest with R vertices and colour the clique in that target's colour. In each **tree component** of H containing an edge, colour one leaf edge in the opposite colour; colour every other edge of H in the clique's colour. The opposite-colour edges form a matching and hence avoid the other target, whose largest star has at least two edges. The clique-colour subgraph of H has at most t nonisolated vertices: a cyclic connected component of e edges has at most e vertices, whereas in a tree with e edges selecting a leaf edge in the opposite colour leaves at most e nonisolated vertices. Thus the clique-colour graph has at most `(D+1)+t` nonisolated vertices. But `R=B−s` and `B−(D+1+t)=t`; the assumption t>s gives `R>D+1+t`. It therefore cannot contain the target forest, contradiction. The standard W-edge star host yields the upper bound. □

### Exact bounded parameter audit

For ordered three-star pairs with n₁,m₁≥2 and D≤9, the previous edge/vertex/equality gates leave **851** pairs. The theorem above excludes **512** of these, leaving **339**. The preexisting parity and one-slack arguments excluded 96 of the 512; thus **416 additional** pairs are excluded beyond those particular earlier gates. Compared with the prior low-slack result, which left 535, this improves the shortlist by **196**.

The 339 surviving pairs by D are: D2=9, D3=36, D4=92, D5=118, D6=82, D7=2, and none for D8,D9. **These are not 339 established open problems**, only cases not excluded by this exact method; many may be settled by other theorems or alternative colourings. No general result for s,t≥4 is claimed.

## 3. Exact and independent verification

- `erdos561_kplus2_atlas.py`: all graph-atlas classes of at most seven vertices, exact exhaustive capped-colouring tests. Out of 4,135 graph/cap cases, 4,100 have at most D+2 saturated vertices and obey the exact isolated-clique classification; 22 are actual below-threshold obstructions. Above threshold there are 35 cases including 9 obstruction cases without an isolated parity clique.
- `erdos561_kplus1_core_experiment.py`: completely enumerates all core-and-pendant constructions with exactly D+2 saturated vertices for D=2,3,4: 41, 768 and 27,449 distinct complementary-core graphs, respectively. All failures have an isolated `K_(D+1)` component.
- `erdos561_kplus2_parameter_gate.py` and independent `erdos561_kplus2_final_gate.py`: exact 3×3 integer filtering, including the preexisting edge, vertex, and special equality gates. Confirmed 851 baseline, 512 new structural exclusions, 339 survivors; the full ordered lists are stored as JSON.

The finite enumerations verify the bounded implementations; the Lovász proof, not these finite computations, establishes the unbounded structural theorem.

## 4. Claim boundaries and next target

- **Proved at paper level:** the D+2 saturated-core classification for all finite simple graphs and positive caps; the k=D+3 sharpness family.
- **Dependent/unpromoted:** the original three-star size-Ramsey corollary, which additionally uses the complete 3×3 joint residual theorem and You's 2026 exact two-component result.
- **Still open:** all cases not covered by current special theorems, general joint residual for four or more components, and unrestricted Erdős #561.
- **Next structural gate:** at k=D+3, isolated cliques are not the only obstruction. Classify odd-order, near-regular, connected degree-D components, starting with `K_(D+3)−C_(D+3)` for even D, and devise Ramsey-avoiding colourings using the bounded exterior-edge budget.

Primary Lovász source: Mikio Kano and Akira Saito, *A short proof of Lovász's factor theorem*, https://gorogoro.cis.ibaraki.ac.jp/web/papers/newKanoSaitoFactor1984.pdf. The proof uses the standard version with `g≤f≤d_G`, avoiding any special extension for vertices with degree less than α.
