# Erdős #561 — two exact 20-edge ORIGINAL 3-by-4 instances

**Research date:** 2026-11-21. **Disposition:** paper-level proof UNDER_REVIEW. This completes TWO fixed original size-Ramsey instances over arbitrary finite simple host graphs. It is not a proof of unrestricted Erdős #561. The upstream new 15-edge joint residual theorem is in \`RIGID_14EDGE_322_3111_THEOREM.md\`. The older universal even-cap splitting theorem is in \`research/erdos-561/even-caps/EVEN_CAP_DEGREE_SPLITTING_THEOREM.md\`.

For a list of positive integers $a=(a_1,\ldots,a_s)$, let $F(a)$ denote the vertex-disjoint union of stars $K_{1,a_i}$. The asymmetric size Ramsey number $\widehat r(R,B)$ is the smallest number of edges of a finite simple graph that arrows $(R,B)$ in every red/blue edge colouring. Star containment is ordinary non-induced subgraph containment.

## Theorem

For both $c=1$ and $c=2$,

$$
\boxed{\widehat r\big(F(3,2,2),F(3,c,1,1)\big)=20.}
$$

The canonical upper host is, in both cases,

$$
H=F(5,4,4,3,2,2),\qquad e(H)=20.
$$

The complete antidiagonal maxima for either original target pair are $(5,4,4,3,2,2)$, and their joint residual antidiagonal tail is $(4,4,3,2,2)$ of size 15.

## Lemma A: monotonic transfer of the sharp residual theorem

Every finite simple graph $Q$ simultaneously arrowing

$$
Q\to(F(2,2),F(3,c,1,1))
$$

and

$$
Q\to(F(3,2,2),F(c,1,1))
$$

has at least 15 edges, for $c=1,2$.

For $c=1$, this is the independently established paper theorem \`RIGID_14EDGE_322_3111_THEOREM.md\`. For $c=2$, every target in the two displayed residual arrowing relations contains the corresponding $c=1$ target as an ordinary vertex-disjoint subgraph: $F(3,2,1,1)$ contains $F(3,1,1,1)$, and $F(2,1,1)$ contains $F(1,1,1)$. Thus a host arrowing the stronger pair also arrows the $c=1$ pair and inherits its 15-edge lower bound. The canonical antidiagonal tail is unchanged, so the bound is sharp for both. This is exactly the previously admitted monotone-plateau principle, not an assumption of the unrestricted conjecture. QED.

## Lemma B: an elementary universal (2,2) edge-degree split

Every finite simple graph $G$ of maximum degree at most four admits an edge partition into red edges of maximum degree at most two and blue edges of maximum degree at most two.

**Proof without invoking an unproved Ramsey claim.** Take two disjoint copies of $G$. For each original vertex $v$, join the two corresponding copies with exactly $4-d_G(v)$ new parallel edges. The resulting loopless multigraph is 4-regular, including possible isolated original vertices (then four parallel rungs are added). Orient every connected component along an Euler tour; each vertex now has indegree two and outdegree two. Replace each oriented edge $u\to v$ by an edge from a left copy $u_L$ to a right copy $v_R$. The resulting bipartite multigraph has degree two at every vertex, so every connected component is an even cycle (allowing a two-edge parallel cycle). Alternate its edges into two perfect matchings. Pulling the two matchings back produces two edge-disjoint directed subgraphs, each with exactly one incoming and one outgoing edge per original multigraph vertex, hence each is 2-regular after directions are forgotten. Finally discard all artificial edges and the entire second copy of $G$. The original edges are now partitioned into two colours of maximum degree at most two. QED.

This is an elementary specialization of the protected GCL even-cap decomposition theorem; no independence or priority claim is made for the classical graph factorization.

## Proof of the original 20-edge lower bound

Fix $c\in\{1,2\}$ and suppose a finite simple graph $G$ arrows

$$
G\to(F(3,2,2),F(3,c,1,1))
$$

with at most 19 edges.

**Vertex-deletion implication.** For every vertex $v$ of $G$, $G-v$ arrows **both** residual relations in Lemma A. To see the red-deleted relation, start with any colouring of $G-v$ avoiding red $F(2,2)$ and blue $F(3,c,1,1)$, and colour all edges incident with $v$ red. Any red $F(3,2,2)$ has three components, at most one of which meets $v$; its other two components necessarily contain two disjoint red two-edge stars in $G-v$. Thus no red full target appears, while the blue target also remains absent. This contradicts original arrowing. The argument for the blue-deleted relation is symmetric: colour all edges incident with $v$ blue, and any blue $F(3,c,1,1)$ would leave the three other components dominating $F(c,1,1)$ in $G-v$, so a purported avoiding colouring cannot extend.

By Lemma A, $e(G-v)\ge15$ for every $v$. Hence

$$
d_G(v)=e(G)-e(G-v)\le19-15=4
$$

for every vertex $v$, i.e. $\Delta(G)\le4$.

Now apply Lemma B. Colour the edges of $G$ red and blue with maximum degree at most two in **each** colour. Neither colour can contain the required three-edge leading star $K_{1,3}$. Hence this colouring has neither a red $F(3,2,2)$ nor a blue $F(3,c,1,1)$, contradicting original arrowing. Thus any original Ramsey host needs at least 20 edges.

## Exact 20-edge upper bound

For $n=(3,2,2)$ and either $m=(3,c,1,1)$, the canonical antidiagonal star-host construction gives precisely the sorted star edge counts $(5,4,4,3,2,2)$. By the elementary greedy star-host Ramsey theorem (proved at \`JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md\`), the 20-edge disjoint-star graph $H$ arrows each original pair. The separate \`verify_original20_322_3111_3211.py\` checks both antidiagonal conventions and **every one of the 5,400 red-arm allocation classes for each original pair**, obtaining no avoiding colouring. This is complete finite upper-host corroboration; the arbitrary-host lower bound is the paper proof above.

We have upper and lower bounds of 20, proving both exact original equalities. QED.

## Claim and governance boundaries

This theorem uses the new paper-level 15-edge joint residual result and a self-contained classical 4-regular factorization. It is not a formal Lean proof, not independent MATHCERT certification, and does not prove the unrestricted Erdős #561 conjecture or all of joint-residual issue #3490. The two original 3-by-4 parameter instances are genuine unrestricted-host conclusions (not a star-host-only experiment). Review and protected source admission must preserve the upstream dependency and UNDER_REVIEW mathematical classification.
