# Erdős #249 — WP07-D: polylogarithmic near-maximal totient valuations and the Fermat-prime decomposition

**Research workstream:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500)  
**Date:** 2026-11-18 UTC  
**Claim status:** noncertifying elementary manuscript proof and exact arithmetic witnesses; original Erdős #249 **OPEN**, MATHCERT **NOT_SUBMITTED**

## 1. Exact antecedent and improvement

The protected [WP07-C](NEARMAX_TOTIENT_VALUATION_007C.md) proved an explicit upper bound for

$$
E_C(X)=\{1\le n\le X:\nu_2(\varphi(n))\ge\lfloor\log_2n\rfloor-C\}
$$

of the form $\exp(O_C(\sqrt{\log X}))$. This WP improves that estimate to a **polynomial in $\log X$ for every fixed integer $C\ge0$**. It also extends the range to a specified slowly growing $C=C(X)$ without requiring an unproved theorem.

**Prior mathematical literature:** Jun-Jia Zhao, *p-Adic Valuation of Euler's Totient Function* (2025), DOI: [10.1007/s40840-025-01869-7](https://doi.org/10.1007/s40840-025-01869-7), states the exact equality characterization at $C=0$: $\nu_2\varphi(n)=\lfloor\log_2n\rfloor$ precisely for products of distinct Fermat primes. The equality classification in Section 3 is included as a self-contained derivation and a hostile consistency check, **not claimed as new or GCL-priority mathematics**. The quantitative strengthening for fixed $C$ should also receive a dedicated literature review before any novelty claim.

Will Cook's *The Binary Totient Series* (2026, revised October 1) supplies much stronger source-locked conditional criteria for the original irrationality conjecture. No consequence of this packet is presented as satisfying those open criteria.

## 2. Theorem A — an explicit polylogarithmic count

Fix $C\ge0$, $X\ge2$ and put

$$
R=\lfloor\log_2 X\rfloor,\quad
B=2^{C+1},\quad
K_B=\max\{k\in\mathbb Z_{\ge0}:3^k<B\}.
$$

Write

$$
D_B=\prod_{\substack{3\le p\le B\\p\ {\rm prime}}}
\left(2+\lfloor\log_p B\rfloor\right).
$$

**Theorem A.** The following fully explicit estimate holds:

$$
\boxed{
\#E_C(X)\le
(R+1)D_B\,
2^{1+\lfloor\log_2 R\rfloor}
\sum_{j=0}^{K_B}\binom{BR}{j}.
}
\tag{A}
$$

In particular, for fixed $C$,

