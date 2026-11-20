# Erdős #561: complementary rigidity proof for the 311 versus b221 family

**Status: complementary mathematical proof UNDER_REVIEW, not a new claim.** The stronger two-parameter statement is already protected in JOINT_PROFILE_MISMATCH_THEOREM.md, Theorem B, and registered as existing claim ERDOS561-JOINT-PROFILE-MISMATCH-INFINITE-010. This manuscript gives a distinct rigidity-based proof of its a=3 specialization, plus a more general saturation-gap lower-bound lemma and a sharp diagnostic of the parameter threshold. It does not claim priority or constitute an independent certified review. This is a restricted family, not a solution of unrestricted Erdős #561. Every host below is an arbitrary finite simple graph unless explicitly described as a star forest. Copies of forests are ordinary non-induced subgraphs with vertex-disjoint components.

Let $F(a_1,\ldots,a_k)$ be a disjoint union of $k$ positive-edge stars, and write $G\to(R,B)$ when every red-blue colouring of the edges of $G$ contains a red $R$ or a blue $B$.

## Already admitted theorem, with an alternative self-contained proof

For **every integer $b\ge4$**, the minimum number of edges in any finite simple graph satisfying both

- R1: $G\to(F(1,1),F(b,2,2,1))$;
- R2: $G\to(F(3,1,1),F(2,2,1))$

is exactly

$$
\boxed{2b+6}.
$$

An attaining graph is the disjoint-star forest $U_b=F(b,b,3,2,1)$. The result, including $b=4$, was already admitted as a corollary of the more general residual-profile mismatch theorem. The argument below is a complementary proof relying on unique-maximum saturated rigidity rather than residual-profile mismatch. There is **no star-forest restriction** on the lower bound.

For the original red and blue sequences $n=(3,1,1)$ and $m=(b,2,2,1)$, the antidiagonal maximum weights at indices $k=3,\ldots,7$ are exactly

$$
(w_3,w_4,w_5,w_6,w_7)=(b,b,3,2,1)
$$

when $b\ge4$. Explicitly, the first two residual weights equal $\max(b,4)$, while the final three are $3,2,1$. Consequently both first weights are $b$ exactly when $b\ge4$. The unrestricted-host joint minimum equals this canonical star-host upper target in the whole proved family.

## Lower bound: exact saturated rigidity

The previously protected lemma in RIGID_15EDGE_311_5221_THEOREM.md is reusable without change: if a positive-edge star forest $H$ has $h$ edges and a unique vertex of maximum degree $d\ge3$, then any graph $G$ arrowing $(2K_2,H)$ with exactly $h+d$ edges is $H\sqcup K_{1,d}$, up to isolates.

For each $b\ge4$, take $H_b=F(b,2,2,1)$. It has $h=b+5$ edges and a **unique** maximum-degree vertex of degree $d=b$. The standard all-red-star deletion colouring implies every R1 host has at least $h+d=2b+5$ edges. If equality holds, saturated rigidity forces

$$
G=F(b,b,2,2,1)
$$

up to isolates.

Colour **exactly two** arms red in each of the two stars of size $b$, colour all arms in the two 2-stars and the 1-star red, and colour the remaining arms of the stars of size $b$ blue. The red host arm counts are $(2,2,2,2,1)$, so red has maximum degree at most two and contains no $F(3,1,1)$. The blue host arm counts are $(b-2,b-2,0,0,0)$, with edges in **only two** components; blue therefore contains no $F(2,2,1)$, which requires three vertex-disjoint positive stars. The colouring defeats R2, regardless of how large $b$ is.

Thus no graph with at most $2b+5$ edges can satisfy both R1 and R2, and every simultaneous host has at least $2b+6$ edges. The argument works for all finite simple hosts, not just star forests.

## Upper bound: a uniform colour-count argument

Let $U_b=F(b,b,3,2,1)$.

**R1:** If there are two red edges in different original star components, they form a red $F(1,1)$. Otherwise every red edge lies inside one original component. The four other components are entirely blue. Removing *any* one component of $U_b$ leaves four components whose descending arm counts dominate $(b,2,2,1)$ coordinatewise, provided $b\ge4$. Those four blue components contain $F(b,2,2,1)$.

