# Erdős #561 — SIX-edge matching bridge for FIVE-versus-THREE heterogeneous star forests

**Research date:** 2026-11-22. **Mathematical status:** unbounded paper-level proofs UNDER_REVIEW; finite computational checks CHECKED only after exact-head replay. **Host scope:** every finite simple graph; targets are ordinary non-induced vertex-disjoint positive star forests. Historical research priority is NOT asserted without a literature audit. The unrestricted all-profile Erdős #561 conjecture and full joint-residual hypothesis #3490 remain OPEN. No MATHCERT certification.

The new source reduces genuine five-red versus three-blue forests to the preceding protected four-red versus three-blue joint theorem. It does not silently assume either unrestricted conjecture or complete five-by-three sharpness.

## 1. Definitions and exact canonical accounting

Let $n=(a,b,c,d,f)$ and $m=(u,v,w)$ be ordered nonincreasing positive edge counts, with **four red arms larger than the smallest red arm**:

$$
a\ge b\ge c\ge d\ge f+1,\qquad u\ge v\ge w\ge1.
$$

Write $F(n)$ for the vertex-disjoint union of the stars of these sizes. A simultaneous JOINT residual host $Q$ satisfies both

$$
Q\to(F(b,c,d,f),F(u,v,w)),\qquad
Q\to(F(a,b,c,d,f),F(v,w)).
$$

Put

$$
w_k=\max_{i+j=k}(n_i+m_j-1)\quad(2\le k\le8),\qquad
J_5(n,m)=\sum_{k=3}^{8}w_k,\qquad
W_5(n,m)=\sum_{k=2}^{8}w_k.
$$

The canonical star-host criterion gives upper bounds $J_5$ for the simultaneous residual minimum and $W_5$ for the ORIGINAL size Ramsey number, but supplies no arbitrary-host lower bound on its own.

## 2. A matching of SIX edges is compulsory in every joint host

**Lemma F.1.** If a red forest $F(x)$ has **five** positive star components and uses at least **fourteen** vertices, and a blue forest $F(y,z)$ has **two** positive star components, then for EVERY finite simple graph

$$
Q\to(F(x),F(y,z))
\quad\Longrightarrow\quad
\nu(Q)\ge6.
$$

**Proof.** Colour every edge at an arbitrary vertex $t$ BLUE and every other edge RED. This blue graph has a one-vertex cover, so it contains no pair of vertex-disjoint positive blue stars. Therefore every $Q-t$ contains the red forest $F(x)$; in particular $\nu(Q-t)\ge5$ for every vertex $t$. Thus $\nu(Q)\ge5$.

If $\nu(Q)=5$, then $\nu(Q-t)=5$ for every vertex. Gallai's matching-stability/factor-critical characterization applies componentwise. Each nontrivial connected component has odd order $2\nu(C)+1$, and the sum of their matching numbers is five. Since there are at most five nontrivial components, the total number $N$ of nonisolated vertices obeys

$$
N=\sum_C(2\nu(C)+1)\le2\cdot5+5=15.
$$

But removing ANY nonisolated vertex must leave enough nonisolated vertices to embed the red forest, which uses at least fourteen. Hence $N\ge15$, forcing equality, red target order exactly fourteen, and **five factor-critical components each of matching number one**, hence precisely five disjoint triangles $5K_3$.

Colour four of the triangles entirely RED and the fifth entirely BLUE. Red is supported on only twelve vertices, fewer than the fourteen needed by its target. Blue is supported on only three vertices, fewer than the at least four needed for two disjoint positive blue stars. This colouring avoids both targets, contradicting arrowing. Therefore $\nu(Q)\ge6$. QED.

**Corollary F.2.** Every simultaneous JOINT host $Q$ for $(n,m)$ in Section 1 has a matching with at least six edges, because the second residual alone arrows the entire red forest $F(n)$ against the two positive blue stars $F(v,w)$, and

$$
|V(F(n))|=a+b+c+d+f+5\ge4\cdot2+1+5=14.
$$

The same conclusion holds after uniformly decrementing all five red arms until the fifth reaches one, or uniformly decrementing all three blue arms until their third reaches one, since the red profile at every intermediate step retains four arms of size at least two and a positive fifth arm.

## 3. Exact 5×3-to-4×3 matching reduction

For the base case $f=w=1$, write

$$
n=(a,b,c,d,1),\quad a\ge b\ge c\ge d\ge2,
\qquad m=(u,v,1),\quad u\ge v\ge1.
$$

Define the smaller four-red/three-blue original profiles

$$
q=(a-1,b-1,c-1,d-1),\qquad m=(u,v,1).
$$

**Lemma F.3.** Every arbitrary finite simple JOINT host $Q$ for $(n,m)$ satisfies

$$
\boxed{e(Q)\ge 6+\mathcal J(q,m),}
$$

