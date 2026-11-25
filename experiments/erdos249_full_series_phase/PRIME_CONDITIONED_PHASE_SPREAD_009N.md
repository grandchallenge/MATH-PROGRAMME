# Erdős #249 — WP09-N: unconditional prime-conditioned full-phase spread

Bounded noncertifying research; issue #3500; predecessor WP09-M PR #3721, protected merge 7615a2f18f1aaef3a244d381104432af6c78fb28. Source: Will Cook, The Binary Totient Series, pinned revision 3368d1e69467aec111eb3244843ad3542171ff96, blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, original full Cook phase and recurrence. Classical prime number theorem in a fixed reduced arithmetic progression and divergence of the sum of reciprocals of primes are external inputs.

## 1. Genuine prime-conditioned arithmetic

Fix h≥1. Choose a squarefree integer M coprime to h with phi(M)/M≤1/100. Such M exists by the divergent prime reciprocal sum, omitting the finitely many divisors of h. For primes p congruent to -h modulo M, the exact totient product and phi(p)=p-1 give

$$
d_p=\varphi(p+h)-\varphi(p)=-p+e_p,
\qquad e_p=1+\varphi(p+h)\le 1+(p+h)/100.
$$

This is a genuine arithmetic restriction on a reduced prime progression, not a probabilistic model of overlapping windows.

For integers r tending to infinity put X=2^r-r-h-10, L=r+5, Q=2^L. Eventually X>0, L≥26+h, and L is the least Cook-legal depth: 16(2X+h+L+2)≤Q, whereas for any smaller depth L'≥h the right-hand side 2^L'≤Q/2<32X. Also 32X≤Q≤33X eventually.

Let P be the primes in [X+L+1,2X+L-1] congruent to -h modulo M; g=|P|. The fixed-modulus prime number theorem gives g asymptotic to X/(phi(M) log X) and the empirical scaled prime positions p/X converge to the uniform distribution on [1,2]. Indeed this holds on every fixed subinterval by subtraction of prime counts, and bounded Riemann sums yield the first and second moments. Thus the empirical variance of p/X tends to 1/12. For large r the standard deviation of p exceeds 7X/25; the standard deviation of e_p is at most X/40, since all e_p lie in [0,X/40]. The triangle inequality for centered L2 gives

$$
\mathrm{Var}_{p\in P}(d_p)\ge X^2/16.
$$

Here and below variance uses the uniform probability measure on this nonempty finite prime set. The proof requires only a fixed arithmetic progression; its modulus can be enormous and the onset is not claimed effective.

## 2. Original full phases and unconditional pair spread

Write the original full Cook numerator D_N as in WP09-L, E_N=exp(2 pi i D_N/Q). At N=p-L-1 the exact sliding recurrence gives the unit phases

$$
A_p=E_{p-L-1},\qquad B_p=E_{p-L},\qquad R_p=B_p\overline{A_p}^{\,2}=\exp(2\pi i d_p/Q).
$$

Both starts belong to [X,2X). For a unit phase family U indexed by P define V(U)=1-|mean U|², equivalently half the mean squared ordered-pair chord. For large r, |d_p-d_q|≤41X/40<Q/8. For 0≤u≤1/8 the chord 2 sin(pi u)≥6u by concavity and sin(pi/8)>3/8. Therefore

$$
V(R)\ge 36\mathrm{Var}(d_p)/Q^2\ge 1/484.
$$

For each ordered pair, |R_p-R_q|≤|B_p-B_q|+2|A_p-A_q| by the unit-circle product identity. Taking L2 over the pairs gives

$$
\sqrt{V(R)}\le\sqrt{V(B)}+2\sqrt{V(A)}.
$$

Consequently max(V(A),V(B))≥1/4356. For every fixed h and every sufficiently late r, at least one of the two genuine full-Cook prime-conditioned phase means has squared modulus ≤1-1/4356, hence ≤1-1/5000. The constant is independent of h; the fixed progression and onset depend on h. By pigeonhole, one of the two offset choices succeeds on a cofinal subsequence. This is unconditional cofinal dispersion of original complete phases, not merely unwrapped variance.

## 3. Exact limitation and rational-shadow control

The selected populations are sparse prime progressions, and the offsets are L+1 and L, not the original WP09-M cofactor anchor t=L-25. This theorem does not prove the WP09-M aggregate C/H bound, or even its weaker 81/100 target for these selected populations. The squared modulus bound 1-1/4356 is much larger than cos²(pi/8). A stronger inequality is required.

Moreover the terminal cocycle proof is stable under any bounded integer coefficient perturbation b of phi. If |b(n)-phi(n)|≤K globally, its terminal difference changes by at most 2K. Its R phase differs pointwise by at most 4 pi K/Q, tending to zero even on this sparse selected progression. Thus its V(R) differs by o(1), and the same L2 transfer gives max(V(A_b),V(B_b))≥1/4356-o(1). In particular the protected WP09-I parity-preserving two-unit dyadic-rational shadow satisfies this same asymptotic bound. The proof is therefore not an irrationality argument and cannot be amplified merely by assuming the sparse prime-conditioned cocycle detects rationality.

Next obligation: establish dispersion for the individual original complete phases substantially beyond this shadow-stable bound, using exact multiplicativity/carry information not stable under bounded coefficient errors. No novelty claim, no MATHCERT.

## 4. Finite exact checks

Using the full Cook numerator and the inherited exact root enclosures, three smaller CRT progressions at the ordinary least legal depth L=19 give the following finite specimens. These small moduli do not satisfy the strong cofinal ratio assumption and are not the canonical s=26 floor at this finite scale. All decimal lower bounds below are rounded downward.

| h | M | X | selected primes | certified lower bound for max(V(A),V(B)) |
|---|---|---|---|---|
| 1 | 30 | 16359 | 204 | 0.998 |
| 2 | 105 | 16358 | 30 | 0.991 |
| 6 | 385 | 16354 | 8 | 0.988 |

The exact terminal chord and pair transfer inequalities pass in all specimens. No finite specimen implies the cofinal required bound. Local complete registered suite: 153/153 PASS. CHAD OS-only source execution capture 59eb9ac53233441e92fb07813a250303, output SHA256 5dc6213c422161b38f1445ba88f5043ad38cedd5f97222059876ea4a476a908b; finite detail capture 27bc0fc801304ce7bdde3e2a0c6a66cf. Neither is an independent theorem attestation.
