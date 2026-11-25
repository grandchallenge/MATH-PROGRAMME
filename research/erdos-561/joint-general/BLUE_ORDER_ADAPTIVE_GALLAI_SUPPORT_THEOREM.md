# Erdős #561 — blue-target-order-adaptive factor-critical matching obstruction

**Research date:** 2026-11-24. **Scope:** all finite simple host graphs; ordinary non-induced vertex-disjoint positive-star forest copies. **Status:** paper UNDER_REVIEW, finite exact checker CHECKED only on fresh pinned-head replay; full unrestricted Erdős #561 OPEN/PARTIAL, no MATHCERT or novelty-priority assertion.

This is a strict sharpening of the no-triangle Gallai matching threshold already source-locked in parent [PR #3722], not an unrelated second computation. Instead of only excluding factor-critical triangle components, it excludes **every factor-critical component too small to hold the entire BLUE two-star forest**, by the same explicit RED/BLUE whole-component avoiding colouring.

## Theorem V — target-order-adaptive unrestricted-host matching lemma

Let $s\ge3$, $A=F(a_1,\ldots,a_s)$ be any RED forest of $s$ vertex-disjoint positive stars with total required vertex count $V_A=\sum_i(a_i+1)$, and $B=F(v,g)$ be a BLUE forest of TWO positive stars, with required vertex count

$$
V_B=v+g+2\ge4.
$$

Set

$$
\rho=\left\lceil\frac{V_B-1}{2}\right\rceil
=\left\lceil\frac{v+g+1}{2}\right\rceil,\qquad \rho\ge2.
$$

If

$$
\boxed{V_A\ge 2s+\left\lfloor\frac{s}{\rho}\right\rfloor,}
$$

then every finite simple graph satisfying $Q\to(A,B)$ has maximum matching

$$
\boxed{\nu(Q)\ge s+1.}
$$

### Proof for arbitrary graph topology

Colour every edge at an arbitrary vertex $x$ BLUE, all other edges RED. The BLUE graph has vertex cover one, hence cannot contain the two disjoint nontrivial BLUE stars. Therefore $Q-x$ contains RED $A$ for every vertex $x$, so $\nu(Q-x)\ge s$ and $\nu(Q)\ge s$.

Suppose $\nu(Q)=s$. Then deletion of any vertex leaves the matching number unchanged. By the classical Gallai matching-stability/factor-critical theorem, every nonisolated connected component $C_i$ is factor-critical, with its number of vertices $|C_i|=2\mu_i+1$, where $\mu_i=\nu(C_i)\ge1$. The component matching numbers sum to $s$; if there are $q$ such components, the total number of nonisolated vertices is $N=2s+q$.

**Exclude every component with fewer than $V_B$ vertices.** If such a component $C$ existed, colour **every edge of the whole component BLUE** and every edge of the other components RED. BLUE cannot contain $B$, because its entire nonisolated support is strictly smaller than $V_B$. RED cannot contain $A$, because deleting $C$ from the RED graph decreases its matching number by $\nu(C)\ge1$, leaving at most $s-1$ matching edges, while $A$ contains an $s$-edge matching. This is a valid avoiding colouring, a contradiction.

Thus every nonisolated component must have size at least $V_B$, and therefore

$$
2\mu_i+1\ge V_B,\qquad
\mu_i\ge\rho.
$$

As $\sum_i\mu_i=s$, we obtain $q\le\lfloor s/\rho\rfloor$ and

$$
N=2s+q\le2s+\lfloor s/\rho\rfloor\le V_A.
$$

But deleting any nonisolated vertex leaves fewer than $V_A$ nonisolated vertices for the compulsory RED copy of $A$. Contradiction. Hence $\nu(Q)\ge s+1$. QED.

The proof also covers $\rho>s$: in that case $q=0$ would contradict the existence of any nonisolated component in a graph of matching number $s\ge3$. No exceptional division-by-zero or vacuous certificate is introduced.

**Comparison:** Since $\rho\ge2$, this hypothesis never demands more RED support than the parent threshold $2s+\lfloor s/2\rfloor$. When the BLUE target occupies six or more vertices, $\rho\ge3$ and it may demand strictly less. The BLUE target's actual star sizes can only make whole-component avoidance easier; this theorem needs only the vertex-order obstruction, not an unjustified assertion about the structure of its star centres.

## Corollary W — stronger all-s three-BLUE JOINT residual certificate

Let original RED sizes $n=(n_1,\ldots,n_s)$ be sorted positive with $s\ge3$, and BLUE sizes $m=(u,v,g)$ sorted positive. Normalize

$$
a_i=n_i-n_s+1,\quad U=u-g+1,\quad V=v-g+1,
$$

and assume $V\ge2$. For the **normalized second JOINT residual**, the BLUE target is $F(V,1)$, requiring $V+3$ vertices. Its target matching factor is

$$
\boxed{\rho_V=\left\lceil\frac{V+2}{2}\right\rceil
=\left\lfloor\frac{V+3}{2}\right\rfloor.}
$$

Thus the RED support criterion is

$$
\boxed{\sum_i(a_i+1)\ge 2s+\left\lfloor\frac{s}{\rho_V}\right\rfloor.}
$$

Under that criterion the source-proved single-BLUE-matching lower bound of claim 045 remains valid **unchanged**:

$$
e(Q)\ge J_{\rm can}(n,m)-P_B,\qquad
P_B=\sum_{i=1}^{s-1}(a_i-T_i)_+,
$$

where $T_i=\max(a_{i+1}+V-1,\ a_{i+2}+U-1\text{ when }i+2\le s)$.

When $P_B=0$, exact canonical JOINT sharpness is proved over all finite simple hosts. An ORIGINAL sharp size-Ramsey formula requires an independently proven original-transfer condition, such as the fifth all-parity core criterion; it does not follow for free.

### Proof of the corollary

The second JOINT relation demands RED $F(n)$ against BLUE $F(v,g)$. Every terminal RED or BLUE decrement made in the source proof increases or preserves RED support relative to the normalized RED forest $F(a)$, and has BLUE second residual sizes at least those of $F(V,1)$. Thus the BLUE target vertex count at each intermediate step is at least $V+3$, so the corresponding factor $\rho$ never decreases below $\rho_V$. Theorem V supplies a matching of size at least $s+1$ at EVERY normalization stage and the final normalized JOINT host. As in source claim 045, colour the final removed matching BLUE and apply the pinned TWO-component JOINT residual bridge after exchanging colours. The antidiagonal identity for $P_B$ is algebraically identical to that already source-proved in claim 045. QED.

## Exact evidence and boundary

On the protected all-s arithmetic grid with 179,928 sorted RED-terminal-one / BLUE $(U,V,1)$ cases:

| Certificate gate | Parent no-triangle | Target-order adaptive |
| --- | ---: | ---: |
| RED support eligible | 179,368 | 179,635 |
| Eligible with exact BLUE deficit $P_B=0$ | 135,852 | 136,118 |
| Direct newly eligible from previous threshold |  | 266 |

The 267 newly supported cases are a finite-grid consequence of the **analytically proved** improved threshold, not an argument by extrapolating the grid to arbitrary profiles. The complete well-founded proof-tree engine is re-run at exact candidate head and its additional JOINT/ORIGINAL certificates reported separately.

**Remaining boundary:** Cases with positive $P_B$, with BLUE normalized second size $V=1$, or violating the improved RED support threshold remain outside this particular sufficient theorem. Other source-proved recursive, two-component and degree-core rules can still apply; the full Erdős #561 conjecture and unrestricted all-profile JOINT lower remain OPEN/PARTIAL.