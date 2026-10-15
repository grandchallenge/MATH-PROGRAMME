RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0894-S01
PROBLEM_ID: 894
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Given any increasing lacunary set A={n_1<n_2<...} of positive integers, with a FIXED eps>0 satisfying n_{j+1}>=(1+eps)*n_j for all j, does there exist a FINITE colouring c:positive integers->{1,...,m}, where m may depend on eps and A, such that for all distinct positive x,y if |x-y| in A then c(x)!=c(y)? Equivalent finite chromatic number for Cayley graph on all Z with difference set A. A finite check or rational rotation for special geometric sequences does not prove the all-lacunary theorem.

## Dated status and primary evidence
Erdős asked in 1987 per Yitzhak Katznelson, 'Chromatic numbers of Cayley graphs on Z and recurrence', Combinatorica 21(2) (2001) pp211–219, DOI https://doi.org/10.1007/s004930100019, publisher/Hebrew University primary abstract inspected on Oct14 2026: states the original Erdős question and recurrence-theoretic solution, with theorem as published. Yuval Peres and Wilhelm Schlag, 'Two Erdős problems on lacunary sequences: Chromatic number and Diophantine approximation', Bulletin of the London Mathematical Society 42(2) (2010), pp295–300, DOI https://doi.org/10.1112/blms/bdp126, original publisher abstract inspected, proves theta circle-separation with delta>=c*eps/log(1/eps) in small-eps regime by Lovasz local lemma, implying chi<=C eps^(-1)log(1/eps), improved from Katznelson C eps^(-2)|log eps| bound, tight up to logarithm. Maintained https://www.erdosproblems.com/894 marks PROVED, linked companion problem #464; frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 PROVED and unformalized. No protected GCL Formal Conjectures source file in pinned provider snapshot. Full 2001 and 2010 proofs not independently re-derived/Lean-built by GCL.

## Strongest verified interface
If a rotation theta has uniform distance ||theta*n_j||>=delta>0 from nearest integer for ALL j, select m positive integer with 1/m<delta and partition unit circle into m half-open equal arcs. Colour integer x by interval containing fractional part theta*x. If x,y same colour, ||theta(x-y)||<1/m<delta, so their difference cannot be in A. This is a complete elementary implication; existence of theta and quantitative delta for arbitrary lacunary A is IMPORTED Katznelson/Peres–Schlag theorem. Independently exact examples: powers of 2 are all nonzero modulo 3 so proper 3-colouring by x mod3 for every integer; powers of 3 odd so parity gives proper 2-colouring. CHAD finite_894_895.py/json tests powers of 2 mod3 and mod5 and powers of 3 mod2 for graph induced on [1,2000], checks complete infinite-modular arithmetic hypotheses, and rational circle-bin lemma on exact Fraction grid. Finite tests are not the universal lacunary theorem.

## Proposed bounded successor task
Given A, theta, delta>0 with ||theta*n_j||>=delta for EVERY j and m integer with 1/m<delta, prove explicit half-open arc colouring is proper for all integers, including negative differences, and is finite with m colours; acceptance complete elementary proof or pinned compiled no-sorry Lean with literal axiom report, rational circle-bin and modulo3/modulo2 regressions, and exact condition on arc endpoints. Falsify by same-colour edge with forbidden difference, endpoint ambiguity or circle wrap-around error. Stop at conditional rotation-to-colouring lemma before any claim to have independently formalized Peres–Schlag local-lemma existence theorem.

## Prerequisites and blocker
Complete 2001 circle-recurrence and 2010 quantitative Diophantine proof not GCL source-proof replayed; publisher abstracts and theorem descriptions source-locked. No protected formal solution, axiom audit, independent mathematical certification or reviewer admission.

## Reuse and claim boundary
Used Katznelson and Peres–Schlag published claims, maintained catalogue, independent conditional lemma, exact modular finite fixture. Original result PROVED, not an open conjecture nor a new GCL theorem. No protected main merge, live deployed MathJax proof, or V2 admission claimed.
