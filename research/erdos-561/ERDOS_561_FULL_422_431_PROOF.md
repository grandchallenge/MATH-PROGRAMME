# Erdős #561 — a complete nonuniform three-star-versus-three-star instance

**Date:** 2026-11-18  
**Programme:** Grand Challenge Labs, MATH-PROGRAMME, Erdős #561  
**Claim scope:** One fixed **original asymmetric size-Ramsey number**, not the unrestricted conjecture.  
**Verification tier:** Self-contained paper-level reduction to classical edge-colouring results (Vizing and the adjacency lemma) and independently replayable finite 11,197-case and seven/eight-vertex certificates. **No Lean kernel replay or independent public peer review claimed.**

## Main theorem

Let `F(n_1,...,n_s)` denote the vertex-disjoint union of stars `K_{1,n_i}`. For finite simple graphs and ordinary non-induced subgraph copies, write `G -> (A,B)` when every red/blue colouring of the edges of `G` has a red copy of `A` or a blue copy of `B`. Define `\hat r(A,B)=min_{G->(A,B)}e(G)`.

**Theorem.**

$$
\boxed{\widehat r(F(4,2,2),F(4,3,1))=24.}
$$

The original Erdős #561 antidiagonal formula gives 7+6+5+4+2=**24** for these parameters. The theorem is one of the first nontrivial three-star-vs-three-star parameter instances attacked by this GCL workstream, but **no claim of historical priority or novelty** is made.

## Required independent facts

**F1 — vertex deletion.** If `G -> (F(n_1,...,n_s),F(m_1,...,m_t))`, then for every vertex `x`, deleting `x` leaves both the red-largest-star-deleted and blue-largest-star-deleted arrowing relations. Proof: extend an avoiding colouring on `G-x` by making all `x`-edges red, respectively blue; a monochromatic forest in the extension must have a component away from `x`. This is Lemma 2.2 of the October 2026 two-component paper, but the argument is elementary and fully reconstructed in the earlier GCL audit.

**F2 — exact joint residual instance.** The previous `ERDOS_561_exact_joint_422_431_release.zip` proves, with a complete 11,197-candidate enumeration independently replayed in C++17 and Python, that

$$
J:=\min\{e(Q):Q\to(F(2,2),F(4,3,1))\ \text{and}\ Q\to(F(4,2,2),F(3,1))\}=17.
$$

Moreover, it proves the **11-edge rigidity lemma**: every `Q` with eleven edges arrowing `(K_{1,2},F(4,3,1))` is, up to isolates, `F(5,4,2)`. The finite certificate has been cross-checked by different code paths: Python complement signature enumeration and C++ direct blue-star embedding for all red matchings. Complete proof in `EXACT_JOINT_422_431_PROOF.md` included in this release.

**F3 — Vizing's theorem.** A finite simple graph of maximum degree `D` has a proper edge-colouring in at most `D+1` colours. In particular, if `D<=5`, it can have its edges divided into at most six matchings, three red and three blue, so **cannot** arrow `(K_{1,4},K_{1,4})`.

**F4 — a finite, independently replayable critical-graph restriction.** Every simple edge-5-critical graph C with at most seventeen edges has exactly seven nonisolated vertices and at least sixteen edges. Thus, in the sole regime needed below, it also satisfies

$$
e(C)\ge\tfrac12(4|V(C)|+3).
$$

This is proved in `CRITICAL5_REPLACEMENT_PROOF.md`, using only **Vizing's adjacency lemma** for the general density inequality `e(C)>=2|V(C)|` and an exact complete census of all connected seven- and eight-vertex graph classes of maximum degree five and the required edge bounds. The certificate `critical5_atlas_verify.py` uses original graph6 datasets stored under `fixtures/`, whose SHA-256 values are pinned and checked. It finds no seven-vertex six-edge-chromatic graph with at most fifteen edges, and ten eight-vertex six-edge-chromatic graph classes with at most seventeen edges, all of which have a pendant vertex and therefore are not edge-critical. This **replaces** the formerly necessary 1994 Kayathri full-text dependency for this fixed problem; the stronger historical theorem is retained as provenance in `SOURCE_LOCK.md` but not invoked.

A graph is edge-5-critical if `χ′(C)=6`, `Δ(C)=5`, and deleting any edge makes it five-edge-colourable. Any graph with `Δ=5` and `χ′=6` contains an edge-minimal such critical subgraph.

## New structural lemma: two nonadjacent maximum-degree apices

