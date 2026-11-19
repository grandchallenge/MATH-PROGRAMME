# Erdős #561 — a second exact joint residual theorem

**Date:** 2026-11-18  
**Programme:** GCL / Erdős #561 / issue [#3490](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3490)  
**Result:** `JOINT_RESIDUAL_EXACT_422_431 = 17`, with complete small finite classification and a universal degree argument.  
**Scope:** Applies to the *joint residual problem*, not directly to the size-Ramsey number of the original `(4,2,2)` versus `(4,3,1)` forests. This does **not** solve unrestricted Erdős #561.

## 1. Precise theorem

Write `F(a_1,...,a_q)` for the vertex-disjoint union of stars `K_{1,a_i}`. The relation `G -> (R,B)` means that every red/blue colouring of the edges of a finite simple graph `G` has a red copy of `R` or a blue copy of `B`. All copies are non-induced.

Let

- **R1:** `G -> (F(2,2), F(4,3,1))`;
- **R2:** `G -> (F(4,2,2), F(3,1))`.

Then

$$
\boxed{\min\{|E(G)|:\ G\text{ satisfies R1 and R2}\}=17.}
$$

In the formulation of issue #3490, this is `J((4,2,2),(4,3,1))=17`, the full antidiagonal-tail sum `(6,5,4,2)`. Each individual residual minimum is 16, under the two-component theorem in the October 2026 paper, so the joint result recovers the one-edge switching surplus. **This proof of the joint minimum does not invoke that paper's two-component theorem.** The proof uses only elementary matching facts, Vizing's classical edge-colouring theorem, and an exhaustively certified finite lemma.

## 2. Lower bound: exclude a simultaneous 16-edge host

Assume for contradiction that a finite simple graph `G` with 16 edges satisfies both R1 and R2.

**Step A — every vertex deletion leaves a constrained graph.** Fix any vertex `v`. R1 implies

$$
G-v \to (K_{1,2},F(4,3,1)). \tag{A}
$$

To see this, start with an arbitrary colouring of `G-v` without a blue `F(4,3,1)` and colour every edge incident to `v` red. R1 forces two disjoint red `K_{1,2}`. At most one contains `v`, so at least one red `K_{1,2}` lies in `G-v`, proving (A).

Let `H=F(4,3,1)`, with `e(H)=8` and matching number `ν(H)=3`. **Any** `Q -> (K_{1,2},H)` has at least 11 edges: its all-blue colouring contains `H`, so `ν(Q)>=3`. Colour the edges of any maximum matching `M` red and every other edge blue. The red graph is a matching and hence has no `K_{1,2}`; the blue graph must contain `H`. Thus `e(Q)-ν(Q)>=8`, giving `e(Q)>=11`.

Therefore `e(G-v)>=11` for every vertex, i.e. `16-d_G(v)>=11` and

$$
\Delta(G)\le 5. \tag{B}
$$

**Step B — the second relation forces the opposite inequality.** R2 implies the weaker one-star arrowing `G -> (K_{1,4},K_{1,3})`. If `Δ(G)<=4`, Vizing's edge-colouring theorem splits `E(G)` into at most five matchings. Colour any three matching classes red and the remaining at most two blue, obtaining red degree at most three and blue degree at most two, avoiding both target stars. Contradiction. Consequently `Δ(G)>=5`, and with (B),

$$
\boxed{\Delta(G)=5.}\tag{C}
$$

**Step C — extremal vertex-deletion rigidity.** Choose a vertex `v` of degree five; put `Q=G-v`. It has exactly eleven edges and satisfies (A). Take a maximum matching `M` in `Q`. As above, `ν(Q)>=3`, and the all-red-matching colouring implies `e(Q)-ν(Q)>=8`, so `ν(Q)=3`. The blue remainder `Q-M` has exactly eight edges and contains `H`, hence equals `H` plus isolated vertices.

Therefore **every possible `Q`** arises from a fixed copy of `H=F(4,3,1)` (11 nonisolated vertices) by adding a matching of exactly three new edges. A matching edge connecting two fresh vertices is impossible, because together with a matching of size three already in `H` it would give a matching of size four in `Q`. Each new edge therefore touches at least one original `H` vertex, and at most three fresh vertices are needed.

The following finite lemma is proved by complete enumeration, with **two independently written executable verifiers** and no graph-isomorphism library required for the C++ replay.

> **Finite rigidity lemma.** Up to isolated vertices, the only simple eleven-edge graph that arrows `(K_{1,2}, F(4,3,1))` is `F(5,4,2)`.

**Exhaustiveness of the finite certificate:** Label the 11 vertices of `H` as `0,...,10` and permit up to three fresh vertices `11,12,13`. Enumerate all matchings of three additional edges, where no added edge duplicates an edge of `H`, no two added edges meet, no edge joins two fresh vertices, and fresh labels are canonical. This produces precisely **11,197** labelled matching extensions of the fixed `H`. For each candidate, test all red matching colourings of its eleven edges. Such colourings are exactly the red colourings avoiding a red `K_{1,2}`. The blue graph must contain eight H edges; this is equivalent to the existence of an eight-edge subset comprising disjoint stars of sizes `4,3,1`. The tests find exactly **two** survivors, described by added matchings

```
(0,11), (5,12), (9,13)
(0,11), (5,12), (10,13)
```

Both are isomorphic to `F(5,4,2)`, since in the one-edge component of `H` either endpoint may be chosen as its centre. This proves the finite rigidity lemma. The Python `exact_degree5_residual.py` implementation uses all three-edge complements of H; the independently implemented C++17 `exact_degree5_cpp_replay.cpp` tests all red matching colourings and searches directly for disjoint blue stars. Both count **11,197** candidate extensions and the same **two** survivors.

