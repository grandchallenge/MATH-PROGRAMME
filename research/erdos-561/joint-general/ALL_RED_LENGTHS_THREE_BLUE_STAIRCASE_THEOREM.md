# Erdős #561 — exact heterogeneous star forests with ARBITRARILY MANY RED components versus THREE BLUE components

**Research date:** 2026-11-23. **Mathematical status:** source-backed paper theorem UNDER_REVIEW, deterministic bounded tests CHECKED after exact-head replay. **Host:** arbitrary finite simple graph, ordinary vertex-disjoint non-induced positive star-forest embeddings. Full Erdős #561 and the all-profile JOINT residual conjecture remain OPEN/PARTIAL. No MATHCERT certification, historical priority assertion or unrestricted-all-profile theorem is implied.

This is an induction in the **NUMBER OF RED COMPONENTS**, not merely a parameter scaling of a fixed four- or five-component case. The input is the previously sourced THREE-BY-THREE exact JOINT theorem plus Gallai's classical factor-critical characterization; there is no reliance on assuming the general conjecture.

## 1. General matching-number obstruction for any component count

**Lemma A (unbounded-component Gallai obstruction).** Let $s\ge3$ and let $F(n)$ be a forest of exactly $s$ positive stars, using at least $3s-1$ vertices:

$$
\sum_{i=1}^{s}(n_i+1)\ge3s-1.
$$

For any two positive blue star sizes $v,w\ge1$ and any finite simple graph $Q$,

$$
Q\to(F(n),F(v,w))
\quad\Longrightarrow\quad
\boxed{\nu(Q)\ge s+1.}
$$

**Proof.** For an arbitrary vertex $t$, colour every edge incident with $t$ BLUE and every other edge RED. The blue edge set has vertex cover one and therefore cannot contain the vertex-disjoint forest $F(v,w)$, which requires a matching of two edges. Consequently $Q-t$ must contain the complete RED $F(n)$, and hence $\nu(Q-t)\ge s$ for EVERY $t$. In particular $\nu(Q)\ge s$.

Suppose $\nu(Q)=s$. Then $\nu(Q-t)=s$ for every vertex. Gallai's matching-stability/factor-critical theorem shows that every nontrivial connected component $C$ is factor-critical with $|V(C)|=2\nu(C)+1$. There are at most $s$ such components, since their positive matching numbers sum to $s$. Their total nonisolated vertex count $N$ is therefore at most

$$
N\le2s+s=3s.
$$

For any nonisolated vertex $t$, the graph $Q-t$ contains a copy of $F(n)$ on at least $3s-1$ nonisolated vertices. Thus $N-1\ge3s-1$, so equality $N=3s$ is forced. Equality in the factor-critical count requires exactly $s$ nontrivial components, each with matching number one and order three, and hence each is a triangle. Up to isolated vertices, $Q=sK_3$.

Colour $s-1$ of those triangles completely RED and the last triangle completely BLUE. The red subgraph occupies at most $3(s-1)=3s-3$ vertices, fewer than the red forest requires; the blue subgraph occupies three vertices, fewer than the four needed for two disjoint positive blue stars. This colouring avoids both targets, contradicting arrowing. Therefore $\nu(Q)\ge s+1$. QED.

This lemma holds over **all finite simple hosts**, not merely graphs made of stars or any bounded graph sample.

## 2. General $(s\times3)\to((s-1)\times3)$ matching bridge and exact deficit

Let $s\ge4$, and let the original nonincreasing red and blue lists be

$$
n=(n_1,\ldots,n_{s-1},1),\quad
n_1\ge\cdots\ge n_{s-1}\ge2,\qquad
m=(u,v,1),\quad u\ge v\ge1.
$$

Let $J_s(n,m)$ denote the minimum number of edges in an arbitrary finite simple graph satisfying BOTH joint residual arrowing conditions for original lists $(n,m)$, and let

$$
J_{\mathrm{can},s}(n,m)
=\sum_{k=3}^{s+3}\max_{i+j=k}(n_i+m_j-1)
$$

denote its canonical antidiagonal upper value. Let

$$
q=(n_1-1,\ldots,n_{s-1}-1),
$$

a positive list of length $s-1$. Define the exact nonnegative **tail matching loss**

