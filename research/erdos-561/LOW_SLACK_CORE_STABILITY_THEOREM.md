# Erdős #561 — exact saturated-core obstruction and low-slack reduction

**Date:** 2026-11-18. **Scope:** finite simple graphs and ordinary two-colour size-Ramsey arrowing. **Disposition:** ordinary paper-level proof and exact finite parameter checks; mathematical claim remains `UNDER_REVIEW`. Unrestricted Erdős #561 remains **OPEN**.

## 1. Exact classification when there are D+1 saturated vertices

**Theorem 1.** Let integers `alpha,beta>=1`, `D=alpha+beta>=2`. Suppose a finite simple graph `G` satisfies `Delta(G)=D` and has **exactly D+1 vertices of degree D**. Then `E(G)` fails to admit a partition into red degrees at most `alpha` and blue degrees at most `beta` **if and only if** `G` has an isolated `K_(D+1)` component, `D` is even and both caps `alpha,beta` are odd.

**Proof.** Set `f(v)=alpha` and `g(v)=max(0,d_G(v)-beta)`. An `(g,f)`-factor is exactly the red half of the desired edge partition. By Lovász's non-parity `(g,f)`-factor theorem (as specialized in the previous degree-core proof), failure supplies disjoint `S,T` for which

`0 <= A(S,T) < q(S,T)`;

`A = alpha|S| + sum_(v in T) min(d(v),beta) - e(S,T)`;

`q` counts components of `Y=G-(S union T)` composed entirely of degree-`D` vertices and with `alpha|C|+e(C,T)` odd.

The crucial degree-sum inequality, proved by expanding all terms and using `d(v)<=D`, is

`D A >= alpha e(S,Y) + beta e(T,Y) >= e(S,Y)+e(T,Y)`.

Each counted component of order `c<=D` has at least `Dc-c(c-1)=c(D-c+1)>=D` boundary edges to `S union T`. If **every** counted component had at most D vertices, their combined boundary would be at least `Dq`, hence `A>=q`, contradiction. Thus some counted component `C` has at least `D+1` saturated vertices.

By the hypothesis there are exactly `D+1` saturated vertices globally. Hence `C` contains all of them and `q=1`. Since A is a nonnegative integer and `A<1`, `A=0`. The inequality forces `e(S,Y)=e(T,Y)=0`; hence C has no neighbours outside itself. Every vertex in `C` has `D` neighbours and `|C|=D+1`, so `C=K_(D+1)` is isolated.

Conversely, any other component has maximum degree at most `D-1` and can be properly edge-coloured using at most `D` colours by Vizing's theorem; split these colour classes into `alpha` red and `beta` blue. The isolated clique also admits the capped partition when `D` is odd, by one-factorization of even-order complete graphs, or when `D,alpha,beta` are all even, by a Hamilton-cycle decomposition of the odd-order clique. If `D` is even and `alpha,beta` are odd, the red degree in the clique would have to equal `alpha` at all `D+1` vertices, contradicting the handshaking lemma because both `(D+1)` and `alpha` are odd. **QED.**

## 2. All low-slack failures isolate an odd clique

Let `v_+(G)` be the number of vertices of nonzero degree, and define the degree-core vertex-budget slack

`s(G)=2e(G)-D^2+1-v_+(G)`.

**Theorem 2.** If `G` fails the `(alpha,beta)` capped partition and `0<=s(G)<=D-2`, then `G` contains an isolated `K_(D+1)` and the caps are odd/odd with even D.

**Proof.** The earlier degree-core theorem forces at least `D+1` vertices of degree D. If their number is `k`, the degree-sum inequality yields

`2e-v_+ >= (D-1)k`, so `D^2-1+s(G)>=(D-1)k`.

When `s(G)<=D-2`, this gives `k<D+2`, hence `k=D+1`. Apply Theorem 1. **QED.**

This theorem **subsumes the zero-, one-, and two-slack structural cases** and reaches all integers `s=0,...,D-2`. No enumeration of how pendant and degree-two vertices attach is needed.

## 3. Clique isolation cannot force a sufficiently large star forest

