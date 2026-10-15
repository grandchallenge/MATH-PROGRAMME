RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0896-S01
PROBLEM_ID: 896
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For each N>=1 and A,B subsets of {1,...,N}, F(A,B)=number of DISTINCT m such that EXACTLY ONE ORDERED ROLE-RESPECTING pair (a,b)∈A×B satisfies ab=m; A,B need not equal, and swapped factors may count twice when both pairs admissible. Find asymptotic order of max_{A,B}F(A,B). It is NOT count of all pairs, nor multiplicity of generic unrestricted multiplication table, nor an unordered factorization problem. Maintained https://www.erdosproblems.com/896 (May 2, 2026) SOLVED order of magnitude N²/((log N)^delta(loglog N)^(3/2)), delta=1−(1+loglog2)/log2≈0.086071, not an exact leading constant.

## Dated status and primary evidence
Original Erdős source reference [Er72,p81] at maintained problem; original page/full 1972 work not independently recovered/visually inspected, so historical notation source lock remains partial. Kevin Ford, 'The distribution of integers with a divisor in a given interval', Annals of Mathematics 168 (2008), pp367–433 DOI10.4007/annals.2008.168.367, primary publisher https://annals.math.princeton.edu/2008/168-2/p01, proves sharp multiplication-table size O(N²/((log N)^delta(loglog N)^(3/2))), upper for every F. Ford, 'Integers with a divisor in (y,2y]', 2008 CRM Proceedings 46 pp65–80, https://arxiv.org/abs/math/0607473, provides a simplified proof of the multiplication-table order. Maintained catalogue lower MATCHING ORDER attributed to GPT-5.5 Pro prompted by Przemek Chojecki, posted Apr26 2026 https://www.erdosproblems.com/forum/thread/896, reviewed publicly but not independently reconstructed in GCL. Historical frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 SOLVED. Maintained page edited May2 2026, not silently substituted into frozen source. No protected GCL provider FC-896 statement; modern catalogue says formalised No.

## Strongest verified interface
Elementary construction: let P={primes p:N/2<p<=N}, A=[1,N]\P, B=P. Since each p>N/2 has no other multiple <=N, every a∈A has no prime factor in P. If ap=a'p' for a,a'∈A and p,p'∈P, the product has a unique prime factor lying in P, so p=p',a=a'. Thus every one of |A||B|=(N−|P|)|P| ordered pairs has a distinct product and F(A,B)=(N−|P|)|P|, of elementary order ~N²/log N by prime distribution. This is WEAKER than Ford/Chojecki sharp order and not its proof. CHAD exact finite_896_897.py/json enumerates ALL 4^N A,B choices for 1<=N<=8, exact optima F=1,2,4,7,10,13,18,22, stores maximizing witnesses and counts multiplication-table distinct products. Independently checks every construction product unique for N=8,12,24,40,80. All tests exact integer arithmetic; no GCL independent proof of matching analytic lower bound.

## Proposed bounded successor task
Formalize ordered multiplication fiber r_{A,B}(m)=#{(a,b)∈A×B:ab=m} and F=#{m:r=1}; prove P> N/2 uniqueness lemma for A complement of P, B=P. Acceptance complete paper proof or pinned no-sorry Lean with literal axiom report, exact exhaustive F maxima for N<=8 and witnesses; falsify by two distinct allowed factor pairs for same product in claimed unique family or mismatch in exhaustive maximum. Separate high-value source task: independently replay Chojecki/GPT-5.5 Pro lower-bound proof, audit Mertens/Ford hypotheses and constants and source attribution; stop before claiming sharp lower asymptotics GCL-certified or leading constant.

## Prerequisites and blocker
1972 Erdős original p81 not directly seen, full April2026 lower-bound note and analytic estimates not line-by-line independently audited; no protected formal provider or proof, no independent GCL mathematical adjudication. Existing source status SOLVED only to order of magnitude.

## Reuse and claim boundary
Uses 2008 Ford primary published upper theorem and maintained public 2026 lower claim, plus elementary uniqueness construction and independent exact finite exhaustive verifier. Does not claim novel sharp asymptotic, Lean check, protected review/merge, public MathJax browser certification or V2 admission.
