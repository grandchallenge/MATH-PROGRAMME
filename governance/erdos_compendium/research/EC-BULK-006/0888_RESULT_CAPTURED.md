RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0888-S01
PROBLEM_ID: 888
DISPOSITION: PARTIAL
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For every N>=1, let A subset {1,...,N} be admissible precisely when, for ALL a<=b<=c<=d chosen from A with REPETITIONS ALLOWED, abcd being a perfect square forces ad=bc. Let F(N)=max |A|. The maintained claim F(N)=Theta(N loglog N/log N) is an asymptotic order-of-magnitude statement; it is not an exact finite formula nor a GCL independently certified upper proof. Examples {1,6,10,15} fail since product 900 is square and 1*15 != 6*10; {2,3,4,6} pass although their square product satisfies 2*6=3*4. Repetition is crucial to the correct predicate.

## Dated status and primary evidence
Historical Erdős, Sárközy, Sós question cited as Erdős Eger 1998 p178, original printed p178 not independently image-inspected. Maintained https://www.erdosproblems.com/888 last edited May 28 2026 SOLVED at order-of-magnitude level. Earlier Sárközy o(N) observation with public Tao proof; primes give Omega(N/log N); Stijn Cambie and Desmond Weisenberg show squarefree semiprimes plus primes lower (1+o(1))*N loglog N/log N. Przemek Chojecki publicly reports matching upper O(N loglog N/log N) obtained by GPT-5.5 Pro via decomposition into largest prime factors p<q and edge colors c, forbidding certain two-colored four-cycle configurations plus prime-distribution estimates, https://www.erdosproblems.com/forum/thread/888?order=newest. Public presenter explicitly reports Aristotle attempted Lean formalization INCOMPLETE due Mertens and other analytic dependencies; Google DeepMind main FormalConjectures/ErdosProblems/888.lean theorem still sorry, no GCL kernel/axiom certification. A separate online AI-generated exact formula for ALL N>=15 not independently proved and NOT admitted.

## Strongest verified interface
Elementary squarefree-kernel uniqueness: if distinct x<y in A have same squarefree kernel, xy is a square, so x^3y is a square; repeated quadruple (x,x,x,y) would force xy=x^2, contradiction. Thus any admissible A has at most one element per squarefree kernel. CHAD exact finite_887_888.py/json enumerates forbidden four-member MULTISETS with repeats and exactly optimizes F(N) for N=1..17: values [1,2,3,3,4,5,6,6,6,7,8,8,9,10,10,10,11]; directly validates witnesses under original predicate and lower family of primes and squarefree semiprimes for N10,15,30,60,100,120 with counts [6,10,17,34,55,65]. All distinct-kernel checks x<y<=49 pass, script was executed and JSON reproduced byte-identically. Independent finite values N<=12 previously obtained from a separate offline checker. Exact finite tests and the kernel lemma do NOT establish full asymptotic upper bound, exact formula or new mathematical priority.

## Proposed bounded successor task
Source-lock complete Chojecki/GPT-5.5 Pro upper-bound argument including factorization a=cpq, dyadic prime ranges, colored bipartite four-cycle obstruction, weighted edge-count lemma, every required Mertens and prime-distribution estimate with correct uniform errors. Independently review full proof or compile source-matched pinned no-sorry Lean theorem with literal axiom report before GCL proof certification; any invalid colored rectangle, missed prime-factor range or false Mertens uniformity falsifies. Separate immediate elementary Lean task formalize squarefree-kernel uniqueness WITH repeated inputs, and replay entire finite optimum N<=17 and semiprime construction <=120. Stop before claiming the unrelated exact all-N formula from data.

## Prerequisites and blocker
Full Erdős original 1998 source page unavailable in current page-image audit. GCL has NOT independently audited Chojecki complete reported upper proof or produced kernel-verified Lean. Public reported formalization incomplete. Exact proposed finite formula is a separate unsupported claim. These are review exceptions, not obstacles to producing a carefully bounded editorial article.

## Reuse and claim boundary
Reused maintained original statement and May 2026 reported upper result, explicit lower construction, independently proven kernel lemma, exact CHAD finite data. Authenticated editorial source return does NOT certify the asymptotic proof, protected mathematical review, protected main merge, public MathJax browser or V2 admission.
