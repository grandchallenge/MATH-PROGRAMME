# Erdős #249 — WP09-M: large-prime localization of the original Cook criterion

Research only; original irrationality OPEN, MATHCERT NOT_SUBMITTED. Issue #3500. Predecessor WP09-L PR #3685, protected merge d21b158f2d3e1d2dd8f1421b6be4143d2c1617ae. Source: Will Cook, The Binary Totient Series, pinned revision 3368d1e69467aec111eb3244843ad3542171ff96, blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section An exponential-sum question. Classical prime number theorem is an external input.

## Theorem A: unconditional population count and conditional localized sufficiency

Fix h≥1, s=26, least source-legal L≥s+h with Q=2^L≥16(2X+h+L+2), t=L-s+1. Let E_N be the original complete Cook phase from WP09-L. For fixed 0<δ<1/2, let H_m consist of starts X≤N<2X with N+t=mp, p prime, 1≤m≤floor(X^δ), also satisfying Cook's A conditions. Put g_m=|H_m|, H=sum g_m, A_m=sum_{N in H_m} E_N and C=sum_{g_m>0}|A_m|²/g_m. No eta-good filter is imposed.

For sufficiently large X all such mp automatically satisfy the A conditions, and the cofactor is unique: p≥(X+t)/m≥X^(1-δ)>2sqrt(X), while m<sqrt(X)/2. The least depth is O(log X) for fixed h, hence t=O(log X). The count is exactly

$$
g_m=\pi((2X-1+t)/m)-\pi((X-1+t)/m).
$$

The ordinary prime number theorem, uniformly on the arguments here because both tend to infinity uniformly and their ratio tends to two uniformly, gives

$$
g_m=(1+o(1))\frac{X}{m\log(X/m)}.
$$

For the sum over m, the function 1/(u log(X/u)) is decreasing on [1,X^δ] for large X; sum-integral difference is O(1/log X). Substitution v=log(u)/log X gives

$$
H/X=\log(1/(1-\delta))+o(1).
$$

No independence of primes or totient values is invoked. For arbitrary unit phases on the block,

$$
\mathrm{Re}\sum_{N=X}^{2X-1} E_N\le X-H+\sqrt{HC}.
$$

This follows by bounding each unselected term by one and applying weighted Cauchy-Schwarz to the selected group sums. At δ=1/5, H/X tends to log(5/4)>1/5, strictly by integrating 1/u on [1,5/4]. If C≤H/4 for each fixed h on arbitrarily large canonical blocks, the complete real sum is eventually below 9X/10. Cook's published criterion then proves irrationality. No group-mean or weighted good-set estimate is needed. This is a sufficient implication only; its cofinal antecedent is OPEN.

More generally C≤ρ²H with fixed 0≤ρ<1 suffices whenever (1-ρ)log(1/(1-δ))>1/10. This is a sufficient tradeoff, not necessary for actual irrationality.

## Theorem B: no short prime-gap estimate is required

For each m the energy expands as a real ordered-pair sum divided by g_m. Fix λ=1/32 and call pairs near when |p-q|≤λ X/m (include diagonal); all others are far. For each eligible p count all primes in [p-λ X/m,p+λ X/m], whose endpoints remain ≥(1-λ)X/m and whose length is exactly 2λ X/m. Uniform PNT on endpoints gives at most (2λ+o(1))g_m eligible near q. The o(1) is uniform in m and p for fixed λ. Thus the near contribution to C, in real part, is at most (1/16+o(1))H. The diagonal alone contributes at most X^δ=o(H). If the real ordered far-pair sum, weighted by 1/g_m, is ≤H/8 on arbitrarily large blocks for each fixed h, then C≤(3/16+o(1))H<H/4. This suffices for Theorem A. No twin-prime or short-gap hypothesis. The far-pair bound itself is OPEN.

## Finite exact actual-phi replay

The registered tests use original WP09-L certified root components and rolling/direct integer Cook numerators, all selected A groups (not the eta-good filter). X=16384, s=26, h=1..8: selected populations 4262 except h=2 (4261), six groups each. Every C/H upper enclosure <3/1000; every exact gate H≥X/5, C≤H/4 and H*C≤(H-X/10)² passes. Exploratory exact replay at protected base 49b7f3afc929ca610bddeda82a8cdbefc5b3adac capture b4516c25f7c34868a2edba88ae73cf77 output SHA256 16ce43fceec3530cad989dd6a68020426a41a9d607b9e551af7e9812797d3315. Decimal values printed there are diagnostics only; comparisons use exact rational bounds.

No finite computation proves the cofinal condition. The unit-phase adversary E_N=1 has C=H for every selected population: the counting theorem cannot imply cancellation. Existing dyadic rational shadows also remain controls. No novelty/priority or independent mathematical certification claim. Next: prove a genuine actual-totient far-prime-pair bound at the growing Cook modulus, or a stronger direct selected-population real bound.
