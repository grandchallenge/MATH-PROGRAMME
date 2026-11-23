# Erdős #249 — WP09-I: an optimal two-unit parity-preserving rational shadow

**Scientific issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Immediate predecessor:** WP09-H [PR #3648](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3648), six-unit shadow which additionally leaves *every odd coefficient* unchanged.  
**Original source lock:** Will Cook, *The Binary Totient Series*, [revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac.  
**Claim scope:** sharp pointwise two-unit parity-preserving *rational comparator*, preserved higher-prime Cook cocycle signals and a finite-step stability barrier. The original Euler-totient irrationality, Cook's full real 10% saving, and weighted prime/cofactor cancellation remain OPEN. MATHCERT NOT_SUBMITTED.

## 1. Main theorem: only two units of correction suffice

Let

$$
\alpha=\sum_{n=1}^\infty\frac{\varphi(n)}{2^n}
$$

be the actual binary totient series. Fix any integer $K\ge6$, set $M=3K$, and define the **explicit dyadic rational**

$$
\boxed{
\gamma_K=\sum_{n=1}^{M}\frac{\varphi(n)}{2^n}
=\frac1{2^M}\sum_{n=1}^M\varphi(n)2^{M-n}.
}
\tag{1}
$$

The true arithmetic tail

$$
\delta_K=\alpha-\gamma_K
=\sum_{n>M}\frac{\varphi(n)}{2^n}
\tag{2}
$$

is strictly positive and at most $(M+2)/2^M$. Define

$$
B_K=2^{1-K},
\qquad
x_K=\delta_K/B_K
=2^{K-1}\sum_{n>3K}\frac{\varphi(n)}{2^n}.
\tag{3}
$$

The envelope $\varphi(n)\le n$ gives

$$
\boxed{0<x_K\le\frac{3K+2}{2^{2K+1}}<1.}
\tag{4}
$$

Let the **canonical floor bits** of this explicit convergent arithmetic tail be

$$
b_j=\lfloor 2^jx_K\rfloor
-2\lfloor2^{j-1}x_K\rfloor\in\{0,1\},
\qquad j\ge1.
\tag{5}
$$

For *every* positive integer n, define the shadow sequence

$$
\boxed{
a_K(n)=
\begin{cases}
\varphi(n),&n\le K,\\
\varphi(n)-2b_{n-K},&n>K.
\end{cases}
}
\tag{6}
$$

**Theorem A (sharp parity-preserving rationalization).** For every $K\ge6$:

1. $a_K(n)$ is integer-valued, satisfies $0\le a_K(n)\le n$ and

$$
\boxed{\lvert a_K(n)-\varphi(n)\rvert\le2\quad\text{for every }n.}
\tag{7}
$$

2. $a_K(n)=\varphi(n)$ for **all** $n\le K$. For all $n\ge3$, both $a_K(n)$ and $\varphi(n)$ are even.
3. The **entire infinite binary series** is exactly the displayed rational $\gamma_K$:

$$
\boxed{
\sum_{n\ge1}\frac{a_K(n)}{2^n}
=\alpha-2^{1-K}\sum_{j=1}^\infty b_j2^{-j}
=\alpha-2^{1-K}x_K
=\gamma_K\in2^{-3K}\mathbb Z.
}
\tag{8}
$$

4. For **every** $h\ge1$, every integer $X\ge3K$ and **every** Cook-admissible depth $L\ge h$ with

$$
Q=2^L\ge16(2X+h+L+2),
\tag{9}
$$

each original complete Cook phase for the sequence $a_K$ satisfies

$$
\boxed{
\left\|D^{a_K}_{h,N,L}/Q\right\|_{\mathbb R/\mathbb Z}
<1/16,\qquad
\mathrm{Re}\exp(2\pi iD^{a_K}_{h,N,L}/Q)
>\cos(\pi/8)>9/10
}
\tag{10}
$$

for **every** $X\le N<2X$.

5. The constant **two** is **optimal among nontrivial parity-preserving integer perturbations**: if an integer sequence differs from $\varphi$ at some index $n\ge3$ and preserves even parity for every $n\ge3$, that difference is a nonzero even integer and hence has magnitude at least two. Since $\delta_K>0$, at least one bit $b_j=1$, so our construction attains this sharp uniform threshold.

Thus the original Cook real tenth-saving can fail on *every* late legal block for a sequence within the **smallest possible nonzero parity-compatible integer distance** of the actual Euler totient.

### Complete proof of Theorem A

Equation (4) follows from $\sum_{n>M}n/2^n=(M+2)/2^M$; its last inequality holds at $K=6$ and becomes stronger with increasing K.

The telescoping floor identity yields

$$
\sum_{j=1}^J b_j2^{-j}
=2^{-J}\lfloor2^Jx_K\rfloor\longrightarrow x_K.
\tag{11}
$$

Because $n>K\ge6$, all modified indices satisfy $n\ge7$. For every $n\ge3$, the genuine totient is a positive even integer, so $\varphi(n)\ge2$ and subtracting either zero or two preserves the coefficient bounds, parity and integrality. Equation (8) follows exactly by substituting (11).

For each $N\ge M$ the **infinite** single-offset tail is an integer:

$$
R_N^{a_K}
=\sum_{j=1}^\infty\frac{a_K(N+j)}{2^j}
=2^N\gamma_K-\sum_{n=1}^Na_K(n)2^{N-n}
\in\mathbb Z,
\tag{12}
$$

since $2^M\gamma_K$ is integral and $N\ge M$. Therefore the infinite shifted-difference tail
$R_{N+h}^{a_K}-R_N^{a_K}$ is an integer.

The full Cook numerator is $D^{a_K}_{h,N,L}=\sum_{j=1}^L2^{L-j}[a_K(N+h+j)-a_K(N+j)]$. With $0\le a_K(n)\le n$,

$$
\left|
R_{N+h}^{a_K}-R_N^{a_K}
-\frac{D^{a_K}_{h,N,L}}Q
\right|
\le\sum_{j>L}\frac{N+h+j}{2^j}
=\frac{N+h+L+2}{Q}<\frac1{16}
\tag{13}
$$

under (9) and $N<2X$. Centering modulo an integer proves (10). This is an all-X analytical proof, not a finite numerical extrapolation.

For example, the entirely finite original-totient prefix through $M=24$ gives the exact **two-unit shadow target**

$$
\boxed{\gamma_8=\frac{5736255}{4194304}.}
\tag{14}
$$

There is **no assumption and no inference** that $\alpha$ itself is rational.

## 2. Theorem B: the genuine two-prime WP09-G Fourier signal survives at two-unit distance

Let $\eta(n)=a_K(n)-\varphi(n)\in\{-2,0\}$. The difference of shifted source differences is much smaller than the WP09-H six-unit version:

$$
\boxed{
|\,[a_K(n+h)-a_K(n)]
-[\varphi(n+h)-\varphi(n)]\,|
=|\eta(n+h)-\eta(n)|\le2.
}
\tag{15}
$$

Every finite-prime or composite-modulus leading signed source moment involving sums over $O(X)$ terminal indices changes by at most $2X$. Every bounded-order fixed-frequency Lipschitz characteristic of normalized values changes by $O(1/X)$.

Now choose the genuine WP09-G setting: $h=1$, $s=L+1$, $Q=2^L$, $E_X^*=3+\mathrm{bitlength}(3X)$ and

$$
X\ge1024E_X^*,\qquad
8(L+2)\le X,\qquad
Q\ge64X,\qquad
Q\ge16(2X+L+3).
\tag{16}
$$

Let

$$
S_j=\{N\in[X,2X-1):N+L+1\equiv j\pmod6\},
\quad j\in\{0,2\},
\tag{17}
$$

and write $E_N^c=\exp(2\pi iD^c_{1,N,L}/Q)$ for c equal to either $\varphi$ or $a_K$. Define the actual complete-Cook *imaginary cocycle contrast*

$$
U^c=
\mathrm{Im}\left(
\sum_{N\in S_0}E_{N+1}^c\overline{E_N^c}^{\,2}
-
\sum_{N\in S_2}E_{N+1}^c\overline{E_N^c}^{\,2}
\right).
\tag{18}
$$

Protected WP09-G proves for **actual Euler totient**, without any randomization,

$$
U^\varphi\ge\frac{\pi X^2}{64Q}.
\tag{19}
$$

Cook's **exact full numerator** cocycle is

$$
E_{N+1}^c\overline{E_N^c}^{\,2}
=\exp\!\left(\frac{2\pi i}{Q}[c(N+L+2)-c(N+L+1)]\right).
\tag{20}
$$

Using $|e^{it}-e^{iu}|\le|t-u|$, (15) and $|S_0|+|S_2|\le X$ gives

$$
\boxed{
|U^{a_K}-U^\varphi|\le\frac{4\pi X}{Q}.
}
\tag{21}
$$

**Theorem B (the actual two-prime signal is parity-shadow invariant).** Under (16), $K\ge6$, $X\ge3K$ and $X\ge512$,

$$
\boxed{
U^{a_K}
\ge\frac{\pi X(X-256)}{64Q}
\ge\frac{\pi X^2}{128Q}>0.
}
\tag{22}
$$

At the legal near-minimum Cook depth $L=L_1(X)+1$, the protected WP09-G bound $Q<256X$ yields for every sufficiently large X

$$
\boxed{
U^{a_K}\ge\frac{\pi X}{32768}.
}
\tag{23}
$$

**This is an order-X, genuine two-prime imaginary cocycle signature in an explicitly dyadic-rational coefficient sequence.** Simultaneously, (10) proves every one of that sequence's original Cook real phases exceeds $0.9$. Therefore even with the optimal parity-preserving coefficient perturbation, the WP09-G imaginary signature cannot alone force Cook's original real tenth-saving.

### Difference from the WP09-H comparator

WP09-H provides a **six-unit** rational shadow that preserves **every odd coefficient including all odd primes exactly**. WP09-I achieves the **sharp two-unit distance** and keeps every coefficient's even parity, but **may change odd-prime coefficients by two**. They establish complementary limits: one preserves a larger exact source set, the other is optimally close pointwise.

## 3. Theorem C: sharpened multistep Fourier stability threshold

For an integer shift h, define the true complete k-step Cook cocycle

$$
C_{N,k}^c
=E_{N+k}^c\overline{E_N^c}^{\,2^k},
\qquad k\ge1.
\tag{24}
$$

The full sliding recurrence gives the exact identity

$$
C_{N,k}^c
=\exp\left(
\frac{2\pi i}{Q}
\sum_{i=0}^{k-1}2^{k-1-i}
[c(N+L+h+1+i)-c(N+L+1+i)]
\right).
\tag{25}
$$

Since the source differences of $\varphi$ and $a_K$ differ by at most **two**, the total perturbation in this weighted numerator is bounded by $2(2^k-1)$. The elementary unit-circle chord inequality proves

$$
\boxed{
|C_{N,k}^{a_K}-C_{N,k}^\varphi|
\le\frac{4\pi(2^k-1)}Q.
}
\tag{26}
$$

For any prescribed set $A$ of at most X sources and any **externally chosen** weights $|w_N|\le1$ which do not depend on the coefficients,

$$
\boxed{
\left|\sum_{N\in A}w_N(C_{N,k}^{a_K}-C_{N,k}^\varphi)\right|
\le\frac{4\pi|A|(2^k-1)}Q.
}
\tag{27}
$$

At Cook depths $Q\asymp X$, normalized differences vanish for all $k$ with $2^k=o(X)$, including every fixed k, $k=O(\log\log X)$, or $k\le(1-\epsilon)\log_2X$ with fixed $\epsilon>0$. Thus **even an optimally close parity-preserving rational sequence cannot be separated from the genuine totient using these short-time external-weight cocycles at leading order**.

The logarithmic threshold is **precisely the sensitivity limit of this comparison bound**, not a universal negative theorem about arguments incorporating exact multiplicativity, coefficient-dependent weights or high-frequency carry information.

For normalized values $a_K(n)/n$ and $\varphi(n)/n$, the corresponding fixed-frequency sensitivity bound is improved to $2m\Lambda/X$ for an m-coordinate test with $\ell^1$ Lipschitz constant $\Lambda$, along offsets at indices n≥X.

## 4. Theorem D: exact arithmetic rigidity still eliminates the sharp comparator

WP09-H proved the general lemma: a globally bounded perturbation of the actual totient which retains **exact coprime multiplicativity** must equal the totient identically.

For this two-unit comparator, the exact defect is quantitative. At least one index n>K has $\eta(n)=-2$ because the positive tail (2) has at least one nonzero binary digit. For every prime p not dividing that n, with $\varphi(p)=p-1$,

$$
a_K(np)-a_K(n)a_K(p)
=\eta(np)-\eta(n)(p-1)-a_K(n)\eta(p).
\tag{28}
$$

Since $|\eta(np)|,|\eta(p)|\le2$ and $0\le a_K(n)\le n$,

$$
\boxed{
|a_K(np)-a_K(n)a_K(p)|
\ge2(p-1)-2(n+1).
}
\tag{29}
$$

In particular this defect grows at least linearly with p along primes $p\nmid n$. Exact coprime multiplicativity, in contrast to fixed-prime normalized moments, detects the rational shadow decisively.

**This does not prove the original irrationality problem.** No link has yet been proved from the actual totient's multiplicativity to a real complete-Cook harmonic of at most $0.9X$. The theorem identifies the **arithmetic information that a successful next proof must use**, or an equally sensitive exact alternative.

## 5. Deterministic, exact-source finite checks

[two_unit_parity_shadow.py](two_unit_parity_shadow.py) computes the rational target (1), generates the **certified first J binary digits of (3)** from an exact totient divisor sieve and a mathematically valid tail interval, constructs the finite coefficient sequence, and verifies the original Cook phases using centered *integer* residues, direct numerator oracles and the exact dyadic target.

For

$$
A_T=\sum_{n=3K+1}^T\varphi(n)2^{T-n},
\quad q=T-(J+K-1),
$$

the integer bounds

$$
\boxed{
\left\lfloor\frac{A_T}{2^q}\right\rfloor
\le\lfloor2^Jx_K\rfloor
\le\left\lfloor\frac{A_T+T+2}{2^q}\right\rfloor
}
\tag{30}
$$

certify the first J bits if the two endpoints coincide. They use only the exact tail envelope $\sum_{n>T}\varphi(n)2^{-n}\le(T+2)/2^T$, with **no evaluation or presumption of irrationality of alpha**. An unresolved boundary is explicitly rejected by the finite oracle; the infinite floor definition remains valid regardless.

The governing tests are appended to [tests/test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py), rather than creating another CI route. The same-agent logically separate Axiomatist, Verifier, Adversary and Referee challenges are documented in [WP09_I_CRITICAL_REVIEW.md](WP09_I_CRITICAL_REVIEW.md); they are **not** independently authenticated review.

### Claim boundaries

| Obligation | Disposition |
| --- | --- |
| Explicit dyadic-rational even-parity comparator with optimal uniform coefficient error exactly two | **PROVED** |
| All late real complete-Cook phases of that comparator remain above 0.9, for every h | **PROVED** |
| Genuine two-prime actual-totient WP09-G imaginary cocycle signal persists in the comparator at order X | **PROVED** |
| Short-time k-step cocycle/finite-prime normalized observables are insensitive to this bounded perturbation | **PROVED under stated externally weighted scope** |
| Exact coprime multiplicativity detects the comparator with an unbounded defect | **PROVED** |
| Strong 10% real Cook harmonic, weighted 14X/25 prime/cofactor estimate, original Erdős #249 irrationality | **OPEN** |
| Independent human mathematical certification, Lean proof, MATHCERT | **NOT_SUBMITTED** |

**Scientific next boundary:** establish a *multiplicativity-sensitive two-adic carry-escape estimate* for the actual Euler totient, or the exact weighted cofactor estimate in Cook's source. Mere finite-prime moments or bounded-time cocycle signatures cannot resolve the open problem, even when the comparator differs from the true totient by the **smallest parity-compatible integer amount**.
