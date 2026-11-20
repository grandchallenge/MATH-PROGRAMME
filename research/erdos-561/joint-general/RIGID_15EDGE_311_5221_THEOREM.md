# Erdős #561: exact joint residual for (3,1,1) versus (5,2,2,1)

**Research status: restricted paper theorem under mathematical review.** Hosts are arbitrary finite simple graphs. Star-forest embeddings are ordinary and non-induced, with vertex-disjoint target components. The unrestricted Erdős #561 conjecture and general joint-residual hypothesis remain OPEN.

Write $F(a_1,\ldots,a_r)$ for the disjoint union of stars with positive arm counts. The symbol $G\to(R,B)$ means every red/blue edge colouring of $G$ contains a red $R$ or blue $B$.

## Theorem (exact 16-edge joint residual)

For $n=(3,1,1)$ and $m=(5,2,2,1)$, the smallest edge count of a graph satisfying both

- R1: $G\to(F(1,1),F(5,2,2,1))$;
- R2: $G\to(F(3,1,1),F(2,2,1))$

is **16**. The disjoint-star host $F(5,5,3,2,1)$ attains the minimum.

## Lemma (sharp single-matching rigidity)

Let $H$ be a positive-edge star forest with $h$ edges, with a unique maximum-degree vertex of degree $d\ge3$. Suppose an arbitrary simple graph $G$ with exactly $h+d$ edges arrows $(2K_2,H)$. Then $G$ is isomorphic to $H\sqcup K_{1,d}$ up to isolated vertices.

**Proof.** Colour all edges incident to a vertex $x$ red, and everything else blue. The red graph has no two disjoint edges, so $G-x$ must contain $H$. Thus $e(G)-\deg_G(x)\ge h$ for each $x$, giving $\Delta(G)\le d$. All-blue contains $H$, implying $\Delta(G)\ge d$. Therefore $\Delta(G)=d$.

Choose a degree $d$ vertex $v$. The graph $G-v$ has exactly $h$ edges and contains $H$, so it equals $H$ plus isolates. Let $w$ be its unique degree $d$ centre. Because $\Delta(G)=d$, $v,w$ cannot be adjacent. The same reasoning shows $G-w$ equals $H$ plus isolates, where $v$ is the unique degree $d$ centre.

There cannot be a third degree $d$ vertex $z$. It would have to be adjacent to both $v$ and $w$, as neither deleted graph has another degree $d$ centre. But in $G-v$ the vertex $z$ would be a leaf of the star centred at $w$, so its degree in $G$ would be at most two, contradicting $d\ge3$.

If $v,w$ had a common neighbour $z$, colour just $vz,wz$ red. The red edges intersect, so there is no red $2K_2$. Both degree $d$ centres then lose one blue edge, and every other vertex had degree less than $d$ already. Thus the blue graph has maximum degree at most $d-1$, so cannot contain $H$. Contradiction.

Finally, in $G-w=H$ plus isolates, $v$ is the unique degree $d$ centre and all its neighbours are leaves of its star, with no other incident edges in $G-w$. Since they are not adjacent to $w$, they have degree one also in $G$. Hence the entire star centred at $v$ is a disjoint component of $G$, and deleting it leaves $H$ plus isolates. QED.

## Lower bound on all finite simple hosts

Take $H=F(5,2,2,1)$ with $h=10$ and unique maximum degree $d=5$. R1 forces $e(G)\ge h+d=15$. At equality, the lemma forces $G=F(5,5,2,2,1)$ plus isolates.

Colour two arms red and three blue in each five-star; colour the remaining two-stars and one-star entirely red. The red arm counts are $(2,2,2,2,1)$, the blue counts $(3,3,0,0,0)$. Red maximum degree is two, excluding red $F(3,1,1)$. The blue graph has only two components with edges, excluding blue $F(2,2,1)$. Thus this forced 15-edge host fails R2. Every simultaneous host has at least **16** edges.

## Upper bound: an elementary proof

Let $U=F(5,5,3,2,1)$, with 16 edges.

For R1, if the red graph has no two disjoint edges, all red edges of this disjoint-star host belong to a single original component. Delete that component. The four remaining, entirely blue star components always have sorted arm sizes dominating $(5,2,2,1)$, so contain blue $H$. Thus R1 holds.

For R2, let $b_i$ be the blue arm count in each original star, and $r_i=h_i-b_i$ the red count. A blue $F(2,2,1)$ exists whenever two distinct host components have at least two blue arms each and a third has a blue arm. Suppose there is no such blue target.

1. If at most two host components have blue edges, at least three are wholly red. At least one of these has at least three arms, since three of the original components have arm counts at least three. The red graph therefore contains $F(3,1,1)$.
2. Otherwise at least three host components have blue edges, but at most one has at least two blue arms. Thus at least one of the original two five-stars has at least four red arms. Of the other three components originally having at least two arms (the other five-star, the three-star and the two-star), at most one has two or more blue arms; the other two each retain at least one red arm. These give a red $F(3,1,1)$ on three disjoint components.

Every colouring contains a red $F(3,1,1)$ or blue $F(2,2,1)$. Thus R2 also holds and $U$ is a joint host. QED.

## Finite upper-host corroboration

The standard-library script verify_rigid15_311_5221.py checks all possible arm allocations in each host. The upper host has exactly $6\cdot6\cdot4\cdot3\cdot2=864$ allocations, each satisfying both arrowing relations. The forced lower host has $6\cdot6\cdot3\cdot3\cdot2=648$ allocations, all satisfying R1 but nine avoiding R2. Assigning each requested target star injectively to a distinct host component is an exact test because the host is a disjoint union of stars. This arithmetic replay checks the finite part; the unrestricted-host lower bound is the proof above, not a bounded graph search.

The claim remains UNDER_REVIEW, with no Lean/MATHCERT or public certification asserted. The full Erdős #561 conjecture remains OPEN.
