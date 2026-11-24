# Erdős #561 — factor-critical SMALL-COMPONENT matching theorem and strengthened all-s BLUE residual exactness

**Date:** 2026-11-24. **Status:** unrestricted-host mathematical PAPER theorem UNDER_REVIEW; finite verifier CHECKED only after exact-head replay. The full Burr–Erdős–Faudree–Rousseau–Schelp star-forest size-Ramsey conjecture and the unrestricted general joint-residual hypothesis in #3490 remain **OPEN/PARTIAL**. No MATHCERT or external independent certification is claimed. All star forests are ordinary non-induced vertex-disjoint positive-star unions in finite simple host graphs.

**Actual addition:** The previously protected all-s BLUE-matching proof in \`ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md\` needed normalized RED vertex support at least $3s-1$. The result below proves the same matching size under a strictly weaker, BLUE-size-sensitive condition. It proves new exact arbitrary-host JOINT lower bounds for red forests previously excluded by the old support threshold, and adds a valid near-sharp numerical bound even where NEITHER sufficient guard holds. It is not a repetition of the previously merged all-s theorem.

## 1. Strengthened universal matching obstruction

Let $n=(n_1,\ldots,n_s)$ have $s\ge2$ positive RED star sizes, with RED forest $F(n)$. Define its *excess edge support* over a matching as

$$
E(n):=\sum_{i=1}^{s}(n_i-1)=|E(F(n))|-s\ge0.
$$

Let $v,g\ge1$. The BLUE target is two disjoint positive stars $F(v,g)$, requiring **exactly $v+g+2$ distinct vertices**.

**Theorem A (factor-critical small-component obstruction).** For every finite simple graph $Q$,

$$
Q\to(F(n),F(v,g))
\quad\text{and}\quad
\boxed{2\left\lfloor\frac{s}{E(n)+1}\right\rfloor\le v+g}
\quad\Longrightarrow\quad
\boxed{\nu(Q)\ge s+1}.
$$

The classical source lemma's vertex-support condition $|V(F(n))|\ge3s-1$ is equivalent to $E(n)\ge s-1$. Under that old condition $\lfloor s/(E+1)\rfloor\le1$, so the NEW condition holds automatically for every positive $v,g$. Thus Theorem A subsumes the old matching obstruction; it is strictly stronger when $E<s-1$ but the two BLUE stars are sufficiently large.

**Proof.** Colour every edge incident to an arbitrary vertex $x$ BLUE and every remaining edge RED. The BLUE subgraph has vertex cover $\{x\}$, hence matching number at most one and cannot contain the BLUE forest $F(v,g)$, which has two disjoint edges. Therefore $Q-x$ contains the *full* RED $F(n)$ for every vertex $x$, and $\nu(Q-x)\ge s$. Hence $\nu(Q)\ge s$.

Suppose $\nu(Q)=s$. Then $\nu(Q-x)=s$ for EVERY vertex $x$. Gallai's matching-stability characterization implies each nontrivial connected component $C$ of $Q$ is factor-critical with $|V(C)|=2\nu(C)+1$. Write their positive matching numbers as $r_1,\ldots,r_c$, so $\sum r_j=s$ and the nonisolated vertex count is $N=2s+c$.

Choose any nonisolated vertex $x$. Since $Q-x$ must contain a RED $F(n)$ on

$$
|V(F(n))|=\sum_i(n_i+1)=2s+E(n)
$$

nonisolated vertices, we have $N-1\ge2s+E$, which forces

$$
\boxed{c\ge E+1.}
$$

If $E+1>s$, this contradicts $c\le\sum_j r_j=s$. Otherwise at least one factor-critical component $C_*$ satisfies

$$
r_*=\nu(C_*)\le\left\lfloor\frac{s}{c}\right\rfloor
\le\left\lfloor\frac{s}{E+1}\right\rfloor
\le\frac{v+g}{2}.
$$

It has $|V(C_*)|=2r_*+1\le v+g+1$, **strictly fewer** than the $v+g+2$ vertices of the BLUE target. Colour every edge of that SINGLE component BLUE and all edges in the OTHER components RED. The BLUE graph is contained in $C_*$ and cannot hold $F(v,g)$ for a simple *vertex-count* reason. The RED graph, with $C_*$ deleted, has matching number at most $s-r_*<s$, whereas any RED $F(n)$ contains $s$ vertex-disjoint edges. Thus the RED target is impossible too. This contradicts Q's arrowing relation.

Therefore $\nu(Q)\ge s+1$. The proof makes **no assumption about the topology, density or edge count of the factor-critical components**. QED.

**Why this advances beyond the old proof:** Under the earlier red-support hypothesis one forces all extremal components to be triangles and recolours one triangle. Here there may be factor-critical components of *arbitrary odd order*. One only needs SOME component smaller than the combined vertex requirement of the TWO BLUE stars; the pigeonhole bound supplies exactly that. This method covers many lower-support forests where the triangle-only argument cannot apply.

## 2. Enhanced all-s one-BLUE-matching JOINT theorem

Let original sorted positive RED $n=(n_1,\ldots,n_s)$ with $s\ge3$ and original sorted positive BLUE $m=(u,v,g)$ with $u\ge v\ge g\ge1$. Set

$$
f=n_s,\quad a_i=n_i-f+1,\quad
U=u-g+1,\quad V=v-g+1.
$$

Thus $a_s=1$. The final TWO BLUE normalized arms are $(V,1)$, and $V\ge2$ is assumed. Let

$$
E_0=\sum_{i=1}^s(a_i-1),\qquad
\Gamma=2\left\lfloor\frac{s}{E_0+1}\right\rfloor.
$$

Use the source-proved BLUE matching interference penalty

$$
P_{\rm B}(a,U,V)=
\sum_{i=1}^{s-1}
\left(a_i-
\max\bigl(a_{i+1}+V-1,\ a_{i+2}+U-1\text{ if }i+2\le s\bigr)\right)_+.
$$

Let $J_{\rm can}$ denote the sum of the $s+1$ canonical nonleading antidiagonal star-host sizes.

**Theorem B (strengthened JOINT exactness criterion).** If

$$
\boxed{V\ge2,\qquad \Gamma\le V+1,}
$$

then every arbitrary finite simple simultaneous JOINT residual host $Q$ satisfies

$$
\boxed{
e(Q)\ge J_{\rm can}(n,m)-P_{\rm B}(a,U,V).
}
$$

Therefore if ALSO $P_{\rm B}=0$, the canonical JOINT minimum is EXACT:

$$
\boxed{\mathcal J(n,m)=J_{\rm can}(n,m).}
$$

The former support hypothesis $E_0\ge s-1$ always implies $\Gamma\le2\le V+1$, and is NOT needed as an additional guard. The canonical star host supplies the upper bound.

**Proof.** The SECOND JOINT relation is $Q\to(F(n),F(v,g))$. Theorem A applies at each normalization stage. To see this exactly, when all RED arms are uniformly raised by $t\ge0$, their excess is $E_0+st$, so $\lfloor s/(E_0+st+1)\rfloor\le\lfloor s/(E_0+1)\rfloor$. When all BLUE arms are raised by a common $j\ge0$, the two BLUE residual stars have total size $(V+j)+(1+j)=V+1+2j\ge V+1$. Thus **the normalized guard is the worst case**; it forces matching number at least $s+1$ at EVERY intermediate RED or BLUE normalization step.

For $f>1$, remove a matching of at least $s+1$ edges and colour its edges RED in both residual relations, lowering each RED star size by one. For $g>1$, use BLUE matching edges to lower each BLUE star by one. Both JOINT arrowing conditions survive because any target star meets a matching in at most one edge. At each step every one of the $s+1$ nonleading canonical antidiagonal sizes decreases by exactly one; the graph loses at least $s+1$ edges.

At the final original lists $(a,(U,V,1))$, Theorem A supplies a further matching of size at least $s+1$. Colour it BLUE and delete it. As source-proved in \`ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md\`, the resulting graph jointly arrows the TWO-component BLUE original list $(U-1,V-1)$ against the unchanged arbitrary RED list $a$. The already source-proved two-component JOINT bridge (Lemma 1 in \`THREE_BY_THREE_JOINT_RECONSTRUCTION.md\`, after colour reversal) yields its exact canonical lower. The independently checked antidiagonal identity is

$$
J_{\rm can}(a,(U,V,1))
=(s+1)+J_{\rm can}(a,(U-1,V-1))+P_{\rm B}(a,U,V).
$$

Adding back the RED and BLUE normalization matchings proves the bound and, if $P_{\rm B}=0$, exact sharpness. QED.

### Universal quantitative bound without ANY vertex-support guard

Even if $\Gamma>V+1$, the first paragraph of Theorem A's proof is unconditional: every JOINT host has matching number **at least $s$**, because its second residual forces $F(n)$ after EVERY vertex deletion. The same lower applies to all intermediate residual hosts. There are precisely $(f-1)+(g-1)+1=f+g-1$ normalization and final BLUE matching removals. Every such step removes at least $s$ edges although the canonical total decreases by $s+1$. Thus **unconditionally** for any sorted positive $n,m$ with normalized $V\ge2$,

$$
\boxed{
\mathcal J(n,m)\ge
J_{\rm can}(n,m)-P_{\rm B}(a,U,V)-(f+g-1).
}
$$

This does NOT promote any case with a positive residual deficit to sharp equality. In the terminal-one case $f=g=1$ with $P_{\rm B}=0$, it bounds the true JOINT minimum to the two consecutive possibilities $J_{\rm can}-1$ or $J_{\rm can}$ even without either exact-matching guard. The graph-theoretic obligation to eliminate the remaining one-edge option is open.

## 3. New exact outcomes beyond the source-proved 52-claim recursive engine

The exact previously protected recursive proof engine \`verify_recursive_vertex_budget_certificates.py\` recognizes several other independently sourced sufficient routes: the source BLUE-matching theorem with **old** support guard, the RED matching reduction, exact individual residuals and FOUR protected ORIGINAL core-transfer gates. The new order-sensitive condition is a *new* JOINT leaf with explicit normalized arithmetic, and is then permitted to propagate to ORIGINAL only through one of those existing four transfer gates. It never silently turns UNKNOWN into a proof.

In the source-locked declared grid, with RED component lengths $s=3,\ldots,8$, RED terminal one and preceding nonincreasing entries in $1,\ldots,8$, and BLUE $(U,V,1)$ for $2\le V\le U\le8$, there are **179,928** parameter profiles. The old BLUE guard excludes RED excess $E_0<s-1$. Of these low-support profiles, **1,959** have zero BLUE interference $P_{\rm B}=0$, and **1,671** additionally satisfy the NEW factor-critical component-size guard $\Gamma\le V+1$.

Independent readback against the currently protected 52-claim certificate engine (exact protected source HEAD used for the audit) found that **845** of those 1,671 were already proved by other rules, leaving **826 NEW exact JOINT proof leaves** with no previous certificate. Of those 826, **436** already satisfy one of the FOUR sourced ORIGINAL transfer gates and are therefore also ORIGINAL-exact when the new JOINT leaf is added. The complete recursive engine can propagate further via shorter RED profiles; its final global counts are to be checked by the new exact-head verifier and must not be inferred by simply adding 826 to the old totals.

A concrete newly proved unrestricted-host ORIGINAL example is

$$
n=(3,1,1,1),\qquad m=(3,2,1).
$$

Here $s=4$, $E_0=2<s-1=3$, but $\Gamma=2\lfloor4/3\rfloor=2\le V+1=3$. The independent BLUE interference terms are all ZERO. Hence the canonical JOINT minimum is **exactly $J_{\rm can}=13$**. The canonical ORIGINAL total is $W_{\rm can}=18$; since the leading RED and BLUE sizes are both odd, the protected even-cap original transfer proves **exactly $\widehat r(F(3,1,1,1),F(3,2,1))=18$**. This is not a graph-host-only upper-bound claim.

## 4. Verification, provenance, boundaries

The source checker \`verify_factorcritical_component_order_certificates.py\` verifies all nonnegative integer guards, exhaustive factor-critical matching-number partitions and real component-colouring witnesses in declared bounded instances; it retains every previously accepted certificate and audits the exact recursive extension on the same 179,928-profile grid. Mathematical lemma and recursion-source dependencies are explicit. Tests do NOT establish the unbounded proof by sampling.

**Remaining mathematics:** profiles with positive $P_{\rm B}$, failure of BOTH component-order and old support matching criteria, or no available ORIGINAL transfer; in particular the terminal-one case with $P_{\rm B}=0$ but $\Gamma>V+1$ remains within one edge of sharpness by the source-proved unconditional lower bound. To reach a full all-profile result one must settle these or find actual counterexamples; the existence of a canonical disjoint-star upper host alone is not a lower-bound proof. MATHCERT and the general Erdős #561 remain open.
