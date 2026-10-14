RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0874-S01
PROBLEM_ID: 874
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For A subset [1,N], restricted r-fold subset sums r^A consist of sums of r pairwise DISTINCT elements. A is admissible iff the restricted sumsets r^A and s^A are disjoint for all distinct possible lengths r,s. Let k(N)=max |A|. Erdős asked whether sufficiently large N attain k(N) at the terminal interval {N-k+1,...,N}. Repetition-allowed sumsets would be a different problem.

## Dated status and primary evidence
Original Erdős 1962 question and Straus 1966 construction are cited in Jean-Marc Deshouillers and Gregory A. Freiman, 'On an Additive Problem of Erdős and Straus, 2', Astérisque 258 (1999), pp.141–148, https://www.numdam.org/item/AST_1999__258__141_0.pdf. DIRECT PRIMARY visual inspection of printed p.142 Theorem 1 (2026-10-14) verified: an effectively computable N0 exists such that for all N>=N0 and admissible A subset [1,N], |A|<=2 sqrt(N+1/4)-1. On the same page Theorem 2 quotes the authors' earlier structural theorem for |A|>1.96 sqrt N; the global upper bound relies on that imported argument. Frozen catalogue teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 says PROVED and unformalized (last update 2025-08-31). Maintained https://www.erdosproblems.com/874 marks the problem solved. No GCL protected Formal Conjectures statement or full independent theorem replay.

## Strongest verified interface
For a terminal interval T=[N-k+1,N] of k integers, its sums of exactly r distinct elements fill the complete integer interval [r(N-k+1)+r(r-1)/2, rN-r(r-1)/2]. Adjacent cardinality intervals are disjoint iff N>=(r+1)(k-r) for every 1<=r<k. Maximizing (r+1)(k-r) gives floor((k+1)^2/4). Thus T is admissible iff (k+1)^2<=4N+1, with maximal terminal length floor(sqrt(4N+1))-1. The 1999 primary upper theorem guarantees this terminal construction globally optimal for sufficiently large N. TWO exact finite maximization methods agree through N=14; incremental search through N=36 agrees with the terminal formula. Reproducible CHAD fixture finite_873_874.py/json, previously source-locked in cohort research, returns all 36 checked maxima. Finite computations do not reprove the 1999 structural theorem.

## Proposed bounded successor task
Input: N,k integers 1<=k<=N and all distinct-summand subset sums for T=[N-k+1,N]. Target: give a fully checked finite interval identity and equivalence T admissible iff (k+1)^2<=4N+1, with all endpoint and floor conventions explicit; separately source-lock the 1995 structural prerequisite used in the 1999 Theorem 1. Method: induction on r for continuous restricted sumsets and quadratic maximization, then a Lean theorem or reviewed paper proof. Acceptance: proof without sorry/custom axioms, independently replayed N<=36 table, exact reference-to-lemma map of Theorems 1–2. Falsify via a finite counterexample to the iff or a proof mismatch for pairwise distinctness. STOP at verified construction lemma unless the imported 1995 structure theorem has been independently established.

## Prerequisites and blocker
The 1999 Theorem 1 is published, visually verified and source-locked; its 1995 structural input and global proof have not been independently replayed or Lean-checked. The original 1962 paper was not directly inspected. No source-equivalent theorem from a protected Formal Conjectures provider is admitted.

## Reuse and claim boundary
Reused the 1999 primary paper, its explicit structural dependency, maintained catalogue and the existing GCL exact finite fixture. Independently derived terminal-interval criterion. This is an authenticated source-audit return, not a novel global theorem, formal certificate, protected review, public MathJax browser check or editorial admission.
