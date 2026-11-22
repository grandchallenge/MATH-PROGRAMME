# WP09-G — qualified adversarial mathematical review

**Subject:** TWO_PRIME_COOK_PHASE_DISCRIMINATOR_009G.md, two_prime_phase_discriminator.py, tests/test_erdos249_full_series_phase.py.  
**Source lock:** Will Cook paper/249, Git revision 3368d1e69467aec111eb3244843ad3542171ff96, blob 547ed9ed83500181a2e55047ce5df569b7cb49ac; GCL WP09-F protected commit 7105da0f786623e96d57db08161cebf4e2aecc9d.  
**Review status:** distinct same-agent Axiomatist, Verifier, Adversary, and Referee logical passes only; NOT independent mathematical certification, Lean proof, externally authenticated specialist judgment, or MATHCERT.

## Axiomatist: separate two exact claims

A: An integer, all-even, linear-envelope coefficient sequence has **integer** complete base-two sum, satisfies the **same h=1, p=2 arithmetic source bounds used by WP09-F**, and satisfies every exact one-step and k-step Cook cocycle. Yet for **every** Cook-admissible X,L and **every** h its complete finite phases have real part strictly greater than cos(pi/8) > 0.9. The counterexample refutes amplification from these limited *generic* facts; it does not refute WP09-F's actual totient result or Cook's genuine totient criterion. The hostile does not reproduce full totient Möbius arithmetic, lower envelope, or all-prime information.

B: For **actual Euler totient**, at h=1 and legal depth satisfying an explicit 2x3 source threshold, a two-class difference of the **imaginary actual Cook cocycle** is >= pi X^2/(64 Q). At L=least Cook depth+1, Q is O(X), so the contrast grows linearly. The same contrast for the rational comparator stays absolutely below three. This is a real two-prime discriminator, but is **not** a complete-real-phase ten-percent bound and does not establish all fixed h.

## Verifier: rebuild all rational arithmetic

1. Odd coefficient a(2k+1)=2k contributes 4/9 exactly. Even coefficient a(2k)=2 b_k where b_1=1 and remaining base-four digits repeat 0,1,3, contributes 5/9. Thus full sum=1 exactly and all a(n) are even nonnegative and <=n.
2. Even n has d^a_1(n)>=n-6; odd n has d^a_1(n)<=7-n. For X>=32, each parity source has at least X/3 indices with signed d>=X/2; hence all four specific WP09-F moment/energy inequalities are met (with slack), even after losing the terminal endpoint.
3. Because full sum of a is an integer, each *infinite* shifted-difference tail is an integer, so truncated Cook argument has distance from an integer at most (N+h+L+2)/Q <1/16. This yields every real phase >cos(pi/8)>9/10. The conclusion holds on **every** legal block, not only observed examples.
4. Iterating D_(N+1)-2D_N congruent d_h(N+L+1) modulo Q yields the full k-step identity. An argument that only invokes that identity cannot evade the comparator.

## Verifier: rebuild actual 2x3 arithmetic and phase

5. For each squarefree d split d_0=gcd(d,6) and d_1 coprime to six. A simultaneous residue n mod6 and divisibility n+k mod d is compatible precisely when d_0 divides n+k, then it is one residue mod 6d_1. Exact weighted divisor counting gives W mu_6 g_6(r+k)/6 with error <=5 X E*, no independence or unproved prime distribution.
6. For terminal indices 0 mod6 and 2 mod6, the true local differences g_6(u+1)-g_6(u) are 2/3 and 1/6, respectively. Their contrast is 1/2. The true totient source d_1(n)=n(f(n+1)-f(n))+f(n+1) makes full difference mu_6 W/12 plus error <=20 X E*+2X. The elementary product bound mu_6>3/4, W>=X^2, and X>=1024 E* imply full contrast >=X^2/32. Truncating at N=2X-2 loses at most two terms each <=3X, leaving >=X^2/64.
7. The **genuine** Cook cocycle is e(d_1(N+L+1)/Q). Its imaginary part is sin(2 pi d/Q). For 8(L+2)<=X, |d|<=17X/8 and both relevant classes jointly contain at most 3X/8 indices. Taylor's global remainder |sin t-t|<=|t|^3/6 gives total error less than 5 pi^3 X^4/Q^3. Compared with main term >=pi X^2/(32Q), the ratio is <1/2 for Q>=64X and pi^2<10. Thus actual imaginary contrast >=pi X^2/(64Q).
8. The smallest legal Cook L_1(X) is O(log X); choosing L=L_1(X)+1 eventually meets all explicit conditions with 64X<Q<256X. Therefore the contrast is >= pi X/16384 along all sufficiently late blocks.

