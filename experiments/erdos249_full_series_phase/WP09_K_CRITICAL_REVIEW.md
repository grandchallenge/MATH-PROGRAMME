# WP09-K — logical adversarial review and authority limits

**Primary source identity:** Will Cook, *The Binary Totient Series*, revision 3368d1e69467aec111eb3244843ad3542171ff96, Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac. **Predecessor:** protected WP09-J PR #3651, merge 954795c4a7647f93a856cd5515221cf39df9b1e3. **Research issue:** #3500, OPEN. **Review type:** distinct Axiomatist, Verifier, Adversary, Referee passes staffed by the same agent. These are NOT independently authenticated mathematical refereeing, a Lean proof or MATHCERT.

## Axiomatist: precise mathematical types

The input b is any integer sequence bounded by the index, parity-compatible with Euler's totient, and pointwise within two of it. At a fixed nontrivial correction index n>=3, epsilon(n) is either +2 or -2. The multiplier progression m≡1 mod n guarantees exact coprimality with n. The experimental arithmetic subsets m≡1 mod q use q=lcm(n,2), to force odd multipliers and a stronger true totient-ratio Euler product. P is a multiple of ten and satisfies the explicit cofinal gates including P>=1000qE_P, P>=100(n+1), P>=L+3 and L+2<=nP. L is the actual **least** source-legal h=1 Cook depth for X=nP; Q=2^L.

The new high-order observable is a **LONG PRODUCT OF ORIGINAL COOK FULL PHASES** built through their true full-numerator rolling recurrence. The result is a modulus gap for these phase words of b (if b differs from phi), while for phi the words are identically one. It says nothing unconditional about the distribution of individual E_N for actual phi. The dyadic-rational shadow a8 is covered because WP09-J proved a8(21)=10 vs phi(21)=12 with an exact integer/four-totient tail certificate.

## Verifier: inspect all analytic constants and orientation

1. CRT counts for each fixed q and d with gcd(q,d)=1 give interval length/(qd) with error at most one, and no solutions when gcd(q,d)>1. The Möbius coefficient 1/d makes total counting error <=H_(2P). Completing the Euler product tail costs at most 1/(20q). Thus |F-T C_q|<E_P on the **high** interval of length P/10.
2. Since q is even, C_q>=8/pi^2>4/5. Gate T=P/(10q)>=100E_P gives F>=79T/100. The full high progression count W_B<=T+1<=101T/100; its mean totient ratio is >=79/101>31/40.
3. If H high elements have totient ratio >=7/10, the other ratios are <=7/10 and all are <=1. Therefore F<=7W_B/10+3H/10. The preceding mean lower bound gives H>=W_B/4>=(T-1)/4>=T/5, so |B|>=P/(50q).
4. The low range has |A|>=T-1>=T/2=P/(20q). The full multiplier progression has W<=P/n+1<=2P/n and q<=2n, hence |A|/W>=1/80 and |B|/W>=1/200.
5. The signed exact defect identity is Delta_b=epsilon(nm)-epsilon(n)phi(m)-b(n)epsilon(m). Let s=-epsilon(n)/2. Then s Delta_b=2phi(m)+e_m with |e_m|<=2(n+1). For low u, s Delta(u)<=11P/5+2(n+1); for high v, s Delta(v)>=133P/50-2(n+1). The resulting separation is >=23P/50-4(n+1)>=21P/50>P/3, valid for both signs and adversarial correction placements.
6. For every source m, |Delta_b|<=2phi(m)+2(n+1)<201P/50. Thus |Delta(v)-Delta(u)|<201P/25. Minimal legal depth and L+2<=X guarantee 32X<Q<96X. Hence 1/(288n)<|Delta(v)-Delta(u)|/Q<201/(800n)<1/2, proving **no integer wrap**.
7. Chord inequality 2sin(pi*t)>=4t for 0<=t<=1/2 gives |chi(v)-chi(u)|>1/(72n). Exact phase-variance identity 1-|mean|^2=(1/(2W^2))sum_{i,j}|chi_i-chi_j|^2, restricted to the two ordered cross-pair sets, implies 1-|mean|^2>=1/(80*200*72^2*n^2)=1/(82944000n^2). Divide by 1+|mean|<=2 to get the claimed modulus deficit 1/(165888000n^2).
8. The full Cook numerator recurrence is exact: D_(N+1)=2D_N-Q*(b(N+2)-b(N+1))+(b(N+L+2)-b(N+L+1)). Therefore C_N=E_(N+1)*conj(E_N)^2=e_Q(b(N+L+2)-b(N+L+1)). The oriented product over j from u to v-1 telescopes to e_Q(b(v)-b(u)), also when u>v by inversion.
9. Anchored word W_b(n;m,m0)=T_b(nm0,nm)*T_b(m0,m)^(-b(n)) equals e_Q(Delta_b(n,m)-Delta_b(n,m0)). The anchor is a **single common unit scalar**, so modulus of the average is exactly the modulus of the defect-character average. For phi, all anchored words equal one exactly; for any modified b the modulus gap follows.
10. The explicit n=21 rational-shadow witness transfers without assuming the status of the true binary totient series. The new high-order original-phase word uses O(nP) original Cook factors, not boundedly many. No first-harmonic conclusion is asserted.

## Adversary: hostile interpretations ruled out

- **No one-point Fourier consequence:** The mean of long products need not be controlled by the mean of individual original E_N, or conversely. The shadow a8 has individual late Cook real parts >0.9 while its long words have a nontrivial modulus gap. This is not a contradiction; the products accumulate long-range dependencies.
- **The true phi is the zero-defect baseline:** Its anchored original-Cook words are identically one, so a gap for false shadows has the *opposite* logical direction from a Cook original-phase cancellation proof for phi.
- **No hidden PNT/independence:** The only mean arithmetic input is CRT plus the exact totient Möbius divisor expansion, and the only harmonic inequality is deterministic phase variance.
- **No illicit plus-sign correction:** All universal statements assume coefficient envelope 0<=b(j)<=j. Adversarial finite tests must reject signs that violate this envelope.
- **No extrapolation from a finite test:** Finite sieves check specific P and actual totient-ratio counts. The theorem holds for all sufficiently large P meeting explicit gates because the proof is analytic.
- **No false denominator gate:** Q<96X is true only for **least** legal h=1 Cook depth with L+2<=X. Arbitrarily deeper windows are outside the theorem.
- **No wrong inverse orientation:** The product for v<u is the inverse of the product for u<v; both are independently checked against the signed exact coefficient difference.
- **No manufactured independence:** The character pairs are *deterministic* and can be maximally dependent. Their separated geometric arcs give the variance bound without assuming random phases.
- **No source-name laundering:** The exact products use the genuine D_{1,N,L}, not a simplified local prime surrogate. The result is still only a long word, NOT the original one-point Cook first harmonic.
- **No protected claim before admission:** CI and same-agent review are preliminary to native protected merge-group success and exact-source readback. Keep original #249 and research #3500 open, MATHCERT NOT_SUBMITTED.

## Referee disposition and successor boundary

This is a bona fide effective modulus strengthening of WP09-J and an algebraically exact transfer into long, original-Cook-phase products. It is a bounded research advance, not irrationality or independent mathematical certification. Subject to exact-head tests, Math Markdown renderer gate, native protected merge queue and material identity verification it is eligible for protected research admission.

**Next actual mathematical obligation:** quantitatively control the high-order correlations in the long Cook-phase word well enough to imply a **one-point original full-Cook phase** real first-harmonic bound or Cook's pinned weighted 14X/25 good-set correlation. Without that bridge the original problem remains unresolved.
