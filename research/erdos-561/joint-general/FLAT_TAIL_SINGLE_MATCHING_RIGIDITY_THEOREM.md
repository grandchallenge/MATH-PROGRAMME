# Erdős #561 — exact flat-tail joint residual by single-matching rigidity

**Date:** 2026-11-21. **Mathematical status:** paper-level theorem UNDER_REVIEW. Hosts may be ANY finite simple graphs, not only disjoint unions of stars. This gives a new infinite strict-switching subfamily of open joint residual issue #3490, not a proof of its unrestricted statement or the original unrestricted Erdős #561 conjecture.

Let $F(n_1,\ldots,n_s)$ denote the vertex-disjoint union of ordinary positive-edge stars. The arrow $G\to(R,B)$ means that every red/blue edge colouring yields red $R$ or blue $B$ as an ordinary, non-induced, vertex-disjoint forest embedding.

## Theorem A — a sharp new infinite joint-residual family

For every pair of integers $c\ge1$ and $b\ge c+1$, the simultaneous residual Ramsey minimum for original red $n=(2,1,1)$ and original blue $m=(b,c,c,c)$ is exactly

$$
\boxed{J\big((2,1,1),(b,c,c,c)\big)=2b+3c+1.}
$$

More explicitly, any finite simple graph $G$ satisfying **both**

$$
G\to(F(1,1),F(b,c,c,c))
$$

and

$$
G\to(F(2,1,1),F(c,c,c))
$$

must have at least $2b+3c+1$ edges. The canonical star forest

$$
F(b,b,c+1,c,c)
$$

has exactly this many edges and satisfies both arrowing relations.

### Proof of the lower bound for b at least three

Fix $b\ge\max(3,c+1)$ and write $H=F(b,c,c,c)$. It has $h=b+3c$ edges and a **unique** maximum-degree vertex of degree $b\ge3$.

The previously protected **sharp single-matching rigidity lemma**, proved in \`RIGID_15EDGE_311_5221_THEOREM.md\`, states:

> If a positive-edge star forest $H$ has $h$ edges and a unique maximum-degree vertex of degree $d\ge3$, and a finite simple graph $G$ of exactly $h+d$ edges arrows $(2K_2,H)$, then $G$ is isomorphic, up to isolates, to $H\sqcup K_{1,d}$.

For clarity, its proof does NOT assume that $G$ is a star forest. Colour all incident edges of an arbitrary vertex red and all others blue. Since red is a single star, it avoids two disjoint red edges; hence $G-v$ contains blue $H$ for every $v$. This forces $\Delta(G)\le d$ when $e(G)=h+d$. The all-blue colouring forces $\Delta(G)\ge d$; a degree $d$ vertex has exact $H$ remaining after deletion. Unique-maximum-degree rigidity and a two-intersecting-red-edges recolouring then exclude a third degree $d$ centre and shared neighbours of the two centres, forcing a detached $K_{1,d}$ component. This is the source-locked complete paper proof.

Without assuming equality, the same red-star deletion argument yields

$$
e(G)\ge h+\Delta(G)\ge h+b=2b+3c
$$

for any graph satisfying the *first* displayed residual arrowing relation. Thus a hypothetical joint host below the claimed value must have exactly $2b+3c$ edges. The rigidity lemma then forces

$$
G\cong F(b,b,c,c,c)
$$

up to isolated vertices.

This forced host **fails the second residual relation**. Colour exactly one edge of each of the three $c$-stars red and all other edges blue, leaving both $b$-stars wholly blue. The red graph is a matching and hence contains no two-edge star; in particular it has no red $F(2,1,1)$. The blue component edge counts are

$$
(b,b,c-1,c-1,c-1).
$$

Since $c-1<c$, only the two $b$-stars have enough blue edges to contain a $c$-edge star; three vertex-disjoint blue $c$-stars are impossible. Therefore this colouring avoids both second-residual targets, contradicting joint arrowing. Every joint host must have at least $2b+3c+1$ edges.

The degenerate boundary $(b,c)=(2,1)$ has $J=8$ by the independent previously protected two-hub peeling family, Theorem C1 of \`JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md\` (its parameters $a=2,b=2,c=1,t=4$). This is the only admissible pair with $b<3$. No unsupported extension of the unique-degree theorem to degree two is made.

### Matching upper bound and explicit antidiagonal arithmetic

The two separate residual pairs have canonical antidiagonal star-size lists

$$
A=(b,b,c,c,c),\qquad
B=(c+1,c+1,c+1,c,c).
$$

Because $b\ge c+1$, their coordinatewise maximum is

$$
\max(A,B)=(b,b,c+1,c,c).
$$

The elementary greedy star-host Ramsey criterion, previously proved for every star-forest pair, shows that the disjoint-star host $F(b,b,c+1,c,c)$ arrows BOTH residual pairs. Its edge count is

$$
b+b+(c+1)+c+c=2b+3c+1.
$$

This matches the unrestricted-host lower bound. QED.

### A genuine, sharply recovered switching surplus

The separate canonical residual edge counts are

$$
L=2b+3c,\qquad R=5c+3.
$$

For $b=c+1$, the larger of these equals the joint value $J=5c+3$ and the algebraic switching surplus is zero. For every $b\ge c+2$,

$$
L=2b+3c\ge5c+4>R,
\qquad
J-\max(L,R)=1.
$$

Thus the theorem recovers exactly **one extra edge of switching surplus in an infinite nonuniform family**, without restricting graph topology or relying on the unproved general joint hypothesis.

## Theorem B — original size-Ramsey consequences, with exact parity scope

The corresponding **original** antidiagonal edge list is

$$
(b+1,b,b,c+1,c,c)
$$

and its sum is

$$
W=3b+3c+2.
$$

For every odd $b\ge3$ and $1\le c\le b-1$,

$$
\boxed{\widehat r(F(2,1,1),F(b,c,c,c))=3b+3c+2.}
$$

This is an ORIGINAL, all-finite-simple-host size-Ramsey equality, not merely a joint-residual value.

For odd $b\ge5$, the leading sizes $2$ and $b$ have opposite parity and $D=2+b-2=b$. Since $c\le b-1$,

$$
W=3b+3c+2\le6b-1\le b(b+1)=D(D+1).
$$

The last inequality holds for all $b\ge5$ because $b^2-5b+1\ge1$. Apply the general core transfer theorem already source-locked in \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`, which deduces the exact original value from the sharp joint residual bound whenever $W\le D(D+1)$ and at least one leading size is odd.

