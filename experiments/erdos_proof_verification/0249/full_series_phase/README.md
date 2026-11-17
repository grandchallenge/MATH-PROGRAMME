# Erdős #249 — full-series moving-depth Fourier investigation 001

**Scope:** Original full series S, research only; NOT proof of irrationality, protected mathematical certification, or a reopening of the completed bounded auxiliary-T verification task #3205. Parent: [MATH-PROGRAMME #3201](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3201).

## Existing results and the actual open question

The open problem asks whether

$$
S=\sum_{n=1}^{\infty}\frac{\varphi(n)}{2^n}
$$

is irrational. The exact identity

$$
S=\frac12+\sum_{d\ge1}\frac{\mu(d)}{(2^d-1)^2}
$$

has already been established in Will Cook, *The Binary Totient Series* (revised October 2026). The same work includes finite denominator exclusions, tail-difference certificates, and unproved uniform harmonic estimates. These are **prior work, not claimed as original GCL discoveries**. See [the research record](https://wcook04.github.io/practical-formal-verification/maths/papers/erdos249-totient-reasoning-surface--chapter-024ee725701b.html) and [long-form paper](https://wcook04.github.io/practical-formal-verification/papers/erdos249-totient-reasoning-surface.pdf). Existing GCL source locks for the original statement are in [manifest 0249](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_proof_verification/manifests/0249.json). The completed Lean proof of the lacunary T series is strictly weaker than the open S problem.

## Theorem A — fixed-depth arithmetic phase collapse

For an integer N, fixed positive integer L, and real t, define

$$
U_{N,L}=\sum_{j=1}^{L}\frac{\varphi(N+j)}{2^j},
\qquad e(t)=\exp(2\pi i t).
$$

**A1: For every fixed positive k, the positive integers n with $2^k$ dividing $\varphi(n)$ have natural density one.**

**Proof.** For a fixed finite set P of distinct odd primes, let

$$
Z_P(n)=\sum_{p\in P}{\bf1}_{p\mid n},
\qquad m_P=\sum_{p\in P}\frac1p.
$$

By the Chinese remainder theorem, the divisibility indicators of these fixed primes, for n uniform on longer initial integer intervals, have a limiting joint law of independent Bernoulli variables of parameters $1/p$. Therefore the limiting mean of $Z_P$ is $m_P$ and its variance is at most $m_P$. If $m_P>k$, Chebyshev gives

$$
\limsup_{Y\to\infty}
\frac{\#\{1\le n\le Y:Z_P(n)<k\}}{Y}
\le\frac{m_P}{(m_P-k)^2}.
$$

Euler's divergence of the sum of reciprocal primes permits $m_P$ to increase without bound. Each distinct odd prime dividing n contributes a factor of 2 to the totient product formula, hence $Z_P(n)\ge k$ implies $2^k\mid\varphi(n)$. Taking arbitrarily large $m_P$ proves A1, including its density assertion.

**A2: For every fixed positive L,**

$$
\lim_{X\to\infty}
\sup_{h\in\mathbb Z}
\left|
\frac1X\sum_{N=X}^{2X-1}e(hU_{N,L})-1
\right|=0.
$$

**Proof.** By A1, for each j from 1 through L, the set of N for which $2^j$ does not divide $\varphi(N+j)$ has density zero. A finite union of such exceptions also has density zero. For all remaining N, every term $\varphi(N+j)/2^j$ is integral. Thus $e(hU_{N,L})=1$ for **all integers h simultaneously**. Each exceptional phase differs from 1 in absolute value by at most 2. Its average discrepancy is bounded by twice the exceptional fraction, independently of h. This proves A2.

**Interpretation:** Fixed-depth phases tend uniformly to 1 on long blocks and thus cannot exhibit the asymptotic cancellation required by full-series irrationality arguments. This is a methodological consequence of classical number-theoretic facts, **not a claimed new Erdős solution**. It says nothing about moving depths.

## Theorem B — the actual discarded tail is large at fixed depth

Define

$$
U_N=\sum_{j=1}^{\infty}\frac{\varphi(N+j)}{2^j}.
$$

Since $\varphi(n)\le n$, geometric summation gives

$$
0\le U_N-U_{N,L}\le\frac{N+L+2}{2^L}.
$$

For every positive integer n, the elementary factorization formula gives

$$
\varphi(n)^2\ge\frac n2.
$$

Indeed, for a prime power $p^a$, the ratio $\varphi(p^a)^2/p^a=p^{a-2}(p-1)^2$ is at least 1 for odd p and is at least $1/2$ for powers of 2. The product over distinct prime powers is therefore at least $1/2$. Keeping only the first omitted positive term in the tail yields

$$
U_N-U_{N,L}
\ge\frac{\sqrt{(N+L+1)/2}}{2^{L+1}}.
$$

For a fixed L this error grows without bound as N tends to infinity, even though A2 says the truncated phases tend to 1. To make the tail less than 1/4, it is necessary that $2^L>\sqrt{2(N+L+1)}$, so a moving depth of at least roughly one-half $\log_2N$ is unavoidable. The upper bound permits depth roughly $\log_2 N$ with a fixed safety margin. **The limits in X and truncation depth L cannot be naively interchanged.**

## Exact finite phase protocol

The full scaled tail satisfies

$$
2^NS=A_N+U_N,
\qquad A_N=\sum_{n=1}^{N}\varphi(n)2^{N-n}\in\mathbb Z.
$$

With $Q=2^L$, define the exactly integer-computable residue

$$
r_{N,L}=
\left(\sum_{j=1}^{L}\varphi(N+j)2^{L-j}\right)\bmod Q.
$$

Its sliding-window recurrence is

$$
r_{N+1,L}=(2r_{N,L}+\varphi(N+L+1))\bmod Q.
$$

The experiment computes the trigonometric average

$$
M_{h,X,L}=\frac1X\sum_{N=X}^{2X-1}
\exp(2\pi ih r_{N,L}/2^L)
$$

for integer harmonics h. The exact analytic bound on truncation-phase error is

$$
\left|M_{h,X,L}-
\frac1X\sum_{N=X}^{2X-1}e(hU_N)\right|
\le\frac{2\pi|h|(2X+L+2)}{2^L}.
$$

The residues and analytic bound are exact. Trigonometric evaluation is standard double precision, **not certified interval arithmetic**. If S were rational with denominator b, then $e(bU_N)=1$ for all N. Distinguishing the exact phase mean from 1 **for every possible b**, with a meaningful uniform arithmetic estimate, would rule out rationality. A bounded sweep of finite h and X does not do so. Cook's prior work already develops stronger unproved sufficient conditions.

## Actual finite computational results

An integer totient sieve (maximum argument 131121), exact rolling modular residues, and bounded double-precision trigonometric evaluation produced the following results with L = 48. The independent depth-stress fixture tests shorter L. These numbers are *finite observations*, not a theorem of cancellation as X grows.

| X | h range | Largest observed absolute phase average | Maximum analytic truncation-phase bound |
| ---: | ---: | ---: | ---: |
| 1,024 | 1–32 | 0.074307130 | 0.000000001499 |
| 4,096 | 1–32 | 0.032810778 | 0.000000005888 |
| 16,384 | 1–64 | 0.017717088 | 0.000000046885 |
| 65,536 | 1–64 | 0.007857192 | 0.000000187325 |

At L = 2 the observed fraction of exactly integral truncated tails rose from 0.889648438 for N in [1024, 2048) to 0.932693481 for N in [65536, 131072). At L = 4 it rose from 0.314453125 to 0.463867188. At L = 48 none of these finite tails was integral; its absolute upper tail error was less than one billionth in both blocks. These frequencies are consistent with A2 but do not establish its convergence rate.

### A necessary rational control

Use the integer coefficient sequence $a_n=2\lfloor n/2\rfloor$ (nonnegative, even, at most n). Its generating value is **rational**:

$$
C(x)=\sum_{n\ge1}a_n x^n
=\frac{2x^2(1+x)}{(1-x^2)^2},
\qquad C(1/2)=\frac43.
$$

For its exact scaled tails, $e(hU_N^{(C)})=e(h2^NC)$. At h = 3 this equals 1 for **all** N. At h = 1 the values alternate between the two nonreal cube roots of unity. On even-sized consecutive blocks their mean is **-1/2**, of modulus 1/2. Thus the statement "first harmonic mean strictly less than one implies irrationality" is **false**, even for a rational series with nonnegative, bounded-by-n, even coefficients. The moving-depth experiment reproduces the expected control values to its stated numerical precision. Tests explicitly reject any attempted single-harmonic inference.

## Evidence, tests, attribution and stopping boundary

Reproducible sources:

- **fourier_probe.py** — integer totient sieve, modular window recurrence and harmonic averages. SHA-256: eb79b8aeaeb89154e399d8940d8caafd8c1233dd9fa951ce89fd37c86d31ce67.
- **depth_stress.py** — the independent fixed/moving-depth matrix. SHA-256: ec5d97e50d3479cd22bb39aee38da3b9a21f741300a9784a59846483dc9a72b8.
- **test_fourier_probe.py** — exact-rational and modular hostile tests. SHA-256: aca481548ef34787aa7afc1852e1f38e717e1900b0a4d2138e078e69ce069cf6.

Actual run data SHA-256:

| JSON result | SHA-256 |
| --- | --- |
| result_1024.json | 6c907fb0245817d73c941da3b4a93aafbb00629ecdbccea1971279ee0b57e753 |
| result_4096.json | 0bf9d87df44bfcb045929ba0a84142761ac76a4fe3ddece4513906284bcb2e57 |
| result_16384.json | cc34b005e989debfba3c66c261d23749944c2d346c737ce54801e751e3ce5e6c |
| result_65536.json | a9da923c1b6bd73161de6b6295ed9ef7b822fc59d3627933918c68888f227caf |
| depth_stress_results.json | 368db4b6674c75b915fa103f8287d8347a6c07dc83b7ddf34afd5d5633201d33 |

The **six automated checks passed** after a deliberately caught Möbius-sieve bug in the test harness was corrected before admission. Checks include the totient sieve against direct gcd counting, the exact modular recurrence against independent direct sums, an exact-rational rational-series comparator, $2\varphi(n)^2\ge n$ for all n up to 132000, and the prior Möbius squared-Lambert identity using independent finite rational arithmetic plus explicit upper bounds for both tails. An isolated failure before correction is not recorded as a successful run.

To reproduce with Python 3, run the phase probe with X = 1024 or 4096 and H = 32, with X = 16384 or 65536 and H = 64, and in each case L = 48. Run depth_stress.py and the six-test unittest fixture. No GPU, external network or W&B account is needed. CPU and memory requirements are modest.

**Review provenance:** Theorem A and B have complete human-readable elementary arguments in this document. They are **not Lean-checked**; a separate human reviewer has not reviewed them, and theorem-level novelty has not been established. The elementary consequences of the classical normal order of prime factors and Euler's prime reciprocal divergence should not be relabeled as GCL discoveries. The Cook record already isolates the need for moving-depth and uniform arithmetic estimates; this experiment contributes an explicit fixed-depth incompatibility warning, control fixture and a bounded empirical pilot rather than an independent resolution.

**Next substantive obligation:** Find a provable moving-depth nonconcentration mechanism for the **actual totient sequence**, with a quantifier strong enough to exclude all rational denominators. Any proposed condition must be compared with Cook's already formalised conditional routes, independently falsified on the exact rational control, and checked at the necessary depth L growing with $\log_2 X$. Another finite range or more lacunary subseries irrationality theorems will not close this obligation. Original Erdős #249 remains **OPEN**, certification **NOT_SUBMITTED**.
