# Erdős #561 — exact Lovász factor bridge for capped edge partitions

**Date:** 2026-11-19. **Mathematical status:** complete paper proof based on the classical Lovász `(g,f)`-factor theorem; not kernel-verified as a complete graph-factor theorem. **Programme status:** UNDER_REVIEW pending independently scoped specialist evidence. This is narrower than the full three-star Ramsey claim.

## Theorem (connected maximum-degree core necessity)

Let $G$ be a finite, loopless, simple graph and let $\alpha,\beta$ be positive integers with $\Delta(G)=D=\alpha+\beta$. If its edge set has **no** partition $E(G)=R\sqcup B$ with $\Delta(R)\le\alpha$ and $\Delta(B)\le\beta$, then **some connected component of $G[V_D]$ contains at least $D+1$ vertices**, where $V_D=\{v:d_G(v)=D\}$.

**Contrapositive:** If every connected component of the induced maximum-degree subgraph $G[V_D]$ has at most $D$ vertices, a capped red/blue partition always exists.

### Step 1: A capped edge partition is an ordinary `(g,f)`-factor

Put $g(v)=\max\{0,d(v)-\beta\}$ and $f(v)=\min\{\alpha,d(v)\}$. For an edge subset $R$, set $B=E(G)\setminus R$. Both degree caps hold exactly when

$$
g(v)\le d_R(v)\le f(v) \qquad (v\in V(G)).
$$

This is an ordinary $(g,f)$ factor of $G$. We have $0\le g(v)\le f(v)\le d(v)$ because $d(v)\le D$. At a vertex of positive degree, where $d(v)>0$, the condition $g(v)=f(v)$ holds precisely when $d(v)=D$; isolated vertices also have $g=f=0$ but cannot contribute to an odd-component penalty.

### Step 2: The exact classical input

The ordinary **Lovász `(g,f)`-factor theorem**, *not the parity-factor variant*, states that an appropriate factor exists if and only if, for every pair of disjoint vertex subsets $S,T$,

$$
\delta(S,T):=f(S)+d(T)-g(T)-e(S,T)-q(S,T)\ge0.
$$

Here $q(S,T)$ counts components $C$ of $G-(S\cup T)$ such that **every vertex of $C$ has $g=f$**, and the integer $f(C)+e(C,T)$ is odd. Sums $f(S)$ and $g(T)$ are over the indicated vertices; $e(X,Y)$ counts edges with one end in each disjoint set.

Source: R. C. Brewster, S. McGuinness, M. H. Nielsen, *Factors With Multiple Degree Constraints in Graphs* (2013), Theorem 1.2, https://faculty.tru.ca/smcguinness/gf_factorfinal.pdf ; independently see *Fractional Matchings, Component-Factors and Edge-Chromatic Critical Graphs*, Theorem 2.12, https://link.springer.com/article/10.1007/s00373-020-02266-6 . We use the ordinary factor theorem's precise tight-component condition; replacing it with the ordinary parity-factor theorem would be incorrect.

### Step 3: The two proportional degree bounds

Write $\theta=\alpha/D\in(0,1)$. For each vertex $v$,

$$
g(v)\le\theta d(v)\le f(v).
$$

The left inequality follows from $d(v)-\beta\le\alpha d(v)/D$ since $d(v)\le D$; the right follows from $\alpha d(v)/D\le\min\{\alpha,d(v)\}$. The exact multiplication-free prerequisites are Lean-checked in `Erdos561FactorCut.lean` as `local_lower_envelope` and `local_upper_envelope`.

Let $U=V(G)\setminus(S\cup T)$ and denote by $e_{SS}$, $e_{TT}$, $e_{SU}$, $e_{TU}$ and $e_{ST}$ the five indicated edge categories. Multiplying Lovász's defect by $D$ and using the degree bounds gives

$$
\begin{aligned}
D\delta(S,T)
&\ge \alpha d(S)+\beta d(T)-D e_{ST}-Dq(S,T)\\
&=2\alpha e_{SS}+2\beta e_{TT}+\alpha e_{SU}+\beta e_{TU}-Dq(S,T).
\end{aligned}
$$

The equality here follows by expanding $d(S)$ and $d(T)$, and using $D=\alpha+\beta$ to cancel all $S$ to $T$ edges. Both nonnegative internal-edge terms may be discarded.

### Step 4: Every tight parity component pays its own penalty

Assume for contradiction that every connected component of $G[V_D]$ has order at most $D$. Let $C$ be any component counted by $q(S,T)$. Because it is tight throughout, its vertices all have degree $D$, unless it is an isolated zero-degree vertex. The latter is not parity-odd since $f(C)+e(C,T)=0$. Hence $C\subseteq V_D$; being connected, $1\le r=|C|\le D$.

Each vertex of $C$ has degree $D$. Simplicity of $G$ bounds the total internal incidence count by $r(r-1)$. Since $C$ is a component of $G[U]$, all edges leaving it go into $S\cup T$. Thus

$$
e(C,S)+e(C,T)=rD-2e(C)\ge r(D-r+1)
=D+(r-1)(D-r)\ge D.
$$

Because $\alpha,\beta\ge1$,

$$
\alpha e(C,S)+\beta e(C,T)\ge e(C,S)+e(C,T)\ge D.
$$

Distinct components counted by $q(S,T)$ are vertex-disjoint, so their boundary-edge sets into $S\cup T$ are disjoint. Summing their contributions proves

$$
\alpha e_{SU}+\beta e_{TU}\ge D q(S,T).
$$

Insert this into the preceding defect inequality. We obtain $D\delta(S,T)\ge0$ and $D>0$, hence $\delta(S,T)\ge0$ for every disjoint $S,T$. By Lovász's factor theorem, $G$ admits a $(g,f)$ factor and therefore the desired capped edge partition. This contradicts the assumption. **QED.**

## What is now formally checked, and what is not

`Erdos561FactorCut.lean` checks, for arbitrary natural numbers and without bespoke axioms or placeholders:

- `small_core_boundary`: $D\le r(D-r+1)$ whenever $1\le r\le D$;
- `weighted_boundary`: positive cap weights pay at least $D$ if the combined boundary has at least $D$ edges;
- `local_lower_envelope` and `local_upper_envelope`: exact scaled inequalities for $g=d-\beta$ and $f=\min(\alpha,d)$;
- `cut_certificate`: the scaled cut inequality, assuming the summation data and weighted bound on the $q$ exceptional components.

The previous formal graph file `Erdos561GraphHandshake.lean` checks the graph-level degree sum and its core edge/vertex bounds. **Not yet kernel-checked:** the general Lovász factor theorem itself, semantic extraction of $q(S,T)$ as connected tight parity components, graph-to-cut edge-category partition identities, and the transfer from edge-list graphs to Mathlib `SimpleGraph`. The proof of the complete theorem is paper-level, using a published classical theorem as a black box; its arithmetic reductions are kernel checked.

This bridge supports the earlier degree-core lemma in PR #3523, but does **not** by itself prove the joint three-star residual bound or the unrestricted Erdős #561 conjecture. Specialist review must still evaluate the entire downstream proof and source hypotheses.
