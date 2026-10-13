# Erdős #41: density-preserving E3-to-H3 reduction

**Status:** mathematical reduction with source-locked Lean certificates and a separate elementary asymptotic proof. This note does not resolve the M3 density conjecture.

## Three conventions

For an infinite set of positive integers, define E3 as uniqueness of sums of exactly three distinct entries; H3 as uniqueness of sums of at most three distinct entries, including comparisons across different lengths; and M3 as uniqueness of exactly three summands counted with multiplicity. Historical Er80 uses H3. Modern Helm/maintained Formal Conjectures uses M3. The old frozen Finset E3 formulation was corrected upstream on 2026-09-01, as documented in the source-fidelity audit.

Let D(A) mean the normalized count has vanishing lower limit:

$$
D(A):\quad\liminf_{N\to\infty}\frac{|A\cap[1,N]|}{N^{1/3}}=0.
$$

Define P_E as the universal statement E3(A) implies D(A) for every infinite A, and likewise P_H and P_M.

## The E3-to-H3 affine reduction

**Theorem 1.** If A is infinite and satisfies E3, then its affine image

$$
B=4A+1=\{4a+1:a\in A\}
$$

is infinite and satisfies H3.

**Proof.** Any collision between distinct two-element subsets of A can be padded with a common element of A outside the union of those subsets, which exists because A is infinite. This gives an E3 collision, a contradiction. Therefore uniqueness of two-element subset sums follows from E3 on any infinite carrier. Uniqueness of singleton sums is automatic, and cardinality zero has just the empty subset. We conclude that A has unique distinct-subset sums at each *fixed cardinality* up to three.

The map f(a)=4a+1 is injective. For any finite subset I of A with cardinality k, the sum over f(I) is exactly

$$
\sum_{a\in I}(4a+1)=4\sum_{a\in I}a+k.
$$

Suppose subsets of B of sizes k and l, each at most three, have equal sums. The equality modulo four forces k=l, since k and l lie between zero and three. Cancelling the equal cardinality terms then gives equal original subset sums in A. Fixed-cardinality uniqueness proves the original subsets, and therefore their images in B, are identical. This proves H3 for B. **The assumption that A is infinite is essential for the padding argument.**

## Density conclusion is preserved and reflected

**Theorem 2.** For any infinite A, D(4A+1) holds if and only if D(A) holds.

**Proof.** Enumerate A in increasing order as a_1,a_2,... and B likewise as b_k=4a_k+1. The elementary counting/growth equivalence (proved in the previous source-fidelity note) gives

$$
D(A)\iff\limsup_{k\to\infty}\frac{a_k}{k^3}=\infty.
$$

Since

$$
\frac{b_k}{k^3}=4\frac{a_k}{k^3}+\frac1{k^3},
$$

unbounded limsup is equivalent for the two sequences. Hence D(B) if and only if D(A).

The exact quantifier-level cubic growth equivalence is also checked in Lean: the auxiliary predicate says that for every positive integer threshold and every tail cutoff there exists a later index whose term exceeds the threshold times a cubic index factor. The coding map preserves and reflects it.

## Universal conjecture implication diagram

**Corollary.** The hypotheses are not equivalent on infinite sets, but the universal density conjectures obey

$$
P_H\ \Longleftrightarrow\ P_E\ \Longrightarrow\ P_M.
$$

For the forward inference from P_H to P_E, apply Theorem 1 and Theorem 2. Conversely H3 implies E3, so P_E implies P_H. Finally M3 implies E3 for every A, so P_E implies P_M. No reverse implication from P_M has been established. Neither P_H nor P_E has been proved true; this is a reduction of statements, not a solution.

## Verification boundary

The Lean kernel checks (i) padding a two-subset collision to a three-subset collision on an infinite set, (ii) the sum-coding identity and encoded at-most-three uniqueness using E3, and (iii) affine invariance of the cubic-growth quantified condition, when their respective file compiler receipts are GREEN. The proof that encoded finite source subsets correspond bijectively to subsets of 4A+1, and the counting-function equivalence of D with cubic growth, are included as elementary written arguments. Do not claim a single end-to-end Lean proof of D or of a universal conjecture.

Source target: current repeated-summand M3 problem at https://www.erdosproblems.com/41, with archival source comparisons at research/erdos-41-critique/INFINITE_FIDELITY.md.