**R2:** Suppose there is no red $F(3,1,1)$. Equivalently for the argument below, we show that absence of blue $F(2,2,1)$ forces a red $F(3,1,1)$. A blue $F(2,2,1)$ is present as soon as at least three original star components are blue-active and at least two of them each have two blue arms.

If **at most two** components are blue-active, at least three are entirely red. Since $U_b$ has three original components with at least three arms (the two stars of size $b$ and the 3-star), at least one completely red component has at least three arms. Choose one red 3-star there and a red edge in each of two other entirely red components: this is $F(3,1,1)$.

If **at least three** components are blue-active but there is no blue $F(2,2,1)$, at most one component can have two or more blue arms. One of the two stars of size $b$ consequently has at most one blue arm, hence at least $b-1\ge3$ red arms. Among the other star of size $b$, the 3-star and the 2-star, at most one has two or more blue arms. The other two each retain at least one red arm. These are three distinct original components, yielding a red $F(3,1,1)$.

So R2 holds as well, establishing the upper bound $2b+6$ and the theorem. QED.

## Stronger reusable lower-bound template

The lower step does not require the exact vector $(b,2,2,1)$. Let $H$ be **any** positive-edge star forest with $h$ edges and a unique degree $d$ maximum centre for $d\ge3$, with *all other component arm counts at most two*. Any graph simultaneously arrowing

- $(2K_2,H)$; and
- $(F(3,1,1),F(2,2,1))$

must have at least $h+d+1$ edges. Indeed the preceding rigidity lemma forces the unique equality host $H\sqcup K_{1,d}$; colour two arms red in the two degree $d$ stars and all lower components red, leaving only the two largest components blue-active. The red graph has maximum degree two and the blue graph lacks three edge-bearing components. This statement requires $d\ge3$ to make the two red-arm choices possible and to invoke rigidity; the unique-maximum assumption is indispensable for this proof.

## Exact mechanism boundary

- **$b=4$:** the result still holds, including the threshold equality $b-1=3$ needed in the upper R2 construction.
- **$b=3$:** the maximum-degree vertex of $H_3=F(3,2,2,1)$ remains unique, and rigidity still gives the genuine general-host lower bound $e(G)\ge12$ for simultaneous hosts. However, the naive 12-edge candidate $F(3,3,3,2,1)$ does **not** arrow R2: red arm counts $(2,2,2,1,0)$ and blue arm counts $(1,1,1,1,1)$ avoid both R2 targets. Also the actual antidiagonal star-host weights change to $(4,4,3,2,1)$, with a **14-edge** canonical star-host upper. Our argument therefore establishes only $12\le J((3,1,1),(3,2,2,1))\le14$; it does NOT determine whether 12 or 13 edges suffice in a nonstar host, and it does not assert a counterexample to the general conjecture.
- **$b=2$:** $F(2,2,2,1)$ has three maximal star centres, so the unique-maximum rigidity hypothesis is false. The specific lower-bound proof cannot be used. This is a structural failure of the method, not a proof that the desired general joint equality fails.

**Distinctness from the protected general argument:** Theorem A of JOINT_PROFILE_MISMATCH_THEOREM.md proves the lower bound by comparing two forced residual forest profiles, and Theorem B covers more general $(a,b)$ parameters. This companion uses only the unique-maximum $(2K_2,H)$ rigidity mechanism, which independently makes the $a=3$ lower obstruction transparent, and gives an extra saturation-gap result for a wider class of $H$. It cannot replace the stronger existing general theorem and must not be entered as a second mathematical claim.

The finite tests in verify_unique_max_311_b221_family.py exhaust all original-star red-arm allocations of both witness hosts for each $4\le b\le14$, independently cross-check a matching-based forest recognizer against sorted-arm dominance for small parameters, and verify the explicit $b=3$ failure. The unbounded claim comes from the argument above, not finite extrapolation. Existing profile-mismatch claim 010 remains UNDER_REVIEW without Lean or public MATHCERT certification; this adds no new claim identifier.
