RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0862-S01
PROBLEM_ID: 862
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For each N, let A1(N) be the number of inclusion-maximal Sidon subsets of [N]. Maximal means no one new element in [N] can be added while retaining distinct unordered pair sums, including doubled pairs; it does NOT mean maximum cardinality. Erdős/Cameron ask whether A1(N)<2^o(sqrt N) and whether A1(N)>2^(N^c) for some c>0.

## Dated status and primary evidence
Original Erdős, 'Some of My Forgotten Problems in Number Theory' 1992 p.39, equations (15)-(16), https://hrj.episciences.org/125/pdf. Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 (2026-01-21) marks SOLVED (LEAN), not GCL certified. Maintained https://www.erdosproblems.com/862 reports the same and cites Saxton-Thomason. Primary mathematical input: David Saxton and Andrew Thomason, 'Online containers for hypergraphs, with applications to linear equations', JCTB 121 (2016), Theorem 1.10 and Section 5, https://arxiv.org/html/1611.01433. Their theorem counts ALL Sidon sets, not maximal ones; the maximal bound is a separate elementary deduction.

## Strongest verified interface
Every finite Sidon S subset [N] extends to an inclusion-maximal Sidon M by successively adding permitted elements until none remains. For any fixed maximal M, at most 2^|M|<=2^f(N) Sidon subsets belong to it. Thus A(N)<=A1(N)*2^f(N), or A1(N)>=A(N)/2^f(N). By Saxton-Thomason's A(N)>=2^((log_2 sqrt(5)+o(1))*sqrt N) and classical f(N)=(1+o(1))*sqrt N, we get A1(N)>=2^((log_2 sqrt(5/4)+o(1))*sqrt N); the positive exponent is ~0.160964. Hence the first #862 question is FALSE and the second TRUE for any c<1/2 when N is large enough. Source-level external Lean code plby/lean-proofs, src/v4.29.1/ErdosProblems/Erdos862.lean, imports PrimeNumberTheoremAnd.Consequences and references _root_.prime_between. This is not an independently rerun compiled proof or axiom audit.

## Proposed bounded successor task
Input: exact Sidon predicate, finite maximal extension lemma, published #861 lower construction and classical f(N) bound. Formalize A(N)<=A1(N)*2^f(N), including the empty set, finite N=0 and the maximum-vs-maximal distinction. Acceptance: a proof or pinned Lean build without sorry, actual #print axioms output and independent finite cross-check of A(10)=216, f(10)=4, A1(10)=64 and A1(18)=1086. Falsify with a Sidon set not extendible to any maximal Sidon set or a violated finite counting inequality. Stop before asserting an independent proof of Ruzsa/Saxton existence or Lean closure.

## Prerequisites and blocker
Reproduce the external Lean pin, its PNT+ prime-between dependency and literal compile/axiom output. The cited forum's older bare-axiom description does not by itself show the current imported dependency tree. Catalogue's SOLVED (LEAN) status is not protected GCL certification.

## Reuse and claim boundary
Reused the authenticated #861 source audit, independently derived finite covering inequality and pinned external proof provenance. No originality, complete Lean replay, source-status promotion, protected review or editorial admission is claimed.
