# Erdős #561 — a unique large maximum-degree obstruction up to 2D+1

**2026-11-19.** An unbounded paper proof from the ordinary Lovász factor theorem, verified with finite independent tests. The original three-star Ramsey corollary also requires the existing paper-level joint-residual theorem. The unrestricted conjecture remains OPEN.

## 1. General structure theorem

Let $G$ be a finite simple graph of maximum degree at most $D=\alpha+\beta$ with positive integer caps $\alpha,\beta$. Let $k$ be the number of vertices of degree exactly $D$.

**Theorem.** If `k≤2D+1`, the edges of `G` cannot be coloured red/blue with maximum red degree at most `α` and maximum blue degree at most `β` **if and only if** both caps are odd and `G` has an **isolated connected `D`-regular component of odd order**. Such a component necessarily has between `D+1` and `2D+1` vertices.

### Proof

Set the red-degree factor bounds

$$
g(v)=\max\{0,d(v)-\beta\},\qquad f(v)=\min\{\alpha,d(v)\}.
$$

These satisfy `0≤ g≤ f≤ d_G`. The ordinary Lovász `(g,f)`-factor theorem says an admissible red factor exists precisely when every pair of disjoint vertex sets `S,T` satisfies

$$
A(S,T):=f(S)+\sum_{t\in T}\min\{\beta,d(t)\}-e(S,T)\ge q(S,T).
$$

The term `q` counts connected components `C` of `G-(S∪ T)` where all vertices have `g=f` and `f(C)+e(C,T)` is odd. This *ordinary* theorem with the exact boundary-to-`T` clause appears in Kano and Saito, *A Short Proof of Lovász's Factor Theorem*, Theorem 1: https://gorogoro.cis.ibaraki.ac.jp/web/papers/newKanoSaitoFactor1984.pdf . This is **not** the separate parity-factor theorem. Isolated degree-zero vertices cannot contribute to `q`, and all other counted vertices have degree exactly `D`.

Let $U=V(G)\setminus(S\cup T)$. The proportional bounds $D f(v)\ge\alpha d(v)$ and $D\min(\beta,d(v))\ge\beta d(v)$ imply

$$
D A(S,T)\ge2\alpha e(S)+2\beta e(T)+\alpha e(S,U)+\beta e(T,U).
$$

In particular $A\ge0$. In a violated cut, $A<q$ with both quantities integers, so $q\ge1$ and $A\le q-1$. Every counted component $C$ of order $r\le D$ has at least

$$
rD-r(r-1)=r(D-r+1)\ge D
$$

edges leaving it, because $G$ is simple and all its vertices have degree $D$. These edges go into $S\cup T$ and each has positive weighted contribution at least one. We call such components **small**.

If all `q` components were small, the displayed inequality would give `D A≥ Dq`, a contradiction. Thus at least one counted component `C_*` contains `D+1` degree-`D` vertices. Because `k≤2D+1`, **there can be only one large counted component**. All the other `q-1` components are small and together contribute at least `D(q-1)`.

Define the large component's weighted boundary as

$$
b_*=\alpha e(C_*,S)+\beta e(C_*,T)\ge0.
$$

Then `D A≥ D(q-1)+b_*`, whereas `D A≤ D(q-1)`. Hence `b_*=0`. Positivity of both caps gives no edges from `C_*` into `S∪ T`. As `C_*` is a component of `G[U]`, it also has no edges into other parts of `U`. It is therefore an **isolated, connected, `D`-regular component of `G`**.

Its parity condition reduces to $\alpha|C_*|$ odd. Consequently $\alpha$ and $|C_*|$ are odd. The degree-sum identity forces $D$ even in an odd-order regular graph; hence $\beta$ is odd. Its order lies between $D+1$ and $k\le2D+1$.

Conversely, suppose such an isolated odd-order regular component exists with odd caps. Any capped split must give *every vertex* of that component exactly $\alpha$ red incident edges, since both caps sum to $D$. The sum of red degrees would be odd, contradicting the handshake lemma. Thus no split exists. QED.

