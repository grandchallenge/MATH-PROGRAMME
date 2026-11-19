# ERDOS-561: exact degree-core equality classification

Date: 2026-11-18. Review disposition: `PROVED_IN_PACKAGE / UNDER_REVIEW`. This is a **new local mathematical argument**, not a protected mathematical certification. All graphs below are finite and simple, and `v_+` counts vertices of positive degree.

## Theorem: the sole cap-partition obstruction at degree-core equality

Fix integers `α,β≥1`, `D=α+β≥2`, and a graph `G` with `Δ(G)=D` and at least `D+1` vertices of degree `D`. Suppose

`v_+(G)=2e(G)−D²+1`.

Then an edge partition `E(G)=R⊔B` satisfying `Δ(R)≤α`, `Δ(B)≤β` **exists, except exactly when** `D` is even, `α` and `β` are odd, and the graph induced by the degree-`D` vertices is `K_(D+1)` (with no missing core edges). In that exceptional case the partition does not exist. The possible additional components outside the core are isolated `K₂` edges (and isolated vertices).

### Proof: equality structure

Let `C` be the degree-`D` vertices and `k=|C|≥D+1`. The degree sum gives

`2e−v_+ = Σ_{d(v)>0}(d(v)−1)≥(D−1)k≥D²−1`.

The assumed equality forces `k=D+1` and every remaining nonisolated vertex to have degree **one**. The core `C` is `K_(D+1)` with some set `M` of edges removed. For each missing core edge `uv`, the degree deficit at `u` and at `v` is restored by one edge from that endpoint to a distinct degree-one outside vertex. All other outside edges form disjoint `K₂` components. Equivalently, the core-plus-pendants graph comes from `K_(D+1)` by replacing every edge in `M` with two pendant stubs at its endpoints.

### Case 1: D odd

`D+1` is even. Use a one-factorization of `K_(D+1)` into `D` perfect matchings. Colour the first `α` factors red and the remaining `β` blue. For every missing core edge, give both corresponding pendant stubs the colour formerly assigned to that edge. Each core vertex still has exactly `α` red and `β` blue edges; outside degree-one vertices present no conflict. Colour independent outside `K₂` edges arbitrarily.

### Case 2: D even, α and β both even

`D+1` is odd. By Walecki's explicit decomposition, `K_(D+1)` decomposes into `D/2` edge-disjoint Hamilton cycles. Colour `α/2` cycles red and `β/2` cycles blue. Again replace each deleted core edge by two stubs of the same colour. Every core vertex retains red degree `α` and blue degree `β`; every degree-one vertex trivially satisfies both caps.

### Case 3: D even, α and β both odd, M nonempty

Select a missing core edge `uv∈M`. Choose the Hamilton cycle `C₀` of a Walecki decomposition containing `uv`. Colour `(α−1)/2` of the other Hamilton cycles red and `(β−1)/2` blue; these account for `α−1` and `β−1` incident edges at every core vertex. Delete `uv` from `C₀`, producing a Hamilton path with `D` edges, an **even** number. Alternately colour its consecutive edges red and blue. Every internal path vertex gains one edge of each colour; the two endpoints gain opposite colours. Give the pendant stub at each endpoint the *other* colour. All core vertices now have red degree `α` and blue degree `β`.

For any other missing core edge, colour its two pendant stubs by the colour that edge carried in this assignment. This preserves the two caps. Colour degree-one outside `K₂` components arbitrarily. Thus the desired partition exists whenever `M` is nonempty.

### Case 4: D even, α and β both odd, M empty

The core is `K_(D+1)`, and its edges cannot leave the core. Since every core vertex has degree `D=α+β`, a capped partition would give **exactly** `α` red edges at each core vertex. But `(D+1)α` is odd, contradicting the handshaking lemma. Disjoint outside `K₂` components cannot repair this core parity obstruction. **QED.**

## Ramsey corollary: equality vertex-bound improvements

