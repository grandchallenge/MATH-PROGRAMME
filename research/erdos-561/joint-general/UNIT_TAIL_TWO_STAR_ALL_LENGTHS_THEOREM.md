# Erdős #561 — exact nonuniform one-edge-tail forests at ALL component counts

**2026-11-21 — paper theorem UNDER_REVIEW.** Hosts are arbitrary finite simple graphs. All target stars have positive edges and are embedded as ordinary, non-induced, vertex-disjoint components. The full Erdős #561 conjecture with arbitrary star-size lists remains OPEN/PARTIAL. This proof is **not** a new claim of historical priority pending a complete literature audit. The published size-Ramsey theorem with two components on one side, pinned Chunlin You, arXiv:2610.25958v1, supplies the only non-elementary size-Ramsey base; the degree-two obstruction is proved constructively here.

Let

$$
A_s=F(\underbrace{2,\ldots,2}_{s-1},1),\qquad
B_t=F(\underbrace{2,\ldots,2}_{t}),\qquad
C_t=F(\underbrace{2,\ldots,2}_{t-1},1).
$$

The value of an antidiagonal star host follows from the standard source-proved canonical star-forest criterion. Write $\mathcal J(n,m)$ for the minimum edges of an arbitrary simple graph satisfying BOTH residual arrowing relations for original star-size lists $n,m$, as in issue #3490.

## Theorem 1 — complete nonuniform versus uniform two-edge stars

For ALL $s,t\ge3$, the exact joint residual and ORIGINAL size-Ramsey numbers satisfy

$$
\boxed{
\mathcal J((2^{s-1},1),(2^t))=3(s+t-3)+2,
}
$$

$$
\boxed{
\widehat r(A_s,B_t)=3(s+t-2)+2.
}
$$

The joint canonical attaining host consists of $s+t-3$ disjoint three-edge stars and one two-edge star. The ORIGINAL canonical attaining host consists of $s+t-2$ disjoint three-edge stars and one two-edge star. Their sizes match the formulas.

## Theorem 2 — complete nonuniform versus nonuniform two-edge stars

For ALL $s,t\ge3$,

$$
\boxed{
\mathcal J((2^{s-1},1),(2^{t-1},1))=3(s+t-3),
}
$$

$$
\boxed{
\widehat r(A_s,C_t)=3(s+t-2).
}
$$

The joint canonical attaining host consists of $s+t-4$ disjoint three-edge stars, one two-edge star, and one one-edge star. The ORIGINAL canonical attaining host consists of $s+t-3$ disjoint three-edge stars, one two-edge star, and one one-edge star.

**Both families include arbitrarily many genuine two-edge stars on BOTH sides and are not covered by the earlier all-uniform theorem.** They hold for unrestricted finite simple host graphs and are not deductions from a star-forest-only lower-bound enumeration.

## The elementary degree-two obstruction

A finite simple graph of maximum degree at most two is a disjoint union of paths, cycles and isolated vertices. On every path or even cycle, alternating red and blue along successive edges makes **each monochromatic subgraph a matching**, so no monochromatic two-edge star exists.

On any odd cycle, alternating colours creates **exactly one monochromatic two-edge star**. We can choose which colour contains that star; the opposite colour has no two-edge star. This includes the three-cycle. Let $k$ be the number of odd cycle components. Their edge counts sum to at least $3k$.

We shall prove two quantitative colouring lemmas. These are stronger than an assertion about particular star-host graphs.

### Lemma 3 — one additional red single edge, blue all two-edge stars

For any positive integers $r\ge1,u\ge1$, any finite simple graph $G$ with

$$
\Delta(G)\le2,\qquad
e(G)<3(r+u-1)+2
$$

has a red/blue colouring containing neither red $F(2^r,1)$ nor blue $F(2^u)$.

**Proof.** Since each odd cycle costs at least three edges, $k\le r+u-1$.

