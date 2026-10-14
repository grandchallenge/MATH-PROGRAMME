RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0889-S01
PROBLEM_ID: 889
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For n>=1,j>=0, v(n,j) counts DISTINCT prime divisors of n+j that have not divided any of n,...,n+j-1; equivalently v(n,j)=#{primes p|n+j : p>j}. Define v_0(n)=max_{j>=0}v(n,j). Ask whether for every M there exists N such that n>=N implies v_0(n)>=M; extended conjecture v_l(n)=max_{j>=l}v(n,j)->infinity for any fixed l>=0. Do not confuse with original printed V(n,j) counting newly seen PRIME POWERS p^a. A max over all j is exactly reducible to a finite j cutoff for each n but not uniformly in n.

## Dated status and primary evidence
P. Erdős and J. L. Selfridge, 'Some problems on the prime factors of consecutive integers', Illinois Journal of Mathematics 11 (1967), pp428–430, DOI 10.1215/ijm/1256054564, primary archival PDF https://combinatorica.hu/~p_erdos/1967-21.pdf. Its printed p428 theorem states exactly v_0(n)=1 iff n in {1,2,3,4,7,8,16}; n>=17 gives v_0>=2, NOT divergence. Printed p428–429 lists 29 n<2500 for v_1(n)=1, last 330, without proof of finite exception list globally; printed p429 separates V(n,j) prime powers. The full primary PDF was searchable/indexed and citations cross-checked, but its individual page screenshot was not independently captured in this execution. Maintained https://www.erdosproblems.com/889 page updated Jan 2, 2026 remains OPEN, frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 OPEN, no protected solved Lean theorem for divergence. Public FC ErdosProblems/889.lean splits solved seven-exception proposition from several open sorry statements. Jan 2026 forum https://www.erdosproblems.com/forum/thread/889 offers shift inequality and reduction, not full proof.

## Strongest verified interface
If prime p<=j divides n+j then also divides n+j-p (an earlier member); if p>j divides n+j, it divides no earlier number with positive difference <=j. Hence exact equivalence. If j>n then n+j<2j and cannot contain two distinct prime factors >j, so v(n,j)<=1 and v_0(n)=max_{0<=j<=n}v(n,j), with v_1 analogous when n>=1. CHAD exact finite_889_890.py/json computes v_0/v_1 for n=1..2000, independent earlier-primes definition for n<=24, and reproduces all seven exceptions and the complete original list of 29 v_1(n)=1 cases below 2500. Finite testing does NOT establish v_l divergence or finiteness of v_1=1 exceptions.

## Proposed bounded successor task
Prove source-normalized threshold equality for each n,j, and the cutoff j>n implying v(n,j)<=1, using complete elementary proof or independently kernel-compiled pinned no-sorry Lean with literal axiom report; execute exact finite regression n<=2000 with independent direct-new-factor checks. Falsify via prime appearing earlier despite p>j, missed earlier occurrence p<=j, or a j>n with two new distinct prime factors. Stop at finite equivalence; independent source-proof review of 1967 seven-exception theorem and true asymptotic growth are separate work.

## Prerequisites and blocker
Full page-image audit of 1967 PDF not obtained this run; public FC theorem body for open divergence contains sorry, no valid asymptotic conclusion. No independent general l>0 shift reduction replay or protected source-provider formal admission.

## Reuse and claim boundary
Reused 1967 original archived text, maintained catalogue and 2026 discussion, independently derived exact finite cutoff and CHAD fixture. No new solution, priority, full Lean proof, protected review/merge, or live browser admission claimed.
