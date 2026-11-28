RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0457-S01
PROBLEM_ID: 457
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Set K=floor(log n), P(n,K)=product of n+i for 1<=i<=K, and q(n,K)=least prime not dividing P. The 1980 Erdős–Graham question asks if some epsilon>0 yields q(n,K)>(2+epsilon)log n infinitely often. SOURCE-DIRECTION EXCEPTION: Erdős's 1979 question instead asks if q(n,K)<(2+epsilon)log n for all sufficiently large n and every epsilon>0. The directions must not be conflated.

## Dated status and primary evidence
Read 2026-10-13: P. Erdős, "Some unconventional problems in number theory," Acta Math. Acad. Sci. Hungar. 33 (1979), printed p.78, https://users.renyi.hu/~p_erdos/1979-23.pdf (SHA256 a4703a104adcbbde0ed605c9ff81379adee8b7ceda3714ea455b5b68ae720dfd), asks eventual UPPER bound. P. Erdős and R. Graham, Old and New Problems and Results in Combinatorial Number Theory (1980), printed p.91, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf (SHA256 0cbf0c32f0ab1e1c71db5121a88bac905bf976c4a6ab6bb6d7d9cf9ddd184ed3), asks infinitely-often LOWER bound. The #457 tracker, last edited 2026-03-07, reports PROVED (LEAN). External Woett/Barreto/Aristotle Lean proof, https://github.com/Woett/Lean-files/blob/main/ErdosProblem457.lean, Git blob b59f01bd433dec13db88aa7734ab5179e7f3ff36, has thm_main at line 202 and erdos_457 at line 327, no active sorry, declares Lean 4.24.0 and mathlib f897ebcf72cd16f89ab4577d0c826cd14afaafc7. GCL has NOT compiled it. The pinned Google DeepMind formal provider at 85f863718beeec7b58a3a1926ee92e3472bc2020, FormalConjectures/ErdosProblems/457.lean, blob 98c6285e67ddb9c0f2eaf7d47cf0624489e44f1c, retains sorry declarations; it is not itself a completed proof.

## Strongest verified interface
Source-derived construction checked stepwise: for large m, A=binomial(2m,m), Q={primes p:2m<p<=3m}. Each p in Q divides binomial(3m,m), hence |Q| log(2m)<=3m log 2. Simultaneous pigeonhole approximation gives 1<=k<=6^|Q| and integers l_p with |kA-l_p*p|<p/6. Let c=floor(3m/5), n=kA-c. Then 1.2m<=log n<=m log 4+O(m/log m), and 2.1 log n<3m eventually. For p<=m the block of floor(log n) consecutive integers contains a multiple of p. For m<p<=2m, p divides A and thus n+c. For 2m<p<=3m, p divides n+i for i=c-(kA-l_p*p), and 1<=i<=floor(log n). Consequently q(n,floor(log n))>2.1 log n for arbitrarily large n. Independent exact spot checks: (n,K,q)=(32,3,13), (113729,11,59). These finite checks are not proof of infinitude. The external main Lean statement matches the 1980 product/floor convention; its provider's auxiliary q-variant uses a non-strict cutoff and is an unproved placeholder.

## Proposed bounded successor task
Use the exact two original pages and external Lean blob. Rebuild under the declared Lean/mathlib toolchain in an isolated runner; capture exit status, hashes, time, #print axioms, and deterministic replay. Check the quantified 1980 statement against the 1979 opposite direction. Acceptance: successful build, no proof holes/unexpected axioms, correct semantic comparison, replay. Falsification: compile or semantic mismatch. Stop after one build and one replay or record an exact dependency blocker.

## Prerequisites and blocker
SOURCE_LOCK_READY only for a qualified documentary article on the 1980 direction, with mandatory 1979-versus-1980 semantic exception and external-Lean-not-recompiled warning. The separate stronger upper-bound question #1181 remains OPEN. The Tao asymptotic and arbitrary fixed constants were not independently reconstructed here. No GCL mathematical certificate.

## Reuse and claim boundary
Reused registry blob 90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5, the two original texts, public formal source, and dated tracker. Independently checked the elementary 2.1 argument and two finite examples. No sibling returns, protected admission, MathCert, or novelty claimed.