If $k\le r+u-2$, choose alternating colour patterns independently on the odd cycles so at most $r-1$ cycles create a red two-edge-star centre, and at most $u-1$ create a blue such centre. Alternate all paths and even cycles, without creating additional two-edge stars. Red has fewer than $r$ distinct two-edge-star centres and blue has fewer than $u$. Thus both requested forests are impossible, regardless of their trailing single-edge requirements.

If $k=r+u-1$, the strict edge budget gives

$$
e(G)\le3k+1.
$$

Every odd cycle must consequently be a **triangle**; the rest of the graph consists of at most ONE isolated edge, plus isolated vertices. Colour exactly $r$ triangle components wholly red and the remaining $u-1$ triangle components wholly blue. Colour the optional isolated edge blue. Red then has support on only $3r$ vertices, but a red copy of $F(2^r,1)$ needs $3r+2$ vertices. Blue has at most $u-1$ distinct two-edge-star centres: the optional isolated edge cannot supply a two-edge star. This colouring avoids both targets. QED.

### Lemma 4 — one trailing single edge on EACH side

For any $r\ge1,u\ge2$, every finite simple graph $G$ with

$$
\Delta(G)\le2,\qquad e(G)<3(r+u)
$$

admits a red/blue colouring avoiding red $F(2^r,1)$ and blue $F(2^u,1)$.

**Proof.** Here $k\le r+u-1$.

If $k\le r+u-2$, use the same independent alternating colouring: assign at most $r-1$ odd-cycle two-edge-star centres red and at most $u-1$ blue. Both targets require more disjoint two-edge stars and hence are excluded.

Suppose $k=r+u-1$. The strict edge budget implies

$$
e(G)\le3k+2.
$$

There are exactly TWO possible shapes for the nontrivial components:

1. Every odd cycle is a triangle, and the remaining edges (outside the triangles) form at most two edges in path components.
2. Exactly one odd cycle is a five-cycle, the others are triangles, and there are no other edges.

In case 1, colour $r$ triangles wholly red and the other $u-1$ triangles wholly blue. Colour all the remaining zero, one or two edges blue. The red support consists exactly of $r$ disjoint triangles, on $3r$ vertices, fewer than the $3r+2$ needed for red $F(2^r,1)$. Blue contains only $u-1$ triangle-supported two-edge stars, together with at most two extra edges. To obtain an additional blue two-edge star, those two extra edges must form one two-edge path, consuming **both** of them and all three vertices of that path. Then every available blue two-edge star would occupy its whole connected component (triangles or the two-edge path), leaving no disjoint blue edge for the additional single-edge component. If instead the extra edges are disjoint, they supply no additional two-edge star. Hence blue avoids $F(2^u,1)$.

In case 2, colour the five-cycle wholly blue. Colour $r$ of the remaining triangles red, and the other $u-2$ triangles blue. This is feasible because $u\ge2$. The red support contains only $r$ triangles and no spare red edge, excluding red $F(2^r,1)$. A blue five-cycle contains **at most one** vertex-disjoint two-edge star, while each blue triangle contains at most one. Hence blue contains at most $u-1$ disjoint two-edge stars and cannot contain $F(2^u,1)$. QED.

The two lemmas give concrete avoiding colourings for EVERY degree-two graph below the prescribed edge budgets. They are not restricted to star forests, paths, trees, or a bounded number of vertices.

## Deduction of Theorem 1 from Lemma 3

Fix any $t\ge3$ and induct on $s\ge3$.

**Base $s=3$.** The first joint-residual condition is

$$
Q\to(F(2,1),F(2^t)).
$$

The pinned **complete two-component** size Ramsey theorem establishes the lower bound

$$
e(Q)\ge3t+2=3(s+t-3)+2,
$$

and the canonical joint star host gives equality. No proposed three-component theorem is required.

**Inductive joint step.** Suppose $s\ge4$ and the result has been established for $s-1$ with the same $t$. Write $J=3(s+t-3)+2$. Let $Q$ jointly arrow the residual pairs for $(2^{s-1},1)$ and $(2^t)$. Assume for contradiction $e(Q)<J$. The **first** residual relation is

$$
Q\to(F(2^{s-2},1),F(2^t)).
$$