For $b=3$, the permitted $c$ are one and two. Any hypothetical original Ramsey host with at most $W-1$ edges would have maximum degree at most $D=3$ by the sharp joint residual lower bound and vertex deletion. Let $k$ be its number of degree-three vertices. The original blue target $F(3,c,c,c)$ needs $7+3c$ nonisolated vertices, and the degree handshake gives

$$
2e(G)\ge3k+(v_+(G)-k)\ge 2k+7+3c.
$$

Since $e(G)\le W-1=10+3c$,

$$
2k\le20+6c-(7+3c)=13+3c.
$$

For $c=1$ we obtain $k\le8$; for $c=2$ we obtain $k\le9$. The **nine-cubic-vertex saturated matching lemma**, proved independently in \`GENERAL_CORE_ORIGINAL_TRANSFER.md\` from ordinary Lovász $(g,f)$ factor theory, supplies a red degree-one / blue degree-two edge partition. Such a partition avoids both original leading stars of sizes two and three, contradicting original arrowing. Thus the original equality holds also for $b=3$.

For **even** $b$, the general core-transfer density criterion supplies a separate infinite subfamily whenever

$$
3b+3c+2\le b(b+1)/2.
$$

In particular, the inequality holds for **all** $1\le c\le b-1$ when even $b\ge12$, because its worst-case left side is $6b-1$ and $b(b+1)/2-(6b-1)=(b^2-11b+2)/2>0$ for $b\ge12$. We do not assert full coverage of smaller even $b$ from this theorem.

## Reproducibility and review boundary

The independent parameter verifier \`verify_flat_tail_rigidity_family.py\` recomputes both residual and original antidiagonal lists using **two distinct index conventions**. In a declared bounded grid of 360 admissible $(b,c)$ pairs it checks each formula, each parent's separate residual edge sum, the explicit B-avoiding colouring of the *forced equality star host*, and the exact surplus split (345 strict surplus, 15 zero surplus). For a smaller grid it exhausts **271,548** red-arm colouring classes of the canonical joint upper hosts, independently checking both residual arrowing relations, and **233,018** arm colouring classes of the forced lower host for the first residual relation. These finite star-host checks corroborate the upper and equality-colouring steps; the unrestricted-host lower bound is **the paper rigidity lemma**, not finite graph enumeration.

The new theorem inherits the UNDER_REVIEW mathematical status of its source-locked single-matching rigidity lemma. Its original $b=3$ corollary additionally depends on the separately protected nine-cubic-vertex lemma. No complete Lean formalization, independent referee attestation, MATHCERT certificate, or unrestricted Erdős #561 proof is claimed. The open general $s,t\ge3$ joint residual issue #3490 remains **OPEN/PARTIAL**.

**Next genuine research boundary:** lift the single-matching equality rigidity argument to a host with *two or more* edges above the first-residual minimum, such as original $n=(2,1,1)$ against $m=(b,c,c,c,c)$, where the joint antidiagonal switching gap can exceed one. This is an actual arbitrary-host structural obstruction, not an invitation to repeat a solved 14-edge census.