$$
\boxed{
P_s=(u-\max(n_{s-2},n_{s-1}+v-1))_+
       +(v-n_{s-1})_+.
}
$$

**Theorem B (all-s matching bridge).** If $\Delta_{s-1}\ge0$ is any already-proved deficit such that EVERY joint host for $(q,m)$ has at least $J_{\mathrm{can},s-1}(q,m)-\Delta_{s-1}$ edges, then

$$
\boxed{
J_{\mathrm{can},s}(n,m)-P_s-\Delta_{s-1}
\ \le\ J_s(n,m)\ \le\ J_{\mathrm{can},s}(n,m).
}
$$

**Proof.** The SECOND joint relation for $(n,m)$ arrows red $F(n)$ against blue $F(v,1)$, two positive blue stars. The red forest has at least $3(s-1)+2=3s-1$ vertices. Lemma A provides a matching $M$ containing at least $s+1$ edges. Colour all edges in $M$ RED when extending an arbitrary colouring of $Q-M$. Every red star uses at most one matching edge, so the two original red residual targets, after removing the matching edges and discarding the final red one-edge star, become exactly the two red residual targets of original shorter list $q$. Blue edges are untouched. Therefore $Q-M$ is a valid joint residual host for $(q,m)$ and

$$
e(Q)\ge |M|+e(Q-M)\ge(s+1)+J_{\mathrm{can},s-1}(q,m)-\Delta_{s-1}.
$$

For the exact arithmetic, write the canonical weights of $(n,m)$ in increasing antidiagonal order. The first $s-1$ nonleading entries equal the corresponding entries of $(q,m)$ **plus one**. The final TWO nonleading entries are

$$
\max(n_{s-2},n_{s-1}+v-1,u),\qquad
\max(n_{s-1},v),
$$

and the last entry is one. The corresponding two final entries of $(q,m)$ (before its final one) equal $\max(n_{s-2},n_{s-1}+v-1)-1$ and $n_{s-1}-1$. Subtracting term by term gives the exact identity

$$
\boxed{
J_{\mathrm{can},s}(n,m)
=(s+1)+J_{\mathrm{can},s-1}(q,m)+P_s.
}
$$

Combining with the lower estimate proves Theorem B. The canonical joint star host supplies the upper. QED.

The loss $P_s$ is explicit and does **not** vanish for arbitrary lists. Theorem B does not assert the full unrestricted conjecture.

### Uniform terminal shifts, all component counts

Whenever all $s$ red star sizes and all three blue sizes are positive, and the RED forest retains at least $3s-1$ vertices during the reduction, Lemma A can be applied repeatedly. Removing a RED matching and colouring it red uniformly decrements all red star sizes by one, while preserving both joint arrowing conditions. Analogously, removing a BLUE matching and colouring it blue decrements all three blue star sizes by one, preserving both relations. For $s$ RED and three BLUE stars, there are exactly $s+1$ nonleading antidiagonal weights, and EACH decreases by one per uniform decrement. Thus exact JOINT lower bounds for a minimal terminal-one pair lift by $(s+1)$ edges per unit RED or BLUE increment, without changing the canonical deficit.

## 3. A genuine ALL-s family with exact JOINT and ORIGINAL values

Let $s\ge3$, $h\ge1$ and $r,k\ge0$ be arbitrary integers. Set $x=r+k$. Define original RED list $A^{(s)}_{h,r}$ by

$$
n_1=(2s-3)h+1+r,\qquad
n_2=2(s-3)h+1+r,\qquad
n_i=2(s-i)h+1+r\quad(3\le i\le s).
$$

Thus, e.g., for $s=3$ the RED list is $(3h+1+r,1+r,1+r)$, for $s=4$ it is $(5h+1+r,2h+1+r,2h+1+r,1+r)$, and for $s=5$ it is $(7h+1+r,4h+1+r,4h+1+r,2h+1+r,1+r)$. The BLUE list is

$$
m=(4h+1+k,\,2h+1+k,\,1+k).
$$

Every list is nonincreasing and positive; all components of both forests have at least two edges whenever $r,k\ge1$. Both lists are genuinely heterogeneous for $h\ge1$ and $s\ge3$.

**Theorem C (unbounded RED component count, exact arbitrary-host Ramsey).** For ALL $s\ge3,h\ge1,r,k\ge0$,