Apply Lemma 3 with $r=s-2$, $u=t$: if $\Delta(Q)\le2$, the lemma constructs a colouring avoiding this first residual pair, contradiction. Hence $Q$ has a vertex $v$ with degree at least THREE.

Colouring all edges incident with $v$ red in both residual relations shows that $Q-v$ jointly arrows the residuals of the **shorter original red profile** $(2^{s-2},1)$ against the unchanged blue profile $(2^t)$. A putative monochromatic copy using $v$ loses at most one star component, and dropping that component leaves a forest dominating the required shorter residual profile. By induction,

$$
e(Q-v)\ge3(s+t-4)+2=J-3.
$$

Adding at least three distinct edges incident to $v$ gives $e(Q)\ge J$, a contradiction. The canonical joint star host supplies the upper.

**ORIGINAL.** Put $W=3(s+t-2)+2=J+3$. Suppose $G\to(A_s,B_t)$ with $e(G)<W$. Lemma 3 with $r=s-1$, $u=t$ forces $\Delta(G)\ge3$. Pick such a vertex $v$. Every $G-v$ jointly arrows the original residual pairs by monochromatic incident-edge extension, so the already proved sharp joint bound gives $e(G-v)\ge J$. Consequently $e(G)\ge3+J=W$, contradiction. Canonical original host gives equality. QED.

## Deduction of Theorem 2 from Lemma 4

Again fix any $t\ge3$ and induct on $s\ge3$.

**Base $s=3$.** The first residual condition is

$$
Q\to(F(2,1),F(2^{t-1},1)).
$$

The pinned exact two-component theorem gives

$$
e(Q)\ge3t=3(s+t-3),
$$

attained by the canonical joint host.

**Inductive joint step.** Let $s\ge4$, and suppose a joint host $Q$ has fewer than $J=3(s+t-3)$ edges. Its first residual relation is

$$
Q\to(F(2^{s-2},1),F(2^{t-1},1)).
$$

Lemma 4 with $r=s-2$, $u=t-1\ge2$ forces a vertex $v$ of degree at least three, because $\Delta(Q)\le2$ would yield an explicit avoiding colouring. Colour all incident edges at $v$ red in both residuals. Then $Q-v$ jointly arrows the original smaller red profile $(2^{s-2},1)$ versus the same blue $(2^{t-1},1)$. Induction gives $e(Q-v)\ge J-3$, and the degree-three vertex contributes the missing three edges. Contradiction. The canonical joint host attains $J$.

**ORIGINAL.** If any $G\to(A_s,C_t)$ had fewer than $W=3(s+t-2)=J+3$ edges, Lemma 4 with $r=s-1$, $u=t-1\ge2$ forces $\Delta(G)\ge3$. For a vertex of degree at least three, $G-v$ jointly arrows the original residual pairs, so $e(G-v)\ge J$. Thus $e(G)\ge J+3=W$, contradiction. Canonical original host gives equality. QED.

## Mathematical significance and scope

The two results cover **nonuniform** original lists for ANY component counts and arbitrary host topology: in Theorem 1 one side has a one-edge tail, and in Theorem 2 **both** sides have a one-edge tail. They are therefore not consequences of the previously published full UNIFORM size Ramsey result. The missing general conjecture concerns arbitrary mixtures and sizes larger than two, where no analogous degree-two path/cycle description applies.

The deterministic checker \`verify_unit_tail_two_stars.py\` independently evaluates original and both residual antidiagonals for broad parameter grids, checks every arm allocation of selected canonical original and joint upper hosts, and reconstructs every finite path/cycle component multiset in a declared small edge range to exercise the degree-two avoiding colour algorithms. The graph checks verify real vertex-disjoint, ordinary non-induced forest embeddings; they are finite tests of the **constructive two-degree lemmas**, not a substitute for the unbounded proofs above.

Claims 034/035 are paper UNDER_REVIEW / finite CHECKED respectively. No novelty or priority assertion is made without full literature analysis; no MATHCERT certification or all-profile conjecture closure is claimed.
