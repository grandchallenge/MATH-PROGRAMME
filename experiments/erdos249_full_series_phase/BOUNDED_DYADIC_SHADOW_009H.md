# Erdős #249 — WP09-H: a six-unit dyadic-rational shadow of the actual totient

**Scientific issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Predecessor:** protected WP09-G [PR #3631](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3631), protected merge 95fdf1224077e6935cbbb00c6427149b8ea4d60b.  
**Primary source lock:** Will Cook, *The Binary Totient Series*, [revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.  
**Exact claim class:** a constructive six-unit rational-shadow **no-go theorem**, a quantitative multi-prime and multistep *stability* theorem, and an exact multiplicative-rigidity obstruction for the shadow. **No claim of irrationality or Cook's strong ten-percent cancellation.** MATHCERT NOT_SUBMITTED.

## 1. Decisive issue exposed by WP09-G

WP09-G established an actual Euler-totient imaginary Cook cocycle contrast, of order X, between terminal classes 0 and 2 modulo six. Its earlier parity-based rational comparator did not have that second-prime signature. This result suggested collecting enough finite-prime cocycle contrasts to force the actual **original Cook phases** away from the real part 1.

**Theorem A below proves that such an inference is invalid when the inputs are only leading normalized finite-prime statistics and bounded-time cocycle sums.** There is a rational sequence within **six integer units of the actual Euler totient at every index**, with parity and the natural $0\le a(n)\le n$ envelope intact. It reproduces the WP09-G *order-X* imaginary cocycle contrast, up to an error of order one, yet its complete original Cook phases are uniformly closer than $1/16$ to integers at every sufficiently late legal Cook block.

The construction is not a heuristic. It is defined through an explicit positive arithmetic tail and exact base-four floor digits, without assuming whether the actual totient series is rational or irrational.

## 2. Theorem A: an arbitrarily late, six-unit, dyadic-rational totient shadow

Let

$$
\alpha=\sum_{n=1}^\infty\frac{\varphi(n)}{2^n}.
\tag{1}
$$

Fix an **arbitrary integer** $K\ge6$, set $M=3K$, and define the explicitly rational number

$$
\boxed{
\beta_K=
\sum_{n=1}^{M}\frac{\varphi(n)}{2^n}
+\frac{M+2}{2^M}
=
\frac{\sum_{n=1}^M\varphi(n)\,2^{M-n}+M+2}{2^M}.
}
\tag{2}
$$

The identity $\sum_{n>M}n/2^n=(M+2)/2^M$ gives the positive **exact** difference

$$
\boxed{
\delta_K=\beta_K-\alpha
=\sum_{n>M}\frac{n-\varphi(n)}{2^n}>0.
}
\tag{3}
$$

Set $B_K=2\cdot4^{-K}$ and

$$
x_K=\frac{\delta_K}{B_K}
=2^{2K-1}\sum_{n>3K}\frac{n-\varphi(n)}{2^n}.
\tag{4}
$$

Because $n-\varphi(n)\le n$,

$$
0<x_K\le\frac{3K+2}{2^{K+1}}<1
\quad(K\ge6).
\tag{5}
$$

Define its **canonical base-four floor digits**, for all $j\ge1$, by

$$
\boxed{
e_j=\lfloor4^j x_K\rfloor
-4\lfloor4^{j-1}x_K\rfloor\in\{0,1,2,3\}.
}
\tag{6}
$$

There is no ambiguity at a rational base-four endpoint: the floor definition chooses the terminating expansion. Telescoping gives

$$
\sum_{j=1}^J\frac{e_j}{4^j}
=\frac{\lfloor4^Jx_K\rfloor}{4^J}
\longrightarrow x_K.
\tag{7}
$$

Now define the genuine **bounded Euler-totient shadow** $a_K(n)$ by

$$
\boxed{
a_K(n)=
\begin{cases}
\varphi(n)+2e_j,&n=2(K+j),\quad j\ge1,\\
\varphi(n),&\text{otherwise}.
\end{cases}
}
\tag{8}
$$

**Theorem A (exact bounded rationalization).** For every $K\ge6$ and every integer $n\ge1$:

1. $a_K(n)$ is an integer, agrees **exactly** with $\varphi(n)$ for every $n\le2K$ and every odd n, and satisfies

$$
\boxed{
0\le a_K(n)-\varphi(n)\le6,\qquad
0\le a_K(n)\le n.
}
\tag{9}
$$

2. For all $n\ge3$, $a_K(n)$ is even, exactly as $\varphi(n)$ is.
3. Its **complete, infinite binary series is the explicit dyadic rational** $\beta_K$:

$$
\boxed{
\sum_{n=1}^\infty\frac{a_K(n)}{2^n}
=\alpha+2\cdot4^{-K}
\sum_{j=1}^\infty\frac{e_j}{4^j}
=\alpha+\delta_K=\beta_K
\in2^{-3K}\mathbb Z.
}
\tag{10}
$$

4. For **every** shift $h\ge1$ and every $N\ge3K$, the infinite shifted Cook argument

$$
T^a_{h,N}=\sum_{j=1}^\infty
2^{-j}[a_K(N+h+j)-a_K(N+j)]
\tag{11}
$$

is an **integer**. Consequently, for every $X\ge3K$ and every $L\ge h$ satisfying the original Cook size condition

$$
2^L\ge16(2X+h+L+2),
\tag{12}
$$

the *complete genuine-length Cook phases* of this shadow satisfy, for all $X\le N<2X$,

$$
\boxed{
\left\|\frac{D^{a_K}_{h,N,L}}{2^L}\right\|_{\mathbb R/\mathbb Z}
<\frac1{16},
\qquad
\mathrm{Re}\exp(2\pi iD^{a_K}_{h,N,L}/2^L)
>\cos(\pi/8)>\frac9{10}.
}
\tag{13}
$$

**Therefore Cook's sufficient ten-percent first-harmonic condition FAILS for this rational comparator on EVERY late admissible block and for EVERY shift h**, although the comparator is uniformly within six of the true totient.

### Proof

For the coefficient envelope, if n is modified then it is even, $n=2(K+j)\ge14$. The ordinary totient satisfies $\varphi(n)\le n/2$ for even n, while $2e_j\le6\le n/2$; hence $a_K(n)\le n$. For all other indices equality with the genuine totient is literal. Parity follows because modified values increase by even integers.

Equation (10) follows by direct exact substitution from (7). No knowledge of $\alpha$ beyond its convergent definition is used.

To prove the late integer-tail assertion, let

$$
R^a_N=\sum_{j=1}^\infty\frac{a_K(N+j)}{2^j}.
$$

By (10), for every $N\ge M=3K$,

$$
R^a_N
=2^N\beta_K
-\sum_{n=1}^N a_K(n)2^{N-n}
\in\mathbb Z,
\tag{14}
$$

since the denominator of $\beta_K$ divides $2^M$. Thus $T^a_{h,N}=R^a_{N+h}-R^a_N$ is an integer.

Using $0\le a_K(n)\le n$ and the exact geometric tail gives

$$
\left|T^a_{h,N}-\frac{D^{a_K}_{h,N,L}}{2^L}\right|
\le\sum_{j>L}\frac{N+h+j}{2^j}
=\frac{N+h+L+2}{2^L}<\frac1{16},
\tag{15}
$$

where the strict bound uses $N<2X$ and (12). Since $T^a_{h,N}$ is integral, the fractional-distance and real-cosine inequalities in (13) follow. The numeric bound $\cos(\pi/8)>0.9$ is elementary, for example $\cos(\pi/8)=\sqrt{2+\sqrt2}/2$. **This proves Theorem A exactly.**

As an explicit instance, $K=8$, $M=24$ gives

$$
\boxed{\beta_8=\frac{11472523}{8388608}.}
\tag{16}
$$

This dyadic rational is computed entirely from $\varphi(1),\ldots,\varphi(24)$; it is **not** a numerical assertion about the unknown irrationality status of $\alpha$.

## 3. Theorem B: the genuine WP09-G two-prime Fourier contrast survives rationalization

Write $\eta(n)=a_K(n)-\varphi(n)$, so $0\le\eta(n)\le6$. For every h,n, let $d_h^\varphi(n)=\varphi(n+h)-\varphi(n)$ and $d_h^a(n)=a_K(n+h)-a_K(n)$. Then

$$
\boxed{
|d_h^a(n)-d_h^\varphi(n)|
=|\eta(n+h)-\eta(n)|\le6.
}
\tag{17}
$$

This is **six**, not twelve, because the perturbations are all nonnegative.

For any finite terminal-index set $A$,

$$
\left|\sum_{N\in A}d_h^a(N+s)
-\sum_{N\in A}d_h^\varphi(N+s)\right|\le6|A|.
\tag{18}
$$

Thus *every* fixed-prime or composite-modulus signed source first moment of order $X^2$ is preserved to relative $o(1)$ on dyadic blocks, independent of the choice of residue classes or fixed h.

Consider the source-locked **actual WP09-G theorem**, with $h=1$, $s=L+1$, $Q=2^L$ and its full explicit gate:

$$
\boxed{
X\ge1024E_X^*,\quad E_X^*=3+\mathrm{bitlength}(3X),\quad
8(L+2)\le X,\quad Q\ge64X,\quad Q\ge16(2X+L+3).
}
\tag{19}
$$

Its two recurrence-ready terminal classes are

$$
S_j=\{X\le N\le2X-2:N+L+1\equiv j\pmod6\},
\quad j\in\{0,2\}.
\tag{20}
$$

For any coefficient sequence c let

$$
E_N^c=\exp(2\pi i D^c_{1,N,L}/Q),
\quad
U^c=
\mathrm{Im}\left[
\sum_{N\in S_0}E_{N+1}^c\overline{E_N^c}^{\,2}
-\sum_{N\in S_2}E_{N+1}^c\overline{E_N^c}^{\,2}
\right].
\tag{21}
$$

WP09-G proves **for the actual Euler totient** under (19) that

$$
U^\varphi\ge\frac{\pi X^2}{64Q}.
\tag{22}
$$

The exact full Cook sliding recurrence gives, for both c=a and c=phi,

$$
E_{N+1}^c\overline{E_N^c}^{\,2}
=\exp(2\pi i\,d_1^c(N+L+1)/Q).
\tag{23}
$$

Since $|e^{it}-e^{iu}|\le|t-u|$, (17) and $|S_0|+|S_2|\le X$ yield the **deterministic, genuinely modulo-one** comparison

$$
\boxed{
|U^{a_K}-U^\varphi|
\le\frac{12\pi X}{Q}.
}
\tag{24}
$$

**Theorem B (rational shadow inherits the true two-prime Fourier signature).** Under (19), for every $K\ge6$ with $X\ge3K$ and $X\ge1536$,

$$
\boxed{
U^{a_K}
\ge\frac{\pi X(X-768)}{64Q}
\ge\frac{\pi X^2}{128Q}>0.
}
\tag{25}
$$

At the cofinal legal choice $L=L_1(X)+1$, the WP09-G least-depth argument supplies $64X<Q<256X$ for every sufficiently large X. Hence the **rational dyadic shadow** satisfies

$$
\boxed{U^{a_K}\ge\frac{\pi X}{32768}.}
\tag{26}
$$

Yet the **same rational shadow** satisfies (13): **every one of its complete original Cook phases has real part greater than $0.9$** on these blocks.

This is a strong, quantitative failure of the proposed implication from *genuine two-prime, order-X imaginary cocycle information* to Cook's desired original-phase real cancellation. WP09-G distinguished the actual totient from its *specific parity-only* rational comparator, but **its stated leading Fourier signal is also shared by the much closer rational shadow (8)**.

The source contrasts themselves survive: WP09-G's full modulus-six arithmetic contrast $\ge X^2/32$ changes by at most $6X$ under (8), and its recurrence-ready contrast $\ge X^2/64$ changes by at most $6X$. In particular for sufficiently large X the rational shadow retains both positive $\Omega(X^2)$ source signatures. There is no probabilistic independence or finite-prime truncation in this argument. **This proves Theorem B.**

## 4. Theorem C: the logarithmic-time barrier for multistep cocycle amplification

For any h, full Cook depth L and $1\le k<X$, define the genuine k-step cocycle

$$
C^c_{N,k}
=E^c_{N+k}\overline{E_N^c}^{\,2^k}.
\tag{27}
$$

Iterating the **exact** full-Cook numerator identity gives

$$
\boxed{
C^c_{N,k}
=\exp\left(
\frac{2\pi i}{Q}
\sum_{i=0}^{k-1}2^{k-1-i}
d_h^c(N+L+1+i)
\right).
}
\tag{28}
$$

Use (17) term by term, and note $\sum_{i=0}^{k-1}2^{k-1-i}=2^k-1$. The unit-circle Lipschitz inequality yields, uniformly in N, X, h, and all legal L,

$$
\boxed{
|C^{a_K}_{N,k}-C^\varphi_{N,k}|
\le\frac{12\pi(2^k-1)}{Q}.
}
\tag{29}
$$

For **any externally specified** index subset $A\subset[X,2X-k)$ and bounded predetermined weights $|w_N|\le1$ independent of the coefficient sequence,

$$
\boxed{
\left|
\sum_{N\in A}w_N C^{a_K}_{N,k}
-\sum_{N\in A}w_N C^\varphi_{N,k}
\right|
\le\frac{12\pi|A|(2^k-1)}Q.
}
\tag{30}
$$

**Theorem C (bounded-step character indistinguishability).** Along least or near-least Cook depths $Q\asymp X$, for any $k=k(X)$ with $2^k=o(X)$, the **normalized** difference between every such weighted k-step cocycle sum for $\varphi$ and for the **dyadic-rational shadow** is $o(1)$. This includes fixed k, $k=O(\log\log X)$ and $k\le(1-\epsilon)\log_2X$ for fixed $\epsilon>0$. An analysis relying only on these bounded external-weight cocycle observables cannot distinguish the rational shadow sufficiently to establish Cook's ten-percent original-phase criterion.

The exact threshold where this deterministic error estimate ceases to be small is $2^k\asymp Q$, equivalently **k at logarithmic scale**. This is a **methodological sensitivity barrier**, not a proof that every technique shorter than that is impossible: coefficient-dependent Cook weights, full high-frequency characteristics, and multiplicativity can carry additional information absent from the theorem's hypotheses.

### Stronger fixed-frequency normalized-statistic stability

For each integer $n\ge X$,

$$
\left|\frac{a_K(n)}n-\frac{\varphi(n)}n\right|\le\frac6X.
\tag{31}
$$

For $m=m(X)$ nonnegative offsets $s_1,\ldots,s_m$, and any complex test F on the normalized m-tuple that is $\Lambda(X)$-Lipschitz in its $\ell^1$ argument, pointwise

$$
\left|
F\left(\frac{a_K(N+s_1)}{N+s_1},\ldots\right)
-
F\left(\frac{\varphi(N+s_1)}{N+s_1},\ldots\right)
\right|
\le\frac{6m\Lambda(X)}X.
\tag{32}
$$

Thus their normalized averages, including arbitrary fixed-prime residue conditioning with the *same counting denominator*, agree asymptotically whenever $m\Lambda=o(X)$. Finite-order fixed-frequency characteristics and normalized CRT moment tests are among these observables. A characteristic with frequency of order X, or original unnormalized Cook phases, is not controlled by (32). This is the **precise information loss** in WP09-E/G source projections.

## 5. Theorem D: exact multiplicativity destroys the rational shadow

The **true** totient is multiplicative on coprime arguments. A bounded correction need not be.

**Theorem D (uniform bounded-error multiplicative rigidity).** Suppose an integer-valued function b is multiplicative on coprime arguments and for a fixed finite B,

$$
|b(n)-\varphi(n)|\le B\quad\text{for all }n\ge1.
\tag{33}
$$

Then **$b(n)=\varphi(n)$ for every n**.

Indeed, write $\xi(n)=b(n)-\varphi(n)$. For any fixed n and prime $p\nmid n$,

$$
\begin{aligned}
\xi(np)
&=b(n)b(p)-\varphi(n)(p-1)\\
&=\xi(n)(p-1)+b(n)\xi(p).
\end{aligned}
\tag{34}
$$

Hence

$$
|\xi(n)|(p-1)\le B(1+|b(n)|).
\tag{35}
$$

There are arbitrarily large primes p not dividing n, so (35) forces $\xi(n)=0$ for every fixed n. No assumptions about the unknown value of the binary totient series are needed.

For the **specific** shadow $a_K$, all odd-prime values are literally unchanged: $a_K(p)=\varphi(p)=p-1$. Since $\delta_K>0$, at least one base-four digit $e_j$ is nonzero, so there is a modified even integer n with $\eta(n)\ge2$. For every odd prime $p\nmid n$, the **exact coprime multiplicativity defect** is

$$
\boxed{
a_K(np)-a_K(n)a_K(p)
=\eta(np)-\eta(n)(p-1),
}
\tag{36}
$$

and therefore

$$
\boxed{
|a_K(np)-a_K(n)a_K(p)|
\ge2(p-1)-6.
}
\tag{37}
$$

Thus the dyadic shadow can replicate arbitrarily many *leading* prime arithmetic and bounded-time modular Fourier signatures, but it necessarily incurs **unbounded exact multiplicative defects** along suitable coprime products. This is a concrete structural discriminator absent from the previous prime-projection framework.

**Important limitation:** Rigidity only eliminates false bounded shadows *if exact multiplicativity is actively enforced*. It does **not** show that multiplicativity by itself yields Cook's ten-percent real Fourier cancellation. A further quantitative bridge from such coprime-product relations to the **actual original-phase distribution** remains a mathematical obligation.

## 6. Reproducibility and numerical-proof separation

[bounded_dyadic_shadow.py](bounded_dyadic_shadow.py) computes the explicit rational target and **certifies finite base-four digit prefixes by two exact integer interval endpoints**. It makes no numerical assumption about the real number alpha. For any requested J, it sums the exact arithmetic tail through T and compares

$$
\left\lfloor\frac{A_T}{2^q}\right\rfloor,\quad
\left\lfloor\frac{A_T+T+2}{2^q}\right\rfloor,
\quad
A_T=\sum_{n=3K+1}^T(n-\varphi(n))2^{T-n},
\quad q=T-(2J+2K-1).
\tag{38}
$$

If the two floors coincide, their common value is **provably** $\lfloor4^Jx_K\rfloor$, with no floating approximation. If an interval straddles a digit boundary, the oracle expands T or fails closed; this computational issue does not affect the infinite existence theorem.

The exact verifier reconstructs $a_K(n)$ on a finite block, confirms the pointwise six-unit and parity/envelope constraints, the source difference and exact Cook recurrence, the centered phase bound (13) **by integer arithmetic**, and the exact dyadic target containment. Trigonometric calculations are optional finite diagnostics, never a substitute for the all-X proof. [WP09_H_CRITICAL_REVIEW.md](WP09_H_CRITICAL_REVIEW.md) separately records same-agent Axiomatist, Verifier, Adversary and Referee logical review.

All eight further hostile checks are appended to the existing policy-routed [tests/test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py); no separate CI lane or policy bypass is necessary.

| Statement | Proven status |
| --- | --- |
| Arbitrarily late, all-even six-unit actual-totient shadow with explicitly dyadic rational generating series | **PROVED**, Theorem A |
| Strong actual-WP09-G two-prime imaginary cocycle signal inherited by a rational shadow | **PROVED**, Theorem B |
| Full fixed-step and sublogarithmic-time cocycle-sum stability relative to actual totient | **PROVED**, Theorem C |
| Exact coprime multiplicativity excludes every nonzero uniformly bounded totient correction | **PROVED**, Theorem D |
| Strong Cook real phase saving for the **actual** Euler totient, source-locked 14X/25 weighted cofactor estimate, original Erdős #249 irrationality | **OPEN** |
| Independent human mathematical review, Lean formalization, MATHCERT certification | **NOT_CLAIMED / NOT_SUBMITTED** |

**Disposition and next true boundary.** WP09-H establishes that finite-prime and short-time modular diagnostics are *too stable under six-unit rationalization* to force ten-percent cancellation by themselves. A valid successor must exploit **exact multiplicativity across arbitrarily large coprime partners**, coefficient-level two-adic carries, or weighted characteristics at **frequencies of order X / logarithmic cocycle time**. More leading-moment or fixed-frequency prime evidence, without such an exact mechanism, cannot resolve the binary totient series.

Research issue #3500 and Erdős #249 remain OPEN. No MATHCERT.
