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

This forced host **fails the second residual relation**. Colour exactly one edge of each of the three stars of size $c$ red and all other edges blue, leaving both stars of size $b$ wholly blue. The red graph is a matching and hence contains no two-edge star; in particular it has no red $F(2,1,1)$. The blue component edge counts are

$$
(b,b,c-1,c-1,c-1).
$$

Since $c-1$ is strictly less than $c$, only the two stars of size $b$ have enough blue edges to contain a star with $c$ edges; three vertex-disjoint blue stars of size $c$ are impossible. Therefore this colouring avoids both second-residual targets, contradicting joint arrowing. Every joint host must have at least $2b+3c+1$ edges.

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

## Theorem B — full parity-free ORIGINAL size-Ramsey family

For every pair of integers $c\ge1$, $b\ge c+1$, with **NO parity restriction**,

$$
\boxed{\widehat r(F(2,1,1),F(b,c,c,c))=3b+3c+2.}
$$

This original size-Ramsey equality holds over **all finite simple graph hosts**, not only disjoint-star hosts. The original antidiagonal star sizes are $(b+1,b,b,c+1,c,c)$ and sum to $W=3b+3c+2$. By Theorem A, the individually proved sharp joint residual lower is $J=2b+3c+1$. For any proposed original-arrowing graph with $e(G)\le W-1$, deleting any vertex gives both residual relations, hence $\Delta(G)\le W-1-J=b=:D$.

### Odd leading b

For odd $b\ge5$, the leading sizes two and $b$ have opposite parity. Since $c\le b-1$,

$$
W=3b+3c+2\le6b-1\le b(b+1)=D(D+1).
$$

The final inequality holds for all $b\ge5$ since $b^2-5b+1\ge1$. Apply the general core transfer theorem in \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`.

For $b=3$, the permitted $c$ are one and two. Any hypothetical original Ramsey host has $e(G)\le W-1=10+3c$, $\Delta(G)\le3$, and at least $7+3c$ nonisolated vertices because its all-blue colouring contains the original forest $F(3,c,c,c)$. If $k$ vertices have degree three,

$$
2k+7+3c\le2e(G)\le20+6c,
\qquad
2k\le13+3c.
$$

Thus $k\le8$ for $c=1$ and $k\le9$ for $c=2$. The source-locked **nine-cubic-vertex saturated matching lemma** in \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`, proved from the ordinary Lovász $(g,f)$ theorem, supplies a red degree-one / blue degree-two partition, avoiding both original leading stars. This contradicts original arrowing.

### Even leading b: regular-core edge-budget exclusion