where $\mathcal J(q,m)$ denotes the actual unrestricted-host joint residual minimum for the FOUR-by-THREE pair, and the canonical joint values obey the independent exact identity

$$
\boxed{
J_5(n,m)=6+J_4(q,m)+P_5(n,m)
}
$$

with explicit nonnegative integer loss

$$
\boxed{
P_5(n,m)
=(u-\max(c,d+v-1))_+
 +(v-d)_+.
}
$$

**Proof.** Corollary F.2 supplies a matching $M$ with at least six edges. Given any red/blue colouring of $Q-M$, colour all matching edges RED. Every red target star uses at most one matching edge. Thus a red copy of $F(a,b,c,d,1)$ in the extended colouring reduces, on removing matching edges and discarding its last one-edge star, to $F(a-1,b-1,c-1,d-1)$; a red copy of $F(b,c,d,1)$ similarly reduces to $F(b-1,c-1,d-1)$. Blue targets are unchanged. Consequently $Q-M$ jointly arrows the two residual pairs of $(q,m)$ and has at least $\mathcal J(q,m)$ edges. Therefore $e(Q)\ge |M|+\mathcal J(q,m)\ge6+\mathcal J(q,m)$.

For the algebra, the six nonleading canonical weights for the original five-by-three pair are

$$
\begin{aligned}
w_3&=\max(a+v-1,b+u-1),\\
w_4&=\max(a,b+v-1,c+u-1),\\
w_5&=\max(b,c+v-1,d+u-1),\\
w_6&=\max(c,d+v-1,u),\\
w_7&=\max(d,v),\qquad w_8=1.
\end{aligned}
$$

The five nonleading canonical weights for the reduced four-by-three $(q,m)$ are

$$
w_3-1,\quad w_4-1,\quad w_5-1,\quad \max(c,d+v-1)-1,\quad d-1.
$$

Direct subtraction gives the claimed six-edge equality plus the two positive-part terms $P_5$. This is exact integer algebra, not a conditional inequality. QED.

**Theorem F.4 (quantitative genuine 5×3 result).** For the general positive $n,m$ of Section 1, define the terminally normalized profiles

$$
n^\flat=(a-f+1,b-f+1,c-f+1,d-f+1,1),\qquad
m^\flat=(u-w+1,v-w+1,1),
$$

and the reduced four-red profile

$$
q=(a-f,b-f,c-f,d-f).
$$

Let $\Delta_4\ge0$ be any *source-proved* FOUR-by-THREE lower-bound deficit for $(q,m^\flat)$, meaning that every joint host for those reduced profiles has at least $J_4(q,m^\flat)-\Delta_4$ edges. In particular, the established separate-residual bound, the RED/BLUE matching-deficit theorem, or the new tied-last-two-red theorem may each supply such a lower bound when its hypotheses apply.

Put

$$
P_5^\flat
=\bigl((u-w+1)-\max(c-f+1,(d-f+1)+(v-w+1)-1)\bigr)_+
+\bigl((v-w+1)-(d-f+1)\bigr)_+.
$$

Then every finite simple joint host for $(n,m)$ satisfies

$$
\boxed{
e(Q)\ge J_5(n,m)-P_5^\flat-\Delta_4.
}
$$

**In particular, if $P_5^\flat=0$ and the already-proved four-by-three bound is SHARP ($\Delta_4=0$), then the full five-by-three JOINT residual is exactly canonical over ALL finite simple graph hosts.**

**Proof.** Uniformly decrement all RED arms until the fifth reaches one, using Corollary F.2 to remove at least six RED matching edges per decrement. Separately decrement all BLUE arms until the third reaches one, removing at least six BLUE matching edges at each step; positivity of the original residuals is preserved since all three blue sizes are initially at least $w$ and the terminal size remains positive. In either step both residual arrowing relations survive by the monochromatic matching-extension argument, and all SIX nonleading canonical weights decrease by exactly one.

After $f+w-2$ decrements, the remaining graph jointly arrows $(n^\flat,m^\flat)$. Lemma F.3 then removes a final red matching and reduces it to the four-by-three JOINT problem $(q,m^\flat)$. Each removed matching contributes at least six distinct edges. The exact six-weight identity from Lemma F.3 at the normalized base yields

$$
e(Q)\ge 6(f+w-2)+6+J_4(q,m^\flat)-\Delta_4
=J_5(n,m)-P_5^\flat-\Delta_4.
$$

The canonical joint star host matches the upper bound when both deficits vanish. No 5×3 unrestricted theorem has been assumed. QED.

The **remaining 5×3 boundary** is explicit: the positive matching deficit $P_5^\flat$, plus whatever residual FOUR-by-THREE deficit $\Delta_4$ survives the source-proved bounds. We do not silently replace either with zero.

