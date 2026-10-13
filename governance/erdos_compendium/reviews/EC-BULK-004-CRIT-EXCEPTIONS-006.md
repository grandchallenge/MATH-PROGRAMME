# EC-BULK-004 — source-critical exception review 006

Date: 2026-10-13. Erdős #461, issue #1731. Accountable editorial coordinator review, **not** independent mathematical certification. Disposition: **LOCAL CONDITIONAL QA WITH HISTORICAL PROOF EXCEPTION; NO PROTECTED ADMISSION**.

## Primary-source statement and semantic drift

The 1980 Erdős–Graham monograph printed p.91 introduces $n+i=a_i b_i$ with prime factors of $a_i$ **strictly below** $t$ and those of $b_i$ at least $t$. Printed p.92 continues the question about $\min_t f(n,t)/t$ and reports $f(n,t)\gg t/\log t$ without a proof there. The modern tracker states the intended uniformity in $n$ and $t$ explicitly. This normalization is documented rather than silently attributed to the original typography. The previously recorded monograph PDF SHA-256 is \`0cbf0c32f0ab1e1c71db5121a88bac905bf976c4a6ab6bb6d7d9cf9ddd184ed3\`. The historical lower-bound proof has NOT been independently inspected; PARTIAL is mandatory.

## Mathematical verification and limitation

Verified the exact collision lemma for smooth components $\ge t$, the construction $n=\operatorname{lcm}(1,\ldots,t)^2$ giving $f(n,t)=t$ for composite $t$ and $t-1$ for prime $t$, and the exact residue-density identity $\Pr(s_t(m)=u)=u^{-1}\prod_{p<t}(1-1/p)$ for $u\le y<t$ over $Q=P_t\operatorname{lcm}(1,\ldots,y)$. Averaging yields $\inf_n f(n,t)\le y+t(1-H_y\prod_{p<t}(1-1/p))$ and, by Mertens with $y=\lfloor t/\log t\rfloor$, the upper obstruction $\limsup_t\inf_n f(n,t)/t\le1-e^{-\gamma}$. This argument is already noted in the public June 2026 discussion; **no novelty** is claimed. The argument does not negate existence of a smaller positive uniform lower bound.

## Adversarial finite checks

Four unittest methods pass: 176 pairs checking noncollision for $s\ge t$, 38 values of $t$ for the $L^2$ identity, a twelve-residue exact density check at $(t,y,Q)=(5,2,12)$, and the forum Hall counterexample $(n,t)=(1407302,38)$ with $f=27$ and five neighbours of six specified divisors. The Hall failure is a warning against using the proposed matching route to assert $f\ge\lfloor t/2\rfloor$; it is not a counterexample to $f\gg t$.

## Hashes, custody and stopping condition

Source return (UNPOSTED) SHA-256: \`67f95a1b5b782e8f6fcebc677e3eb2b131b18d65342126217fdabc5e4e43e565\`. Article raw SHA-256: \`99f55ead8fc4ab4bea76607a6865b62bb215845f8e4297246122a836243fef23\`; normalized SHA-256: \`5d6395bcdeb5784f2e5c68bfbe9788f7d03ff97256348bba4d1bde68c87adad3\`. Test SHA-256: \`09eab440853be2f8c47d5658e8a856d42fe9286a3ba570367811b8f1e48d3c19\`. Preserve the source exception until the historical lower-bound proof is audited. Original issue comment must be authenticated and deduplicated, with real comment ID recorded before source clearance. Do not promote this draft to protected editorial acceptance or MathCert on this review alone.