$$
\boxed{\#E_C(X)=O_C((1+\log X)^{K_B+2}).}
\tag{B}
$$

This is quantitatively stronger than WP07-C's $\exp(O_C(\sqrt{\log X}))$. The powers are upper bounds only; no asymptotic equality is asserted.

**Proof.** Let $n\in E_C(X)$, put $v=\nu_2(\varphi(n))$ and $u=2^{-v}\varphi(n)$, the positive odd part of $\varphi(n)$. As in WP07-C, $\varphi(n)\le n<2^{\lfloor\log_2n\rfloor+1}$ gives

$$
1\le u<B.
\tag{1}
$$

For each distinct odd prime $p\mid n$, factor

$$
p-1=d_p2^{r_p},\qquad d_p\ {\rm odd},\quad r_p\ge1.
\tag{2}
$$

Since $\varphi(n)$ contains every $p-1$ as a multiplicative prime-power factor, the **product** of the odd factors $d_p$ divides $u$. In particular $d_p<B$ and

$$
\prod_{\substack{p\mid n\\p>2}}d_p\le u<B.
\tag{3}
$$

An odd prime with $d_p=1$ is of the form $p=2^{r_p}+1$. **Elementary Fermat factorization:** if $r_p=2^a m$ where $m>1$ is odd, then $2^{2^a}+1$ is a proper factor of $2^{r_p}+1$, contradicting primality. Thus $r_p$ must be a power of two. Because $p\le n\le X$, we have $r_p\le R$. There are at most $1+\lfloor\log_2 R\rfloor$ possible exponents $r_p\in\{1,2,4,\ldots\}$, so the number of subsets of all such candidate primes is at most

$$
2^{1+\lfloor\log_2 R\rfloor}\le2R.
\tag{4}
$$

This is an *overcount*, since most Fermat numbers could be composite and small Fermat primes may also be counted in $D_B$.

For the remaining odd primes, $d_p\ge3$. Equation (3) shows that their **number**, including those with $p>B$, is at most $K_B$, because $3^{K_B+1}\ge B>u$. Each such **large** prime $p>B$ is uniquely specified by a pair $(d_p,r_p)$ with odd $3\le d_p<B$ and $1\le r_p\le R$, giving at most $BR$ candidate slots, even before imposing primality. Therefore the number of subsets containing up to $K_B$ such primes is at most

$$
\sum_{j=0}^{K_B}\binom{BR}{j}.
\tag{5}
$$

If an odd prime $p>B$ divides $n$, its exponent in $n$ is exactly one: an exponent at least two would put the odd factor $p$ into $\varphi(n)$ and hence into $u<B$, impossible. For each odd prime $p\le B$, the exponent of $p$ in $n$ has at most $2+\lfloor\log_pB\rfloor$ choices, including absence, because $p^{a_p-1}$ divides $u$ whenever $a_p\ge1$. Multiplying over small odd primes gives at most $D_B$ patterns. The exponent of $2$ in $n$ has at most $R+1$ choices, including zero.

All allowed factorizations have therefore been counted by the product of (4), (5), the finite small-prime exponent patterns and the exponent of two. That proves (A). Since $B,K_B,D_B$ are constant for fixed $C$, and $\sum_{j=0}^{K_B}\binom{BR}{j}=O_C(R^{K_B})$, the remaining prefactors supply at most $O(R^2)$; (B) follows. QED.

**Where WP07-C lost sharpness:** Its weighted-partition overcount treated every $d_p=1$ prime as if a new candidate existed at *every* exponent $r\le R$. The elementary Fermat-factorization rule instead permits those primes only at exponents $1,2,4,8,\ldots$, reducing their entire subset count to $O(R)$. The $d_p\ge3$ factors consume a bounded, multiplicative odd-part budget, restricting their number to $K_B$. No prime-distribution estimate, Fermat-prime infinitude conjecture, or Selberg–Delange input is used.

## 3. The established exact $C=0$ classification (reproved, not new)

**Proposition (Zhao's equality characterization).** For each positive integer $n$,

$$
\nu_2(\varphi(n))=\lfloor\log_2 n\rfloor
\quad\Longleftrightarrow\quad
n=\prod_{j\in J}\left(2^{2^j}+1\right)
$$

where $J$ is a finite set of nonnegative integers and every displayed Fermat number is prime. The empty product is $n=1$.

**Proof.** For $C=0$ equation (1) gives $1\le u<2$, hence $u=1$ and $\varphi(n)$ is a pure power of two. Consequently $n=2^a$ times a squarefree product of odd primes with $p-1$ a pure power of two. The argument above makes these precisely the Fermat primes. Write their distinct exponents $r_j=2^j$, and put $T=\sum_{j\in J}r_j$.

The finite-product identity, specialized to $x=1/2$,

$$
\prod_{j=0}^{m}(1+2^{-2^j})
=\frac{1-2^{-2^{m+1}}}{1-1/2}<2
\tag{6}
$$

shows that **every** finite subproduct has value in $[1,2)$. Thus

$$
2^{a+T}\le n<2^{a+T+1},
\qquad
\lfloor\log_2n\rfloor=a+T.
$$

If $a\ge1$, then $\varphi(n)=2^{a-1+T}$, giving $\nu_2(\varphi(n))=a-1+T$, one smaller than $\lfloor\log_2n\rfloor$. Hence $a=0$. Conversely an odd squarefree product of distinct Fermat primes has $\varphi(n)=2^T$, and (6) gives $\lfloor\log_2n\rfloor=T$. This establishes the equivalence. QED.

**Corollary.** At $C=0$, the sharper bound

$$
\#E_0(X)\le 2^{1+\lfloor\log_2R\rfloor}\le2R
$$

holds for $R=\lfloor\log_2X\rfloor\ge1$. Its exact count depends on which Fermat numbers are prime and fit below $X$; no unproved assumption is made.

## 4. Uniformly growing nearmax deficit

The explicit estimate (A) remains valid if $C$ varies with $X$. Fix any $0<\delta<1$ and suppose

$$
2^{C(X)+1}\le R^{1-\delta},
\qquad R=\lfloor\log_2X\rfloor.
$$

Then uniformly over such $C(X)$,

$$
\boxed{\#E_{C(X)}(X)\le \exp(o(R))=X^{o(1)}.}
\tag{C}
$$

**Proof.** Set $B=2^{C(X)+1}\le R^{1-\delta}$ and $K_B=O(\log B)$. The product $D_B$ has at most $B$ factors, each at most $2+\lfloor\log_3B\rfloor$, so

$$
\log D_B\le B\log(2+\log_3B)
=O_\delta(R^{1-\delta}\log\log R)=o(R).
$$

For $BR\ge1$,

$$
\sum_{j=0}^{K_B}\binom{BR}{j}
\le(K_B+1)(BR)^{K_B}.
$$

Its logarithm is $O(\log B\log(BR))=O((\log R)^2)=o(R)$. The remaining factors $(R+1)2R$ have logarithms $O(\log R)=o(R)$. Hence the logarithm of the complete right-hand side of (A) is $o(R)$, proving (C). The small ranges where the displayed constraint admits no nonnegative $C$ are vacuous. QED.

This extends the rare near-maximal totient valuation regime to deficits as large as roughly $(1-\delta)\log_2\log_2X$ below the logarithmic exponent, not merely a constant.

## 5. Consequence for *complete* truncated totient sums

At $L=\lfloor\log_2X\rfloor-C$, define as in WP07-C the numerator

$$
A_{N,L}=\sum_{j=1}^{L}2^{L-j}\varphi(N+j).
$$

The protected exact sliding recurrence

$$
A_{N+1,L}=2A_{N,L}-2^L\varphi(N+1)+\varphi(N+L+1)
\tag{7}
$$

shows that if **both** $A_{N,L}$ and $A_{N+1,L}$ vanish modulo $2^L$, then $2^L\mid\varphi(N+L+1)$. For $N\in[X,2X)$ and large $X$, the last index $N+L+1$ belongs to $E_{C+2}(3X)$.

Therefore, for each fixed $C$,

$$
\boxed{\#\{N\in[X,2X):U_{N,L},U_{N+1,L}\in\mathbb Z\}
=O_C((1+\log X)^{K_{2^{C+3}}+2}).}
\tag{D}
$$

The consequent total-integrality bound improves from WP07-C's $\frac X2+X^{o(1)}$ to

$$
\boxed{\#\{N\in[X,2X):U_{N,L}\in\mathbb Z\}
\le \tfrac X2+O_C((1+\log X)^{K_{2^{C+3}}+2})+O(1).}
\tag{E}
$$

The same subpolynomial conclusions hold for varying $C(X)$ that satisfy $2^{C(X)+3}\le \lfloor\log_2(3X)\rfloor^{1-\delta}$ for fixed $\delta>0$, at sufficiently large $X$.

**Scope firewall:** These results concern (a) the *frequency* of unusually high totient valuations and (b) adjacency of **integral whole finite windows**. They give neither a lower bound on the **distance** of nonintegral $U_{N,L}$ to $\mathbb Z$ nor a bound that beats the omitted infinite tail. The rational comparator $a_n=\lfloor n/2\rfloor$ (whose full dyadic sum is exactly $2/3$) even has only $O_C(1)$ integral near-log windows per dyadic block, as independently proved and checked in [GCL issue #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500#issuecomment-6979828806). Thus no irrationality criterion follows from these frequency estimates alone.

The relevant strict dyadic separation criterion would need both a residue of magnitude larger than the hypothetical denominator times the analytic-tail numerator and a truncation depth $L$ beyond the geometric bound $2^{L-1}>q(N+L+2)$. At depths $L\le\lfloor\log_2X\rfloor$, **that criterion is arithmetically impossible even for nonzero residues**, since the least centered residue is at most $2^{L-1}\le X/2$ while $q(N+L+2)>X$ for any positive $q$. This is not a proof about $S$; it identifies why shallow frequency theorems are insufficient without a new transfer mechanism.

## 6. Evidence, adversarial controls, successor

Executable material is appended to the previously protected and already routed [nearmax totient module](nearmax_totient_valuation.py) and [full-series exact tests](../../tests/test_erdos249_full_series_phase.py) to avoid duplicating CI registration. The tests use independent Euler-totient/factorization checks, an exact combinatorial upper bound, the independently characterized $C=0$ Fermat subset list, and malformed-source contracts. Finite examples are supplementary; the universal estimates are proved above.

| Claim | Disposition |
| --- | --- |
| WP07-D-A: explicit fixed-deficit polylogarithmic bound | Elementary manuscript proof, tests; noncertifying |
| WP07-D-B: equality classification at $C=0$ | Independently reproved **antecedent Zhao (2025)**; no priority claim |
| WP07-D-C: uniform $C(X)$ deficit range | Elementary consequence of explicit bound |
| WP07-D-D: improved rarity of adjacent integral full finite totient sums | Elementary consequence of WP07-C and D-A |
| WP07-D-NEG: generic implication to original irrationality | **FALSE**, by the prior rational $\lfloor n/2\rfloor$ comparator |
| Original Erdős #249, cofinal actual-totient fractional separation, mathematical certification | **OPEN / NOT_SUBMITTED** |

**Next positive producer:** Prove a **totient-specific** quantitative cofinal separation of the complete finite sum from rationals, at a depth where the independently bounded infinite remainder cannot cover that separation, for every hypothetical denominator. Equivalently pursue the already source-locked good-base Fourier condition of Cook rather than another general integer-sequence criterion. Do not close research issue #3500 on the strength of this bounded theorem.
