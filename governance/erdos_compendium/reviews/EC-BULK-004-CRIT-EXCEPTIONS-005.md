# EC-BULK-004 — source-critical exception review 005

Date: 2026-10-13. Problem: Erdős #460, original issue #1730. This is the accountable coordinator's mathematical documentary review, **not** independent mathematical certification. Disposition: **LOCAL CONDITIONAL QA WITH SOURCE EXCEPTIONS; NO PROTECTED ADMISSION**.

## Primary statements and semantic boundary

Visually inspected Erdős 1977 printed p.64 (SHA-256 `8fc7f48707af5c2536e792226c9e14505fc05cd46078e0c6e05a00810f8229ea`) and Erdős–Graham 1980 printed p.91 (SHA-256 `0cbf0c32f0ab1e1c71db5121a88bac905bf976c4a6ab6bb6d7d9cf9ddd184ed3`). The 1977 version sets $a_0=0$ and imposes coprimality with $n$; the 1980 version sets $a_0=n$ and checks only earlier positive-index terms. Both originals display an unrestricted reciprocal sum. The maintained tracker adds the necessary $a_i<n$ cutoff, preserving OPEN status. The 1980 $n=2$ greedy construction is degenerate and is excluded from the stated finite fixtures.

## Critical correction to external theorem proof

Inspected the nine-page January 2026 Chojecki note, `erdos-460-v2.pdf`, downloaded 2026-10-13 (SHA-256 `266a1262096cb5a3a08a568466b6c2022fb34fea514942576e52678ff3b3754e`). Its Theorem 8 proof on printed p.4 restricts $a$ to $[N^{1/3},N^{1/2}]$ and asserts that the sum of $1/(a\log a)$ there grows as $\log\log N$. Direct integration gives $\log(3/2)+o(1)$. The displayed proof therefore does **not** establish its claimed $\gg\log\log N$ mean growth. This is a defect in that proof, not a disproof of the theorem. The external note does not claim the pointwise truncated conjecture.

A rigorous weaker proof uses $A=\lfloor\sqrt{\log N}\rfloor$, inclusion-exclusion $\Phi(N-a,a)=(N-a)\prod_{p\leq a}(1-1/p)+O(2^{\pi(a)})$, and Mertens's product bound. For $3\leq a\leq A$, $2^{\pi(a)}\leq2^A=N^{o(1)}$, giving $\Phi(N-a,a)\gg N/\log a$ uniformly. Thus the mean of the forced-rough sum is $\gg\sum_{3\leq a\leq A}1/(a\log a)\gg\log\log\log N$. This establishes unbounded limsup but NOT pointwise divergence. Any stronger mean claim requires a separate uniform-sieve audit.

## Finite verification and hashes

`tests/test_erdos_compendium_0460_greedy.py` passed four tests: 496 inclusion checks for the two variants over $3\leq n\leq250$, six exact small-case lists, weighted lower-bound checks, and the corrected logarithmic integral. The staged issue return `batches/EC-BULK-004_0460_UNPOSTED_RESULT.md` has SHA-256 `52eb596c29abfbde0c1058d2dfb36f500178d7bcbd93ef8530c085724870904a`. The six-section manuscript `editorial/0460.md` has raw SHA-256 `56379a541e33ba9c6545bba2fdb41934f541f76b76a3325bcdcef78bb2588870`. Both are local only. The issue return remains UNPOSTED; no authenticated worker return is invented.

## Remaining obligation

Post exactly one deduplicated authenticated RESULT/1 on #1730 and read back the real comment ID before any source-clearance promotion. Repair or bound the external mean theorem with explicit uniformity, preserving the unresolved pointwise question. Strict MkDocs and all publication-gate tests must pass before protected batch admission; this review does not confer MathCert or independent referee approval.