$$
\boxed{
\mathcal J(A^{(s)}_{h,r},m)
=(s^2+s-1)h+(s+1)(1+r+k)
}
$$

and

$$
\boxed{
\widehat r(F(A^{(s)}_{h,r}),F(m))
=(s^2+3s)h+(s+2)(1+r+k).
}
$$

The canonical antidiagonal switching surplus equals EXACTLY $h$, hence is unbounded uniformly in the RED length $s$.

### Exact canonical antidiagonal evaluation

For $x=r+k$, the original $s+2$ canonical weights are

$$
w_2=(2s+1)h+1+x,\qquad
w_3=(2s-1)h+1+x,
$$

$$
w_j=2(s+3-j)h+1+x
\quad(4\le j\le s+3).
$$

The last sequence is $(2(s-1)h+1+x,\,2(s-2)h+1+x,\ldots,1+x)$. Summing gives the displayed closed forms for $J_{\rm can}$ (all but first) and $W_{\rm can}$ (all weights), with no approximation. Independently the two individual residual canonical sums both equal

$$
S_1=S_2=(s^2+s-2)h+(s+1)(1+x),
$$

so the **canonical** switching surplus is $J_{\rm can}-\max(S_1,S_2)=h$.

### Proof of sharp JOINT lower for ALL red lengths

