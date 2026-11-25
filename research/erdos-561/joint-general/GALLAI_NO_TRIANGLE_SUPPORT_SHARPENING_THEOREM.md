# Erdős #561 — exclude triangle factor-critical components to sharpen the all-s matching threshold

**Research date:** 2026-11-24. **Mathematical status:** UNDER_REVIEW; deterministic finite computations CHECKED only following exact-head replay. **All hosts:** arbitrary finite simple graphs, with ordinary non-induced vertex-disjoint positive-edge star forests. No global Erdős #561 theorem, MATHCERT certification, or historical priority claim.

**Precise contribution:** The previously protected all-s single-BLUE-matching theorem (claim 045, source \`ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md\`) obtains a matching of size at least $s+1$ using the normalized RED vertex-support assumption $V\ge3s-1$. That threshold can be reduced to the strictly weaker

$$
\boxed{V\ge 2s+\lfloor s/2\rfloor}
$$

by eliminating every *three-vertex factor-critical component* of a hypothetical matching-stable graph before applying its vertex budget. This is a genuine all-host graph-theoretic strengthening; the algebraic BLUE penalty and the source two-component bridge remain unchanged.

## Lemma T — improved general matching obstruction

Let $s\ge3$ and let $A=F(a_1,\ldots,a_s)$ be any positive star forest with $s$ pairwise vertex-disjoint nontrivial stars, requiring $V_A=\sum_i(a_i+1)$ vertices. Let $B=F(v,g)$ consist of two positive stars, with $v,g\ge1$. If

$$
V_A\ge 2s+\lfloor s/2\rfloor
$$

and a finite simple graph $Q$ arrows $(A,B)$, then its maximum matching has **at least $s+1$ edges**.

### Unrestricted-host proof

For each vertex $x$ of $Q$, colour all edges incident to $x$ BLUE and every other edge RED. The BLUE graph has a one-vertex cover and cannot contain the two vertex-disjoint positive BLUE stars of $B$. Thus $Q-x$ must contain a complete RED $A$, so

$$
\nu(Q-x)\ge s\quad\text{for EVERY vertex }x.
$$

In particular $\nu(Q)\ge s$. Assume $\nu(Q)=s$. Then $\nu(Q-x)=\nu(Q)$ for every vertex. Apply the classical *Gallai matching-stability/factor-critical theorem* componentwise: every nonisolated connected component $C$ is factor-critical and has odd order $|C|=2\nu(C)+1$. Its matching number is at least one. Write the nonisolated components $C_1,\ldots,C_q$, with matching numbers $\mu_i=\nu(C_i)$. Then

$$
\sum_{i=1}^q\mu_i=s,\qquad N:=\sum_i|C_i|=2s+q.
$$

**Exclude every factor-critical triangle component by a concrete avoiding colouring.** Such a connected simple factor-critical component has three vertices and is exactly a triangle $K_3$. Colour all three of its edges BLUE and every edge of the remaining graph RED (isolated vertices irrelevant). The BLUE triangle cannot contain two vertex-disjoint positive stars because even $F(1,1)$ needs four vertices. The RED part has matching number at most $s-1$, since deleting the triangle component removes exactly one unit of matching capacity. Every RED copy of the red forest $A$ with $s$ components would contain a matching of $s$ edges, one from each disjoint star. Hence RED also avoids $A$. This contradicts the arrowing hypothesis.

Therefore **all nonisolated factor-critical components have $\mu_i\ge2$**. There are at most $\lfloor s/2\rfloor$ such components, so

$$
N=2s+q\le 2s+\lfloor s/2\rfloor\le V_A.
$$

Choose any nonisolated vertex $x$. The red copy of $A$ compelled inside $Q-x$ has $V_A$ distinct nonisolated vertices of $Q-x$, but the latter has at most $N-1\le V_A-1$ nonisolated vertices. Contradiction. Consequently $\nu(Q)\ne s$, proving $\nu(Q)\ge s+1$. QED.

**Important distinction from the old threshold:** We do not claim that a host whose maximum matching is $s$ must consist only of triangles. Instead, we show that the existence of *any* factor-critical triangle component already contradicts arrowing; all surviving components must use at least two matching edges, giving the stronger bound.

## Corollary U — strengthened all-s BLUE-matching residual criterion

Let the original sorted positive RED list have arbitrary length $s\ge3$, $n=(n_1,\ldots,n_s)$, and the original BLUE list be $m=(u,v,g)$ with $u\ge v\ge g\ge1$. Normalize

$$
a_i=n_i-n_s+1,\qquad U=u-g+1,\qquad V=v-g+1.
$$

Assume $V\ge2$ and the **new weaker normalized RED vertex-support condition**

$$
\boxed{\sum_{i=1}^s(a_i+1)\ge 2s+\lfloor s/2\rfloor.}
$$

Use *exactly the already source-proved BLUE matching loss* of claim 045,

$$
T_i=\max\{a_{i+1}+V-1,\ a_{i+2}+U-1\text{ if }i+2\le s\},\qquad
P_B=\sum_{i=1}^{s-1}(a_i-T_i)_+.
$$

For every arbitrary finite simple simultaneous JOINT residual host $Q$ for the pair $(n,m)$, the exact unrestricted-host lower bound is

$$
\boxed{e(Q)\ge J_{\rm can}(n,m)-P_B.}
$$

Consequently $P_B=0$ suffices for the exact canonical **JOINT** minimum, including the newly eligible RED profiles whose support lies between $2s+\lfloor s/2\rfloor$ and $3s-2$. Where an individually proved sharp JOINT certificate is available, *any* of the separately protected GENERAL ORIGINAL degree-core transfer criteria still applies, in particular the fifth all-parity support criterion $2W\le D^2+R$; that remains a separate theorem, not an automatic implication of $P_B=0$.

### Proof

The second residual arrows the complete RED forest $F(n)$ against the two positive BLUE stars $F(v,g)$. Every intermediate graph in the normalization and matching-deletion argument of \`ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md\` therefore satisfies Lemma T, since the normalized RED forest $F(a)$ meets the improved vertex-support threshold and all earlier RED minima are at least those of $a$.

Each normalization step removes a matching with at least $s+1$ edges and colours them entirely RED or BLUE as appropriate, preserving both JOINT arrowing relations while decrementing exactly $s+1$ nonleading canonical antidiagonal weights by one. In the terminal-one case $a_s=1$ and normalized BLUE $(U,V,1)$ with $V\ge2$, remove one final BLUE matching with $s+1$ edges. The remaining graph arrows precisely the two residual conditions for original RED $a$ against the BLUE two-component profile $(U-1,V-1)$. By the source-proved TWO-component residual bridge after exchanging colours, it has at least $J_{\rm can}(a,(U-1,V-1))$ edges. The existing **exact algebraic identity** from claim 045 is

$$
J_{\rm can}(a,(U,V,1))=(s+1)+J_{\rm can}(a,(U-1,V-1))+P_B.
$$

Thus the same quantitative lower follows with the new matching threshold; a canonical disjoint-star host supplies the upper when $P_B=0$. QED.

## Exact finite coverage and non-claims

In the pre-existing declared exhaustive arithmetic grid of original BLUE $(U,V,1)$, $2\le V\le U\le8$, and RED sorted terminal-one profiles of lengths $3\le s\le8$ with preceding arms from 1 through 8, the previous $3s-1$ threshold supported 177,856 of 179,928 profiles, including 134,447 with $P_B=0$.

The new threshold qualifies **179,368** profiles, including **135,852** zero-penalty profiles: **1,512 additionally supported** and **1,405 newly eligible exact JOINT profiles** by this direct theorem. These are strictly bounded grid counts and do not count all integer profiles. An independent, monotone *recursive certificate engine* may discover further JOINT and ORIGINAL exact results by applying the upgraded source lemma to the already protected 54-claim recursive proof rules.

The new theorem is a stronger sufficient condition; it does **not** assert exact sharpness for $P_B>0$, for a normalized second BLUE size $V=1$, or for normalized RED support below $2s+\lfloor s/2\rfloor$. The unrestricted all-profile JOINT residual question #3490 and original Erdős #561 remain **OPEN/PARTIAL**.