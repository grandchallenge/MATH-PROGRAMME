# Erdős #249 WP07-B — independent-source-aware adversarial logical review

**Review role:** GCL non-authoring logical Adversary/Referee pass by the **same** authenticated agent as author. This is neither separately authenticated, independently human-reviewed, Lean-formalized, nor MATHCERT-certified.  
**Parent scientific workstream:** [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500), which remains OPEN for a positive totient-specific cofinal Fourier/residue estimate.  
**Exact manuscript SHA-256:** 8fef87759b231d2172463a66315c69d8add1abe1837063c3ddd43fef7161a1a8.  
**Exact module SHA-256:** e6cac7124cb5246282c333db6a7b460b68f9787531f75997aef459b6e533e681.  
**Extended governed hostile tests SHA-256:** ea48d72304e7b512ad6558d26a00e47f93b50d8f0d1d6022357893f7d1275033.  
**Exact source-head execution:** c2abeee252ee70646d654de355f7876e5ed9efbb; 19/19 tests PASS; log SHA-256 07672ed2b2673699cdc8d086fd00059d5a76c2f6a74017d44e2aeb54c4f7483c; mathematical Markdown gate PASS.

## A. Could a transition across a modulus doubling invalidate divisibility?

No. The integer $b_n$ is the canonical remainder modulo $M_n$, so $a_n=c_n+2b_{n-1}-b_n$ is divisible by $M_n$ *at every index*, including when $M_n$ doubles. The tests include steps 63→64, 127→128, 255→256, 511→512 and 1023→1024 and check all residues through 12,000. The proof is algebraic, not empirical.

## B. Can the coefficients become negative or exceed $n$?

For $n<64$, $a_n=\lfloor n/2\rfloor$. For $n\ge64$, $M_{n-1}\le M_n\le n/32$, and $0\le b_j<M_j$ yield $c_n-(M_n-1)\le a_n\le c_n+2(M_{n-1}-1)$. Hence $n/4\le a_n\le n$ for $n\ge2$. Both sides were proved for all positive integers and checked independently through a long interval.

## C. Does rationality require eventual periodicity of the coefficients?

No. The exact telescoping identity $\sum_{n\le N}(2b_{n-1}-b_n)2^{-n}=-b_N2^{-N}$ is valid for an arbitrary integer sequence $b$ with $b_0=0$. Here $0\le b_N<M_N\le N/32$ for all $N\ge64$, so the boundary term tends to zero. The original base series is *exactly* $2/3$. Coefficients need not be binary digits, so periodicity of a binary **representation** cannot be conflated with periodicity of arbitrary integer **coefficients**.

## D. Is near-logarithmic depth truly all-position?

Yes. For each $N\ge64$ and $1\le j\le\lfloor\log_2N\rfloor-5$, monotonicity of $M_n$ ensures $M_{N+j}\ge M_N\ge2^j$. The construction forces $M_{N+j}\mid a_{N+j}$, hence each scaled term is an integer. There is no exceptional set or density argument.

## E. Does the positive omitted-tail lower bound confuse size and fractional part?

The positive omitted tail is at least its first term, and $a_n\ge n/4$ yields $\ge4$. Separately, the fractional part follows **exactly** from the rational identity $A=2/3$ and the integral scaled finite prefix: for even $N$, $\{2^N A\}=2/3$; for odd $N$, it is $1/3$. The lower bound and fraction are independent facts. A large positive tail can have a small or zero fractional part in other constructions; no unsupported inference is made here.

## F. Is this a counterexample to the actual full-series conjecture or Cook's criterion?

No. This sequence is **not** Euler's totient. It is a rational control for a bundle of generic properties. It does not satisfy or purport to falsify Cook's specific unproved good-base harmonic savings or cofinal totient residue-distance condition. The positive obligation for the real $\varphi(n)$ remains unmet. The generic dyadic coboundary method has already been used in GCL WP06 and rational negative controls appear in Cook's 2026 record; **novelty is not asserted**.

## G. Is the CI routing and source separation legitimate?

The existing exact governed test route \`tests/test_erdos249_rational_pulse_coboundary.py\` is **extended**, not replaced or excluded. Existing WP06 11 tests and new WP07-B eight tests all ran in the same exact-source fixture (19/19), leaving \`governance/policy_components/erdos249_full_series_phase.json\` untouched. That avoids duplicating a route or triggering all unrelated policy shards. No protected policy is weakened. Separate protected PR and exact-merge readback remain necessary for admission.

**Critical disposition:** ACCEPT_WITH_SCOPE as a bounded, noncertifying mathematical countermodel and exact fixtures; no claim about original irrationality, source originality, independent human mathematical review, or positive Fourier closure. Keep WP07 research issue #3500 and parent #3201 OPEN.
