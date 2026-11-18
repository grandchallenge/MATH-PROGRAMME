# Erdős #249 WP07-C — adversarial proof and source review

**Review role:** non-authoring GCL Adversary/Referee logical pass by the **same authenticated agent** as author; not a separate identity, independent human referee, Lean formal proof or MATHCERT certification.  
**Original Erdős #249:** OPEN. **Positive cofinal harmonic producer:** OPEN in [workstream #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Reviewed manuscript SHA-256:** f1ba9a64d53b516a0985589a86fbe78a24f3dd42e40a3121273ab3f6d8fa55d.  
**Reviewed module SHA-256:** 887bf3bc85972b6fdb5647b3ff36edc9b8dc8c546e83e55a83d2197399bb38c2.  
**Reviewed source tests SHA-256:** 1e4c394fa3825eb09a290fc089e94239bbfb1278e61142b198b0329505f7e7c7.  
**Exact test head at execution:** 546ad61087395c01b29c6524c7174d453cb145c9.  
**Source math gate:** PASS. **New tests:** 9/9 PASS. **Whole existing registered full-series suite:** 16/16 PASS.

## A. Is the bounded-odd-part reduction unconditionally valid?

For $n\in E_C(X)$, $k=\lfloor\log_2n\rfloor$ and $v=\nu_2(\varphi(n))\ge k-C$. Because $\varphi(n)\le n<2^{k+1}$, the odd part $u=\varphi(n)/2^v<2^{C+1}$. This uses only positive-integer arithmetic and holds even if $k-C<0$, since the displayed lower bound on $2^v$ remains true. Neither prime distribution nor convergence of the original binary series enters.

## B. Does the permitted odd-prime factor form omit prime powers or repeated $p$?

No. For $p^a\parallel n$ with $p$ odd, $\varphi(p^a)=p^{a-1}(p-1)$ divides $\varphi(n)$ through its multiplicative prime-power factorization. The odd part of $p-1$ therefore divides $u$, hence is below $B=2^{C+1}$. So $p=1+d2^r$ with odd $1\le d<B$ and integer $r\ge1$. When $p>B$, exponent $a$ cannot exceed one because otherwise $p$ divides the odd part $u<B$. When $p\le B$, its exponent is bounded by $1+\lfloor\log_pB\rfloor$. The overcount of up to $B$ candidate primes at each $r$ is safe, irrespective of actual primality or coincidence across levels. Unique factorization prevents duplicate representations of one $n$ from invalidating an upper bound.

## C. Does the weighted partition bound count all combinations?

A large odd prime factor $p=1+d2^r$ contributes more than $r$ binary logarithmic units to $\log_2n$. Thus $\sum r\le R=\lfloor\log_2X\rfloor$. At most $B$ *distinct* eligible primes occur at each $r$. Choosing any subset yields a monomial from $\prod_{r\ge1}(1+t^r)^B$, whose coefficient counts the possible slot-subsets by total cost; the manuscript uses only its coefficients through degree $R$. For $s>0$ their sum is at most $e^{sR}G(e^{-s})$. The elementary $\log(1+y)\le y$ and $e^s-1\ge s$ imply the bound $\exp(sR+B/s)$; at $s=\sqrt{B/R}$ it is $\exp(2\sqrt{BR})$. The proof does not assume prime randomness, independent divisibility, Selberg–Delange or a prime-number theorem.

The nine hostile tests compare this polynomial coefficient count against separately enumerated bit subsets for small $B,R$. One initial independent enumeration test had a grouping-index error; it was corrected on the **source branch** and fresh exactly-head tests passed before this review. The mathematical bound itself was not changed.

## D. Does the near-log termwise corollary impose the right quantifiers?

Yes. Let $k=\lfloor\log_2X\rfloor$, $L=k-C$ and $N\in[X,2X)$. If the finite window is *termwise* integral, its last term implies $\nu_2\varphi(N+L)\ge L$. Since $N+L<3X<2^{k+3}$, $\lfloor\log_2(N+L)\rfloor\le k+2$. Thus $N+L$ belongs to $E_{C+2}(3X)$. Distinct $N$ give distinct last indices. Applying the proven bound yields $X^{o(1)}$ qualifying starts. This statement does not require cancellation assumptions for neighboring indices.

## E. Is an illegitimate finite-sum integrality inference being made?

No. **Termwise integrality** implies integrality of the sum, but the converse is false due to cancellation. The tests deliberately exhibit $\varphi(2)/2+\varphi(3)/4=1$, although both terms are nonintegers. Thus this theorem **does not** give an upper bound for starts with an *integral total* finite tail or a positive lower bound on its residue distance. That missing transfer remains the actual mathematical obstruction to irrationality.

## F. Is the antecedent and implementation scope honest?

The 2025 Zhao paper treats extremal $p$-adic totient valuations, so no priority or novelty assertion follows merely from the near-maximal valuation formulation. GCL WP07-A's loglog-depth totient theorem and WP07-B's rational nearlog-depth comparator provide context, but neither is logically used as a premise in this proof. The exact suite performs a bounded independent factorization audit and verifies full prior registered totient regression. Formal publication/certification is not implied.

**Disposition:** ACCEPT_WITH_SCOPE for the elementary self-contained counting theorem, its strictly termwise nearlog corollary, exact finite hostile tests and explicit open-claim firewall. No independent mathematical certification, no claim that Erdős #249 is solved, and no permission to close #3500 or #3201.
