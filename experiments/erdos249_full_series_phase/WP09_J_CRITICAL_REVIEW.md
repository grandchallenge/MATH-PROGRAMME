# WP09-J — qualified adversarial mathematical review

**Claim materials:** MULTIPLICATIVE_FOURIER_RIGIDITY_009J.md, multiplicative_fourier_rigidity.py, the incremental tests in tests/test_erdos249_full_series_phase.py.  
**Sources:** Original Will Cook paper/249 at revision 3368d1e69467aec111eb3244843ad3542171ff96 and blob 547ed9ed83500181a2e55047ce5df569b7cb49ac. Actual WP09-I two-unit shadow protected PR #3649, protected merge 4f0c20e2b0b901687bb9a6627b0ac502b28341a8.  
**Review authority:** separate same-agent Axiomatist, Verifier, Adversary and Referee *logical* passes only; NOT independently authenticated mathematical certification, external human review, Lean kernel checking, or MATHCERT.

## Axiomatist: the exact nonconflated claim

The new object is the multiplicative-defect character exp(2 pi i (b(nm)-b(n)b(m))/Q), with m in one congruence class modulo fixed n and Q the least source-legal h=1 Cook depth for X=nP. This is **not** the original shifted full-Cook exponential e(D_phi(h,N,L)/Q). The actual totient has **zero** multiplicative defect and therefore normalized real mean 1. Any parity-preserving two-unit perturbation of phi that differs at a fixed n has a **positive-density nonzero Fourier defect** and normalized mean <=1-1/(24000n^2) cofinally.

The result makes high-frequency exact coprime arithmetic available as a strong Fourier observable and is **not** an irrationality claim. It does not use a random or independent prime model.

## Verifier: check each arithmetic and analytic constant

1. The 0<=b(j)<=j and parity conditions force exact b(1)=phi(1)=1 and b(2)=phi(2)=1. Every nontrivial b has a modified n>=3 and |epsilon(n)|=2, since other allowed differences are zero or +/-2.
2. For m ≡1 mod n, (m,n)=1, so true phi(nm)=phi(n)phi(m), without any exception involving shared primes.
3. The identity phi(m)/m=sum_(d|m)mu(d)/d is exact. For squarefree or nonsquarefree d sharing gcd(d,n)>1, the simultaneous system m≡1 mod n, d|m is empty. If gcd(d,n)=1, one residue class modulo nd applies, with count discrepancy <=1 in [P,2P). Summing coefficient errors yields H_(2P)<=1+log(2P), and the Euler-product tail costs <=1/(2n). Thus total error <2+log(2P)<E_P=3+bitlength(2P).
4. C_n=product_(p not dividing n)(1-1/p^2)>=6/pi^2>3/5. The gate P/n>=32E_P gives F >=(3/5-1/32)P/n=91P/(160n). The progression size W<=P/n+1<=(33/32)P/n, so F/W>=91/165>1/2.
5. If H members have phi(m)/m>=1/3, using the true range [0,1] gives F<=W/3+2H/3, therefore H>=W/4. Since W>=P/n-1 and P/n>=32, H>=P/(5n).
6. Exact defect identity for a parity-preserving two-unit b: Delta_b=epsilon(nm)-epsilon(n)phi(m)-b(n)epsilon(m). With |epsilon(n)|=2 and 0<=b(n)<=n, its absolute value is in [2phi(m)-2(n+1),2phi(m)+2(n+1)] (the lower inequality is informative only once positive).
7. For good m, phi(m)>=m/3 and m>=P>=32(n+3), so m/2<=|Delta_b|<=3m. This applies to ALL adversarial signs and placements of other corrections, including b(nm), not merely the special one-sided shadow.
8. For L the **least** Cook-legal depth at X=nP, 2^L>=16(2X+L+3)>32X and predecessor depth failure gives Q<32(2X+L+2)<=96X under L+2<=X. Thus 1/(192n)<|Delta_b|/Q<3/(16n)<=1/16. This excludes integer winding in the multiplicative defect phase.
9. The global inequality 1-cos(2pi t)>=8t^2 for |t|<=1/2 gives per-good-m deficit at least 1/(4608n^2). There are at least P/(5n) good sources, so full deficit >=P/(23040n^3). Divide by W<=33P/(32n) for normalized gap >=1/(23760n^2)>1/(24000n^2).
10. For any b different from phi at some n, that fixed n contradicts limsup Fourier mean =1. Conversely true phi makes every defect zero. Thus the theorem is an exact equivalence within the two-unit parity class, **not** a characterization among all integer sequences.
11. K=8, M=24: phi25=20, phi26=12, phi27=18, phi28=12. Their contribution to 2^20*delta_8 is exactly 1; remaining contribution is >0 and <=15/128. Therefore 1<2^13*x_8<143/128<2, so the first twelve floor bits are zero, b_13=1 and the first changed index is n=8+13=21, phi21=12, shadow a8(21)=10. This exact four-coefficient observation does **not** assume anything about irrationality of alpha.

