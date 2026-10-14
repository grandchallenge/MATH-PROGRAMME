RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0878-S01
PROBLEM_ID: 878
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Given n with distinct prime divisors p, let f(n)=sum_{p|n} max{p^e:p^e<=n}; let F(n) be the maximal sum of DISTINCT pairwise-coprime positive integers a_i<=n whose prime factors all divide n. The integer 1 is allowed (prime-support empty). Erdős asks separately about typical behavior f=o(n loglog n) and F>>n loglog n, maximal order of running maximum m(x)=max_{n<=x} f(n), running maxima equality m(x)=M(x)=max_{n<=x}F(n), count of equality cases f(n)=F(n), and average H(x)=sum_{n<x}f(n)/n. Original 1984 question (6) asks whether m(x)=M(x) for INFINITELY MANY x; 'for all large x' and 'for all x' were stronger possibilities only.

## Dated status and primary evidence
P. Erdős, 'On Two Unconventional Number Theoretic Functions and on Some Related Problems', Calcutta Mathematical Society Diamond/Platinum Jubilee volume part I (1984), pp113-121, original https://users.renyi.hu/~p_erdos/1984-16.pdf DIRECT visual inspection printed p114 on 2026-10-14. Theorem 3 printed p115: F(n)/n -> infinity off a natural-density-zero set. Theorem 4 printed p116: limsup m(x)/(x log x/loglog x)=1, contrasted explicitly with unproved full limit (5). Question (6), printed p114, asks equality m(x)=M(x) for infinitely many x, with stronger all-large/all-x possibilities. Theorems 6 and 7 pp117-118 give oscillatory averages and H(x)<<x logloglog x. Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 and maintained https://www.erdosproblems.com/878 classify this multipart problem OPEN. Maintained page edited May 12, 2026 incorporating Kevin Barreto's finite x=210 counterexample and a deduction from the mean bound.

## Strongest verified interface
For n=210=2*3*5*7, f(210)=2^7+3^4+5^3+7^2=128+81+125+49=383. But (1,125,128,189) are pairwise coprime; 189=3^3*7, all numbers <=210 with prime support drawn from 210, sum=443. Independently implemented exact support-mask optimizer determines F(210)=443, NOT JUST >=443, and independently checks max_{n<=210}f(n)=383. Thus all-x identity of RUNNING maxima fails at x=210; this does not refute original 1984 infinitely-many-x question or an eventual identity. CHAD fixture finite_878.py/json computes f,F exactly for 1<=n<=250, with separate direct GCD enumeration for n<=25 and validity of each optimal witness. Asymptotic subquestions not settled by finite computations. f<=F for n>1; odd special n=1 needs explicit convention F(1)=1,f(1)=0.

## Proposed bounded successor task
Input: n>=2, distinct prime supports of n, per-support largest candidate <=n, finite optimizer. Target: prove F(n)=1 plus maximum-weight partition of available prime support into disjoint nonempty blocks, weights each maximal permitted integer with precisely the block's prime support. Acceptance: mathematically complete finite proof or no-sorry pinned Lean theorem with literal axiom audit; separately check F(210)=443, max_{n<=210}f(n)=383, direct brute-force results n<=25. Falsify with an admissible coprime family exceeding the partition optimum or a contradiction of direct enumeration. STOP before promoting a finite 210 counterexample to asymptotic resolution or inferring full running-max limit from a limsup.

## Prerequisites and blocker
Primary 1984 analytical proof of Theorems 3,4,6,7 identified and original p114 visually read, but no independent full analytic/Lean replay. Some historical claims (Theorems 8 and 9) were stated without proof in primary text; do not silently treat these as independently certified. The unresolved typical F(n) lower and asymptotic H(x) issues remain OPEN.

## Reuse and claim boundary
Reused primary original 1984 paper, maintained May 2026 catalogue and its posted 210 witness; independently computed exact F(210)=443 and exhaustive n<=250 small arithmetic results. No novel priority, solved-status change, independent formal proof, protected review, admission or public MathJax check claimed.
