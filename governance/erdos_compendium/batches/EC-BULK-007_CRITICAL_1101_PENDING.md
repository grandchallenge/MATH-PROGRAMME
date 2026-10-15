# EC-BULK-007 critical sample #1101 — pending infinite-sieve semantics

**Disposition: INDEPENDENT_CRITICAL_REVIEW_PENDING_PRIMARY_SOURCES.** Not a completed critical review.

- Maintained source: https://www.erdosproblems.com/1101
- Authenticated RESULT/1: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2372#issuecomment-6167054489
- Draft: governance/erdos_compendium/editorial/1101.md
- Frozen formal definition: google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020/FormalConjectures/ErdosProblems/1101.lean (both target theorems open and proof placeholders).

The input is increasing pairwise coprime u_i>1, sum 1/u_i<infty, survivor set A={a: all u_i do not divide a}, positive Euler density product delta, t_x from product_{i<=t_x}u_i<=x<product_{i<=t_x+1}u_i. Goodness requires for each fixed epsilon>0 and all sufficiently large x a largest successive survivor gap below x LESS THAN (1+epsilon)*t_x/delta. Erdős reports existence of SOME good prime sequence. Polynomial u_n<n^{O(1)} and subexponential u_n<=exp(o(n)) existence problems remain OPEN and logically distinct.

Finite integer example prime-square prefix 4,9,25,49,121,169 is pairwise coprime; 1..200 sieve leaves 122 survivors and finite Euler product 442368/715715. For x=1000, t_x=3. Neither result proves prime squares give a good infinite sequence; that remains related to an OPEN Erdős problem.

Reviewer obligations: (1) read original Erdős 1981 [Er81h,p.178], compare exact strict inequality and a_k<x boundary convention; (2) verify positivity/convergence of infinite product and exact almost-optimal sieve lower bound under hypotheses; (3) review proof of existence of at least one good prime sequence and check whether polynomial/subexponential rates are excluded by its construction; (4) inspect pinned Lean ASet, A, t, IsGood quantifiers and edge cases and any current revisions; (5) perform independent second-pass review with actual proof-page citations and disposition.

**Still 0/20 completed critical samples** at present. Source certification and protected publication explicitly withheld.
