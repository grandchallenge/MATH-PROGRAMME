RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0475-S01
PROBLEM_ID: 475
DISPOSITION: PARTIAL
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For each prime $p$ and each $A\subseteq\mathbb F_p\setminus\{0\}$ of size $t$, does there exist a permutation $a_1,\ldots,a_t$ of $A$ with pairwise distinct **nonempty** partial sums $s_j=\sum_{i=1}^j a_i$ modulo $p$? Equivalently, no consecutive block $a_{i+1}+\cdots+a_j$ vanishes when $1\le i<j\le t$. The initial $s_0=0$ is NOT included; for the full nonzero set and odd $p$, $s_t=0$, so demanding distinctness from $s_0$ would incorrectly strengthen the question.

## Dated status and primary evidence
Visually inspected Erdős–Graham (1980), *Old and New Problems and Results in Combinatorial Number Theory*, printed p.95, PDF index 90, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf. It attributes the conjecture to Graham (1971). Inspected the primary Pham–Sauermann preprint *On Graham's rearrangement conjecture*, arXiv:2602.15797v1, 17 February 2026, https://arxiv.org/html/2602.15797, Theorem 1.2: for each $0<\alpha<1$, a constant $C_\alpha$ exists so every $A$ with $C_\alpha\le|A|\le p^{1-\alpha}$ has a valid ordering. The authors state that their result combined with complementary range theorems settles the conjecture for all sufficiently large primes. The live tracker https://www.erdosproblems.com/475, last edited 5 March 2026, labels it DECIDABLE, not globally proved for every prime. Pinned registry blob 90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5 maps #475 to issue #1745; source snapshot teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89.

## Strongest verified interface
Theorem 1.2 was inspected as a statement in a primary research manuscript, not independently certified as a 27-page proof. The combined published/preprint range results are reported to leave only finitely many primes. This is NOT an executed finite check or an extracted explicit cutoff $p_0$; distinguish the tracker label DECIDABLE from a demonstrated effective numerical decision procedure. Independent exact backtracking checked all $2^{p-1}$ subsets for each $p\in\{2,3,5,7,11,13\}$, totaling 5206 subsets, finding a valid permutation for every one. A separate brute-permutation oracle agrees for $p\le7$. These are finite results only.

## Proposed bounded successor task
EC004-0475-EFFECTIVE-CUTOFF: inspect and pin the four complementary primary range papers; extract a numerical $p_0$ (or document exactly which constants are ineffective); enumerate primes $p<p_0$ with a bitmask/backtracking witness checker. Save canonical subset-to-order certificates or counterexamples, with the fixed deterministic 20-case independent sample and every exception. Stop at the first missing constant, semantic mismatch, or resource limit; do not claim global resolution from checks through $p=13$.

## Prerequisites and blocker
PARTIAL. The 1980 original statement and 2026 primary theorem were inspected. Other complementary range proofs and an explicit finite cutoff were not independently audited. No global finite-check closure, source-complete proof audit, or MathCert. The authenticated issue-comment return remains UNPOSTED after an execution safety rejection.

## Reuse and claim boundary
Reused pinned registry, issue #1745, primary original scan, Pham–Sauermann v1 and dated tracker. Finite tests independently run. No external worker execution, new theorem, global proof replay, protected admission or mathematical certification claimed.
