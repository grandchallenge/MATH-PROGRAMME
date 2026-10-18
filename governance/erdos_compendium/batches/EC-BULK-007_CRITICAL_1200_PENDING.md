# EC-BULK-007 mandatory independent critical sample #1200: bounded-reciprocal prime residue coverings

**INDEPENDENT NONAUTHOR MATHEMATICAL REVIEW PENDING. This dossier is NOT a solution, an independent approval, Lean certification or a protected editorial admission.**

Catalogue: https://www.erdosproblems.com/1200
Authenticated original research return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2471#issuecomment-6188416229
Primary original evidence: Erdős (1980) p.106, Er80; Erdős–Ruzsa (1980), ErRu80. Related Erdős #688, #783, #784.

## Exact mathematical contract and quantifiers

Does there exist ONE absolute $C<\infty$ so that for each sufficiently large $x$, a family of *distinct primes* $p_i<x$, one chosen congruence $a_i\bmod p_i$ per prime, satisfies $\sum_i1/p_i<C$ while every positive integer $n<x$ lies in **at least one** congruence?

The one-interval covering depends on $x$; neither full periodic coverage of every integer nor arbitrary repeated modulus is permitted. A fixed reciprocal bound ensuring coverage for every $x$ is stronger than a family with positive proportion covered. The opposing ErRu80 sieve question (unavoidable many uncovered integers at bounded reciprocal mass for **all** choices) is logically a potential DISPROOF route and must not be merged into the covering conjecture.

## Exact finite exhaustive evidence

At $x=12$, primes $p<x$ are exactly $2,3,5,7,11$. For each prime choose either no class or exactly one class; 6912 possible assignments. Exact exhaustive enumeration finds 14 assignments covering every positive integer $n=1,\dots,11$. The minimum reciprocal mass among them is $2927/2310$, attained by $(0\bmod2),(0\bmod3),(1\bmod5),(0\bmod7),(5\bmod11)$.

Program: ci/erdos_compendium_007_phase24_checks.py.
Persisted receipt: EC-BULK-007_FINITE_CHECKS_PHASE24.json.

The minimum $2927/2310$ only concerns this **finite** search and does NOT provide a uniform $C$ for arbitrarily large $x$. Coverage of a finite prefix is not coverage of all integers. No conjecture certification is claimed.

## Required independent mathematical critic work

1. Read Er80 p.106 and ErRu80 primary statement with exactly the endpoints, positive $n$ and $p<x$ convention; preserve $C$ uniform in $x$.
2. Independently enumerate the $6912$ assignments, verify $14$ covers, and audit the minimal reciprocal-sum witness using an independent algorithm or exhaustive certificate.
3. Separately reconstruct the ErRu80 positive-proportion divisible-class result and clarify its difference from an all-integers bounded reciprocal-sum cover.
4. Source-check the claimed implication from #688's epsilon lower bound, including all quantifiers; do not borrow a currently unproved implication as a theorem.
5. Independently derive a meaningful growing‑$x$ structural bound or an explicit conditional route; do not extrapolate $x=12$ data.
6. Record specialist nonauthor identity, original source page citations and signed APPROVE/REVISE, including exact scope, before declaring this mandatory deterministic critical sample accepted.

**Critical approval PENDING. Cohort total approved 0/20.**