For $b=2$, the only admissible value is $c=1$. The original exact eleven-edge equality was already proved by the complete 106-class maximum-degree-two certificate in \`GENERAL_CORE_ORIGINAL_TRANSFER.md\`; it is not asserted afresh from the unique-core theorem.

Now suppose $b\ge4$ is even. The proposed capped degrees are $(1,b-1)$, both odd. In an original-arrowing $G$ with $e(G)\le W-1=3b+3c+1$ and $\Delta(G)\le b$, **no** such capped partition can exist, since it would avoid the original leading star of size two in red and size $b$ in blue.

Let $k$ count the degree $b$ vertices and $v_+(G)$ the nonisolated vertices. All-blue arrowing requires a blue copy of $F(b,c,c,c)$, with $b+3c+4$ nonisolated vertices, so $v_+\ge b+3c+4$. The handshake estimate gives

$$
2e(G)\ge v_+(G)+(b-1)k.
$$

Consequently,

$$
(b-1)k
\le 2(W-1)-(b+3c+4)
=5b+3c-2
\le8b-5.
$$

For every even $b\ge4$,

$$
8b-5 < 2b^2-2 = (b-1)(2b+2),
$$

since $2b^2-8b+3>0$. Therefore $k\le2b+1$. The previously source-locked **unique large core** theorem, derived from the ordinary Lovász $(g,f)$ criterion, now applies: a non-partitionable $G$ must contain an *isolated connected odd-order degree $b$ regular component* $C$. Write $u=|V(C)|$. Then $u$ is odd, $u\ge b+1$, and the core consumes exactly $bu/2$ edges.

The all-blue colouring must contain the original blue forest $H=F(b,c,c,c)$, with $M=b+3c$ edges. Because $C$ is isolated, the copy of $H$ splits its components between $C$ and the exterior. The portion inside $C$ is a **forest on at most $u$ vertices** and therefore uses **at most $u-1$ edges**. The exterior must contribute at least $M-(u-1)$ edges. Consequently, a *necessary condition* for an all-blue copy of $H$ is

$$
e(G)\ge\frac{bu}{2}+M-(u-1)
=M+u\left(\frac b2-1\right)+1.
$$

But the counterexample budget gives $e(G)\le W-1=M+2b+1$. Therefore

$$
u\left(\frac b2-1\right)\le2b.
$$

For every even $b\ge6$, this is impossible because $u\ge b+1$ and

$$
(b+1)\left(\frac b2-1\right)>2b
\quad\Longleftrightarrow\quad
b^2-5b-2>0.
$$

Thus **no original counterexample exists for any even $b\ge6$**, irrespective of $c$. This exclusion uses only the edge cost of the isolated regular core and the acyclicity of the required blue target forest; it does not assume a special exterior graph topology.

It remains to handle $b=4$. The necessary inequality becomes $u\le8$; combined with odd $u\ge5$, it leaves **only $u=5$ or $u=7$**.

- If $u=5$, the core consumes ten edges; the exterior has at most $(W-1)-10=(13+3c)-10=3c+3=M-1$ edges. Colour all core edges red and all exterior edges blue. The red target $F(2,1,1)$ needs seven vertices, more than the five in the core; the blue target needs $M=4+3c$ edges, more than the exterior has. Thus this explicit colouring avoids both targets.
- If $u=7$, the core has fourteen edges and the exterior has at most $(W-1)-14=3c-1$ edges. An all-blue copy of $F(4,c,c,c)$ would therefore require at least $M-(3c-1)=5$ of its edges inside the seven-vertex core. For $c=2$ or $c=3$, this is impossible: a four-edge star occupies five vertices and cannot be accompanied by a vertex-disjoint $c$-edge star (which needs at least three more vertices). If no four-edge star lies inside, at most two $c$-edge stars can fit in seven vertices; when $c=2$ these provide at most four edges, and when $c=3$ only one such star fits, providing three edges. Hence no all-blue copy exists. For $c=1$, colour the core blue and exterior red. Blue is then confined to seven vertices, fewer than the eleven needed by $F(4,1,1,1)$, and red has at most two edges, fewer than the four in $F(2,1,1)$. Again both targets are avoided.

Every even $b$ is now excluded from a smaller original Ramsey host, completing the proof for all parities. The canonical antidiagonal star forest gives the required $W$-edge upper bound. QED.

## Reproducibility and review boundary

The independent parameter verifier \`verify_flat_tail_rigidity_family.py\` recomputes both residual and original antidiagonal lists using **two distinct index conventions**. In a declared bounded grid of 360 admissible $(b,c)$ pairs it checks each formula, each parent's separate residual edge sum, the explicit B-avoiding colouring of the *forced equality star host*, and the exact surplus split (345 strict surplus, 15 zero surplus). For a smaller grid it exhausts **271,548** red-arm colouring classes of the canonical joint upper hosts, independently checking both residual arrowing relations, and **233,018** arm colouring classes of the forced lower host for the first residual relation. These finite star-host checks corroborate the upper and equality-colouring steps; the unrestricted-host lower bound is **the paper rigidity lemma**, not finite graph enumeration.

The new theorem inherits the UNDER_REVIEW mathematical status of its source-locked single-matching rigidity lemma. Its original $b=3$ corollary additionally depends on the separately protected nine-cubic-vertex lemma. No complete Lean formalization, independent referee attestation, MATHCERT certificate, or unrestricted Erdős #561 proof is claimed. The open general $s,t\ge3$ joint residual issue #3490 remains **OPEN/PARTIAL**.

**Next genuine research boundary:** lift the single-matching equality rigidity argument to a host with *two or more* edges above the first-residual minimum, such as original $n=(2,1,1)$ against $m=(b,c,c,c,c)$, where the joint antidiagonal switching gap can exceed one. This is an actual arbitrary-host structural obstruction, not an invitation to repeat a solved 14-edge census.