Let `F(n)=⊔_{i=1}^3 K_{1,n_i}` and `F(m)=⊔_{i=1}^3 K_{1,m_i}`, where both largest star sizes are at least two. Assume the previously proved/reviewed *joint 3×3 residual lower bound* `J=W−(n₁+m₁−1)` (still a mathematical review candidate). Put `D=n₁+m₁−2`, `T=D(D+1)/2`, `E=W−1`, `R=max(|V(F(n))|,|V(F(m))|)`, and `B=2E−D²+1`.

If `E>T` and `R=B`, then the original Ramsey formula `rhat(F(n),F(m))=W` holds.

Indeed, any hypothetical `E`-edge arrowing host must have `Δ=D` and at least `D+1` degree-`D` vertices by the joint deletion, Vizing and cap-partition obstruction arguments. The presence of a forest on `R` vertices means `v_+≥R=B`, and Theorem A gives `v_+≤B`, so the equality classification applies. If the core has any deleted edge, the above theorem provides a cap partition, avoiding a red `K_{1,n₁}` and blue `K_{1,m₁}` simultaneously, hence avoiding both whole target forests. If the core has no deleted edges, then `E>T` implies at least one outside `K₂` component. The equality condition gives `R=B=D+1+2(E−T)>D+1`. Colour **all core edges** in the colour of a target forest that needs `R` vertices and all outside `K₂` edges the opposite colour. The first forest cannot fit inside the `D+1` core vertices; the opposite-colour edges form a matching, so cannot contain the opposite target's largest star of size at least two. Contradiction. The canonical `W`-edge star construction supplies the upper bound. **QED.**

### Parameter enumeration consequence

Within the existing `n₁,m₁≥2`, `D≤9` 3×3 parameter shortlist: baseline `851` ordered pairs not excluded by the old degree-core gates; the odd-degree equality lemma already removed `6`, leaving `845`. The new even-degree equality lemma removes **10 more ordered pairs**, leaving **835** not excluded by the currently implemented gates. The five pairs up to colour exchange are:

| First triple | Second triple | W |
| --- | --- | ---: |
| (2,1,1) | (6,5,3) | 27 |
| (2,1,1) | (6,4,4) | 27 |
| (4,4,2) | (6,6,6) | 43 |
| (4,3,3) | (6,6,6) | 43 |
| (3,3,3) | (7,7,6) | 44 |

`verify_even_core.py` constructs the exact capped split for degree-core equality graphs in 20,433 finite cases, including the degree boundary and the sole pure-complete-core odd/odd exception. `verify_even_core_independent.py` independently searches capped red-degree assignments, without Hamilton decomposition, for 3,608 smaller cases. Both use standard Python only; the parameter corollary enumeration is exact arithmetic and verifies 851→845→835.

**Important diagnostic:** Class II is strictly weaker than a cap-partition obstruction. For example, take `K₅` minus one edge and attach a pendant edge to each of that deleted edge's endpoints. Its core contains nine edges on five vertices; it cannot admit a proper four-edge-colouring, because four matchings cover at most eight core edges. Nevertheless, with `(α,β)=(1,3)`, the constructive theorem gives an exact red/blue degree-capped partition. This explains why generic edge-chromatic arguments alone do not close Erdős #561.

## References and governance

- Walecki's Hamilton decomposition of complete graphs of odd order, with explicit construction: https://web.mat.bham.ac.uk/~tregloac/bristol2.pdf (see also https://sas.uwaterloo.ca/~rwoldfor/papers/pairwise/paper.pdf).
- Underlying degree-core and joint residual proof: `JOINT_3x3_AND_DEGREE_CORE_PROOF.md` at PR #3523.
- The two-component size-Ramsey source: Chunlin You, arXiv:2610.25958v1.

This is a paper-level proof under the GCL internal role-separated review policy. It is **not** an independently certified theorem, and the unrestricted Erdős #561 conjecture remains OPEN.
