# Erdős #561 — monotone antidiagonal plateaus

**Research status:** The transfer theorem below is unconditional. Its concrete exact values rely on existing paper-level GCL proofs still marked UNDER_REVIEW. The unrestricted joint-residual conjecture (issue #3490) remains OPEN/PARTIAL.

## Definitions

For a positive nonincreasing sequence n, let F(n) be the disjoint union of stars with the given edge counts. Define H(n,m) as the minimum e(G) for a finite simple graph G that simultaneously arrows

\[
G\longrightarrow(F(n_2,\ldots,n_s),F(m)),\qquad
G\longrightarrow(F(n),F(m_2,\ldots,m_t)).
\]

All subgraph embeddings are ordinary (not induced) and distinct star components must be vertex-disjoint. Let

\[
J(n,m)=\sum_{k=3}^{s+t}\max_{i+j=k}(n_i+m_j-1).
\]

The canonical disjoint-star construction provides H(n,m) <= J(n,m), independently of the conjecture for arbitrary hosts.

## Theorem 1 — monotone plateau transfer

Suppose n <= N and m <= M coordinatewise, with matching sequence lengths. Then

\[
H(N,M)\ge H(n,m),\qquad J(N,M)\ge J(n,m).
\]

If the smaller pair has a proved exact value H(n,m)=J(n,m), and the stronger pair has the **same antidiagonal sum** J(N,M)=J(n,m), then

\[
\boxed{H(N,M)=J(N,M).}
\]

**Proof.** Every copy of a larger star forest contains the corresponding smaller star forest: delete surplus arms at each distinct component centre. Therefore a graph simultaneously arrowing the two larger residual pairs also arrows the smaller residual pairs, and its edge count is at least H(n,m). Every antidiagonal maximum is monotone in the component sizes. Hence

\[
J(N,M)\ge H(N,M)\ge H(n,m)=J(n,m)=J(N,M).
\]

Equality follows. No assumption of the full joint-residual conjecture is used. QED.

**Operational implication:** Before dispatching a new proof or full graph enumeration, close all coordinatewise stronger target pairs for which J remains unchanged. This is a mathematical deduction, not an additional review gate.

## Corollary 2 — the formerly queued 15-edge benchmark and four adjacent cases

Fix n=(3,2,1), and let m=(4,c,d,1), with

\[
1\le d\le\min(c,2),\qquad 1\le c\le3.
\]

Each antidiagonal tail is exactly (5,4,3,2,1), so J=15. These are the five cases m=(4,1,1,1), (4,2,1,1), (4,2,2,1), (4,3,1,1), (4,3,2,1).

The base n=(3,2,1),m=(4,1,1,1) has exact H=15 from the existing paper RIGID_14EDGE_FINITE_THEOREM.md, claim ERDOS561-JOINT-RIGID-3X4-007. Every listed stronger pair dominates it componentwise and has unchanged J. Thus **all five have exact H=15 over arbitrary finite simple host graphs**. The previously queued (3,2,1) versus (4,2,1,1) requires NO additional full graph search.

## Corollary 3 — another inherited 13-edge case

The base n=(3,2,1), m=(3,1,1,1) has exact H=13 in RIGID_12EDGE_FINITE_THEOREM.md. For m=(3,2,1,1), the antidiagonal tail remains (4,3,3,2,1). Therefore

\[
H((3,2,1),(3,2,1,1))=13.
\]

## Corollary 4 — a new infinite family

For every integer a>=4, the previously established exact family n=(a,2,1), m=(a,1,1,1) has H=3a+4 (RIGID_15EDGE_THEOREM.md; claim ERDOS561-JOINT-EQUAL-LEAD-INFINITE-008). Strengthen the second blue star from one to two edges. The antidiagonal tail still equals (a+1,a,a,2,1). Theorem 1 proves

\[
\boxed{H((a,2,1),(a,2,1,1))=3a+4\quad(a\ge4).}
\]

## Corollary 5 — a second new infinite family

The already admitted exact family n=(3,1,1), m=(b,2,2,1), b>=4, has H=2b+6 (JOINT_PROFILE_MISMATCH_THEOREM.md, the sharp two-parameter theorem with a=3; claim ERDOS561-JOINT-PROFILE-MISMATCH-INFINITE-010).

For every b>=5 the stronger m=(b,3,2,1) has the same antidiagonal tail (b,b,3,2,1). Therefore

\[
\boxed{H((3,1,1),(b,3,2,1))=2b+6\quad(b\ge5).}
\]

The b=4 instance is **not** covered by this transfer because its J increases to 15.

## Exact validation and next research target

The source-only verifier verify_joint_monotone_plateaus.py independently evaluates J by two distinct index conventions and checks both finite plateau classifications and these two infinite-formula families at bounded integer values. MONOTONE_PLATEAU_CERTIFICATE.json records the exact derived cases and their parent pairs. The check also inventories nine inherited cases in a bounded 3-by-4 grid (component values 1..6 and J<=19) using selected established parent theorems. It is **not** a declaration that all other cases are mathematically open.

A next candidate not closed by this selected inheritance inventory is n=(3,2,2),m=(3,1,1,1), with proposed J=15, separate residual antidiagonal bounds 14 and 13, and currently available elementary/peeling bound 13. Check other concurrent research before dispatch.

**Claim discipline:** These corollaries inherit the mathematical-review status of the parent paper proofs and do not establish the unrestricted joint-residual hypothesis or the original Erdős #561 conjecture. No independent source-only CI pass should be described as public mathematical certification.