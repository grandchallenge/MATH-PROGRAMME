# Erdős #561: the degree-core obstruction and the complete 3×3 joint residual bound

**Research disposition:** new paper-level mathematical proofs, incorporating a finite **integer-parameter** verification for a bounded end case. No claim that the unrestricted Erdős #561 conjecture has been solved. Independently review before promotion. All graphs finite and simple; star-forest containment means ordinary (not induced) subgraph containment. Source problem: Burr–Erdős–Faudree–Rousseau–Schelp. Earlier two-component theorem: Chunlin You, arXiv:2610.25958v1 (2026-10-19). Classical external results: Lovász's `(g,f)`-factor theorem and Vizing's edge-colouring theorem.

## Definitions

Let `F(n)=⊔_i K_{1,n_i}` for a non-increasing positive sequence. Write `G -> (A,B)` if every red/blue edge-colouring yields red `A` or blue `B`. Let

`w_k(n,m)=max_{1≤i≤s,1≤j≤t,i+j=k}(n_i+m_j-1)` for `k=2,...,s+t`, and `W(n,m)=Σ_k w_k(n,m)`.

The canonical host `⊔_{k=2}^{s+t} K_{1,w_k}` arrows `(F(n),F(m))`, giving `rhat(F(n),F(m)) ≤ W`. (Prove by choosing the leftmost red star of sufficient size and taking blue stars to its right, or consult the source's standard star-host construction.)

## Theorem A — degree-core obstruction (all simple graphs)

Let `α,β≥1`, `D=α+β`, and `Δ(G)≤D`. If `E(G)` admits **no** two-partition `J⊔K` with `Δ(J)≤α`, `Δ(K)≤β`, then the graph induced by its degree-`D` vertices has a connected component on at least `D+1` vertices. Consequently, writing `v_+(G)` for its number of nonisolated vertices,

`e(G)≥D(D+1)/2` and `v_+(G)≤2e(G)−D²+1`.

**Proof.** Take `f(v)=α` and `g(v)=max(0,d(v)−β)`. Lovász's nonnegative `(g,f)`-factor criterion specializes to the following condition for a degree-capped edge partition: for every disjoint `S,T⊆V(G)`,

`A(S,T)=α|S| + Σ_{v∈T} min(d(v),β) − e(S,T) ≥ q_D(S,T)`, where `q_D` counts components `C` of `Y=G−(S∪T)` on which every vertex has **degree D in G** and `α|C|+e(C,T)` is odd. Indeed `g=f` exactly when `d=D`, and the displayed parity is exactly the criterion's odd-component parity.

If the partition fails, some `S,T` have `A<r=q_D`. Since `d≤D` and `min(d,β)≥βd/D`, a degree-sum calculation gives

`D A(S,T) ≥ α e(S,Y) + β e(T,Y) ≥ min(α,β)(e(S,Y)+e(T,Y)) ≥0`.

Thus `r≥1` and `0≤A≤r−1`. If every one of the `r` counted components has `c=|C|≤D`, its boundary to `S∪T` is at least

`Dc−c(c−1)=c(D−c+1)≥D`.

These components are disjoint, so `e(S,Y)+e(T,Y)≥rD`; but then `DA≥rD>D(r−1)≥DA`, contradiction. Hence one counted component has at least `D+1` degree-`D` vertices. For `k≥D+1` such vertices and `v_+−k` remaining nonisolated vertices, degree-sum gives `2e≥Dk+(v_+−k)≥v_++D²−1`. Both consequences follow. **QED.**

The theorem is stronger than merely saying that the graph is Class II; it uses **failure of the specific (α,β)-partition**, not just its chromatic index.

### Equality structure

If `v_+=2e−D²+1`, then exactly `D+1` vertices have degree `D` and every remaining nonisolated vertex has degree one. Let `C` be the `D+1`-vertex maximum-degree set, and set `t=e−D(D+1)/2`. If `m` edges are missing from the complete graph `K_{D+1}` on `C`, its boundary has precisely `2m` edges and `t=m+e(G−C)`, so `m≤t`. Colour every edge meeting `V(G)\C` red, and every edge inside `C` blue. The red maximum degree is at most `max(1,t)`; all blue edges lie on `D+1` vertices.

## Theorem B — joint residual inequality for EVERY pair of three-star forests

Let `n=(a,b,c)`, `m=(p,q,r)`, with `a≥b≥c≥1`, `p≥q≥r≥1`. Let `W=W(n,m)`, `w_2=a+p−1` and `J(n,m)` be the minimum edge count of a graph `Q` which **simultaneously** satisfies

`Q -> (F(b,c),F(p,q,r))` and `Q -> (F(a,b,c),F(q,r))`.

Then

`**J(n,m)=W(n,m)−w_2(n,m).**`

**Upper bound.** For each antidiagonal `k=3,4,5,6`, use a disjoint star with `w_k` edges. This star host contains coordinatewise the canonical host for each of the two residual pairs, so arrows both. Its edge count is `W−w_2`.

**Lower bound, zero-switching case.** Each residual has one forest with exactly two star components, so its minimum edge count is given by You's 2026 two-component theorem. Let `L` and `R` be the two exact minima and put `σ=(W−w_2)−max(L,R)≥0`. If `σ=0`, either residual condition already requires at least `W−w_2` edges.

**Lower bound, positive-switching case.** Define nonnegative gaps `x=a−b`, `y=b−c`, `u=p−q`, `v=q−r`, and `z=c+r−1`. The five original antidiagonal weights are

`w_2=z+x+y+u+v`;
`w_3=z+y+v+max(x,u)`;
`w_4=z+max(x+y,y+v,u+v)`;
`w_5=z+max(y,v)`;
`w_6=z`.

The residual antidiagonal maxima agree at positions 5,6. At position 3, the red-largest-star-deletion residual exceeds the other by `u−x`. Hence `σ>0` forces one of two **strict** opposite-switch patterns:

* `x>u`, while the red-deleted residual strictly wins at position 4: this requires `u+v>max(x+y,y+v)`, hence `v>y`. Then `w_4=c+p−1`, `w_5=c+q−1`, and `w_6=c+r−1`, so `w_4+w_5+w_6 = rhat(K_{1,c},F(p,q,r))` by the elementary one-star-versus-forest formula. Here `w_3=a+q−1` and `d=w_3−1=a+q−2≥2`.
* `u>x`, while the blue-deleted residual strictly wins at position 4: this requires `x+y>max(u+v,y+v)`, hence `y>v`. Then `w_4=a+r−1`, `w_5=b+r−1`, `w_6=c+r−1`, so `w_4+w_5+w_6 = rhat(F(a,b,c),K_{1,r})`. Here `w_3=b+p−1` and `d=b+p−2≥2`.

In either case `a,p≤d`, and the residual condition attaining `w_3` implies `Q` arrows the corresponding pair of individual largest stars, both having at least two edges. By Vizing, `Δ(Q)≥d`. In the case `x>u`, use the **blue-deleted** residual to force `(K_{1,a},K_{1,q})` and hence the degree lower bound, but use the **red-deleted** residual for vertex deletion: colour the incident edges red to obtain `Q−v -> (K_{1,c},F(p,q,r))`. In the case `u>x`, use the **red-deleted** residual for `(K_{1,b},K_{1,p})`, but use the **blue-deleted** residual for vertex deletion: colour the incident edges blue to obtain `Q−v -> (F(a,b,c),K_{1,r})`. Thus in either case, for **every** `v∈V(Q)`, the corresponding elementary one-star-versus-forest bound gives `e(Q−v)≥w_4+w_5+w_6`. Thus if `e(Q)≤w_3+w_4+w_5+w_6−1`, then

`d≤Δ(Q)≤e(Q)−(w_4+w_5+w_6)≤w_3−1=d`.

Consequently `e(Q)=J_*−1` and `Δ(Q)=d`, where `J_*=w_3+w_4+w_5+w_6=W−w_2`. The residual star-pair arrowing excludes any edge partition capped at `(α,β)` corresponding to those two largest stars, with `α+β=d`. Theorem A therefore forces

`J_*−1≥d(d+1)/2` and `v_+(Q)≤2(J_*−1)−d²+1`.

But `w_3≥w_4≥w_5≥w_6`, so `J_*≤4(d+1)`. For `d≥8`, `d(d+1)/2≥4(d+1)>J_*−1`, impossible. Hence `d≤7`. The strict switch conditions above imply `a,p≤d≤7`. It remains to check finitely many non-increasing positive integer triples with largest entries at most seven: **84** possibilities per colour, **7,056 ordered pairs**. Precisely **82** cases have both positive switching surplus **and** forced degree `d≤7`; **74** violate `J_*−1≥d(d+1)/2`. The other **8** violate the forced vertex bound since `Q` must contain full `F(n)` (all-red colouring in the second residual condition) and full `F(m)` (all-blue colouring in the first residual condition). The complete arithmetic-only 82-case enumeration is in `verify_joint3_finite.py`, with its eight cases explicitly listed in `finite_exceptions.json`. The separate `verify_odd_core.py` independently checks all 47,961 ordered bounded pairs for the strengthened core-threshold corollary; `verify_core_and_switching.py` concerns graph-atlas degree partitions only. It invokes no graph-search solver or statistical test.

There is no possible counterexample `Q` with `e(Q)<J_*`. **QED.**

### Exact finite exception list (up to reversal of colours)

The four unordered pairs are `(3,1,1)/(4,3,1)`, `(3,1,1)/(5,4,1)`, `(3,1,1)/(5,4,2)`, and `(4,2,2)/(4,3,1)`; each occurs in both orders. In every case `max(|V(F(n))|, |V(F(m))|)>2(J_*−1)−d²+1`.

## Theorem C — an unconditional family of original Erdős #561 instances

For any `3×3` pair with `W≤D(D+1)/2`, where `D=n_1+m_1−2` and `n_1,m_1≥2`, **regardless of switching surplus**, the predicted original value is exact:

`rhat(F(n),F(m))=W`.

**Proof.** Suppose a host `G` arrows the original pair. Vertex deletion implies **both** residual relations, and hence `e(G)≥Δ(G)+J(n,m)`. Theorem B gives `J=W−(D+1)` for every three-star pair, including positive switching surplus. Vizing implies `Δ(G)≥D`, since `Δ≤D−1` permits a proper edge-colouring using at most `D` colours, split into `n_1−1` red and `m_1−1` blue matchings, defeating both forests. If `Δ≥D+1` then `e≥W`. If `Δ=D` then the same cap partition is impossible, so Theorem A gives `e≥D(D+1)/2≥W`. Combine with the canonical `W`-edge upper host. **QED.**

The exact parameter count for 3×3 pairs with largest sizes ≥2 and all star sizes ≤10 is 47,961 ordered pairs; 44,893 have `σ=0`. The strengthened sufficient condition `W≤D(D+1)/2` covers **46,120** ordered pairs: 43,066 zero-switch pairs and 3,054 positive-switch pairs. These are finite-range applications of the sufficient condition, not independent numerical Ramsey computations.

**Symmetric family.** If `n=m=(A,b,c)` and `A≥b≥c≥1`, then `σ=0` by transposing the two residual conditions. Also `W≤5(2A−1)`. For `A≥6`, `(2A−2)(2A−1)/2 >5(2A−1)−1≥W−1`, giving the exact Erdős formula for **every** such pair. For instance `n=m=(6,4,2)` gives `W=11+9+7+5+3=35`.

## Theorem D — all three-by-three pairs of sufficiently large leading degree

For **every** two three-component star forests, if `n_1+m_1≥12`, then

`rhat(F(n),F(m))=W(n,m)`.

**Proof.** Theorem B provides `J=W−(D+1)`, `D=n_1+m_1−2≥10`. For every original-arrowing host `G`, vertex deletion gives `e(G)≥Δ(G)+J`. If `n_1=1` then `Δ(G)≥m_1=D+1`: otherwise all edges may be coloured blue with maximum blue degree at most `m_1−1`, avoiding both targets. Similarly `m_1=1` forces `Δ≥n_1=D+1`. In those cases `e≥(D+1)+(W−D−1)=W`. If both largest sizes are at least two, Vizing gives `Δ≥D`. If `Δ≥D+1` the same bound finishes. If `Δ=D`, arrowing forbids the cap partition `(n_1−1,m_1−1)` so Theorem A implies

`e≥D(D+1)/2≥5(D+1)≥W`,

since `W` has five antidiagonal terms, each at most `w_2=D+1`. Combine with the standard `W`-edge disjoint-star host. **QED.**

This theorem includes many genuinely nonuniform asymmetric pairs. It establishes a broad original 3×3 case, not all of Erdős #561.

## Corollary — a short, noncomputational proof of the exact 24-edge instance

Take `n=(4,2,2)`, `m=(4,3,1)`. Then `W=24`, `w_2=7`, and Theorem B gives `J=17` (with only a finite *integer* check, not a graph-class enumeration). Suppose `G` arrows the original pair and `e(G)≤23`. For every vertex, both residual arrowing relations hold after deletion, hence `e(G−v)≥17` and `Δ(G)≤e−17≤6`. Vizing forces `Δ(G)≥6`; hence `e(G)=23`, `Δ(G)=6`. No red3/blue3 degree-capped partition exists, so Theorem A gives at least seven degree-six vertices and

`v_+(G)≤2·23−6²+1=11`.

The all-blue colouring requires the blue forest `F(4,3,1)`, with exactly 11 vertices. Therefore equality holds: exactly seven vertices `C` have degree six, and every other nonisolated vertex has degree one. Let `m` be the number of missing edges in `G[C]` relative to `K_7`, and `h=e(G−C)`. Since the seven core vertices have degree six, `e(C,V\C)=2m`, so `23=(21−m)+2m+h=21+m+h`; thus `m≤2`. Colour all edges inside `C` blue and every other edge red. Every red core degree is at most `m≤2`, and every red noncore degree is at most one: no red `K_{1,4}` exists. The blue graph has only seven nonisolated vertices, so it cannot contain the 11-vertex forest `F(4,3,1)`. Contradiction. The canonical 24-edge upper host proves `rhat(F(4,2,2),F(4,3,1))=24`. **QED.**

**Important:** This replaces the earlier 11,197-configuration graph classification and the degree-five critical-density theorem as *essential* dependencies for the fixed 24-edge claim. The unrestricted #561 conjecture remains OPEN. Independent mathematical adjudication of the new dependency route is required before formal promotion.

## Next unresolved theorem

Theorem B proves the joint residual inequality for 3×3, not the full original 3×3 Erdős conjecture. Theorem D settles all pairs with `n_1+m_1≥12`. For n_1,m_1≥2, all undecided original pairs have D≤9. A finite parameter enumeration in `verify_original_remaining.py` finds exactly **851 ordered small-parameter pairs** surviving the original edge, vertex, and equality-colouring budgets. The separately proved odd-degree extremal parity lemma in `ODD_CORE_PARITY_AND_REVIEW.md` and `verify_odd_core.py` eliminates six more, leaving **845 ordered pairs** not excluded by these expanded gates (D=2:9, 3:36, 4:96, 5:200, 6:282, 7:194, 8:34; none for 9). These **are not excluded by the specified degree-core gates**; some have already been resolved by other methods (including (4,2,2) versus (4,3,1)), while others remain open. They provide a finite candidate list for further reductions and literature comparison, not a list of 851 new open mathematical problems. The unrestricted s,t≥4 joint residual bound remains open. No general #561 solution is asserted.

## Adversarial-review addendum: odd-degree equality case

If the degree-core vertex inequality is attained with equality for odd `D≥3`, then exactly `D+1` vertices have degree `D` and every remaining nonisolated vertex has degree one. The `D+1` core vertices have even order. Properly edge-colour their complete graph with `D` colours using a one-factorization; keep those colours on the edges present and reuse the distinct colours of missing core edges for the corresponding pendant edges. The remaining isolated `K₂` components can receive any colour. This yields a proper `D`-edge-colouring and contradicts failure of any `(α,β)` degree partition with `α+β=D`.

The consequent **three additional unordered original 3×3 instances** (six ordered instances) and their full proof are in `ODD_CORE_PARITY_AND_REVIEW.md`; the finite arithmetic gate is `verify_odd_core.py` (851 prior survivors, six new exclusions, 845 remaining). This addendum is **under mathematical review** and does not constitute an independently certified full conjecture proof.


## After the first role-separated review: equality-core classification

The new proof `EVEN_CORE_CAP_PARTITION_THEOREM.md` classifies **all** graphs attaining the vertex-budget equality `v_+=2e−D²+1`: their maximum-degree vertices form a complete `(D+1)`-vertex core with some edges removed and replaced by pendant stubs; all other edges are isolated `K₂`. A red/blue degree-capped partition fails only when `D` is even, both caps are odd, and no core edges were removed. Its proof uses Walecki’s Hamilton decompositions, with an alternating path in the odd/odd case. When an original hypothetical 3×3 counterexample has `e=W−1>D(D+1)/2` and the required forest order exactly saturates the degree-core vertex bound, its nonexistence follows either by this capped partition or by an explicit monochromatic-core avoiding colouring. The resulting additional finite parameter exclusions are 10 ordered pairs, giving the updated **835**-entry list of parameters not excluded by the applied gates (from 851 initially, 845 after the odd-degree refinement). See the two standalone verifiers for exact arithmetic and constructive checks. This theorem remains `UNDER_REVIEW` and does not settle unrestricted Erdős #561.


## One-slack extension (post-review)

`ONE_SLACK_CORE_THEOREM.md` shows that when `D>=3`, `v_+=2e−D²`, and at least `D+1` vertices have degree `D`, exactly `D+1` vertices attain that degree and there is exactly one noncore vertex of degree two. A one-factorization/Hamilton-path recolouring extends the exact equality cap-partition classifier to this one-slack class; the sole failing split is again a complete odd-order core under odd/odd caps, now with a disjoint two-edge path. Its explicit Ramsey-avoiding colouring excludes all original 3×3 `E=W−1>T`, `B−R=1` candidates, conditional on Theorem B. The research shortlist drops by another 80 ordered pairs, `835→755` after the earlier odd/even equality refinements. Full constructive proof, hypotheses and independent finite verifier are in the standalone addendum, and these mathematical statements remain `UNDER_REVIEW`.


## Low-slack core classification (2026-11-18)

`LOW_SLACK_CORE_STABILITY_THEOREM.md` replaces the separate odd/even equality- and one-slack structural derivations with an exact isolated-complete-core obstruction whenever the core vertex-budget slack is `s<=D-2`. Together with a pendant-edge red/blue avoidance construction, the joint 3×3 residual theorem implies the original size-Ramsey formula for **316** of the 851 originally filtered ordered small cases. The arithmetic gate now leaves **535** not excluded by these methods; do not add the earlier 6+10+80 exclusions to 316 (they are subsets). No protected mathematical certification, general #561 remains OPEN.


## Exact saturated-core size D+2 and a sharp small-parameter gate

See `DPLUS2_SATURATED_CORE_THEOREM.md` for a new theorem: an (alpha,beta) capped partition with D=alpha+beta fails in a graph with at most D+2 degree-D vertices precisely when D is even, both caps odd, and an isolated K_(D+1) component is present. The proof uses the unextended Lovász (g,f) factor criterion, with g=max(0,d-beta) and f=min(alpha,d); its odd-component boundary inequalities classify q=1 and q=2. K_(D+3) minus a Hamilton cycle proves that D+2 is the optimal threshold. Combined with the conditional joint 3×3 residual result, this reduces the arithmetic-filter shortlist from its original 851 to 339 (the earlier low-slack gate left 535). This is a paper-level structural result, and the Ramsey corollary depends on the upstream unpromoted theorem.
