RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0462-S01
PROBLEM_ID: 462
DISPOSITION: PARTIAL
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For $m\ge2$, $p(m)$ is its least prime factor. Erdős–Graham (1980), printed p.92, gives a global composite-only sum but asks about a short-interval sum over **all integers**. The question is whether some fixed $C>0$ gives $\sum_{x\le m\le x+C\sqrt x(\log x)^2}p(m)/m\gg1$ for every large $x$. The stronger composite-only variant must remain distinct.

## Dated status and primary evidence
Visually inspected 2026-10-13: Erdős–Graham (1980), printed p.92, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf; previously recorded PDF SHA256 0cbf0c32f0ab1e1c71db5121a88bac905bf976c4a6ab6bb6d7d9cf9ddd184ed3. Pinned registry blob 90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5, source Git blob 4e60263a80af6207aca494d2e1388e44fa372889, OPEN 2025-08-31. Dated tracker https://www.erdosproblems.com/462 also OPEN. Xu Zhang, arXiv:2608.24930v1, 2026-08-22, downloaded 2026-10-13, PDF SHA256 c9c27d422e799cea510080ac7d5de6a137ea7139f9cd2868e55bef5c3efa2b67.

## Strongest verified interface
The semiprime identity p(pq)/(pq)=1/q for primes p<=q was independently checked.
Numbers with at least three prime factors satisfy $p(m)\le m^{1/3}$. For semiprimes, the exact weighted decomposition is $A_2(X)=\sum_{q\le\sqrt X,\ q\ {\rm prime}}\pi(q)/q+\sum_{\sqrt X<q\le X/2,\ q\ {\rm prime}}\pi(X/q)/q$, up to endpoints. The prime number theorem gives the reported $A(X)\sim8\sqrt X/(\log X)^2$. Sliding-window averaging with $H_X=C\sqrt X(\log X)^2$ yields $X^{-1}\int_X^{2X}W(t)\,dt\ge8C(\sqrt2-1)+o(1)$ for composite-only $W(t)$. This proves arbitrarily large good starting points, not every starting point.

The printed variance proof is not source-cleared.
The precise arithmetic defect: the paper bounds a cross term by $(L^2/X^2)(X/(\log X)^2)$, where $L=C\sqrt X(\log X)^2$, but evaluates it as $C^2(\log X)^2/X$. The correct substitution is $C^2(\log X)^2$, which does not vanish. This does not disprove the variance theorem. Five finite tests pass, including this algebraic check.

## Proposed bounded successor task
EC004-0462-VARIANCE-REPAIR: reconstruct the 2026 paper's covariance calculation with explicit $X$‑powers and prime ranges. Target either a valid vanishing variance estimate or the smallest missing cancellation lemma. Check against the exact printed algebra and finite least-factor fixtures. Reject any derivation that confuses a positive pair-count bound with cancellation of signed covariance. Stop after one bounded audit, recording the unresolved step. An almost-all result, even if repaired, does not prove the original every‑$x$ statement.

## Prerequisites and blocker
PARTIAL. The primary statement is inspected, but the August 2026 second-moment proof has a concrete unresolved arithmetic gap. The external July 2026 finite certificate at https://www.erdosproblemaday.com/report/462 is not replayed. No GCL admitted formal statement, authenticated issue return, protected editorial admission, independent MathCert or full solution.

## Reuse and claim boundary
Reused the original issue #1732, pinned registry, 1980 primary monograph, dated tracker and explicitly attributed 2026 external research. The algebraic correction, semiprime checks and sliding-window mean deduction were performed here without a novelty claim. STAGED AND UNPOSTED pending one authenticated, deduplicated GitHub issue comment with actual comment ID readback. Manuscript: governance/erdos_compendium/editorial/0462.md; tests: tests/test_erdos_compendium_0462_least_factor.py.