## Adversary: failure modes and limits

- **Phase identity confusion:** Cook's original E_N is a full, overlapping weighted sum of genuine totients. The positive-density bound here applies to a NEW bilinear product-defect exponential. There is NO valid inference from D_b(n,P)>0 to the original Cook 9X/10 first harmonic.
- **Wrong-sign inference:** For true phi the defect Fourier is identically 1, while for the false rational shadow it is strictly BELOW one. A smaller real mean of this detector is *evidence of departure from phi*, not a proof that phi's original phase cancels.
- **Prime-only density:** The multiplier set contains all integers m in a residue class, not merely primes. The positive fraction is among ALL multipliers P<=m<2P and is at least 1/(5n), with n fixed. No prime-number theorem is invoked.
- **Source-independent correction:** The theorem allows arbitrary signed eta in {-2,0,2} across all indices, but b itself must obey parity and the 0<=b(j)<=j envelope globally. It does not rely on the source's canonical binary correction bits except to certify a8(21) differs.
- **No high-frequency alias:** The scaled defect is explicitly <1/16, so the central-arc cosine inequality applies to the true modulo-one character; no unwrapped energy mistaken for phase energy.
- **Least L versus fixed L:** The Q<96nP upper is derived using *minimality* at h=1 and L+2<=nP. The theorem does not extend to arbitrarily larger L; at large Q the character tends back to 1.
- **Strict P and n boundaries:** The finite gates are explicit; n≥3. The first n21 shadow certificate uses only four phi values and an elementary absolute tail bound, not a hidden evaluation of the true binary series.
- **Actual shadow huge-index digits:** The finite verifier does not compute eta(nm) for m~20000 and n=21. Instead it checks exact worst-case inequalities that hold for **all possible bits**. A separate one-flip sample is labelled a NONRATIONAL control; it is not presented as direct numeric evidence about the infinite rational shadow.
- **Computational samples versus theorem:** 952/952 good multipliers at n21,P20000 is an exact finite observation. The analytic CRT bound proves a weaker >=P/(5n) universally on all eligible P. Finite cosine is diagnostic, not analytic certification.
- **No unapproved novelty/priority or MATHCERT:** Same-agent review and green CI are not external verification. The research theorem is bounded and the actual irrationality target remains open.

## Referee: required disposition and next obligation

Subject to exact-head repository CI, mathematical Markdown source gate, native protected merge queue and exact merge-group validation, the bounded universal Fourier rigidity theorem and explicit n21 rational-shadow witness are eligible for research admission as **new programme progress**, not for irrationality certification.

**Next real obligation:** a quantitative relation between the **product-factorization Fourier character** and the **original full Cook good-set weighted phase** w_N z_N, or a multiplicativity-sensitive two-adic carry-escape estimate with a genuine original-phase 9X/10 bound. Current WP09-J moves exact multiplicativity into a positive-density Cook-scale Fourier test but does not provide this transfer. Keep #3500 and original Erdős #249 OPEN, MATHCERT NOT_SUBMITTED.
