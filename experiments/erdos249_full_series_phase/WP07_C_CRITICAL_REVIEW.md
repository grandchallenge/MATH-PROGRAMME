# Erdős #249 WP07-C — adversarial proof and source review

**Review role:** non-authoring GCL Adversary/Referee logical pass by the **same authenticated agent** as author; not a separate identity, independent human referee, Lean formal proof or MATHCERT certification.  
**Original Erdős #249:** OPEN. **Positive cofinal harmonic producer:** OPEN in [workstream #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Reviewed manuscript SHA-256:** b8176e32a2ed43108dcd7608381e8d6774aeb492e3ca6b490fa1465e52d29b6b.  
**Reviewed module SHA-256:** 661e37d6d837a5a0d1df433d60f33fcd875db4b6f3f8eb427ef91aa61568072c.  
**Reviewed source tests SHA-256:** 35b33bb22d6597b0a8b263b6c20dc3c7b580ec407e4e004756cf599b0be4a5c0.  
**Exact test head at execution:** 88f43bc6871e81ca554ce7eadc1959690854996d.  
**Source math gate:** PASS. **New tests:** 12/12 PASS. **Whole existing registered full-series suite:** 19/19 PASS.

## A. Is the bounded-odd-part reduction unconditionally valid?

For $n\in E_C(X)$, $k=\lfloor\log_2n\rfloor$ and $v=\nu_2(\varphi(n))\ge k-C$. Because $\varphi(n)\le n<2^{k+1}$, the odd part $u=\varphi(n)/2^v<2^{C+1}$. This uses only positive-integer arithmetic and holds even if $k-C<0$, since the displayed lower bound on $2^v$ remains true. Neither prime distribution nor convergence of the original binary series enters.

## B. Does the permitted odd-prime factor form omit prime powers or repeated $p$?

No. For $p^a\parallel n$ with $p$ odd, $\varphi(p^a)=p^{a-1}(p-1)$ divides $\varphi(n)$ through its multiplicative prime-power factorization. The odd part of $p-1$ therefore divides $u$, hence is below $B=2^{C+1}$. So $p=1+d2^r$ with odd $1\le d<B$ and integer $r\ge1$. When $p>B$, exponent $a$ cannot exceed one because otherwise $p$ divides the odd part $u<B$. When $p\le B$, its exponent is bounded by $1+\lfloor\log_pB\rfloor$. The overcount of up to $B$ candidate primes at each $r$ is safe, irrespective of actual primality or coincidence across levels. Unique factorization prevents duplicate representations of one $n$ from invalidating an upper bound.

## C. Does the weighted partition bound count all combinations?

A large odd prime factor $p=1+d2^r$ contributes more than $r$ binary logarithmic units to $\log_2n$. Thus $\sum r\le R=\lfloor\log_2X\rfloor$. At most $B$ *distinct* eligible primes occur at each $r$. Choosing any subset yields a monomial from $\prod_{r\ge1}(1+t^r)^B$, whose coefficient counts the possible slot-subsets by total cost; the manuscript uses only its coefficients through degree $R$. For $s>0$ their sum is at most $e^{sR}G(e^{-s})$. The elementary $\log(1+y)\le y$ and $e^s-1\ge s$ imply the bound $\exp(sR+B/s)$; at $s=\sqrt{B/R}$ it is $\exp(2\sqrt{BR})$. The proof does not assume prime randomness, independent divisibility, Selberg–Delange or a prime-number theorem.

The twelve hostile tests compare this polynomial coefficient count against separately enumerated bit subsets for small $B,R$. One initial independent enumeration test had a grouping-index error; it was corrected on the **source branch** and fresh exactly-head tests passed before this review. The mathematical bound itself was not changed.

## D. Does the near-log termwise corollary impose the right quantifiers?

Yes. Let $k=\lfloor\log_2X\rfloor$, $L=k-C$ and $N\in[X,2X)$. If the finite window is *termwise* integral, its last term implies $\nu_2\varphi(N+L)\ge L$. Since $N+L<3X<2^{k+3}$, $\lfloor\log_2(N+L)\rfloor\le k+2$. Thus $N+L$ belongs to $E_{C+2}(3X)$. Distinct $N$ give distinct last indices. Applying the proven bound yields $X^{o(1)}$ qualifying starts. This statement does not require cancellation assumptions for neighboring indices.

## E. Does the new adjacent-integrality proof validly handle cancellation in the *finite sum*?

Yes. **Termwise integrality** implies integrality of the sum, but the converse is false due to cancellation: $\varphi(2)/2+\varphi(3)/4=1$. The new theorem instead exploits the exact integer numerator recurrence

\[
A_{N+1,L}=2A_{N,L}-2^L\varphi(N+1)+\varphi(N+L+1).
\]

If the whole finite sums at *both* $N$ and $N+1$ are integers, the two numerators vanish modulo $2^L$, forcing $2^L\mid\varphi(N+L+1)$. With $L=\lfloor\log_2 X\rfloor-C$ and $N\in[X,2X)$ this puts the final index $N+L+1$ in $E_{C+2}(3X)$, except for an irrelevant finitely bounded range of small $X$. Injectivity gives at most $X^{o(1)}$ adjacent-integral pairs. Grouping starts into disjoint consecutive pairs proves an upper density of at most one-half for **integral whole finite sums**. Both the recurrence and direct finite-sum arithmetic were independently checked in the new tests. This argument *does not* need any independence hypothesis about neighboring totients.

The proof gives **nonintegrality**, not a quantitative separation from the nearest integer. A dyadic finite sum can have fractional distance as small as $2^{-L}$, while the standard bound on the actual omitted infinite tail is still much larger. Therefore the transfer to nonintegrality of the *infinite* tail, or to Cook's positive Fourier criterion, remains unproved.

## F. Is the antecedent and implementation scope honest?

The 2025 Zhao paper treats extremal prime-adic totient valuations, so no priority or novelty assertion follows merely from the near-maximal valuation formulation. GCL WP07-A's loglog-depth totient theorem and WP07-B's rational nearlog-depth comparator provide context, but neither is logically used as a premise in this proof. The exact suite performs a bounded independent factorization audit, a direct-versus-rolling finite-sum comparison, a rational hostile control, and full prior registered totient regression. Formal publication/certification is not implied.

**Disposition:** ACCEPT_WITH_SCOPE for the elementary self-contained counting theorem, its termwise nearlog corollary, its rare-adjacent-integral-sum and half-density corollary, exact finite hostile tests and explicit open-claim firewall. No independent mathematical certification, no claim that Erdős #249 is solved, and no permission to close #3500 or #3201.