**Theorem (two-apex star-forest edge-colouring).** Let `G` be any finite simple graph with `Δ(G)=D>=6`. Suppose `u,v` are **nonadjacent** vertices each of degree `D`, and `G-{u,v}` is a vertex-disjoint union of stars and isolated vertices. Then

$$
\boxed{\chi'(G)=D.}
$$

**Proof.** Use a palette `P` of exactly `D` colours. Colour the `D` edges incident with `u` bijectively with `P`. Assign colours bijectively to the `D` edges incident with `v` such that, at any common neighbour `x` of `u` and `v`, the colours on `ux` and `vx` are different.

This is a standard application of Hall's marriage theorem. Each `v`-edge has all `D` colours available, except possibly the one already used on the corresponding `u`-edge. These forbidden colours are pairwise distinct for different common neighbours. For any subset of at most `D-1` of the `v`-edges, its combined allowed colours include at least `D-1` colours. For all `D` edges, their combined allowed colours equal `P` (no colour is forbidden at every neighbour because the forbidden colours are distinct and `D>=2`). Thus a system of distinct representatives exists.

Now consider a single star component of `G-{u,v}`. Let `c` be its centre with `h` leaves. Let `P_c` be the colours not used on the apex edges `uc` and `vc`, when present. There are at most two such exclusions, so

$$
|P_c|\geq D-2\geq4,\qquad |P_c|\geq h,
$$

where the second inequality follows because the degree of `c` in `G` is at most `D`. For each leaf `x`, the colour of edge `cx` is chosen from `P_c` excluding the colours already used on `ux` and `vx`, when present. Hence every leaf list has at least `|P_c|-2>=2` colours.

Moreover, **a given colour can be excluded from at most two leaf lists**, because it appears on at most one edge at `u` and at most one edge at `v`. Verify Hall's criterion for a subset `X` of leaves: if `|X|<=2`, one leaf list already has at least two colours, so their union has size at least `|X|`. If `|X|>=3`, no colour is forbidden at every leaf of `X`, so the union of the lists is *all* of `P_c`, whose size is at least `h>=|X|`. Hall therefore assigns the `h` star edges distinct permitted colours. Do this independently at each star centre; no conflicts arise between different star components or the previously coloured apex edges. This gives a proper edge-colouring of `G` with `D` colours. Since `G` has vertices of degree `D`, `χ′(G)>=D`, so equality follows. QED.

**Sharp qualification:** The condition `D>=6` is sufficient for the Hall argument; no claim is made here that it is necessary. The two apices must be nonadjacent for the stated proof. A pure-Python executable `two_apex_colouring.py` constructs the colouring; 3,000 varied eligible random instances at `D=6,7,8` were checked as non-proof corroboration.

## Lower bound: exclude 23 edges

Suppose for contradiction `G -> (F(4,2,2),F(4,3,1))` with `e(G)<=23`.

**1. Vertex deletion confines its degree.** By F1, for every vertex `x`, the graph `G-x` satisfies **both** joint residual arrowing relations defining `J`. F2 gives `e(G-x)>=17`. Therefore

$$
 e(G)-d_G(x)\ge17\quad(\forall x),\qquad\Delta(G)\le e(G)-17\le6.\tag{1}
$$

The original arrowing relation implies the weaker one `G->(K_{1,4},K_{1,4})`. If `Δ(G)<=5`, F3 gives a proper edge-colouring in at most six colours; partition the colours into three red and three blue classes. The resulting colouring has both red and blue degree at most three and avoids **both** target forests, a contradiction. Hence `Δ(G)>=6`. Combining with (1),

$$
\boxed{e(G)=23,\qquad \Delta(G)=6.}\tag{2}
$$

**2. A 17-edge joint residual extremizer must have degree six.** Choose `v` with degree six, and set `Q=G-v`. Then `e(Q)=17`, `Δ(Q)<=6`, and `Q` satisfies both residual conditions R1 and R2.

R2 implies `Q->(K_{1,4},K_{1,3})`. By F3, `Δ(Q)>=5`. Suppose `Δ(Q)=5`. If `Q` were properly 5-edge-colourable, splitting three classes red and two blue would avoid both `K_{1,4}` and `K_{1,3}`; hence `χ′(Q)=6`. Choose an edge-minimal subgraph `C` of `Q` with `χ′(C)=6`. By Vizing and `Δ(Q)=5`, we have `Δ(C)=5`, and `C` is 5-critical. The exact critical-graph lemma F4 gives

$$
 e(C)\ge (4|V(C)|+3)/2.
$$

Since `e(C)<=17`, we get `|V(C)|<=7`. On at most six vertices, every graph is a subgraph of `K_6`, and `K_6` has a proper five-edge-colouring (its one-factorization), so a six-edge-chromatic graph requires at least seven vertices. Thus `|V(C)|=7` and `e(C)>=16`.

Since `Q` has only seventeen edges, there is at most **one** edge of `Q` outside `C`. Thus `Q` has at most `7+2=9` nonisolated vertices. But R1 implies that the all-blue colouring of `Q` contains `F(4,3,1)`, which has **11 nonisolated vertices**. Contradiction. Therefore `Δ(Q)!=5`, and hence

$$
\boxed{\Delta(Q)=6.}\tag{3}
$$

**3. Two nonadjacent apices expose the rigid star forest.** Choose `w` in `Q` with degree six. Since `G` has maximum degree six, `w` is **not adjacent to** `v`, otherwise its degree in `G` would be seven. The first residual arrowing relation R1 implies, by F1, that `Q-w -> (K_{1,2},F(4,3,1))`. Because `e(Q)=17` and `d_Q(w)=6`, the remainder `Q-w` has exactly eleven edges. By F2's complete finite rigidity theorem, `Q-w`, apart from isolates, is `F(5,4,2)`.

Therefore `G-{v,w}` is a disjoint star forest and `v,w` are nonadjacent vertices of degree six in `G`. The new two-apex edge-colouring theorem gives a proper **six-colour edge-colouring of `G`**. Split these classes into three red and three blue matchings: each colour has maximum degree at most three and therefore cannot contain a red `K_{1,4}` or a blue `K_{1,4}`. In particular, the colouring avoids both prescribed forests, contradicting the original arrowing relation.

No graph with at most 23 edges arrows the original pair; hence

$$
\widehat r(F(4,2,2),F(4,3,1))\ge24.
$$

## Upper bound: 24-edge explicit witness

Take `U=F(7,6,5,4,2)`, which has `7+6+5+4+2=24` edges. It arrows `(F(4,2,2),F(4,3,1))`. This is the standard antidiagonal star construction, but it has also been checked completely without relying on that general construction: because `U` is a disjoint union of five stars, every red/blue colouring is equivalent, for the question of monochromatic star-forest containment, to the numbers of red edges at its five centres. The number of cases is

$$
(7+1)(6+1)(5+1)(4+1)(2+1)=5040.
$$

The CPU-only script `exact_original_upper.py` checks all 5,040 possibilities and finds that **every one** contains a red `F(4,2,2)` or a blue `F(4,3,1)`. Hence `\hat r<=24`. Together with the lower bound, this proves the theorem.

## Verification record and commands

This release contains the entire earlier joint-residual evidence pack, including both independent 11,197-case enumerators and their raw outputs, plus the new two-apex constructive implementation and 5,040-case upper witness.

```bash
python3 exact_degree5_residual.py
# 11197 matching augmentations, 2 labelled surviving instances

g++ -std=c++17 -O3 exact_degree5_cpp_replay.cpp -o replay && ./replay
# independent complete replay: TOTAL tested=11197 arrows=2

python3 check_degree5_apex.py
# 2380/2380 colourings defeating the second residual arrow relation

python3 exact_joint_upper.py
# 630/630 centre-colour allocations, joint residual upper bound 17

python3 two_apex_colouring.py
# 3000/3000 varied constructive D-edge colourings for D=6,7,8

python3 exact_original_upper.py
# 5040/5040 centre-colour allocations, original upper bound 24
```

**Scientific acceptance condition:** Independently review the 11-edge rigidity enumerators, the seven/eight-vertex critical-graph census and the Vizing adjacency-lemma reduction, and optionally formalize the short mathematical lemmas in Lean. The current result is **computer-assisted proof with named classical graph-theory input**, not a formally kernel-checked proof, protected mathematical certification, or a claim of historical novelty.

## Implications and limitations

The original problem has a genuine three-star-versus-three-star **nonuniform exact instance** with a complete paper-level proof depending on classical Vizing results and exact finite certificates. The critical technique is a two-stage rigidity cascade:

1. The joint residual bound forces a hypothetical original counterexample to have fixed maximum degree.
2. A critical-graph finite-census restriction forces the residual graph to have a second maximum-degree vertex.
3. Deleting the two vertices exposes the rigid star forest, and an explicit Hall colouring then rules out arrowing.

This is a promising mechanism to attempt on additional parameter families. **It does not prove Erdős #561 for arbitrary numbers or sizes of stars**; general joint-residual inequalities and critical-graph structure remain unproved outside the restricted classes already documented.
