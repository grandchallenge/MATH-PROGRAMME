RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0875-S01
PROBLEM_ID: 875
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let A={a_1<a_2<...} be infinite and admissible: the sets of sums of r DISTINCT members of A are disjoint for distinct r. Determine which real c permit a_{n+1}-a_n<=n^c, with all-index versus eventual pointwise quantifiers preserved. This is stronger than requiring polynomial density or a_n+1/a_n ->1. Distinct elements on both sides are essential.

## Dated status and primary evidence
Erdős, Nicolas and Sárközy, 'Sommes de sous-ensembles', Journal de Théorie des Nombres de Bordeaux 3(1), 1991, pp.55–72, Theorem 2 on printed p.65, https://www.numdam.org/article/JTNB_1991__3_1_55_0.pdf, DIRECTLY INSPECTED p.65: construction of an infinite admissible set with counting function A(x)>>x^(5-2sqrt6). Deshouillers–Freiman, 'On an Additive Problem of Erdős and Straus, 2', Astérisque 258 (1999), Theorem 1, printed p.142, https://www.numdam.org/item/AST_1999__258__141_0.pdf: for large N, |A intersect [1,N]|<=sqrt(4N+1)-1. Pinned teorth catalogue at commit 536408716724a2402bdfa7c1d764bf83d64a8c89 marked OPEN (2025-08-31). Maintained https://www.erdosproblems.com/875 remains OPEN. Lech Mazur's May 2026 forum post reports infinite admissible A with gaps o(n^(3+2sqrt2)) and a Lean formalization later updated for an all-index bound; https://www.erdosproblems.com/forum/thread/875. The July 2026 working report https://www.erdosproblemaday.com/report/875 asserts a barrier for its chosen carry-block framework, NOT a universal lower bound. Neither claimed 2026 Lean proof nor universal asymptotic optimality independently checked.

## Strongest verified interface
Applying 1999 finite upper bound to first n members shows a_n>=(1/4-o(1))*n^2. If eventually every gap g_n=a_{n+1}-a_n<=(1/2-epsilon)n, summation implies a_n<=(1/4-epsilon/2+o(1))*n^2, contradiction. Thus limsup g_n/n>=1/2 and an eventually valid g_n<=n^c is impossible for c<1; the endpoint c=1 is NOT settled. The 1991 Theorem 2 gives a separate established infinite counting lower bound with exponent 5-2sqrt6, not a bound on every individual gap. Finite_875_876.py/json exact checks: 1942 terminal-interval cases, 36 formula cases, exhaustive/DP agreement for N=8,10,12,14 and six extended DP values N=16,18,20,24,30,36. No infinite proof from finite computations.

## Proposed bounded successor task
Inputs: exact May 2026 carry-block construction, explicit stage invariants, original admissibility predicate, toolchain+dependency hash from claimed Lean formalization. Target: prove all stages and their union are admissible, and separately check the eventual little-o gap theorem and the stronger all-index bound. Method: reconstruct stage separation inequalities and independently compile a pinned Lean theorem with literal axiom report. Acceptance: kernel-verified statement without custom axioms/placeholders, original source alignment, finite first-stage regression; falsify via two distinct-cardinality subsets with equal sum or a pointwise gap exceeding its claimed bound. STOP at construction-specific theorem; universal optimality requires an independent all-sequences obstruction.

## Prerequisites and blocker
Original 1998 Erdős problem chapter not directly inspected for quantifier wording; maintained formulation used pending source lock. Claimed external Lean proof not independently replayed; the July framework barrier is not a theorem about all admissible sequences. No protected Formal Conjectures provider theorem admitted.

## Reuse and claim boundary
Primary 1991 and 1999 papers visually checked; an elementary asymptotic gap obstruction derived; finite fixture replayed on CHAD. No priority claim, full mathematical solution, independent Lean certification, protected review, public MathJax check or editorial admission.