**Lemma 3.** Suppose `G=K_(D+1) disjoint_union H`, with `e(H)=t`, and two target star forests `F_red,F_blue` whose components have positive edge counts. If `|V(F_red)|>D+1+t` and the largest blue star has at least two edges, then `G` does **not** arrow `(F_red,F_blue)`.

**Proof.** Let `v_H` be the number of nonisolated vertices of H. A connected component of H which is a tree contributes `1` to `v_H-t`, whereas a cyclic component contributes at most `0`; hence there are at least `max(0,v_H-t)` nontrivial tree components. In each tree component choose a pendant edge and colour it blue; colour all other edges of H and every clique edge red. The blue edges form a matching, so blue cannot contain any star with at least two edges. One degree-one endpoint in every chosen tree component is isolated in red; the red graph therefore has at most `D+1+v_H-max(0,v_H-t) <= D+1+t` nonisolated vertices. It cannot contain the red target, which requires more vertices. **QED.**

The argument also works with the red and blue targets exchanged.

## 4. Original 3-by-3 Erdős corollary

**Dependency:** the draft theorem `J(n,m)=W(n,m)-(n_1+m_1-1)` for all three-star pairs, proved at paper level in PR #3523 and still subject to substantive mathematical review. Let `n_1,m_1>=2`. Put

`D=n_1+m_1-2`, `W=sum of the five antidiagonal maxima`, `E=W-1`, `T=D(D+1)/2`, `B=2E-D^2+1`, and `R=max(sum(n_i)+3,sum(m_i)+3)`. Define `delta=B-R` and `t=E-T`.

**Corollary 4.** If `0<=delta<=D-2` and `t>delta`, then `rhat(F(n),F(m))=W`.

**Proof.** Any hypothetical graph `G` with at most E edges arrowing both original forests must, by joint residual vertex deletion and Vizing, have exactly E edges, maximum degree D, and fail the `(n_1-1,m_1-1)` capped edge partition. The degree-core bound gives `v_+<=B`, and either all-red or all-blue colouring proves `v_+>=R`. Thus `0<=s(G)=B-v_+<=B-R=delta<=D-2`. By Theorem 2, G contains an isolated clique `K_(D+1)`. Its complement H has `t=E-T` edges, while `R=B-delta=D+1+2t-delta>D+1+t`. Apply Lemma 3 to the **larger-order** target forest (swap colours if necessary); the other forest's largest star has at least two edges. This explicitly constructs a two-colouring avoiding both, contradiction. The canonical disjoint-star host with W edges provides the upper bound. **QED.**

## 5. Exact bounded research consequences

The already recorded 851-ordered-pair shortlist covers `n_1,m_1>=2` and `D<=9`, after baseline edge/vertex/equality-colouring gates. `verify_three_star_low_slack.py` independently recalculates all 4,566 small ordered pairs: the criterion in Corollary 4 eliminates exactly **316** of these 851, leaving **535** not excluded by this research filter. Eliminated cases by delta: `0:16, 1:80, 2:69, 3:69, 4:58, 5:24`. These 316 **subsume** the 6 odd-core, 10 even-core, and 80 one-slack previously reported cases; **do not add** them to 316 again. The exact 316-pair set is confirmed by a second independent arithmetic implementation, with sorted-set SHA-256 `d2d741b5432bacce00fc5fc2a7394b54f966c66c9478dcbcb0e4e6b5e33df91b`.

All 535 remaining parameters have `delta>=D-1`, so the first unresolved structural threshold is whether a hypothetical capped-partition obstruction can have **D+2 or more saturated vertices** without an isolated complete clique. The 535 are *not* all certified-open Erdős instances.

## Verification boundaries

- `verify_core_isolation.py`: exact bounded graph-atlas colouring search on graphs with exactly `D+1` saturated vertices, independent of the Lovász proof.
- `verify_three_star_low_slack.py` and `verify_three_star_independent.py`: independent exact integer enumerations; the scripts prove their finite statements only.
- Core Theorems 1–2 and Lemma 3 above are ordinary unbounded mathematical arguments, not consequences of finite experiments.
- The size-Ramsey corollary depends on the currently unpromoted joint residual three-star result and the published two-component theorem arXiv:2610.25958v1. Keep all claims `UNDER_REVIEW`, and do not promote unrestricted Erdős #561.