First set $r=k=0$. The base $s=3$ is the existing FULL three-by-three arbitrary-host JOINT theorem in \`THREE_BY_THREE_JOINT_RECONSTRUCTION.md\`, not an unproved extension.

Assume the main $s-1$ case sharp. In the $s$-case the smallest red arm is one and the penultimate red arm is $2h+1$. The third-last red arm is at least $2h+1$, and the blue arms are $(4h+1,2h+1,1)$. Consequently the exact Theorem B penalty is ZERO:

$$
P_s
=(4h+1-\max(n_{s-2},(2h+1)+(2h+1)-1))_+
 +(2h+1-(2h+1))_+=0.
$$

By Theorem B, removing a matching of at least $s+1$ RED edges yields a joint host for the original shorter RED list

$$
q=(n_1-1,\ldots,n_{s-1}-1),
$$

whose final arm is $2h$. Remove another $2h-1$ RED matchings of at least $s$ edges each. Lemma A remains applicable because every intermediate red $s-1$-component forest has at least $3(s-1)-1$ vertices and the blue second residual has two positive stars. The resulting RED list is **exactly** $A^{(s-1)}_{h,0}$, and the blue list is unchanged. Thus the total number of removed edges is at least

$$
(s+1)+s(2h-1)=2sh+1.
$$

The explicit formula gives

$$
J_{\mathrm{can},s}-J_{\mathrm{can},s-1}=2sh+1.
$$

By induction $e(Q)$ cannot be below the full canonical $J_{\mathrm{can},s}$. The canonical joint star host attains equality, completing the induction. In particular, the result holds for RED length $s$ with **no upper bound whatsoever**.

Finally, to pass from the terminal-one lists to the displayed arbitrary increments $r,k$, repeat legal RED and BLUE matching deletions at cost at least $s+1$ edges per increment. The reduced targets remain positive at every step and Lemma A's vertex-support condition persists. Since the canonical JOINT tail has $s+1$ entries, its exact increase is $(s+1)(r+k)$. The sharp terminal-one equality therefore lifts to all $r,k$.

### Proof of sharp ORIGINAL formula by the protected core transfer

The just-proved sharp JOINT bound is exactly the prerequisite of the protected \`GENERAL_CORE_ORIGINAL_TRANSFER.md\` theorem. The original leading-degree budget is

$$
D=n_1+m_1-2=(2s+1)h+x.
$$

A direct calculation yields

$$
\begin{aligned}
D(D+1)-2W_{\rm can}
={}&(2s+1)^2h^2-(2s^2+4s-1)h-2(s+2)\\
&+\bigl[(4s+2)h-2s-3\bigr]x+x^2.
\end{aligned}
$$

For $s\ge3,h\ge1$, the first line is at least $2(s^2-s-1)>0$ (replace $h^2$ by $h$); the coefficient of $x$ is at least $2s-1>0$. Thus the whole expression is strictly positive for EVERY permitted parameter. By the protected degree-core transfer, an original-arrowing graph below the canonical value is impossible, and the canonical star forest attains $W_{\rm can}$. This proves the ORIGINAL formula for every $s,h,r,k$.

The theorem is a substantial **all-lengths heterogeneous subfamily**, not the full all-profile conjecture. Its RED component count can grow arbitrarily, its star sizes can all exceed one, and its canonical switching surplus grows linearly in the independent scale $h$.

## 4. Individual residual minima and actual switching gap (optional stronger consequence)

The blue-deleted individual residual has only TWO BLUE components. Its exact unrestricted-host original size Ramsey value $S_2$ follows from the pinned published Chunlin You two-component theorem.

For the red-deleted individual residual, the RED list of length $L=s-1$ has a different staircase shape with its top TWO sizes equal. Define, for $L\ge3$,

$$
B^{(L)}_1=B^{(L)}_2=2(L-2)h+1+r,\qquad
B^{(L)}_i=2(L-i)h+1+r\quad(3\le i\le L).
$$

Its blue list is again $(4h+1+k,2h+1+k,1+k)$. When $L=3$, the previously proved complete THREE-by-THREE JOINT theorem gives sharp joint equality. For $L\ge4$, the matching bridge of Theorem B has ZERO penalty for the two terminal red sizes $(2h+1+r,1+r)$ and blue $(4h+1+k,2h+1+k,1+k)$ after terminal normalization. Removing $L+1$ RED matching edges and then $2h-1$ more matchings of size $L$ reduces to the same $B^{(L-1)}$ family. The matching cost is $2Lh+1$, matching exactly the difference between successive canonical JOINT values. Uniform red/blue increments are carried as in Section 3. This proves the complete sharp JOINT formula for $B^{(L)}$ by induction.

For $L=3$, source-proved three-by-three ORIGINAL is sharp. For $L\ge4$, the protected degree-core ORIGINAL transfer applies: leading degree cap $D_B=2Lh+x$ and the canonical ORIGINAL total is

$$
W_B=(L^2+3L)h+(L+2)(1+x).
$$

Direct expansion gives

$$
D_B(D_B+1)-2W_B
=4L^2h^2-(2L^2+4L)h-2(L+2)
 +\bigl(4Lh-2L-3\bigr)x+x^2.
$$

At $h=1,x=0$ this equals $2(L^2-3L-2)$, which is POSITIVE for $L\ge4$ (its smallest value is $4$ at $L=4$). The polynomial is increasing in $h\ge1$ and $x\ge0$ for $L\ge4$, because its $h$-derivative is at least $6L^2-4L>0$ and the coefficient of $x$ is at least $2L-3>0$. Thus the core transfer yields exact ORIGINAL for every such $L$. The case $L=2$ is the pinned TWO-component theorem.

Hence **both individually required unrestricted-host residual minimum edge counts are exactly** $S_1=S_2$, rather than merely having those canonical upper bounds. Thus the **actual** coupled switching surplus is

$$
\boxed{
\mathcal J-\max\bigl(
\widehat r(F(n_{2:}),F(m)),
\widehat r(F(n),F(m_{2:}))
\bigr)=h
}
$$

for EVERY $s\ge3,h\ge1,r,k\ge0$, and grows without bound. This is stronger than merely computing a canonical star-host difference.

## 5. Verification and the precise remaining boundary

The independent \`verify_all_red_lengths_three_blue_staircase.py\` computes canonical antidiagonals in zero- and one-based conventions, the exact all-s tail matching loss, both all-s family and equal-top residual family closed forms, their component-count recurrences, original core inequalities, individual residual canonical sums and actual switching formula conditional on the separately sourced sharp JOINT/ORIGINAL theorems. It runs a declared exhaustive finite canonical-host arm-colour audit and validates the $sK_3$ matching-stability equality obstruction on finite representatives through actual ordinary vertex-disjoint star-embedding searches.

**The remaining mathematical boundary is STILL the unrestricted variable-list JOINT residual lower bound**, now narrowed by a recursive explicit tail deficit $P_s$ and imported shorter-length JOINT deficits. This package proves exact unrestricted-host values for a broad all-lengths staircase family with genuine switching, but **does not prove the general Erdős #561 conjecture or promote all claims to MATHCERT**.