## 4. A fourth unbounded-switching family: FIVE red stars against THREE blue stars

For EVERY integer $h\ge1$ and independent nonnegative RED and BLUE increments $r,k\ge0$, define

$$
n_{h,r}=(6h+r,3h+r,3h+r,3h+r,1+r),
\qquad
m_{h,k}=(4h+k,2h+k,1+k).
$$

The base $r=k=0$ has six nonleading canonical weights and one leading weight given by

$$
(w_2,\ldots,w_8)
=(10h-1,\ 8h-1,\ 7h-1,\ 7h-1,\ 5h-1,\ 3h,\ 1).
$$

The reduced four-red profile for the base is

$$
q_h=(6h-1,3h-1,3h-1,3h-1).
$$

It has TIED final two red arms. Its normalized top two arms for the preceding four-by-three tied-bottom-red Theorem E.2 are $A=3h+1$ and $B=1$, with $A+B=3h+2\ge5$. Its BLUE profile has $(D,E,1)=(4h,2h,1)$, with $E\ge2$. The proven tied-bottom BLUE matching deficit is

$$
P_{\mathrm{tie}}
=(3h+1-\max(2h,4h))_++(1-4h)_+=0.
$$

Therefore the FOUR-by-THREE joint residual is sharp for $(q_h,m_{h,0})$ for all $h\ge1$.

Meanwhile, for the FIVE-by-THREE pair the new matching loss is

$$
P_5=(4h-\max(3h,5h-1))_+ +(2h-3h)_+=0
\quad\text{for all }h\ge1.
$$

Theorem F.4 thus proves the full FIVE-by-THREE JOINT formula at the base. Uniform RED and BLUE terminal increments retain the same normalized data and both zero deficits; every one of the six joint weights grows by $r+k$. Hence

$$
\boxed{
\mathcal J(n_{h,r},m_{h,k})
=30h-3+6(r+k)
\qquad(h\ge1,\ r,k\ge0).
}
$$

The canonical ORIGINAL edge total and its independently computed antidiagonal switching surplus are

$$
\boxed{
W_5(n_{h,r},m_{h,k})
=40h-4+7(r+k),\qquad
\sigma_{\rm can}=h.
}
$$

Here the switching surplus is exactly the difference between the five-by-three canonical JOINT total and the larger of the two **canonical individual residual** totals. For $h\ge2$ the first individual four-by-three ORIGINAL residual is also sharp by the protected four-by-three joint and degree-core transfer; the other individual residual has two blue components and is sharp by the pinned published two-component theorem. Thus for $h\ge2$ this is also the exact switching gap between the individual unrestricted-host minima. For $h=1$ the canonical arithmetic gap is still $1$ and gives a lower bound on that actual gap, without asserting a separate individual ORIGINAL formula not yet proven.

**ORIGINAL sharpness for ALL $h,r,k$.** Let $x=r+k$, $D=n_{h,r,1}+m_{h,k,1}-2=10h+x-2$. Then

$$
\begin{aligned}
D(D+1)-2W_5
&=10(h-1)(10h-1)\\
&\quad +(20h-17)x+x^2\ \ge0
\end{aligned}
$$

for every $h\ge1$ and $x\ge0$, including the equality case $h=1,x=0$. The protected source-proved general ORIGINAL transfer theorem, \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`, therefore yields the exact size-Ramsey value

$$
\boxed{
\widehat r(F(n_{h,r}),F(m_{h,k}))
=40h-4+7(r+k)
\quad\text{for EVERY }h\ge1,\ r,k\ge0.
}
$$

Choosing $r,k\ge1$ makes **all five RED and all three BLUE star components have at least two edges**. This supplies a completely explicit genuinely heterogeneous FIVE-versus-THREE exact family with unbounded antidiagonal switching surplus, arbitrary graph topology, and no single-edge components on either side.

## 5. Verification and exact boundaries

The standalone \`verify_five_by_three_matching_bridge.py\` checks both independent antidiagonal-index conventions, the exact six-edge matching-deletion deficit for every bounded ordered positive 5×3 profile in its declared range, uniform red/blue terminal-lift identities, the tied-red four-by-three source condition for the infinite scale family, all four closed-form identities and protected original core inequality, and the explicit $5K_3$ avoiding-colouring witness against the smallest eligible five-red-star forest and two-blue-star forest using a true vertex-disjoint non-induced graph embedding oracle. It also exhausts canonical star-host arm allocations for declared small joint/original examples, separately from the unbounded proof.

**No claim of full Erdős #561 closure:** the unrestricted FIVE-by-THREE sharp joint assertion is proved only where BOTH explicit matching and imported four-by-three deficits vanish; the unrestricted five-by-three and arbitrary-length cases remain OPEN/PARTIAL. The paper theorem is UNDER_REVIEW, bounded exact checks CHECKED, no independent MATHCERT certification.