**Step D — an explicit colouring rules out every possible reattachment.** By the rigidity lemma, `G-v` consists of three vertex-disjoint stars of sizes `(5,4,2)`, plus isolates. Since `Δ(G)=5`, the vertex `v` cannot be adjacent to the centre of the five-edge star. Colour the edges of `G` as follows:

1. Colour **two** edges at the centre of the five-edge star blue.
2. Colour **one** edge at the centre of the four-edge star blue.
3. Colour **two** of the five edges incident to `v` blue; if `v` is adjacent to the centre of the four-edge star, make that edge one of these two.
4. Colour every other edge red.

Then **every blue degree is at most two**: the apex has two blue edges, the five-star centre has two, the four-star centre has at most two, and every other vertex has at most two (one original-star edge plus possibly one apex edge).

Also **every red degree is at most three**: the apex retains three, the five-star centre retains three, the four-star centre retains three because its possible apex edge was blue, the two-star centre has at most three, and other vertices have at most two.

Thus the red graph has *no* `K_{1,4}` and the blue graph has *no* `K_{1,3}`. It therefore contains neither red `F(4,2,2)` nor blue `F(3,1)`, contradicting R2. No sixteen-edge `G` satisfies both R1 and R2.

This also rules out graphs with fewer than sixteen edges, since any such graph could be padded with disjoint edges to sixteen without destroying arrowing, which the preceding result forbids. More directly the earlier degree inequalities imply `e(G)>=Δ(G)+11>=16` for any joint host; the only possible sixteen-edge equality is excluded above. Hence `J>=17`.

## 3. Upper bound: an explicit seventeen-edge host

Take the vertex-disjoint union

$$
U=F(6,5,4,2),\qquad e(U)=6+5+4+2=17.
$$

It satisfies R1 and R2. Because each component is a star and components are disjoint, the existence of a red/blue star forest depends **only** on the red/blue edge counts at the four centres. Every red/blue edge colouring therefore reduces to one of

$$
(6+1)(5+1)(4+1)(2+1)=630
$$

integer allocations. The small `exact_joint_upper.py` independently enumerates all 630, and for each confirms `red F(2,2) OR blue F(4,3,1)` and `red F(4,2,2) OR blue F(3,1)`. Every allocation passes. Therefore `J<=17`; together with the lower bound, `J=17`.

## 4. Verification evidence and exact commands

From the release directory, with Python 3, a C++17 compiler, and optional NetworkX only for the third cross-check:

```bash
python exact_degree5_residual.py
# candidate_M = 11197; passed = 2; both survivors 14 vertices

g++ -O3 -std=c++17 exact_degree5_cpp_replay.cpp -o replay
./replay
# TOTAL tested=11197 arrows=2; the two added matchings listed above

python check_degree5_apex.py
# 3473 total five-neighbour apex patterns, 2380 respecting maximum degree five;
# all 2380 have the explicitly constructed red-degree<=3, blue-degree<=2 colouring

python exact_joint_upper.py
# PASS: all 630 four-star centre-degree allocations arrow both R1 and R2
```

Two independent algorithms check the finite classification: a Python complement-enumeration method and a C++ direct-centre-and-leaves search. Both enumerate all candidate matching augmentations; the C++ code uses only standard-library facilities. The degree-five colouring is a universal argument; the `2380/2380` finite test only corroborates that argument, rather than setting its scope. The upper host check is a complete exhaustive finite proof because its four components are stars.

**Proof and evidence tiers:**

- Degree restriction `Δ=5`: **ordinary theorem**, relying on Vizing (standard classical result).
- 11-edge rigidity lemma: **finite exhaustive computational proof**, two independent programs; not formally verified in Lean.
- Contradictory colouring of all degree-five apex attachments: **ordinary theorem**, independently corroborated over 2,380 patterns.
- Seventeen-edge upper witness: **complete 630-allocation finite certificate**.
- Joint result `J=17`: **computer-assisted proof**, not an unsupported empirical extrapolation.
- Original size Ramsey number `\hat r(F(4,2,2),F(4,3,1))`: **NOT established by this result**.
- Unrestricted Erdős #561 conjecture: **OPEN**.

## 5. New next question

For the original *(not residual)* pair `(4,2,2)` and `(4,3,1)`, the conjectured size Ramsey number is `24` (antidiagonal weights `(7,6,5,4,2)`). By vertex deletion and the proved joint-residual minimum `17`, any hypothetical 23-edge original arrowing graph satisfies `Δ<=6`. The weaker one-star arrowing `(K_{1,4},K_{1,4})` plus Vizing gives `Δ>=6`, hence any 23-edge counterexample must have **exactly degree six**, and every maximum-degree deletion is a seventeen-edge joint-extremal graph. The unresolved research problem is now to classify or constrain these **17-edge joint-extremal residual graphs**, or construct a 23-edge arrowing host disproving the predicted 24. There is no basis to claim either outcome yet.

## 6. Claim and provenance boundaries

The finite programmes have been executed in the current session on the generated release files. This is self-generated mathematics requiring independent scientific review before a public novelty or priority claim; do not promote paper-level findings to protected mathematical certification without the appropriate evidence gate. The historical original Erdős #561 and the 2026 two-component preprint have distinct claim scopes; neither proves the full unrestricted conjecture. The classification here is specific to H=(4,3,1) with eleven edges and does not assert a general uniqueness theorem for single-star Ramsey extremizers.