**Interpretation:** the previous bound `k≤ D+2` extends to `2D+1`. We no longer require an isolated complete graph: an arbitrary odd-order `D`-regular connected component can obstruct. In particular, for even `D`, the graph obtained by deleting a Hamilton cycle from `K_{D+3}` is a connected example. We make no claim that the new threshold is optimal.

## 2. Three-star Ramsey consequence

Let the red and blue targets be disjoint unions of three stars, given by nonincreasing positive triples `n`, `m`, whose largest entries are at least two. Let `W` be the conjectured antidiagonal edge count. Define the quantities

$$
D=n_1+m_1-2,\quad E=W-1,\quad R=\max\{\textstyle\sum n_i+3,\textstyle\sum m_j+3\},
$$

$$
s=2E-D^2+1-R.
$$

**Conditional corollary.** Assuming the paper-level joint three-star residual theorem from MATH-PROGRAMME, if `s < D²−1`, then a hypothetical graph with `E=W−1` edges arrowing both three-star forests must have an isolated, connected, odd-order `D`-regular component, and both caps `n₁−1`, `m₁−1` must be odd.

**Proof.** The joint-residual theorem and the largest-star Vizing reduction force every counterexample to have exactly `E` edges, maximum degree `D`, and no `(n₁−1,m₁−1)` capped split. The earlier degree-core theorem forces at least `D+1` degree-`D` vertices. If at least `2D+2` vertices had degree `D`, their degree excess would satisfy

$$
2E-v_+(G)\ge(D-1)(2D+2).
$$

But `v₊(G) ≥ R`, so this would force

$$
s\ge(D-1)(D+1)=D^2-1,
$$

contrary to the assumption. Hence the number of maximum-degree vertices is at most `2D+1`, and the general theorem applies.

**Explicit exterior-colouring exclusion.** Suppose the isolated `D`-regular odd component has `c` vertices. It uses exactly `cD/2` edges; the remaining graph has `t=E−cD/2` edges. Colour the core with the colour whose target forest needs `R` vertices. In each nontrivial tree component of the remaining graph, colour one leaf edge the opposite colour and all other edges the core colour; colour cyclic components entirely the core colour. The opposite-colour edges are a matching, so avoid the opposite target (its largest star has at least two edges). The core-colour subgraph has at most `c+t` nonisolated vertices, so avoids its target whenever

$$
R>c+t=c+E-cD/2.
$$

Thus we can exclude the counterexample if the caps fail the odd/odd parity test, **or** the last inequality holds for every feasible odd component order `c` from `D+1` to `2D+1` with `cD/2≤E`.

## 3. Exact bounded results

The fresh, independent integer implementation `verify_parameter_gate.py` reproduces the 851-case earlier shortlist and the 512 earlier D+2 exclusions. It eliminates **186 additional ordered pairs**, leaving **153** research-filter survivors. Of the 186, **176** fail the new parity/unique-core test and **10** fail the explicit exterior-colouring test.

| Forced degree D | Excluded now | Surviving filter entries |
| --- | ---: | ---: |
| 2 | 0 | 9 |
| 3 | 4 | 32 |
| 4 | 22 | 70 |
| 5 | 118 | 0 |
| 6 | 40 | 42 |
| 7 | 2 | 0 |
| Total | **186** | **153** |

`verify_general_core.cpp` independently examines every simple labelled graph on 2 through 6 vertices: 33,866 graphs, 91,727 degree-cap tests. In the 91,657 cases below the `k≤2D+1` threshold, **every** result matches the isolated odd-order regular-component characterization. The program also tests the connected `K_(D+3)`-minus-Hamilton-cycle family for D=2,4,6. The checked general Lovász criterion agrees with explicit red/blue edge searches on 2,809 selected instances. These finite tests corroborate, but do not prove, the unbounded theorem.

**The 153 remaining entries are not 153 new established open problems:** they are only entries not eliminated by the specific tests above. Full Erdős #561, four-or-more-component residual results, and the high-degree-core regime beyond `2D+1` remain open.