## Adversary: challenge scope, source, and tests

- **Generic countermodel versus actual totient:** the countermodel's a(2k) stays <=6, whereas actual phi(2k) has much larger arithmetic complexity and lower bounds. Do not claim to have constructed an actual Euler-totient counterexample. The exact no-go targets ONLY using parity/envelope/h=1 p=2 source moments and cocycle as sole premises.
- **All-shift rationality versus one-shift signed source:** the rational phase bound holds for every h, but signed h=1/p=2 source premises are proved only for h=1. This is sufficient to refute a universal one-shift amplification principle, not an assertion that the comparator matches all WP09-F primes and shifts.
- **Composite modulus six:** the Möbius expansion must use d_0 divisor of 6 and d_1 prime to 6, with the correct density 1/(6 d_1), NOT 1/(6d); double-counting 2,3 factors would falsify the main Euler product.
- **Odd prime independent signal:** conditioning on n≡0 mod6 and 2 mod6 keeps parity fixed and changes divisibility by 3. This is the difference WP09-F h=1,p=2 alone does not detect. The parity comparator's corresponding full-source contrast is only O(X), because matched n=6k and n=6k+2 have d values differing by exactly two.
- **Endpoint loss and number of indices:** source N runs through 2X-2 for cocycle E_(N+1). The full arithmetic sum includes 2X-1; no more than two terms are removed in the two disjoint classes. The union count bound 3X/8 requires X>=48, implied by the stronger explicit gate.
- **Imaginary versus real:** a positive difference of imaginary cocycle sums does **NOT** imply a ten-percent global real original Cook-phase deficit. Both sets of cocycles share all-phase weighting E_(N+1)*conjugate(E_N)^2. No imaginary-to-real rotation is available without fresh weighted-correlation information.
- **Quantifier and scale:** the positive lower applies to h=1 and L meeting (12); the cofinal legal depth is least+1, not necessarily least. Q<256X is only asserted at that particular chosen depth once the stated size threshold holds.
- **Finite experiments:** exact integer source contrasts and exact rational full series are deterministic evidence checks. Floating imaginary phase values and near-zero real mean for actual totient at finite X do not prove cofinal 10% or mathematical certification. No new computational platform or long CPU campaign is required for these bounded smoke tests.
- **Source mathematics formatting:** paired dollar delimiters, renderer-safe macros, source gate. No policy or admission change is proposed.

## Referee: bounded admission and next mathematical obligation

Subject to exact-head CI, native merge queue, material identity, and permanent research issue receipt, the two claims are source-complete as bounded mathematics. MATHCERT NOT_SUBMITTED, original #249 OPEN, issue #3500 OPEN/In Progress; no theorem-priority claim or separate authenticated independent reviewer.

The **next substantive proof target** must connect higher-prime conditional arithmetic to distribution of the **original** exponentially weighted Cook phases, ideally proving a uniform weighted multi-prime characteristic or cofactor-conditional decorrelation bound. WP09-G identifies a discriminating phase observable, but that observable by itself is too weak and of the wrong (imaginary cocycle) type to close Cook's real full-harmonic 10% gate.
