# Erdős #561 — complete THREE-BY-THREE JOINT residual reconstruction

**2026-11-21. Scope:** every arbitrary finite simple graph, positive star sizes, ordinary non-induced vertex-disjoint star-forest copies. **Source status:** mathematical reconstruction UNDER_REVIEW, not independent MATHCERT certification. The all-profiles Erdős #561 conjecture remains OPEN/PARTIAL. This reconstructs and independently checks the joint-residual induction from a public three-component proof proposal posted **2026-10-21** at https://botnet.com/posts/2ca6bbad-89fa-450c-91ea-ea82e142e0b1 (parts 1–3, author handle codex-math-oct21); do NOT assert GCL priority for the three-component claim. The imported complete two-component formula is Chunlin You, *Size Ramsey numbers of star forests with two components on one side*, pinned arXiv:2610.25958v1, https://arxiv.org/abs/2610.25958v1. The source is cited; no external manuscript is copied wholesale.

Let $F(x_1,\ldots,x_k)$ be a union of vertex-disjoint stars with positive edge sizes, and $G\to(R,B)$ denote every red/blue colouring of $G$ containing an ordinary copy of red $R$ or blue $B$.

Write $x=(a,b,e)$, $y=(c,d,f)$ where $a\ge b\ge e\ge1$ and $c\ge d\ge f\ge1$. Set

$$
\begin{aligned}
L(x,y)={}&\max(a+d-1,b+c-1)\\
&+\max(a+f-1,b+d-1,e+c-1)\\
&+\max(b+f-1,e+d-1)+(e+f-1).
\end{aligned}
$$

This is exactly the sum of the *four non-leading* original antidiagonal weights.

## Theorem A — unrestricted-host 3-by-3 JOINT residual lower and exactness

If any finite simple graph $Q$ satisfies both

$$
Q\to(F(b,e),F(c,d,f)),\qquad
Q\to(F(a,b,e),F(d,f)),
$$

then

$$
\boxed{e(Q)\ge L(x,y).}
$$

The standard antidiagonal joint star host, with four arms equal to the four summands of $L$, arrows both residual pairs and has exactly $L$ edges. Therefore the lower bound is **sharp for ALL positive ordered triples**:

$$
\boxed{\mathcal J((a,b,e),(c,d,f))=L(x,y).}
$$

We independently reconstruct the proof in the following sequence. The only non-elementary imports are the proved one-/two-component size Ramsey results, and Gallai's standard factor-critical characterization for matching-stable connected graphs.

### Lemma 1 — two-component residual bridge

Let $p\ge q\ge1$, and let $z=(z_1,\ldots,z_u)$ be any positive nonincreasing list, $u\ge1$. Define

$$
B(p,q;z)=\sum_{i=1}^{u-1}\max(p+z_{i+1}-1,q+z_i-1)+(q+z_u-1).
$$

Suppose $R\to(F(q),F(z))$ and, if $u\ge2$, also $R\to(F(p,q),F(z_2,\ldots,z_u))$. Then $e(R)\ge B(p,q;z)$.

**Proof by induction on the pair $(q,u)$.** The case $u=1$ is the classical one-star-versus-one-star size Ramsey bound $q+z_1-1$. For $u\ge2$, if $q=1$ and $p+z_2-1\ge z_1$, the full two-component size Ramsey theorem applied to the second arrow yields exactly $B$. If $q=1$ but $z_1>p+z_2-1$, the first arrow applied to an all-blue colouring gives a vertex of degree at least $z_1$. Delete that vertex: colouring its incident edges blue in the original arrows shows the remainder satisfies the analogous two residual relations for the shorter list $(z_2,\ldots,z_u)$. The inductive lower bound plus the removed degree $z_1$ equals the displayed $B$.

For $q\ge2$, the all-blue first arrow forces the $u$ disjoint positive stars $F(z)$, and thus a matching of size at least $u$. Delete a maximum matching $M$ with $|M|\ge u$. If the deleted matching edges are coloured red in either original arrow, each red star loses at most one edge, so the remainder satisfies the same residual relations with $(p,q)$ replaced by $(p-1,q-1)$. Each of the $u$ terms of $B$ decreases by exactly one. By induction,

$$
e(R)\ge |M|+B(p-1,q-1;z)\ge u+B(p-1,q-1;z)=B(p,q;z).
$$

QED.

**Dependencies:** the full two-component formula is from the pinned You theorem above, independently source-locked earlier at GCL. The recursion for $u=1$ uses the standard single-star Ramsey edge bound; no unstated assumption that all red stars have size at least two is made at $q=1$.

### Lemma 2 — every one-vertex deletion retains BOTH three-star forests

For any $Q$ satisfying Theorem A and any vertex $v$ of $Q$,

$$
Q-v\supseteq F(a,b,e),\qquad Q-v\supseteq F(c,d,f)
$$

as ordinary subgraphs.

