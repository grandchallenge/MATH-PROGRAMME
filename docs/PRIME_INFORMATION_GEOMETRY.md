# The Information Geometry of Prime Factorization
### A mathematical synthesis of entropy, Euler products, smooth numbers, and computational difficulty

**Grand Challenge Labs — manuscript draft 0.1 (11 October 2026).**  
**Status:** research exposition and internally derived mathematics; **not certified, not a novelty or publication claim**.  
**Related programme:** [TCU-001 uniform transition problem](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/prime-information/TRANSITION_TCU_001.md).

!!! info "Research status and authoritative records"
    **Status:** Working mathematical synthesis, not certified or asserted novel.  
    **Canonical tracker:** [PINFO-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2579).  
    **Open mathematical target:** [MATHSOLVE TCU-001](https://github.com/grandchallenge/MATHSOLVE/issues/1075).  
    **Protected source:** [Research manuscript](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/prime-information/MANUSCRIPT.md).  
    **Transition proof obligations:** [TCU-001](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/prime-information/TRANSITION_TCU_001.md).  
    The mathematical statements retain their recorded internal-review and conjectural statuses. Publication-quality rendering does not confer certification.

## Abstract

Unique prime factorization gives a lossless coordinate representation of positive integers, while bounded-size arithmetic makes the coordinates statistically dependent. We develop an accessible account of three different measures: the entropy of an integer, the total correlation of its prime-exponent vector, and the entropy of its normalized logarithmic factor weights. We introduce the independent geometric prime-factor ensemble arising from finite Euler products, give exact Kullback--Leibler decompositions and an exact exponential-slack conditioning construction, and organize the known and internally derived asymptotic regimes for smooth integers. The main open research problem is a two-sided, uniform saddle-point formula connecting the Dickman and sparse-prime descriptions. Throughout, arithmetic identity, probabilistic modeling, asymptotic inference, and computational factoring cost are kept separate.

## 1. A logarithm appears in two different places

The Prime Number Theorem states

$$
\pi(x)\sim \frac{x}{\log x},
$$

where $\pi(x)$ counts primes not exceeding $x$. Under a local random-integer heuristic the chance of primality near $x$ is roughly $1/\log x$. Its surprisal is therefore approximately $\log\log x$, not $\log x$.

For an integer selected uniformly from $\{1,\dots,m\}$, by contrast, the amount of information required to identify the integer is exactly $\log m$ nats. These are distinct experiments: asking *which integer?* and asking *is it prime?* are not the same question.

Logarithms occur naturally because multiplication becomes addition:

$$
n=\prod_p p^{v_p(n)}
\quad\Longrightarrow\quad
\log n=\sum_p v_p(n)\log p.
$$

The arithmetic weight $\log p$ is not automatically a Shannon entropy. It becomes an information-theoretic quantity only after a probability law is specified.

### 1.1 Prime Number Theorem as modular information capacity

Put $L(m)=\mathop{\mathrm{lcm}}(1,2,\dots,m)$ and $\psi(m)=\sum_{p^j\le m}\log p$. The elementary identity

$$
\log L(m)=\psi(m)
$$

follows by comparing the largest exponent of each prime appearing in the least common multiple. The classical Chebyshev formulation of PNT says

$$
\pi(x)\sim x/\log x
\quad\Longleftrightarrow\quad
\psi(x)\sim x.
$$

Thus $\log L(m)\sim m$. The cyclic group $\mathbb Z/L(m)\mathbb Z$ simultaneously resolves all congruences modulo every $a\le m$, so its uniform residue requires $\log L(m)$ nats to specify. This is a precise *modular capacity* interpretation; it is not the entropy of the distribution of individual primes.

The Riemann hypothesis is equivalent to the classical estimate

$$
\psi(x)-x=O\bigl(\sqrt{x}\log^2x\bigr).
$$

That statement constrains fluctuations of the modular capacity. We do not deduce a new result about RH from information theory.

## 2. Three notions of information: worked example

Take $n=360=2^3\,3^2\,5$. Its logarithmic size satisfies

$$
\log 360=3\log2+2\log3+\log5.
$$

If an integer $N$ is chosen uniformly from $\{1,\dots,m\}$, uniqueness of factorization implies

$$
H(N)=H\bigl((v_p(N))_{p\le m}\bigr)=\log m.
$$

This is **representation invariance**: knowing all prime exponents is exactly as informative as knowing $N$.

There are two other meaningful quantities:

**Total correlation** for a random vector $(V_p)$,

$$
T=\sum_pH(V_p)-H((V_p)_p)
=D\left(P_{(V_p)}\Big\Vert\bigotimes_pP_{V_p}\right).
$$

It measures dependence *across integers in an ensemble*. Even when each marginal looks nearly geometric, the global size constraint couples all coordinates.

**Internal factor entropy** for a *single integer* $n\ge2$,

$$
w_p(n)=\frac{v_p(n)\log p}{\log n},\qquad
S(n)=-\sum_{p\mid n}w_p(n)\log w_p(n).
$$

It measures how evenly that integer's logarithmic size is distributed across its distinct prime factors. For a prime power it is zero; for a product of several comparably sized prime contributions it is larger.

Neither $T$ nor $S(n)$ is an estimate of the time needed to compute the factorization.

## 3. Why Euler products generate independent random prime factors

Fix a finite prime cutoff $y\ge2$ and $s>0$. The finite Euler product is

$$
Z_y(s)=\prod_{p\le y}(1-p^{-s})^{-1}.
$$

It normalizes a probability law on all positive integers whose prime factors do not exceed $y$:

$$
Q_s(N=n)=n^{-s}/Z_y(s).
$$

If $V_p=v_p(N)$, then

$$
Q_s(V_p=j)=(1-p^{-s})p^{-sj},\qquad j=0,1,2,\ldots,
$$

and the different $V_p$ are **exactly independent**. Their energy contributions $V_p\log p$ add to $\log N$. In statistical mechanics, $Z_y(s)$ is a finite-prime partition function, and $s$ acts as an inverse temperature.

The expected logarithmic size and its variance are

$$
M_y(s)=\mathbb E_{Q_s}\log N=\sum_{p\le y}\frac{\log p}{p^s-1},
$$

$$
\sigma_y^2(s)=\mathop{\mathrm{Var}}_{Q_s}(\log N)
=\sum_{p\le y}\frac{(\log p)^2p^s}{(p^s-1)^2}.
$$

For the infinite Euler product $\zeta(s)$, normalizability requires $s>1$. The pole of $\zeta(s)$ at $1$ is an established analytic fact; it does not by itself imply PNT. The zeta statistical-mechanical analogy appears in earlier research, notably Golomb (1992) and Merhav (2026).

## 4. The actual smooth-number ensemble

Let

$$
S(X,y)=\{n\le X:P^+(n)\le y\},\quad
\Psi(X,y)=|S(X,y)|,\quad t=\log X,
$$

including the integer $1$, and draw $N$ uniformly from $S(X,y)$. Then

$$
\sum_{p\le y}V_p\log p\le t.
$$

The factor exponents are no longer independent. They compete for the same logarithmic budget. Their joint entropy is

$$
H((V_p)_{p\le y})=\log\Psi(X,y),
$$

and their total correlation is

$$
T(X,y)=\sum_{p\le y}H(V_p)-\log\Psi(X,y).
$$

### 4.1 Exact KL chain rule

For any $s>0$, compare the actual uniform ensemble $P$ with the independent geometric law $Q_s$. Define $P_p$ as its exponent marginals. Then:

$$
\boxed{
T(X,y)=D(P\Vert Q_s)-\sum_{p\le y}D(P_p\Vert Q_{p,s}).
}\tag{1}
$$

To prove it, expand

$$
D(P\Vert Q_s)
=\sum_{\mathbf v}P(\mathbf v)\log\frac{P(\mathbf v)}{\prod_pQ_{p,s}(v_p)}
$$

and insert and subtract $\sum_p\log P_p(v_p)$. The first resulting term is the total correlation, and the remaining terms are marginal KL divergences. No independence of the true exponents was assumed.

Since $Q_s(n)=n^{-s}/Z_y(s)$,

$$
\boxed{
D(P\Vert Q_s)=\log Z_y(s)+s\mathbb E_P[\log N]-\log\Psi(X,y).
}\tag{2}
$$

This is an exact information accounting identity, valid at every finite $X,y$.

### 4.2 An exact conditioning construction

Draw $N\sim Q_s$ and independently $W\sim\mathop{\mathrm{Exp}}(s)$. Put $E=\log N+W$. For $t>0$,

$$
f_{N,E}(n,t)=\frac{s e^{-st}}{Z_y(s)}\mathbf1_{\{\log n\le t\}},
$$

and hence the conditional law of $N$ given $E=t$ is *exactly uniform* on $S(e^t,y)$. Conditioning on a single continuous total-energy observation generates the entire smooth-number ensemble from independent prime factors. This uses a regular conditional density, not conditioning on a positive-probability point event.

The variable $W$ is unused logarithmic capacity. Its conditional mean is

$$
\Delta(X,y)=t-\mathbb E_P\log N.
$$

## 5. What is known about the different limits?

The parameters $X$ and $y$ can tend to infinity in different ways. It is an error to interchange those limits without uniformity.

### 5.1 All primes permitted: $y=X$

For $N$ uniform on $\{1,\dots,\lfloor X\rfloor\}$, classical Mertens estimates and the exact KL decomposition yield the author-derived asymptotic

$$
T(X,X)=\log\log X+\gamma-1+O(1/\log X)
$$

for integer $X\to\infty$. The previously prepared internal proof controls the summed marginal KL errors; it does **not** simply assume the exponents are independent. This derivation has not been independently certified.

### 5.2 Fixed set of permitted primes

Suppose $y$ is fixed and $k=\pi(y)$. Write $a_i=\log p_i$. Uniform smooth integers correspond to lattice points

$$
(v_1,\dots,v_k)\in\mathbb Z_{\ge0}^k,\qquad \sum_i a_iv_i\le t.
$$

After rescaling $w_i=a_iv_i/t$, these fill the solid simplex $\{w_i\ge0,\sum_iw_i\le1\}$. Each marginal coordinate of the limiting uniform simplex is $\mathop{\mathrm{Beta}}(1,k)$, with differential entropy

$$
h_k=-\log k+\frac{k-1}{k}.
$$

The joint simplex has volume $1/k!$. Subtracting joint from marginal entropies gives

$$
\boxed{
T(X,y)\longrightarrow C_k=\log(k!)-k\log k+k-1.
}\tag{3}
$$

In particular, $k=1$ gives $C_1=0$, and Stirling's formula gives $C_k=\frac12\log(2\pi k)-1+O(1/k)$ as $k\to\infty$. The finite-dimensional argument is documented in Working Note 002; novelty and independent validation are unestablished.

### 5.3 Fixed Dickman parameter

Write $X=y^u$ with fixed $u>1$ and let $y\to\infty$. The classical Dickman--de Bruijn asymptotic describes the number of smooth integers,

$$
\Psi(y^u,y)\sim y^u\rho(u),
$$

where $\rho(u)=1$ on $[0,1]$ and $u\rho'(u)=-\rho(u-1)$ for $u>1$.

Our internal Working Notes 003--005 derive a total-correlation expansion involving

$$
J(u)=\int_0^1\frac{a_u(v)\log a_u(v)-a_u(v)+1}{v}\,dv,
\qquad a_u(v)=\frac{\rho(u-v)}{\rho(u)}.
$$

The **fixed $u$ claim** is

$$
T(X,y)=\log\log y+\gamma-1-\log\rho(u)-J(u)+o(1).
$$

It is included as an internally supported research claim, not as a newly certified theorem. A stronger growing $u$ assertion in Note 005 needs a dedicated external or truly independent source-sensitive proof audit before promotion.

### 5.4 Many primes but an overwhelmingly large cutoff

Let $k=\pi(y)$ and $A=\sum_{p\le y}\log p$. The internal elementary simplex comparison in Working Note 007 states

$$
|T(X,y)-C_k|\le k\sqrt{R-1}+(k+1)\log R,\qquad R=(1+A/t)^k.
$$

Therefore, in the joint range $k\to\infty$ and $k^3A/t\to0$, it gives

$$
T(X,y)=\frac12\log(2\pi k)-1+o(1).
$$

This provides a separate two-sided regime, but does not settle the middle range where $y$ is too large for the volume comparison to be effective.

### 5.5 Why the transition matters

The fixed $u$ and sparse-prime formulas come from two very different representations. One organizes factors using the Dickman delay equation; the other uses high-dimensional simplex geometry. A single theorem would explain both as limits of the same conditioned independent system.

## 6. A single candidate transition theorem

Let $\alpha>0$ solve the *counting saddle-point equation*

$$
M_y(\alpha)=\log X.
$$

Hildebrand and Tenenbaum's classical uniform smooth-number estimate gives, as $u=\log X/\log y\to\infty$ and $y\to\infty$,

$$
\log\Psi(X,y)
=\alpha\log X+\log Z_y(\alpha)
-\log\!\bigl(\alpha\sqrt{2\pi\sigma_y^2(\alpha)}\bigr)
+O(1/u+\log y/y).
$$

Combining this with (1)--(2) yields

$$
\boxed{
T(X,y)=\log\!\bigl(\alpha\sqrt{2\pi\sigma_y^2(\alpha)}\bigr)
-\alpha\Delta-K_\alpha
+O(1/u+\log y/y),
}\tag{4}
$$

where $K_\alpha=\sum_{p\le y}D(P_p\Vert Q_{p,\alpha})$.

Thus there is one sharply framed conjectural bridge:

> As both $u$ and $y$ tend to infinity, can one prove uniformly that $\alpha\Delta\to1$ and $K_\alpha\to0$, with a quantitative error valid through the transition?

If so, then

$$
\boxed{
T(X,y)=\log\!\bigl(\alpha\sqrt{2\pi\sigma_y^2(\alpha)}\bigr)-1+o(1).
}\tag{5}
$$

**Equation (5) is a research target, not an established result.** It requires uniform local estimates, including a summable treatment of large prime powers, and a check for counterregimes. The exact leave-one-prime conditional likelihood formula and falsification obligations appear in [TCU-001](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/prime-information/TRANSITION_TCU_001.md).

The saddle point for counting is also not the parameter minimizing KL divergence to the actual uniform ensemble. The latter matches $\mathbb E_P\log N$, not the cutoff $\log X$; substituting one for the other without correcting the slack term would produce an incorrect sharp constant.

## 7. Internal factor entropy and universal random partitions

For an individual $n\ge2$, the weights $w_p(n)$ form a probability distribution over distinct prime factors. The mean of $S(N)$ for a large uniform integer has an internally checked limit of one nat. The classical antecedent is the Poisson--Dirichlet law for ranked logarithmic prime factors, established by Billingsley and developed via size-biased reordering by Donnelly--Grimmett (1993). Weak convergence alone does not prove convergence of expected entropy; the latter requires control of the small-factor tail. See Working Note 002 for the direct weighted-prime-sum argument.

Total correlation $T(X,y)$ and mean internal entropy $\mathbb E S(N)$ are different observables. One can grow slowly while the other converges to a finite constant. They must not be interchanged in an argument.

## 8. Does the framework help factor large integers?

Not by itself. Representing an integer through its prime exponents is lossless, but entropy invariance says nothing about the cost of *computing* those exponents. The framework could become algorithmically relevant if a dependence observable gives a demonstrably improved prediction of smooth-relation yield, diversity, or linear independence in a factoring pipeline. That requires an explicit benchmark against ordinary smooth-number predictions, not a verbal analogy or a claim of cryptographic impact.

## 9. Status ledger and proof obligations

| Claim | Support class | Open boundary |
|---|---|---|
| Euler-product geometric independence; KL chain rule; exponential slack | exact algebra | no mathematical certification implied |
| PNT / Chebyshev identity; Dickman and HT smooth-count theorems | classical imported mathematics | check exact source hypotheses when used |
| Unrestricted total correlation and one-nat mean entropy | author-derived proof, finite replays | independent mathematical and literature review |
| Fixed $y$ simplex constant and finite-error estimate | author-derived elementary proof | independent proof audit and priority check |
| Fixed $u$ and conservative growing $u$ Dickman KL laws | internal working proofs | check uniform summability and all error dependencies |
| Sparse-prime growing-dimensional bound | internal Working Note 007 | independent validation |
| Uniform saddle-point bridge, equation (5) | **conjectural** | quantitative slack estimate and summable leave-one-prime KL estimate |
| Faster factorization or RH consequences | **not established** | a separate theorem or benchmark would be required |

A successful manuscript should explain *what is established, what is finite evidence, what is author-derived, and what remains open* without promoting proof status merely through polished typesetting.

## 10. Conclusion

Prime factorization is a lossless change of coordinates, while the cutoff $\log N\le\log X$ imposes a shared resource constraint that creates statistical dependencies. Euler products supply independent geometric reference laws. Conditional probability and KL divergence measure exactly how the constrained arithmetic law departs from that reference. The main research problem is now to prove, or falsify in a controlled range, a single two-sided transition law that reconciles the geometric and analytic asymptotics. Computational factoring hardness is a separate question whose relation to the present observables remains to be demonstrated.

## References

1. S. W. Golomb, *Probability, information theory, and prime number theory*, Discrete Mathematics 106--107 (1992), 219--229. https://doi.org/10.1016/0012-365X(92)90549-U .
2. A. Hildebrand and G. Tenenbaum, *Integers without large prime factors*, Journal de Théorie des Nombres de Bordeaux 5 (1993), 411--484. https://doi.org/10.5802/jtnb.101 .
3. P. Donnelly and G. Grimmett, *On the asymptotic distribution of large prime factors*, Journal of the London Mathematical Society 47 (1993), 395--404. https://doi.org/10.1112/jlms/s2-47.3.395 .
4. I. Kontoyiannis, *Some information-theoretic computations related to the distribution of prime numbers* (2007), https://arxiv.org/abs/0710.4076 .
5. G. Tenenbaum, *Sur le biais d'une loi de probabilité relative aux entiers friables*, JTNB 35 (2023), 481--493. https://doi.org/10.5802/jtnb.1253 .
6. T. Tao, *Smooth numbers and max-entropy* (2025), https://terrytao.wordpress.com/2025/09/15/smooth-numbers-and-max-entropy/ .
7. N. Merhav, *Statistical Physics of Coding for the Integers* (2026), https://arxiv.org/abs/2604.00858 .

**Provenance:** GCL local Research Notes 001--007 and internal Adjudication 004 were produced on 2026-10-11, with source hashes for the latest packets listed in [provenance record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/prime-information/README.md). The present manuscript integrates but does not supersede their detailed proof records.
