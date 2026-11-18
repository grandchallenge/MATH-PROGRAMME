# ERDOS-249-S-WP04 — bounded critical mathematical review

**Date:** 2026-11-18 UTC  
**Review mode:** non-authoring logical adversarial pass by the same authenticated GCL agent/account; not independently authenticated, not an external referee, not MATHCERT certification  
**Reviewed mathematical input:** \`MOBIUS_SIGNED_TAIL_DENOMINATOR_004.md\`, source SHA-256 \`83113072c269ed5a461bf31460d73fab460311d1bdcb1b1cc34828ffcb81f385\`  
**Code SHA-256:** \`51deaab6c42e4b273917afafaa6317435778c2868423d8c49fd1ac58f5afb065\`  
**Test SHA-256:** \`ed44da32670fab8239d96862ba5af06a7e9460bebf510962cf7af7798b05d5a2\`

## Challenge 1: is the leading term really larger than all later weights?

Independently, $a_n/2^{-n}=(1-2^{-n})^{-2}$ is strictly decreasing in $n$. Consequently

$$
\sum_{d>n}a_d
<
(1-2^{-n})^{-2}\sum_{d>n}2^{-d}
=(1-2^{-n})^{-2}2^{-n}=a_n.
$$

This verifies the qualitative strict dominance without reusing the manuscript's geometric-derivative expansion. The stronger quantitative gap requires a separate check: expanding the geometric derivative gives a $k=2$ contribution of exactly $4/(3\cdot4^n)$ and every $k\ge3$ term is positive. No omitted negative term or illegitimate conditional-series rearrangement exists: every absolute $a_d$ is summable.

## Challenge 2: does sign assignment fail at squareful indices?

The index $m$ is explicitly the *first later nonzero Möbius coefficient*; squareful indices between $D$ and $m$ contribute zero. Taking absolute values of all terms after $m$ is the worst-case opposing-sign bound, and dominance defeats it. Examples with $D=3,4,7,8$ force the next nonzero index to skip at least one zero coefficient. The exact code checks this.

## Challenge 3: could a shared Mersenne factor cancel the claimed squared denominator?

For $p>D/2$, no other $1\le d\le D$ is a positive multiple of $p$. With $p$ prime, $\gcd(p,d)=1$ for all other $d$. Hence $\gcd(2^p-1,2^d-1)=1$, including at repeated prime factors of $2^p-1$. After removing the index $p$ term from the sum, the remaining rational denominator is coprime to $2^p-1$ (explicit hostile test). Therefore no cancellation of the $(2^p-1)^2$ denominator is possible at any prime-power valuation. Distinct window primes have coprime Mersenne factors, so their product survives.

## Challenge 4: any false inference about the irrationality of the original series?

**Rejected.** Rational superincreasing comparator $w_n=2^{-n}+4^{-n}$ has the exact rational sum $4/3$, although $w_n>\sum_{d>n}w_d$. Thus sign-controllable tails alone do not imply irrationality. The lower bound on $q_D$ likewise only obstructs a direct small-height rational approximation *using this specific truncation family*. The result does not establish a nonzero distance between $S$ and every rational.

## Challenge 5: external theorem / literature / formalization boundary

The PNT-dependent denominator-growth corollary uses the standard asymptotic sum of primes. Neither its proof nor a Lean theorem is bundled. Related Möbius identity and denominator-isolation ideas are already present in Will Cook's 2026 record; novelty is not asserted. The 2026 Erdős catalogue status remains OPEN. The previously completed lacunary $T$ theorem is not used as a substitute for the full $S$ proof.

## Verdict

**PASS as a bounded, noncertifying mathematical research record** for the specific manuscript claims, subject to fresh affected checks and protected admission. **NOT** a mathematical certification, independent external review, original-series solution, historical priority claim, or permission to close Erdős #249. Next mathematical obligation is a new cofinal separation mechanism, not expanding finite denominator tables.