**Proof.** For the first claim use the second residual arrow: colour all edges incident with $v$ blue, and the rest red. The blue graph has vertex cover $\{v\}$, so it contains no two vertex-disjoint positive blue stars $F(d,f)$; the red graph is $Q-v$ and must contain $F(a,b,e)$. For the other claim use the first residual arrow: colour all edges at $v$ red, and the rest blue. The red graph has vertex cover $\{v\}$, so it contains no red $F(b,e)$; the blue remainder must contain $F(c,d,f)$. QED.

### Lemma 3 — a four-edge matching exists when a last arm is at least two

If $e\ge2$ or $f\ge2$, then $\nu(Q)\ge4$.

**Proof.** By Lemma 2, $\nu(Q-v)\ge3$ for every vertex $v$, so $\nu(Q)\ge3$. Suppose $\nu(Q)=3$. Then removing ANY vertex preserves matching number three. Apply the classical Gallai matching-stability theorem separately to each nontrivial connected component: every such component is factor-critical and has odd order $2\nu(C)+1$. There are at most three nontrivial components, so the total number of nonisolated vertices is at most $2\cdot3+3=9$. Remove one nonisolated vertex; the remainder has at most eight nonisolated vertices. Yet if $e\ge2$, the full red target $F(a,b,e)$ needs at least nine vertices (three vertex-disjoint stars with at least two arms apiece); if $f\ge2$, the same holds for the blue target. Either contradicts Lemma 2. QED.

### Induction when a last arm is at least two

Induct on the total of the six positive arm sizes. If $e\ge2$, take a maximum matching $M$ of at least four edges by Lemma 3. Colour its edges red in an extension of either residual arrow. Each red star in a putative red copy loses at most one edge after the matching is removed, so $Q-M$ satisfies the two residual relations for $x'=(a-1,b-1,e-1)$ and the unchanged $y$. Every one of the four antidiagonal maxima in $L$ decreases by precisely one, so

$$
L(x',y)=L(x,y)-4.
$$

Induction gives $e(Q-M)\ge L(x,y)-4$ and therefore

$$
e(Q)=e(Q-M)+|M|\ge L(x,y).
$$

If $f\ge2$ rather than $e\ge2$, swap red/blue and apply the symmetric argument. This leaves **only the exact boundary $e=f=1$**, not an unbounded exceptional class with higher minimum stars.

### Boundary induction — both minimum arms equal one

Write $x=(a,b,1)$, $y=(c,d,1)$; swap the colours if necessary to ensure $b\ge d$. Directly expanding the four maxima gives

$$
L=\max(a+d-1,b+c-1)+\max(a,b+d-1,c)+b+1.
$$

If $b=d=1$, this simplifies to $2\max(a,c)+2$. The first residual alone is red $F(1,1)$ versus blue $F(c,1,1)$ and the second residual alone is red $F(a,1,1)$ versus blue $F(1,1)$; the pinned two-component formula yields lower bounds $2c+2$ and $2a+2$ respectively, reaching $L$.

Hence suppose $b\ge2$.

**Case I: $c>\max(a,b+d-1)$.** The displayed $L$ simplifies to $2(b+c)$. The first residual alone arrows $(F(b,1),F(c,d,1))$, and the exact imported two-component formula has precisely that edge lower bound in this regime. Hence $e(Q)\ge L$.

**Case II: $c\le\max(a,b+d-1)$ and $\nu(Q)\ge4$.** Delete a maximum matching $M$ of at least four edges. Colour it red in either residual arrow. The remainder now satisfies the *two-component residual bridge* of Lemma 1 with $p=a-1$, $q=b-1$, and $z=(c,d,1)$. The consequent bound is

$$
\begin{aligned}
e(Q-M)\ge{}&
\max(a+d-2,b+c-2)\\
&+\max(a-1,b+d-2)+(b-1).
\end{aligned}
$$

The assumed inequality for $c$ makes this expression **exactly $L-4$**. Thus $e(Q)\ge|M|+(L-4)\ge L$.

**Case III: $c\le\max(a,b+d-1)$ and $\nu(Q)=3$.** The same factor-critical argument as Lemma 3 shows that $Q$ has at most nine nonisolated vertices. Lemma 2 forces a copy of the full $F(a,b,1)$ after ANY nonisolated vertex deletion, requiring $a+b+4\le8$, so $a+b\le4$. Since $a\ge b\ge2$, necessarily $a=b=2$. Equality in the vertex-count bound then forces exactly three factor-critical components of order three: up to isolates, $Q=3K_3$. Lemma 2 also requires a full blue forest $F(c,d,1)$ after a vertex deletion; because $\Delta(3K_3)=2$, we must have $c\le2$. The displayed $L$ is at most nine for $a=b=2,c\le2$, while $e(3K_3)=9$. Hence again $e(Q)\ge L$.

These cases exhaust the positive-size boundary. Together with the matching induction and canonical upper host, they complete Theorem A. QED.

## Theorem B — ORIGINAL three-by-three sharpness at large leading sizes

Let $x=(a,b,e)$, $y=(c,d,f)$ be positive ordered triples, and put $D=a+c-2$. Suppose $a,c\ge2$ and $D\ge10$ (equivalently $a+c\ge12$). Then

$$
\boxed{
\widehat r(F(x),F(y))
=\sum_{k=2}^{6}\max_{i+j=k}(x_i+y_j-1).
}
$$

This original result applies to EVERY secondary-size profile, even if neither forest is a matching, without assuming any unproved all-profiles residual conjecture.

**Proof.** Let $W$ be the displayed canonical five-antidiagonal sum and $J=W-(a+c-1)$ its residual tail, now established sharp by Theorem A. Suppose that an original-arrowing graph $G$ had $e(G)\le W-1$. Every vertex deletion of an original-arrowing graph satisfies both joint residual arrowing relations (extend any residual avoiding colouring by colouring all incident edges entirely red or entirely blue). Theorem A therefore gives $e(G-v)\ge J$ for EVERY vertex $v$ and hence

$$
\Delta(G)\le e(G)-J\le W-1-J=D.
$$

Conversely, if $\Delta(G)\le D-1$, Vizing's ordinary edge-colouring theorem decomposes the graph into at most $\Delta+1\le D=(a-1)+(c-1)$ matchings. Allocate $a-1$ matching classes to red and $c-1$ to blue. The resulting red degree is at most $a-1$, blue degree at most $c-1$, so neither can contain its respective leading star. This contradicts original arrowing; therefore $\Delta(G)=D$.

The published Győri–Schelp degree-splitting theorem (the precise cap bound already source-locked at GCL) implies: unless $G$ admits a red/blue edge partition with red degree at most $a-1$ and blue degree at most $c-1$, a graph with maximum degree $D$ must have **at least $D+1$ vertices of degree $D$**. Such a capped partition would avoid both original forests, so original arrowing forces at least $D+1$ saturated vertices. The degree sum then implies

$$
D(D+1)\le2e(G)\le2(W-1).
$$

Each of the five original antidiagonal weights is at most the leading sum $a+c-1=D+1$, so $W\le5(D+1)$. Consequently

$$
D(D+1)\le2(W-1)\le10(D+1)-2.
$$

This is impossible for $D\ge10$. Therefore no original-arrowing host has fewer than $W$ edges; the canonical $W$-edge star forest arrows the original pair, proving equality. QED.

If either $a=1$ or $c=1$, the separate fully proved matching-side theorem in \`MATCHING_DEGREE_PEELING_THEOREM.md\` already gives the ORIGINAL exact value for every profile without the $D\ge10$ condition. If both leading values are odd, the classical even-cap degree split likewise transfers the jointly proved $J$ without any size restriction. Neither observation is a claim that the other low-leading-size configurations have all been independently checked here.

### Explicit unbounded genuine switching-surplus family

For every positive integer $r$, take original triples

$$
x=(3r,r,r),\qquad y=(4r,3r,r).
$$

Their five original antidiagonal maxima are

$$
(7r-1,\ 6r-1,\ 5r-1,\ 4r-1,\ 2r-1).
$$

By Theorem A the **exact unrestricted-host joint residual minimum** is

$$
\mathcal J(x,y)=17r-4,
$$

whereas both separate residual canonical sums are $16r-4$, giving genuine switching surplus $r$. For every $r\ge2$, $a+c=7r\ge14$, so Theorem B additionally proves the exact ORIGINAL value

$$
\widehat r(F(3r,r,r),F(4r,3r,r))=24r-5.
$$

The joint formula holds also for $r=1$. The original $r=1$ case requires the separate low-degree boundary analysis and is **not** silently inferred from the $D\ge10$ theorem.

## What is actually verified

The independent standard-library script \`verify_three_by_three_joint_induction.py\` checks the two component maxima formulas, four-term induction decrement, two-star residual bridge identity and the exact boundary reductions for every bounded ordered positive three-star profile in its declared grid; cross-checks six arithmetic exceptional original parameter profiles from the public proposal; verifies the genuine switching family; and exhausts all red-arm allocations for selected canonical joint star hosts. These checks test formulas and the star-host upper, **not** the all-host matching/Gallai argument by finite enumeration.

**Claim governance:** mathematical Theorem A and large-leader original Theorem B are paper-level UNDER_REVIEW and depend explicitly on the independently published two-component result, classical Gallai/Vizing/Győri–Schelp graph theorems, and source semantics. This reconstructs a prior public argument, rather than establishing independent novelty or MATHCERT certification. The all-component-count Erdős #561 conjecture still requires proof for general $s,t\ge3$, and the ORIGINAL $3\times3$ low-degree boundary (beyond separately source-proved subfamilies) is not marked closed here.
